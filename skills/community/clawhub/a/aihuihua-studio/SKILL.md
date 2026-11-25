---
name: aihuihua-studio
version: 1.0.18
description: 用用户自己的 鼓鼓AI（aihuihua.ai）账号在 Agent 里直接 AI 生图、改图、做视频、写歌、文字转语音，消耗他在网站上的积分。能力：GPT Image 2.5 Flare、GPT Image 2.5 Sunburst、GPT Image 2、Nano Banana Pro、GPT-4o 图片、即梦 Seedream 5.0、Midjourney、即梦 Seedance 2.5、即梦 Seedance 2.0、即梦 Seedance 2.0 Fast、即梦 Seedance 2.0 mini、即梦 Seedance 1.0 Pro、MiniMax H3、Suno 音乐、文字转语音；还有图片高清放大、AI 换脸、AI 抠图。账号能力：授权码登录（浏览器里点一下授权）、查积分余额、查作品和任务、积分不够时选套餐生成微信支付二维码充值。当用户说「画一张 / 生成图片 / 做海报 / 改图 / P 图 / 换背景 / 生成视频 / 图生视频 / 做 MV / 写首歌 / 生成音乐 / 配乐 / 文字转语音 / 配音 / 朗读 / 旁白 / 放大图片 / 换脸」、点名上面任何一个模型、提到 鼓鼓AI / aihuihua.ai，或者问「我还有多少积分 / 充值 / 买积分」时使用。Generate images, videos, music and speech through the user's aihuihua.ai account (GPT Image 2.5, Nano Banana Pro, Midjourney, Seedance, Suno, Doubao TTS…), with device-code login, balance check and WeChat-Pay QR top-up.
---

# 鼓鼓AI AI 创作技能

用用户在 **鼓鼓AI**（https://aihuihua.ai/）的账号调网站上的 AI 绘画、视频、音乐、语音合成模型，按网站价格扣他的积分，
结果自动下载到本地。网站上能用的模型这里都能用，价格和网页端一样。

**入口脚本**：`scripts/studio.mjs`（Node ≥ 20，零依赖）。下文写成 `studio`，执行时换成
**这份 SKILL.md 所在目录**下的绝对路径 —— 技能装在哪儿由工具决定，别照抄示例路径：

```bash
node <技能目录>/scripts/studio.mjs whoami
# 例如装在 ~/.claude/skills 时：
node ~/.claude/skills/aihuihua-studio/scripts/studio.mjs whoami
```

`studio --help` 看全部命令，`studio models` 看全部模型。任何命令加 `--json` 输出 JSON，方便你解析。

退出码：**0** 成功；**1** 出错；**2** 参数不对（看提示改参数）；**3** 积分不足（走第五节充值）；**4** 没登录 / 登录失效 / 等授权或等支付超时。

## 任务完成后的告知（每次都要做）

每次任务完毕（生成、改图、视频出片、放大、换脸、抠图、音乐、卡券兑换等）之后，在回复里：

1. **告知用户本次消耗了多少积分**（以命令输出里的「消耗 N 积分」为准，多次提交就加起来说总数）；
   这次没有消耗积分（失败退回、只是查询、登录、看余额）就**不用提**。
2. 有消耗时，同时告诉用户**可以在这里查看任务明细记录**：https://aihuihua.ai/account/records

## 一、先确认登录

任何操作前先跑：

```bash
node <技能目录>/scripts/studio.mjs whoami
```

退出码 4 表示没登录。登录**分两步跑**（一条命令死等的话，你没法在等的时候把链接告诉用户）：

```bash
node <技能目录>/scripts/studio.mjs login --start
```

输出里有一条 `https://aihuihua.ai/agent-auth?code=XXXX-XXXX` 的链接和授权码（脚本也会尝试自动打开浏览器，
沙箱、远程机器上经常打不开，别指望它）。**把链接和授权码原样写进你的回复**，告诉用户：
「请在浏览器打开这个链接，核对授权码和这里一致后点『授权』」。浏览器里没登录网站的话，页面会先让他登录。
链接不是凭据，可以放心转述。

用户说点完了（或者直接接着等）再跑第二步，Bash 超时给到 300000 毫秒：

```bash
node <技能目录>/scripts/studio.mjs login --wait --timeout 240
```

- 成功打印账号昵称、UID 和积分余额。令牌存在 `~/.aihuihua-studio/credentials.json`（权限 600），之后的命令自动带上。
- 退出码 4 且提示「还没等到授权」：链接 10 分钟内有效，再跑一次 `login --wait` 接着等。
- 过期或被拒绝：重新 `login --start`，把新链接发给用户。
- **不要**读、打印、转述 `~/.aihuihua-studio/` 下的任何文件，里面是用户的登录凭据。
- 用户想看 / 取消授权过哪些 Agent，让他去网站的授权页（就是上面那个链接的页面，不带 code 打开）。

### 技能会自己更新

每条命令运行前，脚本会看一下有没有新版（一小时最多一次），有就自动换掉技能目录、用新版把这条命令重跑一遍。
输出里出现 **「技能已自动更新：vA → vB」** 时，等这条命令结束后**重新读一遍这份 SKILL.md** 再往下走 ——
模型、参数、价格都可能变了。更新失败只打一行「!」开头的提示，照旧用本机这份跑，不用管。

## 二、选模型

