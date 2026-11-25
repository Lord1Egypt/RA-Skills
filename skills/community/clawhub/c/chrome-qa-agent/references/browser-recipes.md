# UI 测试浏览器配方

基于 **chrome-devtools MCP** 的即拷即用配方，用于确定性 UI 检查。对 localhost 和任意已部署 URL 都适用——它们驱动的都是同一个本地 Chrome。

**JS 在这里如何运行：** `mcp__chrome-devtools__evaluate_script` 接收的是**函数声明**，而非裸表达式。需要相应地包裹：`() => document.title`。对于任何异步逻辑，传入 `async () => { ... }` 并 `return` 一个可 JSON 序列化的结果——MCP 会 await 返回的 promise，所以无需操心顶层 `await`。要操作快照里的某个元素，把它作为参数接收，并通过 `args` 数组传入其 `uid`：`evaluate_script { function: "(el) => el.innerText", args: ["<uid>"] }`。

## 无障碍审计（axe-core）

在函数内部注入 axe-core，然后运行它——一次调用，无需单独的加载/等待步骤：

```
mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }

mcp__chrome-devtools__evaluate_script {
  function: `async () => {
    // 若离线则自托管此文件 —— 见下方说明。
    if (!window.axe) {
      await new Promise((res, rej) => {
        const s = document.createElement('script');
        s.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js';
        s.onload = res; s.onerror = rej;
        document.head.appendChild(s);
      });
    }
    const r = await window.axe.run();
    return {
      violations: r.violations.map(v => ({
        id: v.id, impact: v.impact, description: v.description,
        nodes: v.nodes.length, help: v.helpUrl
      })),
      passes: r.passes.length,
      incomplete: r.incomplete.length
    };
  }`
}
```

断言：`violations.length === 0`。

解读结果：
- `impact: "critical"` 或 `"serious"` = 必须修复
- `impact: "moderate"` 或 `"minor"` = 应该修复
- 查看 `helpUrl` 获取修复指引

**离线说明：** 上面的 CDN 注入需要网络访问。如果在离线环境运行，请下载 `axe.min.js` 并把 `s.src` 指向本地路径（或在调用 `window.axe.run()` 之前把脚本主体粘贴进函数里）。

## 性能指标

```
mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }

mcp__chrome-devtools__evaluate_script {
  function: `() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const paint = performance.getEntriesByType('paint');
    return {
      domContentLoaded: Math.round(nav?.domContentLoadedEventEnd),
      loadComplete: Math.round(nav?.loadEventEnd),
      firstPaint: Math.round(paint.find(p => p.name === 'first-paint')?.startTime),
      firstContentfulPaint: Math.round(paint.find(p => p.name === 'first-contentful-paint')?.startTime),
      transferSize: nav?.transferSize,
      domInteractive: Math.round(nav?.domInteractive),
    };
  }`
}
```

阈值（Doherty Threshold + Web Vitals）：
- FCP < 1.8s = 良好，< 3s = 有待改进，> 3s = 差
- Load complete < 3s = 对 SaaS 仪表盘而言良好
- DOM interactive < 400ms = 感觉即时（Doherty Threshold）

## 坏图

```
mcp__chrome-devtools__evaluate_script {
  function: `() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0);
    return broken.map(i => ({ src: i.src, alt: i.alt }));
  }`
}
```

断言：不存在 `naturalWidth === 0` 的图片（结果数组为空）。

## 控制台错误

**优先使用原生工具。** chrome-devtools MCP 会直接捕获控制台输出——无需 eval 取巧：

```
mcp__chrome-devtools__list_console_messages { types: ["error"] }
```

这会返回页面发出的错误和未捕获异常。在页面渲染后立即调用一次，并在交互之后再次调用。断言：错误数组为空。用 `mcp__chrome-devtools__get_console_message` 查看单条记录的完整详情。

### 失败的网络请求（确定性，加载时）

对于失败的资源加载（4xx/5xx），优先使用原生网络工具，而非基于 `performance` entry 的 eval：

```
mcp__chrome-devtools__list_network_requests
# 检查任何可疑的请求：
mcp__chrome-devtools__get_network_request { ... }
```

断言：不存在状态码 >= 400 的请求。（如果你想内联完成，仍可以用 `evaluate_script` 遍历 `performance.getEntries()`，但原生工具能给你 headers、timing 以及响应体。）

### 在交互过程中捕获运行时错误（eval 回退方案）

如果你需要把错误归因到某个具体交互，而原生控制台列表的粒度不够细，可以装一个页内捕获器，先交互，再读回结果：

