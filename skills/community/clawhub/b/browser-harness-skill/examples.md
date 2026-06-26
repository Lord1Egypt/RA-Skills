# browser-harness 使用示例

按场景列举常见任务怎么调。每个例子都假设守护进程已经在跑（`scripts/run.sh setup` 完成过 + `browser-harness --setup` 已经接管 Chrome）。

## 1. 抓取（read-only）

### 1.1 抓 HN 首页前 10 条标题 + 链接

```bash
scripts/run.sh open https://news.ycombinator.com
scripts/run.sh js '
  [...document.querySelectorAll(".titleline a")]
    .slice(0, 10)
    .map(a => ({ title: a.textContent, href: a.href }))
'
```

### 1.2 抓淘宝/京东商品价格（已登录账号）

```bash
# 第一次：把当前页面手动定位到目标商品（用户在 Chrome 里点）
scripts/run.sh page    # 确认当前 URL/title
scripts/run.sh js '
  ({
    title: document.querySelector("h1")?.innerText,
    price: document.querySelector(".price, [data-price]")?.textContent,
    sku:   location.pathname.match(/\d+/)?.[0]
  })
'
```

### 1.3 抓飞书文档全文（需登录）

```bash
# 滚到底确保 lazy-load 全展开
scripts/run.sh exec '
  for (let i = 0; i < 30; i++) {
    const before = await bh.js("document.documentElement.scrollHeight");
    await bh.scroll(400, 400, 1200);
    await bh.wait(0.5);
    const after = await bh.js("document.documentElement.scrollHeight");
    if (before === after) break;
  }
  console.log(await bh.js("document.querySelector(\"[data-page-content]\")?.innerText"));
' > doc.txt
```

## 2. 表单 / 操作（write）

### 2.1 在已登录的 GitHub 给一个 repo 加 star

```bash
scripts/run.sh open https://github.com/browser-use/browser-harness
# 用 aria-label 而不是像素坐标——稳定
scripts/run.sh js 'document.querySelector("[aria-label*=\"Star this repository\"]")?.click()'
```

### 2.2 在公司 CRM 创建一个客户

```bash
scripts/run.sh exec '
  await bh.gotoUrl("https://crm.acme.com/customers/new");
  await bh.waitForLoad();
  await bh.js(`document.querySelector("#name").value = ${JSON.stringify("Acme Corp")}; document.querySelector("#name").dispatchEvent(new Event("input", {bubbles:true}));`);
  await bh.js(`document.querySelector("#email").value = ${JSON.stringify("ops@acme.example")}; document.querySelector("#email").dispatchEvent(new Event("input", {bubbles:true}));`);
  await bh.js("document.querySelector(\"button[type=submit]\")?.click()");
  await bh.waitForLoad();
  console.log(JSON.stringify(await bh.pageInfo(), null, 2));
'
```

> 注意：用 `dispatchEvent(new Event("input"))` 让 React/Vue 框架监听到值变更——直接赋值 `.value` 不触发 onChange。

### 2.3 上传文件到 input[type=file]

```bash
scripts/run.sh upload 'input[type=file]' /Users/me/Pictures/photo.jpg
```

## 3. 多标签 / iframe

### 3.1 在另一个标签页里读数据

```bash
scripts/run.sh tabs    # 列所有真实标签
scripts/run.sh switch '飞书文档'    # 关键词匹配 url 或 title
scripts/run.sh js 'document.title'  # 确认切对了
```

### 3.2 在 iframe 内执行 JS

```bash
scripts/run.sh exec '
  const iframeId = await bh.iframeTarget("docs.google.com/document");
  if (!iframeId) throw new Error("没找到 google docs iframe");
  const text = await bh.js("document.body.innerText", { targetId: iframeId });
  console.log(text.slice(0, 500));
'
```

## 4. 跨任务 / 沉淀知识

### 4.1 第一次摸一个新站点 → 写 domain-skill

```bash
# 1. 摸索
scripts/run.sh open https://internal-tool.acme.com/reports
scripts/run.sh js 'document.querySelectorAll("[data-testid]").length'    # 找稳定的 testid
scripts/run.sh js '[...document.querySelectorAll("[data-testid]")].map(e => e.dataset.testid).slice(0, 20)'

# 2. 把找到的稳定模式写成长期记忆
mkdir -p agent-workspace/domain-skills/internal-tool
cat > agent-workspace/domain-skills/internal-tool/reports.md <<'EOF'
# internal-tool reports

## URL
- 报表列表：https://internal-tool.acme.com/reports
- 单条详情：/reports/<id>，id 是 ULID

## 稳定选择器
- 报表卡片：`[data-testid="report-card"]`
- 卡片标题：`[data-testid="report-card-title"]`
- 卡片状态：`[data-testid="report-card-status"]`（值：`draft|running|done|failed`）
- "运行"按钮：`[data-testid="report-run-btn"]`（disabled 状态在 status=running 时不可点）

## 等待
- waitForLoad 之后还要再 `wait(0.5)`，状态 chip 是 SWR 在 client-side 渲染的

## 私有 API
- POST /api/reports/<id>/run，body 空，需要 X-CSRF-Token（从 <meta name="csrf-token"> 拿）
EOF
```

### 4.2 复用沉淀的知识

