#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用"报纸风金融卡片视频"渲染器 — 零业务依赖。

输入: 一个 JSON 文件 (结构见下), 输出: 1080x1920 竖版 MP4 (H.264/yuv420p,
可选音轨)。卡片数量、字段内容全部由输入决定, 渲染器不硬编码任何行业概念。

流程:
    JSON → HTML (报纸风模板, 占位符替换) → Chrome 无头截图 (每卡一张 PNG 1080x1920)
         → (可选) 逐卡音频, ffprobe 读真实时长 → ffmpeg concat 合成 mp4
         → 合规校验 (绿像素检测 / 敏感词扫描 / 页脚免责非空)

输入 JSON 结构 (全部字段除 cards 外均可选):
{
  "brand": "刊名",                 // 报头刊名 (朱红), 可被 cover.brand 覆盖
  "mast_side": "副标",             // 报头右侧小字
  "footer": "免责文本",            // 全局页脚; 每卡可用 card.footer 覆盖
  "seconds_per_card": 4.0,         // 无逐卡音频时的单卡秒数 (也可用 --sec-per-card)
  "bgm": "path/to/bgm.wav",        // 可选背景音乐
  "cover": {
    "headline": "今日观察", "date": "2026-09-12",
    "kicker_right": "演示版",      // 眉题行右侧 (可空)
    "items": [{"no":"01","name":"示例","code":"000000.XX","price":"12.34"}],
    "focus_label": "本期看点", "focus_name": "可空",
    "note": "看点正文 (支持 **强调**)",
    "footer": "覆盖全局页脚", "audio": "cover.mp3"
  },
  "cards": [
    {"kicker":"观察标的 01", "title":"示例", "subtitle":"代码 · 行业",
     "price_label":"现价", "price":"12.34 元",
     "body":"正文, 支持 **强调** 与 ##数字加粗##",
     "keyline_label":"关键位", "keyline":"上方 13.20 / 下方 11.40",
     "metrics":[{"label":"波动率","value":"58","accent":true}],
     "footer":"", "audio":"card_1.mp3"}
  ],
  "closing": {"headline":"明天见", "text":"结束语", "audio":"closing.mp3"}
}

正文标记 (在 ** 或 ## 之间):
    **文本**  → 朱红强调     ##文本##  → 加粗数字
其余文本一律 HTML 转义后再渲染, 避免输入注入标签。

用法:
    python scripts/make_card_video.py --input examples/sample_cards.json --out demo.mp4
    python scripts/make_card_video.py -i in.json -o out.mp4 --bgm bgm.mp3 --strict

依赖: Pillow (尺寸/配色/绿像素校验, 缺失则降级跳过)、Chrome、ffmpeg/ffprobe。
仅用 Python 标准库 + Pillow, 不 import 任何业务模块、不读任何业务路径。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
DEFAULT_TEMPLATE = SKILL_DIR / "templates" / "paper_card.html"

# ---- 规格 ----
W, H = 1080, 1920
FPS = 30
CRF = 18
PRESET = "medium"

# ---- 报纸风配色 (通用工程规范; 纸上配色, 比屏幕略暗) ----
PAPER = "#FAF7F2"   # 米白纸底 (250,247,242)
INK = "#23262D"     # 墨 (35,38,45)
RULE = "#C8C3BA"    # 分隔线 (200,195,186)
RED = "#C82828"     # 朱红 / 报头 (200,40,40)
GOLD = "#AA823C"    # 金 (170,130,60)
SOFT = "#5A5F68"    # 灰墨 (次要文字)

PAPER_RGB = (250, 247, 242)   # 纸底像素真值, 用于四角采样校验
CORNER_TOL = 3                # 四角允许偏差 (0-255)

# ---- 合规 ----
DEFAULT_FOOTER = "内容仅作研究记录，不构成任何投资建议。"

# 默认敏感词表 (通用金融合规示例; 词表可用 --words 覆盖, 每行一个, # 开头为注释)。
# 命中只告警不拦截; 加 --strict 则命中即退出码 6。
DEFAULT_FORBIDDEN = [
    "荐股", "买入", "卖出", "建仓", "清仓", "目标价", "必涨", "必跌",
    "保证收益", "稳赚", "包赚", "翻倍", "内幕", "抄底", "全仓", "满仓",
    "无风险", "跟单", "带单", "稳赚不赔", "零风险", "保本",
]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]

