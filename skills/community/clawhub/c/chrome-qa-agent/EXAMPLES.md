# UI 测试示例

每个示例都展示了完整的断言协议: 前后对比, 结构化标记, 以及对抗式测试。

所有示例都通过 chrome-devtools MCP (`mcp__chrome-devtools__*` 工具) 驱动同一个本地 Chrome。元素来自 `take_snapshot`, 它会给每个元素分配一个 `uid` (例如 `uid=8 button "Start Free Trial"`)。**uid 不是稳定的** —— 每次快照以及任何 DOM 变化后都会重新编号, 所以使用 uid 前要重新快照。

## Example 1: diff 驱动的组件测试 (正常路径 + 对抗式)

**用户请求**: "我改了 CTA 按钮的文案。测一下。"

```bash
# Analyze diff
git diff --name-only HEAD~1
# Output: src/components/HeroSection.tsx
git diff HEAD~1 -- src/components/HeroSection.tsx
# Shows: "Get Started" changed to "Start Free Trial"
```

```
# Setup — open in an isolated context for a clean run
mcp__chrome-devtools__new_page { url: "http://localhost:3000/", isolatedContext: "ui-test" }

# BEFORE snapshot
mcp__chrome-devtools__take_snapshot
# Tree: uid=8 button "Start Free Trial"
# Evidence: button exists with new text

# Happy path: button is clickable
mcp__chrome-devtools__click { uid: "8" }
mcp__chrome-devtools__take_snapshot
# AFTER: check no crash, page still functional

# STEP_PASS|cta-text|button "Start Free Trial" found at uid=8
# STEP_PASS|cta-click|button click succeeded, page intact after click

# Adversarial: rapid click (re-navigate, re-snapshot — uids are renumbered after navigation)
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/" }
mcp__chrome-devtools__take_snapshot
# uid=8 button "Start Free Trial" (re-read from the fresh snapshot)
mcp__chrome-devtools__click { uid: "8" }
mcp__chrome-devtools__click { uid: "8" }
mcp__chrome-devtools__click { uid: "8" }
mcp__chrome-devtools__take_snapshot
# Check: no duplicate dialogs, no console errors, page still stable

# STEP_PASS|cta-rapid-click|3 rapid clicks, page remains stable, no duplicate side effects

mcp__chrome-devtools__close_page
```

**结果**:
```
## UI Test Results
### STEP_PASS|cta-text|button "Start Free Trial" found at uid=8
### STEP_PASS|cta-click|clicked uid=8, page intact
### STEP_PASS|cta-rapid-click|3 rapid clicks, no duplicate effects
**Summary: 3/3 passed**
```

## Example 2: 表单校验 —— 正常路径, 错误, 以及对抗式

**用户请求**: "我给注册表单加了邮箱校验。彻底测一遍。"

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/signup", isolatedContext: "ui-test" }

# ---- Test 1: Invalid email → error ----
# BEFORE
mcp__chrome-devtools__take_snapshot
# uid=3 textbox "Email", uid=7 button "Sign Up"

# ACT
mcp__chrome-devtools__fill { uid: "3", value: "not-an-email" }
mcp__chrome-devtools__click { uid: "7" }

# AFTER
mcp__chrome-devtools__take_snapshot
# uid=9 alert "Please enter a valid email"

# STEP_PASS|invalid-email|alert "Please enter a valid email" appeared at uid=9

# ---- Test 2: Valid email → success ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/signup" }

# BEFORE (re-snapshot — uids were renumbered by the navigation)
mcp__chrome-devtools__take_snapshot
# uid=3 textbox "Email", uid=7 button "Sign Up"

# ACT
mcp__chrome-devtools__fill { uid: "3", value: "user@example.com" }
mcp__chrome-devtools__click { uid: "7" }
mcp__chrome-devtools__wait_for { text: "Welcome!" }

# AFTER
mcp__chrome-devtools__take_snapshot
# heading "Welcome! Check your email." appeared, form gone

# STEP_PASS|valid-email|heading "Welcome!" appeared, form removed from tree

# ---- Test 3: Empty submission ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/signup" }

# BEFORE
mcp__chrome-devtools__take_snapshot
# uid=7 button "Sign Up"

