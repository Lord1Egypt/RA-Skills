#!/usr/bin/env python3
"""
security_scan.py — 确定性安全检查脚本
用于扫描 skill/prompt/MCP 文件中的安全隐患

用法:
  python3 security_scan.py <file_path> [--check-name <name>] [--known-skills <path>]
  python3 security_scan.py --version

输出: JSON 到 stdout
退出码: 0=clean, 2=有 critical/high 发现, 1=运行错误
"""
import argparse
import base64
import json
import re
import sys
import unicodedata
from pathlib import Path

__version__ = "1.1.0"


# === Unicode 同形字归一化 ===

# 常见西里尔/希腊字母 → ASCII 映射
CONFUSABLES = {
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0441": "c", "\u0445": "x", "\u0443": "y", "\u0456": "i",
    "\u0422": "T", "\u041d": "H", "\u041c": "M", "\u0412": "B",
    "\u0410": "A", "\u0415": "E", "\u041e": "O", "\u0421": "C",
    "\u03bf": "o", "\u03b1": "a", "\u03b5": "e",  # 希腊
    "\uff41": "a", "\uff42": "b", "\uff43": "c",  # 全角
}


def normalize_unicode(text):
    """NFKC 归一化 + 替换常见同形字"""
    text = unicodedata.normalize("NFKC", text)
    for char, replacement in CONFUSABLES.items():
        text = text.replace(char, replacement)
    return text


# === 检测规则 ===

# Prompt injection 模式（severity: critical/high/medium）
INJECTION_PATTERNS = [
    # Critical
    {"pattern": r"ignore\s+(all\s+)?previous\s+instructions", "severity": "critical", "name": "ignore_instructions"},
    {"pattern": r"forget\s+(everything|all)\s+(above|before)", "severity": "critical", "name": "forget_instructions"},
    {"pattern": r"you\s+are\s+now\b", "severity": "critical", "name": "role_override"},
    {"pattern": r"system\s+prompt\s+override", "severity": "critical", "name": "system_override"},
    {"pattern": r"new\s+instructions?\s*:", "severity": "critical", "name": "new_instructions"},
    # High
    {"pattern": r"\[(SYSTEM|ADMIN|ROOT|ASSISTANT)\]", "severity": "high", "name": "fake_role_tag"},
    {"pattern": r"debug\s+mode\s*:\s*(enabled|on|true)", "severity": "high", "name": "debug_mode"},
    {"pattern": r"safety\s+mode\s*:\s*(off|disabled|false)", "severity": "high", "name": "safety_mode_off"},
    {"pattern": r"admin\s+mode\s*(activated|enabled|on)", "severity": "high", "name": "admin_mode"},
    # Medium
    {"pattern": r"note\s+to\s+(ai|assistant|agent)\s*:", "severity": "medium", "name": "note_to_ai"},
    {"pattern": r"(?:i[''`]?m|i\s+am)\s+the\s+developer", "severity": "medium", "name": "social_developer"},
    {"pattern": r"the\s+security\s+check\s+is\s+broken", "severity": "medium", "name": "social_bypass"},
    {"pattern": r"other\s+ai\s+assistants?\s+do\s+this", "severity": "medium", "name": "social_pressure"},
]

# 危险命令模式（2.1 修复：curl/wget 模式放宽，支持中间有 flags）
DANGEROUS_PATTERNS = [
    {"pattern": r"curl\s+.*\|\s*(?:ba)?sh", "severity": "critical", "name": "curl_pipe_bash"},
    {"pattern": r"wget\s+.*\|\s*(?:ba)?sh", "severity": "critical", "name": "wget_pipe_bash"},
    {"pattern": r"\brm\s+-[rR]f\b", "severity": "high", "name": "rm_rf"},
    {"pattern": r"\bsudo\b", "severity": "high", "name": "sudo"},
    {"pattern": r"\bchmod\s+777\b", "severity": "high", "name": "chmod_777"},
    {"pattern": r"\beval\s*\(", "severity": "medium", "name": "eval_call"},
    {"pattern": r"\bexec\s*\(", "severity": "medium", "name": "exec_call"},
    {"pattern": r"\bchild_process\b", "severity": "medium", "name": "child_process"},
    {"pattern": r"\bspawn\s*\(", "severity": "medium", "name": "spawn_call"},
    {"pattern": r"dangerouslyDisableSandbox", "severity": "critical", "name": "disable_sandbox"},
    {"pattern": r"--no-verify", "severity": "medium", "name": "no_verify"},
]

