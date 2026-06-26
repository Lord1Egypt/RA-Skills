#!/usr/bin/env python3
"""
diff-analysis.py — OpenEuler 基线 vs CIS Benchmark 差异分析

从基线目录读取收集到的系统配置，与 CIS Benchmark 映射表中的
期望值进行比较，输出合规审计报告。

用法:
    python3 diff-analysis.py <基线目录> [输出报告路径]
    python3 diff-analysis.py baseline-20250101-120000
    python3 diff-analysis.py baseline-20250101-120000 report.md

依赖:
    Python 3.6+
    yaml (pip install pyyaml) — 可选，用于读取 YAML 配置
"""

import os
import sys
import re
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ============================================================
# CIS Benchmark 映射定义（内嵌默认映射）
# 如需自定义，可复制此结构到 references/custom-mapping.json
# ============================================================

CIS_MAPPING = [
    # ---- 1.1 文件系统 ----
    {
        "id": "1.1.1.1",
        "title": "禁用 cramfs 文件系统",
        "level": "L1",
        "section": "文件系统",
        "expected": "cramfs: 0",
        "check_type": "file_contains",
        "check_path": "disabled-modules.txt",
        "check_pattern": r"^cramfs:\s*0$",
        "description": "lsmod 不应显示 cramfs 已加载"
    },
    {
        "id": "1.1.1.2",
        "title": "禁用 freevxfs 文件系统",
        "level": "L1",
        "section": "文件系统",
        "expected": "freevxfs: 0",
        "check_type": "file_contains",
        "check_path": "disabled-modules.txt",
        "check_pattern": r"^freevxfs:\s*0$",
    },
    {
        "id": "1.1.1.6",
        "title": "禁用 squashfs 文件系统",
        "level": "L1",
        "section": "文件系统",
        "expected": "squashfs: 0",
        "check_type": "file_contains",
        "check_path": "disabled-modules.txt",
        "check_pattern": r"^squashfs:\s*0$",
    },
    {
        "id": "1.1.2",
        "title": "独立 /tmp 分区",
        "level": "L1",
        "section": "文件系统",
        "expected": "/tmp 应有单独分区",
        "check_type": "file_contains",
        "check_path": "mounts.txt",
        "check_pattern": r"\s/tmp\s",
    },
    {
        "id": "1.1.3",
        "title": "/tmp 启用 nodev",
        "level": "L1",
        "section": "文件系统",
        "expected": "/tmp 挂载选项含 nodev",
        "check_type": "file_contains",
        "check_path": "mounts.txt",
        "check_pattern": r"\s/tmp\s.*nodev",
    },
    {
        "id": "1.1.6",
        "title": "独立 /var 分区",
        "level": "L1",
        "section": "文件系统",
        "expected": "/var 应有单独分区",
        "check_type": "file_contains",
        "check_path": "mounts.txt",
        "check_pattern": r"\s/var\s",
    },
    {
        "id": "1.1.8",
        "title": "独立 /var/log 分区",
        "level": "L1",
        "section": "文件系统",
        "expected": "/var/log 应有单独分区",
        "check_type": "file_contains",
        "check_path": "mounts.txt",
        "check_pattern": r"\s/var/log\s",
    },
    {
        "id": "1.1.10",
        "title": "独立 /home 分区",
        "level": "L1",
        "section": "文件系统",
        "expected": "/home 应有单独分区",
        "check_type": "file_contains",
        "check_path": "mounts.txt",
        "check_pattern": r"\s/home\s",
    },

    # ---- 1.5 内核加固 ----
    {
        "id": "1.5.3",
        "title": "ASLR 启用 (kernel.randomize_va_space)",
        "level": "L1",
        "section": "内核参数",
        "expected": "kernel.randomize_va_space = 2",
        "check_type": "file_contains",
        "check_path": "sysctl-params.txt",
        "check_pattern": r"kernel\.randomize_va_space\s*=\s*2",
    },
    {
        "id": "3.1.1",
        "title": "IP 转发禁用",
        "level": "L1",
        "section": "内核参数",
        "expected": "net.ipv4.ip_forward = 0",
        "check_type": "file_contains",
        "check_path": "sysctl-params.txt",
        "check_pattern": r"net\.ipv4\.ip_forward\s*=\s*0",
    },
    {
        "id": "3.1.6",
        "title": "TCP SYN cookies 启用",
        "level": "L1",
        "section": "内核参数",
        "expected": "net.ipv4.tcp_syncookies = 1",
        "check_type": "file_contains",
        "check_path": "sysctl-params.txt",
        "check_pattern": r"net\.ipv4\.tcp_syncookies\s*=\s*1",
    },
    {
        "id": "3.1.3",
        "title": "ICMP redirect 不接受",
        "level": "L1",
        "section": "内核参数",
        "expected": "net.ipv4.conf.all.accept_redirects = 0",
        "check_type": "file_contains",
        "check_path": "sysctl-params.txt",
        "check_pattern": r"net\.ipv4\.conf\.all\.accept_redirects\s*=\s*0",
    },
    {
        "id": "3.1.7",
        "title": "日志伪造包 (log_martians)",
        "level": "L2",
        "section": "内核参数",
        "expected": "net.ipv4.conf.all.log_martians = 1",
        "check_type": "file_contains",
        "check_path": "sysctl-params.txt",
        "check_pattern": r"net\.ipv4\.conf\.all\.log_martians\s*=\s*1",
    },

    # ---- 1.6 SELinux ----
    {
        "id": "1.6.1.2",
        "title": "SELinux 未禁用",
        "level": "L1",
        "section": "SELinux",
        "expected": "SELINUX 不应为 disabled",
        "check_type": "file_contains",
        "check_path": "selinux.txt",
        "check_pattern": r"SELINUX=disabled",
        "invert": True,
    },

    # ---- 2.2 SSH ----
    {
        "id": "2.2.1",
        "title": "SSH Protocol 2",
        "level": "L1",
        "section": "SSH",
        "expected": "protocol 2",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"protocol\s+2",
    },
    {
        "id": "2.2.3",
        "title": "X11Forwarding disabled",
        "level": "L1",
        "section": "SSH",
        "expected": "X11Forwarding no",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"x11forwarding\s+no",
    },
    {
        "id": "2.2.4",
        "title": "MaxAuthTries ≤ 4",
        "level": "L1",
        "section": "SSH",
        "expected": "MaxAuthTries ≤ 4",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"maxauthtries\s+([0-4]$)",
    },
    {
        "id": "2.2.7",
        "title": "PermitRootLogin no",
        "level": "L1",
        "section": "SSH",
        "expected": "PermitRootLogin no",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"permitrootlogin\s+no",
    },
    {
        "id": "2.2.8",
        "title": "PermitEmptyPasswords no",
        "level": "L1",
        "section": "SSH",
        "expected": "PermitEmptyPasswords no",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"permitemptypasswords\s+no",
    },
    {
        "id": "2.2.12",
        "title": "ClientAliveInterval ≤ 300",
        "level": "L1",
        "section": "SSH",
        "expected": "ClientAliveInterval ≤ 300",
        "check_type": "file_contains",
        "check_path": "sshd-config.txt",
        "check_pattern": r"optionalclientalivecountmax\s+(\d+)",
        "custom_check": "check_client_alive_interval",
    },

    # ---- 3.3 网络协议 ----
    {
        "id": "3.3.1",
        "title": "禁用 DCCP",
        "level": "L2",
        "section": "网络协议",
        "expected": "DCCP 未加载",
        "check_type": "file_contains",
        "check_path": "disabled-modules.txt",
        "check_pattern": r"^dccp:\s*0$",
    },
    {
        "id": "3.3.2",
        "title": "禁用 SCTP",
        "level": "L2",
        "section": "网络协议",
        "expected": "SCTP 未加载",
        "check_type": "file_contains",
        "check_path": "disabled-modules.txt",
        "check_pattern": r"^sctp:\s*0$",
    },

    # ---- 4.1 auditd ----
    {
        "id": "4.1.1.1",
        "title": "auditd 已安装",
        "level": "L2",
        "section": "Audit",
        "expected": "audit 包已安装",
        "check_type": "file_contains",
        "check_path": "packages.txt",
        "check_pattern": r"^audit-",
    },
    {
        "id": "4.1.1.2",
        "title": "auditd 已启用并运行",
        "level": "L2",
        "section": "Audit",
        "expected": "auditd active + enabled",
        "check_type": "file_contains",
        "check_path": "services.txt",
        "check_pattern": r"^auditd:.*enabled=.*active=active",
    },

    # ---- 5.1 密码策略 ----
    {
        "id": "5.1.1",
        "title": "密码过期天数 ≤ 365",
        "level": "L1",
        "section": "密码策略",
        "expected": "PASS_MAX_DAYS ≤ 365",
        "check_type": "file_contains",
        "check_path": "password-policy.txt",
        "check_pattern": r"PASS_MAX_DAYS\s+(\d+)",
        "custom_check": "check_pass_max_days",
    },
    {
        "id": "5.1.2",
        "title": "密码最少使用天数 ≥ 7",
        "level": "L1",
        "section": "密码策略",
        "expected": "PASS_MIN_DAYS ≥ 7",
        "check_type": "file_contains",
        "check_path": "password-policy.txt",
        "check_pattern": r"PASS_MIN_DAYS\s+(\d+)",
        "custom_check": "check_pass_min_days",
    },
    {
        "id": "5.2.1",
        "title": "无空密码用户",
        "level": "L1",
        "section": "用户",
        "expected": "无空密码用户",
        "check_type": "file_contains",
        "check_path": "password-policy.txt",
        "check_pattern": r"空密码用户检查.*none",
    },
    {
        "id": "5.2.2",
        "title": "Root 唯一 UID 0",
        "level": "L1",
        "section": "用户",
        "expected": "仅 root 有 UID 0",
        "check_type": "file_contains",
        "check_path": "password-policy.txt",
        "check_pattern": r"UID 0.*root$",
    },
    {
        "id": "5.3.1",
        "title": "sudo 已安装",
        "level": "L1",
        "section": "Sudo",
        "expected": "sudo 包已安装",
        "check_type": "file_contains",
        "check_path": "packages.txt",
        "check_pattern": r"^sudo-",
    },
    {
        "id": "5.3.4",
        "title": "sudo 超时 ≤ 15 min",
        "level": "L1",
        "section": "Sudo",
        "expected": "timestamp_timeout ≤ 15",
        "check_type": "file_contains",
        "check_path": "sudo.txt",
        "check_pattern": r"timestamp_timeout\s*[:=]\s*(\d+)",
        "custom_check": "check_sudo_timeout",
    },
]


