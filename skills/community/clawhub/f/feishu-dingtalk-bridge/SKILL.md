---
name: feishu-dingtalk-bridge
version: 1.0.0
author: AI-Workflows
license: MIT
description: 打通飞书/钉钉开放API，实现日程同步、审批追踪、文档解析与智能待办分发的企业协同中枢
tags:
  - 企业协同
  - 办公自动化
  - 飞书
  - 钉钉
  - 流程引擎
parameters:
  platform:
    type: string
    required: true
    description: 目标平台（feishu/dingtalk）
  action:
    type: string
    required: true
    description: 执行动作（sync_calendar/fetch_approval/parse_doc/distribute_task）
  auth_token:
    type: string
    required: true
    description: 平台应用访问凭证（App Token/Access Token）
  query_context:
    type: string
    required: false
    description: 查询条件或上下文（如：部门ID/时间范围/文档链接/待办关键词）
output_format: markdown
compatibility:
  - OpenClaw
  - Dify
  - Coze
  - SkillHub
---
# 🌐 飞书钉钉协同中枢

## 🎯 核心定位
将企业IM/审批/日历/文档API转化为结构化工作流，自动聚合碎片信息并生成可执行待办清单。

## 🔄 工作流指令
1. 校验 `platform` 与 `auth_token` 格式，失败则终止并提示授权路径。
2. 根据 `action` 路由至对应API逻辑：
   - `sync_calendar`：拉取指定周期日程 → 冲突检测 → 输出时间轴
   - `fetch_approval`：查询审批流状态 → 超时/驳回预警 → 输出处理建议
   - `parse_doc`：提取文档关键段落（合同/纪要/SOP）→ 结构化摘要
   - `distribute_task`：按角色/部门拆分任务 → 生成派单模板
3. 清洗返回数据，过滤脱敏字段，对齐企业字段映射规范。
4. 按输出模板生成 Markdown 报告。

## 📤 输出模板
```markdown
# 📅 协同工作流执行报告

## 1. 数据聚合摘要
| 模块 | 数据量 | 异常项 | 同步状态 |
|:---|:---|:---|:---|
| 日程/审批/文档/任务 | ... | ... | ✅/⚠️ |

## 2. 核心事项清单
| 事项名称 | 责任方 | 截止时间 | 当前状态 | 下一步动作 |
|:---|:---|:---|:---|:---|
| ... | ... | ... | ... | ... |

## 3. 自动化建议
- 规则匹配项：...
- 需人工介入项：...
- 建议调度策略：...
> ⚠️ 所有API调用已遵循平台限频策略。敏感数据已脱敏处理。
