#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
from pathlib import Path

# ====== 检测规则 ======
PYTHON_PATTERNS = {
    "env": [r"os\.environ", r"os\.getenv"],
    "network": [r"requests\.", r"httpx\.", r"urllib", r"socket"],
    "encode": [r"base64", r"b64encode"],
    "exec": [r"subprocess", r"os\.system", r"eval\("],
}

BASH_PATTERNS = {
    "env": [r"\benv\b", r"\bprintenv\b", r"\$\{?[A-Z_]+\}?"],
    "network": [r"curl", r"wget", r"nc", r"netcat"],
    "exec": [r"\bbash\b", r"\bsh\b"],
}


# ====== 风险评分 ======
def risk_score(flags):
    score = 0

    if flags["env"]:
        score += 2
    if flags["network"]:
        score += 3
    if flags["encode"]:
        score += 2
    if flags["exec"]:
        score += 2

    if score >= 6:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    else:
        return "CLEAN"

def detect_type(filepath, content):
    if filepath.endswith(".py"):
        return "python"
    elif filepath.endswith(".sh"):
        return "bash"
    elif content.startswith("#!/") and "python" in content.split("\n")[0]:
        return "python"
    elif content.startswith("#!/") and ("bash" in content.split("\n")[0] or "sh" in content.split("\n")[0]):
        return "bash"
    return "unknown"

# ====== 扫描文件 ======
def scan_file(filepath):
    try:
        content = Path(filepath).read_text(errors="ignore")
    except Exception:
        return None
    
    ftype = detect_type(filepath, content)
    #is_python = filepath.endswith(".py")
    if ftype == "python":
        patterns = PYTHON_PATTERNS
    elif ftype == "bash":
        patterns = BASH_PATTERNS
    else:
        #patterns = {}
        return None
    

    findings = []
    flags = {"env": False, "network": False, "encode": False, "exec": False}

    for category, regex_list in patterns.items():
        for regex in regex_list:
            if re.search(regex, content):
                findings.append((category, regex))
                flags[category] = True

    return {
        "file": filepath,
        "type": ftype,
        "risk": risk_score(flags),
        "findings": findings,
    }


# ====== 扫描路径 ======
def scan_path(path):
    results = []
    p = Path(path)

    if p.is_file():
        res = scan_file(str(p))
        if res:
            results.append(res)
        return results

    for file in p.rglob("*"):
        if file.suffix in [".py", ".sh"]:
            res = scan_file(str(file))
            if res:
                results.append(res)

    return results


# ====== 输出 ======
def print_report(results, show_all=False):
    for r in results:
        if not show_all and r["risk"] == "CLEAN":
            continue

        print(f"\nFILE: {r['file']}")
        print(f"TYPE: {r['type']}")
        print(f"RISK: {r['risk']}")

        if r["findings"]:
            print("FINDINGS:")
            for cat, rule in r["findings"]:
                print(f"  - [{cat}] {rule}")


# ====== CLI ======
def main():
    parser = argparse.ArgumentParser(
        description="ENV Leak Detector (Python + Bash)"
    )

    parser.add_argument("target", help="File or directory to scan")

    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all files (including clean)",
    )

    args = parser.parse_args()

    results = scan_path(args.target)
    print_report(results, show_all=args.all)


if __name__ == "__main__":
    main()
