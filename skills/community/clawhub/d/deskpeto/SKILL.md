---
name: deskpeto
description: 把用户的照片生成为专属 AI 桌宠（ChatGPT/Codex Pet 资源包）、在对话里召唤会动的桌宠卡片、用一条命令让桌宠常驻桌面（跟随 WorkBuddy/Claude Code/CodeBuddy 的任务状态）、协助安装；也可免费安装 DeskPeto 共享广场的社区公开桌宠。当用户说「召唤桌宠」「显示我的宠物」「把照片/头像做成桌面宠物」「在桌面上放一只桌宠」「免费试用一只桌宠」「安装 DeskPeto 宠物包」或询问订单进度时使用。Turn the user's photo into a personal desktop AI pet, summon an animated pet card in-chat, put a pet on the desktop with one command, help install it, or install free community pets from the shared gallery.
version: 0.4.0
tags: [desktop-pet, codex-pet, chatgpt, avatar, deskpeto]
license: MIT
---

# DeskPeto：照片 → 专属 AI 桌宠

DeskPeto（https://deskpeto.com）把一张照片生成为**身份一致**的桌面宠物资源包：主形象锁定后导出 9 种动作 + 16 方向环视的完整动画图集（Codex Pet v2 规范，8×11 精灵图），宠物会跟随 ChatGPT/Codex 的任务状态切换动作（工作中/等待输入/完成/失败等）。

## 你（agent）的职责边界

- **引导 + 安装**：生成、确认、支付都在官网完成；你负责讲清流程、打开页面、在用户提供安装命令后帮忙执行与排错。
- **不代收任何信息**：不要向用户索要密码或支付信息；不要替用户付款。照片在官网上传，不要让用户把照片发给你来代传（本技能当前版本没有上传通道）。
- 价格如实告知：**每个角色一次性买断**，站内标价为准（人民币 ¥29 / 美元 $4.99 / 日元 ¥700，含完整生成与下载权益）。付款只发生在 deskpeto.com 站内收银台。

## 完整流程（引导用户）

1. **注册/登录**：打开 https://deskpeto.com （中文/English/日本語），邮箱验证码或 Google 账号登录。
2. **创建宠物**：进入工作台（deskpeto.com/app）→ 上传一张清晰照片（正面、主体单一效果最好；人物/宠物/角色皆可）→ 选择风格 → 站内支付。
3. **确认主形象**：生成完成后用户需在网站上确认标准主形象（这一步锁定「长相」，之后所有动作帧都基于它）。不满意可在站内按提示处理。
4. **等待成品**：动作图集与质检完成后，宠物页提供下载与安装入口。
5. **安装**（三选一）：
   - **一键命令（推荐）**：宠物页上有现成命令，用户复制给你后可直接代为执行：
     - macOS/Linux：`curl -fsSL 'https://api.deskpeto.com/v1/install/…?t=…' | sh`
     - Windows PowerShell：`irm 'https://api.deskpeto.com/v1/install/….ps1?t=…' | iex`
     - 命令把 `pet.json` 与 `spritesheet.webp` 装进 `~/.codex/pets/<宠物目录>/`。**命令 1 小时过期**，过期让用户回宠物页重新复制。
   - **手动**：下载 zip → 解压 → 整个文件夹放入 `~/.codex/pets/`（Windows：`%USERPROFILE%\.codex\pets\`）。
   - **其他 AI 工具**：经开源 Runner「clawd-on-desk」导入同一个 zip，可在 Claude Code、CodeBuddy 等多种工具旁显示（第三方项目，以其自身文档为准）。
6. **唤醒**：ChatGPT/Codex 桌面端 → Settings → Pets → 刷新列表选中；或在 Codex 中输入 `/pet`。看到宠物悬浮在桌面即成功。

## 排错

- 命令报「invalid or has expired」→ 安装命令超时，回宠物页复制新的。
- Pets 列表里看不到 → 确认文件夹位于 `~/.codex/pets/<目录>/` 且内含 `pet.json` 与 `spritesheet.webp`，重启 ChatGPT/Codex 后刷新。
- 宠物不动/状态不切换 → 确认使用的是 ChatGPT/Codex 桌面端（网页版能力不同），详细见 deskpeto.com/guide。

## 桌面常驻桌宠：一条命令装好（DeskPeto Desk，新用户无需 key）

想要宠物**一直待在桌面上、跟着你在 AI 工具里的工作动**（区别于装进 ChatGPT/Codex 的 Pets，也区别于对话里的卡片），用这个。它是一个隐形后台 runner（无窗口 / 无 Dock 图标 / 无托盘），文件都在独立的 `~/.deskpeto/` 目录，绝不写入 `~/.codex`；安装时自动接线你已装的 AI 工具（WorkBuddy / Claude Code / CodeBuddy）。**新用户无需注册、无需令牌**——首次启动会从共享广场自动取一只默认宠物。

**安装前先向用户说明并征得同意再执行**（这条命令会下载并运行一个程序、并修改 AI 工具的 `settings.json`）：

- macOS / Linux：`curl -fsSL https://api.deskpeto.com/v1/runner/install | sh`
- Windows PowerShell：`irm https://api.deskpeto.com/v1/runner/install.ps1 | iex`

