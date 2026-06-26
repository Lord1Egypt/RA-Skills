---
name: design-daily-insights
description: "Design Daily Insights — Track design tool updates, AI product news, design system evolution, UX research, and design inspiration. Triggers on: '今日设计资讯', '设计资讯', '今日设计', 'design daily', 'design news', /design."
---

# Design Daily Insights / 设计每日资讯

设计领域每日双语资讯 — 追踪设计工具更新、AI 产品动态、设计系统、深度研究和灵感发现。

## 数据源

详见 [references/sources.md](references/sources.md)，共 19 个信息源：

### A 类 — web_fetch 直接抓取（13 个）

**🎨 工具更新（5 个）**
- Figma Blog: https://www.figma.com/blog/
- Lovable Blog: https://lovable.dev/blog
- Cursor Blog: https://cursor.com/blog
- Framer Blog: https://www.framer.com/blog
- VS Code Updates: https://code.visualstudio.com/updates

**🤖 AI 动态（2 个）**
- Anthropic News: https://www.anthropic.com/news
- Anthropic Research: https://www.anthropic.com/research

**🏗️ 设计系统（2 个）**
- Zeroheight Blog: https://zeroheight.com/blog/
- Supernova Blog: https://www.supernova.io/blog

**📖 设计深度（3 个）**
- NNGroup: https://www.nngroup.com/articles/
- Smashing Magazine: https://www.smashingmagazine.com/
- Creativerly: https://www.creativerly.com/

**💡 灵感发现（1 个）**
- Sidebar.io: https://sidebar.io

### B 类 — web_search 补充（6 个）

| 源 | 搜索关键词 |
|---|---|
| Product Hunt | `Product Hunt design tools launches` |
| The Rundown AI | `The Rundown AI newsletter` |
| Ben's Bites | `Ben's Bites AI news` |
| UX Collective | `site:uxdesign.cc design` |
| TLDR Design | `TLDR design newsletter` |
| Google Stitch | `Google Stitch design update` |

## 摘要规则

- **双语**：标题 `English Title / 中文标题` 放同一行
- **内容**：英文摘要在前（2-3 句），中文摘要在后（2-3 句），各段折行显示
- **角度**：突出"是什么 + 对设计师/开发者有什么影响"
- **每条附原文链接**：`→ full-url`
- **⚠️ 链接必须是具体文章 URL，不能是官网/博客首页**：
  - ✅ `https://www.figma.com/blog/five-figma-weave-workflows/`
  - ❌ `https://www.figma.com/blog/`（首页，看不到具体文章）
  - ✅ `https://cursor.com/blog/bugbot-learning`
  - ❌ `https://cursor.com/blog`（首页）
  - 获取方式：抓取博客索引页时，必须从页面中提取每篇文章的实际 URL，而非统一链接到分类页或首页
- **总条数**：10-15 条，每分类 2-3 条
- **总输出**：≤ 2000 字（中文计）

## 分类

- 🎨 工具更新 / Tool Updates — 产品功能、版本发布、更新公告
- 🤖 AI 动态 / AI Updates — 模型发布、AI 产品、行业变动
- 🏗️ 设计系统 / Design Systems — 设计系统更新和深度内容
- 📖 设计深度 / Design Deep Dive — UX 研究、方法论、案例
- 💡 灵感发现 / Inspiration — 精选内容、趋势、展示案例

## 去重

读写 `memory/design-digest-state.json`，按 URL 去重：

```json
{
  "seen": {
    "url-or-id-1": "2026-03-28"
  }
}
```

- 每次运行时读取已有 seen 列表
- 抓到的新内容中，过滤掉已存在于 seen 中的 URL
- 生成摘要后，将新 URL 以当天日期（YYYY-MM-DD）写回 seen
- 自动清理 7 天前的条目

## 运行流程

1. 读 `memory/design-digest-state.json` 获取去重状态
2. web_fetch 13 个 A 类源，每个源最多抓取前 5000 字
3. web_search 6 个 B 类源补充
4. 过滤已读内容（URL 去重）
5. 三层筛选：
   - 新鲜度：只保留 7 天内的内容
   - 相关性：匹配分类关键词
   - 价值度：优先头部产品、信息密度高、独特分析的内容
