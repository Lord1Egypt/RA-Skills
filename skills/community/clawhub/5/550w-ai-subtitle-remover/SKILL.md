---
name: ai-subtitle-remover
description: 上传视频或提供 URL，调用 550W AI 去字幕 API 擦除硬字幕/水印/台标/Logo，返回处理后视频
metadata: { "openclaw": { "emoji": "🎬", "requires": { "env": ["SUBTITLE_REMOVER_USER_NO", "SUBTITLE_REMOVER_API_KEY"] }, "primaryEnv": "SUBTITLE_REMOVER_API_KEY" } }
---

# AI 视频去字幕

## When to Use

- 用户需要去除视频中的硬字幕、水印、台标或 Logo
- 用户提供了本地视频文件或视频 URL，希望得到去字幕后的干净视频
- 用户需要查询去字幕任务的处理进度或历史记录
- 用户需要查询账户积分余额或预估处理费用

## 凭证配置

首次使用前需要配置凭证：
- **userNo**: 用户编号
- **apiKey**: 调用密钥
- 申请地址: https://qzm.550wai.cn

## 支持的 Actions

| Action | 说明 |
|--------|------|
| uploadVideo | 上传本地视频文件，获取云端 URL |
| submitTask | 提交去字幕任务，指定字幕区域 |
| taskDetail | 查询任务处理状态和结果 |
| taskList | 分页查询历史任务列表 |
| queryCredits | 查询账户积分余额，支持消耗预估 |
| workflow | 端到端工作流：上传→提交→轮询→返回结果 |

## Workflow

### 重要：调用规则

**调用 workflow action 时，只传 `file` 或 `videoUrl` 一个参数即可。禁止传递 width、height、duration、x1、y1、x2、y2 参数。** Skill 内部会自动获取视频元信息并使用全屏去字幕模式。不要使用 ffprobe 或其他工具预先探测视频信息。

正确调用示例：
```json
{ "action": "workflow", "params": { "videoUrl": "https://example.com/video.mp4" } }
```
或：
```json
{ "action": "workflow", "params": { "file": <视频文件对象> } }
```

错误调用示例（不要这样做）：
```json
{ "action": "workflow", "params": { "videoUrl": "...", "width": 1920, "height": 1080, "duration": 60, "x1": 0, "y1": 0, "x2": 0, "y2": 0 } }
```

### 执行流程

1. 用户提供视频文件或视频 URL。
2. 直接调用 `workflow` action，仅传 `file` 或 `videoUrl`。
3. Skill 自动获取 width/height/duration，坐标默认全屏模式。
4. Skill 自动完成上传（如需）、提交任务、轮询状态，最终返回去字幕后的视频下载地址。
5. 如果任务在 10 分钟内未完成，返回 taskId 供后续手动查询。

### 分步模式

1. 调用 `uploadVideo` 上传视频文件，获取 videoUrl。
2. 调用 `submitTask` 提交去字幕任务，指定 videoUrl、宽高、时长和字幕区域坐标。
3. 调用 `taskDetail` 轮询任务状态，直到 status 为 success 或 failed。
4. 成功时从 resultUrl 下载去字幕后的视频。

## 参数约束

- **视频格式**: 仅支持 mp4、mov
- **文件大小**: 最大 1GB
- **分辨率**: width × height ≤ 2,073,600 像素
- **时长**: 1~600 秒
- **宽高**: 1~10000 像素
- **字幕区域**: 全屏模式设 x1=y1=x2=y2=0；非全屏模式需满足 x2>x1, y2>y1, x2≤width, y2≤height
- **videoUrl**: 必须以 http:// 或 https:// 开头，长度 ≤2048

## 积分计费

- 720p 及以下（≤921,600 像素）: ⌈时长(秒) × 1.3⌉ 积分
- 超过 720p（>921,600 像素）: ⌈时长(秒) × 1.6⌉ 积分
- 任务失败时积分自动退还

## 错误处理

- **code=-100**: 鉴权失败，检查 userNo 和 apiKey 配置
- **code=-200**: 参数不合法，根据 message 修正参数
- **code=-300**: 业务拒绝（积分不足、任务不存在等）
- **code=-500**: 服务异常，建议 30 秒后重试

## 注意事项

- 相同 videoUrl 重复提交会被视为独立任务并独立计费
- workflow 模式最多轮询 10 分钟（20 次，每次间隔 30 秒）
- 连续 3 次轮询失败时 workflow 会提前终止并返回 taskId
- 查询接口超时 10 秒，上传接口超时 180 秒，提交接口超时 150 秒

## 回复用户规范

任务完成后，**必须**将结果告知用户：

**成功时回复：**
- 告知用户去字幕已完成
- 提供去字幕后的视频下载链接（resultUrl）
- 可选：告知消耗积分数

**失败时回复：**
- 告知用户任务失败
- 提供失败原因（failReason）
- 告知积分已自动退还

**超时时回复：**
- 告知用户任务仍在处理中
- 提供 taskId 供后续查询

**禁止回复 NO_REPLY。任何情况下都必须向用户展示处理结果。**
