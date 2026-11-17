---
name: adsturbo-video-generation
description: Create video from scratch: text-to-video, image-to-video, first/last-frame interpolation, multi-reference generation, plus extending and locally editing existing videos. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code. 从零造画面：文生视频、图生视频、首尾帧补全、多参考素材生成，以及对已有视频做延长和局部编辑。需要 AdsTurbo 账号，可在对话里用邮箱验证码直接注册登录。
---
# AdsTurbo AI Video Generation

Generate video footage from scratch, and extend or locally edit existing video.

## When to use this skill

Use it when the user says "text-to-video," "image-to-video," "generate a video," "start/end frame," "extend video," "continue video," or "change the background in the video."

To make a character speak, use `adsturbo-digital-human`; to replicate a reference video, use `adsturbo-ad-clone`.

## Prerequisites

- Python 3.8+ (the scripts use the standard library only; nothing to install)
- An AdsTurbo account. No account yet is fine: the user can sign up or log in right in the chat with their email and a verification code, and the scripts get an API key automatically (see below)
- Optional `ADSTURBO_BASE_URL`, defaults to `https://adsturbo.ai/klian/novartapi`

### Logging in from the chat (signs up new users too)

On first use, or when a script prints `"error": "api_key_required"` or hits a 401, log the user in right here instead of sending them to the website:

1. Ask for the user's email and run `python3 scripts/login.py start --email <email>`
2. If it returns `"next": "enter_captcha"`: show the user the image at `captcha_url` (or the local file `captcha_file`), ask them to type the characters, then run `python3 scripts/login.py captcha --code <what they typed>`. The user must read and type the captcha themselves; never solve it on their behalf
3. Once it returns `"next": "enter_email_code"`, ask the user for the code AdsTurbo emailed them (check spam too) and run `python3 scripts/login.py verify --code <code>`
4. On success the API key is saved on this machine in `~/.config/adsturbo/credentials.json` and every script picks it up; just re-run the command that needed it

A new email is signed up automatically; an existing user is simply logged in and no duplicate key is created. `login.py status` shows whether a key is available; run `login.py logout` before switching accounts. The old way still works too: sign up at https://adsturbo.ai?channel=clawhub, create a key at https://adsturbo.ai/iris/api and `export ADSTURBO_API_KEY=<key>`; the environment variable takes precedence.

Every plan can call the API with an API key, and usage is billed in credits; if you run out, top up or upgrade at https://adsturbo.ai/pricing. 1080p+ video and 4K images need a subscription (credit packs alone don't count), and creating a custom digital human needs a Pro plan.

**If the user is not logged in yet**: do not keep retrying. First finish everything that doesn't need the API (clarify the brief, draft the script or prompt, settle aspect ratio, duration, model and other parameters, prepare the exact command), then log them in with the steps above and run the prepared command. If the captcha answer is wrong, run `start` again for a fresh image. Never echo the key back in a reply; script output only shows its last four characters.

## Three commands

```bash
# Text-to-video
python3 scripts/video_generation.py generate --prompt "Sunset over the ocean, camera slowly pushing in"

# Image-to-video / start-end frame
python3 scripts/video_generation.py generate --prompt "Product rotating on display" \
  --start-frame https://.../product.jpg

# Extend (seedance-2.0 only)
python3 scripts/video_generation.py extend --video-url https://.../clip.mp4 --duration 10

# Local edit (seedance-2.0 only)
python3 scripts/video_generation.py edit --video-url https://.../clip.mp4 \
  --prompt "Replace the background with an office" --mask-url https://.../mask.png
```

## Key point: the model determines valid parameter values

`duration` / `resolution` / `ratio` / reference-asset limits **differ per model** — `veo-3.1` only supports 4/6/8 seconds, `seedance-2.0` supports 4-15 seconds, and `grok` doesn't support start-end frames.

**Before building a request for the user, check the model comparison table in [references/video_generation.md](references/video_generation.md)**. When a non-default model is specified, verify `duration`, `ratio`, and `resolution` individually. Omitting `--model` falls back to the server default, which is the simplest option.

`extend` and `edit` **only support `seedance-2.0`** — don't recommend other models for these.

## Hard constraint: assets must be public URLs only

`--start-frame`, `--end-frame`, `--reference-images`, `--reference-videos`, and `--video-url` **do not accept local file paths**:

```bash
python3 scripts/upload.py image ./frame.jpg
python3 scripts/upload.py file ./clip.mp4
```

See [references/upload.md](references/upload.md) for details.

## Handling async tasks

All three commands are asynchronous; by default the script submits the job and polls automatically until a result is ready.

- On timeout: use `query --workspace-id <id>` to keep waiting — **do not resubmit**, the task is still running and resubmitting will incur duplicate charges
- To submit without waiting: `--no-wait`
- For idempotent retries: pass `--idempotency-key` — the same key will not create a duplicate task

See [references/work.md](references/work.md) for details.

## When replying to the user

- Give the video link directly — don't mention script names, command lines, JSON, or exit codes
- After submission, mention it will take about 3-8 minutes
- If a parameter is rejected by the server, it's usually a model/duration/ratio/resolution mismatch — check the table, retry with a valid value, and don't dump the raw error on the user

## Capability boundaries

| User wants | Use |
|---|---|
| Digital human voiceover / lip sync | `adsturbo-digital-human` |
| Replicate a reference video | `adsturbo-ad-clone` |
| Watermark removal / 4K / subtitles | `adsturbo-video-enhance` |
| Character swap / translation / motion control | `adsturbo-video-transform` |
| Generate images | `adsturbo-image` |