DOC_SHELL = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
             '<title>{title}</title>\n<style>{css}</style>\n</head>\n<body>\n{body}\n'
             '</body>\n</html>\n')


# ------------------------------------------------------------------
# 模板
# ------------------------------------------------------------------
def load_template(path):
    """把模板文件切成命名区块: css/cover/card/closing/cover_item/keyline/figures/fig_item。"""
    text = Path(path).read_text(encoding="utf-8")
    blocks = {}

    def grab(tag):
        # 锚定行首/行尾: 防止正文注释里出现标记字样时被误判为区块边界
        m = re.search(r"^<!--#%s-->[ \t]*$(.*?)^<!--/#%s-->[ \t]*$" % (tag, tag),
                      text, re.S | re.M)
        return m.group(1) if m else ""

    for tag in ("CSS", "COVER", "COVER_ITEM", "CARD", "KEYLINE",
                "FIGURES", "FIG_ITEM", "CLOSING"):
        blocks[tag.lower()] = grab(tag)
    missing = [k for k in ("css", "cover", "card", "closing") if not blocks[k].strip()]
    if missing:
        raise SystemExit(f"FATAL: 模板缺少区块: {missing} ({path})")
    return blocks


def fill(text, mapping):
    for k, v in mapping.items():
        text = text.replace("{{%s}}" % k, "" if v is None else str(v))
    # 未替换的占位符留空, 防止 {{X}} 漏到画面里
    return re.sub(r"\{\{[A-Z0-9_]+\}\}", "", text)


def markup(s):
    """HTML 转义 → 应用 **强调** / ##数字## → 换行转 <br>。"""
    s = escape(str(s))
    s = re.sub(r"\*\*(.+?)\*\*", r'<span class="hl">\1</span>', s, flags=re.S)
    s = re.sub(r"##(.+?)##", r'<span class="num">\1</span>', s, flags=re.S)
    return s.replace("\n", "<br>")


def css_for(tpl):
    return fill(tpl["css"], {"PAPER": PAPER, "INK": INK, "RULE": RULE,
                             "RED": RED, "GOLD": GOLD, "SOFT": SOFT})


def _footer(obj, global_footer, kind):
    """页脚三级回落: 页面级 → 全局 → 内置默认; 永不返回空 (合规要求)。"""
    t = (obj.get("footer") or global_footer or "").strip()
    if t:
        return markup(t)
    print(f"[合规] ⚠ {kind} 页脚为空 → 回落内置默认免责文本")
    return markup(DEFAULT_FOOTER)


def render_cover(tpl, css, brand, side, cov, global_footer=""):
    items = []
    lst = cov.get("items") or []
    for i, it in enumerate(lst):
        items.append(fill(tpl["cover_item"], {
            "LAST": " last" if i == len(lst) - 1 else "",
            "NO": it.get("no", ""), "NAME": markup(it.get("name", "")),
            "CODE": markup(it.get("code", "")), "PRICE": markup(it.get("price", "")),
        }))
    fn = cov.get("focus_name")
    focus_name = (f'      <div class="fn">{markup(fn)}</div>\n'
                  if fn else "")
    body = fill(tpl["cover"], {
        "BRAND": markup(brand), "MAST_SIDE": markup(side),
        "HEADLINE": markup(cov.get("headline", "")),
        "DATE": markup(cov.get("date", "")),
        "KICKER_RIGHT": markup(cov.get("kicker_right", "")),
        "ITEMS": "\n".join(items),
        "FOCUS_LABEL": markup(cov.get("focus_label", "本期看点")),
        "FOCUS_NAME": focus_name,
        "FOCUS_TEXT": markup(cov.get("note", "")),
        "FOOTER": _footer(cov, global_footer, "cover"),
    })
    return DOC_SHELL.format(title=markup(cov.get("headline", "cover")), css=css, body=body)