def load_custom_mapping(mapping_path: str) -> List[Dict]:
    """尝试从外部 JSON 文件加载自定义映射"""
    path = Path(mapping_path)
    if path.exists():
        import json
        with open(path) as f:
            return json.load(f)
    return CIS_MAPPING


def load_baseline_file(baseline_dir: Path, filename: str) -> str:
    """读取基线文件的内容"""
    filepath = baseline_dir / filename
    if filepath.exists():
        return filepath.read_text()
    return ""


def check_client_alive_interval(content: str) -> Tuple[bool, str]:
    """检查 ClientAliveInterval ≤ 300"""
    match = re.search(r"optionalclientalivecountmax\s+(\d+)", content, re.IGNORECASE)
    if not match:
        return False, "未配置 ClientAliveInterval"
    val = int(match.group(1))
    return (val <= 300), f"ClientAliveInterval={val} {'√' if val <= 300 else '✗'}"


def check_pass_max_days(content: str) -> Tuple[bool, str]:
    """检查 PASS_MAX_DAYS ≤ 365"""
    match = re.search(r"PASS_MAX_DAYS\s+(\d+)", content)
    if not match:
        return False, "PASS_MAX_DAYS 未配置"
    val = int(match.group(1))
    return (val <= 365), f"PASS_MAX_DAYS={val} {'√' if val <= 365 else '✗'}"