# ACT: submit with nothing filled
mcp__chrome-devtools__click { uid: "7" }

# AFTER
mcp__chrome-devtools__take_snapshot
# Check: error message? Or silent failure? Or crash?

# STEP_PASS|empty-submit|alert "Please enter a valid email" appeared — form handles empty input

# ---- Test 4: XSS in email field ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/signup" }
mcp__chrome-devtools__take_snapshot
# uid=3 textbox "Email", uid=7 button "Sign Up"

mcp__chrome-devtools__fill { uid: "3", value: "<script>alert('xss')</script>" }
mcp__chrome-devtools__click { uid: "7" }
mcp__chrome-devtools__take_snapshot
# Note: the XSS payload WILL appear in the snapshot as StaticText inside the input
# field — that's just the input value, not rendered HTML. The real checks are:
# 1. Is there a validation error? (email format rejected)
# 2. Is the payload rendered as HTML outside the input? (check for script execution)
mcp__chrome-devtools__evaluate_script { function: "() => document.querySelector('[role=alert]')?.textContent || 'no alert'" }
# Result: "Please enter a valid email"
mcp__chrome-devtools__evaluate_script { function: "() => document.querySelector('input[name=email]')?.value" }
# Result: "<script>alert('xss')</script>" — payload stays as text in the input, not rendered as HTML

# STEP_PASS|xss-email|XSS payload rejected by validation, no inline script injection detected

# ---- Test 5: Very long email ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/signup" }
mcp__chrome-devtools__take_snapshot
# uid=3 textbox "Email", uid=7 button "Sign Up"

