# TikTok 视频 AI 生成与发布（TikTokFlow）

基于 DeepSOP 平台数字员工 **Toby** 的 AI 视频生成与 TikTok 发布技能。理解自然语言指令、自动拆解任务参数、生成 AI 视频并定时发布到指定 TikTok 账号，按用户指定时间自动查询播放/点赞/评论/分享数据。

## ✨ 主要能力

- **AI 视频生成**：支持 Veo3.1 / Sora2 / Wan2.x / Seedance / kling-v3-omni 等多种视频模型
- **TikTok 自动发布**：按用户配置的数量、开始时间、间隔自动定时发布到指定账号
- **结果统计**：自动查询播放量、点赞、评论、分享、视频明细等数据，并展示 TikTok 链接

> 仅做 TikTok 视频生成与发布。如需配合客户挖掘 / 邮件 / 电话 / 短信等销售协作，请使用 `deepsop-humabot`。

## 🚀 快速开始

1. **获取 API Key**
   - 已有账号 → [https://ai.deepsop.com/login?source=5](https://ai.deepsop.com/login?source=5)
   - 没有账号 → [https://ai.deepsop.com/register?source=5](https://ai.deepsop.com/register?source=5)
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
   - "生成一条产品宣传视频发布到 TikTok"
   - "帮我每天发 3 条 AI 视频到 TikTok，从早 9 点开始，间隔 1 小时"
   - "生成 5 条库阔 AI 介绍视频，9:30 开始发布"

## 📖 完整文档

详细使用说明、参数约定、错误处理流程请查看 [SKILL.md](SKILL.md)。

## ⚠️ 重要提醒

- 提交 `agentSubmitTask` **必须**走 `scripts/submit_task.py`（脚本内置 UTF-8 安全提交 + 参数预校验）
- **禁止**直接写 `curl` 命令（Windows cp936 代码页会导致中文乱码）
- `param` 必须传完整 27 个键（即使当前 methodType 下某些字段不生效，也按默认值给出）
