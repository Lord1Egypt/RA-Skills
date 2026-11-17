#!/usr/bin/env python3
"""
CodeRisk MCP Server — 生产版 v1.0.2
====================================
2 个核心 Tool：
  1. coderisk_scan_code   — 内部跑完整四层流水线
  2. coderisk_lookup_cve  — 本地 CVE 数据库查询

LLM 后端：云端 API 优先（OpenAI/Anthropic/DeepSeek），本地 GPU 可选。

⚠️ 安全警告：SSE 模式仅供本地调试使用，默认绑定 127.0.0.1。
   如需远程访问，必须配置 API Key 认证和 TLS，切勿在无认证环境下暴露到公网。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.server.sse import SseServerTransport
    from mcp.types import Tool, TextContent
except ImportError:
    print("ERROR: mcp SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# ─── 自动发现 skill 包内的 core/ 和 agents/ ────────────────
_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

# ─── 引入原有 CodeRisk 核心 ─────────────────────────────────
from core.models import (
    AnalysisResult, CodeFile, Language, Risk,
    Severity, Confidence, Evidence
)
from core.cve_client import CVEClient
from core.memory import MemoryLayer
from core.dependency_scanner import scan_project_dependencies
from core.taint_analyzer import TaintAnalyzer
from core.semgrep_runner import analyze_with_semgrep

from agents.static_analyzer import StaticAnalyzer
from agents.report_generator import ReportGenerator

# ─── 云端 LLM 客户端 ────────────────────────────────────────
import httpx


class CloudLLMClient:
    """支持 OpenAI / Anthropic / DeepSeek / 本地 的 LLM 客户端。
    通过环境变量切换后端，零侵入原有代码。
    """

    def __init__(self):
        self.backend = os.getenv("CODERISK_LLM_BACKEND", "openai").lower()
        self.api_key = os.getenv("CODERISK_API_KEY", "")
        self.base_url = os.getenv("CODERISK_BASE_URL", "")
        self.model = os.getenv("CODERISK_MODEL", "")
        self.timeout = 120
        self._http: Optional[httpx.Client] = None
        self._local_llm = None

        if self.backend == "openai":
            self.base_url = self.base_url or "https://api.openai.com/v1"
            self.model = self.model or "gpt-4o"
        elif self.backend == "anthropic":
            self.base_url = self.base_url or "https://api.anthropic.com/v1"
            self.model = self.model or "claude-3-5-sonnet-20241022"
        elif self.backend == "deepseek":
            self.base_url = self.base_url or "https://api.deepseek.com/v1"
            self.model = self.model or "deepseek-coder"
        elif self.backend == "local":
            self._init_local()

        if self.backend != "local":
            self._http = httpx.Client(
                base_url=self.base_url,
                headers=self._auth_headers(),
                timeout=self.timeout,
            )

    def _auth_headers(self) -> dict:
        if self.backend == "anthropic":
            return {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _init_local(self):
        try:
            from llama_cpp import Llama
            model_path = os.getenv("CODERISK_LOCAL_MODEL_PATH", "")
            if not model_path or not Path(model_path).exists():
                raise RuntimeError("Local model not found. Set CODERISK_LOCAL_MODEL_PATH.")
            self._local_llm = Llama(model_path=model_path, n_ctx=4096, verbose=False)
            self.model = "local-llama"
        except Exception as e:
            raise RuntimeError(f"Local LLM init failed: {e}")

    def chat_json(self, system: str, user: str, max_tokens: int = 4096) -> dict:
        """统一接口：返回结构化 JSON。"""
        if self.backend == "local":
            return self._chat_local_json(system, user, max_tokens)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        if self.backend == "anthropic":
            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }
            r = self._http.post("/messages", json=payload)
        else:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": max_tokens,
            }
            r = self._http.post("/chat/completions", json=payload)

        r.raise_for_status()
        data = r.json()

        if self.backend == "anthropic":
            raw = data["content"][0]["text"]
        else:
            raw = data["choices"][0]["message"]["content"]

        return self._extract_json(raw)

    def _chat_local_json(self, system: str, user: str, max_tokens: int) -> dict:
        prompt = f"<|im_start|>system\n{system}\n<|im_end|>\n<|im_start|>user\n{user}\n<|im_end|>\n<|im_start|>assistant\n"
        result = self._local_llm(prompt, max_tokens=max_tokens, temperature=0.1, stop=["<|im_end|>"])
        raw = result["choices"][0]["text"]
        return self._extract_json(raw)

    @staticmethod
    def _extract_json(text: str) -> dict:
        """从 LLM 响应中提取 JSON，多策略回退。"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        if "```json" in text:
            start = text.index("```json") + 7
            end = text.find("```", start)
            if end > start:
                try:
                    return json.loads(text[start:end].strip())
                except json.JSONDecodeError:
                    pass

        depth = 0
        start = -1
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        start = -1

        stripped = text.strip()
        if stripped.startswith("{"):
            opens = stripped.count("{")
            closes = stripped.count("}")
            if opens > closes:
                try:
                    return json.loads(stripped + "}" * (opens - closes))
                except json.JSONDecodeError:
                    pass
        raise ValueError(f"Failed to extract JSON from LLM response:\n{text[:500]}")

    def close(self):
        if self._http:
            self._http.close()


