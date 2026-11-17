# 完整流水线 · 从讲义到成片

以"一节 20 分钟横屏课程"为例，逐步给出可执行命令。

## 先定成片形态

动手前先定这个，它决定了成本量级，改起来要重做。

**A. 串行（推荐）** —— 讲师段与课件段前后接续，同一时刻只有一种画面：

```
[讲师 开场 30s] → [课件 正文] → [讲师 转场 10s] → [课件 正文] → … → [讲师 结尾 20s]
```

讲师只需驱动 110 秒 ≈ **2640 积分**。这是知识付费最主流的形态，也是本技能的默认路线。

**B. 全程画中画** —— 课件铺满，讲师小窗常驻右下角：

讲师要驱动满 1200 秒 ≈ **27840 积分**。**10 倍成本**，换来的只是一个六分之一大小的常驻人头。除非甲方明确要求，否则不值。

**C. 局部画中画（折中）** —— 串行为主，只在 2~3 个关键讲解点让小窗出现 30 秒：

比 A 多花约 2000 积分，换来"讲师一直在场"的感觉。做企业内训、需要强讲师存在感时用这条。

下面按 **A** 展开，⑥ 里给出画中画的合成命令（C 用得上）。

## 成本结构

| 步骤 | 命令 | 积分 |
|---|---|---|
| ① 底图 | `gpt-image-2 --quality high` | 37（一门课一次） |
| ① 派生机位 | `gpt-image-2 --images` | 60 × 2（一门课一次） |
| ② 讲稿 | `claude-sonnet-5` | 个位数 |
| ③ 配音 | `qwen-tts` **固定 6 积分/次** | 约 108 |
| ④ **驱动** | `jimeng-omnihuman-1.5` 1080p × 110 秒 | **2530** |
| ⑤ 课件 | `gpt-image-2` 静态板 × N | 37 × N |
| ⑥ 装配 | 沙箱模板 / 自己 ffmpeg | — |
| 单节合计 | | **约 2650** |

底图那 157 积分（37 + 60×2）是**整门课一次性**的，摊到 30 节上每节 5 积分。

**驱动占 95%。** 所以省钱只有一个方向：**砍露脸时长**，不是砍画质。

## ① 底图

从 `recipes.md` 选一条，先出正文主力机位（配方 11），再派生另外两个机位：

```bash
# 主力机位：右三分之一构图，左侧留给课件
dlazy gpt-image-2 --input @payload/base.json --batch 4 --save ./lecturer/11-third.png

# 从它派生开场/结尾用的全画幅（保住同一张脸）
dlazy gpt-image-2 --images ./lecturer/11-third.png --input @payload/derive-full.json \
  --save ./lecturer/12-full.png
```

`--batch 4` 并行出 4 张选一张（积分 ×4 = 148）。**人脸一次难中，这个钱值得花一次**——选定后这张脸要用几十节课。

出图后按 `recipes.md` 末尾的检查清单逐项过再往下走。带着一张不合格的底图，后面每一节课的驱动积分都是白花的。

## ② 讲稿

**关键：露脸段和正文段用两种切法。** 这是课程版最容易做错的一步。

| | 切法 | 为什么 |
|---|---|---|
| 露脸段 | **110~130 字一段** | 受 omnihuman 的 30 秒硬上限约束 |
| 正文段 | **写满 500 字符** | 不驱动，无时长约束；TTS 固定 6 积分/次，写满省钱 |

中文口播约 **每秒 4.5 字**（实测 `qwen-tts` 为 4.54~4.71 字/秒），130 字 ≈ 29 秒，卡在 30 秒上限内安全。

```bash
dlazy claude-sonnet-5 --prompt "为这门课的第 3 节写讲稿。
主题：<本节主题>
时长：20 分钟，共 6 个章节
输出三类文本，用 === 分隔：
1. 开场白：110 字以内，抛出本节要解决的问题，不要自我介绍和寒暄
2. 章节转场 × 6：每条 45 字以内，承上启下，点出下一章要讲什么
3. 正文讲解 × 6：每章一段，每段严格控制在 480 字以内（含标点），
   语言口语化可直接朗读，有具体例子和数字，避免书面语和排比句
4. 结尾总结：90 字以内，收束要点并给出下一节的钩子
合规要求：不得出现升学率、通过率、保过、包会等承诺性表述，
不得虚构任何机构背书、职称或从业资质
输出纯文本，不要任何解释"
```

最后那条合规要求是硬线，别删——原因见 `troubleshooting.md` 的"教培合规红线"。

