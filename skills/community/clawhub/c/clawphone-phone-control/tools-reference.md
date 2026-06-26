# MCP 工具完整参考

## 感知工具

| 工具 | 参数 | 返回 | 速度 |
|------|------|------|------|
| `get_screen_info` | 无 | 包名+可见文字+分辨率 | 快（优先用） |
| `capture_screen` | 无 | 带网格的 JPEG 图 | 慢（需坐标时用） |
| `get_current_app` | 无 | 当前包名 | 快 |
| `get_screen_texts` | 无 | 所有可见文字列表 | 快 |
| `find_node` | text | 元素坐标+属性 | 快 |

## 操作工具

| 工具 | 参数 | 说明 |
|------|------|------|
| `tap` | x,y (0~1) | 归一化坐标点击 |
| `long_press` | x,y,duration | 长按弹菜单，默认 800ms |
| `click_by_text` | text | 按文字找元素点击（微信弹窗无效）|
| `type_text` | text | 输入文字（自动剪贴板+粘贴）|
| `press_enter` | 无 | 找「发送」或触发 IME |
| `press_back` | 无 | 返回键 |
| `press_home` | 无 | Home 键 |
| `scroll` | direction(up/down/left/right) | 滑动约 40% 屏幕 |
| `launch_app` | package_name | 先尝试直接启动；若前台未切到目标 App，再回桌面后截图找图标点击 |
| `open_notification_panel` | 无 | 下拉通知栏 |

## 剪贴板工具

| 工具 | 参数 | 说明 |
|------|------|------|
| `set_clipboard` | text | 写入剪贴板（type_text 内部已调用，通常不需单独用）|
| `clear_input` | 无 | 清空当前输入框 |

## 事件工具

| 工具 | 参数 | 说明 |
|------|------|------|
| `get_phone_events` | 无 | 取出并清空事件队列 |
| `peek_phone_events` | 无 | 只看不取 |

## 微信专属注意事项

| 场景 | 正确做法 | 错误做法（勿用）|
|------|---------|--------------|
| 启动微信 | 先看当前界面；可先尝试 `launch_app("com.tencent.mm")`，若仍停留桌面，再 `press_home` → 截图找图标 → `tap` | 未确认前台是否切到微信，就假定已成功启动 |
| 输入文字 | 先截图确认真实输入框位置并点亮输入框，再 `type_text(...)`，随后确认绿色发送按钮是否出现 | 直接 `type_text` 不先点输入框；把某次截图里的输入框坐标当成通用规则 |
| 点击弹出菜单 | `tap` 精确坐标 | `click_by_text`（微信弹窗不在无障碍树）|
| 语音转文字 | 长按气泡后先截图确认弹窗布局，再临时点击当前截图里的“转文字”区域 | `click_by_text("转文字")`；把某次弹窗坐标固化下来 |
| 发送消息 | 优先点当前可见的绿色`发送`按钮；`press_enter`只作兜底，且发送后必须截图确认新气泡出现 | 文字还没进输入框就发送；只调用 `press_enter` 就认定已发出 |
| 发送后退出 | 若后续依赖新消息事件，`press_back` 回到会话列表 | 停留在聊天界面（会导致哨兵停推事件）|

## 常用包名

| App | 包名 |
|-----|------|
| 微信 | com.tencent.mm |
| 飞书 | com.ss.android.lark |
| 华为桌面 | com.huawei.android.launcher |
| 华为系统 UI | com.android.systemui |