# ─── Prompt 模板 ────────────────────────────────────────────

SEMANTIC_SYSTEM = """You are a senior code security auditor. Analyze the provided source code and risks.

For EACH existing risk, determine if it is a true positive or false positive.
Also scan for MISSED vulnerabilities that static analysis did not catch.

Output MUST be valid JSON:
{
  "validated_risks": [
    {
      "id": "RISK-001",
      "is_true_positive": true,
      "reasoning": "...",
      "attack_scenario": "...",
      "impact": "...",
      "adjusted_severity": "critical|high|medium|low|info",
      "confidence": 0.85
    }
  ],
  "new_risks": [
    {
      "title": "...",
      "description": "...",
      "severity": "critical|high|medium|low",
      "cwe_id": "CWE-xxx",
      "line_start": 10,
      "line_end": 10,
      "attack_scenario": "...",
      "suggestion": "..."
    }
  ]
}"""

VERIFY_SYSTEM = """You are a security verification expert. Given code and a list of risks:

1. VERIFY each risk: Is it confirmed by multiple sources?
2. FIND MISSED vulnerabilities
3. FLAG FALSE POSITIVES

Output JSON:
{
  "verified_risks": [
    {
      "id": "RISK-001",
      "confirmed": true,
      "confidence_reason": "...",
      "false_positive_likelihood": "low|medium|high"
    }
  ],
  "missed_risks": [
    {
      "title": "...",
      "description": "...",
      "severity": "critical|high|medium|low",
      "cwe_id": "CWE-xxx",
      "line_start": 10,
      "line_end": 10,
      "reasoning": "...",
      "suggestion": "..."
    }
  ]
}"""


# ─── 全局单例 ───────────────────────────────────────────────
_static_analyzer: Optional[StaticAnalyzer] = None
_taint_analyzer: Optional[TaintAnalyzer] = None
_cve_client: Optional[CVEClient] = None
_memory: Optional[MemoryLayer] = None
_llm: Optional[CloudLLMClient] = None
_report_generator: Optional[ReportGenerator] = None
_risk_counter: int = 0


def _init_engine(enable_ai: bool = False) -> None:
    global _static_analyzer, _taint_analyzer, _cve_client, _memory, _llm, _report_generator
    if _static_analyzer is None:
        _static_analyzer = StaticAnalyzer()
    if _taint_analyzer is None:
        _taint_analyzer = TaintAnalyzer()
    if _cve_client is None:
        _cve_client = CVEClient()
    if _memory is None:
        _memory = MemoryLayer()
    if _report_generator is None:
        _report_generator = ReportGenerator()

    if enable_ai and _llm is None:
        try:
            _llm = CloudLLMClient()
        except Exception as e:
            print(f"[WARN] LLM init failed, AI phases disabled: {e}", file=sys.stderr)


def _next_risk_id() -> str:
    global _risk_counter
    _risk_counter += 1
    return f"RISK-{_risk_counter:03d}"


