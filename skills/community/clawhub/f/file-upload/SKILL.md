---
name: file-upload
description: >-
  通过 Flyelep 开放接口把本地图片、视频、音频上传到云存储，返回可公网访问的直链。
  当用户提供的是本地文件而不是 URL，或需要为其它 Flyelep 技能准备 imgUrls（抠图、翻译、延展、局部重绘等）、
  referenceImageStr / referenceVideoStr / referenceAudioStr（生成视频）入参时使用此技能。
---
# Flyelep 文件上传
通过 Flyelep 开放接口把本地图片、视频、音频文件上传到云存储，并返回永久可访问的 URL。

**重要：这是一个 HTTP API 调用技能。必须通过 HTTP POST 请求调用 API 接口，禁止通过浏览器访问 Flyelep 网站。**

## API 接口信息
- **URL**: `POST https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload`
- **Content-Type**: `multipart/form-data`
- **认证方式**: 在请求头中传入 `secretKey`
- **超时时间**: 图片建议 60-120 秒，视频、音频建议 300 秒

## 认证方式
需在请求头中传入 `secretKey`。该密钥需由用户在 Flyelep 开放平台申请获得：https://www.flyelep.cn/controlboard 。

请求头示例：

```http
secretKey: 用户提供的API密钥
```

> **安全说明**：不要将真实密钥写入技能文件、示例代码仓库或持久化配置中，应在运行时由用户动态提供。

## 请求参数
本接口使用 `multipart/form-data` 上传，不是 JSON body。

| 字段 | 类型 | 说明 |
|------|------|------|
| file | 文件 | 图片、视频或音频二进制文件，`multipart/form-data` 方式上传 |

单次请求只能上传一个文件。需要上传多个时并发调用多次，每次得到一个独立 URL。

**不要手动设置 `Content-Type` 请求头**，让 HTTP 客户端自动生成带 boundary 的值，手写会导致服务端解析失败。

## 响应格式
统一响应结构：

```json
{
  "code": 200,
  "msg": null,
  "data": {
    "relativePath": "cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.png",
    "fullPath": "https://agent-1404002717.cos.ap-guangzhou.myqcloud.com/cos_ai_agent/2026-08-11/3f2a9c1b7d84e6f5a012.png",
    "serviceProvider": null
  }
}
```

- `code=200` 表示调用成功
- **判断成功只看 `code`，不要只看 HTTP 状态码**：业务失败时 HTTP 仍是 200，`code` 会是 500 或 9999，原因在 `msg` 里
- `data.fullPath` 为完整可访问 URL，永久有效、不带签名、不会过期
- `data.relativePath` 为对象存储的内部 key
- `data.serviceProvider` 恒为 `null`，开放接口固定落国内 COS 桶，不需要处理这个字段

## 参数映射规则
### 该用哪个返回字段
- 展示给用户、或作为其它 Flyelep 技能的 `imgUrls` / `imageUrl` / `referenceImageStr` / `referenceVideoStr` / `referenceAudioStr` 入参，一律用 `fullPath`
- `relativePath` 是存储侧内部标识，除非接口明确要求，否则不要传

### 文件名与 URL 的关系
- 服务端会把对象重命名为 `cos_ai_agent/yyyy-MM-dd/32位UUID.后缀`，**原文件名不出现在 URL 里**（只留档在文件记录中）
- 因此中文名、空格、括号、特殊字符的文件名都能正常上传，不需要提前改名；但**后缀必须保留**，服务端靠它判断格式
- 同一个文件重复上传会得到两个不同的 URL，服务端不做去重。**同一个文件在一次任务里只上传一次**，把 `fullPath` 记下来复用，不要每步都重传

### 是否计费
上传不消耗算力/积分，也不占用生图的并发额度，只做鉴权和内容审核。但它会真实写入对象存储，不要拿它做批量试探或压测。

### 支持的文件格式
| 类别 | 支持的后缀 |
|------|-----------|
| 图片 | `bmp`、`gif`、`jpg`、`jpeg`、`png` |
| 视频 | `mp4`、`mov`、`m4v`、`webm`、`avi`、`mkv` |
| 音频 | `mp3`、`wav`、`m4a`、`aac`、`ogg`、`flac` |

- 后缀取自文件名，取不到时才回退到 Content-Type。**务必保证上传的文件名带正确后缀**，否则可能被判为格式不支持
- Content-Type 回退只认 `png`、`jpg`、`jpeg`、`bmp`、`gif`、`mp4`、`avi` 这几种。`.mov` 走回退会被识别成 `quicktime` 而落到白名单外，`webm`、`mkv`、`m4v` 和全部音频格式则完全无法回退，这些文件**必须**带后缀
- 表格外的格式会被直接拒绝。图片里的 `webp` 也不支持，需先转成 `png` 或 `jpg` 再传
- 视频、音频的格式范围与「生成视频」技能的参考素材识别范围一致，上传成功的文件都能直接作为参考素材使用

