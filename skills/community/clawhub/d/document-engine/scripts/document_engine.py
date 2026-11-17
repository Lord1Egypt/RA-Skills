"""企业级文书合规审计引擎 · 单文件版（Document Engine）。

纯规则库、零第三方依赖、可离线运行。仅使用 Python 标准库。
核心能力：
- 通用多类型文书审计（合同 contract / 制度 regulation / 公文 official_doc / 通用 generic）
- 条款级规则扫描 + 文档级审计（要素完整性 / 一致性 / 权利义务对等 / 公文格式）
- 责任闭环锚定与全链路可追溯
- HTML / JSON / Markdown 三格式报告

用法：
    python document_engine.py audit --type contract --input 合同.txt --output 报告.html
    python document_engine.py audit --type regulation --input 制度.txt --format json
    python document_engine.py list-rules --type contract
    python document_engine.py demo
    python document_engine.py audit --type contract --input 合同.txt --rules-dir ./my_rules

规则库内嵌于本文件（_EMBEDDED_RULES），亦可用 --rules-dir 指向外部 JSON 规则目录覆盖。
全部判定为决定论式（命中即判定），不输出概率估计。
"""

import argparse
import json
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import bisect

__version__ = "1.0.0"

# =============================================================================
# 核心数据模型
# =============================================================================


class RiskLevel(Enum):
    SAFE = auto()
    WARNING = auto()
    CRITICAL = auto()
    FATAL = auto()


class NodeStatus(Enum):
    RAW = auto()
    SCANNED = auto()
    AUDITED = auto()
    PRUNED = auto()
    ACTIVE = auto()


class DocType(Enum):
    CONTRACT = "contract"
    REGULATION = "regulation"
    OFFICIAL_DOC = "official_doc"
    GENERIC = "generic"

    @classmethod
    def from_str(cls, s: str) -> "DocType":
        try:
            return cls(s.strip().lower())
        except ValueError:
            return cls.GENERIC


@dataclass
class TraceLog:
    timestamp: str
    operation: str
    stage: str
    node_id: Optional[str]
    remark: str
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @staticmethod
    def now(operation: str, stage: str, node_id: Optional[str], remark: str) -> "TraceLog":
        return TraceLog(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            operation=operation,
            stage=stage,
            node_id=node_id,
            remark=remark,
        )


@dataclass
class ResponsibilityAccount:
    """责任闭环锚定：每项审计动作绑定到具名责任节点（组织/角色/阶段）。"""

    organization: str
    role: str
    stage: str
    nonce: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    trace_chain: List[str] = field(default_factory=list)

    def bind_stage(self, stage: str) -> bool:
        self.trace_chain.append(f"{stage}|{uuid.uuid4().hex[:6]}")
        return True


@dataclass
class AuditFinding:
    rule_id: str
    category: str
    severity: RiskLevel
    message: str
    suggestion: str
    location: str
    snippet: str
    confidence: float = 1.0
    offset: int = -1


@dataclass
class AuditNode:
    """文书中的审计单元：一条条款 / 一个段落 / 一个制度条目。"""

    node_id: str
    content: str
    section: str = ""
    findings: List[AuditFinding] = field(default_factory=list)
    status: NodeStatus = NodeStatus.RAW
    score: float = 100.0
    start: int = 0
    end: int = 0


@dataclass
class AuditReport:
    doc_type: DocType
    title: str
    overall_score: float
    passed: bool
    findings: List[AuditFinding]
    nodes: List[AuditNode]
    trace: List[TraceLog]
    responsibility: ResponsibilityAccount
    summary: Dict[str, Any]
    generated_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )


# =============================================================================
# 内嵌规则库（与原 rules/*.json 等价，可用 --rules-dir 外部覆盖）
# =============================================================================

