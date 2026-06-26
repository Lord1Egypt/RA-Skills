#!/usr/bin/env python3
"""
记录错误到 Agent Error Logger
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

def get_next_error_number(log_file: Path) -> int:
    """获取下一个错误编号"""
    if not log_file.exists():
        return 1
    
    content = log_file.read_text()
    numbers = []
    for line in content.split('\n'):
        if '### 错误 #' in line:
            try:
                num = int(line.split('#')[1].split(' ')[0])
                numbers.append(num)
            except:
                pass
    
    return max(numbers, default=0) + 1

def record_error(task: str, error: str, cause: str, fix: str, tags: str):
    """记录错误到日志文件"""
    memory_dir = Path(__file__).parent.parent.parent.parent / 'workspace' / 'memory'
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    # 当前月份日志文件
    now = datetime.now()
    log_file = memory_dir / f'error-log-{now.year}-{now.month:02d}.md'
    
    # 获取下一个错误编号
    error_num = get_next_error_number(log_file)
    
    # 生成错误记录
    timestamp = now.strftime('%Y-%m-%d %H:%M')
    record = f"""
### 错误 #{error_num:03d} - {task[:50]}
- **时间**: {timestamp}
- **任务**: {task}
- **错误**: {error}
- **原因**: {cause}
- **修正**: {fix}
- **模式标签**: {tags}
- **相似错误**: 无

"""
    
    # 写入日志文件
    if log_file.exists():
        content = log_file.read_text()
        # 插入到 "## YYYY-MM-DD" 之前
        header = f"## {now.year}-{now.month:02d}\n"
        if header in content:
            # 找到 header 位置，插入到其后
            parts = content.split(header, 1)
            content = parts[0] + header + record + parts[1]
        else:
            # 没有本月 header，添加到开头
            content = f"{header}{record}\n{content}"
        log_file.write_text(content)
    else:
        # 创建新文件
        content = f"""# Error Log - {now.year}年{now.month}月

> 详细错误日志，按时间倒序记录。

---

{header}{record}
"""
        log_file.write_text(content)
    
    # 更新模式索引
    update_patterns_index(memory_dir, tags)
    
    print(f"✓ 错误 #{error_num:03d} 已记录到 {log_file}")
    print(f"  标签：{tags}")

def update_patterns_index(memory_dir: Path, tags: str):
    """更新错误模式索引"""
    patterns_file = memory_dir / 'error-patterns.md'
    
    # 解析标签
    tag_list = [t.strip() for t in tags.split() if t.startswith('#')]
    
    if not patterns_file.exists():
        print(f"  提示：{patterns_file} 不存在，请先创建模式索引文件")
        return
    
    content = patterns_file.read_text()
    
    # 简单实现：只更新出现次数（实际应该更智能）
    for tag in tag_list:
        if tag in content:
            # 找到表格中的行，增加计数
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if tag in line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        try:
                            count = int(parts[2].strip())
                            parts[2] = f" {count + 1} "
                            lines[i] = '|'.join(parts)
                        except:
                            pass
            content = '\n'.join(lines)
    
    patterns_file.write_text(content)

def main():
    parser = argparse.ArgumentParser(description='记录 Agent 错误')
    parser.add_argument('--task', required=True, help='任务描述')
    parser.add_argument('--error', required=True, help='错误信息')
    parser.add_argument('--cause', required=True, help='原因分析')
    parser.add_argument('--fix', required=True, help='修正方案')
    parser.add_argument('--tags', required=True, help='模式标签，如 "#文件校验 #图片处理"')
    
    args = parser.parse_args()
    record_error(args.task, args.error, args.cause, args.fix, args.tags)

if __name__ == '__main__':
    main()