| 类型 | 模型 ID | 名称 | 能做什么 | 价格（积分） |
|---|---|---|---|---|
| 图片 | `gpt-image-2.5-flare` | GPT Image 2.5 Flare | OpenAI 最新一代生图，速度快、性价比高：文生图、精确改图、多图融合、局部重绘、透明背景 | 按画质×尺寸计价，每张参考图 +2积分。1K（auto 与 1024/1536 三种尺寸）：low 4 / medium 6 / high 10 / xhigh 22 / max 50；2048x2048：6 / 8 / 25 / 45 / 100；3840x2160：8 / 12 / 30 / 50 / 110 |
| 图片 | `gpt-image-2.5-sunburst` | GPT Image 2.5 Sunburst | GPT Image 2.5 精细版：细节和文字渲染更好、更听话，出图更慢；适合海报、带字设计、产品精修 | 按画质×尺寸计价，每张参考图 +2积分。1K（auto 与 1024/1536 三种尺寸）：low 4 / medium 6 / high 10 / xhigh 22 / max 50；2048x2048：6 / 8 / 25 / 45 / 100；3840x2160：8 / 12 / 30 / 50 / 110 |
| 图片 | `gpt-image-2` | GPT Image 2 | 上一代 GPT 生图，对话式理解提示词，支持参考图改图；固定价格 | 每张 8积分 |
| 图片 | `nano-banana-pro` | Nano Banana Pro（Gemini 3 Pro Image） | Google 的生图 / 改图模型：人物一致性强、换装换背景、多图合成、风格迁移（吉卜力、手办等） | 每张 8积分 |
| 图片 | `gpt-4o-image` | GPT-4o 图片（gpt-image-1） | GPT-4o 生图 / 图片编辑，一次可出多张 | 每张 8积分（--n 张数 × 8） |
| 图片 | `seedream-5` | 即梦 Seedream 5.0（豆包） | 字节即梦 / 豆包 Seedream 5.0：2K～3K 高清大图，中文理解好；支持组图（一次多张连贯图）和故事书（分镜 + 文案） | 每张 8积分，组图 / 故事书按实际生成张数计 |
| 图片 | `midjourney` | Midjourney | 艺术感最强的生图：插画、概念图、摄影风格；一次出 4 张的四宫格，之后可以放大（U）、变体（V）、扩图 | 出图 8积分；U 放大 2；V 变体 8；zoom1.5 8；zoom2 16；pan 扩图 8 |
| 视频 | `seedance-2.5` | 即梦 Seedance 2.5 | 最强模型，画面与音效同步生成，最长 30 秒；自带音效 / 配乐，4～30 秒 | 按分辨率 × 时长计价（积分）：480p 每 5 秒约 53，720p 每 5 秒约 113，1080p 每 5 秒约 278；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准 |
| 视频 | `seedance-2.0` | 即梦 Seedance 2.0 | 全模态能力，支持 1080P 与 4K 输出；自带音效 / 配乐，4～15 秒 | 按分辨率 × 时长计价（积分）：480p 每 5 秒约 35，720p 每 5 秒约 74，1080p 每 5 秒约 184，4k 每 5 秒约 375；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准 |
| 视频 | `seedance-2.0-fast` | 即梦 Seedance 2.0 Fast | 极速推理，效果接近 2.0；自带音效 / 配乐，4～15 秒 | 按分辨率 × 时长计价（积分）：480p 每 5 秒约 28，720p 每 5 秒约 60；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准 |
| 视频 | `seedance-2.0-mini` | 即梦 Seedance 2.0 mini | 极致性价比，出片更快；自带音效 / 配乐，4～15 秒 | 按分辨率 × 时长计价（积分）：480p 每 5 秒约 18，720p 每 5 秒约 37；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准 |
| 视频 | `seedance-1.0-pro` | 即梦 Seedance 1.0 Pro | 经典版本，价格最低；无声，2～12 秒 | 按分辨率 × 时长计价（积分）：480p 每 5 秒约 12，720p 每 5 秒约 25，1080p 每 5 秒约 55；具体以 price 命令为准 |
| 视频 | `minimax-h3` | MiniMax H3（海螺） | 海螺 H3 视频：运镜和物理效果好，支持首尾帧、多图参考，还能用参考视频 / 参考音频；4～15 秒，768P 或 2K | 按官方价：768P 每秒约 7.4积分、2K 每秒约 11.8积分；提交前会先报价 |
| 音乐 | `suno` | Suno 音乐 | AI 写歌：一句描述生成带人声的完整歌曲（含作词），或用自己的歌词 + 风格作曲；也能出纯音乐。每次出 2 首 | 每次 40积分（一次出 2 首） |
| 语音 | `tts` | 文字转语音（豆包语音合成 2.0） | 把文字念成 mp3：400 多种音色（中文男女声、旁白、角色、有声书、客服，以及英日韩西法等外语），可调语速、用一句话指定语气 | 按字数计费，最少 1 积分 |
| 图片工具 | `upscale` | 图片高清放大 | AI 超分辨率放大，老照片 / 小图变清晰 | 倍数² × 5 + 10积分：2 倍 30，3 倍 55，4 倍 90 |
| 图片工具 | `faceswap` | AI 换脸 | 把一张人脸照片换到底图人物脸上 | 每次 60积分 |
| 图片工具 | `remove-bg` | AI 抠图（去背景） | 一键去掉背景，输出透明底 PNG（RMBG-2.0，发丝级边缘） | 每次 5积分 |

