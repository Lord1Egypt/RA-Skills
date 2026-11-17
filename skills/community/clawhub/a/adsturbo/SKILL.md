---
name: adsturbo
description: AdsTurbo full toolkit: product-link ad videos, AI spokesperson video, video generation & extension, ad cloning, watermark removal, 4K upscaling, video translation, character swap, motion control, subtitles, AI image generation and e-commerce photos. Best for workflows spanning multiple capabilities. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code. AdsTurbo 全能力入口：贴商品链接出广告、AI 数字人口播、视频生成与延长、广告复刻、去水印、4K 超分、视频翻译、换角色、动作控制、字幕、AI 图片生成与电商图。适合需要跨能力串联的完整创作流程。需要 AdsTurbo 账号，可在对话里用邮箱验证码直接注册登录。
---
# AdsTurbo AI Creation Suite

The full set of AdsTurbo's open capabilities: product-link ad videos, digital human voiceover, video generation, ad cloning, video refinement and transformation, AI image creation.

## When to use this skill

Use it for complete creative workflows that **chain multiple capabilities together** — e.g. "clone this ad, swap in our spokesperson, then translate it to English", a single request that bundles three capabilities.

For a single task (just remove a watermark, just generate one image), installing the corresponding single-capability skill is lighter weight.

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

## Intent → script

```
What does the user want?
│
├─ Has a product link, wants an ad
│   ├─ Paste the link, get the ad          → url2video.py create --product-url
│   └─ Link can't be fetched, pass product data → url2video.py create --title ... --ad-type
│
├─ Have someone read out a script
│   ├─ Use a platform avatar     → digital_human.py actors → perform
│   ├─ Use their own likeness    → digital_human.py persona-create → perform
│   └─ Just an image + audio     → digital_human.py lipsync
│
├─ Generate footage from scratch
│   ├─ Text-to-video / image-to-video / first-last frame → video_generation.py generate
│   ├─ Extend an existing video   → video_generation.py extend
│   └─ Edit part of a video       → video_generation.py edit
│
├─ Work from a reference video
│   ├─ Clone it                  → ad_clone.py analyze → generate
│   ├─ Clone with edited lines / your own people or products → ad_clone.py draft-create → draft-preview → draft-submit
│   └─ Analyze only, no generation → ad_clone.py inspect
│
├─ Existing video, make it cleaner (content unchanged)
│   ├─ Remove watermark/clutter  → video_enhance.py remove-object
│   ├─ Remove burned-in subtitles → video_enhance.py erase --method rm_subtitle
│   ├─ Boost resolution/4K       → video_enhance.py upscale
│   └─ Add/translate subtitles   → video_enhance.py subtitle
│
├─ Existing video, swap out an element
│   ├─ Swap the on-screen person → video_transform.py character-swap
│   ├─ Animate a static portrait → video_transform.py motion-control
│   └─ Change language (dubbing) → video_transform.py translate
│
├─ Images
│   ├─ Text-to-image / edit image → image.py create
│   ├─ Product photo set          → image.py ecommerce
│   ├─ Event poster                → image.py poster
│   ├─ Cutout                       → image.py cutout
│   ├─ Remove watermark             → image.py erase
│   └─ Upscale                      → image.py upscale
│
├─ Local file needs to become a URL → upload.py image / audio / file
└─ Check task progress               → work.py status / batch / wait
```

## Phrase quick-reference

| User says | Command |
|---|---|
| Product link to ad, turn this product page into a video | `url2video.py create` (tell the user the estimated credits before submitting) |
| Digital human voiceover, have the avatar say this | `digital_human.py perform` |
| Clone my likeness, make a digital human from my photo | `digital_human.py persona-create` |
| Lip sync, sync lips to audio | `digital_human.py lipsync` |
| Text-to-speech, TTS | `digital_human.py say` |
| Text-to-video, image-to-video, first-last frame | `video_generation.py generate` |
| Extend video, continue, add a few seconds | `video_generation.py extend` |
| Edit video, change background, partial edit | `video_generation.py edit` |
| Clone video, replicate, shoot one just like it | `ad_clone.py analyze` + `generate` |
| Shot breakdown, video analysis | `ad_clone.py inspect` |
| Clone while rewriting lines, swapping in your own people or products, or checking the price first | `ad_clone.py draft-create` → `draft-preview` → `draft-submit` (submit charges credits; confirm the quote first) |
| Remove watermark, remove logo | `video_enhance.py remove-object` |
| Remove subtitles, erase burned-in subtitles | `video_enhance.py erase --method rm_subtitle` |
| 4K, improve quality, upscale, super-resolution | `video_enhance.py upscale` |
| Add subtitles, translate subtitles | `video_enhance.py subtitle` |
| Swap character, replace the whole person, face swap | `video_transform.py character-swap` |
| Motion control, animate a photo | `video_transform.py motion-control` |
| Video translation, translate to English | `video_transform.py translate` |
| Generate an image, AI drawing, text-to-image | `image.py create` |
| Cutout, remove background | `image.py cutout` |
| Product hero shot, e-commerce image, product photo | `image.py ecommerce` |
| Event poster, promo image | `image.py poster` |