def render_card(tpl, css, brand, side, card, global_footer=""):
    figs = []
    for m in (card.get("metrics") or []):
        figs.append(fill(tpl["fig_item"], {
            "LABEL": markup(m.get("label", "")),
            "VALUE": markup(m.get("value", "")),
            "ACCENT": " gold" if m.get("accent") else "",
        }))
    figures = ""
    if figs:
        figures = fill(tpl["figures"], {"FIG_ITEMS": "\n".join(figs)})
    keyline = ""
    if (card.get("keyline") or "").strip():
        keyline = fill(tpl["keyline"], {
            "KEYLINE_LABEL": markup(card.get("keyline_label", "关键位")),
            "KEYLINE": markup(card["keyline"]),
        })
    body = fill(tpl["card"], {
        "BRAND": markup(brand), "MAST_SIDE": markup(side),
        "KICKER": markup(card.get("kicker", "")),
        "SUBTITLE": markup(card.get("subtitle", "")),
        "TITLE": markup(card.get("title", "")),
        "PRICE_LABEL": markup(card.get("price_label", "现价")),
        "PRICE": markup(card.get("price", "")),
        "BODY": markup(card.get("body", "")),
        "KEYLINE": keyline,
        "FIGURES": figures,
        "FOOTER": _footer(card, global_footer, "card"),
    })
    return DOC_SHELL.format(title=markup(card.get("title", "card")), css=css, body=body)


def render_closing(tpl, css, brand, side, close, global_footer=""):
    body = fill(tpl["closing"], {
        "BRAND": markup(brand), "MAST_SIDE": markup(side),
        "HEADLINE": markup(close.get("headline", "")),
        "TEXT": markup(close.get("text", "")),
        "FOOTER": _footer(close, global_footer, "closing"),
    })
    return DOC_SHELL.format(title=markup(close.get("headline", "closing")), css=css, body=body)


# ------------------------------------------------------------------
# 合规扫描
# ------------------------------------------------------------------
def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_strings(v)


def scan_words(data, words):
    """扫描输入里所有字符串, 返回 {词: 命中次数}。"""
    hits = {}
    for s in iter_strings(data):
        for w in words:
            if w and w in s:
                hits[w] = hits.get(w, 0) + s.count(w)
    return hits


def nonempty_footers(data):
    """返回页脚为空/缺省的卡片路径列表 (渲染时会回落到默认免责文本)。"""
    bad = []
    if isinstance(data.get("cover"), dict) and not (data["cover"].get("footer") or "").strip():
        bad.append("cover (回落全局/默认)")
    for i, c in enumerate(data.get("cards") or []):
        if not ((c.get("footer") or data.get("footer") or "").strip()):
            bad.append(f"cards[{i}] (回落默认)")
    if isinstance(data.get("closing"), dict) and not (data["closing"].get("footer") or "").strip():
        bad.append("closing (回落全局/默认)")
    return bad


# ------------------------------------------------------------------
# Chrome 截图
# ------------------------------------------------------------------
def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    return shutil.which("chrome") or shutil.which("chrome.exe") or shutil.which("chromium")