6. 筛选 top 10-15 条，按 5 个分类组织
7. 生成双语摘要
8. 更新 `memory/design-digest-state.json`（写入新 URL + 清理过期条目）
9. **部署网页**：将 HTML 输出到 `design-daily-site/index.html`（使用下方「网页设计」中的杂志风模板），启动本地 HTTP 服务器，通过 locaddr.run 生成临时公开 URL
10. 按输出模板格式化，在飞书消息末尾附上网页链接，发送飞书消息

> ⚠️ 署名已更新为「多啦啊木 🐾」

> **⚠️ 关于网页 URL**：locaddr.run 每次重启链接会变。如需固定 URL，推荐部署到 GitHub Pages、Cloudflare Pages 或 Vercel（`npx vercel` 一键部署），可获得永久地址。

## Token 控制

- 每个源站最多抓取前 5000 字
- 每条最终摘要 ≤ 3 句（英文）+ 3 句（中文）
- 总输出 ≤ 2000 字

## 飞书输出模板

```
📅 设计每日资讯 | Design Daily — YYYY-MM-DD
🔗 网页版：https://<当期-locaddr-URL>

🎨 工具更新 / Tool Updates

1. English Title / 中文标题
   英文摘要 1-2 句。
   中文摘要 1-2 句。
   → https://actual-article-url-here.com/article-slug

2. ...

🤖 AI 动态 / AI Updates

3. English Title / 中文标题
   ...

🏗️ 设计系统 / Design Systems

6. English Title / 中文标题
   ...

📖 设计深度 / Design Deep Dive

10. English Title / 中文标题
    ...

💡 灵感发现 / Inspiration

12. English Title / 中文标题
    ...

—
Sources: Figma · Cursor · Framer · Anthropic · Zeroheight · Supernova · NNGroup · Smashing Magazine · Sidebar | Curated by 多啦啊木 🐾
```

### 排版规则

- **网页链接位置**：标题下方第一行，紧跟日期之后（先 URL，再内容）
- **来源署名**：底部独占一行，以 `—` 分隔结尾
- **每条格式**：序号 + 英文标题/中文标题（同一行）→ 英文摘要 → 中文摘要 → 链接（`→` + 完整文章 URL）
- **不使用 markdown 表格**（飞书兼容）
- **同一新闻多源出现时只保留最佳版本**
- **跳过低价值内容**：纯营销、泛泛列表文、招聘信息

- 标题：一行，`English Title / 中文标题`
- 英文摘要在前，折行；中文摘要在后，折行
- 链接：`→ full-url` 独占一行
- 不使用 markdown 表格（飞书兼容）
- 同一新闻多源出现时只保留最佳版本
- 跳过低价值内容：纯营销、泛泛列表文、招聘信息

## 网页设计 / Web Design

### 模板位置
`/Users/Ellison/.openclaw/workspace/design-daily-site/index.html`

### 设计风格：高级杂志风（Editorial Magazine）

**⚠️ 设计已锁定，不主动更换**
- `design-daily-site/index.html` = 杂志风 HTML 模板
- 每次运行时只替换内容（日期、各 article 区块），不修改 CSS 结构和设计变量
- 如需改版设计，需 MZQ 明确授权

**配色方案（大胆张扬）**

```css
:root {
  --paper: #f8f6f1;        /* 暖调米白底 */
  --paper-warm: #f0ebe2;   /* 微暖卡片底 */
  --ink: #120d0a;          /* 深墨文字 */
  --ink-soft: #4a3530;     /* 温暖次要文字 */
  --muted: #8a7060;        /* 弱化文字 */
  --rule: #d8cfc5;         /* 分隔线 */
  --accent: #c94830;       /* 赤陶红强调（大胆） */
  --accent-soft: rgba(201,72,48,0.1);
}
```

**背景纹理（四层弥散渐变 + SVG noise）**

```css
background:
  var(--paper)
  radial-gradient(ellipse 80% 60% at  10%  0%, rgba(201,72,48,0.09) 0%, transparent 60%),
  radial-gradient(ellipse 60% 50% at  90% 10%, rgba(160,50,30,0.07) 0%, transparent 55%),
  radial-gradient(ellipse 50% 40% at  50%  0%, rgba(201,72,48,0.06) 0%, transparent 50%),
  radial-gradient(ellipse 70% 80% at  80% 100%, rgba(50,90,60,0.07) 0%, transparent 60%);
/* noise texture via ::before pseudo-element with inline SVG */
```

