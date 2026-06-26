import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

import requests


UTC8 = timezone(timedelta(hours=8))
DEADLINE_PATTERNS = [
    re.compile(r"(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)"),
    re.compile(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+20\d{2}(?:\s+\d{1,2}:\d{2})?)", re.I),
]
RISK_KEYWORDS = ["private key", "seed phrase", "mnemonic", "助记词", "私钥"]


@dataclass
class SourceResult:
    name: str
    url: str
    changed: bool
    old_hash: str
    new_hash: str
    extracted_deadlines: List[str]
    risks: List[str]


def now() -> datetime:
    return datetime.now(UTC8)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_text(url: str, timeout: int = 20) -> str:
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "airdrop-monitor-cn/0.2"})
    r.raise_for_status()
    text = r.text
    text = re.sub(r"\s+", " ", text)
    return text[:15000]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def extract_deadlines(text: str) -> List[str]:
    found: List[str] = []
    for p in DEADLINE_PATTERNS:
        found.extend([m.group(1) for m in p.finditer(text)])
    # 去重保持顺序
    seen = set()
    out = []
    for d in found:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out[:8]


def detect_risks(text: str, url: str) -> List[str]:
    risks: List[str] = []
    lower = text.lower()
    if lower.startswith("fetch_error:"):
        risks.append("来源抓取失败，请检查网络/证书/目标站可达性")
    for k in RISK_KEYWORDS:
        if k in lower:
            risks.append(f"文本出现高风险关键词: {k}")

    if url.startswith("http://"):
        risks.append("来源为非 HTTPS 链接")
    if re.search(r"https?://\d+\.\d+\.\d+\.\d+", url):
        risks.append("来源使用 IP 地址，需人工核验")
    if "xn--" in url:
        risks.append("来源疑似 punycode 域名，警惕仿冒")
    return risks


def build_actions(results: List[SourceResult]) -> List[str]:
    actions: List[str] = []
    changed = [r for r in results if r.changed]
    if changed:
        actions.append(f"优先复核 {len(changed)} 个发生变化的来源页面")
    for r in changed[:3]:
        actions.append(f"检查【{r.name}】的新公告并更新任务清单")

    deadlines = [d for r in results for d in r.extracted_deadlines]
    if deadlines:
        actions.append("整理所有截止时间，设置 T-24h/T-6h/T-1h 提醒")
    else:
        actions.append("今日未提取到明确截止时间，建议人工确认关键项目")

    if any(r.risks for r in results):
        actions.append("先处理风险项：可疑链接或私钥/助记词相关内容一律跳过")

    return actions[:5]


def run_monitor(config_path: str, state_path: str = ".state/airdrop-monitor-state.json") -> Dict[str, Any]:
    cfg = load_json(Path(config_path), default={})
    if not cfg.get("projects"):
        raise ValueError("配置缺少 projects")

    state_file = Path(state_path)
    state = load_json(state_file, default={"sources": {}})

    results: List[SourceResult] = []
    for proj in cfg["projects"]:
        pname = proj.get("name", "unknown")
        for src in proj.get("sources", []):
            sname = f"{pname}:{src.get('name', 'source')}"
            surl = src["url"]
            try:
                text = fetch_text(surl)
            except Exception as e:
                text = f"fetch_error: {e}"

            h = digest(text)
            old_h = state["sources"].get(surl, "")
            changed = old_h != "" and old_h != h

            result = SourceResult(
                name=sname,
                url=surl,
                changed=changed,
                old_hash=old_h,
                new_hash=h,
                extracted_deadlines=extract_deadlines(text),
                risks=detect_risks(text, surl),
            )
            results.append(result)
            state["sources"][surl] = h

    save_json(state_file, state)

    risk_items = [f"{r.name}: {x}" for r in results for x in r.risks]
    changed_items = [r.name for r in results if r.changed]
    deadlines = [{"source": r.name, "items": r.extracted_deadlines} for r in results if r.extracted_deadlines]

    return {
        "generated_at": now().strftime("%Y-%m-%d %H:%M:%S %z"),
        "summary": {
            "total_sources": len(results),
            "changed_sources": len(changed_items),
            "risk_count": len(risk_items),
        },
        "changed_sources": changed_items,
        "deadlines": deadlines,
        "risks": risk_items,
        "priority_actions": build_actions(results),
    }


def format_markdown_report(data: Dict[str, Any]) -> str:
    lines = [
        f"# 空投监控日报 ({data['generated_at']})",
        "",
        "## 概览",
        f"- 监控来源: {data['summary']['total_sources']}",
        f"- 有变化来源: {data['summary']['changed_sources']}",
        f"- 风险项: {data['summary']['risk_count']}",
        "",
        "## 变化来源",
    ]
    if data["changed_sources"]:
        lines.extend([f"- {x}" for x in data["changed_sources"]])
    else:
        lines.append("- 暂无来源变化")

    lines.extend(["", "## 截止时间线索"])
    if data["deadlines"]:
        for d in data["deadlines"]:
            lines.append(f"- {d['source']}: {', '.join(d['items'])}")
    else:
        lines.append("- 暂无")

    lines.extend(["", "## 风险提示"])
    if data["risks"]:
        lines.extend([f"- {x}" for x in data["risks"]])
    else:
        lines.append("- 暂无")

    lines.extend(["", "## 今日 Top 动作"])
    lines.extend([f"{i+1}. {x}" for i, x in enumerate(data["priority_actions"])])
    return "\n".join(lines)
