slug: cn-todo-today
name: 今日待办生成器
description: "cn-todo-today。纯Python标准库，无需API Key。"
keywords: todo, today
version: "1.0.0"
author: 千策


# 今日待办生成器


简单易用的今日待办事项管理工具。

## 功能

- 添加待办事项
- 标记完成
- 查看今日待办
- 统计完成情况

## 使用方法

```bash
# 添加待办
python3 cn_todo_today.py add "完成报告"

# 列出今日待办
python3 cn_todo_today.py list

# 标记完成
python3 cn_todo_today.py done 1

# 删除待办
python3 cn_todo_today.py delete 1

# 统计
python3 cn_todo_today.py stats
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `action` | 操作：add/list/done/delete/stats | 必填 |
| `--text` | 待办文本（add时） | 空 |
| `--id` | 待办ID（done/delete时） | 空 |

## 数据存储

- 本地JSON文件：`~/.cn_todo_today.json`

## 示例

```bash
# 添加
python3 cn_todo_today.py add "写周报"
python3 cn_todo_today.py add "回复邮件"

# 查看
python3 cn_todo_today.py list

# 完成
python3 cn_todo_today.py done 1
```

## 依赖

- Python 3.x（内置json模块）

## 注意事项

- 数据存储在用户主目录
- 每天会自动清理已完成的待办

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
