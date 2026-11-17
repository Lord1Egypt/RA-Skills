---
name: adsturbo-video-enhance
description: Clean up a video without changing its content: remove watermarks, logos and burnt-in subtitles, upscale to 2K/4K, add or translate subtitles. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code. 画面内容不变，只让成片更干净：去水印、去 logo、去硬字幕、提升分辨率到 2K/4K、添加或翻译字幕。需要 AdsTurbo 账号，可在对话里用邮箱验证码直接注册登录。
---
# AdsTurbo Video Enhance

Leaves the picture content unchanged and just makes the final cut cleaner: watermark removal, resolution upscaling, subtitle handling.

## When to use this skill

Use it when the user says "remove watermark," "remove logo," "remove subtitles," "4K," "improve quality," "upscale," "enhance resolution," "add subtitles," or "translate subtitles."

To **change elements in the picture** (swap the person, dub into another language) use `adsturbo-video-transform` instead — that changes content, this skill only cleans up.

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

## Choosing a command

```
What does the user want to process?
├─ Watermark / logo / clutter        → remove-object
├─ Hardcoded subtitles burned in     → erase --method rm_subtitle
├─ Blurry footage, need 2K/4K        → upscale (or enhance --resolution 4k)
└─ Add subtitles / translate them    → subtitle
```

```bash
python3 scripts/video_enhance.py remove-object --video-url https://.../clip.mp4
python3 scripts/video_enhance.py erase --video-url https://.../clip.mp4 --method rm_subtitle
python3 scripts/video_enhance.py upscale --video-url https://.../clip.mp4
python3 scripts/video_enhance.py subtitle --video-url https://.../clip.mp4 \
  --source-language zh --translate-language en
```

Watch out for two similarly-named concepts:

- **Remove hardcoded subtitles** (`erase --method rm_subtitle`) = erase subtitles already burned into the picture
- **Add subtitles** (`subtitle`) = generate new subtitles; `--translate-language` translates the subtitles, it does not re-dub the audio

The standard combo for localizing a video is `erase --method rm_subtitle` first, then `subtitle --translate-language en`.

Full parameter reference: [references/video_enhance.md](references/video_enhance.md).

## Hard constraint: only public URLs are accepted

`--video-url` **does not accept local file paths**:

```bash
python3 scripts/upload.py file ./clip.mp4
```

You can also use `--workspace-id` to feed the output of a previous task directly as input, skipping the download-then-upload step. See [references/upload.md](references/upload.md) for details.

## Handling async tasks

Everything is async; by default the script submits the job and polls automatically until the result is ready.

- On timeout: run `query --workspace-id <id>` and keep waiting — **do not resubmit**. The task is still running, and resubmitting will double-charge.
- To submit without waiting: use `--no-wait`.

See [references/work.md](references/work.md) for details.

## When replying to the user

- Give the video link directly; don't mention script names, command lines, JSON, or exit codes
- After submitting, state the expected duration: upscaling 3–5 minutes, removal 2–5 minutes, subtitles 2–5 minutes, longer for longer videos
- When the user says "remove subtitles," confirm first whether they mean erasing existing hardcoded subtitles or skipping new subtitles — these are very different things

## Capability boundaries

| User wants | Use |
|---|---|
| Swap out the person on screen | `adsturbo-video-transform` |
| Video translation (re-dub with lip sync) | `adsturbo-video-transform` |
| Generate a new video | `adsturbo-video-generation` |
| Replicate a reference video | `adsturbo-ad-clone` |
| Digital human voiceover | `adsturbo-digital-human` |
| Image watermark removal / image upscaling | `adsturbo-image` |

---

# AdsTurbo 视频精修

画面内容不动，只让成片更干净：去水印、提分辨率、处理字幕。

## 什么时候用这个 skill

用户说「去水印」「去 logo」「去字幕」「4K」「提升画质」「高清化」「超分」「加字幕」「字幕翻译」时用它。

要**改掉画面里的元素**（换人、换语言配音）用 `adsturbo-video-transform`——那是改内容，这里只做清理。

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

## 命令怎么选

```
用户要处理什么？
├─ 水印 / logo / 杂物      → remove-object
├─ 烧死在画面里的硬字幕     → erase --method rm_subtitle
├─ 画质太糊、要 2K/4K      → upscale（或 enhance --resolution 4k）
└─ 要加字幕 / 翻译字幕      → subtitle
```

```bash
python3 scripts/video_enhance.py remove-object --video-url https://.../clip.mp4
python3 scripts/video_enhance.py erase --video-url https://.../clip.mp4 --method rm_subtitle
python3 scripts/video_enhance.py upscale --video-url https://.../clip.mp4
python3 scripts/video_enhance.py subtitle --video-url https://.../clip.mp4 \
  --source-language zh --translate-language en
```

注意区分两组同名概念：

- **去硬字幕**（`erase --method rm_subtitle`）= 抹掉已经烧进画面的字幕
- **加字幕**（`subtitle`）= 生成新字幕；`--translate-language` 是翻译字幕，不是重新配音

视频出海的常规组合是先 `erase --method rm_subtitle` 再 `subtitle --translate-language en`。

完整参数见 [references/video_enhance.md](references/video_enhance.md)。

## 硬约束：素材只收公网 URL

`--video-url` **不接受本地文件路径**：

```bash
python3 scripts/upload.py file ./clip.mp4
```

也可以用 `--workspace-id` 直接拿上一个任务的产物当输入，省掉下载再上传。详见 [references/upload.md](references/upload.md)。

## 异步任务怎么处理

全部异步，脚本默认提交后自动轮询到出结果。

- 超时了：`query --workspace-id <id>` 接着等，**不要重新提交**——任务还在跑，重交会重复扣费
- 只想提交不等：`--no-wait`

详见 [references/work.md](references/work.md)。

## 回复用户时

- 直接给视频链接，不要提脚本名、命令行、JSON 或退出码
- 提交后说一句预计时长：超分 3–5 分钟，消除 2–5 分钟，字幕 2–5 分钟，长视频更久
- 用户说「去字幕」时先确认是抹掉原有硬字幕还是不要新字幕——这两件事差别很大

## 能力边界

| 用户想要 | 该用 |
|---|---|
| 换掉出镜的人 | `adsturbo-video-transform` |
| 视频翻译（重新配音对口型） | `adsturbo-video-transform` |
| 生成新视频 | `adsturbo-video-generation` |
| 照着参考视频复刻 | `adsturbo-ad-clone` |
| 数字人口播 | `adsturbo-digital-human` |
| 图片去水印 / 图片高清放大 | `adsturbo-image` |