**字体搭配**
- 标题/品牌：`Playfair Display`（衬线，优雅）
- 正文：`Inter`（无衬线，现代）
- 中文备选：`Noto Serif SC`

**布局结构**
1. **Masthead** — 双栏报头，大字 `设计每日资讯`，双线分隔符
2. **Hero Zone** — 左侧大标题 + 副标题 + 日期，右侧 Sidebar 小标题列表
3. **Section Header** — 装饰分隔线 + 全大写分类标签（🎨 / 🤖 / 🏗️ / 📖 / 💡）
4. **Article Cards** — 编号列表，大号灰色数字 + 标题 + 摘要 + 文章链接
5. **Pull Quote** — 左侧红色装饰竖线 + 引文
6. **Footer** — 双线分隔符 + 来源列表 + 署名 `多啦啊木 🐾`

**署名**：页面底部 `多啦啊木 🐾`，飞书消息末尾同步

**移动端适配（三档响应式，已优化）**
- **1000px**（平板）：双栏 → 单栏；Hero 右栏加顶部分隔线替代左分隔线；数字列表隐藏来源域名
- **640px**（手机主档）：报头大字缩至 38px、隐藏副标题/期号；导航栏横向滚动（隐藏滚动条）；卡片网格单列 + 圆角卡片；分类标题 10px 紧凑字间距；数字列表行号 32px；页脚单列紧凑排布
- **360px**（超小屏）：标题/正文字号再缩一档
- 导航栏：横滚 + `flex-shrink:0` + `overflow-x:auto` + `scrollbar-width:none`

### 内容替换位置（每次运行）

运行时只需替换 HTML 中以下位置的内容：
1. `<title>` 和 `.hero-date` — 当天日期
2. 各 `<article>` 区块 — 精选文章标题、摘要、链接
3. `<footer>` 来源行 — 当期来源列表

CSS 变量、字体引用、背景纹理代码**不改动**。

### 部署流程

```bash
# 1. 写入 HTML（用模板覆盖）
cp /Users/Ellison/.openclaw/workspace/design-daily-site/index.html \
   /Users/Ellison/.openclaw/workspace/design-daily-site/build.html

# 2. 启动本地 HTTP 服务器（端口 8766）
cd /Users/Ellison/.openclaw/workspace/design-daily-site
python3 -m http.server 8766 &

# 3. 创建公开链接（locaddr.run）
ssh -o StrictHostKeyChecking=no \
  -R 80:localhost:8766 locaddr.run &

# 4. 验证可用性
curl -s -o /dev/null -w "%{http_code}" https://<生成的URL>/
```

### 部署脚本

已创建的辅助脚本：`scripts/design-daily-cron.sh`（见下方定时任务章节）

## 定时任务 / Cron

### 设置每日 9:00 北京时间自动发送

```bash
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

> ⚠️ 推荐加上 `--timeout-seconds 180`（3分钟），因为任务涉及 13 个源站抓取 + locaddr 隧道建立，30秒默认超时容易触发。
> `--failure-alert --failure-alert-after 2` 开启连续2次失败后通知。

### 另一种方式：指定小时判断

如果 cron 不支持时区转换，可写一个包装任务：

1. 创建一个辅助脚本 `scripts/design-daily-cron.sh`：

```bash
#!/bin/bash
# 每天北京时间 9:00 触发（UTC 1:00）
openclaw run "今日设计资讯" --channel feishu
```

2. 设置 cron：`0 1 * * * /Users/Ellison/.openclaw/workspace/skills/design-daily/scripts/design-daily-cron.sh`

3. 确保脚本有执行权限：`chmod +x scripts/design-daily-cron.sh`

### 查看/删除定时任务

```bash
openclaw cron list
openclaw cron delete <id>
```

### 定时任务的限制

- 定时任务运行在独立的 session 中，无主 session 历史上下文
- **默认超时 30 秒**，任务涉及多源抓取 + 隧道部署，建议设为 180 秒避免超时
- 建议在 `memory/design-digest-state.json` 中记录上次运行时间，避免重复发送
- 如果需要在飞书群发送，channel 指定为群 ID 或群名

## 命令

- `/design` — 手动触发一期 digest
- `/design setup` — 初始化配置和去重状态
- `/design sources` — 查看当前追踪的所有信息源
- `/design add <URL>` — 添加新的 A 类信息源到 sources.md
