#!/usr/bin/env python3
"""
保存报告文档（永久保留）
- 支持多行输入（stdin）
- 区分报告类型
- 支持错误处理
"""
import os
import sys
import datetime

def main():
    report_content = ""

    # 支持从 stdin 或 argv 获取内容
    if not sys.stdin.isatty():
        report_content = sys.stdin.read()
    elif len(sys.argv) >= 2:
        report_content = sys.argv[1]
    elif len(sys.argv) == 2 and sys.argv[1] == "-":
        report_content = sys.stdin.read()

    if not report_content.strip():
        print("ERROR: No content provided.")
        sys.exit(1)

    # 构建输出路径（永久保留）
    base = os.path.expanduser("~/.openclaw/workspace/skills/daily-fintech-brief")
    output_dir = os.path.join(base, "output", "reports")
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"Fintech_Brief_{datetime.date.today()}.md"
    file_path = os.path.join(output_dir, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"SUCCESS: 报告已保存至（永久保留）: {file_path}")
    except OSError as e:
        print(f"ERROR: 写入失败 - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()