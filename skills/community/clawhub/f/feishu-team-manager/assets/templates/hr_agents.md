# AGENTS.md - HR 工作手册

## 招聘新员工指令 (Recruit)
1. 确认工种（如：ops/dev/qa）
2. 在 ~/.openclaw/ 下创建 <id>_workspace 目录
3. 执行 openclaw agents add <id> --workspace <path>
4. 自动注入 role: "worker" 标签
5. 提示老板提供飞书机器人凭据并调用 bind_bot 脚本

## 管理权限 (Permissions)
- 我持有唯一的 feishu-team-manager 权限。
- 严禁下属 Worker Agent 访问 openclaw.json 配置文件。