```
mcp__chrome-devtools__evaluate_script {
  function: `() => {
    window.__logs = [];
    const orig = { error: console.error, warn: console.warn };
    console.error = (...args) => { window.__logs.push({type:'error', text: args.join(' ')}); orig.error(...args); };
    console.warn  = (...args) => { window.__logs.push({type:'warn',  text: args.join(' ')}); orig.warn(...args); };
    window.addEventListener('error', e => window.__logs.push({type:'uncaught', text: e.message}));
    window.addEventListener('unhandledrejection', e => window.__logs.push({type:'rejection', text: String(e.reason)}));
    return 'installed';
  }`
}

# 使用快照中的 uid 与页面交互（点击、表单提交等）。
mcp__chrome-devtools__click { uid: "<uid>" }

# 读回交互过程中捕获到的内容。
mcp__chrome-devtools__evaluate_script { function: `() => window.__logs` }
```

大多数情况下 `list_console_messages { types: ["error"] }` 更简单，且在导航后仍能存续——只有当你确实需要把捕获范围限定在单次交互时，才使用这个回退方案。

## 键盘导航

依次 Tab 遍历所有可聚焦元素并记录顺序：

```
mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }

# 一次 Tab 一步
mcp__chrome-devtools__press_key { key: "Tab" }
mcp__chrome-devtools__evaluate_script {
  function: `() => {
    const el = document.activeElement;
    const s = el ? window.getComputedStyle(el) : null;
    return {
      tag: el?.tagName,
      text: el?.textContent?.trim().slice(0, 40),
      role: el?.getAttribute('role'),
      ariaLabel: el?.getAttribute('aria-label'),
      hasFocus: s ? (s.outlineStyle !== 'none' || s.boxShadow !== 'none') : false
    };
  }`
}

# 重复 press_key Tab + evaluate_script 以构建完整的 tab 顺序。
# 当 activeElement 返回 BODY（回环）时停止。
```

在结果中需要检查的点：
- 每个可交互元素都应出现在 tab 顺序中
- 顺序应遵循视觉布局（从上到下、从左到右）
- 每个元素的 `hasFocus` 都应为 true（可见的焦点环）
- 不应有元素被跳过或顺序错乱

## 响应式截图巡检

```
mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }

# 移动端（iPhone SE）
mcp__chrome-devtools__resize_page { width: 375, height: 812 }
mcp__chrome-devtools__take_screenshot { filePath: "/tmp/mobile.png", fullPage: true }

# 平板（iPad）
mcp__chrome-devtools__resize_page { width: 768, height: 1024 }
mcp__chrome-devtools__take_screenshot { filePath: "/tmp/tablet.png", fullPage: true }

# 桌面端
mcp__chrome-devtools__resize_page { width: 1440, height: 900 }
mcp__chrome-devtools__take_screenshot { filePath: "/tmp/desktop.png", fullPage: true }
```

要得到真实的设备画像（触摸 + 设备像素比 + UA），请使用带设备预设的 `mcp__chrome-devtools__emulate`，而非裸的 `resize_page`。

截图完成后，用 Read 工具读取每张截图并评估：
- 移动端：有汉堡菜单吗？触控目标 ≥44px 吗？内容会溢出吗？
- 平板：布局是自适应还是仅仅缩小？侧边栏行为是否正确？
- 桌面端：内容宽度是否合理？是否没有被拉伸到边到边？

## 检查所有链接

```
mcp__chrome-devtools__evaluate_script {
  function: `() => {
    const links = Array.from(document.querySelectorAll('a[href]'));
    return links.map(a => ({
      href: a.href,
      text: a.textContent?.trim().slice(0, 50),
      isExternal: !a.href.startsWith(location.origin),
      opensNewTab: a.target === '_blank'
    }));
  }`
}
```

## 检查表单结构

```
mcp__chrome-devtools__evaluate_script {
  function: `() => {
    const forms = Array.from(document.querySelectorAll('form'));
    return forms.map(f => ({
      action: f.action,
      method: f.method,
      inputs: Array.from(f.querySelectorAll('input,select,textarea')).map(i => ({
        name: i.name, type: i.type, required: i.required,
        hasLabel: !!(i.labels?.length || i.getAttribute('aria-label') || i.getAttribute('aria-labelledby')),
        placeholder: i.placeholder
      }))
    }));
  }`
}
```

断言（表单标签）：每个 input 都有 `hasLabel: true`。

## 检查空状态

导航到一个没有数据的页面/区块并截图：

```
mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }  # 例如没有任何 session 的 /sessions
mcp__chrome-devtools__wait_for { text: "<text that proves the page is ready>" }
mcp__chrome-devtools__take_screenshot { filePath: "/tmp/empty-state.png", fullPage: true }
mcp__chrome-devtools__take_snapshot  # 检查是否有有用的文案/CTA
```

评估：它有提示信息吗？有插画吗？有引导创建第一项的 CTA 吗？还是只是一片空白？
