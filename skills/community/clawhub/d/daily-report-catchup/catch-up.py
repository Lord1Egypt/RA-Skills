#!/usr/bin/env python3
"""
码虫日报补课脚本
基于 Hermes Agent 学习循环思路

模式：
  --detect   只检测，不生成（用于预检）
  --full     检测 + 生成补录（默认）
  --quiet    静默模式，只返回 exit code

用法:
  python3 catch-up.py               # 完整流程
  python3 catch-up.py --detect     # 只检测漏发
  python3 catch-up.py --quiet      # 静默检测
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/colbert/.openclaw/workspace-coding-advisor")
REPORT_DIR = WORKSPACE / "memory/daily-reports"
INDEX_FILE = REPORT_DIR / "INDEX.md"
LOG_DIR = WORKSPACE / "memory/logs"
STATE_FILE = WORKSPACE / ".catch-up-state"
HERMES_REFLECTIONS = Path.home() / "hermes-agent/reflections.md"

# 静默模式
QUIET = '--quiet' in sys.argv or '-q' in sys.argv
DETECT_ONLY = '--detect' in sys.argv or '-d' in sys.argv

def log(msg, quiet=False):
    """写日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [补课] {msg}"
    if not quiet:
        print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def is_workday(date):
    """判断是否为工作日（周一到周五）"""
    return date.weekday() < 5

def get_chinese_weekday(date):
    """获取中文星期"""
    names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return names[date.weekday()]

def get_all_index_dates():
    """从 INDEX 文件中提取所有日期（只取表格中的日期行）"""
    dates = []
    if INDEX_FILE.exists():
        collecting = False
        for line in INDEX_FILE.read_text().splitlines():
            # 找到日期列头之后开始收集
            if "| 日期 |" in line and "星期" in line:
                collecting = True
                continue
            # 遇到空行或状态说明标题，停止收集
            if collecting and (line.strip() == "" or line.startswith("## ")):
                break
            # 收集日期行（跳过表头分隔线）
            if collecting and line.startswith("|") and "2026-" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 1 and parts[1].startswith("2026"):
                    dates.append(parts[1])
    return dates

def get_index_status(date_str):
    """获取 INDEX 中某日期的状态"""
    # 表格格式: | 日期 | 星期 | 状态 | 执行时间 | 备注 |
    # parts:     [0]   [1]   [2]    [3]       [4]    [5]
    if not INDEX_FILE.exists():
        return None
    for line in INDEX_FILE.read_text().splitlines():
        if f"| {date_str} |" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) > 3:
                return parts[3]  # 状态列
    return None

def get_all_report_dates():
    """获取所有已存在的报告日期"""
    dates = []
    for f in REPORT_DIR.glob("2026-*.md"):
        if f.name != "INDEX.md":
            dates.append(f.stem)  # 文件名去掉 .md
    return set(dates)

def detect_missed_days():
    """检测漏发的工作日
    
    只检测：
    1. INDEX 中完全没有记录的日子（真正的漏发）
    2. 过去7个工作日内
    3. 跳过周末
    4. 对于 INDEX 有记录的情况：
       - failed/skipped 状态：没有文件是正常的，不补录
       - success/caught-up 状态：文件丢失则补录
    """
    today = datetime.now()
    index_dates = set(get_all_index_dates())
    report_dates = get_all_report_dates()
    
    log(f"📋 INDEX 中记录日期数: {len(index_dates)}")
    log(f"📋 实际报告文件数: {len(report_dates)}")
    
    missed = []
    
    # 只扫描过去7个工作日
    for i in range(1, 15):  # 扫描更多天以确保找到7个工作日
        d = today - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        
        if not is_workday(d):
            continue  # 跳过周末
        
        in_index = date_str in index_dates
        has_file = date_str in report_dates
        status = get_index_status(date_str) if in_index else None
        
        if not in_index:
            # INDEX 中完全没有记录 = 漏发
            missed.append((date_str, d))
            log(f"⚠️ 发现漏发: {date_str} ({get_chinese_weekday(d)})", quiet=QUIET)
        elif status in ("success", "caught-up") and not has_file:
            # 原本成功但文件丢失 = 补录
            missed.append((date_str, d))
            log(f"⚠️ 发现文件丢失: {date_str} ({get_chinese_weekday(d)})", quiet=QUIET)
        # failed/skipped 没有文件是正常的，不补录
        
        # 找到7个漏发就停止
        if len(missed) >= 7:
            break
    
    return missed

def generate_catchup_report(date_str, date_obj):
    """生成补录报告"""
    weekday = get_chinese_weekday(date_obj)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# 📋 码虫每日日报（补录）

> **补录日期**: {date_str} ({weekday})
> **生成时间**: {timestamp}
> **补录类型**: 系统离线后自动补录