## ③ 配音

`qwen-tts` 的 prompt **上限 512 字符，超出整次请求 400，积分不退**。

`qwen-tts` 的输出是 **WAV 不是 MP3**（响应 URL 后缀为 `.wav`，文件头为 `RIFF/WAVE`）。`--save` 只决定本地文件名，不做转码——存成 `.mp3` 会得到一个扩展名骗人的 WAV 文件，第 ⑥ 步 ffmpeg 装配时按扩展名推断格式就会出错。**存成 `.wav`。**


```bash
# 露脸段（短，受驱动时长约束）
dlazy qwen-tts --input @payload/tts-open.json  --save ./audio/open.wav
dlazy qwen-tts --input @payload/tts-trans1.json --save ./audio/trans1.wav

# 正文段（写满 500 字符，一次调用顶四次）
dlazy qwen-tts --input @payload/tts-body1.json --save ./audio/body1.wav
```

`payload/tts-open.json` 形如：

```json
{ "prompt": "<文本>", "voice": "Cherry" }
```

音色选择：

- `--voice Cherry`（默认，年轻女声）
- `--voice Serena` / `Vivian`（成熟女声，适合人文、管理类）
- `--voice Ethan` / `Ryan`（男声，适合技术、商业类）
- 全部系统音色见 `dlazy qwen-tts -h`

要更贴合人设的声音，用设计模式自然语言描述：

```bash
dlazy qwen-tts --generation_mode design \
  --voice_prompt "40岁男性，语速平稳偏慢，讲课语气，重点处有自然停顿，不夸张" \
  --prompt "<文本>" --save ./audio/open.wav
```

**整门课必须用同一个音色。** 不只是同一节课——第 5 节换了声音，等于换了老师。把音色 id 写进项目配置文件，别靠记忆。

课程配音比带货要**慢**。带货求煽动，课程求听得清。设计模式里写"语速平稳偏慢"比默认语速更适合教学。

## ④ 驱动

**只驱动露脸段。** 正文段没有讲师画面，跳过这一步——这就是省下 90% 积分的地方。

**这一步是单点依赖。** dLazy 有 5 个数字人相关模型，只有 `jimeng-omnihuman-1.5` 接受「静态图 + 音频」：

| 模型 | 输入 | 能否用底图驱动 |
|---|---|---|
| `jimeng-omnihuman-1.5` | `--images` + `--audio` | ✅ 唯一 |
| `videoretalk` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `sync-lipsync-3` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `heygen-lipsync-speed` | `--video_url` + `--audio_url` | ❌ 要现成视频 |
| `jimeng-dream-actor` | `--images` + `--videos` | ❌ 动作迁移，不吃音频 |

它一挂整条链路就断。降级路径是「i2v 生成说话视频 → videoretalk 对口型」，成本翻倍，能走主路径就别走。

```bash
# 开场：全画幅机位
dlazy jimeng-omnihuman-1.5 \
  --images ./lecturer/12-full.png \
  --audio ./audio/open.wav \
  --input @payload/drive.json \
  --resolution 1080p \
  --save ./clips/open.mp4

# 章节转场：偏侧机位，可降 720p 省钱
dlazy jimeng-omnihuman-1.5 \
  --images ./lecturer/11-third.png \
  --audio ./audio/trans1.wav \
  --input @payload/drive.json \
  --resolution 720p \
  --save ./clips/trans1.mp4
```

`--prompt` 上限 **300 字符且可选**（`payload/drive.json` 里就一行）。它控制的是**运镜与动作幅度**，不是画面内容——画面已被底图定死。课程场景的有效写法：

| 想要 | 写法 |
|---|---|
| 讲课标准态 | `人物自然讲解，幅度克制，偶尔轻微点头，身体基本不动` |
| 开场问候 | `人物微笑讲话，开场有轻微的点头示意，表情自然亲和` |
| 强调重点 | `人物讲解语气加重时头部小幅前倾，眼神专注` |

**不要写**画面描述、镜头运动、服装——底图已经定了，写了不生效还占额度。

**它对手部的控制有限。** 实测（带货版）：底图双手完全不入镜、prompt 明确写了"手部不做大幅动作"，omnihuman 仍自行生成了双手抬到胸前的讲解动作。要避免只能从底图的景别入手，靠 prompt 挡不住。

**`fast_mode` 参数**：`jimeng-omnihuman-1.5` 有 `--fast_mode` 开关（默认 false）。计费逻辑只看 `resolution` 不看它（源码核对），所以开了**不涨价也不降价**，是纯粹的速度/质量取舍。一节课要跑十几段时值得试一次对比效果。