# ─── Tool 定义（模块级常量，避免动态枚举）──────────────────

TOOLS: list[Tool] = [
    Tool(
        name="coderisk_scan_code",
            description="对代码文件或目录执行完整的安全分析流水线（四层：静态分析→语义分析→深度验证→报告生成）。"
                        "支持 C (.c/.h) 和 Python (.py)。"
                        "默认使用云端 LLM API，也可通过环境变量切换为本地 GPU 推理。",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_path": {
                        "type": "string",
                        "description": "要分析的代码文件或目录的绝对路径"
                    },
                    "enable_ai": {
                        "type": "boolean",
                        "default": False,
                        "description": "是否启用 LLM 语义分析（需要配置 API key）"
                    },
                    "enable_semgrep": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否启用 Semgrep 扩展规则"
                    },
                    "scan_dependencies": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否扫描项目依赖漏洞"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["json", "md", "sarif", "terminal"],
                        "default": "json",
                        "description": "报告格式。建议 AI 使用 json 便于解析，再渲染为 Markdown 展示"
                    },
                    "max_reflection_rounds": {
                        "type": "integer",
                        "default": 2,
                        "description": "Agent 3 自反思循环最大轮数（0=关闭）"
                    }
                },
                "required": ["target_path"]
            }
        ),
        Tool(
            name="coderisk_lookup_cve",
            description="查询本地 CVE 数据库（NVD SQLite），获取指定 CWE 关联的 CVE 漏洞信息。",
            inputSchema={
                "type": "object",
                "properties": {
                    "cwe_id": {
                        "type": "string",
                        "description": "CWE ID，例如 CWE-120、CWE-78"
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 5,
                        "description": "最大返回条数"
                    }
                },
                "required": ["cwe_id"]
            }
        ),
    ]


# ─── MCP Server（v2.0 API）

async def _on_list_tools(ctx, params):
    from mcp.types import ListToolsResult
    return ListToolsResult(tools=TOOLS)


async def _on_call_tool(ctx, params):
    from mcp.types import CallToolResult
    name = params.name
    arguments = params.arguments or {}
    _init_engine(enable_ai=arguments.get("enable_ai", False))

    try:
        if name == "coderisk_scan_code":
            content = await _handle_scan_code(arguments)
        elif name == "coderisk_lookup_cve":
            content = await _handle_lookup_cve(arguments)
        else:
            content = [TextContent(type="text", text=f"Unknown tool: {name}")]
        return CallToolResult(content=content)
    except Exception as e:
        import traceback
        return CallToolResult(
            content=[TextContent(type="text", text=f"ERROR: {e}\n{traceback.format_exc()}")],
            isError=True
        )


app = Server("coderisk-agent", on_list_tools=_on_list_tools, on_call_tool=_on_call_tool)


# ─── Tool: 完整流水线 ───────────────────────────────────────

