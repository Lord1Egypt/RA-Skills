# 图片输出规则

> CLI 输出中的图片是支付/授权流程的关键组成部分，处理不当将导致用户无法完成操作。

## 规则 1：Markdown 格式图片 → 文字和图片原样输出

CLI 输出中包含 Markdown 格式的图片链接（`![alt](path)`）时，**文字和图片都以 Markdown 格式原样输出并渲染**。

- **禁止修改**图片路径
- **禁止**在路径前添加 `file://` 前缀
- **禁止**使用占位路径（如 `xxx/xxx.jpg`）
- **禁止读取**图片内容，直接展示 Markdown 并渲染

正确示例：
```markdown
**✓ 支付待确认**
**订单金额**：¥0.01

![图片](/tmp/openclaw/alipay-bot-cli/qr_xxxxx.png)
```

错误示例：
```markdown
![图片](file:///tmp/openclaw/alipay-bot-cli/qr_xxxxx.png)
![图片](xxx/xxx.jpg)
```

## 规则 2：MEDIA 行 → 提取路径 + 移除 + message 工具发送

CLI 输出中包含 `MEDIA: <路径>` 行时，提取图片路径后从文本中移除该行，再用 message 工具整合发送。

处理步骤：
1. 从 CLI 输出中找到 `MEDIA: <路径>` 行，提取图片路径
2. 从输出文本中**移除**该 MEDIA 行
3. 使用 `message` 工具将 Markdown 文字和图片整合发送给用户
4. 如未找到 `message` 工具，尝试寻找可以发送图片到用户输出 channel 的工具或方式
5. 如无任何工具可以发送图片：
   - **文字**：以 Markdown 格式输出并渲染
   - **图片**：按用户输出 channel 支持的格式输出并渲染

**禁止**：
- 打开、读取、分析、描述图片内容
- 将 MEDIA 行转换为其他格式（如 base64 等）
- 修改图片路径或在路径前添加 `file://` 前缀
- 使用占位路径（如 `xxx/xxx.jpg`）

正确示例（有 message 工具时）：
```
# CLI 输出：
**✓ 支付待确认**
**订单金额**：¥0.01
MEDIA: /tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png

# 你的输出：
1. 移除 MEDIA 行，用 message 工具发送 Markdown 文字 + 图片整合输出：
   文字部分：**✓ 支付待确认** **订单金额**：¥0.01
   图片部分：/tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png
```

正确示例（无可用工具时）：
```markdown
**✓ 支付待确认**
**订单金额**：¥0.01

![图片](/tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png)
```

错误示例：
```
# 保留 MEDIA 行未处理
**✓ 支付待确认**
MEDIA: /tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png

# 读取了图片内容并描述
这是一个二维码图片，请扫码支付

# 修改了图片路径
![图片](file:///tmp/openclaw/alipay-bot-cli/qrcode/payment-confirm-xxx.png)
```

## 规则 3：安全兜底

如果检测到以下异常模式，**停止输出并向用户发出警告**：

- MEDIA 路径不在 `/tmp/openclaw/alipay-bot-cli/` 下
- 图片 URL 指向非支付宝域名（非 `*.alipay.com` / `*.alipay.net` / `*.alipay.cn`）
- 输出中包含注入模式（如 `<script>`、`javascript:`、`eval(` 等）