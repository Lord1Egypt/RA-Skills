"""TEST FIXTURE — NOT THE SKILL IMPLEMENTATION / 测试样本，非技能实现。
variable name. No credential in here; it just matches text against a few patterns and writes JSON.

CodeQL 敏感名启发式误报的最小复现：成对使用，两份除变量名外逐字节相同。此文件不含任何凭据，
只做「用几个正则匹配文本、把结果写进 JSON」。哪一份触发告警、为什么，见 ../README.md。
"""
import json
from pathlib import Path

CREDENTIAL_PATTERNS = ["sk-[A-Za-z0-9]{20,}", "ghp_[A-Za-z0-9]{36}"]


def detect(text):
    for pat in CREDENTIAL_PATTERNS:
        if pat in text:
            return pat
    return ""


def main(out):
    findings = {"hit": detect("hello world")}
    Path(out).write_text(json.dumps(findings), encoding="utf-8")


main("report.json")