# 数据外传模式
DATA_EXFIL_PATTERNS = [
    {"pattern": r"curl\s+.*(?:-d\s+@|--data.*@|--upload-file)", "severity": "critical", "name": "curl_data_exfil"},
    {"pattern": r"wget\s+.*--post-file", "severity": "critical", "name": "wget_data_exfil"},
    {"pattern": r"\bnc\s+\S+\s+\d+", "severity": "high", "name": "netcat_connection"},
    {"pattern": r"curl\s+.*-X\s+POST", "severity": "medium", "name": "curl_post"},
]

# 凭证访问模式（3.3 修复：增加 $HOME 变体）
CREDENTIAL_PATTERNS = [
    {"pattern": r"~/\.ssh\b|\.ssh/|\$\{?HOME\}?/\.ssh", "severity": "high", "name": "ssh_access"},
    {"pattern": r"~/\.aws\b|\.aws/|\$\{?HOME\}?/\.aws", "severity": "high", "name": "aws_access"},
    {"pattern": r"~/\.env\b|\.env\b|\$\{?HOME\}?/\.env", "severity": "high", "name": "env_access"},
    {"pattern": r"\.credentials\b|credentials\.json", "severity": "high", "name": "credentials_access"},
    {"pattern": r"~/\.bashrc|~/\.zshrc|~/\.profile", "severity": "medium", "name": "shell_config_access"},
    {"pattern": r"\bcrontab\b|/etc/cron", "severity": "medium", "name": "crontab_access"},
]

# CSS/样式隐藏
OBFUSCATION_PATTERNS = [
    {"pattern": r"display\s*:\s*none", "severity": "medium", "name": "css_display_none"},
    {"pattern": r"visibility\s*:\s*hidden", "severity": "medium", "name": "css_visibility_hidden"},
    {"pattern": r"font-size\s*:\s*0", "severity": "medium", "name": "css_font_zero"},
]

# 零宽字符
ZERO_WIDTH_CHARS = ["\u200b", "\u200c", "\u200d", "\ufeff"]

# HTML 注释中的隐藏指令
HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)

MAX_SCAN_SIZE = 50 * 1024  # 50KB


def decode_base64_strings(text):
    """查找并解码 base64 字符串（支持递归一层解码）"""
    findings = []
    b64_pattern = re.compile(r"[A-Za-z0-9+/]{20,}={0,2}")

    def _check_decoded(decoded, original_match, line_offset):
        """检查解码内容是否可疑"""
        if any(re.search(p["pattern"], decoded, re.IGNORECASE) for p in INJECTION_PATTERNS):
            findings.append({
                "category": "obfuscation",
                "severity": "high",
                "pattern": "base64_injection",
                "location": {"line": line_offset, "context": original_match[:60]},
                "raw_match": f"base64 decoded: {decoded[:100]}",
            })
            return True
        return False

    for match in b64_pattern.finditer(text):
        try:
            decoded = base64.b64decode(match.group()).decode("utf-8", errors="ignore")
            line_num = text[:match.start()].count("\n") + 1
            if _check_decoded(decoded, match.group(), line_num):
                continue
            # 3.1 修复：递归一层，检查双重 base64
            inner_matches = b64_pattern.findall(decoded)
            for inner in inner_matches:
                try:
                    inner_decoded = base64.b64decode(inner).decode("utf-8", errors="ignore")
                    _check_decoded(inner_decoded, match.group(), line_num)
                except Exception:
                    pass
        except Exception:
            pass
    return findings


