---
name: codegraph-assistant
version: 1.0.0
description: 一键代码图谱助手 — 包装 npm codegraph，自动初始化/索引/注入上下文。让 DeepSeek TUI 编程时一句话拿到项目结构、符号索引、影响分析。
---

# CodeGraph Assistant

> npm codegraph 的加速包装器。不需要手动 `codegraph init -i` → `query` 三步走。

## 解决的问题

| 无此技能 | 有此技能 |
|---------|---------|
| 手动 `codegraph init -i` 每项目 | `setup` 一键完成 |
| `codegraph context "fix bug"` 怕输错格式 | `ask "你的问题"` 自动组命令 |
| 不知道改了影响哪些测试 | `affected file.py` 直接出结果 |
| 不会注入到 memory | `inject` 写入 MEMORY.md |

## 命令

```bash
python codegraph_assist.py setup [path]     # init + index 项目
python codegraph_assist.py ask "问题描述"    # 生成任务上下文 (markdown)
python codegraph_assist.py query "类名"     # 搜索符号
python codegraph_assist.py affected file.py # 改动影响分析
python codegraph_assist.py inject [path]    # 注入摘要到 MEMORY.md
python codegraph_assist.py status [path]    # 索引统计
```

## 依赖

- `npm codegraph`（`@colbymchenry/codegraph`）已全局安装
- Python 3.11+

## 典型工作流

```bash
# 新项目
cd myproject
codegraph-assistant setup     # 30s，一次性

# 编程时
codegraph-assistant ask "重构数据库连接层"
# → 输出 markdown 上下文，含入口点、相关符号、调用链
```

## 集成

DeepSeek TUI 可通过 `exec_shell` 直接调用：
```
> codegraph_assist.py query "ClassName" -j    # 拿 JSON 结果
> codegraph_assist.py affected src/file.py     # 改动前检查
```