**怎么选**（用户没指定模型时）：
- 通用文生图、海报、带中文字的设计、电商图 → `gpt-image-2.5-flare`（默认 high 画质）；要更精细、文字更准 → `gpt-image-2.5-sunburst`
- 改图、换背景、保持人物 / 商品一致、多图合成、风格迁移 → `nano-banana-pro`，或 `gpt-image-2.5-flare` 带 `--image`
- 艺术插画、概念设计、摄影感大片、要四选一 → `midjourney`
- 2K～3K 高清壁纸、一组风格统一的图、绘本故事书 → `seedream-5`
- 透明底（贴纸、图标、商品抠图） → `gpt-image-2.5-flare --background transparent`；已有图片要去背景 → `remove-bg`
- 视频：默认 `seedance-2.0-fast`（快、便宜、带音效）；效果最好 / 要 30 秒长视频 → `seedance-2.5`；最便宜 → `seedance-2.0-mini`、`seedance-1.0-pro`；用户给了白模动画 / 动作参考 / 运镜参考视频 → Seedance 2.x 加 `--ref-video`；复杂运镜、物理效果、要用参考音频 → `minimax-h3`
- 写歌、配乐、纯音乐 → `suno`
- 文字转语音、配音、旁白、朗读 → `tts`（先 `voices` 挑音色，把几个候选的试听链接给用户听）
- 小图变清晰 → `upscale`；换脸 → `faceswap`

用户点名了模型就用他点的。拿不准参数就跑 `studio models <模型ID>`，会列出全部参数、取值和价格。

## 三、生成

```bash
node <技能目录>/scripts/studio.mjs gen <模型ID> --prompt "提示词" [参数…] [--out 目录]
```

- **参数先问用户，不要自己猜**：生图、生视频（以及音乐、语音等）提交之前，这个模型支持的参数（`studio models <模型ID>` 列出的那些），
  用户没说清楚的都要先问他用哪个值 —— 比如图片尺寸 / 比例、画质、张数，视频时长、比例、分辨率、要不要声音 / 音效、首帧图，语音的音色、语速等，
  可以把可选值和默认值列出来让他选，一次问完。用户明确说「你定」「用默认」「随便」时才按默认值或你的判断来。
- **花积分之前先说清楚**：先用 `studio price <模型ID> [同样的参数]` 算一下，告诉用户「用 X 模型，预计消耗 N 积分」。
  单次预计超过 100 积分（4K / max 画质、长视频、批量）**先问用户确认再提交**；便宜的直接做，结果里说一句花了多少。
  可以加 `--max-cost N` 兜底：预估超过 N 就不提交。
- **参考图、首帧、人脸照片**：`--image` 后面直接写本地文件路径或 http(s) 链接，本地文件会自动上传；要多张就重复写 `--image a.png --image b.jpg`。
- **提示词**：写具体 —— 主体、场景、风格、构图、光线、色调、画面里的文字（用引号标出来）。用户给的需求很短时，你来扩写成一段好的提示词，
  但别改掉他的原意；Midjourney 用英文效果更好（中文会被自动翻译），参数放最后（`--ar 16:9 --v 7`）。长提示词可以写进 .txt 文件，`--prompt 文件路径`。
- **结果**：自动下载到 `--out` 目录（默认当前目录下的 `aihuihua-outputs/`），输出本地路径和在线地址，还有本次消耗和剩余积分。
  把**本地路径和在线链接都给用户**，并按下面「任务完成后的告知」说明消耗；你能看图的话可以打开图片检查一下效果，不满意就调整提示词再来（每次都要花积分，别无限重试）。
- 生图一般 10 秒～3 分钟（GPT Image 2.5 的 max / 4K 和 Sunburst 更久），Bash 超时给到 600000 毫秒。
- 失败（违规内容、上游报错）一般不扣点。提示含敏感词时改提示词再试，同一个违规提示词别反复提交。

### Midjourney 的后续操作

出图后输出里有「MJ 图片 ID」和可用操作。用户要放大第 N 张、出变体、扩图时：

```bash
node <技能目录>/scripts/studio.mjs mj-action --id <MJ图片ID> --action U2
```

| `--action` | 作用 | 积分 |
|---|---|---|
| `U1` | 放大第 1 张 | 2 |
| `U2` | 放大第 2 张 | 2 |
| `U3` | 放大第 3 张 | 2 |
| `U4` | 放大第 4 张 | 2 |
| `V1` | 以第 1 张为基础出 4 张变体 | 8 |
| `V2` | 以第 2 张出变体 | 8 |
| `V3` | 以第 3 张出变体 | 8 |
| `V4` | 以第 4 张出变体 | 8 |
| `zoom1.5` | 画面向外扩 1.5 倍（只对放大后的单图有效） | 8 |
| `zoom2` | 画面向外扩 2 倍（只对放大后的单图有效） | 16 |
| `pan-left` | 向左扩图 | 8 |
| `pan-right` | 向右扩图 | 8 |
| `pan-up` | 向上扩图 | 8 |
| `pan-down` | 向下扩图 | 8 |

操作只在出图后 1 小时内有效。

### 文字转语音：先挑音色

```bash
node <技能目录>/scripts/studio.mjs voices --lang 中文 --gender 男     # 筛选音色，★ 是推荐音色
node <技能目录>/scripts/studio.mjs voices --q 擎苍                     # 按名字搜
node <技能目录>/scripts/studio.mjs gen tts --voice <音色ID> --prompt ./稿子.txt
```

- 每个音色都带**试听链接**（mp3，直接能听，不扣积分）。用户没指定音色时，按用途挑 3～5 个候选，
  **把名字和试听链接一起给用户**让他选；用户说「随便 / 你定」就用默认的擎苍或按场景挑一个。
- 按字数扣积分，先 `price tts --prompt <同样的文本>` 告诉用户预计消耗。结果是 mp3，下载到本地。

## 四、视频（异步任务）

视频提交后要几分钟才出片。`gen` 默认会一直等到出片并下载，**Bash 超时给到 600000 毫秒**；
如果 Bash 先超时了，任务不会丢 —— 任务 ID 在输出里，接着跑：