def check_pass_min_days(content: str) -> Tuple[bool, str]:
    """检查 PASS_MIN_DAYS ≥ 7"""
    match = re.search(r"PASS_MIN_DAYS\s+(\d+)", content)
    if not match:
        return False, "PASS_MIN_DAYS 未配置"
    val = int(match.group(1))
    return (val >= 7), f"PASS_MIN_DAYS={val} {'√' if val >= 7 else '✗'}"


def check_sudo_timeout(content: str) -> Tuple[bool, str]:
    """检查 sudo timestamp_timeout ≤ 15"""
    match = re.search(r"timestamp_timeout\s*[:=]\s*(\d+)", content, re.IGNORECASE)
    if not match:
        return False, "timestamp_timeout 未配置（默认可能为 15）"
    val = int(match.group(1))
    return (val <= 15), f"timestamp_timeout={val} {'√' if val <= 15 else '✗'}"


def _detect_os_version(baseline_dir: Path) -> str:
    """从基线文件中提取 OpenEuler 版本"""
    content = load_baseline_file(baseline_dir, "system-info.txt")
    match = re.search(r"openEuler\s+(\S+)", content)
    if match:
        return match.group(1)
    match = re.search(r"VERSION_ID=\"?([^\"]+)\"?", content)
    if match:
        return match.group(1)
    return "unknown"