def detect_zero_width(text):
    """检测零宽字符"""
    findings = []
    for i, line in enumerate(text.split("\n"), 1):
        for char in ZERO_WIDTH_CHARS:
            if char in line:
                findings.append({
                    "category": "obfuscation",
                    "severity": "medium",
                    "pattern": "zero_width_char",
                    "location": {"line": i, "context": repr(line[:80])},
                    "raw_match": f"U+{ord(char):04X}",
                })
                break  # 每行只报一次
    return findings


def detect_html_hidden(text):
    """检测 HTML 注释中的隐藏指令"""
    findings = []
    for match in HTML_COMMENT_RE.finditer(text):
        content = match.group(1).strip()
        for p in INJECTION_PATTERNS + DANGEROUS_PATTERNS:
            if re.search(p["pattern"], content, re.IGNORECASE):
                findings.append({
                    "category": "prompt_injection",
                    "severity": "high",
                    "pattern": "html_comment_hidden",
                    "location": {"line": text[:match.start()].count("\n") + 1,
                                 "context": content[:80]},
                    "raw_match": content[:100],
                })
                break
    return findings


def detect_patterns(text, patterns, category):
    """通用模式匹配（3.4 修复：同行同模式去重）"""
    findings = []
    seen = set()
    for p in patterns:
        for match in re.finditer(p["pattern"], text, re.IGNORECASE):
            line_num = text[:match.start()].count("\n") + 1
            dedup_key = (category, p["name"], line_num)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            lines = text.split("\n")
            line_text = lines[line_num - 1] if line_num <= len(lines) else ""
            findings.append({
                "category": category,
                "severity": p["severity"],
                "pattern": p["name"],
                "location": {"line": line_num, "context": line_text.strip()[:80]},
                "raw_match": match.group()[:100],
            })
    return findings


def detect_typosquat(name, known_skills_path):
    """检测名称是否与已知 skill 过于相似"""
    findings = []
    if not name or not known_skills_path:
        return findings

    known_path = Path(known_skills_path)
    if not known_path.exists():
        return findings

    known_names = []
    for line in known_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            known_names.append(line.lower())

    name_lower = name.lower()
    if name_lower in known_names:
        return findings

    for known in known_names:
        dist = _edit_distance(name_lower, known)
        if 0 < dist <= 2 and len(name_lower) > 3:
            findings.append({
                "category": "typosquat",
                "severity": "high",
                "pattern": "edit_distance",
                "location": {"line": 0, "context": f"名称 '{name}' 与已知 skill '{known}' 相似"},
                "raw_match": f"编辑距离: {dist}",
            })
            break

    homoglyphs = {"1": "l", "l": "1", "0": "o", "o": "0", "rn": "m", "m": "rn"}
    for old, new in homoglyphs.items():
        variant = name_lower.replace(old, new)
        if variant != name_lower and variant in known_names:
            findings.append({
                "category": "typosquat",
                "severity": "high",
                "pattern": "homoglyph",
                "location": {"line": 0, "context": f"名称 '{name}' 可能是 '{variant}' 的同形字变体"},
                "raw_match": f"{old} -> {new}",
            })
            break
    return findings


def _edit_distance(s1, s2):
    """Levenshtein 编辑距离"""
    if len(s1) < len(s2):
        return _edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[len(s2)]


def decode_url_encoded(text):
    """检测并解码 URL 编码内容"""
    findings = []
    url_pattern = re.compile(r"(?:%[0-9A-Fa-f]{2}){3,}")
    for match in url_pattern.finditer(text):
        try:
            from urllib.parse import unquote
            decoded = unquote(match.group())
            if any(re.search(p["pattern"], decoded, re.IGNORECASE) for p in INJECTION_PATTERNS + DANGEROUS_PATTERNS):
                findings.append({
                    "category": "obfuscation",
                    "severity": "high",
                    "pattern": "url_encoded_injection",
                    "location": {"line": text[:match.start()].count("\n") + 1,
                                 "context": match.group()[:60]},
                    "raw_match": f"URL decoded: {decoded[:100]}",
                })
        except Exception:
            pass
    return findings


