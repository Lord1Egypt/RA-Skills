---
name: adsturbo-ad-clone
description: Clone a competitor ad: auto-storyboard it into shots and prompts, then regenerate a new video with the same structure -- or open an editable draft to rewrite lines, swap in your own people or products and check the price before generating. Can also run analysis only, with no generation. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code. 看中一条广告就照着做一条：自动拉片得出分镜与提示词，再生成同款结构的新视频；也能先出可编辑草稿，改台词、换成自己的人物或产品、看好报价再生成。也可只做视频分析不生成。需要 AdsTurbo 账号，可在对话里用邮箱验证码直接注册登录。
---
# AdsTurbo Ad Video Clone

Found an ad you like the structure of? Build your own following that same structure.

## When to use this skill

Use it when the user says "clone this video," "make one like this," "replicate it," "same-style video," "shot-by-shot breakdown," or "analyze this ad."

For generating from scratch without referencing any video, use `adsturbo-video-generation`.

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

## Two steps: analyze first, then clone

```bash
# 1. Analyze the reference video (synchronous, seconds to 2 minutes)
python3 scripts/ad_clone.py analyze --video-url https://.../reference.mp4

# 2. Generate the new video using the prompt from the analysis
python3 scripts/ad_clone.py generate --prompt "<prompt from previous step>" \
  --video-url https://.../reference.mp4 --ratio 9:16
```

**These two steps must be used together** — the `generate` prompt is the output of `analyze`. In between, you can tweak a few lines of the prompt based on what the user wants — this is the most effective way to adjust the clone's outcome, and it's cheaper than repeatedly rerunning generation.

Each clip has a 12-second cap; for longer videos, trim a segment first with `--clip-start` / `--clip-end`.

If you just want to understand a video without generating anything, use `inspect`. Full parameter reference: [references/ad_clone.md](references/ad_clone.md).

## To rewrite lines, swap people or products, or see the price first: use the draft flow

When the user wants to change the original dialogue, replace the on-screen person or product with their own, or know the credit cost up front, switch to the draft flow:

```bash
# 1. Create a draft and wait for the analysis (the trimmed source must not exceed 15 seconds)
python3 scripts/ad_clone.py draft-create --video-url https://.../reference.mp4
# 2. See the edited prompt and the quote -- no charge
python3 scripts/ad_clone.py draft-preview --clone-id <clone_id> \
  --line "L1=New line" --ref "person@subject_1=https://.../me.jpg"
# 3. Generate once the user confirms -- this charges credits; keep the edits identical to step 2
python3 scripts/ad_clone.py draft-submit --clone-id <clone_id> \
  --line "L1=New line" --ref "person@subject_1=https://.../me.jpg"
```

`draft-submit` charges credits: tell the user the quote from `draft-preview` and submit only after they confirm. See [references/ad_clone.md](references/ad_clone.md).

## Hard constraint: only public URLs are accepted for source material

`--video-url` **does not accept local file paths**:

```bash
python3 scripts/upload.py file ./reference.mp4
```

See [references/upload.md](references/upload.md) for details.

## Handling async tasks

`analyze` is synchronous — you get the result directly. `generate` / `inspect` are asynchronous; the script polls automatically by default until the result is ready.

- On timeout: use `query --workspace-id <id>` to keep waiting — **do not resubmit**. The task is still running, and resubmitting will incur duplicate charges.
- To submit without waiting: use `--no-wait`

See [references/work.md](references/work.md) for details.

## When replying to the user

- Give the video link directly — don't mention script names, command lines, JSON, or exit codes
- The shot breakdown and prompt from `analyze` can be described to the user so they can confirm whether adjustments are needed before moving on to `generate`
- After submitting generation, mention it will take roughly 3–10 minutes
- In the draft flow, walk the user through the editable lines, the replaceable people/products and the quote, and let them decide what to change

## Scope boundaries

The finished clone often needs further processing, which belongs to other skills:

