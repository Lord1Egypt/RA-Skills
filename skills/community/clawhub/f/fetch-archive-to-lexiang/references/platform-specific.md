### 微信公众号文章处理（mp.weixin.qq.com）

**首选方案：乐享 MCP `file_create_hyperlink`（2026-05-09 验证 ✅）**

乐享后端原生支持微信公众号文章的抓取与解析，**一步到位**，无需本地抓取和手动上传图片。

```
mcp__lexiang__file_create_hyperlink(
  url = "https://mp.weixin.qq.com/s/...",
  parent_entry_id = "<目标目录 entry_id>",
  name = "<文章标题>"  // 可选，不传会自动从微信提取
)
```

**返回值**：
- `finished: true` — 后端抓取完成
- `entry.id` — 新创建的知识条目 ID
- `entry_type: "flink"` — 外部链接类型
- `extension: "wechat"` — 自动识别微信来源

**后端自动完成的事情**：
1. 抓取微信文章全文（正文 + 图片）
2. 图片保存到乐享 COS（`/assets/xxx` 格式）
3. OCR 识别图片中的文字（用于全文检索和 AI 解析）
4. 自动提取标题、作者、发布时间等元信息

**优势**：
- 一步完成，省去 fetch_article.py + 分块导入 + 逐张上传图片的复杂流程
- Token 消耗从 ~50K 降到 <1K
- 图片质量由乐享后端保证，无需本地下载和上传
- 支持乐享的全文检索和 AI 解析（RAG）

**如需附加用户评价/评论**：
- 优先使用乐享评论能力。
- 若必须修改页面内容，仅作为少量人工增量维护，并同步本地 Markdown。

**降级方案（当 `file_create_hyperlink` 失败时）**：
- 如果返回 `finished: false` 或错误码，改用 `fetch_article.py` 本地抓取 + 降级方案 A 导入
- 某些被限制的微信文章（如已删除、需付费等）可能无法通过此接口抓取

**注意事项**：
- 产出的 entry_type 是 `flink`（外部链接），而非 `page`（在线文档）
- flink 类型在乐享中以原始文章格式展示，支持全文检索和 AI 解析
- 如果用户明确要求以「在线文档/page」格式存储（需要后续编辑），才使用 fetch_article.py 降级方案

### 得到 APP 文章抓取（dedao.cn）

**核心问题**：得到 APP（`www.dedao.cn`）的文章内容是**付费内容 + SPA 动态渲染**，`web_fetch` 和 `fetch_article.py` 的通用提取逻辑都无法直接获取正文。

**技术原因**：
1. **SPA 架构**：得到网页版是 React SPA，文章正文通过 JS 异步渲染，`web_fetch` 只能拿到空白壳页面
2. **付费墙**：文章属于付费专栏内容，必须有已登录且已订阅的账号才能查看全文
3. **DOM 结构特殊**：正文容器使用 `.iget-articles` 类名，不在 `fetch_article.py` 的默认选择器列表（`article`、`.post-content` 等）中。通用 `article` 选择器只匹配到极少内容（~167 字符），而真正的正文在 `.iget-articles` 中有 6000+ 字符
4. **内容区混杂**：正文容器中混入了标题重复、音频时长、"划重点"、用户评论等非正文内容，需要清理

**抓取方案**：使用 **CDP 模式**连接 CDP Chrome（9222 端口）：

```bash
# 前提：CDP Chrome 在运行，且用户已在 CDP Chrome 窗口（非日常 Chrome）登录得到
curl -s http://127.0.0.1:9222/json/version   # 预检
~/.fetch_article/start-cdp-chrome.sh          # 若未运行
python scripts/fetch_article.py fetch "https://www.dedao.cn/course/article?id=<ID>" --output-dir <目录> --cdp
```

**已知限制**：
- `fetch_article.py` 的通用内容提取逻辑对得到 DOM 结构匹配不佳，**抓取结果可能不完整**
- **CDP 零标签页陷阱**（2026-07-07 修复）：CDP Chrome 所有 tab 关闭时 `connect_over_cdp` 失败；v2.8.3 起自动创建种子 tab。旧版会静默回退到 `Google Chrome for Testing`（无登录态）
- **CDP 连接失败**：`--cdp` 模式下 v2.8.3 起禁止回退到 Testing Chrome，应修复 CDP 环境（见 SKILL.md Step 0d）后重试
- **WebFetch 降级方案**：当 CDP 完全不可用时，可用 `WebFetch` 侦察，但若无法证明是完整原文则不得归档；手工补全时也必须生成标准 `source.md`、`images/`、`meta.json`
- 正确做法是通过 Playwright CDP 连接后，**手动指定 `.iget-articles` 选择器**提取正文：

```python
# 通过 CDP 连接后，用专用选择器提取得到文章正文
content_el = await page.query_selector('.iget-articles')
if content_el:
    text = await content_el.inner_text()  # 完整正文
```