async def _handle_scan_code(args: dict) -> list[TextContent]:
    target = Path(args["target_path"])
    enable_ai = args.get("enable_ai", False)
    enable_semgrep = args.get("enable_semgrep", True)
    scan_deps = args.get("scan_dependencies", True)
    output_format = args.get("output_format", "json")
    max_reflection = args.get("max_reflection_rounds", 2)

    if not target.exists():
        return [TextContent(type="text", text=json.dumps({
            "success": False, "error": f"Path not found: {target}"
        }, indent=2, ensure_ascii=False))]

    start_time = time.monotonic()
    perf = {}

    # Phase 1: 文件收集
    files = _collect_files(target)
    if not files:
        return [TextContent(type="text", text=json.dumps({
            "success": False, "error": f"No supported files found in {target}"
        }, indent=2, ensure_ascii=False))]

    # Phase 2: 静态分析（Agent 1，并行）
    t0 = time.monotonic()
    all_risks: list[Risk] = []

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(_static_analyzer.analyze, f): f for f in files}
        for future in as_completed(futures):
            f = futures[future]
            try:
                risks = future.result()
                all_risks.extend(risks)
            except Exception as e:
                print(f"[WARN] Static analysis failed for {f.path}: {e}", file=sys.stderr)

    # Semgrep
    if enable_semgrep:
        for f in files:
            try:
                risks = analyze_with_semgrep(f, config="p/default")
                all_risks.extend(risks)
            except Exception:
                pass

    # Taint
    for f in files:
        try:
            if f.language == Language.C:
                flows = _taint_analyzer.analyze_c(f.content, str(f.path))
            elif f.language == Language.PYTHON:
                flows = _taint_analyzer.analyze_python(f.content, str(f.path))
            else:
                flows = []
            for flow in flows:
                all_risks.append(_taint_flow_to_risk(flow, f))
        except Exception:
            pass

    perf["phase1_static"] = int((time.monotonic() - t0) * 1000)

    # Phase 1.5: 依赖扫描
    if scan_deps:
        t0 = time.monotonic()
        try:
            project_root = _find_project_root(files)
            dep_findings = scan_project_dependencies(project_root)
            for finding in dep_findings:
                all_risks.append(Risk(
                    id=_next_risk_id(),
                    title=f"Vulnerable dep: {finding['package']} {finding['version']}",
                    description=finding['description'],
                    severity=Severity.HIGH,
                    confidence=Confidence.HIGH,
                    cwe_id=finding.get('cwe'),
                    language=Language.UNKNOWN,
                    file_path=Path(finding.get('file', 'requirements.txt')),
                    line_start=0, line_end=0,
                    evidence=[Evidence(
                        source="dependency_scan",
                        snippet=f"{finding['package']}=={finding['version']}",
                        line_start=0, line_end=0,
                        reasoning=finding['description']
                    )],
                    suggestion=finding.get('fix', 'Update to patched version.')
                ))
            perf["phase1_5_deps"] = int((time.monotonic() - t0) * 1000)
        except Exception:
            perf["phase1_5_deps"] = 0

    # Phase 3: LLM 语义分析（Agent 2）
    if enable_ai and _llm:
        t0 = time.monotonic()
        for f in files:
            file_risks = [r for r in all_risks if r.file_path == f.path]
            if f.line_count < 5 and not file_risks:
                continue
            try:
                enriched = _run_semantic_analysis(f, file_risks)
                all_risks = [r for r in all_risks if r.file_path != f.path]
                all_risks.extend(enriched)
            except Exception as e:
                print(f"[WARN] Semantic analysis failed for {f.path}: {e}", file=sys.stderr)
        perf["phase2_semantic"] = int((time.monotonic() - t0) * 1000)
    else:
        perf["phase2_semantic"] = 0

    # Phase 4: 深度验证（Agent 3）
    if enable_ai and _llm:
        t0 = time.monotonic()
        all_risks = _run_deep_verification(files, all_risks, max_reflection)
        perf["phase3_verify"] = int((time.monotonic() - t0) * 1000)
    else:
        perf["phase3_verify"] = 0

    # Phase 5: 报告生成（Agent 4）
    t0 = time.monotonic()
    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    result = AnalysisResult(
        request_id=f"scan-{int(time.time())}",
        files_analyzed=len(files),
        risks=all_risks,
        analysis_time_ms=elapsed_ms,
        model_used="cloud-llm" if (enable_ai and _llm) else "static-only",
        perf_timings=perf,
    )

    # 记忆存储
    for r in all_risks:
        if r.confidence == Confidence.HIGH and r.severity in (Severity.CRITICAL, Severity.HIGH):
            _memory.store_correct(r)

    # 格式化输出
    if output_format == "json":
        report = _report_generator.generate_json(result)
        text = json.dumps(report, indent=2, ensure_ascii=False)
    elif output_format == "md":
        text = _report_generator.generate_markdown(result)
    elif output_format == "sarif":
        report = _report_generator.generate_sarif(result)
        text = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        report = _report_generator.generate_json(result)
        text = json.dumps(report, indent=2, ensure_ascii=False)

    perf["phase4_report"] = int((time.monotonic() - t0) * 1000)

    return [TextContent(type="text", text=text)]