_EMBEDDED_RULES: List[Dict[str, Any]] = [
    # ---- generic（common.json）----
    {
        "id": "COM-001",
        "scope": "generic",
        "category": "用词规范",
        "severity": "WARNING",
        "kind": "risk_keywords",
        "patterns": ["及时", "尽快", "适当", "酌情", "视情况", "等"],
        "message": "存在模糊时间/程度词，责任边界不清",
        "suggestion": "改为可量化的时限或标准",
    },
    {
        "id": "COM-002",
        "scope": "generic",
        "category": "风险条款",
        "severity": "CRITICAL",
        "kind": "risk_keywords",
        "patterns": ["概不负责", "最终解释权", "概不退换", "不承担任何责任"],
        "message": "单方免责条款，可能被认定无效",
        "suggestion": "删除或改为双方对等责任条款",
    },
    {
        "id": "COM-003",
        "scope": "generic",
        "category": "用词规范",
        "severity": "WARNING",
        "kind": "risk_keywords",
        "patterns": ["绝对", "百分之百", "永不", "一切"],
        "message": "绝对化用语，易引发歧义或承诺过载",
        "suggestion": "替换为限定性表述",
    },
    # ---- contract（contract.json）----
    {
        "id": "CT-001",
        "scope": "contract",
        "category": "风险条款",
        "severity": "CRITICAL",
        "kind": "risk_keywords",
        "patterns": ["最终解释权", "概不负责", "单方解除", "无条件", "免责"],
        "message": "存在单方优势或免责条款",
        "suggestion": "调整为双方对等条款",
    },
    {
        "id": "CT-002",
        "scope": "contract",
        "category": "合规红线",
        "severity": "FATAL",
        "kind": "regex",
        "pattern": "最低工资.{0,8}(低于|不足)",
        "message": "劳动报酬条款可能违反最低工资标准",
        "suggestion": "核对当地最低工资标准",
    },
    {
        "id": "CT-003",
        "scope": "contract",
        "category": "合规红线",
        "severity": "FATAL",
        "kind": "regex",
        "pattern": "违约金.{0,10}(超过|高于).{0,4}(30%|百分之三十)",
        "patterns": [
            "违约金.{0,10}(超过|高于).{0,4}(30%|百分之三十)",
            "违约金.{0,12}(3[1-9]|[4-9][0-9]|100)\\s*%",
        ],
        "message": "违约金比例可能超过法定上限",
        "suggestion": "违约金不超过实际损失的30%",
    },
    {
        "id": "CT-004",
        "scope": "contract",
        "category": "合规红线",
        "severity": "FATAL",
        "kind": "regex",
        "pattern": "加班.{0,8}(无补偿|不支付|没有加班费)",
        "message": "加班无补偿条款违反劳动法",
        "suggestion": "按法定标准支付加班费",
    },
    {
        "id": "CT-005",
        "scope": "contract",
        "category": "风险条款",
        "severity": "CRITICAL",
        "kind": "risk_keywords",
        "patterns": ["押金", "保证金"],
        "message": "押金/保证金条款需明确返还条件与时限",
        "suggestion": "补充返还条件、时限与利息约定",
    },
    # ---- regulation（regulation.json）----
    {
        "id": "RG-001",
        "scope": "regulation",
        "category": "职责权限",
        "severity": "WARNING",
        "kind": "risk_keywords",
        "patterns": ["相关部门", "有关人员", "视情况"],
        "message": "职责主体不明确",
        "suggestion": "明确到具体部门或岗位",
    },
    {
        "id": "RG-002",
        "scope": "regulation",
        "category": "合规红线",
        "severity": "CRITICAL",
        "kind": "risk_keywords",
        "patterns": ["未经审批", "自行决定", "擅自"],
        "message": "存在未经审批即可执行的权限漏洞",
        "suggestion": "补充审批流程与权限边界",
    },
    {
        "id": "RG-003",
        "scope": "regulation",
        "category": "风险条款",
        "severity": "WARNING",
        "kind": "risk_keywords",
        "patterns": ["有权", "可以自行"],
        "message": "权限表述宽泛，需界定边界",
        "suggestion": "明确权限范围与限制条件",
    },
    # ---- official_doc（official_doc.json）----
    {
        "id": "OD-001",
        "scope": "official_doc",
        "category": "格式规范",
        "severity": "CRITICAL",
        "kind": "regex",
        "pattern": "\\d{4}[./-]\\d{1,2}[./-]\\d{1,2}",
        "message": "日期格式不规范",
        "suggestion": "使用「YYYY年MM月DD日」格式",
    },
    {
        "id": "OD-002",
        "scope": "official_doc",
        "category": "格式规范",
        "severity": "WARNING",
        "kind": "regex",
        "pattern": "请示[^。]{0,20}(报告|汇报)",
        "message": "请示与报告文种混用",
        "suggestion": "请示用于请求指示，报告用于汇报工作",
    },
    {
        "id": "OD-003",
        "scope": "official_doc",
        "category": "用词规范",
        "severity": "WARNING",
        "kind": "risk_keywords",
        "patterns": ["大概", "大约", "差不多"],
        "message": "公文用词含糊",
        "suggestion": "使用精确数字与表述",
    },
]


# =============================================================================
# 规则引擎
# =============================================================================


def _parse_severity(s: str) -> RiskLevel:
    try:
        return RiskLevel[s.strip().upper()]
    except KeyError:
        return RiskLevel.WARNING


def _snippet_at(text: str, idx: int, length: int, radius: int = 18) -> str:
    if idx < 0:
        return ""
    start = max(0, idx - radius)
    end = min(len(text), idx + length + radius)
    return text[start:end]


