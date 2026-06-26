## 可运行工具

> **数据存储说明**：以下脚本部分会在 `SKILL_DIR/data/` 目录下生成本地统计数据（评估历史、洞察记录、会话状态）。
> 所有数据仅保存在本机，不对外传输。如需清除数据，删除 `SKILL_DIR/data/` 目录即可。

本技能包含以下可执行脚本（位于 `scripts/` 目录）：

| 脚本 | 功能 | 是否存储数据 |
|------|------|------------|
| `assessment.py` | 错位程度评估问卷 | ✅ 存储评估历史 |
| `reflection.py` | 听见防御日记（每日反思） | ❌ 纯文本输出 |
| `breathing_timer.py` | 30秒呼吸计时器 | ❌ 无数据存储 |
| `scenario_practice.py` | 场景对话练习 | ❌ 无数据存储 |
| `visualize.py` | 家庭互动模式可视化 | ✅ 读取已存储历史数据 |
| `action_planner.py` | 行为计划生成与反馈 | ✅ 存储反馈和计划 |
| `insight_capturer.py` | 对话洞察捕获 | ✅ 存储洞察记录 |
| `system_integrator.py` | 系统集成器 | ✅ 存储会话状态 |

运行方式：`python scripts/YOUR_SCRIPT.py`

---

### 工具七：修复对话指南（v2.0.1 NEW）