def _run_semantic_analysis(code_file: CodeFile, existing_risks: list[Risk]) -> list[Risk]:
    """Agent 2: 云端 LLM 语义分析"""
    risk_summaries = []
    for r in existing_risks:
        risk_summaries.append(
            f"- {r.id}: [{r.severity.value}] {r.title}\n"
            f"  CWE: {r.cwe_id or 'N/A'} | Lines: {r.line_start}-{r.line_end}\n"
            f"  Desc: {r.description[:200]}"
        )

    user_prompt = f"""## Source File: {code_file.path}
Language: {code_file.language.value}

```{code_file.language.value}
{code_file.content}
```

## Risks Found by Static Analysis
{chr(10).join(risk_summaries) if risk_summaries else "No risks found by static analysis."}

Please validate each risk and identify any missed vulnerabilities."""

    response = _llm.chat_json(SEMANTIC_SYSTEM, user_prompt, max_tokens=4096)

    validated = response.get("validated_risks", [])
    new_raw = response.get("new_risks", [])

    risk_map = {r.id: r for r in existing_risks}
    merged: list[Risk] = []

    for v in validated:
        rid = v.get("id", "")
        if rid not in risk_map:
            continue
        risk = risk_map[rid]

        if not v.get("is_true_positive", True):
            risk = risk.model_copy(update={
                "severity": Severity.INFO,
                "confidence": Confidence.LOW,
                "description": risk.description + " [LLM: likely false positive]"
            })
        else:
            conf = v.get("confidence", 0.5)
            new_conf = Confidence.HIGH if conf >= 0.8 else Confidence.MEDIUM if conf >= 0.5 else Confidence.LOW
            if new_conf != risk.confidence:
                risk = risk.model_copy(update={"confidence": new_conf})

            parts = []
            if v.get("attack_scenario"):
                parts.append(f"Attack: {v['attack_scenario']}")
            if v.get("impact"):
                parts.append(f"Impact: {v['impact']}")
            if parts:
                risk = risk.model_copy(update={
                    "description": risk.description + " | " + " | ".join(parts)
                })

            adj = v.get("adjusted_severity", "").lower()
            if adj and adj in [s.value for s in Severity]:
                risk = risk.model_copy(update={"severity": Severity(adj)})

        merged.append(risk)

    validated_ids = {v.get("id") for v in validated}
    for r in existing_risks:
        if r.id not in validated_ids:
            merged.append(r)

    for nr in new_raw:
        sev_str = nr.get("severity", "medium").lower()
        sev = Severity(sev_str) if sev_str in [s.value for s in Severity] else Severity.MEDIUM
        merged.append(Risk(
            id=f"RISK-{uuid.uuid4().hex[:8].upper()}",
            title=nr.get("title", "LLM-detected risk"),
            description=nr.get("description", ""),
            severity=sev,
            confidence=Confidence.MEDIUM,
            cwe_id=nr.get("cwe_id"),
            language=code_file.language,
            file_path=code_file.path,
            line_start=nr.get("line_start", 0),
            line_end=nr.get("line_end", 0),
            evidence=[Evidence(
                source="ai",
                snippet="",
                line_start=nr.get("line_start", 0),
                line_end=nr.get("line_end", 0),
                reasoning=f"LLM semantic analysis: {nr.get('attack_scenario', 'detected by AI')}"
            )],
            suggestion=nr.get("suggestion", "Review this code section.")
        ))

    return merged