```bash
# 下次任务开头先读
cat agent-workspace/domain-skills/internal-tool/*.md

# 现在知道选择器就直接用，不用重新摸
scripts/run.sh exec '
  await bh.gotoUrl("https://internal-tool.acme.com/reports");
  await bh.waitForLoad();
  await bh.wait(0.5);
  const cards = await bh.js(`[...document.querySelectorAll("[data-testid=\"report-card\"]")].map(c => ({
    title: c.querySelector("[data-testid=\"report-card-title\"]")?.textContent,
    status: c.querySelector("[data-testid=\"report-card-status\"]")?.textContent
  }))`);
  console.log(JSON.stringify(cards, null, 2));
'
```

## 5. helpers（可重用 + 类型安全）

把 selector + 业务步骤封到 `agent-workspace/agent_helpers.ts`：

```ts
import type { BH } from "browser-harness-ts";

export async function runReport(bh: BH, reportId: string): Promise<{ status: string }> {
  await bh.gotoUrl(`https://internal-tool.acme.com/reports/${reportId}`);
  await bh.waitForLoad();
  await bh.wait(0.5);
  await bh.js(`document.querySelector('[data-testid="report-run-btn"]').click()`);
  // 轮询状态
  for (let i = 0; i < 60; i++) {
    const status = await bh.js<string>(`document.querySelector('[data-testid="report-card-status"]')?.textContent`);
    if (status && status !== "running") return { status };
    await bh.wait(1);
  }
  throw new Error("report timed out after 60s");
}
```

调用：

```bash
scripts/run.sh helpers     # 确认 runReport 已注册
scripts/run.sh exec '
  const r = await h.runReport(bh, "01HXYZ...");
  console.log("done:", r.status);
'
```

## 6. 截图 / 视觉

### 6.1 视口截图

```bash
scripts/run.sh shot ./current.png
```

### 6.2 整页截图（含视口外）

```bash
scripts/run.sh shot --full ./fullpage.png
```

### 6.3 元素截图

```bash
scripts/run.sh exec '
  const rect = await bh.js(() => {
    const el = document.querySelector(".chart");
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  });
  if (!rect) throw new Error("没找到 .chart");
  // 滚到元素再截全页，然后裁剪——bh 不内置 clip，借 sharp 之类
  el.scrollIntoView();
  await bh.captureScreenshot({ path: "./chart-full.png", full: true });
  console.log(JSON.stringify(rect));    // 拿到 rect 后用 sharp 裁
'
```

## 7. 处理弹窗 / dialog

```bash
# 当前页有 alert/confirm/prompt 时 pageInfo 会返回 {dialog: ...}
scripts/run.sh page
# 输出形如：{"dialog":{"type":"confirm","message":"确认离开？"}}

# 处理 dialog（接受 / 拒绝）
scripts/run.sh exec '
  const dlg = await bh.pendingDialog();
  if (dlg) await bh.cdp("Page.handleJavaScriptDialog", { accept: true });
'
```

## 8. 跨语言 (Python ↔ TS) 协同

### 8.1 Python 端探索（LLM 友好）

```bash
browser-harness -c '
new_tab("https://twitter.com")
print(page_info())
# 用 Python REPL 风格快速摸接口
import json
print(js("[...document.querySelectorAll(\"article\")].length"))
'
```

### 8.2 TS 端跑生产管线（同一个 Chrome、同一份登录态）

```bash
scripts/run.sh exec '
  const tweets = await bh.js(`[...document.querySelectorAll("article")].slice(0, 20).map(a => ({
    author: a.querySelector("[data-testid=\"User-Name\"] span")?.textContent,
    text:   a.querySelector("[data-testid=\"tweetText\"]")?.textContent
  }))`);
  console.log(JSON.stringify(tweets, null, 2));
' > tweets.json
```

## 9. 多 namespace 并行

```bash
# 终端 A
BU_NAME=research scripts/run.sh open https://arxiv.org
BU_NAME=research scripts/run.sh js 'document.title'

# 终端 B（独立守护、独立 Chrome）
BU_NAME=writing scripts/run.sh open https://draft.local
BU_NAME=writing scripts/run.sh exec '...'
```

注意：每个 BU_NAME 第一次用都需要单独的 `BU_NAME=<n> browser-harness --setup` 接管一个 Chrome 实例。

## 10. 反例（不要这么干）

### ❌ 用像素坐标点东西

```bash
scripts/run.sh click 920 220     # 浏览器宽度变了 / 缩放变了 / DPR 变了 → 失败
```

✅ 用稳定选择器：

```bash
scripts/run.sh js 'document.querySelector("[aria-label*=\"Star\"]").click()'
```

### ❌ 把外部变量塞进 `bh.js`

```ts
const sel = "#name";
await bh.js(() => document.querySelector(sel));   // ReferenceError
```

✅ 通过字符串模板 + JSON.stringify：

```ts
const sel = "#name";
await bh.js<string>(`document.querySelector(${JSON.stringify(sel)}).value`);
```

### ❌ 把 cookie / token 写进 domain-skills

```markdown
<!-- agent-workspace/domain-skills/internal-tool/auth.md -->
session_token: <REDACTED-JWT-EXAMPLE>    ← 仓库会进 git，泄露！
```

✅ 只写"在哪取 token"和"token 寿命多长"：

```markdown
- token 在 `<meta name="csrf-token">` 里
- session 是 `__Host-internal_sid` cookie，30 分钟过期
- 过期后 GET /login 会 302 到 SSO，跑 `scripts/run.sh setup` 重新 attach 即可恢复
```

### ❌ 守护没起就硬调

```bash
scripts/run.sh js 'document.title'
# Error: browser-harness daemon "default" not running
```

✅ 先体检：

```bash
scripts/run.sh doctor
# 输出告诉你是没装 / 没接 / 还是接错了
```
