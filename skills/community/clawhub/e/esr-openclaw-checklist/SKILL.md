---
name: esr-openclaw-checklist
description: 运行 ESR OpenClaw 主机安全检查脚本并完整展示结果。用于用户要求“运行ESR安全检查”、“执行 ESR 安全审计”、“检查 OpenClaw 主机安全配置”、“查看 ESR 安全检查结果”或需要调用该 skill 的脚本 `/home/may/.openclaw/skills/ESR_openclaw-checklist-v3.2/scripts/openclaw_checklist.py` 时。
---

# ESR OpenClaw 安全检查

执行 ESR 提供的安全检查脚本，并把脚本输出完整呈现给用户。

## 执行方式

- 手动执行时，运行：
  - `python3 {baseDir}/scripts/openclaw_checklist.py`
- 如果用户明确要求定时任务脚本，再运行：
  - `python3 {baseDir}/scripts/openclaw_checklist_scheduled.py`

## 工作要求

1. 完整显示 Python 脚本输出，不截断、不改写检查项含义。
2. 基于输出总结风险点，但不要替代原始输出。
3. 不要自动修改系统配置。
4. 如果发现需要修复的问题，先说明风险和建议，再征求用户确认。

## 检查重点

脚本会覆盖以下 8 项检查：

1. 默认端口使用情况
2. 服务监听地址检查
3. 内网穿透工具检测
4. Node.js 版本检查
5. 密码登录模式检查
6. Skill 数量及官方来源检查
7. 配置文件权限检查
8. OpenClawd 深度安全审计

## 输出后处理

- 先给出原始结果。
- 再用简洁语言总结：
  - 总体是否安全
  - 发现了几项风险
  - 每项风险的修复建议
- 若用户要求修复，再逐项执行，并在修改前再次确认。