def _run_deep_verification(files: list[CodeFile], risks: list[Risk], max_rounds: int) -> list[Risk]:
    """Agent 3: 深度验证 + 自反思"""
    if not risks:
        return risks

    critical_cwes = {r.cwe_id for r in risks if r.cwe_id and r.severity in (Severity.CRITICAL, Severity.HIGH)}
    for cwe in critical_cwes:
        try:
            _cve_client.get_cve_summary(cwe)
        except Exception:
            pass

    verified = []
    suppressed = 0

    for risk in risks:
        mem = _memory.recall(risk)
        if mem:
            entry, mtype = mem
            if mtype == "error" and entry.source_count >= 2:
                suppressed += 1
                continue
            elif mtype == "correct" and risk.confidence != Confidence.HIGH:
                risk = risk.model_copy(update={"confidence": Confidence.HIGH})

        confirmations = 0
        reasons = []
        has_pattern = any(e.source == "pattern_match" for e in risk.evidence)
        has_ai = any(e.source == "ai" for e in risk.evidence)
        has_semgrep = any(e.source == "semgrep" for e in risk.evidence)

        if has_pattern:
            confirmations += 1
            reasons.append("pattern")
        if has_semgrep:
            confirmations += 1
            reasons.append("semgrep")
        if has_ai:
            confirmations += 1
            reasons.append("ai")

        if risk.cwe_id and risk.severity in (Severity.CRITICAL, Severity.HIGH):
            try:
                cve_sum = _cve_client.get_cve_summary(risk.cwe_id)
                if "No CVE data" not in cve_sum:
                    confirmations += 1
                    reasons.append("cve_db")
                    risk = risk.model_copy(update={
                        "description": risk.description + f" [CVE: {cve_sum[:120]}]"
                    })
            except Exception:
                pass

        new_conf = Confidence.HIGH if confirmations >= 2 else Confidence.MEDIUM if confirmations >= 1 else Confidence.LOW
        if new_conf != risk.confidence:
            risk = risk.model_copy(update={
                "confidence": new_conf,
                "description": risk.description + f" [Verification: {confirmations} confirmations ({', '.join(reasons)})]"
            })

        verified.append(risk)

    if suppressed > 0:
        print(f"[INFO] Suppressed {suppressed} known false positives", file=sys.stderr)

    # 自反思
    if _llm and max_rounds > 0:
        for f in files:
            file_risks = [r for r in verified if r.file_path == f.path]
            all_new = []
            current = list(file_risks)

            for rnd in range(max_rounds):
                risk_text = "\n".join(
                    f"- {r.id}: [{r.severity.value}] {r.title} (CWE: {r.cwe_id or 'N/A'})"
                    for r in current
                ) if current else "No risks found."

                user_prompt = f"""## Source File: {f.path}
Language: {f.language.value}

```{f.language.value}
{f.content}
```

## Current Risks
{risk_text}

Verify these risks and find any missed vulnerabilities."""

                try:
                    response = _llm.chat_json(VERIFY_SYSTEM, user_prompt, max_tokens=4096)
                except Exception:
                    break

                missed = response.get("missed_risks", [])
                if not missed:
                    break

                for mr in missed:
                    sev_str = mr.get("severity", "medium").lower()
                    sev = Severity(sev_str) if sev_str in [s.value for s in Severity] else Severity.MEDIUM
                    new_risk = Risk(
                        id=f"RISK-{uuid.uuid4().hex[:8].upper()}",
                        title=mr.get("title", "Missed risk"),
                        description=mr.get("description", ""),
                        severity=sev,
                        confidence=Confidence.MEDIUM,
                        cwe_id=mr.get("cwe_id"),
                        language=f.language,
                        file_path=f.path,
                        line_start=mr.get("line_start", 0),
                        line_end=mr.get("line_end", 0),
                        evidence=[Evidence(
                            source="ai",
                            snippet="",
                            line_start=mr.get("line_start", 0),
                            line_end=mr.get("line_end", 0),
                            reasoning=f"Agent 3 reflection: {mr.get('reasoning', 'missed by previous agents')}"
                        )],
                        suggestion=mr.get("suggestion", "Review this code section.")
                    )
                    all_new.append(new_risk)
                    current.append(new_risk)

            verified.extend(all_new)

    return verified


# ─── Tool: CVE 查询 ─────────────────────────────────────────

async def _handle_lookup_cve(args: dict) -> list[TextContent]:
    cwe_id = args["cwe_id"]
    max_results = args.get("max_results", 5)
    results = _cve_client.query_by_cwe(cwe_id, max_results)
    return [TextContent(type="text", text=json.dumps({
        "cwe_id": cwe_id,
        "results": results,
        "db_stats": _cve_client.get_stats()
    }, indent=2, ensure_ascii=False))]


