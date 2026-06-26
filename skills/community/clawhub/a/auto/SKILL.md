---
name: auto
description: Helps automate repetitive tasks with scripts, scheduled jobs, and simple workflows. Use when the user wants to script an action, run something on a schedule (cron, Task Scheduler), automate builds or deploys, or reduce manual steps in a workflow.
---

# Auto（自动化）

本 Skill 帮助把**重复性操作**做成脚本或定时任务：写小脚本、配置定时执行、以及简单的自动化流程（如构建、备份、发布前检查）。

---

## 何时使用

当用户提到或需要：

- 把一系列命令/操作写成脚本（Shell、PowerShell、Node、Python 等）
- 定时执行某任务（每天、每小时、开机后等）
- 自动化构建、测试、打包、部署中的某一步或整条流水线
- 批量处理文件、拉取数据、发通知等可重复流程
- “不想每次手动做，想一键/定时跑”

---

## 脚本自动化

- **目标**：用最少步骤完成一件事，可重复跑、易维护。
- **选语言**：跨平台或 Linux/macOS 常用 Bash；Windows 优先 PowerShell；复杂逻辑或用 Python/Node。
- **注意**：脚本里用相对路径或环境变量表示路径/密钥；关键步骤加简单日志或 `echo`，失败时用非零退出码或 `set -e`（Bash）便于调用方判断。

按用户当前 OS 和已有环境给出对应示例（如 Windows 用 PowerShell，Linux 用 Bash）。

---

## 定时执行

### Windows

- **任务计划程序（Task Scheduler）**：创建基本任务 → 设置触发器（每日/开机/登录等）→ 操作选“启动程序”，填脚本或可执行文件路径。
- 命令行创建：`schtasks /create /tn "任务名" /tr "powershell -File C:\path\to\script.ps1" /sc daily /st 09:00`（参数依需求改）。

### Linux / macOS

- **cron**：`crontab -e`，一行一条。格式：分 时 日 月 周 命令。
  - 每天 9 点：`0 9 * * * /path/to/script.sh`
  - 每 5 分钟：`*/5 * * * * /path/to/script.sh`
- 确保脚本有执行权限（`chmod +x`），必要时在 crontab 里设 `PATH` 或使用绝对路径。

根据用户说的“多久跑一次”和系统类型，给出具体 cron 或 schtasks 示例。

---

## 简单流水线/流程

- **本地**：用脚本串联命令（先构建 → 再测试 → 再打包），步骤间用退出码判断是否继续。
- **CI/CD**：在 GitHub Actions、GitLab CI、Jenkins 等里写一段 job，调用现有脚本或内联命令；本 Skill 只给单步或短流程示例，复杂流水线建议看对应平台文档。
- **幂等**：能重复跑不破坏状态（如“同步到目录”而不是“每次追加不检查”），在说明里提一句即可。

---

## 使用原则

- **先弄清要自动化的步骤**：把“现在手头怎么做”列成 1、2、3，再变成脚本或任务。
- **最小可行**：先实现能跑通的一版，再考虑错误处理和日志。
- **敏感信息**：密码、API 密钥用环境变量或密钥管理，不写进脚本或任务命令里。