class RuleEngine:
    """加载规则库并按文书类型匹配。

    默认使用内嵌规则（_EMBEDDED_RULES）；传入 rules_dir 时从该目录
    读取 *.json 规则文件（格式与原 compliance_engine/rules/*.json 相同）。
    匹配为决定论式：命中即产出 finding，不输出概率。
    """

    def __init__(self, rules_dir: Optional[Path] = None):
        self.rules: List[Dict[str, Any]] = []
        if rules_dir is not None:
            self.rules_dir = Path(rules_dir)
            self._load_all()
        else:
            self.rules = [dict(r) for r in _EMBEDDED_RULES]

    def _load_all(self) -> None:
        if not self.rules_dir.is_dir():
            raise FileNotFoundError(f"规则目录不存在: {self.rules_dir}")
        for f in sorted(self.rules_dir.glob("*.json")):
            self._load_file(f)

    def _load_file(self, path: Path) -> None:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        file_scope = data.get("doc_type")
        for rule in data.get("rules", []):
            rule = dict(rule)
            scope = rule.get("scope") or file_scope or "generic"
            rule["scope"] = scope
            self.rules.append(rule)

    def rules_for(self, doc_type: DocType) -> List[Dict[str, Any]]:
        return [r for r in self.rules if r.get("scope") in (doc_type.value, "generic")]

    def list_rules(self, doc_type: Optional[DocType] = None) -> List[Dict[str, Any]]:
        if doc_type is None:
            return list(self.rules)
        return self.rules_for(doc_type)

    def scan(self, text: str, doc_type: DocType) -> List[AuditFinding]:
        """对整篇文书做条款级扫描，返回全部命中 finding。"""
        findings: List[AuditFinding] = []
        for rule in self.rules_for(doc_type):
            findings.extend(self._apply(rule, text))
        return findings

    def _apply(self, rule: Dict[str, Any], text: str) -> List[AuditFinding]:
        kind = rule.get("kind", "risk_keywords")
        severity = _parse_severity(rule.get("severity", "WARNING"))
        if kind == "risk_keywords":
            return self._match_keywords(rule, text, severity)
        if kind == "forbidden_keywords":
            return self._match_keywords(rule, text, severity)
        if kind == "regex":
            return self._match_regex(rule, text, severity)
        return []

    def _match_keywords(
        self, rule: Dict[str, Any], text: str, severity: RiskLevel
    ) -> List[AuditFinding]:
        findings: List[AuditFinding] = []
        for kw in rule.get("patterns", []):
            if not kw:
                continue
            start = 0
            while True:
                idx = text.find(kw, start)
                if idx < 0:
                    break
                findings.append(
                    AuditFinding(
                        rule_id=rule["id"],
                        category=rule.get("category", "风险条款"),
                        severity=severity,
                        message=rule.get("message", f"命中风险词「{kw}」"),
                        suggestion=rule.get("suggestion", ""),
                        location="全文",
                        snippet=_snippet_at(text, idx, len(kw)),
                        offset=idx,
                    )
                )
                start = idx + len(kw)
        return findings

    def _match_regex(
        self, rule: Dict[str, Any], text: str, severity: RiskLevel
    ) -> List[AuditFinding]:
        findings: List[AuditFinding] = []
        patterns = rule.get("patterns") or [rule.get("pattern", "")]
        matches = []
        for raw in patterns:
            if not raw:
                continue
            try:
                pat = re.compile(raw)
            except re.error:
                continue
            for m in pat.finditer(text):
                matches.append((m.start(), m.group(0)))
        matches.sort(key=lambda x: x[0])
        seen = set()
        for pos, value in matches:
            if pos in seen:
                continue
            seen.add(pos)
            findings.append(
                AuditFinding(
                    rule_id=rule["id"],
                    category=rule.get("category", "格式规范"),
                    severity=severity,
                    message=rule.get("message", f"命中模式「{value}」"),
                    suggestion=rule.get("suggestion", ""),
                    location="全文",
                    snippet=_snippet_at(text, pos, len(value)),
                    offset=pos,
                )
            )
        return findings


# =============================================================================
# 文档级审计器：要素完整性 / 一致性 / 权利义务对等 / 公文格式
# =============================================================================

# 各文书类型的必备要素（关键词组，全部缺失任一即告警）
_COMPLETENESS: Dict[DocType, List[Dict[str, object]]] = {
    DocType.CONTRACT: [
        {"name": "当事人", "keywords": ["甲方", "乙方", "当事人"]},
        {"name": "标的", "keywords": ["标的", "项目", "服务", "货物", "产品"]},
        {"name": "价款", "keywords": ["价款", "金额", "费用", "价格", "报酬"]},
        {"name": "履行期限", "keywords": ["期限", "日期", "时间", "交付", "完成"]},
        {"name": "违约责任", "keywords": ["违约"]},
        {"name": "争议解决", "keywords": ["争议", "仲裁", "诉讼", "法院", "管辖"]},
    ],
    DocType.REGULATION: [
        {"name": "目的", "keywords": ["目的", "为规范", "为加强", "为进一步"]},
        {"name": "适用范围", "keywords": ["适用范围", "适用于", "本办法", "本制度"]},
        {"name": "职责", "keywords": ["职责", "负责", "承担"]},
        {"name": "流程", "keywords": ["流程", "程序", "步骤", "办理"]},
        {"name": "罚则", "keywords": ["罚则", "处罚", "奖惩", "责任追究", "考核"]},
        {"name": "生效条款", "keywords": ["生效", "施行", "发布之日起", "自发布"]},
    ],
    DocType.OFFICIAL_DOC: [
        {"name": "标题", "keywords": ["关于"]},
        {"name": "主送机关", "keywords": ["各", "单位", "部门", "处室"]},
        {"name": "成文日期", "keywords": ["年", "月", "日"]},
        {"name": "文号", "keywords": ["〔", "["]},
    ],
    DocType.GENERIC: [],
}