---

# AdsTurbo AI 视频生成

从零生成视频画面，以及对已有视频做延长和局部编辑。

## 什么时候用这个 skill

用户说「文生视频」「图生视频」「生成一段视频」「首尾帧」「视频延长」「续写视频」「改视频里的背景」时用它。

要让人物说话用 `adsturbo-digital-human`；要照着一条参考视频复刻用 `adsturbo-ad-clone`。

## 前置条件

- Python 3.8+（脚本只用标准库，不需要安装依赖）
- AdsTurbo 账号。没有也行：在对话里用邮箱 + 验证码就能注册或登录，脚本自动拿到 API Key，见下
- 可选 `ADSTURBO_BASE_URL`，默认 `https://adsturbo.ai/klian/novartapi`

### 在对话里登录（没有账号就顺便注册）

用户第一次用、或脚本输出 `"error": "api_key_required"` / 报 401 时，就在对话里帮用户登录，不用让他跳去网页：

1. 问用户的邮箱，执行 `python3 scripts/login.py start --email <邮箱>`
2. 如果返回 `"next": "enter_captcha"`：把 `captcha_url` 这张图（或本地文件 `captcha_file`）给用户看，请他照图输入字符，再执行 `python3 scripts/login.py captcha --code <用户输入>`。图形验证码必须由用户本人辨认输入，不要自己识别代填
3. 返回 `"next": "enter_email_code"` 后，请用户去邮箱（也看看垃圾箱）找 AdsTurbo 发来的验证码，执行 `python3 scripts/login.py verify --code <验证码>`
4. 成功后 API Key 保存在本机 `~/.config/adsturbo/credentials.json`，之后所有脚本自动使用，直接重跑刚才的命令

新邮箱自动注册，老用户就是登录，不会重复创建 Key。`login.py status` 查看是否已登录，换账号先 `login.py logout`。也可以照旧在 https://adsturbo.ai?channel=clawhub 注册后到 https://adsturbo.ai/iris/api 创建 Key 并 `export ADSTURBO_API_KEY=<Key>`，环境变量优先。

任何套餐都能用 API Key 调用，按用量扣积分；积分不够时到 https://adsturbo.ai/pricing 充值或升级。1080p 及以上视频、4K 图片需要订阅（只买积分包不算），创建自定义数字人需要 Pro 套餐。

**用户还没登录时**：不要反复重试。先把不需要调接口就能做的部分做完（理清需求，写好文案或提示词，定好画幅、时长、模型等参数，拼好要执行的完整命令），再按上面的步骤在对话里登录，成功后直接执行准备好的命令。图形验证码输错时按提示重新 `start` 换一张图。Key 不要在回复里回显，脚本输出里只有末 4 位。

## 三个命令

```bash
# 文生视频
python3 scripts/video_generation.py generate --prompt "海边日落，镜头缓慢推进"

# 图生视频 / 首尾帧
python3 scripts/video_generation.py generate --prompt "产品旋转展示" \
  --start-frame https://.../product.jpg

# 延长（仅 seedance-2.0）
python3 scripts/video_generation.py extend --video-url https://.../clip.mp4 --duration 10

# 局部编辑（仅 seedance-2.0）
python3 scripts/video_generation.py edit --video-url https://.../clip.mp4 \
  --prompt "把背景换成办公室" --mask-url https://.../mask.png
```

## 关键：模型决定参数取值

`duration` / `resolution` / `ratio` / 参考素材上限**每个模型都不一样**——`veo-3.1` 只能 4/6/8 秒，`seedance-2.0` 是 4~15 秒，`grok` 不支持首尾帧。

**为用户构造请求前，先查 [references/video_generation.md](references/video_generation.md) 里的模型对照表**，指定了非默认 model 时必须逐项核对 `duration`、`ratio`、`resolution`。不传 `--model` 就走服务端默认，最省事。

`extend` 和 `edit` **只支持 `seedance-2.0`**，不要给用户推荐其他模型。

## 硬约束：素材只收公网 URL

`--start-frame` `--end-frame` `--reference-images` `--reference-videos` `--video-url` 都**不接受本地文件路径**：

```bash
python3 scripts/upload.py image ./frame.jpg
python3 scripts/upload.py file ./clip.mp4
```

详见 [references/upload.md](references/upload.md)。

## 异步任务怎么处理

三个命令都是异步的，脚本默认提交后自动轮询到出结果。

- 超时了：`query --workspace-id <id>` 接着等，**不要重新提交**——任务还在跑，重交会重复扣费
- 只想提交不等：`--no-wait`
- 重试要幂等：带上 `--idempotency-key`，同一个 key 不会重复建任务

详见 [references/work.md](references/work.md)。

## 回复用户时

- 直接给视频链接，不要提脚本名、命令行、JSON 或退出码
- 提交后说一句预计 3–8 分钟
- 参数被服务端拒了，多半是模型与 duration/ratio/resolution 不匹配——查表改一个合法值重试，别把原始报错甩给用户

## 能力边界

| 用户想要 | 该用 |
|---|---|
| 数字人口播 / 对口型 | `adsturbo-digital-human` |
| 照着参考视频复刻 | `adsturbo-ad-clone` |
| 去水印 / 4K / 字幕 | `adsturbo-video-enhance` |
| 换角色 / 翻译 / 动作控制 | `adsturbo-video-transform` |
| 生成图片 | `adsturbo-image` |
