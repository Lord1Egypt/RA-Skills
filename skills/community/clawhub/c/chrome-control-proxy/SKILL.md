---
name: chrome-control-proxy
description: 宿主机 chrome-control-proxy 服务调用指南。通过 HTTP 控制 Chrome 生命周期与 Playwright（page-dom 快照、run 脚本）。适用于 OpenClaw 在容器内访问 host.docker.internal:3333 或宿主机直接访问 127.0.0.1:3333。必读以避免 Playwright 与请求顺序踩坑。
version: 1.0.2
metadata:
  openclaw:
    emoji: 🌐
    homepage: https://github.com/zhengxiangqi/chrome-control-proxy
    os:
      - macos
      - linux
      - windows
    requires:
      bins:
        - node
---

# chrome-control-proxy 服务（OpenClaw）

## 前置条件

1. 宿主机已安装 **Node ≥ 18**，并全局安装服务包：`npm install -g chrome-control-proxy`。
2. 服务已启动：宿主机执行 `ccp start`，默认 **`http://127.0.0.1:3333`**。
3. 自动化前通常需 **Chrome 已带远程调试**：`POST /browser/start`（或你手动用 `--remote-debugging-port=9222` 启动）。
4. 容器内将主机换为 **`host.docker.internal:3333`**（Linux Docker 可能需配置 `extra_hosts`）。

---

## 推荐调用顺序（自动化任务）

1. `GET /health` → 确认 HTTP 服务可用；`browser.running` 为 false 时先 `POST /browser/start`。
2. `GET /playwright/status` → 确认 CDP 可连（失败则检查 Chrome 是否在 `CHROME_PORT` 监听）。
3. 需要页面结构时：`POST /playwright/page-dom`，优先传 `selector` 与 `playwrightSnapshotMode: "compact"`。
4. 只执行动作：`POST /playwright/run`；动作前后都要拿快照时优先用 `POST /playwright/pipeline`。

`page-dom`、`pipeline` 与 `run` 在服务端 **串行队列**，不要假设并行请求能同时操作同一标签页。

---

## POST /playwright/page-dom

用于把页面信息交给模型生成脚本，**优先用 Playwright 专用快照减 token**。

**建议 body：**

- `url`：要打开的地址（可选；不传则对当前 `target` 对应标签页快照）。
- `waitUntil`：如 `domcontentloaded`、`networkidle`、`load`。**页面分析优先 `domcontentloaded`**。
- `timeout`：导航超时毫秒数。
- `target`：`first` | `last` | `new`。
- **`includeHtml: false`**：不需要整页 HTML 时务必关闭。
- **`includePlaywrightSnapshot: true`**：返回 `playwright.targets[]`，每项含 `tag`、`name`、`placeholder`、`suggestedLocator` 等，便于写 `page.locator` / `getByRole`。
- **`playwrightSnapshotMode: "compact"`**：只保留精简的 `targets[]` 字段，更适合高频分析链路。
- `selector`：只截取某子树（如主内容区）。
- `includeInnerText` / `includeAccessibility`：按需。

响应中 `playwright` 过大可能被截断，注意 `playwrightTruncated`。

---

## POST /playwright/pipeline

用于一次请求完成以下任意组合：

- 外层导航到目标页
- `beforePageDom`：执行前快照
- `script`：执行脚本
- `afterPageDom`：执行后快照

适合“点击后还要继续分析页面状态”的链路，避免额外再调一次 `page-dom`。

---

## POST /playwright/run

Body 中 **`script`** 为字符串，内容是 **async 函数体**（不是完整 `async function(){ }` 包裹），可：

- `await page.goto(...)`
- `await page.locator(...).click()`
- `return { ok: true, ... }` 把结果回传给 HTTP JSON。

注入变量：**`page`、`context`、`browser`**（与当前 CDP 浏览器一致）。

### 踩坑 1：外层 `url` 与脚本内导航

若请求 body 里带了 **`url`**，服务会 **先对该 URL 执行 `goto`，再执行脚本**。

- **登出再登入、先清 Cookie 再打开登录页**：请 **不要** 在外层传 `url`，只在脚本里写 `await page.context().clearCookies()`、`localStorage.clear()`、`sessionStorage.clear()` 后再 `goto` 业务站。否则会出现「先跳进已登录态页面，再清 Cookie」的顺序错误。

### 踩坑 2：会话与多步 OAuth

统一登录常跳转到独立域名（如 OAuth）。多步流程（账号 → 租户）可用 **多次 `run`**，且 **`target` 保持一致**（如 `first`），除非有意新开标签页用 `new`。

### 踩坑 3：便捷登录 / 确认框

若出现「便捷登录」等 **Element Plus / Dialog**，优先点 **主按钮**：如 `.el-message-box__btns .el-button--primary`、`.el-dialog__footer .el-button--primary`，或 `getByRole('button', { name: /确认|确定|继续/ })`。  
仅在 **`input[name="account"]` 等元素可见** 时再填账号密码验证码，避免「不必等输密码」的场景下仍机械填表。

### 踩坑 4：UI 退出登录

不要直接点隐藏菜单里的「退出登录」节点（可能被首页层遮挡）。优先 **`clearCookies` + 存储清理** 或先展开用户下拉再点退出。

### 踩坑 5：超时

大页面或慢网络：增大 `timeout`（导航）与 **`scriptTimeout`**（脚本总执行时间，受 `PLAYWRIGHT_RUN_DEFAULT_MS` 等影响）。

### 踩坑 6：安全

脚本在沙箱中执行，**不要对公网暴露** 本服务；勿向不可信方开放 `/playwright/run`。

---

## 与浏览器控制接口的关系

| 能力 | 路径 |
|------|------|
| 启停 Chrome | `POST /browser/start`、`stop`、`restart` |
| 健康检查 | `GET /health`、`GET /browser/status` |
| Playwright | `GET /playwright/status`、`POST /playwright/page-dom`、`POST /playwright/pipeline`、`POST /playwright/run` |

停止 Chrome 会断开 Playwright 的 CDP 连接；再次自动化前需重新 `browser/start` 并确保 Playwright 能连上。

---

## CLI 备忘（宿主机）

全局安装包后可用 **`ccp start|stop|restart|status`** 管理 HTTP 进程，详见项目 **`README.md`**。
