# Design Daily Insights 🎨

追踪设计工具、AI 设计动态和设计资讯的每日/每周摘要。

## 功能

- 追踪 19 个信息源（Figma、Cursor、Anthropic、Smashing Magazine、NNGroup 等）
- 每日/每周自动推送到你的聊天窗口
- 双语输出（中文/英文）
- 智能去重，避免重复内容
- 自动清理 7 天前的历史记录

## 支持的平台

- OpenClaw（推荐）
- Claude Code

## 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install design-daily-insights
```

### 方式二：手动安装

```bash
# Clone 到你的 skills 目录
git clone https://github.com/yourusername/design-digest ~/.openclaw/workspace/skills/design-daily
```

## 快速开始

安装完成后，在你的 OpenClaw 聊天窗口输入：

```
/design
```

第一次运行时会自动初始化配置和去重状态文件。

## 命令

| 命令 | 说明 |
|--------|------|
| `/design` | 手动触发一期设计资讯摘要 |
| `/design setup` | 初始化配置和去重状态 |
| `/design sources` | 查看当前追踪的所有信息源 |
| `/design add <URL>` | 添加新的信息源（仅限 web_fetch 支持的站点） |

## 数据源

### A 类 — 直接抓取（13 个）

**🎨 工具更新**
- Figma Blog: https://www.figma.com/blog/
- Lovable Blog: https://lovable.dev/blog
- Cursor Blog: https://cursor.com/blog
- Framer Blog: https://www.framer.com/blog
- VS Code Updates: https://code.visualstudio.com/updates

**🤖 AI 动态**
- Anthropic News: https://www.anthropic.com/news
- Anthropic Research: https://www.anthropic.com/research

**🏗️ 设计系统**
- Zeroheight Blog: https://zeroheight.com/blog/
- Supernova Blog: https://www.supernova.io/blog

**📖 设计深度**
- NNGroup: https://www.nngroup.com/articles/
- Smashing Magazine: https://www.smashingmagazine.com/
- Creativerly: https://www.creativerly.com/

**💡 灵感发现**
- Sidebar.io: https://sidebar.io

### B 类 — 搜索补充（6 个）

| 源 | 搜索关键词 |
|-----|-----------|
| Product Hunt | `Product Hunt design tools launches` |
| The Rundown AI | `The Rundown AI newsletter` |
| Ben's Bites | `Ben's Bites AI news` |
| UX Collective | `site:uxdesign.cc design` |
| TLDR Design | `TLDR design newsletter` |
| Google Stitch | `Google Stitch design update` |

## 自定义

### 添加信息源

```
/design add https://example.com/blog
```

### 调整摘要风格

编辑 `SKILL.md` 中的"摘要规则"部分：

- 每条摘要的句子数量
- 输出字数限制
- 分类组织方式

### 更换语言和频率

编辑 `SKILL.md` 中的"输出模板"部分：

- 修改为单语或双语
- 调整每日/每周触发频率

## 网页展示

每次推送时会生成一份高级杂志风（Editorial Magazine）的独立网页，发布到临时的公开 URL，方便在更大屏幕上阅读或分享。

**设计特点：**
- 暖调米白底 + 赤陶红强调色，配 SVG 噪点纹理
- 字体：Playfair Display（标题） + Inter（正文）+ Noto Serif SC（中文）
- 完整响应式：桌面 / 平板（1000px）/ 手机（640px）/ 超小屏（360px）
- 导航锚点分类：🎨 工具更新 / 🤖 AI 动态 / 🏗️ 设计系统 / 📖 设计深度 / 💡 灵感发现
- Hero 区域展示 Featured 文章，侧边栏显示热门条目
- 卡片网格 + 数字编号列表 + 引用块

**部署方式：**
- 本地 HTTP 服务器（端口 8766）+ locaddr.run 隧道
- 如需固定 URL，推荐部署到 GitHub Pages、Cloudflare Pages 或 Vercel（`npx vercel` 一键部署）

**注意：** 网页设计已锁定，不主动更换 CSS 结构。如需改版设计，需明确授权。

## 定时推送

使用 OpenClaw 的 cron 功能设置自动推送：

```bash
# 每天北京时间 9:00 自动推送
openclaw cron create \
  --name "Design Daily 每日设计资讯" \
  --schedule "0 0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "今日设计资讯" \
  --channel feishu \
  --timeout-seconds 180 \
  --failure-alert \
  --failure-alert-after 2
```

> ⚠️ 建议 `--timeout-seconds 180`（3分钟），因为任务涉及 13 个源站抓取 + locaddr 隧道建立，默认 30 秒容易超时。

## 输出示例

推送内容包含飞书消息 + 网页版链接：

```
📅 设计每日资讯 | Design Daily Insights — 2026-04-10
🔗 网页版：https://xxxxx.locaddr.run

🎨 工具更新 / Tool Updates

1. Five Figma Weave Workflows / 五个 Figma Weave 工作流
   展示如何通过自然语言提示构建、编辑和主导视觉输出。
   展示如何通过自然语言提示构建、编辑和主导视觉输出。
   → https://www.figma.com/blog/five-figma-weave-workflows/

🤖 AI 动态 / AI Updates

2. Glasswing / The Secure AI Initiative
   Anthropic 联合 AWS、Apple、Google、Microsoft、NVIDIA 等 12 家科技巨头
   启动 Glasswing 计划，目标是保障全球关键软件的安全。
   → https://www.anthropic.com/glasswing

🏗️ 设计系统 / Design Systems
📖 设计深度 / Design Deep Dive
💡 灵感发现 / Inspiration

—
Sources: Figma · Cursor · VS Code · Anthropic · Zeroheight · Supernova · NNGroup · Smashing Magazine · Sidebar | Curated by 多啦啊木 🐾
```

## 工作原理

1. 读取 `memory/design-digest-state.json` 获取去重状态
2. 使用 `web_fetch` 抓取 A 类源（每个源最多 5000 字）
3. 使用 `web_search` 补充 B 类源
4. 过滤已读内容（URL 去重）
5. 三层筛选：新鲜度（7 天内）→ 相关性 → 价值度
6. 筛选 top 10-15 条，按 5 个分类组织
7. 生成双语摘要
8. 更新去重状态文件（清理 7 天前数据）
9. 按模板格式化，发送到聊天窗口

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
