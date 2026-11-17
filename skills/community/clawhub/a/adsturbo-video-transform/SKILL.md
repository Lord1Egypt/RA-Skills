---
name: adsturbo-video-transform
description: Swap out one element of a video: replace the on-screen person, drive a static portrait with a reference video's motion, or translate the whole video into another language. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code. 换掉视频里的某个元素：把出镜人物换成另一个人、用参考视频的动作驱动静态人像、把整条视频翻译成另一种语言。需要 AdsTurbo 账号，可在对话里用邮箱验证码直接注册登录。
---
# AdsTurbo Video Transform

Replace an element in a video: the person, the motion, or the language.

## When to use this skill

Use it when the user says "swap the character", "swap the person", "face swap", "translate the video", "translate to English", "motion control", or "make this photo move".

For pure quality, watermark, or subtitle issues, use `adsturbo-video-enhance` instead — that's cleanup, this is content transformation.

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
What does the user want to replace?
├─ The on-screen person (keep the motion/scene) → character-swap
├─ Make a still portrait perform a reference motion → motion-control
└─ The language (re-dub with lip sync)            → translate
```

```bash
python3 scripts/video_transform.py character-swap \
  --video-url https://.../original.mp4 --image-url https://.../new-person.jpg

python3 scripts/video_transform.py motion-control \
  --video-url https://.../dance.mp4 --image-url https://.../portrait.jpg

python3 scripts/video_transform.py translate \
  --video-url https://.../clip.mp4 --target-lang en
```

`character-swap` and `motion-control` take similar-looking parameters with opposite meanings — don't mix them up:

| | Video provides | Image provides |
|---|---|---|
| `character-swap` | Scene and footage | The new person |
| `motion-control` | The motion | The portrait to be driven |

Full parameter reference: [references/video_transform.md](references/video_transform.md).

## Hard constraint: assets must be public URLs

`--video-url` and `--image-url` **do not accept local file paths**:

```bash
python3 scripts/upload.py file ./clip.mp4
python3 scripts/upload.py image ./person.jpg
```

You can also chain a previous task's output via `--workspace-id`. See [references/upload.md](references/upload.md) for details.

## Handling async tasks

Everything is async; by default the script submits and then auto-polls until the result is ready.

- On timeout: run `query --workspace-id <id>` to keep waiting — **do not resubmit**. The task is still running, and resubmitting will double-charge credits.
- To submit without waiting: use `--no-wait`.

See [references/work.md](references/work.md) for details.

## When replying to the user

- Give the video link directly — don't mention script names, command lines, JSON, or exit codes
- After submitting, state an estimated duration: character swap and motion control take 3-5 minutes, translation takes 5-10 minutes
- For character swap, if the source has multiple shots or the same person changing outfits, later shots may not swap cleanly — in that case, suggest the user split the video into single shots and process them separately; this works better than rerunning the whole clip
- When the user says "translate the video", confirm whether they want re-dubbing (this skill) or just adding foreign-language subtitles (`subtitle` in `adsturbo-video-enhance`)

## Capability boundaries

| What the user wants | Use |
|---|---|
| Remove watermark / 4K / add subtitles | `adsturbo-video-enhance` |
| Generate a new video | `adsturbo-video-generation` |
| Replicate a reference video | `adsturbo-ad-clone` |
| Digital human voiceover / lip sync | `adsturbo-digital-human` |
| Swap a character in an image | `adsturbo-image` |

---

# AdsTurbo 视频改造

换掉视频里的某个元素：人物、动作、语言。

## 什么时候用这个 skill

用户说「换角色」「换个人」「换脸」「视频翻译」「翻译成英文」「动作控制」「让这张照片动起来」时用它。

只是画质、水印、字幕的问题用 `adsturbo-video-enhance`——那是清理，这里是改内容。

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
用户要换掉什么？
├─ 出镜的人（保留动作场景）  → character-swap
├─ 让静态人像做出参考动作    → motion-control
└─ 语言（重新配音对口型）    → translate
```

```bash
python3 scripts/video_transform.py character-swap \
  --video-url https://.../original.mp4 --image-url https://.../new-person.jpg

python3 scripts/video_transform.py motion-control \
  --video-url https://.../dance.mp4 --image-url https://.../portrait.jpg

python3 scripts/video_transform.py translate \
  --video-url https://.../clip.mp4 --target-lang en
```

`character-swap` 和 `motion-control` 参数长得一样但含义相反，别搞混：

| | 视频提供 | 图片提供 |
|---|---|---|
| `character-swap` | 画面与场景 | 新的人 |
| `motion-control` | 动作 | 被驱动的人像 |

完整参数见 [references/video_transform.md](references/video_transform.md)。

## 硬约束：素材只收公网 URL

`--video-url` `--image-url` **不接受本地文件路径**：

```bash
python3 scripts/upload.py file ./clip.mp4
python3 scripts/upload.py image ./person.jpg
```

也可以用 `--workspace-id` 接上一个任务的产物。详见 [references/upload.md](references/upload.md)。

## 异步任务怎么处理

全部异步，脚本默认提交后自动轮询到出结果。

- 超时了：`query --workspace-id <id>` 接着等，**不要重新提交**——任务还在跑，重交会重复扣费
- 只想提交不等：`--no-wait`

详见 [references/work.md](references/work.md)。

## 回复用户时

- 直接给视频链接，不要提脚本名、命令行、JSON 或退出码
- 提交后说一句预计时长：换角色和动作控制 3–5 分钟，翻译 5–10 分钟
- 换角色遇到多镜头、同一人换装出现的素材，后段镜头可能换不干净——这时建议用户把视频裁成单镜头分别处理，比重跑整条更有效
- 用户说「翻译视频」时确认要的是重新配音（这里）还是只加外语字幕（`adsturbo-video-enhance` 的 `subtitle`）

## 能力边界

| 用户想要 | 该用 |
|---|---|
| 去水印 / 4K / 加字幕 | `adsturbo-video-enhance` |
| 生成新视频 | `adsturbo-video-generation` |
| 照着参考视频复刻 | `adsturbo-ad-clone` |
| 数字人口播 / 对口型 | `adsturbo-digital-human` |
| 图片换角色 | `adsturbo-image` |
