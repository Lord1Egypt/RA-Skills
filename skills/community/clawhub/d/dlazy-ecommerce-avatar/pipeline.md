# 完整流水线 · 从商品到成片

以"一条 60 秒竖屏带货口播"为例，逐步给出可执行命令。

## 先看成本结构

这决定了你该在哪里省钱。一条 60 秒成片的积分构成：

| 步骤 | 命令 | 积分 |
|---|---|---|
| ① 底图 | `gpt-image-2 --quality high` | 37 |
| ② 脚本 | `claude-sonnet-5` | 个位数 |
| ③ 配音 | `qwen-tts` × 3 段 | 18 |
| ④ **驱动** | `jimeng-omnihuman-1.5` 1080p × 60 秒 | **1380** |
| ⑤ 空镜 | `seedance-2.5` 1080p × 5 秒 × 2 条 | 视档位 |
| 合计 | | **约 1450+** |

**驱动占了 95%。** 结论有两个：

1. 底图那 37 积分**绝对不要省**。用 `seedream-5.0`（8 积分）省下的 29 分，还不够驱动多跑 2 秒。底图差导致重驱动一次，亏 1380。
2. 真要省钱，降 `--resolution 720p`（15 积分/秒，省 35%），或者砍口播时长——把 60 秒压到 40 秒，比任何其他优化都有效。

## ① 底图

从 `recipes.md` 选一条，执行，存到本地长期复用：

```bash
dlazy gpt-image-2 --prompt "<配方 prompt>" \
  --size 2160x3840 --quality high --imageFormat png \
  --batch 4 --save ./avatar/base.png
```

`--batch 4` 并行出 4 张选一张（积分 ×4 = 148）。人脸一次难中，**这个钱值得花一次**——选定后这张脸能用几百条视频。

出图后按 `recipes.md` 的"必须/禁止"表逐条检查再进入下一步。带着一张侧脸图往下走，后面 1380 积分全打水漂。

## ② 脚本

**关键：按 25 秒一段切好。** `jimeng-omnihuman-1.5` 的音频硬上限是 1080p ≤ 30 秒、720p ≤ 60 秒，写完整段才发现要切会打乱语气。

中文口播约 **每秒 4.5 字**，25 秒 ≈ 110 字。（实测 `qwen-tts` 音色 Cherry：29 字出 6.16 秒、45 字出 9.92 秒，合 4.54~4.71 字/秒，按 4.5 估算留有余量。）

```bash
dlazy claude-sonnet-5 --prompt "为这个商品写一条 60 秒抖音带货口播脚本。
商品：<名称/卖点/价格>
要求：
- 切成 3 段，每段严格控制在 110 字以内，段落之间语气连贯可无缝拼接
- 第 1 段：3 秒内抛出痛点或反常识钩子，不要自我介绍
- 第 2 段：讲卖点，要具体数字与使用场景，不要形容词堆砌
- 第 3 段：给价格锚点与行动指令
- 口语化，短句为主，避免书面语和排比句
- 不得出现绝对化用语（最、第一、国家级）与医疗功效暗示
输出格式：三段纯文本，用 --- 分隔，不要任何解释"
```

最后两条要求是合规硬线，别删。

## ③ 配音

`qwen-tts` 的 prompt **上限 512 字符，超出整次请求 400，积分不退**。110 字的分段刚好安全。

`qwen-tts` 的输出是 **WAV 不是 MP3**（响应 URL 后缀为 `.wav`，文件头为 `RIFF/WAVE`）。`--save` 只决定本地文件名，不做转码——存成 `.mp3` 会得到一个扩展名骗人的 WAV 文件，第 ⑥ 步 ffmpeg 装配时按扩展名推断格式就会出错。**存成 `.wav`。**


```bash
dlazy qwen-tts --prompt "<第 1 段文本>" --voice Cherry --save ./audio/seg1.wav
dlazy qwen-tts --prompt "<第 2 段文本>" --voice Cherry --save ./audio/seg2.wav
dlazy qwen-tts --prompt "<第 3 段文本>" --voice Cherry --save ./audio/seg3.wav
```

音色选择：

- `--voice Cherry`（默认，年轻女声，通用带货）
- `--voice Serena` / `Vivian`（成熟女声，适合家居母婴）
- `--voice Ethan` / `Ryan`（男声，适合 3C 商务）
- 全部 38 个系统音色见 `dlazy qwen-tts -h`

要更贴合人设的声音，用设计模式自然语言描述：

```bash
dlazy qwen-tts --generation_mode design \
  --voice_prompt "35岁女性，语速偏快，热情但不聒噪，尾音有轻微上扬" \
  --prompt "<文本>" --save ./audio/seg1.wav
```