_ASSIGN_RE = re.compile(
    r"([\u4e00-\u9fa5]{2,8})(?:为|是|：)([0-9]{2,}[年月日元%]|[一二三四五六七八九十百千]+[年月日元%])"
)

_PARTY_RIGHT_RE = re.compile(r"(甲方|乙方)(?:有权|可|可以|应)")
_PARTY_DUTY_RE = re.compile(r"(甲方|乙方)(?:应|须|应当|有义务)")


class CompletenessAuditor:
    """要素完整性：必备要素缺失即告警（决定论：缺失=命中）。"""

    def audit(self, text: str, doc_type: DocType) -> List[AuditFinding]:
        findings: List[AuditFinding] = []
        for item in _COMPLETENESS.get(doc_type, []):
            name = item["name"]
            keywords = item["keywords"]
            if not any(k in text for k in keywords):
                findings.append(
                    AuditFinding(
                        rule_id=f"COMPLETE-{doc_type.value}",
                        category="要素完整性",
                        severity=RiskLevel.CRITICAL,
                        message=f"缺少必备要素：{name}",
                        suggestion=f"补充「{name}」相关内容（如：{' / '.join(keywords[:3])}）",
                        location="全文",
                        snippet="",
                    )
                )
        return findings


class ConsistencyAuditor:
    """一致性：同一赋值短语出现多次但取值不同 → 前后矛盾。"""

    def audit(self, text: str, doc_type: DocType) -> List[AuditFinding]:
        groups: Dict[str, List[str]] = {}
        for m in _ASSIGN_RE.finditer(text):
            key, val = m.group(1), m.group(2)
            groups.setdefault(key, []).append(val)
        findings: List[AuditFinding] = []
        for key, vals in groups.items():
            unique = list(dict.fromkeys(vals))
            if len(unique) > 1:
                findings.append(
                    AuditFinding(
                        rule_id=f"CONSIST-{doc_type.value}",
                        category="一致性",
                        severity=RiskLevel.CRITICAL,
                        message=f"「{key}」前后取值矛盾：{' / '.join(unique)}",
                        suggestion="核对并统一为单一取值",
                        location="全文",
                        snippet=f"{key}为{' / '.join(unique)}",
                    )
                )
        return findings


class BalanceAuditor:
    """权利义务对等（合同）：甲方权利词显著多于乙方 → 失衡。"""

    def audit(self, text: str, doc_type: DocType) -> List[AuditFinding]:
        if doc_type != DocType.CONTRACT:
            return []
        rights = {"甲方": 0, "乙方": 0}
        for m in _PARTY_RIGHT_RE.finditer(text):
            rights[m.group(1)] += 1
        duties = {"甲方": 0, "乙方": 0}
        for m in _PARTY_DUTY_RE.finditer(text):
            duties[m.group(1)] += 1
        imbalance = rights["甲方"] - rights["乙方"]
        findings: List[AuditFinding] = []
        if imbalance >= 2:
            findings.append(
                AuditFinding(
                    rule_id="BALANCE-CONTRACT",
                    category="权利义务对等",
                    severity=RiskLevel.WARNING,
                    message=(
                        f"权利义务失衡：甲方权利表述 {rights['甲方']} 处，"
                        f"乙方 {rights['乙方']} 处（差 {imbalance}）"
                    ),
                    suggestion="检查是否存在单方优势条款，补充乙方对等权利",
                    location="全文",
                    snippet=f"甲方有权×{rights['甲方']} / 乙方有权×{rights['乙方']}",
                )
            )
        return findings


class FormatAuditor:
    """公文格式：文号缺失、落款缺失。"""

    def audit(self, text: str, doc_type: DocType) -> List[AuditFinding]:
        if doc_type != DocType.OFFICIAL_DOC:
            return []
        findings: List[AuditFinding] = []
        if "〔" not in text and "[" not in text:
            findings.append(
                AuditFinding(
                    rule_id="FORMAT-OFFICIAL",
                    category="格式规范",
                    severity=RiskLevel.CRITICAL,
                    message="缺少公文文号（如：×发〔2026〕×号）",
                    suggestion="补充规范文号",
                    location="标题下方",
                    snippet="",
                )
            )
        if not re.search(r"\d{4}年\d{1,2}月\d{1,2}日", text):
            findings.append(
                AuditFinding(
                    rule_id="FORMAT-OFFICIAL",
                    category="格式规范",
                    severity=RiskLevel.WARNING,
                    message="缺少成文日期（YYYY年MM月DD日）",
                    suggestion="在落款处补充成文日期",
                    location="落款",
                    snippet="",
                )
            )
        return findings