| User wants | Use |
|---|---|
| Replace the person in the cloned video with themselves | `adsturbo-video-transform` |
| Translate the clone into another language for overseas ads | `adsturbo-video-transform` |
| Remove the original watermark before cloning | `adsturbo-video-enhance` |
| Generate from scratch with no reference video | `adsturbo-video-generation` |
| Digital human voiceover | `adsturbo-digital-human` |

---

# AdsTurbo 广告视频复刻

看中一条广告，照着它的结构做一条自己的。

## 什么时候用这个 skill

用户说「复刻这条视频」「照着这个拍一个」「仿制」「同款视频」「拉片」「分析这条广告」时用它。

要凭空生成不参考任何视频用 `adsturbo-video-generation`。

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

## 两步：先拉片，再复刻

```bash
# 1. 分析参考视频（同步，秒级到 2 分钟）
python3 scripts/ad_clone.py analyze --video-url https://.../reference.mp4

# 2. 用分析出的 prompt 生成新片
python3 scripts/ad_clone.py generate --prompt "<上一步的 prompt>" \
  --video-url https://.../reference.mp4 --ratio 9:16
```

**这两步必须连用**，`generate` 的 prompt 就是 `analyze` 的产出。中间可以按用户需求改几句 prompt——这是调整复刻效果最有效的地方，比反复重跑生成划算。

单个片段上限 12 秒，长视频用 `--clip-start` / `--clip-end` 先裁一段。

只想读懂一条视频、不生成，用 `inspect`。完整参数见 [references/ad_clone.md](references/ad_clone.md)。

## 要改台词、换人换货、先看报价：用草稿流程

用户想在生成前改掉原片台词、把出镜人物或产品换成自己的、或者先知道要花多少积分，就改用草稿流程：

```bash
# 1. 建草稿并等分析完（源片段截取后不能超过 15 秒）
python3 scripts/ad_clone.py draft-create --video-url https://.../reference.mp4
# 2. 看改完的 prompt 和报价，不扣费
python3 scripts/ad_clone.py draft-preview --clone-id <clone_id> \
  --line "L1=新台词" --ref "person@subject_1=https://.../me.jpg"
# 3. 用户确认后生成，扣积分；编辑参数和第 2 步保持一致
python3 scripts/ad_clone.py draft-submit --clone-id <clone_id> \
  --line "L1=新台词" --ref "person@subject_1=https://.../me.jpg"
```

`draft-submit` 会扣积分：先把 `draft-preview` 的报价讲给用户，确认了再提交。详见 [references/ad_clone.md](references/ad_clone.md)。

## 硬约束：素材只收公网 URL

`--video-url` **不接受本地文件路径**：

```bash
python3 scripts/upload.py file ./reference.mp4
```

详见 [references/upload.md](references/upload.md)。

## 异步任务怎么处理

`analyze` 是同步的，直接拿结果。`generate` / `inspect` 是异步的，脚本默认自动轮询到出结果。

- 超时了：`query --workspace-id <id>` 接着等，**不要重新提交**——任务还在跑，重交会重复扣费
- 只想提交不等：`--no-wait`

详见 [references/work.md](references/work.md)。

## 回复用户时

- 直接给视频链接，不要提脚本名、命令行、JSON 或退出码
- `analyze` 出来的分镜和提示词可以讲给用户听、请他确认要不要调整，再进 `generate`
- 提交生成后说一句预计 3–10 分钟
- 草稿流程里先把可改的台词、可替换的人物/产品和报价讲给用户，让他决定改什么

## 能力边界

复刻出的成片常常还要再加工，那属于别的 skill：

| 用户想要 | 该用 |
|---|---|
| 把复刻结果里的人换成自己 | `adsturbo-video-transform` |
| 复刻后翻译成外语投海外 | `adsturbo-video-transform` |
| 去掉原片水印再复刻 | `adsturbo-video-enhance` |
| 不参考任何视频，凭空生成 | `adsturbo-video-generation` |
| 数字人口播 | `adsturbo-digital-human` |
