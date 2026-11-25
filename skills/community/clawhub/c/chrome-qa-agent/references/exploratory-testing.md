# 探索式测试

探索式测试由 agent 驱动：你使用 chrome-devtools MCP 工具自由地浏览应用，自行判断点什么、试什么、哪里看起来不对——就像一名人工 QA 测试员。

## 工作原理

与测试套件执行（针对特定路由的结构化测试）不同，探索式测试是开放式的。agent 使用 `take_snapshot` 来理解页面，对下一步该做什么做出判断，执行操作，然后观察结果。

## 工作流

```
1. mcp__chrome-devtools__navigate_page { type: "url", url: "TARGET_URL" }
   (or mcp__chrome-devtools__new_page { url: "TARGET_URL", isolatedContext: "ui-test" } for a clean tab)
2. mcp__chrome-devtools__take_snapshot       → understand what's on the page (elements have uids)
3. mcp__chrome-devtools__take_screenshot     → see what it looks like (Read the screenshot)
4. Decide: what looks wrong? What should I try?
5. click { uid } / fill { uid, value } / press_key { key }  → interact (uids from the latest snapshot)
6. mcp__chrome-devtools__take_snapshot       → observe result
7. Repeat 4-6, navigating through the app freely
```

## 重点关注什么

### 第一印象（30 秒）
- 这个页面的用途是否一目了然？
- 是否有清晰的视觉层级？
- 有没有任何东西看起来坏了、错位或格格不入？
- 有没有控制台错误？（`list_console_messages { types: ["error"] }`）

### 导航测试
- 从当前页面能否到达每一个主要区块？
- 后退按钮能用吗？
- 面包屑是否准确？
- 有没有死胡同（没有任何方式离开的页面）？
- logo 是否链接到首页？

### 表单压力测试
- 尝试提交空表单
- 输入极长的文本（200+ 字符）
- 输入特殊字符：`<script>alert('xss')</script>`、`"quotes"`、`emoji 🎉`
- 快速双击提交按钮
- 用 Tab 遍历所有字段——顺序是否合乎逻辑？
- 校验失败时会发生什么？错误提示是否有帮助？

### 状态持久化
- 填一半表单，跳走，再回来——数据是否保留？
- 创建一个条目，刷新页面——它是否还在？
- 应用筛选条件，刷新——筛选是否保留？
- 打开一个模态框，按 Escape——它是否干净地关闭？

### 边界情况
- 没有数据时页面长什么样（空状态）？
- 当你访问一个不存在的 URL 时会发生什么（404）？
- 会话过期 / 无认证时会发生什么？
- 把视口缩到移动端尺寸（`resize_page { width: 375, height: 812 }`，或用 `emulate` 套用设备预设）——它还能用吗？

### 性能感知
- 页面感觉是快还是卡？
- 慢操作有没有加载指示？
- 内容是突然蹦出来，还是平滑加载？

## 探索式测试报告格式

对每一个发现：
```
FINDING: [brief description]
SEVERITY: critical / high / medium / low
ROUTE: /path/where/found
EVIDENCE: [screenshot path or snapshot excerpt]
RECOMMENDATION: [specific fix suggestion]
```

示例：
```
FINDING: Settings page — "Regenerate API Key" button has no confirmation dialog
SEVERITY: high
ROUTE: /orgs/:slug/:projectId/settings/general
EVIDENCE: Clicked "Regenerate" and the key changed immediately with no warning
RECOMMENDATION: Add a confirmation dialog: "This will invalidate your existing key. Are you sure?"
```