## Chaining capabilities (the value of this package)

Add `--no-wait` to an async command to get a `workspace_id`, then feed the previous step's output directly into the next step with `--workspace-id` — no need to download and re-upload:

```bash
# Paste a product link → a 15-second ad with a spoken voiceover (720p is about 270 credits; confirm before submitting)
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set \
  --ad-type ugc --language English

# Clone an ad → swap in your own spokesperson → translate to English
python3 scripts/ad_clone.py analyze --video-url https://.../ref.mp4
python3 scripts/ad_clone.py generate --prompt "<analysis result>" --no-wait
python3 scripts/video_transform.py character-swap --workspace-id ws_aaa --image-url https://.../ceo.jpg --no-wait
python3 scripts/video_transform.py translate --workspace-id ws_bbb --target-lang en

# Generate an image → use it as the first frame for a video → upscale
python3 scripts/image.py create --prompt "product still life"
python3 scripts/video_generation.py generate --prompt "slow orbit" --start-frame <image url from previous step> --no-wait
python3 scripts/video_enhance.py upscale --workspace-id ws_ccc

# Voiceover → drive a digital human with that audio
python3 scripts/digital_human.py say --actor-id act_1 --script "script text"
python3 scripts/digital_human.py perform --actor-id act_1 --said-url <audio_url from previous step>
```

## Two hard constraints

**1. Only public URLs are accepted for assets.** All `--*-url` parameters do not accept local paths. If the user provides a local file, run it through `upload.py` first:

```bash
python3 scripts/upload.py image ./photo.jpg
python3 scripts/upload.py audio ./voice.mp3
python3 scripts/upload.py file ./clip.mp4
```

**2. The model determines valid parameter values.** `duration` / `ratio` / `resolution` / reference-asset limits for video generation and image creation **vary by model**, and image models also split into "text-to-image only" vs. "edit only". Check the model table in the relevant reference before building a request — don't guess from memory.

## Async tasks

Except for image `create`, digital human `say`, and clone `analyze` / `draft-preview`, which are synchronous, everything else is async. Scripts poll automatically to completion by default after submission.

- On timeout: keep waiting with that script's `query --workspace-id <id>` — **do not resubmit**. The task is still running, and resubmitting will double-charge.
- To check progress in bulk: `work.py batch --workspace-ids ws_a ws_b ws_c`
- Retries must be idempotent: include `--idempotency-key`

See [references/work.md](references/work.md) for details.

## When replying to the user

- Give the result link directly — don't mention script names, command lines, JSON, or exit codes
- After submission, give an expected duration: images 30 seconds–3 minutes, video tasks 2–10 minutes
- On error, state the problem in one sentence before asking whether to retry; a rejected parameter is usually a mismatch between model and parameter — check the table, use a valid value, and retry
- If a step fails partway through a chained workflow, the outputs already completed remain valid — continue from the failed step rather than starting over

## Reference docs

| Doc | Covers |
|---|---|
| [digital_human.md](references/digital_human.md) | Digital human, persona, lip sync, TTS |
| [video_generation.md](references/video_generation.md) | Video generate/extend/edit + model comparison table |
| [url2video.md](references/url2video.md) | Product link to ad video, credits, error codes |
| [ad_clone.md](references/ad_clone.md) | Ad cloning, shot breakdown |
| [video_enhance.md](references/video_enhance.md) | Watermark removal, upscaling, subtitles |
| [video_transform.md](references/video_transform.md) | Character swap, motion control, translation |
| [image.md](references/image.md) | Image generate/edit + model capability table, e-commerce photo sets |
| [upload.md](references/upload.md) | Local file to URL |
| [work.md](references/work.md) | Task status, idempotency, timeout handling |