# =============================================================================
# 主引擎：编排审计流程、责任闭环锚定、评分与报告组装
# =============================================================================

_SECTION_RE = re.compile(r"^(第[一二三四五六七八九十百千0-9]+[条款]|[0-9]+[.、．]|[一二三四五六七八九十]+[、．])")


class ComplianceEngine:
    """流程：分节 → 规则扫描 → 文档级审计 → 责任闭环 → 评分 → 报告。"""

    def __init__(self, rules_dir: Optional[Path] = None):
        self.rule_engine = RuleEngine(rules_dir)
        self.account = ResponsibilityAccount(
            organization="Compliance-Core",
            role="ComplianceAuditor",
            stage="audit",
        )
        self.trace: List[TraceLog] = []

    def audit(
        self,
        text: str,
        doc_type: DocType,
        title: str = "",
    ) -> AuditReport:
        self.trace = []
        self.account.bind_stage("audit")
        self._log("START", None, f"启动审计：{doc_type.value}")

        nodes = self._segment(text)
        self._log("SEGMENT", None, f"文书分节完成：{len(nodes)} 个审计单元")

        findings: List[AuditFinding] = []
        findings.extend(self.rule_engine.scan(text, doc_type))
        self._log("RULE_SCAN", None, f"规则扫描命中：{len(findings)} 条")

        findings.extend(CompletenessAuditor().audit(text, doc_type))
        findings.extend(ConsistencyAuditor().audit(text, doc_type))
        findings.extend(BalanceAuditor().audit(text, doc_type))
        findings.extend(FormatAuditor().audit(text, doc_type))
        self._log("DOC_AUDIT", None, f"文档级审计完成：累计 {len(findings)} 条")

        findings = self._dedup(findings)
        self._attach_to_nodes(findings, nodes)

        score = self._score(findings)
        passed = score >= 60 and not any(
            f.severity in (RiskLevel.FATAL, RiskLevel.CRITICAL) for f in findings
        )
        summary = self._summarize(findings)
        self._log("SCORE", None, f"评分 {score:.0f}，判定 {'通过' if passed else '不通过'}")

        return AuditReport(
            doc_type=doc_type,
            title=title or "未命名文书",
            overall_score=score,
            passed=passed,
            findings=findings,
            nodes=nodes,
            trace=list(self.trace),
            responsibility=self.account,
            summary=summary,
        )

    # ---------- 内部流程 ----------
    def _segment(self, text: str) -> List[AuditNode]:
        nodes: List[AuditNode] = []
        current: List[str] = []
        current_section = "开头"
        block_start = -1
        block_end = 0
        pos = 0

        def flush():
            nonlocal current, block_start, block_end
            if current:
                nodes.append(
                    AuditNode(
                        node_id=f"N{len(nodes) + 1:03d}",
                        content="\n".join(current),
                        section=current_section,
                        status=NodeStatus.SCANNED,
                        start=max(block_start, 0),
                        end=block_end,
                    )
                )
                current = []
                block_start = -1

        for raw in text.splitlines(keepends=True):
            line_start = pos
            pos += len(raw)
            ln = raw.strip()
            if not ln:
                continue
            m = _SECTION_RE.match(ln)
            if m:
                flush()
                current_section = m.group(0).strip()
            if block_start < 0:
                block_start = line_start
            block_end = pos
            current.append(ln)
        flush()
        return nodes

    def _attach_to_nodes(self, findings: List[AuditFinding], nodes: List[AuditNode]) -> None:
        if not nodes:
            return
        starts = [n.start for n in nodes]
        for f in findings:
            if not f.snippet:
                continue
            node = None
            if f.offset >= 0:
                i = bisect.bisect_right(starts, f.offset) - 1
                if i >= 0 and f.offset < nodes[i].end:
                    node = nodes[i]
            if node is None:
                for candidate in nodes:
                    if f.snippet in candidate.content:
                        node = candidate
                        break
            if node is not None:
                node.findings.append(f)
                node.status = NodeStatus.AUDITED

    def _dedup(self, findings: List[AuditFinding]) -> List[AuditFinding]:
        seen = set()
        out: List[AuditFinding] = []
        for f in findings:
            key = (f.rule_id, f.message, f.snippet)
            if key in seen:
                continue
            seen.add(key)
            out.append(f)
        return out

    def _score(self, findings: List[AuditFinding]) -> float:
        score = 100.0
        for f in findings:
            if f.severity == RiskLevel.WARNING:
                score -= 5
            elif f.severity == RiskLevel.CRITICAL:
                score -= 15
            elif f.severity == RiskLevel.FATAL:
                score -= 30
        return max(0.0, score)

    def _summarize(self, findings: List[AuditFinding]) -> Dict[str, object]:
        by_severity: Dict[str, int] = {}
        by_category: Dict[str, int] = {}
        for f in findings:
            by_severity[f.severity.name] = by_severity.get(f.severity.name, 0) + 1
            by_category[f.category] = by_category.get(f.category, 0) + 1
        return {
            "total_findings": len(findings),
            "by_severity": by_severity,
            "by_category": by_category,
        }

    def _log(self, operation: str, node_id: Optional[str], remark: str) -> None:
        self.trace.append(
            TraceLog.now(operation=operation, stage="audit", node_id=node_id, remark=remark)
        )