批量跑（一节课有 8 段露脸），用 `--no-wait` 并发发出：

```bash
for seg in open trans1 trans2 trans3 trans4 trans5 trans6 end; do
  dlazy jimeng-omnihuman-1.5 --images ./lecturer/11-third.png \
    --audio ./audio/$seg.wav --resolution 720p --no-wait
done
# 各自返回 generateId，再逐个取回
dlazy status <generateId> --save ./clips/open.mp4
```

**第一次跑完，先探一下输出规格**（各模型规格互不相同，⑥ 要用）：

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 ./clips/open.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of csv=p=0 ./clips/open.mp4
```

带货版实测竖屏 720p 档出的是 **704x1248 @ 25fps / 24000Hz 单声道**（不是标准 720x1280），且成片比输入音频长 0.1~0.2 秒。**横屏档的实际输出尺寸尚未实测**，第一次跑完务必自己探一次，把结果填进 ⑥ 的命令里。

## ⑤ 课件

正文那 18 分钟的画面主体。三条路，按精度需求选：

**A. `file-to-video` 模板（推荐）** —— 已有 PPT / Word / PDF 讲义时，直接解析成带旁白和字幕的课件视频：

```bash
dlazy chat --skill file-to-video \
  --prompt "把这份讲义做成 18 分钟的课程视频，六个章节，
每章配旁白和字幕，风格克制专业，用深墨蓝配琥珀的双色系统，
章节之间加过渡卡，不要花哨转场" \
  --files ./讲义.pptx
```

它内部走 Remotion，**文字是真排版不是生图**，中文清晰可控可改。

**B. 静态板 + Remotion 排版** —— 没有现成讲义时，用 `recipes.md` D 组出背景板，文字在 Remotion 里排：

```bash
dlazy gpt-image-2 --input @payload/chapter.json --save ./slides/ch1.png
```

**C. `math-explainer-video` 模板** —— 公式推导、定理可视化类课程，KaTeX 排公式 + SVG 画图：

```bash
dlazy chat --skill math-explainer-video --prompt "把贝叶斯公式的推导做成 3 分钟动画讲解"
```

**永远不要让生图模型写课件上的字。** 中文必然乱码，英文经常拼错，而且改一个字就要重出整张图。生图只负责背景和意象，文字交给 Remotion。

## ⑥ 装配

**CLI 不做视频合成。** `dlazy` 是模型调用器，没有 merge / concat 命令。

**下面的 ffmpeg 命令均已本地实跑验证**（用 lavfi 造的规格不一致素材：1248x704@25fps/24000Hz mono 的讲师段 + 1920x1080@30fps/44100Hz stereo 的课件段），语法和规格统一逻辑确认可用。真实素材的规格请按 ④ 末尾探到的实际值替换。

### 串行拼接（形态 A）

**各段规格互不相同，必须全重编码。** `-c copy` 和 `-c:v copy` 都不能用——带货版实测过，视频流会刷屏 `Non-monotonic DTS`，产物被塞进错误的容器，画面不花但音画不同步。

```bash
ffmpeg -i clips/open.mp4 -i slides/body1.mp4 -i clips/trans1.mp4 -filter_complex \
"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v0];\
[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v1];\
[2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25[v2];\
[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0];\
[1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1];\
[2:a]aformat=sample_rates=44100:channel_layouts=stereo[a2];\
[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
-c:a aac -ar 44100 -ac 2 lesson.mp4
```

实测结果：零警告，三段 6 + 10 + 4 秒拼出 **20.04 秒**（误差 0.04），输出统一为 1920x1080 / 25fps / 44100Hz stereo。

**用 `aformat` 不要用 `aresample`。** `aresample=44100` 只统一采样率，不统一声道数——讲师段是单声道、课件段是立体声，混着送进 `concat`。ffmpeg 7.0 实测能自动协商跑通，但这是版本行为，不保险。`aformat=sample_rates=44100:channel_layouts=stereo` 把两项都显式钉死，两种写法输出完全一致，没有理由用前者。

段数变化时改三处：输入 `-i` 的个数、`[vN]/[aN]` 的编号、`concat=n=` 的数字。

### 画中画（形态 C）

课件铺满，讲师小窗叠在右下角。

**矩形小窗**（推荐，最稳）：

```bash
ffmpeg -i slides/body2.mp4 -i clips/talk2.mp4 -filter_complex \
"[1:v]scale=480:-2,setsar=1[pip];[0:v][pip]overlay=W-w-48:H-h-48:shortest=1[v]" \
-map "[v]" -map 1:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
-c:a aac -ar 44100 -ac 2 pip.mp4
```

**`shortest=1` 不能省。** 实测：讲师视频 6 秒、课件 10 秒，不加这个参数输出会是 10 秒——后 4 秒讲师小窗**定格成一张照片**（overlay 默认 `repeatlast=1`），音轨同时静音，看起来像播放器卡死。加上后输出 6.02 秒，跟随讲师段结束。

`-map 1:a` 取讲师的音频（画中画时是讲师在讲）。`scale=480:-2` 的 `-2` 让高度按比例自适应并保持偶数（libx264 要求）。

**圆形小窗**（更像课程直播，实测可用）：

```bash
ffmpeg -i slides/body2.mp4 -i clips/talk2.mp4 -filter_complex \
"[1:v]scale=360:360:force_original_aspect_ratio=increase,crop=360:360,setsar=1,format=rgba,\
geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(gt(pow(X-W/2,2)+pow(Y-H/2,2),pow(W/2,2)),0,255)'[pip];\
[0:v][pip]overlay=W-w-48:H-h-48:shortest=1[v]" \
-map "[v]" -map 1:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
-c:a aac -ar 44100 -ac 2 pip_circle.mp4
```

`geq` 逐像素算 alpha，**比矩形版慢得多**。长视频建议先用矩形版对好时间轴，最后再换圆形出一次。

圆形裁切要求底图下巴留足余量，否则圆一裁下巴就没了——这是 `recipes.md` 配方 13 存在的原因。

### 或者交给沙箱模板

需要字幕、章节标题、转场动画时，比手写 ffmpeg 省事：

```bash
dlazy chat --skill file-to-video \
  --prompt "把这些素材装配成一节 20 分钟的课程视频：open.mp4 开场，
