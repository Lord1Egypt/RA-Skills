---
name: claw-planops
description: 基于交付物证据的项目执行规划技能。当用户需要解析任务通知、生成项目计划、导出日历、检查真实文件进度、或动态调整计划时使用。
user-invocable: true
---

# ClawPlanOps – 项目执行规划技能

## 核心理念

**让 AI 做 AI 擅长的事（文本理解），让代码做代码擅长的事（确定性操作）。**

- 文本解析 → 用你的 LLM 能力直接提取结构化信息
- 计划生成 → 调用代码工具（反向拆解 + 微任务生成）
- 日历导出 → 调用代码工具（ICS 文件生成 + VALARM）
- 进度检查 → 调用代码工具（文件扫描 + Git 证据）
- 动态重排 → 调用代码工具（压缩/砍功能/优先级调整）

## 工作流

### 当用户提供任务通知时：

**Step 1 – 你自己解析文本（不要调用 parse_task_requirements 工具）**

阅读用户提供的通知文本，直接提取以下结构化信息：

```json
{
  "task_name": "完整的任务/比赛名称",
  "deadline": "2026-06-22T12:00:00",
  "deliverables": ["交付物1", "交付物2"],
  "constraints": ["限制条件1", "限制条件2"],
  "submission_rules": ["提交规则1"]
}
```

重要规则：
- deadline 取最终提交截止时间，不要取报名时间
- 如果文本有多个日期，找"作品提交""材料报送""截止"相关的
- deliverables 列出所有需要产出/提交的东西
- 如果通知只有一个邮箱和申请表，那交付物就是申请表

**Step 2 – 调用 clawplanops_build_deliverable_plan**

把 Step 1 的 JSON 作为 `task_requirements` 参数传入。
可选参数：
- `available_days` — 手动指定可用天数（默认从 deadline 自动计算）
- `daily_available_hours` — 每天可用小时数（默认 2）
- `custom_templates` — 自定义交付物模板，格式：
  ```json
  {
    "商业计划书": {
      "sub_tasks": ["市场调研", "撰写正文", "财务分析"],
      "evidence": ["商业计划书.pdf"]
    }
  }
  ```
  自定义模板会覆盖内置模板中同名的条目。

**Step 3 – 调用 clawplanops_generate_calendar_schedule**

用 plan 中的 `micro_tasks`、`start_date`、`deadline` 生成日历。
可选参数：
- `preferred_work_time` — 工作时间段，如 "20:00-22:00"（默认）
- `output_path` — 输出路径（默认 ./output/schedule.ics）

**Step 4 – 总结并告知用户**

用中文总结：任务名、截止日期、几个阶段、几个微任务、日历文件位置。

---

### 当用户要求检查进度时：

调用 `clawplanops_check_progress_evidence`，传入项目路径。

汇报：进度百分比、风险等级、缺失项、下一步建议。

---

### 当用户进度落后时：

先调用 `clawplanops_check_progress_evidence` 获取当前进度，
再调用 `clawplanops_reschedule_plan` 获取重排建议。

---

## 工具列表

| 工具 | 用途 | 输入 |
|------|------|------|
| `clawplanops_parse_task_requirements` | **仅限 CLI 备用** — 代码规则解析，不如你亲自解析准确，不要在技能流程中使用 | content, input_type |
| `clawplanops_build_deliverable_plan` | 生成交付物计划 + 微任务 | task_requirements, available_days?, daily_available_hours?, custom_templates? |
| `clawplanops_generate_calendar_schedule` | 生成 .ics 日历文件 | micro_tasks, start_date, deadline, preferred_work_time?, output_path? |
| `clawplanops_check_progress_evidence` | 扫描项目文件 + Git 证据 | project_path |
| `clawplanops_reschedule_plan` | 动态重排建议 | progress_report, original_plan, deadline |

### macOS 日历直连

CLI 用户可使用 `--apple-cal` 标志将日历事件直接导入 macOS Calendar.app：

```bash
claw-planops calendar plan.json --apple-cal
claw-planops full notice.txt . --apple-cal
```

导入前会显示事件摘要并要求用户确认（y/N）。事件会写入名为 "ClawPlanOps" 的专属日历。

编程方式调用：
```typescript
import { importToAppleCalendar } from 'claw-planops';
const result = importToAppleCalendar(calendarEvents);
// result: { success, imported_count, calendar_name, errors }
```

## 配置文件

用户可以在项目根目录创建 `.planopsrc.json` 自定义行为：

```json
{
  "name": "my-project",
  "preferred_work_time": "09:00-12:00",
  "daily_available_hours": 3,
  "output_dir": "./output",
  "deliverables": {
    "商业计划书": {
      "sub_tasks": ["市场调研", "撰写正文"],
      "evidence": ["商业计划书.pdf"]
    }
  },
  "exclude_patterns": ["node_modules", ".git", "dist"]
}
```

## 示例

用户：
> 帮我分析这个比赛通知：郑州大学"四创"大赛，6月22日12:00前提交申请表电子版到 cschuangjing@163.com，纸质版下午送到办公室

你应该：
1. 自己提取结构化信息（不要调用 parse_task_requirements）
2. 调用 build_deliverable_plan
3. 调用 generate_calendar_schedule
4. 用中文总结

## 关键原则

- **解析靠 AI，不靠正则** — 语言理解能力远超任何正则表达式
- **计划生成靠代码** — 反向拆解、微任务估算、日历生成由工具完成
- **进度检查靠文件证据** — 不靠用户打卡，扫描目录 + Git log
- **日历自带提醒** — ICS 含 30分钟前 + 1天前 VALARM