# =============================================================================
# 报告生成：HTML（可视化）/ JSON（结构化）/ Markdown（简洁）
# =============================================================================

_SEV_COLOR = {
    RiskLevel.FATAL: "#dc2626",
    RiskLevel.CRITICAL: "#ea580c",
    RiskLevel.WARNING: "#d97706",
    RiskLevel.SAFE: "#16a34a",
}
_SEV_LABEL = {
    RiskLevel.FATAL: "致命",
    RiskLevel.CRITICAL: "严重",
    RiskLevel.WARNING: "警告",
    RiskLevel.SAFE: "安全",
}


def to_dict(report: AuditReport) -> Dict[str, Any]:
    return {
        "doc_type": report.doc_type.value,
        "title": report.title,
        "overall_score": report.overall_score,
        "passed": report.passed,
        "generated_at": report.generated_at,
        "summary": report.summary,
        "responsibility": {
            "organization": report.responsibility.organization,
            "role": report.responsibility.role,
            "stage": report.responsibility.stage,
            "trace_chain": report.responsibility.trace_chain,
        },
        "findings": [
            {
                "rule_id": f.rule_id,
                "category": f.category,
                "severity": f.severity.name,
                "message": f.message,
                "suggestion": f.suggestion,
                "location": f.location,
                "snippet": f.snippet,
            }
            for f in report.findings
        ],
        "trace": [
            {
                "timestamp": t.timestamp,
                "operation": t.operation,
                "stage": t.stage,
                "node_id": t.node_id,
                "remark": t.remark,
            }
            for t in report.trace
        ],
    }


def to_json(report: AuditReport) -> str:
    return json.dumps(to_dict(report), ensure_ascii=False, indent=2)


def to_markdown(report: AuditReport) -> str:
    lines = [
        f"# 文书合规审计报告：{report.title}",
        "",
        f"- 文书类型：{report.doc_type.value}",
        f"- 综合评分：{report.overall_score:.0f} / 100",
        f"- 判定：{'通过' if report.passed else '不通过'}",
        f"- 审计时间：{report.generated_at}",
        f"- 责任节点：{report.responsibility.organization} / {report.responsibility.role}",
        "",
        "## 汇总",
        "",
        f"- 发现总数：{report.summary.get('total_findings', 0)}",
        f"- 按严重度：{_fmt_dict(report.summary.get('by_severity', {}))}",
        f"- 按维度：{_fmt_dict(report.summary.get('by_category', {}))}",
        "",
        "## 问题清单",
        "",
    ]
    if not report.findings:
        lines.append("未发现合规问题。")
    for f in sorted(report.findings, key=lambda x: x.severity.value):
        lines.append(
            f"- **[{_SEV_LABEL[f.severity]}] {f.category}** {f.message}"
            f"\n  - 位置：{f.location} | 命中：`{f.snippet or '—'}`"
            f"\n  - 建议：{f.suggestion}"
        )
    lines += ["", "## 审计追溯链", ""]
    for t in report.trace:
        lines.append(f"- `{t.timestamp}` {t.operation} | {t.remark}")
    return "\n".join(lines)