中文方言音色也在系统音色里（`Nofish`、`Kiki` 等），做地域性带货可以试。

**三段必须用同一个音色。** 换音色 = 换人，拼起来会很怪。

## ④ 驱动

**先记住一件事：这一步是单点依赖。** dLazy 有 5 个数字人相关模型，但只有 `jimeng-omnihuman-1-5` 接受「静态图 + 音频」：

| 模型 | 输入 | 能否用底图驱动 |
|---|---|---|
| `jimeng-omnihuman-1.5` | `--images` + `--audio` | ✅ 唯一 |
| `videoretalk` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `sync-lipsync-3` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `heygen-lipsync-speed` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `jimeng-dream-actor` | `--images` + `--videos` | ❌ 动作迁移，不吃音频 |

其余四个都是「视频 + 音频」换口型，前提是你**已经有一段人物说话的视频**。所以 omnihuman 一旦不可用（限流、账号 401、上游故障），整条链路就断了——这是本流水线最脆弱的一环。

**降级路径**（成本约为主路径的 2 倍，按需使用）：

```bash
# 1) 底图 → 一段"人在说话"的视频
dlazy seedance-2.5 --input @payload/i2v.json --save ./clips/base.mp4
#    prompt 写：面向镜头自然说话，嘴部有开合动作，头部轻微点头，镜头固定，背景静止

# 2) 该视频 + 你的配音 → 对口型
dlazy videoretalk --video_url ./clips/base.mp4 --audio_url ./audio/seg1.wav --save ./clips/seg1.mp4
```

成本对照（10 秒 720p 竖屏）：omnihuman 直驱 **150 积分**，而 `seedance-2.5` 生成 10 秒就要 **227 积分**，再加 `videoretalk` 的对口型费用。能走主路径就别走这条。

---

每段音频配同一张底图，分别驱动：

```bash
dlazy jimeng-omnihuman-1.5 \
  --images ./avatar/base.png \
  --audio ./audio/seg1.wav \
  --prompt "人物自然口播，轻微点头示意，肩部有细微起伏，手部不做大幅动作" \
  --resolution 1080p \
  --save ./clips/seg1.mp4
```

`--prompt` 上限 **300 字符且可选**。它控制的是**运镜与动作幅度**，不是画面内容——画面已经被底图定死了。有效的写法只有这几类：

| 想要 | 写法 |
|---|---|
| 稳重专业 | `人物自然口播，幅度克制，轻微点头，身体基本不动` |
| 热情带货 | `人物热情口播，语气激动时头部小幅摆动，肩部有明显起伏` |
| 亲和分享 | `人物放松口播，偶尔轻微侧头，表情自然生动` |

**不要写**画面描述（"背景是白色的"）、镜头运动（"镜头推近"）、服装（"穿红色衣服"）——底图已经定了，写了也不生效，还占用 300 字额度。

**它对手部的控制是有限的。** 实测：底图里双手自然下垂、完全不入镜，driving prompt 明确写了「手部不做大幅动作」，omnihuman 仍然自行生成了双手交叠抬到胸前的讲解动作。渲染质量没问题，但**你无法靠 prompt 阻止它加手**。要避免手部出画，只能从底图入手——把画面裁到肩部以下更近的景别，让手根本没有出现的空间。

**输出规格不是标准的 720x1280。** 实测 720p 档出的是 **704x1248 @ 25fps，音频 24000Hz 单声道**，且成片比输入音频长 0.1~0.2 秒（6.16 秒音频出 6.28 秒视频）。这个规格与其它模型都对不上，拼接时必须重编码，详见 ⑥。

三段并行跑省时间（每段约 3 分钟）：

```bash
for i in 1 2 3; do
  dlazy jimeng-omnihuman-1.5 --images ./avatar/base.png \
    --audio ./audio/seg$i.wav --resolution 1080p --no-wait
done
# 各自返回 generateId，再逐个等待
dlazy status <generateId> --save ./clips/seg1.mp4
```

## ⑤ 空镜（B-roll）

带货视频全程一张脸会掉完播率。每 15~20 秒插入 2~3 秒产品画面。

用 D 组配方出的产品图驱动成动态镜头：

```bash
dlazy seedance-2.5 \
  --generation_mode components \
  --images ./broll/16-hold.png \
  --prompt "镜头以极缓慢的速度向产品推近，景深逐渐变浅，背景虚化加深，产品表面的光泽随镜头移动产生细微变化，整体运动平稳无抖动，无人物入画" \
  --ratio 9:16 --resolution 1080p --duration 5 \
  --save ./broll/clip1.mp4
```