**内容清理要点**：
- 去掉正文开头的标题重复、日期、音频时长等元信息（通常在 `凡哥杂谈，你好` 或类似开场白之前）
- 去掉正文末尾的"划重点"、"添加到笔记"、"首次发布"、"用户留言"等非正文内容
- 如果是多篇系列文章（如上/下篇），合并时用 `## 上篇` / `## 下篇` 分隔
- 作者信息需要手动确认（通用提取器可能抓错）

**得到文章现行流程**：

1. `fetch_article.py ... --cdp` 生成标准 `source.md`、`images/`、`meta.json`。
2. 不在抓取层删除图片或清洗正文；非中文或需复杂清洗时，将整个工作包交给
   `trans-doc-to-md` Prepared Markdown Package 模式。
3. 最终标题 Markdown 只交给 `upload-markdown-to-lexiang`，由 uploader 保持图片位置并
   渲染富元素。

**适用场景**：得到 APP 专栏文章（`www.dedao.cn/course/article?id=xxx`）

**计划**：考虑在 `fetch_article.py` 中增加得到专用检测和选择器（类似微信公众号的 `_is_wechat_article` 机制），自动使用 `.iget-articles` 提取正文。

### SPA 网站 Playwright 直接出 PDF（正文隔离方案）

**适用场景**：
- `fetch_article.py` 抓取后正文为空或极少（< 200 字符），说明网站是 SPA 动态渲染，通用 Markdown 提取器无法工作
- 批量抓取帮助中心/文档站（如 Guru help.getguru.com、readme.io 托管站、GitBook 等）
- 已知案例：`vcsmemo.com`（Nuxt.js SPA）、`help.getguru.com`（readme.io）

**核心方案**：用 Playwright 无头浏览器直接访问页面 → 等待 SPA 渲染完成 → 隔离正文区域 → `page.pdf()` 生成 PDF。

**关键步骤**：

#### 1. 加载与等待
```javascript
await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
await page.waitForTimeout(5000); // SPA 需要额外等待 JS 渲染
```

#### 2. 滚动触发懒加载图片
```javascript
await page.evaluate(async () => {
  const delay = (ms) => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < document.body.scrollHeight; i += 300) {
    window.scrollBy(0, 300);
    await delay(200);
  }
  window.scrollTo(0, 0);
});
await page.waitForTimeout(3000);
```

#### 3. 正文隔离（⚠️ 最关键的一步）

**问题**：直接 `page.pdf()` 会把整个页面打进 PDF，包括导航栏、侧边栏、相关推荐、页脚等非正文内容。**必须在生成 PDF 前隔离正文区域**。

**正文隔离策略（三步法）**：

**Step A：定位正文容器** — 找到包含文章核心段落的最小公共祖先节点
```javascript
// 用文章中的关键句子定位正文 <p> 标签
const articleParagraphs = [];
document.querySelectorAll("p").forEach(p => {
  if (p.textContent.includes("文章中的某段独特文字")) {
    articleParagraphs.push(p);
  }
});

// 计算所有正文段落的最小公共祖先
let commonAncestor = articleParagraphs[0];
for (let i = 1; i < articleParagraphs.length; i++) {
  // ... 向上遍历 DOM 树找公共祖先
}
```

**Step B：替换 body** — 将整个 `document.body` 的内容替换为正文容器的克隆
```javascript
const articleContent = commonAncestor.cloneNode(true);
document.body.innerHTML = "";
document.body.appendChild(articleContent);
```

**Step C：清理残余** — 从正文容器内部移除混入的非正文元素
```javascript
// 移除正文容器内可能混入的非内容元素
articleContent.querySelectorAll(
  '[class*="related"], [class*="sidebar"], [class*="comment"], ' +
  '[class*="share"], [class*="subscribe"], nav, header, footer'
).forEach(el => el.remove());

// 按文本内容移除（如"相关文章"、"登录"等中文导航项）
articleContent.querySelectorAll("*").forEach(el => {
  const t = el.textContent.trim();
  if (t === "相关文章" || t === "登录" || t.startsWith("Signal, not noise")) {
    const wrapper = el.closest("section, div, aside");
    wrapper ? wrapper.remove() : el.remove();
  }
});
```

#### 4. 样式优化
```javascript
articleContent.style.maxWidth = "750px";
articleContent.style.margin = "0 auto";
articleContent.style.padding = "30px 20px";
articleContent.style.fontSize = "15px";
articleContent.style.lineHeight = "1.8";

articleContent.querySelectorAll("img").forEach(img => {
  img.style.maxWidth = "100%";
  img.style.height = "auto";
});
```

#### 5. 生成 PDF
```javascript
await page.pdf({
  path: outputPath,
  format: "A4",
  printBackground: true,
  margin: { top: "15mm", bottom: "15mm", left: "15mm", right: "15mm" },
});
```

**常见需要移除的非正文元素**：