```bash
node <技能目录>/scripts/studio.mjs task <模型ID> <任务ID>     # 等到出片并下载
node <技能目录>/scripts/studio.mjs task <模型ID> <任务ID> --no-wait   # 只看一眼状态
node <技能目录>/scripts/studio.mjs task                          # 列出最近提交的任务
```

想一次提交多个视频，可以每个都加 `--no-wait`，再逐个 `task` 取结果。**同一个需求不要重复提交**（会重复扣积分），
先用 `task` 查之前那个。视频提交时预扣积分，失败全额退回；Seedance 带参考视频、H3 出片后按实际用量结算，多扣的退回。

## 五、积分不够了：充值

命令返回退出码 3（「积分不足」）或用户说要充值时：

1. `studio whoami` 看余额，`studio buy --list` 列出套餐，**把套餐（价格、积分数）告诉用户，让他选**。
   花钱的事必须用户明确选定套餐，你不要替他决定。技能只消耗积分，和网站的包月会员无关，所以这里只有积分包；
   用户问会员 / 包月，告诉他技能用不上，买积分包就行。
2. 用户选好后下单：

   ```bash
   node <技能目录>/scripts/studio.mjs buy --pkg <套餐ID>
   ```

   会生成微信支付二维码：传一张 PNG 到网上，同时在本地存 PNG / HTML 并尝试在浏览器打开。
   **用户看不到命令输出（会被折叠），二维码必须由你放进回复里让他直接看到**，不要只甩一个文件路径让他自己去开：

   - 输出里有一行 `![微信扫码支付 ¥…](https://…png)`，**把这一行原样、单独一行放进你的回复**（不要包进代码块或引号），
     对话里就会直接显示二维码，用户掏出微信扫就行。
   - 你的环境如果有「把文件/图片发给用户看」的工具（比如 SendUserFile、图片预览、Artifact），再用它把本地 PNG 发一份。
   - 都显示不出来时，才退而求其次：把 HTML 文件路径给用户，并说明浏览器应该已经自动打开了。

   回复里写清金额、积分数、二维码 2 小时内有效。二维码是给人扫的，不要试图自己解读或重画。
3. 用户说付好了（或者直接接着等），Bash 超时给到 330000 毫秒：

   ```bash
   node <技能目录>/scripts/studio.mjs buy --wait --timeout 300
   ```

   成功会打印新的余额，然后回去接着做刚才没做完的生成。超时（退出码 4）就再跑一次 `buy --wait`。

有卡券（卡号 + 卡密）的话直接兑换：`studio redeem --code <卡号> --password <卡密>`

也可以让用户直接去网站充值：https://aihuihua.ai/?buy=points

## 六、查询

```bash
node <技能目录>/scripts/studio.mjs whoami              # 账号和积分余额
node <技能目录>/scripts/studio.mjs history --limit 10  # 最近的作品（图片、视频），带消耗和链接
node <技能目录>/scripts/studio.mjs models --type video # 某一类的全部模型
node <技能目录>/scripts/studio.mjs price <模型ID> …    # 预估价格
```

## 七、每个模型的参数

下面是全部参数，不传就用默认值。`file` 类型的参数都能写本地路径或 URL。

### `gpt-image-2.5-flare` —— GPT Image 2.5 Flare

OpenAI 最新一代生图，速度快、性价比高：文生图、精确改图、多图融合、局部重绘、透明背景

- 没传 --image 是文生图；传 1～10 张 --image 是改图 / 多图参考（保留人物、商品、版式）
- --mask 配合 1 张 --image 做局部重绘：mask 是和原图同尺寸的 PNG，透明区域是要重画的地方
- 中英文提示词都行，能准确渲染图片里的文字（海报、包装、信息图）
- --background transparent 出透明底（需 png 或 webp），做贴纸、图标、抠好的商品图
- **价格**：按画质×尺寸计价，每张参考图 +2积分。1K（auto 与 1024/1536 三种尺寸）：low 4 / medium 6 / high 10 / xhigh 22 / max 50；2048x2048：6 / 8 / 25 / 45 / 100；3840x2160：8 / 12 / 30 / 50 / 110

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--size` | `auto` / `1024x1024` / `1536x1024` / `1024x1536` / `2048x2048` / `3840x2160`，默认 `1024x1024` | 尺寸：自动 / 方图 / 横图 3:2 / 竖图 2:3 / 2K 方图 / 4K 横图 |
| `--quality` | `low` / `medium` / `high` / `xhigh` / `max`，默认 `high` | 画质，越高越精细越慢越贵 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图 / 要改的原图，本地路径或 URL，可传多次 |
| `--mask` | 本地路径或 URL | 局部重绘蒙版（PNG，透明处重画），只能配 1 张 --image |
| `--format` | `png` / `jpeg` / `webp`，默认 `png` | 输出格式 |
| `--background` | `auto` / `transparent` / `opaque`，默认 `auto` | 背景；transparent 透明底 |

```bash
studio gen gpt-image-2.5-flare --prompt "极简风咖啡店开业海报，标题写「晨光咖啡」，暖色调" --size 1024x1536
studio gen gpt-image-2.5-flare --prompt "把背景换成海边日落，人物不变" --image ./photo.jpg --size auto
studio gen gpt-image-2.5-flare --prompt "一只柴犬贴纸，粗描边" --background transparent --quality medium
```

### `gpt-image-2.5-sunburst` —— GPT Image 2.5 Sunburst

GPT Image 2.5 精细版：细节和文字渲染更好、更听话，出图更慢；适合海报、带字设计、产品精修

- 没传 --image 是文生图；传 1～10 张 --image 是改图 / 多图参考（保留人物、商品、版式）
- --mask 配合 1 张 --image 做局部重绘：mask 是和原图同尺寸的 PNG，透明区域是要重画的地方
- 中英文提示词都行，能准确渲染图片里的文字（海报、包装、信息图）
- --background transparent 出透明底（需 png 或 webp），做贴纸、图标、抠好的商品图
- **价格**：按画质×尺寸计价，每张参考图 +2积分。1K（auto 与 1024/1536 三种尺寸）：low 4 / medium 6 / high 10 / xhigh 22 / max 50；2048x2048：6 / 8 / 25 / 45 / 100；3840x2160：8 / 12 / 30 / 50 / 110

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--size` | `auto` / `1024x1024` / `1536x1024` / `1024x1536` / `2048x2048` / `3840x2160`，默认 `1024x1024` | 尺寸：自动 / 方图 / 横图 3:2 / 竖图 2:3 / 2K 方图 / 4K 横图 |
| `--quality` | `low` / `medium` / `high` / `xhigh` / `max`，默认 `high` | 画质，越高越精细越慢越贵 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图 / 要改的原图，本地路径或 URL，可传多次 |
| `--mask` | 本地路径或 URL | 局部重绘蒙版（PNG，透明处重画），只能配 1 张 --image |
| `--format` | `png` / `jpeg` / `webp`，默认 `png` | 输出格式 |
| `--background` | `auto` / `transparent` / `opaque`，默认 `auto` | 背景；transparent 透明底 |