`seedance-2.5` 的 prompt 没有严格短上限，运镜描述可以写详细。这里是除底图外第二个提示词有杠杆的地方。

`--ratio 9:16` 必须显式写，默认是 `16:9` 横屏。

## ⑥ 装配

**CLI 不做视频合成。** `dlazy` 是模型调用器，没有 merge / concat 命令。三个选择：

**A. 交给沙箱模板（推荐）** —— 有完整的剪辑、字幕、转场能力：

```bash
dlazy chat --skill product-to-ecommerce-video \
  --prompt "把这些素材剪成一条 60 秒竖屏带货视频：口播片段 seg1~3 顺序拼接，
在第 20 秒和第 40 秒各插入一个 3 秒产品空镜，全片加中文字幕，片尾加价格卡片" \
  --files ./clips/seg1.mp4 ./clips/seg2.mp4 ./clips/seg3.mp4 ./broll/clip1.mp4
```

沙箱会返回一个项目 id，后续用 `dlazy chat --project <id> --prompt "..."` 继续调整。

**B. 自己用 ffmpeg** —— **各模型的输出规格互不相同，必须全重编码**：

先看实测到的规格差异（同一条片子里的三段素材）：

| 来源 | 分辨率 | 帧率 | 音频 |
|---|---|---|---|
| `jimeng-omnihuman-1.5`（口播） | **704x1248** | **25 fps** | 24000Hz **mono** |
| `seedance-2.5`（空镜） | **720x1280** | **24 fps** | 32000Hz **stereo** |

分辨率、帧率、采样率、声道数**四项全不一致**。omnihuman 出的甚至不是标准 720x1280。

所以 `-c copy` 不能用，`-c:v copy` 也不能用——实测拼接时视频流会刷屏 `Non-monotonic DTS`，产物被强行塞进 704x1248 / 24.75fps 的怪异容器。画面本身没花，但时间戳已错位，播放器上会音画不同步。

正确做法是 concat filter 全重编码，把三段统一到同一规格：

```bash
ffmpeg -i clips/talk1.mp4 -i broll/clip1.mp4 -i clips/talk2.mp4 -filter_complex "[0:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v0];[1:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v1];[2:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v2];[0:a]aresample=44100[a0];[1:a]aresample=44100[a1];[2:a]aresample=44100[a2];[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -ar 44100 -ac 2 output.mp4
```

实测结果：零警告，时长 21.44 秒（三段之和 21.46，误差 0.02），输出统一为 720x1280 / 25fps / 44100Hz stereo。**而且体积比 `-c:v copy` 还小一半**（4.8MB vs 9.5MB）——重编码在这里没有代价，只有好处。

段数变化时改三个地方：输入 `-i` 的个数、`[vN]/[aN]` 的编号、`concat=n=` 的数字。
**C. 导入剪映 / CapCut** —— 需要精细控制节奏和贴纸时。

## 一次性跑完的脚本骨架

**中文一律走 JSON 文件，不要用 shell 变量。** 见 `troubleshooting.md` 的"编码陷阱"一节——用 `$(cat ...)` 拼中文 prompt 会静默产生乱码，命令照样返回 `ok: true`，但出来的东西跟你要的毫无关系。

```bash
#!/usr/bin/env bash
set -e
mkdir -p avatar audio clips broll payload

# 底图只做一次，之后注释掉复用
# dlazy gpt-image-2 --input @payload/base.json --save ./avatar/base.png

for i in 1 2 3; do
  # payload/tts$i.json 形如 {"prompt": "<第 i 段文本>", "voice": "Cherry"}
  dlazy qwen-tts --input @payload/tts$i.json --save ./audio/seg$i.wav

  dlazy jimeng-omnihuman-1.5 --images ./avatar/base.png     --audio ./audio/seg$i.wav     --input @payload/drive.json     --resolution 1080p --save ./clips/seg$i.mp4
done

# 三段口播统一规格后拼接（omnihuman 出 704x1248@25fps，与其他模型不一致）
ffmpeg -i clips/seg1.mp4 -i clips/seg2.mp4 -i clips/seg3.mp4 -filter_complex \
"[0:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v0];\
[1:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v1];\
[2:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v2];\
[0:a]aresample=44100[a0];[1:a]aresample=44100[a1];[2:a]aresample=44100[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -ar 44100 -ac 2 output.mp4
```

JSON 文件用 UTF-8 保存（`payload/drive.json` 就一行：`{"prompt": "人物自然口播，轻微点头示意，手部不做大幅动作"}`）。

跑之前先在每条命令后加 `--dry-run` 走一遍，确认参数和积分预估。
