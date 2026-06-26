# -*- coding: utf-8 -*-
"""
持续学习套件 - 初始化脚本

创建必要的学习文件和目录结构
"""
import sys
import os
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORKSPACE = Path.cwd()


def create_file(filepath, content=None):
    """创建文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        if content:
            f.write(content)
    print(f"✅ {filepath}")


def main():
    print("\n持续学习套件 - 初始化")
    print("=" * 60)

    # 创建学习文件目录
    learnings_dir = WORKSPACE / ".learnings"
    learnings_dir.mkdir(exist_ok=True)

    # 创建ERRORS.md
    create_file(
        learnings_dir / "ERRORS.md",
        """# 错误教训记录

> 每次犯错立即记录，避免重复

---

## 格式

### 错误：[简短描述]
**错误**: [具体错误内容]
**正确**: [正确做法]
**教训**: [避免方法]
**日期**: YYYY-MM-DD

---

## 示例

### 错误：LIMS报告下载字段错误
**错误**: 猜测LIMS API用`sampleBaseUuid`获取报告
**正确**: 应该用`sampleBaseTestingUuid`
**教训**: API字段名必须查证，不能猜测；先验证再使用
**日期**: 2026-04-10
"""
    )

    # 创建LEARNINGS.md
    create_file(
        learnings_dir / "LEARNINGS.md",
        """# 学习成果记录

> 从错误和被纠正中获得的知识

---

## 格式

### 学习：[主题]
**收获**: [学到的内容]
**应用**: [应用场景]
**日期**: YYYY-MM-DD

---

## 示例

### 学习：登录类API握手流程
**收获**: 必须先GET再POST，不能直接POST
**应用**: LIMS登录、企业微信认证
**日期**: 2026-04-10
"""
    )

    # 创建FEATURES.md
    create_file(
        learnings_dir / "FEATURES.md",
        """# 功能需求和改进建议

> 用户提出的功能需求、todo项

---

## 格式

### [功能名称]
**需求**: [详细描述]
**状态**: pending/doing/done
**优先级**: high/medium/low
**日期**: YYYY-MM-DD

---

## 示例

### 植物大战僵尸游戏
**需求**: 在手机上创建可直接运行的植物大战僵尸游戏
**状态**: pending
**优先级**: low
**日期**: 2026-04-10
"""
    )

    # 创建memory目录
    memory_dir = WORKSPACE / "memory"
    memory_dir.mkdir(exist_ok=True)

    # 创建今日记忆文件
    today = datetime.now().strftime('%Y-%m-%d')
    today_memory = memory_dir / f"{today}.md"
    if not today_memory.exists():
        create_file(
            today_memory,
            f"# {today} - 今日对话记录\n\n> 自动生成的记忆文件\n\n"
        )

    # 创建通知队列空文件
    queue_file = WORKSPACE / ".notification_queue.json"
    if not queue_file.exists():
        create_file(queue_file, "[]")

    print("=" * 60)
    print("\n✅ 初始化完成！")
    print("\n创建的文件：")
    print("  - .learnings/ERRORS.md")
    print("  - .learnings/LEARNINGS.md")
    print("  - .learnings/FEATURES.md")
    print(f"  - memory/{today}.md")
    print("  - .notification_queue.json")
    print("\n下一步：")
    print("  1. 配置 config/dream_config.json")
    print("  2. 运行 setup/install_cron.py 安装定时任务")
    print("  3. 测试 sync/sync_notification.py")
    print("  4. 测试 dream/dream_cycle.py")


if __name__ == '__main__':
    main()