```bash
studio gen gpt-image-2.5-sunburst --prompt "高端护肤品电商主图，产品居中，大理石台面" --image ./product.png --quality xhigh
```

### `gpt-image-2` —— GPT Image 2

上一代 GPT 生图，对话式理解提示词，支持参考图改图；固定价格

- 可传最多 10 张 --image 做参考 / 改图
- 尺寸由模型按提示词自动决定（可以在提示词里写「横版 16:9」）
- **价格**：每张 8积分

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图，本地路径或 URL，可传多次 |

```bash
studio gen gpt-image-2 --prompt "赛博朋克风格的城市夜景，横版 16:9"
```

### `nano-banana-pro` —— Nano Banana Pro（Gemini 3 Pro Image）

Google 的生图 / 改图模型：人物一致性强、换装换背景、多图合成、风格迁移（吉卜力、手办等）

- 可传多张 --image：保持同一个人 / 物体，换场景、换衣服、合成到一张图
- 很适合「把这张照片改成 X 风格」这类编辑
- **价格**：每张 8积分

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图，本地路径或 URL，可传多次 |

```bash
studio gen nano-banana-pro --prompt "把这张照片变成吉卜力动画风格" --image ./me.jpg
studio gen nano-banana-pro --prompt "让图1的人穿上图2的衣服，站在图3的场景里" --image a.jpg --image b.jpg --image c.jpg
```

### `gpt-4o-image` —— GPT-4o 图片（gpt-image-1）

GPT-4o 生图 / 图片编辑，一次可出多张

- --n 一次出 1～10 张，按张计费
- 传 --image 走编辑模式（最多 10 张参考图）
- **价格**：每张 8积分（--n 张数 × 8）

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--n` | 整数 1～10，默认 `1` | 张数 |
| `--size` | `auto` / `1024x1024` / `1536x1024` / `1024x1536`，默认 `auto` | 尺寸 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图 / 要编辑的图 |

```bash
studio gen gpt-4o-image --prompt "水彩风格的小猫插画" --n 2 --size 1024x1024
```

### `seedream-5` —— 即梦 Seedream 5.0（豆包）

字节即梦 / 豆包 Seedream 5.0：2K～3K 高清大图，中文理解好；支持组图（一次多张连贯图）和故事书（分镜 + 文案）

- --mode single 单张；group 组图（--count 1～15 张同一主题、风格统一）；story 故事书（自动写故事 + 每页配图）
- 可传 --image 做参考图（人物 / 风格保持）
- 尺寸都是 2K 级别以上，适合做壁纸、海报、绘本
- **价格**：每张 8积分，组图 / 故事书按实际生成张数计

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--size` | `2048x2048` / `2304x1728` / `1728x2304` / `2560x1440` / `1440x2560` / `2496x1664` / `1664x2496` / `3024x1296`，默认 `2048x2048` | 尺寸：1:1 / 4:3 / 3:4 / 16:9 / 9:16 / 3:2 / 2:3 / 21:9 |
| `--mode` | `single` / `group` / `story`，默认 `single` | 单张 / 组图 / 故事书 |
| `--count` | 整数 1～15 | 组图、故事书的张数 |
| `--image` | 本地路径或 URL，可重复，最多 10 个 | 参考图 |

```bash
studio gen seedream-5 --prompt "未来城市壁纸" --size 2560x1440
studio gen seedream-5 --prompt "小兔子去森林探险的绘本" --mode story --count 6
```

### `midjourney` —— Midjourney

艺术感最强的生图：插画、概念图、摄影风格；一次出 4 张的四宫格，之后可以放大（U）、变体（V）、扩图

- 提示词最好用英文，可以带 MJ 参数放在最后：--ar 16:9（比例）、--v 7 / --niji 6（版本）、--s 250（风格化）、--q 1、--no text、--seed 123、--sref <图片URL>（风格参考）、--cref <图片URL>（人物参考）
- 中文会被自动翻译成英文；参考图直接把图片 URL 放在提示词最前面，和文字用空格隔开
- 出图后用 mj-action 命令：U1～U4 放大单张（2 点），V1～V4 出变体（8 点），zoom1.5 / zoom2、pan-left/right/up/down 扩图；一小时内有效
- **价格**：出图 8积分；U 放大 2；V 变体 8；zoom1.5 8；zoom2 16；pan 扩图 8

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |

