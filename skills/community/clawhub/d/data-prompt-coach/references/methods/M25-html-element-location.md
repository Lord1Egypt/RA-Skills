# M25 — HTML 元素定位法

> 来源：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》教程蒸馏
> 挂载版本：v3.4.0（2026-07-26）
> 触发咒语："元素定位""HTML 复制""元素块""DevTools"

## R — 原文引用

> "抓取技巧：当需要抓取网页上特定数据，但 AI 没有识别到，可以这样定向获取 HTML 内容，发送给 AI：右键点击网页空白的的地方，选「检查」点击右上角「选择元素」的箭头，然后点击想要抓取的元素，例如下载按钮。右侧会出现元素相关的 HTML 代码，右键点击代码块、选择「Edit as HTML」，然后复制 HTML，发给 AI 就 OK。选择元素的时候，范围可以稍微大一点，要包含整个元素块。"

## I — 方法论重写

**核心命题**：AI 抓取网页数据时，有时识别不到特定字段（如下载按钮、嵌套表格、动态加载的内容）。此时用户应主动用 DevTools 定位 HTML 元素，复制给 AI，让 AI 基于真实 HTML 结构写解析规则。

**5 步定位流程**：

### Step 1：打开 DevTools
- **方式 A**：右键网页空白处 → 检查
- **方式 B**：F12 快捷键
- **方式 C**：Ctrl+Shift+I

### Step 2：选择元素
- **点击箭头**：DevTools 左上角的"选择元素"箭头
- **点击目标**：在网页上点击要抓取的元素（如下载按钮、标题、价格）
- **范围放大**：选择时范围稍微大一点，包含整个元素块（不要只选文字）

### Step 3：定位 HTML 代码
- **Elements 面板**：右侧自动跳转到对应 HTML 代码
- **高亮确认**：网页上对应元素会高亮，确认选对了
- **展开父级**：如果选的太窄，向上展开到包含完整数据的父元素

### Step 4：复制 HTML
- **右键代码块**：在 Elements 面板右键点击对应 HTML 代码块
- **选择 Edit as HTML**：进入编辑模式
- **Ctrl+A 全选**：选中整个 HTML 块
- **Ctrl+C 复制**：复制到剪贴板

### Step 5：发送给 AI
- **粘贴给 AI**：把 HTML 粘贴到对话中
- **说明需求**："这是网页上 X 元素的 HTML，请基于这个结构写解析规则，提取 Y 字段"
- **多次提供**：如果一个元素不够，可以提供多个（如标题+价格+评分各一份）

## A1 — 书中案例

**Airtable 社区案例**：
- AI 未识别到帖子分类字段
- 用户用 DevTools 定位帖子分类的 HTML 元素
- 复制 HTML 给 AI
- AI 基于 HTML 结构写了 CSS 选择器：`.topic-category .badge`
- 成功提取帖子分类

**通用案例**：
- AI 未识别到下载按钮
- 用户用 DevTools 定位下载按钮的 HTML
- 复制给 AI
- AI 写出 XPath：`//button[@class="download-btn"]`

## A2 — 未来触发

**何时用 M25**：
- 用户说"AI 没识别到我要的数据"
- 用户说"AI 抓取的字段不对"
- 用户说"怎么把 HTML 发给 AI"
- 用户说"元素定位""HTML 复制""DevTools"
- 场景 1 中 AI 第一次抓取失败时主动追加

**与 M22 的关系**：
- M22 优先：先看是否是 SPA（如果是，找 API 而非解析 HTML）
- M25 兜底：如果不是 SPA，或 API 难以分析，用 HTML 元素定位

## E — 可执行步骤

**AI 主动引导用户的话术**：

```
我没能识别到你要的 [字段名] 字段。请帮我做以下操作：

1. 在网页上按 F12 打开开发者工具
2. 点击左上角的"选择元素"箭头（或 Ctrl+Shift+C）
3. 点击包含 [字段名] 的元素
4. 右侧 Elements 面板会跳到对应 HTML 代码
5. 右键代码块 → Edit as HTML → Ctrl+A 全选 → Ctrl+C 复制
6. 把 HTML 粘贴给我

注意：选择时范围稍微大一点，包含整个元素块（如整个卡片，不只是文字）。

我收到 HTML 后会基于真实结构写解析规则。
```

**AI 收到 HTML 后的执行步骤**：

```
1. 分析 HTML 结构，识别目标字段的位置
2. 选择解析方式：
   - CSS 选择器（推荐，简洁）
   - XPath（复杂结构时用）
   - BeautifulSoup find_all（Python）
3. 写解析代码 + 测试用例
4. 输出完整代码 + 字段提取规则说明
```