## Scope boundaries

Only the capabilities listed above are supported. The following are **not supported** — do not imply to the user that they can be done: template-based video creation, TikTok data analytics, viral ad library lookup, video clipping and merging.

---

# AdsTurbo AI 创作全家桶

AdsTurbo 的全部开放能力：商品链接出广告、数字人口播、视频生成、广告复刻、视频精修与改造、AI 图片创作。

## 什么时候用这个 skill

需要**跨能力串联**的完整创作流程时用它——比如「复刻这条广告，换成我们的代言人，再翻译成英文」这种一句话里套了三个能力的需求。

只做单件事（只去个水印、只生成一张图）时，装对应的单能力 skill 更轻。

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

## 意图 → 脚本

```
用户要什么？
│
├─ 有商品链接，要一条广告
│   ├─ 贴链接直接出          → url2video.py create --product-url
│   └─ 链接抓不到，改传商品信息 → url2video.py create --title ... --ad-type
│
├─ 让一个人把文案念出来
│   ├─ 用平台形象      → digital_human.py actors → perform
│   ├─ 用自己的形象    → digital_human.py persona-create → perform
│   └─ 就一张图+音频   → digital_human.py lipsync
│
├─ 凭空造画面
│   ├─ 文生/图生/首尾帧 → video_generation.py generate
│   ├─ 延长已有视频     → video_generation.py extend
│   └─ 改视频局部       → video_generation.py edit
│
├─ 照着一条视频做
│   ├─ 复刻            → ad_clone.py analyze → generate
│   ├─ 改台词/换人换货再复刻 → ad_clone.py draft-create → draft-preview → draft-submit
│   └─ 只分析不生成    → ad_clone.py inspect
│
├─ 已有视频，让它更干净（内容不变）
│   ├─ 去水印/杂物     → video_enhance.py remove-object
│   ├─ 去硬字幕        → video_enhance.py erase --method rm_subtitle
│   ├─ 提分辨率/4K     → video_enhance.py upscale
│   └─ 加/翻译字幕     → video_enhance.py subtitle
│
├─ 已有视频，换掉里面的元素
│   ├─ 换出镜的人      → video_transform.py character-swap
│   ├─ 驱动静态人像    → video_transform.py motion-control
│   └─ 换语言（配音）  → video_transform.py translate
│
├─ 图片
│   ├─ 文生图/改图     → image.py create
│   ├─ 商品套图        → image.py ecommerce
│   ├─ 活动海报        → image.py poster
│   ├─ 抠图            → image.py cutout
│   ├─ 去水印          → image.py erase
│   └─ 高清放大        → image.py upscale
│
├─ 本地文件要变成 URL  → upload.py image / audio / file
└─ 查任务进度          → work.py status / batch / wait
```

## 中文说法速查

| 用户说 | 命令 |
|---|---|
| 商品链接出广告、贴链接出片、商品页一键成片 | `url2video.py create`（提交前先告诉用户预计积分） |
| 数字人口播、让数字人说这段话 | `digital_human.py perform` |
| 克隆我的形象、用我的照片做数字人 | `digital_human.py persona-create` |
| 对口型、口型同步 | `digital_human.py lipsync` |
| 语音合成、文字转语音、TTS | `digital_human.py say` |
| 文生视频、图生视频、首尾帧 | `video_generation.py generate` |
| 视频延长、续写、加几秒 | `video_generation.py extend` |
| 视频编辑、改背景、局部修改 | `video_generation.py edit` |
| 复刻视频、仿制、照着拍一个 | `ad_clone.py analyze` + `generate` |
| 拉片、视频分析 | `ad_clone.py inspect` |
| 复刻时改台词、换成自己的人或产品、先看报价 | `ad_clone.py draft-create` → `draft-preview` → `draft-submit`（submit 扣积分，先确认报价） |
| 去水印、去 logo | `video_enhance.py remove-object` |
| 去字幕、抹掉硬字幕 | `video_enhance.py erase --method rm_subtitle` |
| 4K、提升画质、高清化、超分 | `video_enhance.py upscale` |
| 加字幕、字幕翻译 | `video_enhance.py subtitle` |
| 换角色、替换整个人、换脸 | `video_transform.py character-swap` |
| 动作控制、让照片动起来 | `video_transform.py motion-control` |
| 视频翻译、翻译成英文 | `video_transform.py translate` |
| 生成图片、AI 画图、文生图 | `image.py create` |
| 抠图、去背景 | `image.py cutout` |
| 商品主图、电商图、产品图 | `image.py ecommerce` |
| 活动海报、宣传图 | `image.py poster` |