```bash
studio gen midjourney --prompt "a cozy cabin in a snowy forest at night, warm light, cinematic --ar 16:9 --v 7"
```

### `upscale` —— 图片高清放大

AI 超分辨率放大，老照片 / 小图变清晰

- --image 传 1 张（本地或 URL），--scale 放大倍数
- **价格**：倍数² × 5 + 10积分：2 倍 30，3 倍 55，4 倍 90

| 参数 | 取值 | 说明 |
|---|---|---|
| `--image` | 本地路径或 URL，**必填** | 要放大的图片 |
| `--scale` | 整数 2～4，默认 `2` | 放大倍数 2～4 |

```bash
studio gen upscale --image ./small.jpg --scale 2
```

### `faceswap` —— AI 换脸

把一张人脸照片换到底图人物脸上

- --image 底图（被换脸的那张，可以是 AI 生成的图）；--face 清晰的正脸照片，别戴眼镜效果更好
- **价格**：每次 60积分

| 参数 | 取值 | 说明 |
|---|---|---|
| `--image` | 本地路径或 URL，**必填** | 底图 |
| `--face` | 本地路径或 URL，**必填** | 人脸照片 |

```bash
studio gen faceswap --image ./poster.png --face ./me.jpg
```

### `remove-bg` —— AI 抠图（去背景）

一键去掉背景，输出透明底 PNG（RMBG-2.0，发丝级边缘）

- --image 传 1 张（本地或 URL）；自动识别人物 / 商品 / 动物等主体，失败不扣点
- **价格**：每次 5积分

| 参数 | 取值 | 说明 |
|---|---|---|
| `--image` | 本地路径或 URL，**必填** | 要抠图的图片 |

```bash
studio gen remove-bg --image ./product.jpg
```

### `seedance-2.5` —— 即梦 Seedance 2.5

最强模型，画面与音效同步生成，最长 30 秒；自带音效 / 配乐，4～30 秒

- 生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）；reference 全能参考（0～9 张 --image，保持人物 / 商品 / 场景）
- 参考视频（白模动画、动作 / 运镜参考）：--ref-video 最多 10 段，合计 ≤30 秒，单段 ≥2 秒，MP4/MOV ≤200MB、24～60fps、480P～4K；传了自动用 reference 方式，可以不传 --image；提示词里用「视频1」「图1」指代
- 分辨率：480p / 720p / 1080p；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）
- 提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查
- 提交时一次扣足点数，失败全额退回；带参考视频时按「输入含视频」单价、输入时长也计费，提交按上限预扣，出片后按实际用量退差额
- **价格**：按分辨率 × 时长计价（积分）：480p 每 5 秒约 53，720p 每 5 秒约 113，1080p 每 5 秒约 278；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 9 个 | 首帧 / 首尾帧 / 参考图 |
| `--ref-video` | 本地路径或 URL，可重复，最多 10 个 | 参考视频（白模 / 动作参考，mp4/mov） |
| `--mode` | `text` / `first` / `frames` / `reference` | 生成方式，不传自动判断 |
| `--resolution` | `480p` / `720p` / `1080p`，默认 `720p` | 分辨率 |
| `--duration` | 整数 4～30，默认 `5` | 时长（秒） |
| `--ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` | 画面比例，文生视频默认 16:9，图生视频默认 adaptive |
| `--audio` | 开关（`--audio` / `--no-audio`），默认开 | 同时生成音效，--no-audio 关掉 |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen seedance-2.5 --prompt "海浪拍打礁石，镜头缓慢推进，日落" --duration 10 --resolution 1080p --ratio 16:9
```

### `seedance-2.0` —— 即梦 Seedance 2.0

全模态能力，支持 1080P 与 4K 输出；自带音效 / 配乐，4～15 秒

- 生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）；reference 全能参考（0～9 张 --image，保持人物 / 商品 / 场景）
- 参考视频（白模动画、动作 / 运镜参考）：--ref-video 最多 3 段，合计 ≤15 秒，单段 ≥2 秒，MP4/MOV ≤200MB、24～60fps、480P～4K；传了自动用 reference 方式，可以不传 --image；提示词里用「视频1」「图1」指代
- 分辨率：480p / 720p / 1080p / 4k；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）
- 提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查
- 提交时一次扣足点数，失败全额退回；带参考视频时按「输入含视频」单价、输入时长也计费，提交按上限预扣，出片后按实际用量退差额
- **价格**：按分辨率 × 时长计价（积分）：480p 每 5 秒约 35，720p 每 5 秒约 74，1080p 每 5 秒约 184，4k 每 5 秒约 375；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 9 个 | 首帧 / 首尾帧 / 参考图 |
| `--ref-video` | 本地路径或 URL，可重复，最多 3 个 | 参考视频（白模 / 动作参考，mp4/mov） |
| `--mode` | `text` / `first` / `frames` / `reference` | 生成方式，不传自动判断 |
| `--resolution` | `480p` / `720p` / `1080p` / `4k`，默认 `720p` | 分辨率 |
| `--duration` | 整数 4～15，默认 `5` | 时长（秒） |
| `--ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` | 画面比例，文生视频默认 16:9，图生视频默认 adaptive |
| `--audio` | 开关（`--audio` / `--no-audio`），默认开 | 同时生成音效，--no-audio 关掉 |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen seedance-2.0 --prompt "让照片里的人转头微笑" --image ./portrait.jpg --resolution 1080p
studio gen seedance-2.0 --prompt "按视频1 的白模动作和运镜，把角色换成图1 的女孩，写实电影质感" --ref-video ./white-model.mp4 --image ./girl.png --duration 5
```

