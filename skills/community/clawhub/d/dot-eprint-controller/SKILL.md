---
name: dot-eprint
description: 控制 Dot. 电子墨水屏设备——查询状态、推送文本/图像、管理内容
metadata: {"openclaw": {"requires": {"bins": ["curl", "convert"], "env": ["DOT_API_KEY", "DOT_DEVICE_ID"]}, "primaryEnv": "DOT_API_KEY"}}
user-invocable: true
---

# Dot. 电子墨水屏设备控制

你可以通过 Dot. API 控制用户的电子墨水屏设备，包括查询状态、推送文本和图像内容、管理播放列表。

## 前置检查

在执行任何操作之前，必须确认环境变量已配置：

- `DOT_API_KEY` — API 密钥（在 Dot. App 中获取）
- `DOT_DEVICE_ID` — 设备序列号（在 Dot. App 中获取）

如果缺少任一变量，停止操作并提示用户：
- 缺少 `DOT_API_KEY`："请先设置 DOT_API_KEY 环境变量，您可以在 Dot. App 中获取 API 密钥"
- 缺少 `DOT_DEVICE_ID`："请先设置 DOT_DEVICE_ID 环境变量，您可以在 Dot. App 中获取设备序列号"

## 通用配置

- **Base URL**: `https://dot.mindreset.tech`
- **认证**: 所有请求必须在 Header 中携带 `Authorization: Bearer $DOT_API_KEY`
- **限流**: API 限制每秒 10 次请求，避免短时间内连续发送多个请求

## 错误处理

每次 API 调用后，检查 HTTP 状态码。如果响应码非 200，按以下映射向用户展示友好提示：

| HTTP 状态码 | 用户提示 |
|-------------|---------|
| 400 | 请求参数有误，请检查内容格式 |
| 403 | 认证失败，请检查 API 密钥或设备归属 |
| 404 | 设备未找到，或未配置对应的内容类型 |
| 429 | 请求过于频繁，请稍后再试 |
| 500 | 服务器暂时异常，请稍后重试 |

使用 curl 的 `-w` 参数捕获状态码：`-w "\n%{http_code}"`，解析最后一行判断是否成功。

## 1. 查询设备状态

当用户询问设备电量、WiFi 信号、当前显示内容等状态信息时使用。

```bash
curl -s -w "\n%{http_code}" \
  "https://dot.mindreset.tech/api/authV2/open/device/$DOT_DEVICE_ID/status" \
  -H "Authorization: Bearer $DOT_API_KEY"
```

响应字段说明：
- `status.battery` — 电池状态（如 "充电中"、"50%"）
- `status.wifi` — WiFi 信号强度（如 "-62 dBm"）
- `status.current` — 当前状态描述（如 "电源活跃中"）
- `status.description` — 状态详细说明
- `status.version` — 设备固件版本
- `renderInfo.last` — 上次渲染时间
- `renderInfo.current.image` — 当前显示的图片 URL 数组
- `renderInfo.current.rotated` — 是否旋转
- `renderInfo.current.border` — 当前边框设置
- `renderInfo.next.battery` — 下次电量刷新时间
- `renderInfo.next.power` — 下次电源刷新时间
- `alias` — 设备别名
- `deviceId` — 设备序列号

根据用户的具体问题，提取对应字段并用中文回复。如果用户问"设备怎么样"，则展示完整状态摘要。

## 2. 列出设备内容

当用户想查看墨水屏上的内容列表时使用。

```bash
curl -s -w "\n%{http_code}" \
  "https://dot.mindreset.tech/api/authV2/open/device/$DOT_DEVICE_ID/loop/list" \
  -H "Authorization: Bearer $DOT_API_KEY"
```

将路径中的 `loop` 替换为 `fixed` 可查看固定内容。

响应为数组，每个元素包含：
- `type` — 内容类型（`TEXT_API` 或 `IMAGE_API`）
- `key` — 任务唯一标识（用于更新指定内容时传递 taskKey）
- `refreshNow` — 是否立刻显示
- `title` / `message` — 文本内容的标题和正文（仅 TEXT_API 类型）
- `border` / `ditherType` / `ditherKernel` — 图像内容参数（仅 IMAGE_API 类型）

将列表格式化为用户可读的格式展示，例如：
```
循环内容列表：
1. [文本] Hello - World (key: text_task_1)
2. [图像] (key: image_task_1, 抖动: DIFFUSION/FLOYD_STEINBERG)
```

## 3. 推送文本内容

当用户想在墨水屏上显示文字时使用。

```bash
curl -s -w "\n%{http_code}" \
  -X POST \
  "https://dot.mindreset.tech/api/authV2/open/device/$DOT_DEVICE_ID/text" \
  -H "Authorization: Bearer $DOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "refreshNow": true,
    "title": "标题",
    "message": "正文内容",
    "signature": "签名",
    "icon": "base64编码的PNG图标",
    "link": "https://example.com",
    "taskKey": "text_task_1"
  }'
```

