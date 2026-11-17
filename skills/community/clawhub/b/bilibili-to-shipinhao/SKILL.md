---
name: bilibili-to-shipinhao
description: 把B站横屏中长视频(读书解读/知识类)自动改造为微信视频号9:16竖屏短视频切片。当用户说"B站视频转视频号""横屏转竖屏切片""读书视频切片""视频号短视频制作""横屏改竖屏"时使用。覆盖下载→转写→选段→横转竖→烧字幕→封面全流程, 含本机环境坑与画质/字幕优化。
agent_created: true
slug: bilibili-to-shipinhao
displayName: B站横屏视频转视频号竖屏切片
version: 1.0.0
category: communication
visibility: public
license: MIT
---

# B站横屏视频 → 微信视频号竖屏切片

把 B 站 16:9 中长视频(20-40分钟读书解读/知识类)改造成 1-5 条 1-3 分钟 9:16 竖屏短视频。
已在本机 4 核 CPU + 16GB 内存上跑通两个样例:
- BV1TFe56uEnJ《马斯克: 重回太空》31 分钟(动态画面) → 5 条切片
- BV1g8aa6REa1《学会提问》21 分钟(静态幻灯片+内嵌字幕) → 1 条切片, 全流程约 8 分钟

## 何时使用

- 用户要把 B 站/其他横屏长视频搬运或改造到微信视频号、抖音、快手
- 需要"横转竖 + 切片 + 烧字幕 + 封面"这套组合拳
- 用户问"横屏视频能不能直接发视频号"(不能, 必须改造)

## 环境准备(一次性)

**Python**(managed): `C:/Users/DELL/.workbuddy/binaries/python/versions/3.13.12/python.exe`
该环境已有 yt-dlp 2026.08.19、faster-whisper、Pillow、imageio-ffmpeg。

**ffmpeg**: scoop 装的常是空壳 shim(报 `Could not create process`)。用 imageio-ffmpeg 自带的二进制:
```bash
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
# 复制为 ./bin/ffmpeg.exe —— 文件名必须叫 ffmpeg.exe, 否则 yt-dlp 的 --ffmpeg-location 认不出
mkdir -p bin && cp "<上面输出的路径>" bin/ffmpeg.exe
./bin/ffmpeg.exe -version   # 必须真跑一次验证
```

**本机有系统代理(`http://127.0.0.1:12902`), HF 相关脚本一律设 `HF_HUB_OFFLINE=1`**
不设离线时 huggingface_hub 会走代理去校验/拉模型, 表现为两种随机故障:
`ProxyError: 502 Bad Gateway`(加载直接失败) 或
`RuntimeError: mkl_malloc: failed to allocate memory`(加载到一半分配失败, 极易误判成内存不足)。
设了 `HF_HUB_OFFLINE=1` 后只读本地缓存: small 加载 5s、97s 音频转写 44s, 稳定可复现。
**排查顺序**: 遇到上面两个错误先加离线模式, 不要先去查内存或换模型。

## 五步流程

### 1. 下载(B站 DASH 分离流, 需 ffmpeg 合并)
```bash
python -m yt_dlp -F "<URL>"          # 先看格式 ID
python -m yt_dlp -f "bv*[height<=720]+ba/b" --ffmpeg-location bin \
  -o "download/src.mp4" --merge-output-format mp4 "<URL>"
```
- 通用选择器 `bv*[height<=720]+ba/b` 比写死 `30064+30280` 更稳(不同稿件格式 ID 会变)
- 1080P 通常需大会员; 720P(约 29MB / 26s 下完)对本流程足够
- 合并后会删中间流, 受控环境会被 safe-delete hook 拦 → 子进程 env 设 `CODEBUDDY_SAFE_DELETE_ENABLED=0`
- **B站字幕拿不到**: yt-dlp 报需登录; 直接调 `player/wbi/v2`(带 wbi 签名)也返回 `subtitles=[]`。
  DownKyi 能拿到是因为它带登录态。没有登录态就走 whisper 转写。
- 频道批量选题: `yt_dlp --flat-playlist --print "%(id)s|%(duration)s|%(title)s" "https://space.bilibili.com/<mid>/video"`
  只给 ID 不给标题/时长; 逐个 `--skip-download --print "%(id)s|%(duration)s|%(title)s"` 补元数据。
  直接打 `api.bilibili.com/x/space/arc/search` 容易吃 `-799 请求过于频繁`。

### 1.5 抽帧探形态(30 秒, 决定后面字幕怎么处理)
```bash
bin/ffmpeg.exe -y -ss 300 -i download/src.mp4 -frames:v 1 -q:v 2 download/probe.png
```
看清两类源片:
- **动态画面**(口播/实拍/动画) → 走默认: 源画面居中 + 外烧字幕
- **静态幻灯片/图文轮播 + 画面内嵌字幕** → 必须处理重复问题, 见下节
再跑 `scripts/probe_subs_band.py` 量出"内嵌字幕带"的像素行范围。