def run_checks(baseline_dir: Path, mapping: List[Dict]) -> List[Dict]:
    """执行所有检查，返回结果列表"""
    results = []

    for item in mapping:
        check_id = item["id"]
        title = item["title"]
        expected = item["expected"]
        section = item.get("section", "通用")
        level = item.get("level", "L1")
        check_path = item.get("check_path", "")
        invert = item.get("invert", False)
        custom_check_fn = item.get("custom_check")

        # 读取需要检查的基线文件
        content = load_baseline_file(baseline_dir, check_path)

        # 自定义检查器
        if custom_check_fn:
            fn_name = custom_check_fn
            fn_map = {
                "check_client_alive_interval": check_client_alive_interval,
                "check_pass_max_days": check_pass_max_days,
                "check_pass_min_days": check_pass_min_days,
                "check_sudo_timeout": check_sudo_timeout,
            }
            if fn_name in fn_map:
                passed, detail = fn_map[fn_name](content)
                results.append({
                    "id": check_id,
                    "title": title,
                    "section": section,
                    "level": level,
                    "expected": expected,
                    "actual": detail,
                    "passed": passed,
                    "status": "PASS" if passed else "FAIL",
                })
            else:
                results.append({
                    "id": check_id,
                    "title": title,
                    "section": section,
                    "level": level,
                    "expected": expected,
                    "actual": "未知自定义检查",
                    "passed": False,
                    "status": "MANUAL",
                })
            continue

        # 正则检查
        if check_path:
            pattern = item.get("check_pattern", "")
            match = re.search(pattern, content, re.IGNORECASE)
            found = match is not None
            if invert:
                passed = not found
                detail = "匹配到禁用配置" if found else "未发现禁用配置"
            else:
                passed = found
                detail = match.group(0) if found else "未检测到期望值"

            results.append({
                "id": check_id,
                "title": title,
                "section": section,
                "level": level,
                "expected": expected,
                "actual": detail if not passed else detail,
                "passed": passed,
                "status": "PASS" if passed else "FAIL",
            })
        else:
            results.append({
                "id": check_id,
                "title": title,
                "section": section,
                "level": level,
                "expected": expected,
                "actual": "未知检查类型",
                "passed": False,
                "status": "MANUAL",
            })

    return results