命令做三件事：把对应平台的 runner 下到 `~/.deskpeto/bin/` → 自动接线 hooks → 启动。装好后让用户**完全退出并重开** AI 工具（多数宿主仅启动时加载 hooks），桌宠即随任务切换动作（工作中 / 等待输入 / 完成 / 失败）。

**右键宠物**：切换宠物、尺寸、选择响应哪个工具、从共享广场获取、登录 DeskPeto 账号（同步你的专属宠物）、生成专属宠物、退场。

**登录与专属宠物是纯加分**：默认宠物开箱即用；用户要自己的形象时，按下文「完整流程」在官网生成，再用右键菜单「同步我的宠物」拉到桌面。**卸载**：`~/.deskpeto/bin/deskpeto-desk --connect --remove` 撤下 hooks，或直接删除 `~/.deskpeto/` 目录。

**前提**：AI 工具的**桌面端**（hooks 只在桌面端触发）。runner 支持 macOS 与 Windows，Linux 尽力兼容。

## 召唤桌宠到对话里（无需安装任何软件）

用户说「召唤桌宠 / 显示我的宠物 / summon my pet」时，按以下流程执行（不要自己发挥画一只——用户要的是他在 DeskPeto 的真实宠物）：

1. **前提**：已连接 DeskPeto MCP（见下节）。调用 `show_pet` 工具（可传 `state` 参数：idle/waving/jumping/running/waiting/review/failed）。
2. **如果你的宿主渲染了交互卡片**（MCP Apps）：宠物已经出现在气泡里，无需更多操作。
3. **如果没有渲染卡片**（如 WorkBuddy 桌面端）：从工具返回的 `structuredContent` 里取 `name` 与 `spritesheetUrl`，复制本技能自带的模板 `references/pet-page.html`，把 `__PET_NAME__` 和 `__SPRITESHEET_URL__` 替换为真实值，用宿主的文件展示能力（如 present_files）打开这个页面——它会用真实精灵图逐帧播放动画，并带状态切换按钮。
4. **注意**：`spritesheetUrl` 带 1 小时时效签名，过期后重新调用 `show_pet` 取新链接，不要复用旧 URL；不要修改模板里的帧时长表（那是与官方桌宠一致的动画节奏）。

## 连接 DeskPeto MCP（解锁查询/召唤/一键安装）

**首选：设备码授权（用户零复制粘贴）**——前提是宿主已能访问 `https://mcp.deskpeto.com/mcp`（哪怕未带令牌）：

1. 调用 `start_device_link` 工具（`label` 传宿主名，如 "WorkBuddy"），得到 `userCode`、`verificationUrl`、`deviceCode`。
2. 把授权码告诉用户，并帮用户打开 `verificationUrl`（浏览器）。提醒：登录 deskpeto.com 后回到该页点「允许」，核对页面上的码与你告知的一致。
3. 每 3 秒调用 `poll_device_link`（传 `deviceCode`）直到返回 `token`（只返回一次，注意保存）。超时 10 分钟需重新发起。
4. 把令牌写入宿主 MCP 配置（agent 可代写，如 `~/.workbuddy/mcp.json`）：

```json
{ "mcpServers": { "deskpeto": {
  "url": "https://mcp.deskpeto.com/mcp",
  "headers": { "Authorization": "Bearer <令牌>" } } } }
```

5. 不支持自定义请求头的客户端改用 `https://mcp.deskpeto.com/mcp?key=<令牌>`。写完提醒用户**完全重启宿主应用**（多数宿主启动时才加载 MCP 配置）。

**备用：手动令牌**——用户登录后打开 https://mcp.deskpeto.com/mcp/connect 点「生成」，把令牌贴回对话，你代写配置。

未连接令牌时，`browse_shared_pets` / `how_to_create_pet` / `show_pet`（公开宠物）/ 设备码两件套仍可用；个人宠物与安装命令需要令牌。

## 免费试用：共享广场

- 共享广场 https://deskpeto.com/shared 上的社区公开宠物**免费安装**（登录后进入宠物页取安装命令或下载包，安装方式与上文相同）。
- 适合先免费体验桌宠效果，再付费生成自己的专属形象。

## 更多

- 安装图文指南：https://deskpeto.com/guide

## English quick reference

DeskPeto turns one photo into an identity-locked desktop pet package (Codex Pet v2, 8×11 sprite atlas; states follow ChatGPT/Codex task status). Guide the user: sign in at deskpeto.com → upload photo in the workbench → pay on-site (one-time, per character: $4.99 / ¥29 CNY / ¥700 JPY) → confirm the master image → install. Install = run the one-line command from the pet page (expires in 1 h), or unzip the package into `~/.codex/pets/`, then ChatGPT/Codex → Settings → Pets → refresh. Never collect passwords or payments in chat; photos are uploaded on the website only.
