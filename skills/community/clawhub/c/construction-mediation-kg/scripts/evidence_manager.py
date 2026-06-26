# 证据管理系统
# 度量衡商事调解智库 - 证据链自动归集与审查

import os
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 枚举定义
# ============================================================

class EvidenceType(Enum):
    """证据类型"""
    CONTRACT = "合同文件"
    CHANGE_ORDER = "变更签证"
    PAYMENT_PROOF = "付款凭证"
    CORRESPONDENCE = "往来函件"
    INSPECTION_REPORT = "验收报告"
    QUALITY_REPORT = "质量鉴定报告"
    ENGINEERING_LOG = "施工日志"
    PHOTO_VIDEO = "照片/视频"
    EXPERT_OPINION = "专家意见"
    OTHER = "其他"


class EvidenceStatus(Enum):
    """证据状态"""
    SUBMITTED = "已提交"
    VERIFIED = "已验证"
    DISPUTED = "有争议"
    REJECTED = "已排除"


class EvidenceWeight(Enum):
    """证据效力"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


# ============================================================
# 数据结构
# ============================================================

@dataclass
class EvidenceItem:
    """证据条目"""
    evidence_id: str
    case_id: str
    evidence_type: str
    
    name: str
    description: str
    submitter: str      # 提交方
    submit_date: str
    
    # 文件信息
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    file_size: Optional[int] = None
    
    # 审查信息
    status: str = EvidenceStatus.SUBMITTED.value
    weight: str = EvidenceWeight.MEDIUM.value
    relevance: str = ""      # 与争议焦点关联
    authenticity: str = ""   # 真实性说明
    validity: str = ""       # 合法性/关联性/证明力
    
    # 备注
    notes: str = ""


@dataclass
class EvidenceChain:
    """证据链"""
    chain_id: str
    case_id: str
    dispute_point: str    # 对应的争议焦点
    
    evidence_ids: List[str]
    chain_logic: str     # 证据链逻辑说明
    conclusion: str       # 基于证据链的结论
    strength: str         # 证据链强度评估


# ============================================================
# 证据管理器
# ============================================================

class EvidenceManager:
    """
    证据管理系统
    
    功能：
    1. 证据提交与登记
    2. 证据审查与分类
    3. 证据链构建
    4. 证据清单自动生成
    5. 证据目录导出
    """
    
    def __init__(self, data_dir: str = "./evidence_data"):
        self.data_dir = data_dir
        self.evidences: Dict[str, EvidenceItem] = {}
        self.chains: Dict[str, EvidenceChain] = {}
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_data(self):
        """加载数据"""
        filepath = os.path.join(self.data_dir, "evidences.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for e in data.get("evidences", []):
                    ev = EvidenceItem(**e)
                    self.evidences[ev.evidence_id] = ev
    
    def _save_data(self):
        """保存数据"""
        filepath = os.path.join(self.data_dir, "evidences.json")
        data = {
            "evidences": [asdict(e) for e in self.evidences.values()]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _calculate_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        if not os.path.exists(file_path):
            return ""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    # ========== 证据操作 ==========
    
    def submit_evidence(self,
                       case_id: str,
                       evidence_type: str,
                       name: str,
                       description: str,
                       submitter: str,
                       file_path: Optional[str] = None,
                       notes: str = "") -> EvidenceItem:
        """
        提交证据
        
        Args:
            case_id: 案件ID
            evidence_type: 证据类型
            name: 证据名称
            description: 证据描述
            submitter: 提交方
            file_path: 文件路径（可选）
            notes: 备注
            
        Returns:
            创建的证据对象
        """
        evidence_id = f"EV-{case_id}-{len(self.evidences)+1:03d}"
        
        file_hash = None
        file_size = None
        if file_path and os.path.exists(file_path):
            file_hash = self._calculate_hash(file_path)
            file_size = os.path.getsize(file_path)
        
        evidence = EvidenceItem(
            evidence_id=evidence_id,
            case_id=case_id,
            evidence_type=evidence_type,
            name=name,
            description=description,
            submitter=submitter,
            submit_date=datetime.now().strftime("%Y-%m-%d"),
            file_path=file_path,
            file_hash=file_hash,
            file_size=file_size,
            status=EvidenceStatus.SUBMITTED.value,
            notes=notes
        )
        
        self.evidences[evidence_id] = evidence
        self._save_data()
        
        return evidence
    
    def verify_evidence(self, 
                       evidence_id: str,
                       weight: str,
                       authenticity: str,
                       validity: str) -> bool:
        """
        审查证据
        
        Args:
            evidence_id: 证据ID
            weight: 证据效力
            authenticity: 真实性
            validity: 合法性/关联性
            
        Returns:
            是否成功
        """
        evidence = self.evidences.get(evidence_id)
        if not evidence:
            return False
        
        evidence.weight = weight
        evidence.authenticity = authenticity
        evidence.validity = validity
        evidence.status = EvidenceStatus.VERIFIED.value
        
        self._save_data()
        return True
    
    def get_case_evidences(self, case_id: str) -> List[EvidenceItem]:
        """获取案件所有证据"""
        return [e for e in self.evidences.values() if e.case_id == case_id]
    
    def get_evidence_by_type(self, case_id: str, evidence_type: str) -> List[EvidenceItem]:
        """按类型获取证据"""
        return [e for e in self.evidences.values() 
                if e.case_id == case_id and e.evidence_type == evidence_type]
    
    # ========== 证据链 ==========
    
    def build_evidence_chain(self,
                            case_id: str,
                            dispute_point: str,
                            evidence_ids: List[str],
                            chain_logic: str,
                            conclusion: str) -> EvidenceChain:
        """
        构建证据链
        
        Args:
            case_id: 案件ID
            dispute_point: 对应争议焦点
            evidence_ids: 证据ID列表
            chain_logic: 证据链逻辑
            conclusion: 结论
            
        Returns:
            证据链对象
        """
        chain_id = f"CHAIN-{case_id}-{len(self.chains)+1:02d}"
        
        chain = EvidenceChain(
            chain_id=chain_id,
            case_id=case_id,
            dispute_point=dispute_point,
            evidence_ids=evidence_ids,
            chain_logic=chain_logic,
            conclusion=conclusion,
            strength=self._evaluate_chain_strength(evidence_ids)
        )
        
        self.chains[chain_id] = chain
        return chain
    
    def _evaluate_chain_strength(self, evidence_ids: List[str]) -> str:
        """评估证据链强度"""
        if not evidence_ids:
            return "弱"
        
        high_count = sum(1 for eid in evidence_ids 
                        if eid in self.evidences 
                        and self.evidences[eid].weight == EvidenceWeight.HIGH.value)
        
        ratio = high_count / len(evidence_ids)
        
        if ratio >= 0.7:
            return "强"
        elif ratio >= 0.4:
            return "中等"
        else:
            return "弱"
    
    def get_case_chains(self, case_id: str) -> List[EvidenceChain]:
        """获取案件所有证据链"""
        return [c for c in self.chains.values() if c.case_id == case_id]
    
    # ========== 报告生成 ==========
    
    def generate_evidence_list(self, case_id: str) -> str:
        """生成证据清单（Markdown格式）"""
        evidences = self.get_case_evidences(case_id)
        
        lines = [
            f"# 证据清单",
            f"",
            f"**案件ID**: {case_id}",
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d')}",
            f"",
            "---",
            "",
            f"## 证据统计",
            "",
            f"- 总证据数：{len(evidences)}",
            f"- 已验证：{sum(1 for e in evidences if e.status == EvidenceStatus.VERIFIED.value)}",
            f"- 有争议：{sum(1 for e in evidences if e.status == EvidenceStatus.DISPUTED.value)}",
            "",
            "---",
            "",
            "## 证据明细",
            ""
        ]
        
        # 按类型分组
        type_groups = {}
        for e in evidences:
            if e.evidence_type not in type_groups:
                type_groups[e.evidence_type] = []
            type_groups[e.evidence_type].append(e)
        
        for evidence_type, items in type_groups.items():
            lines.append(f"### {evidence_type}")
            lines.append("")
            lines.append("| 序号 | 证据名称 | 提交方 | 提交日期 | 效力 | 状态 |")
            lines.append("|------|----------|--------|----------|------|------|")
            
            for i, e in enumerate(items, 1):
                lines.append(f"| {i} | {e.name} | {e.submitter} | {e.submit_date} | {e.weight} | {e.status} |")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_evidence_report(self, case_id: str) -> str:
        """生成证据分析报告"""
        evidences = self.get_case_evidences(case_id)
        chains = self.get_case_chains(case_id)
        
        lines = [
            f"# 证据分析报告",
            f"",
            f"**案件ID**: {case_id}",
            f"**生成日期**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "---",
            "",
            "## 一、证据概况",
            "",
            f"- 证据总数：{len(evidences)}",
            f"- 证据链数量：{len(chains)}",
            "",
        ]
        
        # 证据效力分布
        weight_dist = {}
        for e in evidences:
            weight_dist[e.weight] = weight_dist.get(e.weight, 0) + 1
        
        lines.append("### 证据效力分布")
        for w, count in weight_dist.items():
            lines.append(f"- {w}效力：{count}份")
        
        lines.extend([
            "",
            "## 二、证据链分析",
            ""
        ])
        
        for chain in chains:
            lines.extend([
                f"### 争议焦点：{chain.dispute_point}",
                f"- 证据链强度：{chain.strength}",
                f"- 涉及证据：{len(chain.evidence_ids)}份",
                f"- 证据链逻辑：{chain.chain_logic}",
                f"- 分析结论：{chain.conclusion}",
                ""
            ])
        
        lines.extend([
            "## 三、证据使用建议",
            "",
            "1. 重点关注高效力证据的举证",
            "2. 关注有争议证据的补充说明",
            "3. 完善证据链的完整性",
            ""
        ])
        
        return "\n".join(lines)


# ============================================================
# 便捷函数
# ============================================================

def submit_evidence(case_id: str, evidence_type: str, name: str, 
                  submitter: str, description: str = "") -> EvidenceItem:
    """快速提交证据"""
    manager = EvidenceManager()
    return manager.submit_evidence(case_id, evidence_type, name, 
                                  description, submitter)


def generate_list(case_id: str) -> str:
    """快速生成证据清单"""
    manager = EvidenceManager()
    return manager.generate_evidence_list(case_id)


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    manager = EvidenceManager()
    
    # 示例1：提交证据
    print("=== 示例1：提交证据 ===")
    evidence = manager.submit_evidence(
        case_id="CASE-20260404-001",
        evidence_type="合同文件",
        name="建设工程施工合同（主合同）",
        description="2023年签订的主合同，约定工程款支付方式",
        submitter="承包人"
    )
    print(f"证据已提交: {evidence.evidence_id}")
    
    # 示例2：审查证据
    print("\n=== 示例2：审查证据 ===")
    manager.verify_evidence(
        evidence.evidence_id,
        weight=EvidenceWeight.HIGH.value,
        authenticity="真实有效",
        validity="合法、关联性高"
    )
    print("证据已审查")
    
    # 示例3：构建证据链
    print("\n=== 示例3：构建证据链 ===")
    chain = manager.build_evidence_chain(
        case_id="CASE-20260404-001",
        dispute_point="工程款支付金额",
        evidence_ids=[evidence.evidence_id],
        chain_logic="合同约定付款节点+验收报告+付款凭证",
        conclusion="证据充分支持承包人主张"
    )
    print(f"证据链已构建: {chain.chain_id}, 强度: {chain.strength}")
    
    # 示例4：生成清单
    print("\n=== 示例4：生成证据清单 ===")
    evidence_list = manager.generate_evidence_list("CASE-20260404-001")
    print(evidence_list[:300] + "...")