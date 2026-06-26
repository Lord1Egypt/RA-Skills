# Abby Browser Skill

_基于 OpenClaw 内置浏览器工具封装_

---

## 解决的问题

让爸爸可以用自然语言控制浏览器，不需要记住复杂命令。

---

## 核心功能

| 功能 | 命令 | 示例 |
|------|------|------|
| 打开网页 | `open` | 打开 Google |
| 截图 | `screenshot` | 截取当前页面 |
| 点击 | `click` | 点击按钮 |
| 输入 | `type` | 输入文字 |
| 填表单 | `fill` | 填写表单 |
| 提取数据 | `snapshot` | 获取页面内容 |
| 等待 | `wait` | 等待加载 |
| 滚动 | `scroll` | 滚动页面 |

---

## 使用方法

### 在对话中

```
爸爸：帮我打开 Google
Abby：好的爸爸！让我打开 Google...
[执行 openclaw browser open https://google.com]
✅ 已打开 Google

爸爸：帮我截图
Abby：好的，截个图...
[执行 openclaw browser screenshot]
📸 截图已保存

爸爸：帮我点击登录按钮
Abby：好的...
[执行 openclaw browser click 12]
✅ 已点击
```

### 常用命令

```bash
# 打开网页
openclaw browser open https://example.com

# 截图
openclaw browser screenshot
openclaw browser screenshot --full-page

# 点击元素 (需要先 snapshot 获取 ref)
openclaw browser click 12
openclaw browser click 12 --double

# 输入文字
openclaw browser type 12 "hello world"

# 填写表单
openclaw browser fill --fields '[{"ref":"1","value":"xxx"}]'

# 获取页面快照
openclaw browser snapshot
openclaw browser snapshot --format aria

# 等待
openclaw browser wait --text "Done"
openclaw browser wait --selector ".content"

# 滚动
openclaw browser evaluate --fn 'window.scrollTo(0, document.body.scrollHeight)'
```

---

## 封装脚本

### scripts/open.py

打开网页的封装脚本。

### scripts/screenshot.py

截图的封装脚本。

### scripts/click.py

点击元素的封装脚本。

### scripts/form.py

表单填写的封装脚本。

### scripts/extract.py

数据提取的封装脚本。

---

## 重要概念

### 1. Element Reference (ref)

每次执行 `snapshot` 后，元素会有一个编号 (ref)：
```
<button ref="12">登录</button>
<input ref="23" />
```

点击 ref=12：`openclaw browser click 12`

### 2. Snapshot 格式

- `--format ai` (默认) - AI 理解
- `--format aria` - 辅助功能树

### 3. 等待加载

操作前最好等待：
```bash
openclaw browser wait --text "加载完成"
```

---

## 安全考虑

- ❌ 不自动执行危险操作
- ✅ 执行前确认
- ✅ 记录操作日志
- ✅ 异常处理

---

## 依赖

- OpenClaw browser 工具
- Chrome/Chromium 浏览器

---

## 相关文档

- [OpenClaw Browser Docs](https://docs.openclaw.ai/cli/browser)

---

_创建于 2026-02-15_
