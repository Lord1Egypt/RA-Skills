#!/usr/bin/env python3
"""
🔐 API Key Guardian — 敏感信息安全扫描
用法:
  python3 guardian.py                        # 扫描当前目录
  python3 guardian.py --path /some/dir       # 扫描指定目录
  python3 guardian.py --file /path/to/.env   # 扫描单个文件
  python3 guardian.py --git-history          # 扫描 git 提交历史
  python3 guardian.py --ai                   # 启用 AI 风险分析
"""
import re, os, sys, argparse, subprocess, json, urllib.request
from pathlib import Path
from patterns import PATTERNS, SKIP_DIRS, SKIP_EXTS, SKIP_FILES, SEVERITY_ORDER

# ANSI 颜色
R  = "\033[0m"
BOLD = "\033[1m"
RED  = "\033[91m"
YEL  = "\033[93m"
GRN  = "\033[92m"
GRAY = "\033[90m"
CYN  = "\033[96m"

SEVERITY_COLOR = {"critical": RED+BOLD, "high": RED, "medium": YEL, "low": GRAY}
SEVERITY_ICON  = {"critical": "🔴", "high": "🔴", "medium": "🟡", "low": "⚪"}


def mask(text: str) -> str:
    """脱敏：保留前4后4，中间替换为..."""
    if len(text) <= 10:
        return text[:2] + "..." + text[-2:]
    return text[:4] + "..." + text[-4:]


def scan_text(content: str, source: str) -> list:
    findings = []
    for pattern in PATTERNS:
        for m in re.finditer(pattern["regex"], content):
            # 找到行号
            line_no = content[:m.start()].count("\n") + 1
            matched = m.group(0)
            # 对于 Generic Secret，取第2个捕获组
            if pattern["name"] == "Generic Secret" and m.lastindex and m.lastindex >= 2:
                matched = m.group(0)  # 整体匹配用于显示
            findings.append({
                "pattern": pattern["name"],
                "severity": pattern["severity"],
                "source": source,
                "line": line_no,
                "raw": matched,
                "masked": mask(matched),
            })
    return findings


def scan_file(path: Path) -> list:
    if path.suffix.lower() in SKIP_EXTS:
        return []
    if path.name in SKIP_FILES:
        return []
    try:
        content = path.read_text(errors="replace")
        return scan_text(content, str(path))
    except Exception:
        return []


def scan_dir(root: Path) -> list:
    findings = []
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # 跳过不需要扫描的目录
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            fp = Path(dirpath) / fname
            results = scan_file(fp)
            findings.extend(results)
            file_count += 1
    return findings, file_count


def scan_git_history(repo_path: Path, max_commits: int = 100) -> list:
    findings = []
    try:
        result = subprocess.run(
            ["git", "log", f"--max-count={max_commits}", "--pretty=format:%H %s", "--name-only"],
            cwd=repo_path, capture_output=True, text=True, timeout=30
        )
        commits_raw = subprocess.run(
            ["git", "log", f"--max-count={max_commits}", "--pretty=format:%H", "-p"],
            cwd=repo_path, capture_output=True, text=True, timeout=60
        )
        if commits_raw.returncode == 0:
            results = scan_text(commits_raw.stdout, "git-history")
            findings.extend(results)
    except Exception as e:
        print(f"{GRAY}git history 扫描失败: {e}{R}")
    return findings


def llm_analyze(findings: list) -> str:
    summary = "\n".join([
        f"- {f['pattern']} ({f['severity']}) 在 {f['source']} 第{f['line']}行"
        for f in findings[:10]
    ])
    prompt = f"""以下是代码扫描发现的敏感信息问题，请用中文简洁说明每个的风险和修复建议：

{summary}

请逐条回答，格式：
1. [问题名] - 风险：xxx | 修复：xxx
"""
    try:
        url = "http://127.0.0.1:18790/anthropic/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "sk-RPBUoe2SH7KigJ0SZn6IPDirZtJ2fUaWSukEx1FwxjhWFx0G",
            "anthropic-version": "2023-06-01"
        }
        data = json.dumps({
            "model": "ppio/pa/claude-sonnet-4-6",
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["content"][0]["text"]
    except Exception as e:
        return f"AI 分析失败: {e}"


def print_findings(findings: list, file_count: int = 0):
    print(f"\n{BOLD}🔐 API Key Guardian 扫描报告{R}")
    if file_count:
        print(f"{GRAY}扫描文件：{file_count} 个 | 发现问题：{len(findings)} 处{R}")
    print(f"\n{'─'*60}")

    if not findings:
        print(f"{GRN}✅ 未发现敏感信息泄露，看起来很安全！{R}")
        return

    # 按严重程度排序
    findings.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 9))

    for f in findings:
        col = SEVERITY_COLOR.get(f["severity"], "")
        icon = SEVERITY_ICON.get(f["severity"], "⚪")
        print(f"\n{icon} {col}{f['severity'].upper()}: {f['pattern']}{R}")
        print(f"  {GRAY}文件：{f['source']} · 第{f['line']}行{R}")
        print(f"  内容：{CYN}{f['masked']}{R}")

    print(f"\n{'─'*60}")
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    for sev in ["critical", "high", "medium", "low"]:
        if sev in counts:
            col = SEVERITY_COLOR.get(sev, "")
            print(f"  {col}{sev.upper()}: {counts[sev]} 处{R}")


def main():
    parser = argparse.ArgumentParser(description="🔐 API Key Guardian — 敏感信息扫描")
    parser.add_argument("--path",        default=".", help="扫描目录路径")
    parser.add_argument("--file",        help="扫描单个文件")
    parser.add_argument("--git-history", action="store_true", help="扫描 git 提交历史")
    parser.add_argument("--ai",          action="store_true", help="启用 AI 风险分析")
    args = parser.parse_args()

    findings = []
    file_count = 0

    if args.file:
        fp = Path(args.file)
        findings = scan_file(fp)
        file_count = 1
    elif args.git_history:
        findings = scan_git_history(Path(args.path))
        print(f"{GRAY}已扫描 git history（最近100次提交）{R}")
    else:
        root = Path(args.path).resolve()
        print(f"{GRAY}正在扫描：{root} ...{R}")
        findings, file_count = scan_dir(root)

    print_findings(findings, file_count)

    if args.ai and findings:
        print(f"\n{BOLD}🤖 AI 风险分析{R}")
        print(f"{'─'*60}")
        analysis = llm_analyze(findings)
        print(analysis)

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