def to_html(report: AuditReport) -> str:
    sev_counts = report.summary.get("by_severity", {})
    cards = "".join(
        f'<span class="sev sev-{s.name.lower()}" style="background:{_SEV_COLOR[s]}">{_SEV_LABEL[s]} {sev_counts.get(s.name, 0)}</span>'
        for s in (RiskLevel.FATAL, RiskLevel.CRITICAL, RiskLevel.WARNING)
    )
    findings_html = ""
    for f in sorted(report.findings, key=lambda x: x.severity.value):
        findings_html += f"""
<div class="finding sev-{f.severity.name.lower()}">
  <div class="f-head">
    <span class="badge" style="background:{_SEV_COLOR[f.severity]}">{_SEV_LABEL[f.severity]}</span>
    <strong>{f.category}</strong>
    <span class="rule">{f.rule_id}</span>
  </div>
  <p class="f-msg">{f.message}</p>
  <p class="f-snip">命中：<code>{f.snippet or '—'}</code></p>
  <p class="f-loc">位置：{f.location}</p>
  <p class="f-sug">建议：{f.suggestion}</p>
</div>"""
    if not findings_html:
        findings_html = '<div class="finding sev-safe"><p class="f-msg">未发现合规问题。</p></div>'
    trace_html = "".join(
        f"<li><code>{t.timestamp}</code> {t.operation} — {t.remark}</li>"
        for t in report.trace
    )
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>文书合规审计报告 · {report.title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; margin: 0; background: #f4f5f7; color: #1f2937; }}
.wrap {{ max-width: 900px; margin: 0 auto; padding: 32px 20px; }}
h1 {{ font-size: 24px; border-bottom: 3px solid #2563eb; padding-bottom: 12px; }}
.meta {{ display: flex; gap: 24px; flex-wrap: wrap; margin: 16px 0; color: #4b5563; font-size: 14px; }}
.score-box {{ background: #fff; border-radius: 12px; padding: 20px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
.score {{ font-size: 42px; font-weight: 700; color: #2563eb; }}
.verdict {{ font-size: 16px; font-weight: 600; }}
.verdict.pass {{ color: #16a34a; }} .verdict.fail {{ color: #dc2626; }}
.sev {{ color: #fff; padding: 3px 10px; border-radius: 12px; font-size: 13px; margin-right: 8px; }}
h2 {{ font-size: 18px; margin-top: 28px; }}
.finding {{ background: #fff; border-radius: 10px; padding: 14px 16px; margin: 10px 0; box-shadow: 0 1px 3px rgba(0,0,0,.06); border-left: 5px solid #9ca3af; }}
.finding.sev-fatal {{ border-left-color: #dc2626; }} .finding.sev-critical {{ border-left-color: #ea580c; }}
.finding.sev-warning {{ border-left-color: #d97706; }} .finding.sev-safe {{ border-left-color: #16a34a; }}
.f-head {{ display: flex; align-items: center; gap: 10px; }}
.badge {{ color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 12px; }}
.rule {{ color: #9ca3af; font-size: 12px; }}
.f-msg {{ margin: 8px 0 4px; font-weight: 600; }}
.f-snip, .f-loc, .f-sug {{ margin: 3px 0; font-size: 13px; color: #4b5563; }}
code {{ background: #f3f4f6; padding: 1px 6px; border-radius: 4px; }}
ul.trace {{ background: #fff; border-radius: 10px; padding: 16px 16px 16px 36px; box-shadow: 0 1px 3px rgba(0,0,0,.06); font-size: 13px; color: #4b5563; }}
</style>
</head>
<body>
<div class="wrap">
<h1>文书合规审计报告 · {report.title}</h1>
<div class="meta">
  <span>类型：{report.doc_type.value}</span>
  <span>责任节点：{report.responsibility.organization} / {report.responsibility.role}</span>
  <span>时间：{report.generated_at}</span>
</div>
<div class="score-box">
  <div class="score">{report.overall_score:.0f}<span style="font-size:16px;color:#9ca3af"> / 100</span></div>
  <div class="verdict {'pass' if report.passed else 'fail'}">判定：{'通过' if report.passed else '不通过'}</div>
  <div style="margin-top:10px">{cards}</div>
</div>
<h2>问题清单（{report.summary.get('total_findings', 0)}）</h2>
{findings_html}
<h2>审计追溯链</h2>
<ul class="trace">{trace_html}</ul>
</div>
</body>
</html>"""


def _fmt_dict(d: Dict[str, Any]) -> str:
    return "、".join(f"{k}={v}" for k, v in d.items()) if d else "无"


# =============================================================================
# 内置演示：三份含合规问题的示例文书（合同 / 制度 / 公文）
# =============================================================================

SAMPLES: Dict[DocType, tuple] = {
    DocType.CONTRACT: (
        "示例采购合同",
        """采购合同

甲方：星辰科技有限公司
乙方：云帆供应链有限公司

第一条 合同标的
甲方向乙方采购办公设备一批，标的为办公设备及配套服务。

第二条 价款与支付
合同总价款为人民币200000元。甲方应于验收合格后30日内支付。
乙方应于收到款项后5日内开具发票。

第三条 履行期限
乙方应于2026年9月30日前完成交付。

第四条 违约责任
违约金为50000元。
若乙方逾期交付，违约金为80000元。
乙方加班无补偿，需自行安排进度。

第五条 争议解决
因本合同产生的争议，双方协商解决；协商不成的，提交甲方所在地人民法院诉讼。

第六条 其他
本合同最终解释权归甲方所有。
甲方有权调整交付计划，甲方有权变更验收标准，甲方有权单方解除合同。
乙方应尽快完成交付。""",
    ),
    DocType.REGULATION: (
        "示例差旅费用管理制度",
        """差旅费用管理制度

第一章 总则
第一条 目的
为规范公司差旅费用管理，加强费用控制，特制定本制度。

第二条 适用范围
本制度适用于公司全体员工。

第二章 职责与流程
第三条 职责
财务部负责差旅费用的审核与报销，行政部负责差旅审批。

第四条 报销流程
员工出差前须提交出差申请，经审批后出差；出差结束后提交报销单据，财务部在5个工作日内完成审核。

第五条 权限
相关部门可自行决定差旅标准，财务部有权调整报销比例。

第三章 罚则
第六条 责任追究
对虚报差旅费用的员工，视情况给予警告或处罚。

第七条 生效
本制度自发布之日起施行。""",
    ),
    DocType.OFFICIAL_DOC: (
        "关于申请采购办公设备的请示",
        """关于申请采购办公设备的请示

星辰科技〔2026〕12号

各部门：

为满足公司业务发展需要，拟采购办公设备一批，预算约人民币50万元，交付时间大约在2026.8.18前后，特此请示。

妥否，请批示。

星辰科技有限公司
2026年8月18日""",
    ),
}


def run_demo(out_dir: Path, doc_type: Optional[DocType] = None) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    engine = ComplianceEngine()

    for dt, (title, text) in SAMPLES.items():
        if doc_type is not None and dt != doc_type:
            continue
        report = engine.audit(text, dt, title)
        base = out_dir / f"demo_{dt.value}"
        (out_dir / f"{base.name}.html").write_text(to_html(report), encoding="utf-8")
        (out_dir / f"{base.name}.json").write_text(to_json(report), encoding="utf-8")
        (out_dir / f"{base.name}.md").write_text(to_markdown(report), encoding="utf-8")

        print(f"\n===== {title} [{dt.value}] =====")
        print(f"评分：{report.overall_score:.0f}/100 | 判定：{'通过' if report.passed else '不通过'}")
        print(f"发现：{report.summary['total_findings']} 条 | 严重度分布：{report.summary['by_severity']}")
        for f in report.findings:
            print(f"  [{f.severity.name}] {f.category} | {f.message}")
        print(f"报告：{base.name}.html / .json / .md")

    print("\n演示完成。")


# =============================================================================
# CLI 入口：audit / list-rules / demo
# =============================================================================


def _read_input(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"输入文件不存在: {p}")
    return p.read_text(encoding="utf-8")


def _write_output(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")
    print(f"报告已写入: {path}")


def cmd_audit(args: argparse.Namespace) -> int:
    text = _read_input(args.input)
    doc_type = DocType.from_str(args.type)
    engine = ComplianceEngine(rules_dir=Path(args.rules_dir) if args.rules_dir else None)
    report = engine.audit(text, doc_type, title=args.title or Path(args.input).stem)

    fmt = args.format
    if args.output:
        fmt = fmt or ("html" if args.output.endswith(".html") else "json")
    fmt = fmt or "html"

    if fmt == "json":
        content = to_json(report)
    elif fmt == "md":
        content = to_markdown(report)
    else:
        content = to_html(report)

    if args.output:
        _write_output(args.output, content)
    else:
        print(content)
    return 0


def cmd_list_rules(args: argparse.Namespace) -> int:
    engine = ComplianceEngine(rules_dir=Path(args.rules_dir) if args.rules_dir else None)
    doc_type = DocType.from_str(args.type) if args.type else None
    rules = engine.rule_engine.list_rules(doc_type)
    for r in rules:
        print(
            f"{r['id']:<16} [{r.get('scope','generic'):<12}] {r.get('severity','WARNING'):<8} "
            f"{r.get('category','')} — {r.get('message','')}"
        )
    print(f"\n共 {len(rules)} 条规则")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir) if args.output_dir else Path.cwd()
    run_demo(out_dir, doc_type=DocType.from_str(args.type) if args.type else None)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="document_engine",
        description="企业级文书合规审计引擎（纯规则库，零依赖，可离线）",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="审计一份文书")
    p_audit.add_argument("--type", required=True, choices=[t.value for t in DocType],
                         help="文书类型")
    p_audit.add_argument("--input", required=True, help="输入文书文件路径（UTF-8）")
    p_audit.add_argument("--title", default="", help="文书标题（默认取文件名）")
    p_audit.add_argument("--format", choices=["html", "json", "md"], default=None,
                         help="输出格式（默认 html；指定 --output 时按扩展名推断）")
    p_audit.add_argument("--output", default="", help="输出文件路径")
    p_audit.add_argument("--rules-dir", default="", help="自定义规则目录")
    p_audit.set_defaults(func=cmd_audit)

    p_list = sub.add_parser("list-rules", help="列出规则库")
    p_list.add_argument("--type", default="", choices=[t.value for t in DocType],
                        help="按类型过滤")
    p_list.add_argument("--rules-dir", default="", help="自定义规则目录")
    p_list.set_defaults(func=cmd_list_rules)

    p_demo = sub.add_parser("demo", help="运行内置演示（生成示例报告）")
    p_demo.add_argument("--type", default="", choices=[t.value for t in DocType],
                        help="仅演示指定类型")
    p_demo.add_argument("--output-dir", default="", help="报告输出目录（默认当前目录）")
    p_demo.set_defaults(func=cmd_demo)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