def shoot(chrome, html_path, png_path, profile):
    """Chrome headless 截图 → 1080x1920 PNG。

    固化参数及原因 (踩坑记录):
      --user-data-dir=<临时目录>  : 不指定会复用/污染用户真实 profile; 并发时更会互锁
                                    (Chrome 单实例锁) 导致截图随机失败 → 必带, 且每任务独立
      --disable-lcd-text          : 关闭次像素(亚像素)抗锯齿。开启时文字边缘会出现彩色
                                    杂点 —— 包括绿边, 直接违反"禁绿"铁律, 也会让
                                    绿像素检测出现假阳性 → 必带
      --force-color-profile=srgb  : 不锁定则跟随显示器色彩配置, 同一 HTML 在不同机器上
                                    产出色偏 → 截图像素不可复现 → 必带
      --hide-scrollbars           : 不隐藏时滚动条会被截进画面, 右侧出现灰条 → 必带
      --window-size=1080,1920     : 视口必须精确等于成片尺寸, 否则 --screenshot 只截视口大小,
                                    排版会错位 → 必带
    其余 (--disable-gpu/--no-first-run/--virtual-time-budget/--default-background-color)
    都是稳定性参数: 关 GPU 避免无显卡机的黑屏截图, virtual-time-budget 给字体/布局留时间,
    默认底色避免透明背景被合成为黑。
    """
    url = "file:///" + str(html_path).replace("\\", "/")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-lcd-text",
        "--force-color-profile=srgb",
        "--force-device-scale-factor=1",
        "--window-size=%d,%d" % (W, H),
        "--default-background-color=" + PAPER.lstrip("#"),
        "--virtual-time-budget=3000",
        "--user-data-dir=%s" % profile,
        "--screenshot=%s" % png_path,
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print("  [chrome stderr]", (r.stderr or "")[-600:])
    return Path(png_path).exists()


# ------------------------------------------------------------------
# 音视频
# ------------------------------------------------------------------
def ffmpeg_path():
    return shutil.which("ffmpeg") or "ffmpeg"


def ffprobe_path():
    return shutil.which("ffprobe") or "ffprobe"


def probe_duration(path):
    """ffprobe 读媒体真实时长 (秒); 读不到返回 0.0。"""
    try:
        r = subprocess.run([ffprobe_path(), "-v", "error", "-show_entries",
                            "format=duration", "-of",
                            "default=noprint_wrappers=1:nokey=1", str(path)],
                           capture_output=True, text=True, timeout=60)
        return float((r.stdout or "0").strip() or 0)
    except Exception:
        return 0.0


def probe_streams(mp4):
    r = subprocess.run([ffprobe_path(), "-v", "error", "-show_streams",
                        "-show_format", "-of", "json", str(mp4)],
                       capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout or "{}")
        return list(d.get("streams") or []), dict(d.get("format") or {})
    except Exception:
        return [], {}


def _audio_map(card_audios, card_durs, bgm):
    """构造音频滤镜: 每段音频 adelay 到它所属卡片的起点; BGM 0.10 音量 + 2s fade。

    返回 (filter_fragment, audio_input_paths, n_in)。
    第 i 张卡起点 = 前 i 张卡时长之和 → 音画严格同起点, 末段不被裁。
    """
    base = len(card_durs)
    parts, inputs, labels, start = [], [], [], 0.0
    for i, d in enumerate(card_durs):
        a = card_audios[i]
        if a:
            idx = base + len(inputs)
            inputs.append(a)
            ms = int(round(start * 1000))
            parts.append(
                f"[{idx}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,"
                f"adelay={ms}|{ms}[as{len(labels)}]")
            labels.append(f"[as{len(labels)}]")
        start += d
    if bgm:
        total = sum(card_durs)
        idx = base + len(inputs)
        inputs.append("__BGM__")
        fo = max(0.0, total - 2.0)
        parts.append(
            f"[{idx}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,"
            f"volume=0.10,afade=t=in:st=0:d=2,afade=t=out:st={fo:.3f}:d=2[abgm]")
        labels.append("[abgm]")
    n_in = len(labels)
    if n_in == 0:
        return "", [], 0
    if n_in == 1:
        parts.append(labels[0] + "anull[aout]")
    else:
        parts.append("".join(labels) + f"amix=inputs={n_in}:normalize=0:duration=longest[aout]")
    return ";".join(parts), inputs, n_in


