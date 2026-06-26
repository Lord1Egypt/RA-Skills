---
slug: auto-continue
name: 任务自动续接
version: "1.0.0"
author: 千策
---


# Auto-Continue — 任务自动续接

检测未完成任务，提醒继续推进。

## 触发条件

当检测到 `memory/in_progress.md` 中存在未完成的任务时，提醒 Agent 继续执行下一步。

## 使用方式

```bash
# 检查任务状态
python3 scripts/check_progress.py --check
```

## 判断逻辑

1. 读取 `memory/in_progress.md` 查看当前任务状态
2. 扫描 skills 目录检查完整性（SKILL.md + 脚本是否齐全）
3. 报告未完成项，建议下一步

## 安全边界

本技能仅**检测和提醒**，不自动执行以下操作：
- 不自动提交 git
- 不自动上传/发布
- 不自动删除文件
- 不读取系统凭据或密钥

需要执行以上操作时，由 Agent 自行判断是否需要用户确认。

## 任务状态文件格式

在 `memory/in_progress.md` 中记录：

```markdown
# 进行中的任务
## 当前任务
- 任务：开发 XXX Skill
- 状态：脚本编写中
- 下一步：测试脚本
## 待办队列
1. [ ] 任务1
2. [ ] 任务2
```

## 检测脚本

`scripts/check_progress.py` 会扫描：
- skills 目录中缺少脚本或 SKILL.md 的目录
- in_progress.md 中标记为"进行中"的任务

输出未完成项列表，供 Agent 参考。

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