### 2. 提音频
```bash
bin/ffmpeg.exe -i download/src.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 download/src.wav
```

### 3. 两段式转写(关键性能策略)
4 核 CPU 上 small 模型转写全片 20-30 分钟音频要半小时以上, 所以分两步:

**① 全片用 tiny 快速转写 + 生成 30 秒分块预览**(只为选段):
```bash
python scripts/transcribe_full.py download/src.wav download/src_transcript.json download/preview_30s.txt
# 21分钟音频 -> 5分34秒(3.84x 实时), 651 段 / 43 块, 预览约 1 万字, 供主 agent 通读
```
tiny 有错字和繁体, 但足够判断内容结构。想看精确边界时再从 JSON 里打区间:
```python
for s in js:
    if 1040 <= s['start'] <= 1200: print(s['start'], s['text'])
```

**② 只精转选中的片段**(用 small, 简体引导 + 内存降级):
```bash
python scripts/transcribe_clips.py     # 改脚本里的 CLIPS 时间戳
```
- `initial_prompt="以下是普通话的句子，请使用简体中文输出。"` 这句能显著减少繁体
- 实测: 97 秒音频 → 44 秒转完, 33 段, 简体, 质量明显优于 tiny
- small 还会自动纠正 tiny 的错(如 tiny 的"904的人/你而" → small 的"94%的人/尼尔")
- 异常时脚本按 `small beam1 → small beam5 → tiny` 逐级降级

### 4. LLM 选段(这步由主 agent 做, 是流水线最值钱的环节)
读 30 秒分块预览, 选 1-3 分钟片段, 优先这几类:
- **决策转折**: 有戏剧性的临场改变(如"凌晨电话把5台发动机改9台")
- **可落地干货**: 反常识数字对比(如"300万设备8.6万从废品站淘, 波音花3.75亿")
- **情绪爆点**: 全书高潮(如"火箭落地那刻全员以为炸了")
- **反常识钩子**: 一句能立住的颠覆性判断(如"统计数据看起来最科学, 但它经常撒谎")
- **金句升华**: 适合收尾(如"多考察这些论据的来龙去脉")
避免选需要上下文铺垫的段落——切片是独立观看的。
时间戳要卡在**句子边界**(用第 3 步的区间打印确认), 不要在句子中间切。

### 5. 切片 + 横转竖 + 烧字幕 + 封面
```bash
python scripts/fix_terms.py                    # 先修专名+半角标点
python scripts/slice_vertical.py               # 默认: 裁源内嵌字幕带 + 模糊背景 + 烧字幕
python scripts/slice_vertical.py --no-crop --tag _原样   # 技能原样, 用于对比
python scripts/make_cover.py                   # 竖屏封面(改 __main__ 里的书名/金句)
```
横转竖用**模糊背景填充**(不是加黑边——黑边会被算法判为低质搬运):
```
crop=iw:ih-{DROP_BOTTOM}:0:0,          # 可选: 先裁掉源内嵌字幕带
split=2[bg][fg];
[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.06[bgout];
[fg]scale=1080:-2[fgout];
[bgout][fgout]overlay=(W-w)/2:(H-h)/2,subtitles='{srt}':force_style='FontSize=12,FontName=Microsoft YaHei,Outline=2,Alignment=2,MarginV=38,...'
```
字幕样式依据: libass 默认按 PlayResY=288 缩放 force_style, **实际像素 = 值×1920/288≈6.7 倍**——
FontSize=12→约80px, MarginV=38→距底约253px, 正好落在下方模糊区, 不挡内容。
封面用 PIL 生成 1080×1920, **关键信息放中间 60% 安全区**(视频号会裁上下)。

## 静态幻灯片/图文轮播源: 解决字幕重复

这类源片(读书号很常见)是**一张静态书封 + 画面底部一行内嵌字幕**。若照默认烧外字幕,
一屏会出现两套字幕。处理顺序:

1. **量内嵌字幕带位置**(不要目测):
   ```bash
   python scripts/probe_subs_band.py download/src.mp4 24
   # 输出: 内容带 y ∈ [396, 531] 最多 24/24 帧命中
   #       内容带 y ∈ [605, 639] 最多 20/24 帧命中   <- 这条就是内嵌字幕带
   ```
   原理: 采 24 帧, 跳过左上角频道水印, 统计底部各行与背景色的差异像素数。