## B — 边界与盲点

### 适用边界
- ✅ 静态 HTML 网站（直接解析）
- ✅ SPA 网站的 HTML 预览（部分元素可见时）
- ✅ AI 第一次抓取失败时的兜底方案
- ✅ 用户想快速验证字段提取规则
- ❌ 完全动态加载的内容（HTML 中没有，需用 M22 找 API）
- ❌ 需要登录才能看到的内容（需先处理认证）

### HTML 脱敏门控（v3.4.4 强制，回应 ClawHub Instruction Scope concern - raw HTML sharing without redaction gates）

⚠️ **复制 HTML 给 AI 前，必须先扫描并脱敏以下敏感内容**：

| 敏感内容 | 是否脱敏 | 脱敏方式 |
|---------|---------|---------|
| 内嵌的 `Authorization` / `X-API-Key` | ✅ 必脱敏 | 替换为 `<REDACTED_AUTH>` |
| 内嵌的用户 Token / Session ID | ✅ 必脱敏 | 替换为 `<REDACTED_TOKEN>` |
| 内嵌的 CSRF Token | ✅ 必脱敏 | 替换为 `<REDACTED_CSRF>` |
| 用户邮箱 / 手机号（如 `<a href="mailto:user@xxx">`） | ✅ 必脱敏 | 替换为 `<REDACTED_EMAIL>` |
| 用户 ID / 用户名（如果是私有数据） | ⚠️ 视场景 | 公开页面保留，私有页面脱敏 |
| 表单中的隐藏字段值 | ✅ 必脱敏 | 替换为 `<REDACTED_HIDDEN_VALUE>` |
| 内嵌的 Cookie 值 | ✅ 必脱敏 | 替换为 `<REDACTED_COOKIE>` |

**脱敏流程**：
1. 用户在 DevTools 复制 HTML 后，先在本地文本编辑器粘贴
2. 用正则搜索 `value="..."` / `data-token="..."` / `authorization` / `csrf` 等关键词
3. 把所有匹配的敏感值替换为 `<REDACTED_*>` 占位符
4. 把脱敏后的 HTML 发给 AI

**脱敏示例**：
```html
<!-- ❌ 原始 HTML（含敏感值，禁止发给 AI） -->
<form action="/api/submit" method="POST">
  <input type="hidden" name="csrf_token" value="abc123xyz_secret_csrf_value">
  <input type="hidden" name="user_id" value="98765">
  <input type="hidden" name="session_token" value="sess_xxxxxxxxxxxxx">
  <button class="download-btn">Download</button>
</form>

<!-- ✅ 脱敏后 HTML（可发给 AI） -->
<form action="/api/submit" method="POST">
  <input type="hidden" name="csrf_token" value="<REDACTED_CSRF>">
  <input type="hidden" name="user_id" value="<REDACTED_USER_ID>">
  <input type="hidden" name="session_token" value="<REDACTED_SESSION>">
  <button class="download-btn">Download</button>
</form>
```

**禁止行为**：
- ❌ 直接把含真实 Token / Session / CSRF 的 HTML 粘贴给 AI
- ❌ 在 GitHub 仓库 / 飞书文档 / IMA 笔记中保存含敏感值的 HTML 快照
- ❌ 把脱敏前的 HTML 存入缓存文件（如 `assets/.backup/`）

### 盲点与陷阱
1. **HTML 不完整**：用户复制的 HTML 可能是片段，缺少上下文 → 让用户复制父级元素
2. **动态 class 名**：Vue/React 生成的 class 可能是 `css-abc123` 这种哈希名，每次构建变化 → 用稳定的属性（如 `data-testid`）
3. **iframe 内容**：iframe 中的内容不能直接选择 → 需要先切换到 iframe 上下文
4. **Shadow DOM**：Web Components 用 Shadow DOM，DevTools 难以选择 → 需用特殊配置
5. **复制时机**：动态加载的内容需要在加载完成后复制，否则 HTML 是空的

### 与其他方法论的关系
- **兜底**：M22 失败时用 M25（先试 API，失败再试 HTML 解析）
- **配套**：M1 黄金五要素（HTML 也是"数据源"的一种）
- **后续**：M7 验真闭环（验证 HTML 解析结果）

## 引用关系

- **前置**：M22（先试 API，失败再用 HTML 定位）
- **配套**：M1（数据源识别）
- **后续**：M7 验真闭环

## 版本

- v3.4.0（2026-07-26）：首次创建，源自 TRAE 社区爬虫教程蒸馏