---

> ⚠️ **注意**: 此为离线期间自动生成的补录报告，内容基于系统状态自动填充。

## 📋 当时工作

*系统离线，无详细记录*

## 📚 当时学习

*系统离线，无详细记录*

## 🔍 复盘

**做得好的**:
- 系统自动检测到漏发并补录

**需要改进**:
- 建议保持机器在线，确保实时记录

## 💡 备注

本报告为系统离线期间自动生成的补录记录。
实际工作内容以当日真实情况为准。

---
_🤖 码虫 🐛 Daily Report (Catch-Up)_
_生成时间: {timestamp}_
"""
    
    report_file = REPORT_DIR / f"{date_str}.md"
    report_file.write_text(content)
    log(f"✅ 补录报告已生成: {report_file.name}")

def update_index(date_str, status, note):
    """更新索引文件"""
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("""# 📊 码虫日报发送记录索引

| 日期 | 星期 | 状态 | 执行时间 | 备注 |
|------|------|------|----------|------|
""")
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = get_chinese_weekday(date_obj)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = INDEX_FILE.read_text()
    lines = content.splitlines()
    
    # 找到表格最后一行的位置
    table_end_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("|"):
            table_end_idx = i
    
    # 查找是否已有该日期的记录
    found = False
    new_lines = []
    for i, line in enumerate(lines):
        if i <= table_end_idx and f"| {date_str} |" in line:
            # 更新
            new_lines.append(f"| {date_str} | {weekday} | {status} | {timestamp} | {note} |")
            found = True
        elif i <= table_end_idx:
            new_lines.append(line)
        elif i > table_end_idx:
            # 保留表格之后的内容（状态说明等）
            new_lines.append(line)
    
    if not found:
        # 在表格最后一行之后插入新记录
        new_lines.insert(table_end_idx + 1, f"| {date_str} | {weekday} | {status} | {timestamp} | {note} |")
    
    INDEX_FILE.write_text("\n".join(new_lines) + "\n")
    log(f"📝 索引已{'更新' if found else '追加'}: {date_str} -> {status}")

def hermes_reflect(event, detail):
    """记录到 Hermes 反思文件"""
    if HERMES_REFLECTIONS.exists():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = HERMES_REFLECTIONS.read_text()
        content += f"""

## {timestamp} - 补课事件
- Event: {event}
- Detail: {detail}
"""
        HERMES_REFLECTIONS.write_text(content)
        log(f"📝 已记录到 Hermes: {event}")

def main():
    global LOG_FILE
    
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR / "catch-up.log"
    
    if not QUIET:
        print("\n" + "=" * 50)
        log("🤖 码虫日报补课系统启动")
        print("=" * 50)
    else:
        log("🤖 码虫日报补课系统启动", quiet=True)
    
    # 检测漏发
    missed = detect_missed_days()
    
    if not missed:
        if not QUIET:
            log("✅ 没有发现漏发的日报")
        else:
            log("✅ 没有发现漏发的日报", quiet=True)
    else:
        if not QUIET:
            log(f"📊 发现 {len(missed)} 个漏发工作日")
        else:
            log(f"📊 发现 {len(missed)} 个漏发工作日", quiet=True)
        
        if not DETECT_ONLY:
            # 生成补录
            caught_dates = []
            for date_str, date_obj in missed:
                generate_catchup_report(date_str, date_obj)
                update_index(date_str, "caught-up", "系统离线后自动补录")
                caught_dates.append(date_str)
            
            hermes_reflect("日报补课", f"检测到 {len(missed)} 个漏发日，已全部补录: {', '.join(caught_dates)}")
            if not QUIET:
                log(f"✅ 补课完成: {len(missed)} 个报告已生成")
            else:
                log(f"✅ 补课完成: {len(missed)} 个报告已生成", quiet=True)
        else:
            # 只检测模式
            if not QUIET:
                log("📝 检测模式：跳过补录生成")
            else:
                log("📝 检测模式：跳过补录生成", quiet=True)
    
    # 更新状态文件
    state_content = f"""# 码虫补课状态
last_run={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
last_catchup={datetime.now().strftime('%Y-%m-%d')}
missed_count={len(missed)}
"""
    STATE_FILE.write_text(state_content)
    
    if not QUIET:
        print("=" * 50)
        log("✅ 补课系统任务完成")
        print("=" * 50 + "\n")
    
    # 返回 exit code：0=正常，1=有漏发
    return 1 if missed else 0

if __name__ == "__main__":
    exit_code = main()
    if QUIET:
        sys.exit(exit_code)
    else:
        sys.exit(0)  # 质量检查脚本才用 exit_code，这里保持 0 避免误判