mcp__chrome-devtools__fill { uid: "3", value: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@test.com" }
mcp__chrome-devtools__take_snapshot
# Check: does the input overflow its container? Is layout broken?
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/long-email.png" }
# Visual check: input stays within bounds

mcp__chrome-devtools__click { uid: "7" }
mcp__chrome-devtools__take_snapshot
# Check: does validation handle long but valid emails?

# STEP_PASS|long-email|60-char email accepted, layout intact, no overflow

# ---- Test 6: Keyboard-only flow ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/signup" }

mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script { function: "() => document.activeElement?.name || document.activeElement?.tagName" }
# Should focus email input
mcp__chrome-devtools__type_text { text: "keyboard@test.com" }
mcp__chrome-devtools__press_key { key: "Tab" }
# Should move to submit button
mcp__chrome-devtools__evaluate_script { function: "() => document.activeElement?.tagName" }
# Should be BUTTON
mcp__chrome-devtools__press_key { key: "Enter" }

mcp__chrome-devtools__take_snapshot
# Check: form submitted successfully via keyboard alone

# STEP_PASS|keyboard-flow|form submitted via Tab+type+Tab+Enter, success message appeared

mcp__chrome-devtools__close_page
```

**结果**:
```
## UI Test Results
### STEP_PASS|invalid-email|alert "Please enter a valid email" at uid=9
### STEP_PASS|valid-email|heading "Welcome!" appeared, form removed
### STEP_PASS|empty-submit|empty form shows validation error
### STEP_PASS|xss-email|XSS payload rejected, not rendered as HTML
### STEP_PASS|long-email|60-char email accepted, layout intact
### STEP_PASS|keyboard-flow|full form flow works via keyboard only
**Summary: 6/6 passed**
```

## Example 3: 模态框生命周期 —— 完整状态机

**用户请求**: "我给删除操作加了一个确认模态框。测一下。"

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/dashboard", isolatedContext: "ui-test" }

# ---- Test 1: Modal opens ----
# BEFORE
mcp__chrome-devtools__take_snapshot
# uid=15 button "Delete Account", no dialog in tree

# ACT
mcp__chrome-devtools__click { uid: "15" }

# AFTER
mcp__chrome-devtools__wait_for { text: "Confirm Action" }
mcp__chrome-devtools__take_snapshot
# uid=20 dialog "Confirm Action", uid=22 button "Cancel", uid=23 button "Confirm"

# STEP_PASS|modal-open|dialog "Confirm Action" appeared at uid=20 with Cancel and Confirm buttons

# ---- Test 2: Cancel closes modal, no side effects ----
# BEFORE: dialog present
mcp__chrome-devtools__take_snapshot

# ACT
mcp__chrome-devtools__click { uid: "22" }

# AFTER
mcp__chrome-devtools__take_snapshot
# No dialog in tree. button "Delete Account" still present.

# STEP_PASS|modal-cancel|dialog removed from tree, delete button still present, no side effects

# ---- Test 3: Escape closes modal ----
# Re-snapshot to get the current Delete button uid (it shifted after the dialog closed)
mcp__chrome-devtools__take_snapshot
# uid=15 button "Delete Account"
mcp__chrome-devtools__click { uid: "15" }
mcp__chrome-devtools__wait_for { text: "Confirm Action" }
mcp__chrome-devtools__take_snapshot
# dialog present

mcp__chrome-devtools__press_key { key: "Escape" }
mcp__chrome-devtools__take_snapshot
# Check: dialog gone?

# STEP_PASS|modal-escape|Escape key closed dialog

# ---- Test 4: Confirm executes action ----
mcp__chrome-devtools__take_snapshot
# uid=15 button "Delete Account"
mcp__chrome-devtools__click { uid: "15" }
mcp__chrome-devtools__wait_for { text: "Confirm Action" }
mcp__chrome-devtools__take_snapshot
# uid=23 button "Confirm"

mcp__chrome-devtools__click { uid: "23" }
mcp__chrome-devtools__take_snapshot
# Check: dialog gone AND the destructive action occurred

# STEP_PASS|modal-confirm|dialog closed and action executed after Confirm click

# ---- Test 5: Focus trap (adversarial) ----
mcp__chrome-devtools__take_snapshot
# uid=15 button "Delete Account"
mcp__chrome-devtools__click { uid: "15" }
mcp__chrome-devtools__wait_for { text: "Confirm Action" }

# Tab through dialog — focus should stay inside
mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script { function: "() => document.activeElement?.textContent?.trim().slice(0,20)" }
mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script { function: "() => document.activeElement?.textContent?.trim().slice(0,20)" }
mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script { function: "() => document.activeElement?.textContent?.trim().slice(0,20)" }
# Check: does focus cycle within dialog, or does it escape to page behind?

# STEP_PASS|focus-trap|focus cycles within dialog (Cancel → Confirm → Cancel)
# or on failure:
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/focus-trap.png" }
# STEP_FAIL|focus-trap|expected focus trapped in dialog → focus escaped to nav link behind modal|.context/ui-test-screenshots/focus-trap.png

mcp__chrome-devtools__close_page
```

## Example 4: 带确定性断言的无障碍审计

**用户请求**: "对设置页跑一遍无障碍测试。"

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/settings", isolatedContext: "ui-test" }

# ---- Test 1: axe-core audit ----
# Load axe-core, then run it. evaluate_script awaits the returned promise, so an
# async function can both inject the script and run the audit in one call.
mcp__chrome-devtools__evaluate_script { function: "async () => { await new Promise((res, rej) => { const s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); const r = await axe.run(); return { violations: r.violations.map(v => ({ id: v.id, impact: v.impact, description: v.description, nodes: v.nodes.length })), passes: r.passes.length }; }" }
# Result: {"violations":[],"passes":33}

# Assert: violations.length === 0
# STEP_PASS|axe-audit|0 violations, 33 passes

# If violations existed:
# STEP_FAIL|axe-audit|expected 0 violations → found 2: color-contrast (serious, 3 nodes), label (critical, 1 node)

# ---- Test 2: Form labels ----
mcp__chrome-devtools__evaluate_script { function: "() => Array.from(document.querySelectorAll('input,select,textarea')).map(i => ({ name: i.name, type: i.type, hasLabel: !!i.labels?.length, ariaLabel: i.getAttribute('aria-label') }))" }
# Check: every input has hasLabel:true or ariaLabel

# STEP_PASS|form-labels|all 3 inputs have associated labels

# ---- Test 3: Keyboard navigation ----
mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script { function: "() => ({ tag: document.activeElement?.tagName, text: document.activeElement?.textContent?.trim().slice(0,30) })" }
# Repeat for each interactive element
# Track: element order, whether focus ring is visible

# STEP_PASS|keyboard-nav|8 elements reachable via Tab, logical order, all focusable

# ---- Test 4: Broken images ----
mcp__chrome-devtools__evaluate_script { function: "() => Array.from(document.querySelectorAll('img')).filter(i => !i.complete || i.naturalWidth === 0).map(i => ({ src: i.src, alt: i.alt }))" }
# Result: []

# STEP_PASS|images|0 broken images

mcp__chrome-devtools__close_page
```

## Example 5: 带前后对比的响应式测试

**用户请求**: "我的应用在手机上能用吗?"

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/", isolatedContext: "ui-test" }

# ---- Desktop baseline ----
mcp__chrome-devtools__resize_page { width: 1440, height: 900 }
mcp__chrome-devtools__take_snapshot
# Record desktop state: nav layout, content width, element positions
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/desktop.png", fullPage: true }

# ---- Mobile ----
mcp__chrome-devtools__resize_page { width: 375, height: 812 }
mcp__chrome-devtools__take_snapshot
# Compare against desktop:
# - Did nav collapse to hamburger? Or is it overflowing?
# - Is content full-width? Or is there horizontal scroll?
# - Are buttons large enough for touch (44px+)?
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/mobile.png", fullPage: true }

# Check for horizontal overflow (deterministic)
mcp__chrome-devtools__evaluate_script { function: "() => document.documentElement.scrollWidth > document.documentElement.clientWidth" }
# Result: false = PASS, true = FAIL (content overflows viewport)

# STEP_PASS|mobile-overflow|no horizontal overflow at 375px (scrollWidth <= clientWidth)

# Check touch target sizes
mcp__chrome-devtools__evaluate_script { function: "() => Array.from(document.querySelectorAll('button,a,[role=button]')).map(el => { const r = el.getBoundingClientRect(); return { text: el.textContent?.trim().slice(0,20), width: Math.round(r.width), height: Math.round(r.height) }; }).filter(e => e.width < 44 || e.height < 44)" }
# Result: [] = all targets >= 44px, otherwise list of undersized elements

# STEP_PASS|touch-targets|all interactive elements >= 44px

# ---- Tablet ----
mcp__chrome-devtools__resize_page { width: 768, height: 1024 }
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/tablet.png", fullPage: true }

mcp__chrome-devtools__close_page
```

> 你也可以用 `mcp__chrome-devtools__emulate` 选择一个命名的设备预设, 而不必用 `resize_page` 手动指定尺寸。

## Example 6: 控制台健康检查 —— 确定性错误检测

**用户请求**: "我的应用有没有 JS 报错?"

chrome-devtools MCP 原生捕获控制台消息, 所以你不需要注入 console 垫片。用 `list_console_messages` 查运行时错误, 用 `list_network_requests` 查加载失败。

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/", isolatedContext: "ui-test" }

# ---- Check each route for failed resource loads and JS errors ----

# Method 1: Failed resource loads — list network requests and look for >= 400 status
mcp__chrome-devtools__list_network_requests
# Inspect statuses; any 4xx/5xx is a failed load. For details on one request:
# mcp__chrome-devtools__get_network_request { url: "<failing url>" }

# You can also pull failed loads deterministically via the performance API:
mcp__chrome-devtools__evaluate_script { function: "() => performance.getEntries().filter(e => e.entryType === 'resource' && e.responseStatus >= 400).map(e => ({ url: e.name, status: e.responseStatus }))" }
# Result: [] = PASS, any failed resources = FAIL

# Method 2: Runtime / uncaught errors — the MCP records them; just list errors
mcp__chrome-devtools__list_console_messages { types: ["error"] }

# Now interact (click buttons, submit forms, navigate), then re-check console
# mcp__chrome-devtools__click { uid: "<some button>" }
# mcp__chrome-devtools__list_console_messages { types: ["error"] }

# Example: check homepage
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/" }
mcp__chrome-devtools__evaluate_script { function: "() => performance.getEntries().filter(e => e.entryType === 'resource' && e.responseStatus >= 400).map(e => e.name)" }
# Result: [] — no failed loads
# STEP_PASS|console-home|0 failed resources on initial load

# Example: check dashboard with interaction
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/dashboard" }
mcp__chrome-devtools__take_snapshot
# uid=12 button "Refresh"
mcp__chrome-devtools__click { uid: "12" }
mcp__chrome-devtools__list_console_messages { types: ["error"] }
# Result: 1 error — "Failed to fetch /api/items"
# STEP_FAIL|console-dashboard|expected 0 errors → 1 error during interaction: "Failed to fetch /api/items"

mcp__chrome-devtools__close_page
```

## Example 7: 在已部署站点上的登录态测试

**用户请求**: "测一下我们的预发布 dashboard。我本地已经登录了。"

chrome-devtools MCP 驱动的是你真实的本地 Chrome, 所以如果你已经在那个浏览器里登录了预发布环境, 那些会话会自动延续过来 —— 不需要 cookie 同步, 不需要远程浏览器, 也不需要 context ID。直接在 **默认** context 里导航即可 (这里不要用 `isolatedContext`, 因为那会以未登录状态启动)。

```
# Navigate in the user's default Chrome — inherits the existing login
mcp__chrome-devtools__navigate_page { type: "url", url: "https://staging.myapp.com/dashboard" }

# Verify authenticated state
mcp__chrome-devtools__take_snapshot
# Check: user avatar present? Dashboard content loaded? Not a login redirect?
mcp__chrome-devtools__evaluate_script { function: "() => location.href" }
# Verify URL is /dashboard, not /login

# STEP_PASS|remote-auth|authenticated dashboard loaded, user avatar present, URL is /dashboard

# Run tests against authenticated pages
mcp__chrome-devtools__navigate_page { type: "url", url: "https://staging.myapp.com/settings" }
mcp__chrome-devtools__take_snapshot
# Verify settings content loads

# STEP_PASS|remote-settings|settings page loaded with form fields, not login redirect

# axe-core on the authenticated page
mcp__chrome-devtools__evaluate_script { function: "async () => { await new Promise((res, rej) => { const s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); const r = await axe.run(); return { violations: r.violations.length, passes: r.passes.length }; }" }
```

> 如果用户 **尚未** 登录, 在 Chrome 里手动登录一次 (或用 `fill`/`click` 脚本化登录表单), 之后会话会在整个运行过程中持续有效。不要关掉用户的标签页 —— 只 `close_page` 你自己打开的那些标签页。

## Example 8: 探索式测试 —— 想办法把它弄崩

**用户请求**: "探索一下我的应用, 找找 bug。"

```
mcp__chrome-devtools__new_page { url: "http://localhost:3000/", isolatedContext: "ui-test" }

# ---- First impressions ----
mcp__chrome-devtools__take_snapshot
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/explore-home.png" }

# Console health check
mcp__chrome-devtools__list_console_messages { types: ["error"] }

# ---- Empty state audit ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/dashboard" }
mcp__chrome-devtools__take_snapshot
# Is there a designed empty state? Or just blank space?
# Check for: message, CTA, illustration
# STEP_PASS|empty-state|dashboard shows "No items yet." with CTA "Create your first item"
# or on failure:
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/empty-state.png" }
# STEP_FAIL|empty-state|expected designed empty state → page is blank with no guidance|.context/ui-test-screenshots/empty-state.png

# ---- 404 handling ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/this-page-does-not-exist" }
mcp__chrome-devtools__take_snapshot
# Check: custom 404? Or generic error? Or blank?
mcp__chrome-devtools__evaluate_script { function: "() => location.href" }
# STEP_PASS|404-page|custom 404 page with "Page not found" and link to home
# or: STEP_FAIL|404-page|expected custom 404 → got default Next.js error page

# ---- Form stress test ----
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/contact" }
mcp__chrome-devtools__take_snapshot
# uid=4 textbox "Message", uid=2 textbox "Email", uid=9 button "Send"

# Extremely long input
mcp__chrome-devtools__fill { uid: "4", value: "This is a very long message that keeps going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going and going" }
mcp__chrome-devtools__take_snapshot
mcp__chrome-devtools__take_screenshot { filePath: ".context/ui-test-screenshots/long-input.png" }
# Check: does textarea grow? Overflow? Break layout?

# Special characters (fill both fields at once with fill_form)
mcp__chrome-devtools__fill_form { elements: [
  { uid: "2", value: "test@test.com" },
  { uid: "4", value: "<img src=x onerror=alert(1)> & \"quotes\" and emoji 🎉" }
] }
mcp__chrome-devtools__click { uid: "9" }
mcp__chrome-devtools__take_snapshot
# Check: content rendered safely? Not interpreted as HTML?

# ---- Navigation dead ends ----
# Click every nav link, check each page has a way back
mcp__chrome-devtools__navigate_page { type: "url", url: "http://localhost:3000/pricing" }
mcp__chrome-devtools__take_snapshot
# Are there nav links? Can you get back to home?

mcp__chrome-devtools__close_page
```

**探索式发现的报告格式**:
```
FINDING: Contact form textarea has no maxlength — 500+ char input accepted without truncation
SEVERITY: low
ROUTE: /contact
EVIDENCE: Filled 280 chars into message field, form accepted it, layout intact
RECOMMENDATION: Consider adding maxlength or character counter if there's a backend limit

FINDING: No custom 404 page — default Next.js error shown
SEVERITY: medium
ROUTE: /does-not-exist
EVIDENCE: Navigated to non-existent route, got default "404 | This page could not be found."
RECOMMENDATION: Add a custom not-found.tsx with navigation back to the app
```

## Example 9: 在已部署站点上的分组顺序测试

**用户请求**: "对预发布站点做 QA —— 测注册, dashboard, 以及无障碍。"

只有 **一个共享的 Chrome**, 而且 `select_page` 是全局的, 所以测试组不能并发运行 —— 并行的 agent 会互相破坏对方的页面状态。正确做法是把工作拆成若干组以实现 **context 隔离**, 然后 **一组接一组** 地运行: 派发一个子 agent, 等它跑完并汇报, 再派发下一个。每组在自己的回合里独占浏览器。

**第 1 步: 规划分组**

```
Sequential Groups (run one at a time)
=====================================
Group 1 (signup)     → /signup form tests (happy path + adversarial)
Group 2 (dashboard)  → /dashboard content + empty state
Group 3 (a11y)       → /settings axe-core + keyboard nav
```

**第 2 步: 鉴权 (如有需要)**

没有 cookie 同步。如果预发布站点需要登录, 在运行前于真实 Chrome (默认 context) 里登录一次 —— chrome-devtools MCP 会让每一组都复用那个会话。需要鉴权的组应当在 **默认** context 里打开页面 (而不是 `isolatedContext`, 后者会以未登录状态启动)。

```bash
mkdir -p .context/ui-test-screenshots
```

**第 3 步: 一次派发一个 agent (顺序进行)**

使用 Agent 工具, 但 **每条消息只发一个** 提示词, 并等每个跑完再开始下一个 —— 它们共享这一个浏览器, 必须轮流来。

```
Agent 1 prompt (runs first, finishes, then Agent 2 starts):
  "You are running UI tests on https://staging.myapp.com/signup.
   You own the single shared Chrome for this turn — no other agent is using it.
   Drive the browser ONLY through chrome-devtools MCP tools (mcp__chrome-devtools__*).
   Start with:
     mcp__chrome-devtools__navigate_page { type: 'url', url: 'https://staging.myapp.com/signup' }
   (The default Chrome context is already logged in. Don't open an isolated context.)

   Run these tests using the before/after snapshot pattern:
   1. [happy] Fill valid email, submit, verify success
   2. [adversarial] Submit empty form, verify error
   3. [adversarial] Fill XSS payload, verify rejected
   4. [adversarial] Double-click submit, verify no duplicate

   For each test: snapshot BEFORE, act, snapshot AFTER, compare, emit:
     STEP_PASS|<id>|<evidence>  or  STEP_FAIL|<id>|<expected> → <actual>
   Prefix any screenshot filenames with the group name: signup-<step-id>.png
   When done, close any tabs you opened with mcp__chrome-devtools__close_page so the next agent inherits a clean browser."

Agent 2 prompt (runs only after Agent 1 reports back):
  "You are running UI tests on https://staging.myapp.com/dashboard.
   You own the single shared Chrome for this turn.
   Drive the browser ONLY through chrome-devtools MCP tools.
   Start with:
     mcp__chrome-devtools__navigate_page { type: 'url', url: 'https://staging.myapp.com/dashboard' }

   Run these tests:
   1. Check empty state — is there a message and CTA, or blank?
   2. Check data display — table columns, row count, formatting
   3. Check console errors — list_console_messages { types: ['error'] } after interacting

   Emit STEP_PASS/STEP_FAIL markers. Prefix screenshots with dashboard-<step-id>.png.
   When done, close tabs you opened with close_page."

Agent 3 prompt (runs only after Agent 2 reports back):
  "You are running accessibility tests on https://staging.myapp.com/settings.
   You own the single shared Chrome for this turn.
   Drive the browser ONLY through chrome-devtools MCP tools.
   Start with:
     mcp__chrome-devtools__navigate_page { type: 'url', url: 'https://staging.myapp.com/settings' }

   Run these tests:
   1. axe-core audit — load script, run, check violations
   2. Form labels — every input has an associated label
   3. Keyboard nav — Tab through all elements, verify focus order
   4. Broken images — check naturalWidth on all img elements

   Emit STEP_PASS/STEP_FAIL markers. Prefix screenshots with a11y-<step-id>.png.
   When done, close tabs you opened with close_page."
```

**第 4 步: 合并结果**

每个 agent 返回时, 把标记收集进一份统一报告:

```
## UI Test Results (Sequential Run — 3 groups, one shared Chrome)

### Group: signup
STEP_PASS|valid-email|heading "Welcome!" appeared at uid=15 after submit
STEP_PASS|empty-submit|alert "Email required" appeared at uid=9
STEP_PASS|xss-email|XSS payload rejected by validation
STEP_FAIL|double-submit|expected single submission → two success toasts|.context/ui-test-screenshots/signup-double-submit.png

### Group: dashboard
STEP_PASS|empty-state|"No items yet" with CTA "Create first item"
STEP_PASS|data-display|table: 5 rows, 4 columns, dates formatted
STEP_PASS|console-health|0 errors during interaction

### Group: a11y
STEP_FAIL|axe-audit|expected 0 violations → 2: color-contrast (serious, 3 nodes), label (critical, 1 node)|.context/ui-test-screenshots/a11y-axe-audit.png
STEP_PASS|form-labels|all 4 inputs have associated labels
STEP_PASS|keyboard-nav|10 elements reachable, logical order
STEP_PASS|images|0 broken images

---
**Summary: 9/11 passed, 2 failed (3 groups, run sequentially)**
Failed: double-submit (signup), axe-audit (a11y)
```

**第 5 步: 清理**

```
# Each agent should already have closed its own tabs. As a safety net, list pages
# and close any extras you opened — do NOT close the user's original tabs.
mcp__chrome-devtools__list_pages
# mcp__chrome-devtools__close_page   # for each leftover tab you created
```

## 小贴士

- **每次交互都做前后对比** —— 不对比状态变化就不要下断言
- **确定性检查最有力** —— axe-core 计数, 控制台错误数组, 溢出布尔值
- **想办法把它弄崩** —— 空输入, 超长输入, 特殊字符, 快速连点, 纯键盘操作
- **使用结构化标记** —— `STEP_PASS|id|evidence` 或 `STEP_FAIL|id|expected → actual|screenshot-path`
- **每个失败都截图** —— `take_screenshot { filePath: ".context/ui-test-screenshots/<step-id>.png" }`, 这样开发者能看到到底哪里崩了
- **使用 uid 前先重新快照** —— 每次快照以及任何 DOM 变化后 uid 都会重新编号; 永远基于最新的一份快照来操作
- **干净运行用隔离 context** —— `new_page { isolatedContext: "ui-test" }` 用于可复现的 localhost QA; 只有在需要复用已有登录态时才用默认 context
- **鉴权 = 真实 Chrome 会话** —— 在你本地 Chrome (默认 context) 里登录一次就会延续过来; 没有 cookie 同步, 没有远程浏览器
- **只关你自己打开的标签页** —— 完事后 `close_page` 你自己的标签页; 绝不杀掉用户的其他标签页
- **需要 await 时用 `async () => { ... }`** —— `evaluate_script` 会等待返回的 promise; 结果必须是可 JSON 序列化的
- **一个浏览器, 同一时刻只能一个 agent** —— `select_page` 是全局的; 顺序派发测试组子 agent, 绝不并发
