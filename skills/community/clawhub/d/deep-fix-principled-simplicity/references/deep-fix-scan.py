#!/usr/bin/env python3
"""
deep-fix-scan.py — 代码库证据收集器（开发者可选工具）

职责：只观测，不判断。把客观事实交给 Claude，由 Claude 结合
Principled Simplicity skill 的 Step 0–2 做诊断。

适用场景：你有一个本地代码库，想在和 Claude 对话前先收集量化证据。
非代码库用户无需运行此脚本——直接用 SKILL.md 的 Step 0 四个问题
和 Claude 对话，效果等价。

用法:
  python deep-fix-scan.py <path>           # 扫代码目录或单文件
  python deep-fix-scan.py --prompt <file>  # 只做 prompt 结构分析
  python deep-fix-scan.py --full <path>    # 代码 + 自动查找 prompt 文件

输出直接贴给 Claude，说：
「根据这份报告，用 Principled Simplicity skill 诊断根因，给出修复层级判决。」
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field

CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"}
PROMPT_MARKERS = ["system_prompt", "system prompt", "SYSTEM", "你是", "You are", "instructions"]

INTENT_WORDS = re.compile(
    r'\b(user|query|input|message|request|intent|text|content|action|说|问|输入)\b',
    re.IGNORECASE
)
SCHEMA_WORDS = re.compile(
    r'\b(isinstance|type\(|len\(|None|null|empty|valid|schema|required|format|int|str|bool)\b',
    re.IGNORECASE
)

@dataclass
class Observation:
    file: str
    line: int
    kind: str
    snippet: str

@dataclass
class ScanReport:
    path: str
    observations: list[Observation] = field(default_factory=list)
    prompt_buckets: dict = field(default_factory=dict)
    prompt_e_items: list[str] = field(default_factory=list)
    file_count: int = 0
    notes: list[str] = field(default_factory=list)


def scan_file(path: Path) -> list[Observation]:
    obs = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return obs
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        if s.startswith(("if ", "elif ")):
            if INTENT_WORDS.search(s) and not SCHEMA_WORDS.search(s):
                obs.append(Observation(str(path), i, "if_else_on_intent", s[:120]))
        if re.search(r'(keywords?|triggers?|patterns?|rules?|intents?)\s*[=:]\s*[\[\{]', s, re.I):
            obs.append(Observation(str(path), i, "keyword_list", s[:120]))
        if re.search(r're\.(match|search|findall|sub|compile)\s*\(', s) and INTENT_WORDS.search(s):
            obs.append(Observation(str(path), i, "regex_on_input", s[:120]))
        if re.search(r'(#.*(hack|workaround|temp.*fix|patch.*case|fixme)|TODO.*patch)', s, re.I):
            obs.append(Observation(str(path), i, "patch_comment", s[:120]))
    return obs


def find_cross_file_duplicates(all_obs: list[Observation]) -> list[str]:
    snippet_files: dict[str, set] = defaultdict(set)
    for o in all_obs:
        key = o.snippet[:40].strip()
        if len(key) > 15:
            snippet_files[key].add(o.file)
    return [
        f"「{snip}…」出现在 {len(files)} 个文件"
        for snip, files in snippet_files.items()
        if len(files) >= 3
    ]


def scan_codebase(path: Path) -> ScanReport:
    report = ScanReport(path=str(path))
    all_obs, count = [], 0
    for ext in CODE_EXTENSIONS:
        for f in path.rglob(f"*{ext}"):
            if any(skip in f.parts for skip in SKIP_DIRS):
                continue
            all_obs.extend(scan_file(f))
            count += 1
    report.observations, report.file_count = all_obs, count
    dups = find_cross_file_duplicates(all_obs)
    if dups:
        report.notes.append(f"跨文件重复片段（≥3 文件）: {len(dups)} 处")
        report.notes.extend(f"  {d}" for d in dups[:5])
    return report


BUCKET_RULES = [
    (re.compile(r'\b(never|always|must not|forbidden|prohibited|禁止|严禁|不得)', re.I),
     "C", "强制约束词 → 可能是代码/validator 层"),
    (re.compile(r'\b(if.{0,30}then|when.{0,30}should|except when|unless|如果.*则|当.*时)', re.I),
     "E", "条件分支 → 可能是未决产品决策"),
    (re.compile(r'\b(our product|we offer|pricing|plan|tier|version|我们的产品|定价|方案|版本)', re.I),
     "A", "产品事实 → 可能属于 Wiki/Memory"),
    (re.compile(r'(step \d|first[,，]? then|follow these steps|按以下步骤|第[一二三四五]步)', re.I),
     "B", "流程步骤 → 可能是 Skill"),
    (re.compile(r'\b(json|xml|output format|schema|输出格式|返回格式|valid json)', re.I),
     "C", "格式约束 → 可能是 schema/validator 层"),
    (re.compile(r'\b(tone|style|empathetic|concise|friendly|persona|语气|简洁|亲切|角色)', re.I),
     "D", "语气/风格 → 属于 Prompt"),
]

def classify_sentence(s: str) -> tuple[str, str]:
    if len(s.strip()) < 10:
        return "skip", ""
    for pattern, bucket, reason in BUCKET_RULES:
        if pattern.search(s):
            return bucket, reason
    return "D", "未命中规则，归 D（请人工核认）"


def analyze_prompt(text: str) -> tuple[dict, list[str]]:
    sentences = re.split(r'(?<=[.。!！?？])\s+|\n{2,}', text)
    counts: dict[str, int] = defaultdict(int)
    e_items = []
    for s in sentences:
        s = s.strip()
        if len(s) < 10:
            continue
        bucket, reason = classify_sentence(s)
        if bucket == "skip":
            continue
        counts[bucket] += 1
        if bucket == "E":
            e_items.append(f"「{s[:100]}」  ← {reason}")
    return dict(counts), e_items


def format_report(report: ScanReport) -> str:
    lines = [
        "=" * 60,
        "PRINCIPLED SIMPLICITY SCAN — 观测报告 / Observation Report",
        f"路径: {report.path}",
        "=" * 60,
        "",
        "本报告只呈现观测事实，不做诊断判断。",
        "把报告贴给 Claude，说：",
        "「根据这份报告，用 Principled Simplicity skill 诊断根因，给出修复层级判决。」",
        "",
    ]

    if report.observations or report.file_count:
        lines += [f"📂 代码扫描  ({report.file_count} 个文件)", "─" * 40]
        KIND_LABEL = {
            "if_else_on_intent": "if/else 处理用户意图（非 schema 校验）",
            "keyword_list":      "关键词/规则列表赋值",
            "regex_on_input":    "正则用于用户输入匹配",
            "patch_comment":     "补丁/workaround 注释",
        }
        by_kind: dict[str, list[Observation]] = defaultdict(list)
        for o in report.observations:
            by_kind[o.kind].append(o)
        for kind, obs_list in by_kind.items():
            label = KIND_LABEL.get(kind, kind)
            lines.append(f"\n  [{label}] — {len(obs_list)} 处")
            for o in obs_list[:4]:
                lines.append(f"    {Path(o.file).name}:{o.line}  {o.snippet[:80]}")
            if len(obs_list) > 4:
                lines.append(f"    … 还有 {len(obs_list)-4} 处")
        if report.notes:
            lines += ["", "  跨文件观测:"] + [f"  {n}" for n in report.notes]

    if report.prompt_buckets:
        lines += ["", "📝 Prompt 结构分析", "─" * 40]
        total = sum(report.prompt_buckets.values())
        BUCKET_LABEL = {
            "A": "产品事实     → Wiki/Memory",
            "B": "流程方法     → Skill",
            "C": "确定性约束   → Code/Validator",
            "D": "语义/风格    → 留在 Prompt ✓",
            "E": "条件分支     → 待决策",
        }
        for b in "ABCDE":
            n = report.prompt_buckets.get(b, 0)
            pct = n / total * 100 if total else 0
            bar = "█" * int(pct / 5)
            lines.append(f"  {b}: {bar:<20} {pct:4.0f}%  ({n})  {BUCKET_LABEL[b]}")
        d_pct = report.prompt_buckets.get("D", 0) / total * 100 if total else 100
        lines.append(f"\n  D 类占比: {d_pct:.0f}%  （健康基准 ≥ 70%，仅供参考）")
        if report.prompt_e_items:
            lines += [f"\n  E 类明细（{len(report.prompt_e_items)} 条，可能是未决产品决策）:"]
            lines += [f"  {item}" for item in report.prompt_e_items[:6]]
            if len(report.prompt_e_items) > 6:
                lines.append(f"  … 还有 {len(report.prompt_e_items)-6} 条")

    lines += ["", "=" * 60]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(0)

    if args[0] == "--prompt" and len(args) > 1:
        target = Path(args[1])
        if not target.exists():
            print(f"文件不存在: {target}"); sys.exit(1)
        b, e = analyze_prompt(target.read_text(encoding="utf-8", errors="replace"))
        report = ScanReport(path=str(target), prompt_buckets=b, prompt_e_items=e)

    elif args[0] == "--full" and len(args) > 1:
        target = Path(args[1])
        if not target.exists():
            print(f"路径不存在: {target}"); sys.exit(1)
        report = scan_codebase(target) if target.is_dir() else ScanReport(path=str(target))
        search_root = target if target.is_dir() else target.parent
        for f in list(search_root.rglob("*.txt")) + list(search_root.rglob("*.md")):
            if any(skip in f.parts for skip in SKIP_DIRS):
                continue
            try:
                snippet = f.read_text(errors="replace")[:300].lower()
                if any(m.lower() in snippet for m in PROMPT_MARKERS):
                    b, e = analyze_prompt(f.read_text(errors="replace"))
                    for k, v in b.items():
                        report.prompt_buckets[k] = report.prompt_buckets.get(k, 0) + v
                    report.prompt_e_items.extend(e)
                    report.notes.insert(0, f"Prompt 文件: {f.name}")
                    break
            except Exception:
                continue

    else:
        target = Path(args[0])
        if not target.exists():
            print(f"路径不存在: {target}"); sys.exit(1)
        if target.is_dir():
            report = scan_codebase(target)
        elif target.suffix in CODE_EXTENSIONS:
            report = ScanReport(path=str(target), file_count=1,
                                observations=scan_file(target))
        else:
            b, e = analyze_prompt(target.read_text(encoding="utf-8", errors="replace"))
            report = ScanReport(path=str(target), prompt_buckets=b, prompt_e_items=e)

    print(format_report(report))


if __name__ == "__main__":
    main()
