# ⚙️ 自动化脚本库

> ⚠️ 结构契约文件：此文件定义脚本库的文件命名规则和组织约定。
> ⚠️ 未经用户明确授权，本技能在使用过程中不得修改此文件。
> ⚠️ 擅自修改可能导致后续动态创建的脚本文件格式混乱。
>
> 此目录下的其他脚本文件（*.py，非 capability-tracker.py）可自由创建和修改，但 SKILL.md 永远不可修改。

## 文件命名规则
- 格式：`{功能描述}-工具.py` 或 `{功能描述}-handler.py`
- 使用英文小写 + 连字符
- 示例：`data-formatter.py`、`api-requester.py`、`chart-generator.py`

## 脚本结构模板
```python
# -*- coding: utf-8 -*-
"""
{功能描述}
用途：...
触发场景：...
依赖：...
"""

import ...

def main():
    ...

if __name__ == "__main__":
    main()
```

## 与 capability-tracker.py 的关系
- `capability-tracker.py` 是结构锁定文件，不得修改
- 其他脚本为自由生长文件，可自由创建、修改、删除
- 新脚本与 tracker 无耦合，独立运行

## 当前已有脚本
- `capability-tracker.py` — 🔒🟠 结构锁定，能力追踪自动化工具