def generate_report(baseline_dir: Path, results: List[Dict], os_version: str) -> str:
    """生成 Markdown 格式的合规报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    manual = sum(1 for r in results if r["status"] == "MANUAL")

    lines = []
    lines.append(f"# CIS Benchmark 合规审计报告")
    lines.append(f"")
    lines.append(f"**目标系统:** OpenEuler {os_version}")
    lines.append(f"**基线目录:** {baseline_dir}")
    lines.append(f"**审计时间:** {now}")
    lines.append(f"")
    lines.append(f"## 摘要")
    lines.append(f"")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总计 | {total} |")
    lines.append(f"| ✅ 通过 | {passed} |")
    lines.append(f"| ❌ 未通过 | {failed} |")
    lines.append(f"| ⚠️ 需人工检查 | {manual} |")
    lines.append(f"| 通过率 | {(passed/total*100):.1f}% |")
    lines.append(f"")

    # 按 section 分组
    sections = {}
    for r in results:
        sec = r["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(r)

    lines.append(f"## 详细检查结果")
    lines.append(f"")

    for section_name, items in sections.items():
        lines.append(f"### {section_name}")
        lines.append(f"")
        lines.append(f"| ID | 标题 | 等级 | 期望 | 实际 | 状态 |")
        lines.append(f"|----|------|------|------|------|------|")
        for r in items:
            status_icon = {"PASS": "✅", "FAIL": "❌", "MANUAL": "⚠️"}.get(r["status"], "❓")
            lines.append(f"| {r['id']} | {r['title']} | {r['level']} | {r['expected']} | {r['actual']} | {status_icon} {r['status']} |")
        lines.append(f"")

    # 失败项汇总
    failed_items = [r for r in results if r["status"] == "FAIL"]
    if failed_items:
        lines.append(f"## ❌ 需修复项目")
        lines.append(f"")
        for r in failed_items:
            lines.append(f"- **{r['id']}** {r['title']}: 期望 `{r['expected']}`，实际 `{r['actual']}`")
        lines.append(f"")

    # 人工检查项
    manual_items = [r for r in results if r["status"] == "MANUAL"]
    if manual_items:
        lines.append(f"## ⚠️ 需人工检查的项目")
        lines.append(f"")
        for r in manual_items:
            lines.append(f"- **{r['id']}** {r['title']}: {r['actual']}")
        lines.append(f"")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 diff-analysis.py <基线目录> [输出报告路径]", file=sys.stderr)
        sys.exit(1)

    baseline_path = Path(sys.argv[1])
    if not baseline_path.exists() or not baseline_path.is_dir():
        print(f"错误: 基线目录不存在: {baseline_path}", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # 检测 OS 版本
    os_version = _detect_os_version(baseline_path)
    print(f"[INFO] 检测到 OpenEuler 版本: {os_version}")

    # 尝试加载自定义映射
    mapping_path = baseline_path.parent / ".." / "references" / "cis-mapping.json"
    mapping = load_custom_mapping(mapping_path)
    print(f"[INFO] 加载 {len(mapping)} 个检查项")

    # 执行检查
    results = run_checks(baseline_path, mapping)
    print(f"[INFO] 完成检查: {len(results)} 项")

    # 生成报告
    report = generate_report(baseline_path, results, os_version)

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report)
        print(f"[INFO] 报告已保存: {output_file}")
    else:
        print()
        print("=" * 60)
        print(report)

    # 摘要输出
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    manual = sum(1 for r in results if r["status"] == "MANUAL")
    print(f"\n[SUMMARY] ✅ {passed} / ❌ {failed} / ⚠️ {manual} (共 {len(results)} 项)")


if __name__ == "__main__":
    main()
