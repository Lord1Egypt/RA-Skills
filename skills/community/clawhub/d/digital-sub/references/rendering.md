# Base64 二维码渲染参考

## AI 对话内嵌渲染

当对话接口支持图片消息，优先将 Base64 转成 data URI 后作为图片内容返回：

```js
function toDataUri(base64, mime = "image/png") {
  const payload = String(base64).replace(/^data:[^,]+,/, "").replace(/\s+/g, "");
  return `data:${mime};base64,${payload}`;
}
// 将返回值作为图片消息/富媒体图片输出，而不是普通文本
const imageDataUri = toDataUri(item.qrCode, item.qrMimeType);
```

如果运行环境只接受 HTML，可使用：

```js
const img = document.createElement("img");
img.alt = "微信扫码绑定企业全情报订阅";
img.src = toDataUri(qrCode, "image/png");
document.body.appendChild(img);
```

不要把未经校验的字符串放入 `<script>`；Base64 只应进入 `img.src` 或图片消息字段。

## CLI 文件模式

Node.js 标准库即可完成解码，不需要把 Base64 放进命令行参数：

```js
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { randomBytes } from "node:crypto";

const payload = String(process.env.QR_BASE64 || "")
  .replace(/^data:[^,]+,/, "").replace(/\s+/g, "");
if (!/^[A-Za-z0-9+/]*={0,2}$/.test(payload)) throw new Error("Invalid Base64");
const file = join(tmpdir(), `digital-sub-qr-${randomBytes(8).toString("hex")}.png`);
writeFileSync(file, Buffer.from(payload, "base64"), { mode: 0o600 });
console.log(file);
```

将输出的绝对路径交给 macOS `open` 或 Linux `xdg-open`。如果 CLI 进程无法创建临时文件，应退回输出 data URI 或提示用户授予临时目录权限，不要尝试写入受保护目录。
