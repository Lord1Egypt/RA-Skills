---
name: doctor_assistant
description: 医生工作台助手。整理患者基本信息、关键时间线、检验趋势、待办事项并生成随访任务草稿。当用户以医生身份查询患者情况或需要随访建议时触发。
---

# 医生工作台助手 Skill

## 何时使用

当用户以医生角色请求患者相关信息时使用，例如：
- 「帮我整理这个患者最近的情况」
- 「查看患者时间线」
- 「生成随访任务」

本 skill 独立于科研任务流程，可单独触发。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"doctor-assistant","display_name":"医生工作台助手","status":"running","message":"正在整理患者摘要、时间线与检验趋势..."}'
```

### 2. 读取数据并输出

读取 `/home/ubuntu/workspace/demo/mock_data/doctor_demo.json`，向用户展示：

- **患者基本信息**：姓名（脱敏）、性别、年龄、主诊断、主治医生
- **关键事件时间线**：按时间顺序列出每个事件的日期、类型、摘要
- **检验指标趋势**：列出各日期的 WBC、CRP（如有 PCT 也列出）数值，标注趋势方向
- **待办事项清单**：按优先级列出每条待办
- **随访任务草稿**：
  - 任务标题
  - 建议随访时间
  - 关键随访问题列表

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"doctor-assistant","display_name":"医生工作台助手","status":"completed","message":"患者摘要已整理，随访任务草稿已生成"}'
```
