---
name: financial-card-video
description: 用 JSON 生成报纸风竖版金融卡片视频 (1080x1920).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [video, ffmpeg, chrome-headless, newspaper-style, finance, compliance]
    related_skills: [narrated-slideshow-video, pillow-frame-video, wechat-article-publishing]
---

# 报纸风金融卡片视频 (通用脱敏版)

把一个 JSON 文件渲染成 1080x1920 竖版 MP4: 报纸风排版 (报头 → 粗红线 → 眉题行 →
头条 → 正文 → 细线 → 关键位 / 指标行 → 页脚免责), Chrome 无头截图, ffmpeg 合成,
内置合规自检 (绿像素检测 / 敏感词扫描 / 免责页脚非空)。

**零业务依赖**: 不 import 任何业务模块, 不读任何业务数据目录, 卡片数量与全部文案
由输入决定。任何金融/研究类内容都可以喂进来, 渲染器本身不认识"标的"是什么。

## When to Use

- 要把一批结构化条目 (观察清单 / 指标卡 / 每日要点) 做成竖版卡片视频
- 要报纸、刊物式的排版风格 (纸底 + 朱红报头 + 细线分隔), 不要圆角卡 / 渐变 / 进度条
- 视频要带逐卡语音或 BGM, 且音画必须严格对齐
- 需要机器可验的合规自检 (禁绿、敏感词、免责声明)

Don't use for:
- 需要横版 / 16:9 或复杂转场 — 本技能只做竖版单屏静态卡 (无动画)
- 需要自动生成配音 — 逐卡音频由外部准备好 (TTS / 录音), 本技能只负责按真实时长对齐
- 动态图表 / 数据可视化动画 — 走别的方案

## Prerequisites

| 依赖 | 说明 |
|---|---|
| Chrome | 无头截图必需。脚本自动探测常见安装路径, 找不到时用 PATH 里的 `chrome`/`chromium` |
| ffmpeg / ffprobe | 合成与时长探测。`ffmpeg -version` 能跑即可 |
| Pillow | 尺寸/配色/绿像素校验。缺失时脚本降级为"跳过像素校验"并打印提示 |

无需任何 API key, 无网络请求。

## Input Format

`examples/sample_cards.json` 是可直接跑通的虚构示例。除 `cards` 外所有字段可选:

```json
{
  "brand": "刊名",                    // 报头刊名 (朱红)
  "mast_side": "副标",                // 报头右侧小字
  "footer": "免责文本",               // 全局页脚 (页面级可覆盖)
  "seconds_per_card": 4.0,            // 无逐卡音频时的单卡秒数
  "bgm": "path/bgm.mp3",              // 背景音乐 (音量 0.10 + 2s fade, 自动循环)
  "cover":  { "headline": "...", "date": "...", "kicker_right": "...",
              "items": [{"no":"01","name":"...","code":"...","price":"..."}],
              "focus_label": "本期看点", "focus_name": "...", "note": "...",
              "audio": "cover.mp3" },
  "cards":  [{ "kicker": "观察标的 01", "title": "标题", "subtitle": "副题/代码行",
               "price_label": "现价", "price": "12.34 元",
               "body": "正文", "keyline_label": "关键位", "keyline": "上方 A / 下方 B",
               "metrics": [{"label":"波动率","value":"58","accent":true}],
               "audio": "card_1.mp3" }],
  "closing": { "headline": "明天见", "text": "...", "audio": "closing.mp3" }
}
```

文案标记 (渲染前先做 HTML 转义, 不会注入标签):

| 写法 | 效果 |
|---|---|
| `**文本**` | 朱红强调 |
| `##文本##` | 加粗数字 (tabular-nums) |
| 换行 | `<br>` |

布局规则: `keyline` 为空 → 整行省略; `metrics` 为空 → 指标行省略; `audio` 缺失或
文件不存在 → 该卡回落 `seconds_per_card` 固定时长。

## How to Run

```bash
python scripts/make_card_video.py --input examples/sample_cards.json --out out.mp4
```

带音频 (示例见下) 和严格合规闸:

```bash
python scripts/make_card_video.py -i cards.json -o out.mp4 \
  --bgm assets/bgm.mp3 --strict --words my_forbidden.txt
```

常用参数:

| 参数 | 作用 |
|---|---|
| `--sec-per-card N` | 无逐卡音频时的单卡秒数 (默认 4.0; JSON 的 `seconds_per_card` 优先) |
| `--pad N` | 有音频时语音结束后的留白 (默认 0.5s) |
| `--bgm PATH` | 背景音乐, 音量 0.10 + 首尾 2s fade |
| `--words FILE` | 敏感词表 (每行一词, `#` 注释); 默认内置通用金融禁词 |
| `--strict` | 命中敏感词直接失败 (退出码 6), 否则只告警 |
| `--template PATH` | 换模板 (默认 `templates/paper_card.html`) |
| `--keep-workdir` | 保留中间 HTML/PNG 便于排查版式 |

退出码: `0` 成功 / `2` 输入问题 / `3` 无 Chrome / `4` 截图失败 / `5` 合成或校验失败 / `6` 敏感词闸。

## Quick Reference

```bash
# 跑通演示
python scripts/make_card_video.py --input examples/sample_cards.json --out demo.mp4

# 用 ffprobe 看规格
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,pix_fmt \
        -of default=noprint_wrappers=1 demo.mp4
```