### 内容审核
- **图片**要先过内容审核才入桶，审核不通过则整个请求失败，不会产生半成品文件。审核加上传通常几秒，超时不要设得太短
- 送审时服务端会先把图片缩到 1024×1024 以内，但**这只是送审用的副本**；进桶的是原始文件，画质、分辨率、体积都不变，所以不用担心上传会降质
- **视频和音频不做内容审核**，直接入库。不要用它上传来源不明的内容

### 文件体积
视频、音频体积远大于图片，上传耗时更长，超时时间要相应放宽（建议视频用 300 秒）。

服务端的单文件上限由部署配置决定，接口本身不返回明确的体积提示：**超限时只会得到 `code=9999`、`msg` 为 `服务繁忙，请稍后再试` 的通用错误**。遇到这个响应且文件明显偏大时，按体积问题处理——先压缩或裁剪再重试，不要反复原样重传。

作为「生成视频」技能的参考素材时，还要满足该技能自己的限制：参考视频单个不超过 50MB、总时长不超过 15 秒。

## 调用示例
本接口没有 JSON body，因此不存在中文编码问题，无需创建临时文件。

- **Windows/PowerShell 环境**：使用 `curl.exe`（而非 `curl`，后者在 PowerShell 中是 `Invoke-WebRequest` 的别名）。`-F` 的值用引号包住，`@` 不会被误解析。
- **macOS/Linux 环境**：直接使用 `curl`。

**示例 1：上传单张图片（Windows/PowerShell）**

```bash
curl.exe -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 120 -F "file=@C:/path/to/product.png"
```

**示例 2：上传单张图片（macOS/Linux）**

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 120 -F "file=@./product.png"
```

**示例 3：上传视频（超时时间放宽）**

```bash
curl.exe -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload" -H "secretKey: 你的密钥" --max-time 300 -F "file=@C:/path/to/reference.mp4"
```

**示例 4：上传后接着调用其它技能**

1. 上传本地文件，从响应里取出 `data.fullPath`
2. 图片 URL 作为 `imgUrls` 传给抠图、翻译、延展等技能；视频、音频 URL 作为 `referenceVideoStr`、`referenceAudioStr` 传给生成视频技能

```bash
curl -X POST "https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting" -H "Content-Type: application/json; charset=utf-8" -H "secretKey: 你的密钥" --max-time 300 --data-binary '{"imgUrls":"上一步返回的 fullPath"}'
```

## 常见错误及解决方案
| 错误 | 原因与解决 |
|------|-----------|
| `msg` 为 `上传的文件不能为空` | 文件是 0 字节，或路径写错导致读到空文件 |
| `msg` 为 `文件格式不支持，图片仅支持：...` | 后缀不在白名单，或文件名没带后缀，参照上面的格式表转换后重试 |
| `msg` 为 `密钥不能为空!` | 带了 `secretKey` 请求头但值是空字符串 |
| `msg` 为 `密钥无效!` | 密钥错误或已失效，向用户重新索取 |
| `msg` 为 `密钥格式错误!` | 密钥能解密但内容不是合法客户 ID，密钥被截断或拼接错了，向用户重新索取 |
| `msg` 为 `用户不存在` | 密钥有效但对应客户没有关联的系统用户，属于账号侧问题，重试无效，让用户联系平台 |
| `msg` 提示图片违规 | 内容审核未通过，需更换图片，重试无效 |
| `msg` 为 `COS上传文件异常` / `保存文件信息失败` / `文件上传失败，请稍后重试` | 存储或落库环节失败，属于服务端瞬时问题，可重试 |
| `code` 为 `9999`、`msg` 为 `服务繁忙，请稍后再试` | 通用兜底错误，最常见的三个原因：完全没带 `secretKey` 请求头、表单字段名不是 `file`、文件体积超出服务端上限。**先自查这三项再重试** |
| 服务端解析失败 | 手动设置了 `Content-Type` 导致 boundary 丢失，去掉该请求头 |
| 请求超时 | 文件较大时适当增大超时时间，视频建议 300 秒 |

> **注意**：缺少 `secretKey` 请求头或写错 `file` 字段名时，接口不会给出针对性提示，只返回上面那条通用错误。所以拿到 `9999` 时不要当成服务端故障，先核对请求头和表单字段名。

密钥问题、格式问题、审核不通过、体积超限，重试都不会好，不要自动重试。只有网络超时、5xx 和存储类异常值得重试。

## 使用时机
当用户给的是本地文件路径而不是公网 URL 时，先用此技能上传拿到直链，再调用其它 Flyelep 技能。如果用户已经提供了公网可访问的直链，则不需要此技能，直接调用目标技能即可。
