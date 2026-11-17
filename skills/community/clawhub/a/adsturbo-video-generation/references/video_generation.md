# AI Video Generation

Script: `scripts/video_generation.py`

## generate — Generate Video (Async)

```bash
# Text-to-video
python3 scripts/video_generation.py generate --prompt "海边日落，镜头缓慢推进"

# Image-to-video (first frame)
python3 scripts/video_generation.py generate --prompt "产品旋转展示" \
  --start-frame https://.../product.jpg

# First and last frame
python3 scripts/video_generation.py generate --prompt "从白天过渡到夜晚" \
  --start-frame https://.../day.jpg --end-frame https://.../night.jpg

# Multiple reference assets
python3 scripts/video_generation.py generate --prompt "把这几个元素组合起来" \
  --reference-images https://.../a.jpg https://.../b.jpg
```

## Model Differences Table (Important)

`duration` / `resolution` / `ratio` / reference asset limits **vary by model**. Check this table before building a request for the user; for any non-default model, verify each field individually.

| model | duration | resolution | ratio | start/end_frame | ref_images | ref_videos | ref_audios | Notes |
|---|---|---|---|---|---|---|---|---|
| `veo-3.1` | 4/6/8 (default 8) | 720p/1080p/4k | 16:9 / 9:16 | ≤2 | unlimited | — | — | frame and reference are mutually exclusive |
| `kling-3.0` | 3-15 (default 8) | — | — | ≤2 | ≤1 | — | — | |
| `grok` | 6/10 (default 6) | — | — | not supported | ≤1 (used as first frame) | — | — | |
| `seedance-2.0` | 4-15 (default 15) | 720p/1080p | — | ≤2 | ≤9 | ≤3 | ≤3 | frame and reference are mutually exclusive; audio requires an accompanying image/video |
| `happyhorse-1.0` | 3-15 (default 5) | 720p/1080p | 16:9 / 9:16 / 1:1 / 4:3 / 3:4 | ≤1 | ≤9 | ≤1 (limit drops to ≤5 images when a video is present) | — | frame and reference are mutually exclusive |

If `--model` is omitted, the server default is used. **Server-side validation is authoritative** — combinations not listed in the table will be rejected, and the error message will explain why.

## extend — Extend Video (Async)

```bash
python3 scripts/video_generation.py extend --video-url https://.../clip.mp4 \
  --prompt "继续向前推进" --duration 10
```

**Only `seedance-2.0` is supported**, `duration` 4-15 (default 15), `resolution` is `720p` or `1080p`.

Choose one input source: `--video-url` for an external video, or `--workspace-id` to directly extend the result of the previous generation.

## edit — Partial Video Edit (Async)

```bash
python3 scripts/video_generation.py edit --video-url https://.../clip.mp4 \
  --prompt "把背景换成办公室" --mask-url https://.../mask.png
```

**Only `seedance-2.0` is supported**, `resolution` is `720p` or `1080p`.

`--mask-url` is optional; the white area marks the region to modify. Without a mask, the model decides what to change based on the prompt. `--reference-images` can provide a reference style for the desired result.

## Idempotency

All three commands support `--idempotency-key`: resubmitting with the same key produces only one task, so network retries won't cause duplicate charges.

## Assets Must Be Public URLs

`--start-frame` `--end-frame` `--reference-*` `--video-url` all accept URLs only. Upload local files first:

```bash
python3 scripts/upload.py image ./frame.jpg
python3 scripts/upload.py file ./clip.mp4
```

## Time Reference

Generation, extension, and editing all take 3–8 minutes. Auto-polling is enabled by default; `--no-wait` only submits the task, after which you can use `query --workspace-id <id>` to retrieve the result.

---

# AI 视频生成 / Video Generation

脚本：`scripts/video_generation.py`

## generate — 生成视频（异步）

```bash
# 文生视频
python3 scripts/video_generation.py generate --prompt "海边日落，镜头缓慢推进"

# 图生视频（首帧）
python3 scripts/video_generation.py generate --prompt "产品旋转展示" \
  --start-frame https://.../product.jpg

# 首尾帧
python3 scripts/video_generation.py generate --prompt "从白天过渡到夜晚" \
  --start-frame https://.../day.jpg --end-frame https://.../night.jpg

# 多参考素材
python3 scripts/video_generation.py generate --prompt "把这几个元素组合起来" \
  --reference-images https://.../a.jpg https://.../b.jpg
```

## 模型差异表（关键）

`duration` / `resolution` / `ratio` / 参考素材上限**因模型而异**。为用户构造请求前先查这张表，非默认模型必须逐项核对：

| model | duration | resolution | ratio | start/end_frame | ref_images | ref_videos | ref_audios | 备注 |
|---|---|---|---|---|---|---|---|---|
| `veo-3.1` | 4/6/8（默认 8） | 720p/1080p/4k | 16:9 / 9:16 | ≤2 | 无上限 | — | — | frame 与 reference 互斥 |
| `kling-3.0` | 3~15（默认 8） | — | — | ≤2 | ≤1 | — | — | |
| `grok` | 6/10（默认 6） | — | — | 不支持 | ≤1（当首帧用） | — | — | |
| `seedance-2.0` | 4~15（默认 15） | 720p/1080p | — | ≤2 | ≤9 | ≤3 | ≤3 | frame 与 reference 互斥；audio 需配 image/video |
| `happyhorse-1.0` | 3~15（默认 5） | 720p/1080p | 16:9 / 9:16 / 1:1 / 4:3 / 3:4 | ≤1 | ≤9 | ≤1（有视频时图片改限 ≤5） | — | frame 与 reference 互斥 |

不传 `--model` 走服务端默认。**服务端校验为准**——表里没有的组合会被拒绝，报错信息会说明原因。

## extend — 视频延长（异步）

```bash
python3 scripts/video_generation.py extend --video-url https://.../clip.mp4 \
  --prompt "继续向前推进" --duration 10
```

**仅支持 `seedance-2.0`**，`duration` 4~15（默认 15），`resolution` 取 `720p` / `1080p`。

输入源二选一：`--video-url` 给外部视频，或 `--workspace-id` 直接延长上一次的生成结果。

## edit — 视频局部编辑（异步）

```bash
python3 scripts/video_generation.py edit --video-url https://.../clip.mp4 \
  --prompt "把背景换成办公室" --mask-url https://.../mask.png
```

**仅支持 `seedance-2.0`**，`resolution` 取 `720p` / `1080p`。

`--mask-url` 可选，白色区域为要改动的部分；不给 mask 就由模型按 prompt 自行判断改哪里。`--reference-images` 可提供改动后的参考样式。

## 幂等

三个命令都支持 `--idempotency-key`：同一个 key 重复提交只会产生一个任务，网络重试时不会重复扣费。

## 素材必须是公网 URL

`--start-frame` `--end-frame` `--reference-*` `--video-url` 都只收 URL。本地文件先传：

```bash
python3 scripts/upload.py image ./frame.jpg
python3 scripts/upload.py file ./clip.mp4
```

## 耗时参考

生成 / 延长 / 编辑均为 3–8 分钟。默认自动轮询；`--no-wait` 只提交，之后用 `query --workspace-id <id>` 取结果。