## 跨能力串联（这个包的价值所在）

异步命令加 `--no-wait` 拿到 `workspace_id`，下一步用 `--workspace-id` 直接消费上一步的产物，不用下载再上传：

```bash
# 贴商品链接 → 出一条带真人口播的 15 秒广告（720p 约 270 积分，提交前先确认）
python3 scripts/url2video.py create --product-url https://shop.example.com/products/linen-sheet-set \
  --ad-type ugc --language English

# 复刻广告 → 换成自家代言人 → 翻译成英文
python3 scripts/ad_clone.py analyze --video-url https://.../ref.mp4
python3 scripts/ad_clone.py generate --prompt "<分析结果>" --no-wait
python3 scripts/video_transform.py character-swap --workspace-id ws_aaa --image-url https://.../ceo.jpg --no-wait
python3 scripts/video_transform.py translate --workspace-id ws_bbb --target-lang en

# 出图 → 拿图当首帧生成视频 → 超分
python3 scripts/image.py create --prompt "产品静物图"
python3 scripts/video_generation.py generate --prompt "缓慢环绕" --start-frame <上一步的图片 url> --no-wait
python3 scripts/video_enhance.py upscale --workspace-id ws_ccc

# 配音 → 用这段音频驱动数字人
python3 scripts/digital_human.py say --actor-id act_1 --script "文案"
python3 scripts/digital_human.py perform --actor-id act_1 --said-url <上一步的 audio_url>
```

## 两条硬约束

**1. 素材只收公网 URL。** 所有 `--*-url` 参数都不接受本地路径。用户给本地文件先过 `upload.py`：

```bash
python3 scripts/upload.py image ./photo.jpg
python3 scripts/upload.py audio ./voice.mp3
python3 scripts/upload.py file ./clip.mp4
```

**2. 模型决定参数取值。** 视频生成和图片创作的 `duration` / `ratio` / `resolution` / 参考素材上限**因模型而异**，图片模型还分「只能文生」「只能编辑」。构造请求前先查对应 reference 里的模型表，别凭印象填。

## 异步任务

除图片 `create`、数字人 `say`、复刻 `analyze` / `draft-preview` 是同步外，其余都是异步。脚本默认提交后自动轮询到出结果。

- 超时了：用该脚本的 `query --workspace-id <id>` 接着等，**不要重新提交**——任务还在跑，重交会重复扣费
- 批量看进度：`work.py batch --workspace-ids ws_a ws_b ws_c`
- 重试要幂等：带 `--idempotency-key`

详见 [references/work.md](references/work.md)。

## 回复用户时

- 直接给结果链接，不要提脚本名、命令行、JSON 或退出码
- 提交后给出预计时长：图片 30 秒–3 分钟，视频类 2–10 分钟
- 出错时一句话说清问题再问要不要重试；参数被拒多半是模型与参数不匹配，查表换合法值重试即可
- 串联流程中途某步失败时，前面已完成的产物仍然有效，从失败那步接着做，不用从头再来

## 参考文档

| 文档 | 覆盖 |
|---|---|
| [digital_human.md](references/digital_human.md) | 数字人、persona、对口型、TTS |
| [video_generation.md](references/video_generation.md) | 视频生成/延长/编辑 + 模型对照表 |
| [url2video.md](references/url2video.md) | 商品链接出广告、积分、错误码 |
| [ad_clone.md](references/ad_clone.md) | 广告复刻、拉片 |
| [video_enhance.md](references/video_enhance.md) | 去水印、超分、字幕 |
| [video_transform.md](references/video_transform.md) | 换角色、动作控制、翻译 |
| [image.md](references/image.md) | 图片生成/编辑 + 模型能力表、电商套图 |
| [upload.md](references/upload.md) | 本地文件转 URL |
| [work.md](references/work.md) | 任务状态、幂等、超时处理 |

## 能力边界

只承诺上面列出的能力。以下**不支持**，不要向用户暗示可以做：模板化出片、TikTok 数据分析、爆款广告库查询、视频剪辑与合并。