# ─── 辅助函数 ───────────────────────────────────────────────

def _collect_files(target: Path) -> list[CodeFile]:
    exts = {".c", ".h", ".py"}
    files = []
    if target.is_file():
        if target.suffix in exts:
            files.append(CodeFile.from_path(target))
    else:
        for ext in exts:
            for f in target.rglob(f"*{ext}"):
                if f.is_file():
                    files.append(CodeFile.from_path(f))
    return files


def _find_project_root(files: list[CodeFile]) -> Path:
    markers = ["requirements.txt", "setup.py", "pyproject.toml", "package.json", "go.mod", "Cargo.toml", "Makefile"]
    start = Path(files[0].path).resolve().parent
    current = start
    for _ in range(10):
        if any((current / m).exists() for m in markers):
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return start


def _taint_flow_to_risk(flow, code_file: CodeFile) -> Risk:
    """将 TaintFlow 对象转换为 Risk。使用 getattr 防御属性缺失。"""
    sev_val = getattr(flow, 'severity', 'medium')
    sev = Severity(sev_val) if sev_val in [s.value for s in Severity] else Severity.MEDIUM
    conf_val = getattr(flow, 'confidence', '')
    conf = Confidence.HIGH if conf_val == "high" else Confidence.MEDIUM
    return Risk(
        id=_next_risk_id(),
        title=f"Taint: {getattr(flow, 'description', 'data flow')[:60]}",
        description=getattr(flow, 'description', ''),
        severity=sev,
        confidence=conf,
        cwe_id=getattr(flow, 'cwe_id', None),
        language=code_file.language,
        file_path=code_file.path,
        line_start=getattr(flow, 'sink_line', 0),
        line_end=getattr(flow, 'sink_line', 0),
        evidence=[Evidence(
            source="taint_analysis",
            snippet=f"{getattr(flow, 'source', '')} -> {getattr(flow, 'sink', '')}",
            line_start=getattr(flow, 'source_line', 0),
            line_end=getattr(flow, 'sink_line', 0),
            reasoning=f"Data flow: {getattr(flow, 'source', '')} -> {getattr(flow, 'sink', '')}"
        )],
        suggestion=getattr(flow, 'suggestion', 'Review data flow.')
    )


# ─── 启动入口 ───────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="CodeRisk MCP Server")
    parser.add_argument("--sse", action="store_true", help="启用 SSE 模式（仅供本地调试，默认绑定 127.0.0.1）")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="SSE 绑定地址（默认 127.0.0.1，切勿设为 0.0.0.0 暴露到公网）")
    parser.add_argument("--port", type=int, default=8080, help="SSE 端口（默认 8080）")
    args = parser.parse_args()

    if args.sse:
        # 强制 SSE 模式仅允许绑定 127.0.0.1
        if args.host != "127.0.0.1":
            print("[SECURITY ERROR] SSE mode is restricted to 127.0.0.1 only. "
                  "Remote access is not permitted. Use stdio mode for production.", file=sys.stderr)
            sys.exit(1)

        # SSE 模式必须配置 API Key
        sse_api_key = os.getenv("CODERISK_SSE_API_KEY", "")
        if not sse_api_key:
            print("[SECURITY ERROR] SSE mode requires CODERISK_SSE_API_KEY environment variable. "
                  "Set a strong random key before starting SSE mode.", file=sys.stderr)
            sys.exit(1)

        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as (rs, ws):
                await app.run(rs, ws, app.create_initialization_options())

        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request._send)

        # 生产模式：debug=False
        starlette_app = Starlette(debug=False, routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages/", endpoint=handle_messages, methods=["POST"]),
        ])

        # 添加 API Key 认证中间件
        starlette_app = APIKeyAuthMiddleware(starlette_app, sse_api_key)

        print(f"[CodeRisk MCP] SSE mode on http://127.0.0.1:{args.port}/sse (LOCAL ONLY, AUTH REQUIRED)", file=sys.stderr)
        uvicorn.run(starlette_app, host="127.0.0.1", port=args.port)
    else:
        async with stdio_server() as (rs, ws):
            await app.run(rs, ws, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