### `seedance-2.0-fast` —— 即梦 Seedance 2.0 Fast

极速推理，效果接近 2.0；自带音效 / 配乐，4～15 秒

- 生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）；reference 全能参考（0～9 张 --image，保持人物 / 商品 / 场景）
- 参考视频（白模动画、动作 / 运镜参考）：--ref-video 最多 3 段，合计 ≤15 秒，单段 ≥2 秒，MP4/MOV ≤200MB、24～60fps、480P～4K；传了自动用 reference 方式，可以不传 --image；提示词里用「视频1」「图1」指代
- 分辨率：480p / 720p；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）
- 提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查
- 提交时一次扣足点数，失败全额退回；带参考视频时按「输入含视频」单价、输入时长也计费，提交按上限预扣，出片后按实际用量退差额
- **价格**：按分辨率 × 时长计价（积分）：480p 每 5 秒约 28，720p 每 5 秒约 60；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 9 个 | 首帧 / 首尾帧 / 参考图 |
| `--ref-video` | 本地路径或 URL，可重复，最多 3 个 | 参考视频（白模 / 动作参考，mp4/mov） |
| `--mode` | `text` / `first` / `frames` / `reference` | 生成方式，不传自动判断 |
| `--resolution` | `480p` / `720p`，默认 `720p` | 分辨率 |
| `--duration` | 整数 4～15，默认 `5` | 时长（秒） |
| `--ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` | 画面比例，文生视频默认 16:9，图生视频默认 adaptive |
| `--audio` | 开关（`--audio` / `--no-audio`），默认开 | 同时生成音效，--no-audio 关掉 |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen seedance-2.0-fast --prompt "一只猫在窗台上打哈欠" --duration 5
studio gen seedance-2.0-fast --prompt "从白天过渡到夜晚" --image ./day.jpg --image ./night.jpg --mode frames
```

### `seedance-2.0-mini` —— 即梦 Seedance 2.0 mini

极致性价比，出片更快；自带音效 / 配乐，4～15 秒

- 生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）；reference 全能参考（0～9 张 --image，保持人物 / 商品 / 场景）
- 参考视频（白模动画、动作 / 运镜参考）：--ref-video 最多 3 段，合计 ≤15 秒，单段 ≥2 秒，MP4/MOV ≤200MB、24～60fps、480P～4K；传了自动用 reference 方式，可以不传 --image；提示词里用「视频1」「图1」指代
- 分辨率：480p / 720p；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）
- 提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查
- 提交时一次扣足点数，失败全额退回；带参考视频时按「输入含视频」单价、输入时长也计费，提交按上限预扣，出片后按实际用量退差额
- **价格**：按分辨率 × 时长计价（积分）：480p 每 5 秒约 18，720p 每 5 秒约 37；带参考视频时参考视频时长也计费（按上限预扣、出片后按实际结算）；具体以 price 命令为准

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 9 个 | 首帧 / 首尾帧 / 参考图 |
| `--ref-video` | 本地路径或 URL，可重复，最多 3 个 | 参考视频（白模 / 动作参考，mp4/mov） |
| `--mode` | `text` / `first` / `frames` / `reference` | 生成方式，不传自动判断 |
| `--resolution` | `480p` / `720p`，默认 `720p` | 分辨率 |
| `--duration` | 整数 4～15，默认 `5` | 时长（秒） |
| `--ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` | 画面比例，文生视频默认 16:9，图生视频默认 adaptive |
| `--audio` | 开关（`--audio` / `--no-audio`），默认开 | 同时生成音效，--no-audio 关掉 |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen seedance-2.0-mini --prompt "产品 360 度旋转展示" --image ./product.png --mode reference --resolution 480p
```

### `seedance-1.0-pro` —— 即梦 Seedance 1.0 Pro

经典版本，价格最低；无声，2～12 秒

