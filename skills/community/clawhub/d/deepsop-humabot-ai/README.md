# 人机协作台（Human-AI Collaboration）

基于 DeepSOP 平台的智能销售任务助手，理解自然语言指令、自动拆解任务参数、调用 deepsop API 提交任务，并按用户指定时间自动查询结果。

## ✨ 主要能力

- **客户挖掘**（AiWa）— 找客户、行业客户，自动生成带样式的 xlsx 报表
- **邮件销售**（Frank）— 提交邮件销售任务并统计发送/已读/回复
- **电话销售**（Fran）— 自动查询号码池与场景库后提交电话销售任务
- **短信销售**（Lisa）— 提交短信任务并统计发送结果
- **电话场景创建/审核** — 当账号下没有可用场景库时，引导用户即时填写"场景信息 + TTS 音色 + 机器人 prompt"，一键提交阿里云审核并轮询至 `PUBLISHED`

> AI 视频生成与 TikTok 发布（Toby）已抽离到独立技能 [`deepsop-tiktokflow`](../deepsop-tiktokflow/README.md)。

## 🚀 快速开始

1. **获取 API Key**
   - 已有账号 → [https://ai.deepsop.com/login?source=3](https://ai.deepsop.com/login?source=3)
   - 没有账号 → [https://ai.deepsop.com/register?source=3](https://ai.deepsop.com/register?source=3)
   - 复制以 `sk-` 开头的密钥

2. **配置环境变量**

   ```bash
   # Linux/macOS
   export DEEPSOP_API_KEY="sk-your_api_key_here"
   ```

   ```powershell
   # Windows PowerShell
   $env:DEEPSOP_API_KEY="sk-your_api_key_here"
   ```

3. **直接对 OpenClaw 说出需求**，例如：
   - "帮我找 50 个美国做服装的客户"
   - "给这批客户发一封产品介绍邮件"
   - "给老客户发一条短信通知"
   - "创建一个外呼电话场景，用于邀约客户参加 4 月发布会"

## 📖 完整文档

详细使用说明、参数约定、错误处理流程请查看 [SKILL.md](SKILL.md)。

## ⚠️ 重要提醒

- 提交 `agentSubmitTask` **必须**走 `scripts/submit_task.py`（脚本内置 UTF-8 安全提交 + 参数预校验）
- 创建/审核电话场景 **必须**走 `scripts/submit_script_review.py`（同样 UTF-8 安全 + 预校验 + 自动轮询审核状态）
- **禁止**直接写 `curl` 命令（Windows cp936 代码页会导致 prompt/openingPrompt 中文乱码）

---

## 🔒 安全审计报告

> 本技能已通过 `skill-vetter` 安全审计工具的完整审查，可放心安装使用。

| 字段 | 内容 |
|---|---|
| **审计日期** | 2026-05-12 |
| **审计工具** | skill-vetter (clawhub@latest) |
| **来源** | ClawdHub / DeepSOP 官方 |
| **审查文件数** | 10（SKILL.md、api_paths.py、submit_task.py、submit_script_review.py、3 个参数校验器、格式化脚本等） |
| **可疑模式** | ✖ 无 |
| **网络访问** | `https://ai.deepsop.com/prod-api/...`（合法的 DeepSOP 任务提交接口，单一已知域名） |
| **API Key 处理** | 仅从环境变量 `DEEPSOP_API_KEY` 读取，未硬编码、无外泄 |
| **文件访问** | 不直接读写本地文件（仅 JSON 任务体） |
| **依赖命令** | 仅 Python 标准库 `urllib`，无第三方依赖 |
| **风险等级** | 🟡 MEDIUM（需配置 API Key，向已知服务提交任务） |
| **审计结论** | ✅ **SAFE TO INSTALL — 安全可安装** |

**审计要点：**
- 设计上具备纵深防御：HTTP 提交前先做参数预校验。
- 全程 UTF-8 编码安全，规避 Windows 代码页导致的中文乱码问题。
- 单一已知 API 域名，未发现凭据外泄路径。
- 误报澄清：`.py` 文件中出现的 `curl` 仅为注释/文档示例，并未实际执行。

> 完整的多技能审计报告见仓库根目录 `SKILL_VETTING_REPORT.md`。