2. **设 `slice_vertical.py` 的 `DROP_BOTTOM`**(1280×720 基准, 单位像素):
   `DROP_BOTTOM = 120` → 裁掉 y≥600, 内嵌字幕带(605-639)整体消失, 而画面内容止于 531 不受影响。
   裁剪后源变 1280×600, 居中占 y∈[707,1213], 下方模糊区更宽, 字幕更好放。
3. **不要用"干脆不烧字幕"**(旧方案): 内嵌字幕是 720P 里的 ~30px 小字, 缩到 1080 宽后仅约 25px,
   手机上看不清。**裁源 + 烧自己的大字幕**才是正解。
4. 裁多少由第 1 步实测值决定, 换视频要重量。

## 关键坑(血泪清单)

| 坑 | 症状 | 解法 |
|---|---|---|
| **系统代理劫持 HF** | `ProxyError: 502 Bad Gateway` 或 `mkl_malloc: failed to allocate memory` | **`HF_HUB_OFFLINE=1`**(只读本地缓存)。先试这个, 再谈内存 |
| HF xet 后端 | `cas-server.xethub.hf.co 401` | `HF_HUB_DISABLE_XET=1` |
| Windows symlink | 模型下完了但 `model.bin is incomplete` / snapshot 0 字节 | `HF_HUB_DISABLE_SYMLINKS=1` + 删掉 0 字节文件重建(blob 保留, 不用重下) |
| 模型下载卡死 | `.incomplete` 文件停在整 40MB 不动 | 弃用该模型, 换本地已完整的(如 small 928MB 完整可用) |
| 模型下载慢 | — | `HF_ENDPOINT=https://hf-mirror.com` |
| ffmpeg shim | `Could not create process` | 用 imageio-ffmpeg 二进制, 改名 ffmpeg.exe |
| ffmpeg 路径 | subtitles 滤镜报找不到文件 | Windows 路径要转义 `:` → `\:` |
| 4核CPU太慢 | small 全片 30 分钟跑不完 | 两段式: tiny 选段 + small 只精转选中段 |
| whisper 出繁体 | 字幕是繁体 | `initial_prompt` 引导简体(无登录态拿不到源字幕) |
| 专名音译错 | 猎鹰→列英, 梅林→美林, 尼尔→您而, 论据→论句 | `fix_terms.py` 术语表(长词优先, 按主题分组) |
| 半角标点 | 字幕里出现 `,` `?` | `fix_terms.py` 的 `PUNCT` 归一化为 `，？` |
| 源视频自带字幕 | 外烧字幕与画面内文字重复 | 抽帧 + `probe_subs_band.py` 定量, 再 `DROP_BOTTOM` 裁掉源字幕带 |
| 字幕巨大+挡画面 | force_style FontSize=20 渲染成 130px+ 大字压在源画面上 | libass 按 PlayResY=288 缩放(×6.7); 用 FontSize=12 + MarginV=38 把字幕放进下方模糊区 |
| 后台任务无输出 | 跑十几分钟没结果, 无法判断是慢还是卡 | 用 `python -u` 且**不接 `grep/tail` 管道**(会缓冲到进程结束) |

## 复用入口(换一个视频怎么做)

1. 下载 → `-o download/src.mp4`(文件名统一, 后面脚本都按这个路径写死)
2. 提音频 → `download/src.wav`; 抽帧 + `probe_subs_band.py` 定 `DROP_BOTTOM`
3. `scripts/transcribe_full.py download/src.wav ...` 出预览 → 主 agent 读预览选段
4. `scripts/transcribe_clips.py` 的 `CLIPS` 填 `(序号, 起, 止, 标题)`
5. `scripts/fix_terms.py` 的 `TERMS` 按新主题**新增一组**(社科/财经/人物…, 长词排前)
6. `scripts/slice_vertical.py` 的 `CLIPS` 填 `(起, 止, 标题, 封面金句)` + `DROP_BOTTOM`
7. `scripts/make_cover.py` 的 `__main__` 改书名/金句/序号总数
8. 重跑: `fix_terms.py` → `slice_vertical.py` → `make_cover.py`
9. 抽帧验收: `bin/ffmpeg.exe -ss <秒> -i output/clip1_*.mp4 -frames:v 1 verify.png`

诊断工具: `scripts/bench_transcribe.py <model> <beam> <wav> [threads]` —— 单模型计时+首段文本, 用来快速定位转写异常。

## 视频号发布提醒(人工环节, 无法自动化)

- **真人片头必须自己录**(哪怕只 5 秒)——纯图文/无真人会被判低质限流, 200-500 播放封顶
- 视频号**没有对个人开放的发布 API**, 上传只能手动
- 竖屏 9:16 完播率比横屏高约 27%; 前 3 秒必须有钩子
- 千万别留微信号/外链; 口播引导"完整版看主页"是安全的