- 生成方式（--mode，不传按图片张数自动选）：text 文生视频；first 首帧图生视频（1 张 --image）；frames 首尾帧（2 张 --image，按顺序首帧、尾帧）
- 分辨率：480p / 720p / 1080p；比例：16:9、4:3、1:1、3:4、9:16、21:9，图生视频可用 adaptive（跟随图片）
- 提交后一般 1～10 分钟出片，命令会一直等到出片并下载；--no-wait 只提交，之后用 task 命令查
- 提交时一次扣足点数，失败全额退回
- **价格**：按分辨率 × 时长计价（积分）：480p 每 5 秒约 12，720p 每 5 秒约 25，1080p 每 5 秒约 55；具体以 price 命令为准

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--image` | 本地路径或 URL，可重复，最多 2 个 | 首帧 / 首尾帧 / 参考图 |
| `--mode` | `text` / `first` / `frames` | 生成方式，不传自动判断 |
| `--resolution` | `480p` / `720p` / `1080p`，默认 `720p` | 分辨率 |
| `--duration` | 整数 2～12，默认 `5` | 时长（秒） |
| `--ratio` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` | 画面比例，文生视频默认 16:9，图生视频默认 adaptive |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen seedance-1.0-pro --prompt "樱花飘落的街道" --resolution 480p --duration 5
```

### `minimax-h3` —— MiniMax H3（海螺）

海螺 H3 视频：运镜和物理效果好，支持首尾帧、多图参考，还能用参考视频 / 参考音频；4～15 秒，768P 或 2K

- 文生视频：只写提示词；首帧图生视频：--first；首尾帧：--first + --last（比例自动 adaptive）
- 参考素材（不能和首尾帧混用）：--image 参考图 ≤9 张、--ref-video 参考视频 ≤3 个、--ref-audio 参考音频 ≤3 个
- 提交前先向网站报价，按官方价计费：768P 约 7.4 点/秒，2K 约 11.8 点/秒，参考图超过 5 张每张 +3 点、参考视频按时长另计；结束后按实际用量多退少不补
- 一般 3～15 分钟出片；--no-wait 只提交，之后用 task 命令查
- **价格**：按官方价：768P 每秒约 7.4积分、2K 每秒约 11.8积分；提交前会先报价

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--resolution` | `768P` / `2K`，默认 `768P` | 分辨率 |
| `--duration` | 整数 4～15，默认 `6` | 时长（秒） |
| `--ratio` | `16:9` / `21:9` / `4:3` / `1:1` / `3:4` / `9:16` / `adaptive` | 比例，首尾帧必须 adaptive（自动） |
| `--first` | 本地路径或 URL | 首帧图 |
| `--last` | 本地路径或 URL | 尾帧图（必须同时给 --first） |
| `--image` | 本地路径或 URL，可重复，最多 9 个 | 参考图 |
| `--ref-video` | 本地路径或 URL，可重复，最多 3 个 | 参考视频（mp4） |
| `--ref-audio` | 本地路径或 URL，可重复，最多 3 个 | 参考音频 |
| `--watermark` | 开关（`--watermark` / `--no-watermark`），默认关 | 加 AI 生成水印 |
| `--wait` | 开关（`--wait` / `--no-wait`），默认开 | 等出片并下载，--no-wait 只提交 |

```bash
studio gen minimax-h3 --prompt "镜头环绕人物一周，电影感" --first ./hero.jpg --duration 6
studio gen minimax-h3 --prompt "按参考视频的运镜拍这个产品" --image ./product.png --ref-video ./ref.mp4 --resolution 2K
```

### `suno` —— Suno 音乐

AI 写歌：一句描述生成带人声的完整歌曲（含作词），或用自己的歌词 + 风格作曲；也能出纯音乐。每次出 2 首

- 描述模式：只写提示词（例如「一首关于夏天海边的轻快中文流行歌」），自动作词作曲
- 歌词模式：--lyrics 传歌词文本或歌词文件路径（可用 [Verse] [Chorus] 标段），--style 写风格（例如 "mandopop, female vocal, piano"），--title 歌名
- --instrumental 纯音乐（无人声），用提示词或 --style 描述曲风
- 一般 1～3 分钟出歌，下载为 mp3，同时给出封面图
- **价格**：每次 40积分（一次出 2 首）

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径 | 提示词 |
| `--lyrics` | 文本 | 歌词文本，或歌词文件路径 |
| `--style` | 文本 | 音乐风格 / 标签（英文效果更好） |
| `--title` | 文本 | 歌名 |
| `--instrumental` | 开关（`--instrumental` / `--no-instrumental`），默认关 | 纯音乐 |

```bash
studio gen suno --prompt "一首关于毕业季的中文流行歌，温暖、钢琴"
studio gen suno --lyrics ./lyrics.txt --style "mandopop, female vocal, acoustic guitar" --title "夏夜"
studio gen suno --prompt "适合咖啡店的轻松爵士" --instrumental
```

### `tts` —— 文字转语音（豆包语音合成 2.0）

把文字念成 mp3：400 多种音色（中文男女声、旁白、角色、有声书、客服，以及英日韩西法等外语），可调语速、用一句话指定语气

- --prompt 就是要念的文字（也可以传 .txt 文件路径），一次最多 5000 字，长文会自动分段合成后拼成一个 mp3
- 先用 voices 命令挑音色（可按 --lang --gender --scene --q 筛选，每个音色都附试听链接，试听不扣积分），再用 --voice <音色ID>
- 不传 --voice 默认用「擎苍」（沉稳男声，适合旁白、诗词朗诵）
- --speed 0.5～2 倍速；--instruction 一句话语气，例如「用开心活泼的语气」「用沉稳庄重的语气朗读」
- **价格**：按字数计费，最少 1 积分

| 参数 | 取值 | 说明 |
|---|---|---|
| `--prompt` | 文本或 .txt 文件路径，**必填** | 提示词 |
| `--voice` | 文本 | 音色 ID（voices 命令查） |
| `--speed` | 文本，默认 `1` | 语速倍数 0.5～2 |
| `--instruction` | 文本 | 语气指令（可选） |

```bash
studio voices --lang 中文 --gender 女 --scene 有声阅读
studio gen tts --voice zh_male_dongfanghaoran_uranus_bigtts --prompt ./narration.txt
studio gen tts --voice zh_female_vv_uranus_bigtts --prompt "欢迎来到我的频道！" --speed 1.2 --instruction "用开心活泼的语气"
```


## 八、兜底：直接调网站接口

上面没覆盖到的功能，可以用 `call` 直接调网站接口（自动带登录令牌）：

```bash
node <技能目录>/scripts/studio.mjs call POST /art/v2/api/<接口> --data '{"key":"value"}' [--stream]
```

只在你确定接口和参数时用；会扣积分的接口照样扣。

## 注意

- 生成的内容要遵守网站规则：涉政、色情、暴力等内容会被拦截，多次违规可能被封号。
- 不要把令牌、`~/.aihuihua-studio/` 下的文件内容写进代码、提交记录或回复里。
- 用户问价格就跑 `price` 或 `models`，以脚本输出为准，别凭印象报价。