def assess_permissions(text):
    """评估文件中暗示的权限范围"""
    findings = []
    has_network = bool(re.search(r"\b(fetch|curl|wget|axios|request)\s*\(", text, re.IGNORECASE)) or \
                  bool(re.search(r"\b(curl|wget)\s+\S", text, re.IGNORECASE))
    has_shell = bool(re.search(r"\b(shell|bash|exec|spawn|child_process|subprocess)\b", text, re.IGNORECASE))
    if has_network and has_shell:
        findings.append({
            "category": "permission_scope",
            "severity": "high",
            "pattern": "network_plus_shell",
            "location": {"line": 0, "context": "同时需要 network + shell 权限（数据外传风险）"},
            "raw_match": "network + shell combination detected",
        })
    elif has_shell:
        findings.append({
            "category": "permission_scope",
            "severity": "medium",
            "pattern": "shell_access",
            "location": {"line": 0, "context": "需要 shell 权限"},
            "raw_match": "shell access detected",
        })
    elif has_network:
        findings.append({
            "category": "permission_scope",
            "severity": "low",
            "pattern": "network_access",
            "location": {"line": 0, "context": "需要 network 权限"},
            "raw_match": "network access detected",
        })
    return findings


def scan_file(file_path, check_name=None, known_skills_path=None):
    """扫描单个文件，返回结果 dict"""
    path = Path(file_path)

    # 4.1 修复：文件不存在时优雅处理
    if not path.exists():
        return {
            "scan_target": str(file_path),
            "error": f"文件不存在: {file_path}",
            "findings": [],
            "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "clean": True},
        }

    # 大小限制
    file_size = path.stat().st_size
    if file_size > MAX_SCAN_SIZE:
        text = path.read_text(encoding="utf-8", errors="ignore")[:MAX_SCAN_SIZE]
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")

    # 2.2 修复：Unicode 同形字归一化（在原文上检测零宽字符后再归一化）
    raw_text = text
    text = normalize_unicode(text)

    all_findings = []

    # 1. Prompt injection
    all_findings.extend(detect_patterns(text, INJECTION_PATTERNS, "prompt_injection"))

    # 2. 危险命令
    all_findings.extend(detect_patterns(text, DANGEROUS_PATTERNS, "dangerous_command"))

    # 3. 数据外传
    all_findings.extend(detect_patterns(text, DATA_EXFIL_PATTERNS, "data_exfiltration"))

    # 4. 凭证访问
    all_findings.extend(detect_patterns(text, CREDENTIAL_PATTERNS, "credential_access"))

    # 5. CSS/样式隐藏
    all_findings.extend(detect_patterns(text, OBFUSCATION_PATTERNS, "obfuscation"))

    # 6. Base64 混淆
    all_findings.extend(decode_base64_strings(text))

    # 7. URL 编码混淆
    all_findings.extend(decode_url_encoded(text))

    # 8. 零宽字符（用原始文本检测，归一化前）
    all_findings.extend(detect_zero_width(raw_text))

    # 9. HTML 隐藏内容
    all_findings.extend(detect_html_hidden(text))

    # 10. 权限范围评估
    all_findings.extend(assess_permissions(text))

    # 11. Typosquat
    if check_name:
        all_findings.extend(detect_typosquat(check_name, known_skills_path))

    # 汇总
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in all_findings:
        sev = f["severity"]
        if sev in severity_counts:
            severity_counts[sev] += 1

    return {
        "scan_target": str(file_path),
        "findings": all_findings,
        "summary": {
            **severity_counts,
            "clean": len(all_findings) == 0,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="安全扫描脚本")
    parser.add_argument("file", nargs="?", help="要扫描的文件路径")
    parser.add_argument("--check-name", help="要检查 typosquat 的名称")
    parser.add_argument("--known-skills", help="known_skills.txt 路径")
    parser.add_argument("--version", action="version", version=f"security_scan.py {__version__}")
    args = parser.parse_args()

    if not args.file:
        parser.error("必须指定要扫描的文件路径")

    result = scan_file(args.file, args.check_name, args.known_skills)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 2.3 修复：exit code 区分 clean/dirty
    if result["summary"]["critical"] > 0 or result["summary"]["high"] > 0:
        sys.exit(2)


if __name__ == "__main__":
    main()