## Procedure

1. **准备 JSON** — 写出 `cover` / `cards[]` / `closing`, 每个页脚都写明免责文本。
2. **干跑一次** — `--sec-per-card 1 --keep-workdir`, 打开 `page_*.png` 检查版式
   (看有无溢出 / 空行 / 缺字段)。完成判据: 每张 PNG 都是 1080x1920 且元素齐全。
3. **加音频** — 逐卡准备好音频文件, 在 JSON 里写 `audio` 字段 (相对路径以 JSON
   所在目录为基准)。完成判据: 脚本打印的每卡时长 = 该音频真实时长 + `--pad`。
4. **正式合成** — 去掉 `--sec-per-card`, 加 `--bgm` / `--strict` 跑正式产物。
5. **过清单** — 按 `PUBLISH_CHECKLIST.md` 逐项确认后再发布。

## Pitfalls

- **不用 concat demuxer 拼单帧 PNG**。单帧图没有时间基, demuxer 拼出来的时长会塌缩。
  正确做法: 每张图 `-loop 1 -t <秒>` 作为独立输入, 再用 `concat` **filter** 拼接 ——
  这样每张图的停留时长才受控。
- **Chrome 截图必须锁死 5 个参数**: `--user-data-dir=<临时目录>` (不隔离会复用真实
  profile, 并发时被单实例锁卡死)、`--disable-lcd-text` (次像素渲染会在文字边缘产生
  彩色杂点, 含绿边 → 绿像素检测假阳性)、`--force-color-profile=srgb` (不锁则跟随
  显示器色彩配置, 像素不可复现)、`--hide-scrollbars` (滚动条会被截进画面)、
  `--window-size=1080,1920` (视口必须等于成片尺寸, 否则排版错位)。
- **模板区块注释必须独占一行**。解析器按行首/行尾锚定 `<!--#TAG-->`; 若在文件头部
  注释里原样写出该标记, 会被当成区块边界, 整段说明文字会被当成 CSS 渲染到画面上。
- **`VOLUMEDETECT` 要能被看见**: 用 `-v error` 会连 `volumedetect` 的统计一起吞掉,
  排查音量时用 `-hide_banner` 而不是 `-v error`。
- **绿像素检测别用 PIL 的 mode "1" + `logical_and`**: Pillow 对 "1" 模式图的
  `histogram()` 语义跨版本不一致 (12.x 返回 256 桶), 会让检测**恒为 0** —— 一个永远
  通过的合规检查比没有检查更危险。全程保持 "L" 模式, 用 `ImageChops.multiply` 求交集,
  取 `histogram()[255]`。**改了检测逻辑一定要用一张纯绿测试图回归** (见 Verification)。
- **绿像素是设计约束不是bug**: 涨跌一律用朱红 / 灰墨表意; 想加"涨绿"就不要用本模板。
- **BGM 短于成片**: 脚本用 `-stream_loop -1` 循环铺满, 不要再手工裁剪对齐。
- 中文字体依赖系统 `Microsoft YaHei`; 非 Windows 机器请在模板 CSS 里改成可用字体。

## Verification

跑完一次渲染, 脚本自己会打印全部判据, 应当看到:

- `绿像素合计 = 0 (PASS)`
- 每张 PNG `四角纸色偏差 = 0` (纸色 250,247,242 ±3)
- `容器时长 = 各卡之和` (差 ≤ 0.15s)
- 音轨存在时 `max_volume` 不接近 -99dB (不是静音)
- `敏感词命中 = 无`, `页脚缺省回落 = 无`

逐卡音频对齐可再用频域抽查: 对每个卡的期望音, `bandpass` 后取 `mean_volume`,
期望音频明显高于其它频率 (实测差 ~20dB)。

**合规检测器自身也要回归** (否则可能是一个永远通过的假闸)。用一个纯绿测试块跑
`count_green`, 必须得到 >0; 纸色/朱红/金/灰墨必须为 0:

```python
import importlib.util
from PIL import Image
spec = importlib.util.spec_from_file_location("m", "scripts/make_card_video.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
im = Image.new("RGB", (200, 200), (250, 247, 242))
for y in range(50, 150):
    for x in range(50, 150):
        im.putpixel((x, y), (20, 180, 60))
im.save("green_probe.png")
assert m.count_green(Image.open("green_probe.png")) == 10000   # 检测器真的在工作
```

Windows (git-bash) 下注意: `terminal` 里的 `/tmp/x` 传给**原生** Python 会被解释成
`\tmp\x` (盘符根), 需要文件时请用 `$LOCALAPPDATA/Temp/...` 这类原生路径。

## Information Boundary (使用本技能时)

产出物会公开发布, 因此**禁止**把内部信息带进 JSON 或模板: 内部项目/代号名称、
因子命名与评分体系、数据源接口与认证细节、策略参数与阈值、推送渠道与账号、
本机私有绝对路径。示例数据必须完全虚构 (公司名 + 保留位代码)。逐项清单见
`PUBLISH_CHECKLIST.md`。

## Files

```
SKILL.md                  本文件
scripts/make_card_video.py 渲染器 (JSON → MP4, 全部逻辑在此)
templates/paper_card.html  报纸风模板 (区块注释 + {{占位符}})
examples/sample_cards.json 虚构示例数据 (可直接跑通)
PUBLISH_CHECKLIST.md       发布前信息边界审计清单
```