def compose(pngs, durs, mp4, card_audios, bgm):
    """每张 PNG -loop 1 -t <d> 作为独立输入, 用 concat **filter** 拼接。

    为什么不用 concat demuxer: 单帧 PNG 没有时间基, demuxer 拼的是"帧序列",
    每张图只出现 1 帧 → 时长塌缩/变速, 且无法逐段控制时长。concat filter 配合
    -loop 1 -t 才能给出"每张图停留 N 秒"的精确时间轴。
    """
    n = len(pngs)
    total = sum(durs)
    cmd = [ffmpeg_path(), "-y", "-hide_banner"]
    for p, d in zip(pngs, durs):
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(p)]

    vf = "".join(f"[{i}:v]scale={W}:{H},setsar=1,fps={FPS},format=yuv420p[v{i}];"
                 for i in range(n)) + \
         "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[outv]"

    af, aud_inputs, n_in = _audio_map(card_audios, durs, bgm)
    if n_in:
        for a in aud_inputs:
            if a == "__BGM__":
                # BGM 常短于成片 → 循环铺满
                cmd += ["-stream_loop", "-1", "-i", str(bgm)]
            else:
                cmd += ["-i", str(a)]
        cmd += ["-filter_complex", vf + ";" + af, "-map", "[outv]", "-map", "[aout]",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2"]
        print(f"[audio] 音轨段={n_in} (逐卡音频={sum(1 for a in card_audios if a)}"
              f" BGM={'on' if bgm else 'off'})")
    else:
        cmd += ["-filter_complex", vf, "-map", "[outv]", "-an"]
        print("[audio] 无音轨")

    cmd += ["-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-movflags", "+faststart", "-t", f"{total:.3f}", str(mp4)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        print("[ffmpeg stderr]", (r.stderr or "")[-2500:])
    return r.returncode == 0


# ------------------------------------------------------------------
# 校验
# ------------------------------------------------------------------
def count_green(im):
    """统计绿像素: g > r+25 且 g > b+25。

    实现要点 (踩坑): 用 PIL 通道运算向量化 (2M 像素毫秒级, 纯 Python 循环要几十秒)。
    但**不要**把掩码转成 mode "1" 再 logical_and —— Pillow 对 "1" 模式图的
    histogram() 语义在不同版本下不一致 (12.x 返回 256 桶), 会导致恒为 0 的假通过。
    改为全程保持 "L" 模式, 用 multiply 做交集: 255*255/255=255, 其余为 0,
    再取 histogram()[255] 计数, 语义稳定。
    """
    from PIL import ImageChops
    r, g, b = im.convert("RGB").split()
    mask = lambda band: band.point(lambda v: 255 if v > 25 else 0)
    m1 = mask(ImageChops.subtract(g, r))   # g - r (负值截断为 0)
    m2 = mask(ImageChops.subtract(g, b))   # g - b
    return ImageChops.multiply(m1, m2).histogram()[255]


def corner_ok(im):
    """四角各采 6x6 色块, 全部落在纸色 ±CORNER_TOL 内才算通过。"""
    px = im.convert("RGB").load()
    w, h = im.size
    worst = 0
    for cx, cy in ((0, 0), (w - 6, 0), (0, h - 6), (w - 6, h - 6)):
        for y in range(cy, cy + 6):
            for x in range(cx, cx + 6):
                r, g, b = px[x, y]
                worst = max(worst, abs(r - PAPER_RGB[0]), abs(g - PAPER_RGB[1]),
                            abs(b - PAPER_RGB[2]))
    return worst <= CORNER_TOL, worst


def verify(mp4, pngs, durs, green_total, bad_footers, word_hits):
    ok = True
    print("\n===== 校验 =====")

    try:
        from PIL import Image
    except ImportError:
        Image = None
        print("[png ] 未安装 Pillow → 跳过尺寸/配色/绿像素校验 (pip install pillow)")

    if Image:
        greens = 0
        for p in pngs:
            with Image.open(p) as im:
                size, cok, worst = im.size, *corner_ok(im)
                g = count_green(im)
            greens += g
            bad = ""
            if size != (W, H):
                bad += f" 尺寸异常 {size[0]}x{size[1]}"
                ok = False
            if not cok:
                bad += f" 四角非纸色 (最大偏差 {worst})"
                ok = False
            if g:
                bad += f" 绿像素 {g}"
                ok = False
            print(f"[png ] {p.name}  {size[0]}x{size[1]}  绿像素={g}  "
                  f"四角纸色偏差={worst}{'  OK' if not bad else '  ▶' + bad}")
        print(f"[合规] ① 绿像素合计 = {greens} {'(PASS)' if greens == 0 else '(FAIL — 出现绿色)'}")

    streams, fmt = probe_streams(mp4)
    types = [s.get("codec_type") for s in streams]
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    a = next((s for s in streams if s.get("codec_type") == "audio"), {})
    fdur = float(fmt.get("duration") or 0)
    print(f"[流  ] ② video={v.get('codec_name')} {v.get('width')}x{v.get('height')} "
          f"{v.get('pix_fmt')} {v.get('r_frame_rate')} | "
          f"audio={a.get('codec_name') or '无'} {a.get('sample_rate') or '-'}Hz")
    if v.get("pix_fmt") != "yuv420p" or (v.get("width"), v.get("height")) != (W, H):
        print("[流  ] ⚠ 规格不符 (期望 h264/yuv420p/1080x1920)")
        ok = False
    exp = sum(durs)
    gap = abs(fdur - exp)
    print(f"[时长] ③ 容器 {fdur:.3f}s vs 各卡之和 {exp:.3f}s "
          f"(差 {gap:.3f}s) {'一致' if gap <= 0.15 else '不一致!'}")
    if gap > 0.15:
        ok = False
    print(f"[时长]    各卡时长 = {['%.2f' % d for d in durs]}")

    if a:
        r = subprocess.run([ffmpeg_path(), "-hide_banner", "-i", str(mp4),
                            "-af", "volumedetect", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=120)
        mm = re.search(r"max_volume: (-?[\d.]+) dB", r.stderr or "")
        mn = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr or "")
        mx = float(mm.group(1)) if mm else -99.0
        mean = float(mn.group(1)) if mn else -99.0
        print(f"[音量] ④ max={mx:.1f}dB mean={mean:.1f}dB"
              + ("  ⚠ 疑似静音!" if mx < -50 else "  ⚠ 峰值过高" if mx > -1.5 else ""))

    print(f"[合规] ⑤ 敏感词命中 = {word_hits or '无'}")
    print(f"[合规] ⑥ 页脚缺省回落 = {bad_footers or '无 (全部显式提供)'}")
    print(f"[产物] {mp4}  {mp4.stat().st_size if mp4.exists() else 0} bytes")
    return ok and mp4.exists()


# ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="通用报纸风金融卡片视频渲染器 (JSON → 1080x1920 MP4)")
    ap.add_argument("-i", "--input", required=True, help="输入 JSON 文件")
    ap.add_argument("-o", "--out", required=True, help="输出 MP4 路径")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="HTML 模板路径")
    ap.add_argument("--sec-per-card", type=float, default=None,
                    help="无逐卡音频时的单卡秒数 (默认 4.0, JSON 的 seconds_per_card 优先)")
    ap.add_argument("--pad", type=float, default=0.5,
                    help="有逐卡音频时, 语音结束后的留白秒数 (默认 0.5)")
    ap.add_argument("--bgm", default=None, help="背景音乐 (音量 0.10 + 2s fade; 自动循环)")
    ap.add_argument("--words", default=None, help="敏感词表文件 (每行一词, # 为注释)")
    ap.add_argument("--strict", action="store_true", help="敏感词命中即失败 (退出码 6)")
    ap.add_argument("--keep-workdir", action="store_true", help="保留中间 HTML/PNG 便于排查")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"FATAL: 输入不存在 {src}")
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))

    brand = data.get("brand", "")
    side = data.get("mast_side", "")
    global_footer = (data.get("footer") or "").strip()
    sec = args.sec_per_card if args.sec_per_card is not None \
        else float(data.get("seconds_per_card") or 4.0)
    bgm = args.bgm or data.get("bgm")
    if bgm and not Path(bgm).exists():
        print(f"[bgm ] ⚠ 找不到 {bgm}, 忽略")
        bgm = None

    # ---- 敏感词扫描 (渲染前, 便宜且能提前拦) ----
    words = DEFAULT_FORBIDDEN
    if args.words:
        wtxt = Path(args.words).read_text(encoding="utf-8")
        words = [ln.strip() for ln in wtxt.splitlines()
                 if ln.strip() and not ln.strip().startswith("#")]
    hits = scan_words(data, words)
    print(f"[合规] 敏感词扫描: 词表 {len(words)} 词 → 命中 {hits or '无'}")
    if hits and args.strict:
        print("FATAL: --strict 且命中敏感词, 终止")
        return 6
    bad_footers = nonempty_footers(data)
    if bad_footers:
        print(f"[合规] ⚠ 页脚为空, 已回落默认免责文本: {bad_footers}")

    # ---- 组装卡片序列 ----
    tpl = load_template(args.template)
    css = css_for(tpl)
    pages = []   # (kind, html, audio_path)
    if isinstance(data.get("cover"), dict):
        cov = data["cover"]
        pages.append(("cover", render_cover(tpl, css, cov.get("brand", brand),
                                            side, cov, global_footer), cov.get("audio")))
    for i, card in enumerate(data.get("cards") or []):
        pages.append((f"card_{i + 1}", render_card(tpl, css, card.get("brand", brand),
                                                   side, card, global_footer), card.get("audio")))
    if isinstance(data.get("closing"), dict):
        cl = data["closing"]
        pages.append(("closing", render_closing(tpl, css, cl.get("brand", brand),
                                                side, cl, global_footer), cl.get("audio")))
    if not pages:
        print("FATAL: 输入里没有 cover/cards/closing, 无可渲染内容")
        return 2
    print(f"[输入] {src.name}  页面数={len(pages)}  "
          f"({', '.join(k for k, _, _ in pages)})")

    chrome = find_chrome()
    if not chrome:
        print("FATAL: 找不到 Chrome")
        return 3
    print(f"[chrome] {chrome}")

    work = Path(tempfile.mkdtemp(prefix="card_video_"))
    profile = work / "chrome_profile"
    profile.mkdir()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        pngs, durs, audios = [], [], []
        for i, (kind, html, audio) in enumerate(pages):
            hp = work / f"page_{i:02d}.html"
            pp = work / f"page_{i:02d}.png"
            hp.write_text(html, encoding="utf-8")
            if not shoot(chrome, hp, pp, profile):
                print(f"FATAL: 截图失败 {kind}")
                return 4
            ap_ = None
            if audio:
                ap_ = audio if Path(audio).is_absolute() else str((src.parent / audio))
                if not Path(ap_).exists():
                    print(f"[audio] ⚠ 缺文件 {ap_}, 该卡回落固定时长")
                    ap_ = None
            d = probe_duration(ap_) + args.pad if ap_ else sec
            d = max(1.0, round(d, 3))
            pngs.append(pp)
            durs.append(d)
            audios.append(ap_)
            print(f"[page ] {kind:<9} png 1080x1920  时长={d:.2f}s"
                  f"{'  音频=' + Path(ap_).name if ap_ else ''}")

        print(f"[plan ] 总时长≈{sum(durs):.2f}s  输出={out}")
        if not compose(pngs, durs, out, audios, bgm):
            print("FATAL: ffmpeg 合成失败")
            return 5

        ok = verify(out, pngs, durs, None, bad_footers, hits)
        if args.keep_workdir:
            print(f"[work ] 中间产物保留在 {work}")
        print("\nDONE ->", out)
        return 0 if ok else 5
    finally:
        if not args.keep_workdir:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
