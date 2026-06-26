---
name: ai-news-publisher
description: AI新闻一键发布技能。从36氪/虎嗅获取AI新闻，改写成爆款文章，发布到微信公众号。触发词：发布AI新闻、公众号发文章、科技新闻发布、爆款文章。
---

# AI新闻一键发布

一键从科技媒体获取AI新闻，改写成爆款文章，发布到微信公众号草稿箱。
完全独立，不依赖任何第三方技能。

## 目录结构
- `scripts/`: 包含微信发布脚本(`publish.sh`)、环境配置(`setup.sh`)和新闻抓取脚本(`scrape_news.py`)。
- `assets/`: 默认封面图(`default-cover.jpg`)。
- `references/`: 包含详细的写作指南和Scrapling抓取/解析说明。

## 环境准备与依赖
- 依赖：确保已安装 `scrapling` (Python) 和 `@wenyan-md/cli` (Node.js)。
- 凭证：环境变量须包含 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`（或通过 `source scripts/setup.sh` 加载）。
- 权限：确保当前服务器IP（可通过 `curl ifconfig.me` 获取）已加入公众号开发基本配置的白名单。

## 完整工作流程

当触发本技能时，请严格按以下步骤执行：

1. **抓取新闻列表**
   使用 `scrapling` 获取 36氪 或 虎嗅 的AI频道新闻列表：
   ```bash
   scrapling extract get "https://www.36kr.com/information/AI/" /tmp/ai-news.md
   ```
   *(注：如果遇到反爬拦截，可使用 `fetch --network-idle` 或 `stealthy-fetch`)*

2. **去重与选题策划**
   - 提取最新10条新闻的标题、摘要、链接。
   - 读取已发布记录：`cat memory/selected-topics.md`，排除近3天已发布或相似的主题。
   - 选出1条最具爆款潜质的新闻（热点性、争议性、情绪价值等）。

3. **抓取原文与改写**
   - 抓取选中新闻的原文内容。
   - **极其重要**：在改写之前，请务必阅读 [references/writing-guide.md](references/writing-guide.md) 获取爆款标题公式、结构模板和行文节奏指南。
   - 按照指南，改写为 1000-2000 字的高质量文章，包含钩子、痛点、分析、互动引导和金句。

4. **格式化文章**
   生成包含必需 Frontmatter 的 Markdown 文件：
   ```markdown
   ---
   title: 爆款标题（≤30字）
   cover: /root/.openclaw/workspace/skills/ai-news-publisher/assets/default-cover.jpg
   ---
   
   # 正文开始...
   ```
   *(注意：封面必须是绝对路径，正文段落宜简短并适当加粗)*

5. **发布到草稿箱**
   使用专用脚本发布（推荐使用 lapis 主题和 solarized-light 代码高亮）：
   ```bash
   /root/.openclaw/workspace/skills/ai-news-publisher/scripts/publish.sh /tmp/final-article.md lapis solarized-light
   ```

6. **记录选题与收尾**
   - 记录本次发布：
     ```bash
     echo "- $(date +%H:%M) | 文章标题 | 原文链接" >> memory/selected-topics.md
     ```
   - 向用户返回文章草稿箱链接及预览信息。

## 错误处理
- **抓取失败**：依次降级尝试 `fetch` -> `stealthy-fetch` -> 更换新闻源。
- **发布报错 (ip not in whitelist)**：提示用户将服务器公网IP加白。
- **发布报错 (title/cover missing)**：检查 Markdown 头部是否严格按照要求包含了 `title` 和 `cover` 字段。

## 详细指南（按需参考）
在使用此技能时，遇到具体细节问题请查阅以下参考文件：
- [writing-guide.md](references/writing-guide.md) - **写作必读**：爆款文章结构、标题公式、金句模板及排版要求。
- [scrapling-fetching.md](references/scrapling-fetching.md) - 抓取指南：命令用法、隐身模式、代理配置。
- [scrapling-parsing.md](references/scrapling-parsing.md) - 解析指南：CSS/XPath选择器用法与API。