之后六个章节的课件段与转场讲师段交替，end.mp4 结尾，全片加中文字幕，
章节开头加标题卡" \
  --files ./clips/*.mp4 ./slides/*.mp4
```

沙箱返回项目 id，后续用 `dlazy chat --project <id> --prompt "..."` 继续调整。

## 一次性跑完的脚本骨架

**中文一律走 JSON 文件，不要用 shell 变量。** 见 `troubleshooting.md` 的"编码陷阱"——用 `$(cat ...)` 拼中文 prompt 会静默产生乱码，命令照样返回 `ok: true`，出来的东西跟你要的毫无关系。

```bash
#!/usr/bin/env bash
set -e
mkdir -p lecturer audio clips slides payload

# 底图整门课只做一次，做完注释掉
# dlazy gpt-image-2 --input @payload/base.json --batch 4 --save ./lecturer/11-third.png
# dlazy gpt-image-2 --images ./lecturer/11-third.png --input @payload/derive-full.json --save ./lecturer/12-full.png

# 露脸段：配音 + 驱动
for seg in open trans1 trans2 trans3 trans4 trans5 trans6 end; do
  dlazy qwen-tts --input @payload/tts-$seg.json --save ./audio/$seg.wav
done

dlazy jimeng-omnihuman-1.5 --images ./lecturer/12-full.png \
  --audio ./audio/open.wav --input @payload/drive.json \
  --resolution 1080p --save ./clips/open.mp4

for seg in trans1 trans2 trans3 trans4 trans5 trans6; do
  dlazy jimeng-omnihuman-1.5 --images ./lecturer/11-third.png \
    --audio ./audio/$seg.wav --input @payload/drive.json \
    --resolution 720p --save ./clips/$seg.mp4
done

dlazy jimeng-omnihuman-1.5 --images ./lecturer/12-full.png \
  --audio ./audio/end.wav --input @payload/drive.json \
  --resolution 1080p --save ./clips/end.mp4

# 正文段：写满 512 字符，一次调用顶四次
for i in 1 2 3 4 5 6; do
  dlazy qwen-tts --input @payload/tts-body$i.json --save ./audio/body$i.wav
done

# 课件与装配交给沙箱模板（CLI 不做合成）
echo "露脸段与配音已就绪，接下来跑 ⑤ 与 ⑥"
```

所有 JSON 用 **UTF-8** 保存。`payload/drive.json` 就一行：

```json
{ "prompt": "人物自然讲解，幅度克制，偶尔轻微点头，身体基本不动" }
```

跑之前先在每条命令后加 `--dry-run` 走一遍，确认参数和积分预估。一节课十几次驱动调用，参数写错一个字母就是几百积分。