| 元素类型 | 典型选择器/文本 | 说明 |
|---------|---------------|------|
| 左侧导航 | `nav`, `[class*="sidebar"]`, 包含"首页/快讯/登录"等文本 | 网站主导航 |
| 右侧推荐 | `[class*="related"]`, 包含"相关文章"文本 | 相关文章推荐 |
| 顶部搜索 | `[class*="search"]`, `header` | 搜索栏和网站 header |
| 底部页脚 | `footer`, `[class*="footer"]` | 版权信息等 |
| 作者卡片 | `[class*="author-card"]`, 包含头像+简介的独立区块 | 如果在正文外部 |
| 订阅入口 | `[class*="subscribe"]`, `[class*="newsletter"]` | CTA 按钮 |

**调试技巧**：
- 在 `page.pdf()` 之前先 `page.screenshot({ path: "debug.png", fullPage: true })` 截图确认隔离效果
- 如果首次隔离不干净，根据截图调整选择器，迭代优化

**已验证的 SPA 网站**：

| 网站 | 框架 | 正文定位方式 |
|------|------|-------------|
| `vcsmemo.com` | Nuxt.js | 通过文章段落文本找公共祖先，class `left` 内的 `section` |
| `help.getguru.com` | readme.io | 移除 `.rm-Sidebar` + `nav` + `header` + `footer` |
| `dedao.cn` | React SPA | CDP 模式 + `.iget-articles` 专用选择器 |

### Substack 站点（如 lennysnewsletter.com）

`fetch_article.py` 对 Substack 托管站（`*.substack.com`、`a16z.news`、
`lennysnewsletter.com` 等）默认复用 **CDP Chrome profile**：
1. 每次先连接已配置端口（默认 9222，端口写在 `~/.fetch_article/cdp_port`）的现有
   Google Chrome 上下文；没有 page target 时创建种子 tab，再连接并复用。若 9222 被
   Ardot 等非 Google Chrome 进程占用，启动脚本自动选择 9223–9232 的空闲端口。
2. 不启动 `Google Chrome for Testing`，不另存一套 Playwright `storage_state`。
3. 公开且正文完整的文章无需登录；仅检测到付费墙或正文过短时才引导用户在 CDP Chrome 登录。
4. 转 Markdown 时过滤 `Discover more`、订阅组件、相关推荐、newsletter disclaimer
   及其图片；作者、发布日期优先读取 canonical meta、`time[datetime]` 和 JSON-LD。

```bash
python scripts/fetch_article.py login   # 首次在 CDP Chrome 登录，后续直接复用
```

**付费墙检测信号**：DOM `[data-testid="paywall"]`/`.paywall`；文本 `This post is for paid subscribers`/`Subscribe to read`/`Upgrade to paid`。不同站点结构不同，抓取不全时检查实际付费墙标识并更新检测逻辑。

### X.com / Twitter 帖子（必须 CDP）

X.com 是登录墙典型，`web_fetch` 与普通 Cookie 注入都不行，**必须 CDP**：

```bash
python scripts/fetch_article.py fetch "https://x.com/<user>/status/<id>" --output-dir <目录> --cdp
```

CDP 通过 Chrome DevTools Protocol(9222) 复用真实 Chrome 已登录会话，绕过 X 对自动化浏览器的检测。帖子转 Markdown、媒体下载到 `images/`、链接转 md 链接、转赞数等元信息保留。

### 微博帖子（必须 CDP）

微博强制登录（PC/移动/API 端口均是），`web_fetch` 和普通 Playwright 都会被重定向到 `Sina Visitor System`。**必须 CDP**：

```bash
python scripts/fetch_article.py fetch "https://weibo.com/<uid>/<mid>" --output-dir <目录> --cdp
```

| 坑 | 说明 |
|---|---|
| `web_fetch` 失败 | 被重定向到 `passport.weibo.com/visitor/visitor` |
| Playwright 失败 | 检测 HeadlessChrome UA，`--browser=chrome` 也被拦 |
| 内容整理 | 原始 HTML 含导航/按钮噪音，需清理为结构化 markdown |
| 标题 | 默认「微博正文 - 微博」，转存改为 `<作者>：<主题关键词>`（如 `唐杰THU：最近的一些想法`） |
| 图片 | `sinaimg.cn` CDN，部分需 Referer |

转存时生成标准工作包，最终 Markdown 统一交给 uploader；`file_create_hyperlink` 仅用于
支持的微信链接场景。

### web_fetch 获取的免费文章

通过 `web_fetch` 拿到完整内容的免费文章，**同样保存原文全文**（不总结/不摘要/不改写）：
生成标准 `source.md`、`meta.json` 和可选 `images/`，最终标题文件由编排流程生成。

> ⚠️ `web_fetch` 可能返回**总结版**而非全文。若内容明显被缩写（缺段落/引用/细节），调用时明确要求「返回完整原始全文，不要总结或缩写」。保存的必须是原文全文。

### Python 兼容性

脚本使用 `from __future__ import annotations` 以兼容 Python 3.9（`str | None` 联合类型语法在 3.9 中不可用）。