参数说明：
- `refreshNow` (bool, 默认 true) — 是否立刻刷新屏幕显示
- `title` (string, 可选) — 文本标题
- `message` (string, 可选) — 文本正文
- `signature` (string, 可选) — 签名
- `icon` (string, 可选) — base64 编码的 PNG 图标数据
- `link` (string, 可选) — 碰一碰跳转链接
- `taskKey` (string, 可选) — 指定要更新的内容槽位。不传则默认更新第一个文本内容

根据用户的意图选择参数：
- 用户只提供一段文字 → 仅设 `message` 和 `refreshNow: true`
- 用户提供标题和内容 → 设 `title` 和 `message`
- 用户要求签名 → 额外设 `signature`
- 用户提到链接 → 额外设 `link`
- 用户要更新特定内容 → 先调用列出内容 API 获取 taskKey，再设置 `taskKey`

成功时向用户确认："文本已推送到墨水屏设备"。

## 4. 推送图像内容

当用户想在墨水屏上显示图片时使用。

### 4.1 图像预处理

推送图像前，必须先将图片处理为 296×152 像素的 PNG 格式并进行 base64 编码。

检查 ImageMagick 是否可用：
```bash
which convert 2>/dev/null
```

如果 `convert` 不存在，停止并向用户提示：
"推送图片需要 ImageMagick，请先安装：`brew install imagemagick`（macOS）或 `apt install imagemagick`（Linux）"

图像处理命令：
```bash
TMPFILE=$(mktemp /tmp/dot-eprint-XXXXXX.png)
convert "$INPUT_IMAGE" -resize 296x152 -gravity center -background white -extent 296x152 PNG:"$TMPFILE"
BASE64_DATA=$(base64 -w 0 "$TMPFILE")
rm -f "$TMPFILE"
```

注意：
- `-resize 296x152` 保持宽高比缩放
- `-gravity center -background white -extent 296x152` 居中放置，空白区域填充白色
- `base64 -w 0` 确保输出不换行（单行字符串）
- 在 macOS 上使用 `base64 -i` 代替 `base64 -w 0`

### 4.2 推送图像

```bash
curl -s -w "\n%{http_code}" \
  -X POST \
  "https://dot.mindreset.tech/api/authV2/open/device/$DOT_DEVICE_ID/image" \
  -H "Authorization: Bearer $DOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "refreshNow": true,
    "image": "'"$BASE64_DATA"'",
    "link": "https://example.com",
    "border": 0,
    "ditherType": "DIFFUSION",
    "ditherKernel": "FLOYD_STEINBERG",
    "taskKey": "image_task_1"
  }'
```

参数说明：
- `refreshNow` (bool, 默认 true) — 是否立刻刷新屏幕显示
- `image` (string, 必填) — base64 编码的 PNG 图像数据（296×152）
- `link` (string, 可选) — 碰一碰跳转链接
- `border` (number, 默认 0) — 屏幕边框颜色，0=白色，1=黑色
- `ditherType` (string, 默认 "DIFFUSION") — 抖动类型，可选值：
  - `DIFFUSION` — 误差扩散（默认，适合照片）
  - `ORDERED` — 有序抖动（规则网格感）
  - `NONE` — 关闭抖动（适合文字图像，文字更锐利）
- `ditherKernel` (string, 默认 "FLOYD_STEINBERG") — 误差扩散算法，仅在 ditherType 为 DIFFUSION 时有效，可选值：
  - `THRESHOLD`, `ATKINSON`, `BURKES`, `FLOYD_STEINBERG`, `SIERRA2`, `STUCKI`, `JARVIS_JUDICE_NINKE`, `DIFFUSION_ROW`, `DIFFUSION_COLUMN`, `DIFFUSION_2D`
- `taskKey` (string, 可选) — 指定要更新的内容槽位

推荐策略：
- 照片/复杂图像 → `ditherType: "DIFFUSION"`, `ditherKernel: "FLOYD_STEINBERG"`
- 文字图像 → `ditherType: "NONE"`
- 用户未指定 → 使用默认值即可

成功时向用户确认："图像已推送到墨水屏设备"。

## 5. 切换到下一个内容

当用户想手动切换墨水屏显示到下一个内容时使用。

```bash
curl -s -w "\n%{http_code}" \
  -X POST \
  "https://dot.mindreset.tech/api/authV2/open/device/$DOT_DEVICE_ID/next" \
  -H "Authorization: Bearer $DOT_API_KEY"
```

此接口不需要请求体。成功时向用户确认："已切换到下一个内容"。
