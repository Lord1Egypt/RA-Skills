# 对抗式测试模式

用这些模式去尝试破坏功能。把它们应用到你测试的每一个可交互元素上。

所有步骤都驱动 **chrome-devtools MCP**（`mcp__chrome-devtools__*`）。uid 来自 `take_snapshot`，且每次快照都会重新编号——使用前请重新快照。

### 表单——尝试破坏它们

```
# 空提交
take_snapshot                            # BEFORE: 记下表单字段 + uid
click { uid: "<submit-uid>" }            # ACT: 提交空表单
take_snapshot                            # AFTER: 应出现错误提示

# 长输入（500+ 字符）
fill { uid: "<name-uid>", value: "aaaa....(500 chars)" }
take_snapshot                            # 检查：布局会崩坏吗？文本被截断了吗？

# 特殊字符
fill { uid: "<name-uid>", value: "<script>alert('xss')</script>" }
fill { uid: "<email-uid>", value: "'; DROP TABLE users;--" }
take_snapshot                            # 检查：输入被净化了吗？没有渲染原始 HTML 吧？
# （一次填多个字段：fill_form { elements: [{ uid, value }, ...] }）

# 快速提交 / 快速点击 —— 连续紧挨着触发多次点击
take_snapshot                            # 获取提交按钮当前的 uid
click { uid: "<submit-uid>" }
click { uid: "<submit-uid>" }            # 同一 uid，中间不快照——背靠背连击
take_snapshot                            # 检查：只处理了一次提交吗？
# 注意：click { uid, dblClick: true } 是一次 OS 级双击，并非快速连击。
# 要实现真正的快速连击，请用多次 click 调用，或用一次 evaluate_script
# 通过 args 传入元素并在其上派发多个 click 事件。
# 确认只发出了一次请求：list_network_requests（或查看后端日志）。
```

### 弹窗——测试完整生命周期

```
take_snapshot                            # BEFORE: 树中无 dialog

# 打开
click { uid: "<trigger-uid>" }
take_snapshot                            # AFTER: 应出现 dialog 元素
# ASSERT: 树中存在 dialog role

# 按 Escape 关闭
press_key { key: "Escape" }
take_snapshot                            # AFTER: dialog 应消失
# ASSERT: 树中已移除 dialog role

# 重新打开并取消
click { uid: "<trigger-uid>" }
take_snapshot                            # dialog 出现——重新快照以获取新鲜 uid
click { uid: "<cancel-uid>" }
take_snapshot                            # dialog 消失

# 重新打开并确认
click { uid: "<trigger-uid>" }
take_snapshot                            # dialog 出现——重新快照以获取新鲜 uid
click { uid: "<confirm-uid>" }
take_snapshot                            # dialog 消失 + 副作用已发生

# 点击外部关闭：重新快照，然后点击 backdrop 元素的 uid。
# 原生 alert/confirm/prompt 对话框用 handle_dialog 处理，而非 click。
```

### 导航——验证路由是否正常

```
take_snapshot                            # BEFORE: 记下当前 URL 与内容
click { uid: "<nav-link-uid>" }          # ACT: 点击一个导航链接
wait_for { text: "<text on the destination page>" }
evaluate_script { function: "() => location.href" }   # 检查 URL 是否变化
take_snapshot                            # AFTER: 内容与目标页面一致
# 对比：不同的标题、不同的页面内容

# 后退按钮
navigate_page { type: "back" }
evaluate_script { function: "() => location.href" }   # 应返回原始 URL
take_snapshot                            # 内容与原始页面一致
```

### 错误态——找出缺失的那些

```
# 导航到一个没有数据的页面
navigate_page { type: "url", url: "http://localhost:3000/items" }
take_snapshot
# 检查：是否有设计过的空状态，带提示信息和 CTA？
# 还是只是一片空白？

# 导航到一个不存在的路由
navigate_page { type: "url", url: "http://localhost:3000/does-not-exist" }
take_snapshot
# 检查：404 页面？还是空白/报错？

# 提交无效数据并检查错误恢复
take_snapshot                            # 获取字段 + 提交按钮的 uid
fill { uid: "<field-uid>", value: "invalid" }
click { uid: "<submit-uid>" }
take_snapshot
# 检查：错误提示有用吗？它告诉你哪里错了吗？
# 检查：用户的输入被保留了吗？还是表单被清空了？
```

### 键盘无障碍——不用鼠标能用吗？

```
navigate_page { type: "url", url: "http://localhost:3000/page" }
wait_for { text: "<text that proves the page is ready>" }

# Tab 遍历所有可交互元素
press_key { key: "Tab" }
evaluate_script { function: "() => ({ tag: document.activeElement?.tagName, text: document.activeElement?.textContent?.trim().slice(0,40), role: document.activeElement?.getAttribute('role') })" }
# 重复 press_key Tab + evaluate_script，直到 activeElement 返回 BODY
# 检查：每个可交互元素都能到达吗？焦点环可见吗？顺序合理吗？

# 尝试用键盘激活元素
press_key { key: "Enter" }               # 应激活当前聚焦的按钮
take_snapshot                            # 验证动作已发生
```
