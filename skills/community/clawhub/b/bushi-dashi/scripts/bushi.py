#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""我不是大师 · 卜算内核 CLI（从游戏版 GDScript 逐行对应翻译）

方法：钱筮法（三枚铜钱，字=2 背=3，六掷成卦）
      区别于大衍筮法（蓍草）。爻值 6 老阴 / 7 少阳 / 8 少阴 / 9 老阳，
      概率 1/8 · 3/8 · 3/8 · 1/8；6 与 9 为变爻。

子命令：
  cast    起卦。--seed N 可复现；--lines 9,8,7,6,7,8 报亲手掷出的六爻
  judge   断卦。--lines ... 输出七法主副辞 + 签级 + 白话 + 应语（--topic --note）
  study   学卦。--bits 63 [--section gua] [--src zhengyi] 四源注疏按节输出
  record  卦册。save 落档 / list 列表 / show 最近一卦详情

输出为 JSON（供 WorkBuddy 读取后按 SKILL.md 规约组织成先生的话）。
编码约定：卦用 6 位整数 bits，bit0=初爻，阳=1；乾=63，坤=0（与通行卦序不同）。
"""
import argparse
import json
import os
import random
import re
import shutil
import sys
import unicodedata
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def _codex_path():
    """卦册是客人私人数据，不放在 Skill 目录内：从市场安装后该目录可能只读、
    升级时会被整包覆盖。固定在用户家目录 ~/.bushi-dashi/codex.json：
    本 Skill 不读取任何自定义环境变量做重定向（家目录本身在 Unix 上遵循
    系统 HOME 约定，那是系统行为，不是本 Skill 的重定向入口）。"""
    home = os.path.join(os.path.expanduser("~"), ".bushi-dashi")
    path = os.path.join(home, "codex.json")
    legacy = os.path.join(DATA, "codex.json")   # 旧版本存在 Skill 目录内
    if not os.path.exists(path) and os.path.exists(legacy):
        try:
            os.makedirs(home, exist_ok=True)
            shutil.copyfile(legacy, path)       # 搬迁旧卦册，客人记录不丢
        except OSError:
            return legacy
    return path


CODEX_PATH = _codex_path()

LINE_NAMES = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}
TOPICS = ["事业", "姻缘", "财运", "健康", "出行", "失物", "心事"]
TONE_SCORE = {"ji": 90.0, "bian": 20.0, "ping": 0.0, "xiong": -90.0}
# 本卦/之卦话语权（朱熹变占法简化）：按变爻数
WEIGHTS = {0: (1.0, 0.0), 1: (0.8, 0.2), 2: (0.7, 0.3), 3: (0.6, 0.4),
           4: (0.3, 0.7), 5: (0.2, 0.8), 6: (0.0, 1.0)}
TIER_LABEL = {"shangshang": "上上签", "shang": "上签", "zhong": "中签",
              "xia": "下签", "xiaxia": "下下签"}


def _out(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=1))
    sys.stdout.write("\n")


def _die(msg):
    _out({"error": msg})
    sys.exit(1)


# ================= 数据 =================

_hex_cache = None
_study_cache = {}


def hexagrams():
    global _hex_cache
    if _hex_cache is None:
        with open(os.path.join(DATA, "hexagrams.json"), encoding="utf-8") as f:
            _hex_cache = json.load(f)
    return _hex_cache


def hex_of(bits):
    return hexagrams().get(str(bits), {})


def hex_name(bits):
    return hex_of(bits).get("name", "未知卦")


def study_data(bits):
    if bits not in _study_cache:
        key = {63: "qian", 0: "kun"}.get(bits, "x%d" % bits)
        path = os.path.join(DATA, "study_%s.json" % key)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                _study_cache[bits] = json.load(f)
        else:
            _study_cache[bits] = {}
    return _study_cache[bits]


# ================= 卦象编码 =================

def is_yang(v):
    return v in (7, 9)


def is_changing(v):
    return v in (6, 9)


def primary_bits(lines):
    b = 0
    for i in range(6):
        if is_yang(lines[i]):
            b |= 1 << i
    return b


def changed_bits(lines):
    b = 0
    for i in range(6):
        yang = is_yang(lines[i])
        if is_changing(lines[i]):
            yang = not yang
        if yang:
            b |= 1 << i
    return b


def changing_positions(lines):
    """变爻位，1-based 升序"""
    return [i + 1 for i in range(6) if is_changing(lines[i])]


def unchanged_positions(lines):
    """不变爻位，0-based 升序"""
    return [i for i in range(6) if not is_changing(lines[i])]


# ================= 钱筮法 =================

def cast_once(rng):
    return sum(2 if rng.randint(0, 1) == 0 else 3 for _ in range(3))


def cast_hexagram(rng):
    return [cast_once(rng) for _ in range(6)]


# ================= 卦图 =================
#
# 对齐铁律（黑白 CLI 与聊天窗口都要站齐）：
#   · 爻画用粗线 ▄（黑白终端里醒目），但**恒置于行尾**——▄ 属东亚歧义宽度
#     （有的字体 1 列、回退中文字体 2 列），放在行尾其宽度就不参与对齐
#   · 爻画之前的对齐区只用宽度确定的字符：爻题全角（恒 2 列/字）、
#     变爻标记全角 Ｘ（恒 2 列，老阴老阳同记，遵参照图）、静爻补两个半角空格（恒 1 列/个）
#   · 补白按「显示宽度」而非字符数（中文一字 2 列）
# 版式：本卦六爻自上而下（动爻在爻尾标 Ｘ）；有变爻时之卦六爻另列一段。
YANG_BAR = "▄▄▄▄▄▄▄"
YIN_BAR = "▄▄▄ ▄▄▄"
# 遵主人参照图：老阴、老阳同记 ×（阴阳以实线/断线区分），× 即「动爻」
CHANGE_MARK = {9: "Ｘ", 6: "Ｘ"}
# 参照图「四种情况」→ 爻值：三阴=6 老阴 / 二阴一阳=7 少阳 / 一阴二阳=8 少阴 / 三阳=9 老阳
TOSS_MAP = {"3阴": 6, "2阴1阳": 7, "1阴2阳": 8, "3阳": 9}

W_YAOTI, W_MARK = 4, 2             # 爻题 / 标记 两栏显示宽度


def _dw(s):
    """显示宽度：宽字符(W)/全角(F) 计 2 列，其余计 1 列"""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def _fit(s, w):
    """按显示宽度右侧补空格到 w 列（超出则原样返回）"""
    return s + " " * max(0, w - _dw(s))


def build_diagram(lines):
    """文本卦图：本卦六爻自上而下（上爻→初爻），动爻（老阴/老阳）爻尾标 Ｘ；
    有变爻时之卦六爻另列一段。爻画恒在行尾，对齐不依赖字体宽窄。"""
    pb, cb = primary_bits(lines), changed_bits(lines)
    ch = changing_positions(lines)
    yaoti_p = hex_of(pb).get("yaoti", [""] * 6)
    yaoti_c = hex_of(cb).get("yaoti", [""] * 6)
    has_ch = bool(ch)

    def bar(bits, k):
        return YANG_BAR if (bits >> k & 1) else YIN_BAR

    rows = []
    if has_ch:
        rows.append("本卦：%s　→　之卦：%s" % (hex_name(pb), hex_name(cb)))
    else:
        rows.append("本卦：%s" % hex_name(pb))
    for k in range(5, -1, -1):     # 上爻 → 初爻
        yt = _fit(yaoti_p[k] if k < len(yaoti_p) else "", W_YAOTI)
        mk = _fit(CHANGE_MARK.get(lines[k], ""), W_MARK)
        rows.append("%s %s %s" % (yt, mk, bar(pb, k)))
    if has_ch:
        rows.append("")
        rows.append("之卦：%s" % hex_name(cb))
        for k in range(5, -1, -1):
            yt = _fit(yaoti_c[k] if k < len(yaoti_c) else "", W_YAOTI)
            rows.append("%s %s %s" % (yt, " " * W_MARK, bar(cb, k)))
    rows.append("")
    rows.append("变爻：%s" % ("、".join("%s%s" % (yaoti_p[p_ - 1], CHANGE_MARK[lines[p_ - 1]])
                                     for p_ in ch) if ch else "无（六爻安静）"))
    if ch:
        rows.append("（爻尾 Ｘ 为动爻：老阳动而变阴，老阴动而变阳）")
    return "\n".join(rows)


# ================= 断卦七法 =================

def yao_text(bits, pos):
    ya = hex_of(bits).get("yaoci", [])
    return ya[pos] if 0 <= pos < len(ya) else ""


def yao_title(bits, pos):
    yt = hex_of(bits).get("yaoti", [])
    return yt[pos] if 0 <= pos < len(yt) else ""


def _opt(role, bits, pos, grade):
    """pos: ≥0 爻位(0-based) / -1 卦辞 / -2 用辞"""
    if pos == -1:
        kind, title, text = "卦辞", hex_name(bits), hex_of(bits).get("guaci", "")
    elif pos == -2:
        kind = "用辞"
        title = hex_name(bits) + (" · 用九" if bits == 63 else " · 用六")
        text = hex_of(bits).get("yong", "")
    else:
        kind = "爻辞"
        title = "%s · %s" % (hex_name(bits), yao_title(bits, pos))
        text = yao_text(bits, pos)
    return {"role": role, "kind": kind, "title": title, "text": text,
            "grade": grade, "bits": bits, "pos": pos}


def verdict(lines):
    """断卦七法，遵主人参照图（钱币法流行七则）：
    0 变→本卦卦辞；1 变→本卦变爻爻辞；2 变→本卦两变爻爻辞、以上爻为主；
    3 变→本卦卦辞为主、变卦卦辞为辅；4 变→本卦两不变爻爻辞、以下爻为主；
    5 变→变卦不变爻爻辞；6 变→变卦卦辞。
    （图外不添辞：单源档只出一辞，不再附「另有一说」。）"""
    pb, cb = primary_bits(lines), changed_bits(lines)
    ch = changing_positions(lines)
    n = len(ch)
    out = []
    if n == 0:
        out.append(_opt("主", pb, -1, "shang"))
    elif n == 1:
        out.append(_opt("主", pb, ch[0] - 1, "shang"))
    elif n == 2:
        out.append(_opt("主", pb, ch[1] - 1, "shang"))
        out.append(_opt("副", pb, ch[0] - 1, "zhong"))
    elif n == 3:
        out.append(_opt("主", pb, -1, "shang"))
        out.append(_opt("副", cb, -1, "zhong"))
    elif n == 4:
        unch = unchanged_positions(lines)
        out.append(_opt("主", pb, unch[0], "shang"))
        out.append(_opt("副", pb, unch[1], "zhong"))
    elif n == 5:
        unch = unchanged_positions(lines)
        out.append(_opt("主", cb, unch[0], "shang"))
    else:  # 6 变：乾坤取用九/用六（朱熹《易学启蒙》特例），余卦取变卦卦辞
        if pb in (63, 0):
            out.append(_opt("主", pb, -2, "shang"))
        else:
            out.append(_opt("主", cb, -1, "shang"))
    return out


# ================= 签级 =================

def tone_score(bits):
    return TONE_SCORE.get(hex_of(bits).get("tone", "ping") or "ping", 0.0)


def score(lines):
    n = len(changing_positions(lines))
    w = WEIGHTS.get(n, (0.5, 0.5))
    return tone_score(primary_bits(lines)) * w[0] + tone_score(changed_bits(lines)) * w[1]


def tier_of(s):
    if s >= 70.0:
        return "shangshang"
    if s >= 30.0:
        return "shang"
    if s > -30.0:
        return "zhong"
    if s > -70.0:
        return "xia"
    return "xiaxia"


def tier(lines):
    return tier_of(score(lines))


# ================= 卦册 =================

def load_codex():
    if os.path.exists(CODEX_PATH):
        with open(CODEX_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"visits": 0, "casts": [], "codex": []}


def save_codex(c):
    d = os.path.dirname(os.path.abspath(CODEX_PATH))
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        _die("卦册目录无法创建：%s" % d)
    with open(CODEX_PATH, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=1)


# ================= 子命令 =================

def parse_toss(s):
    """把一掷的「N阴N阳」报法换成爻值（遵参照图四种情况）。
    接受：3阴 / 3阳 / 2阴1阳 / 1阴2阳（顺序与分隔可宽松，如「二阴一阳」「2阴,1阳」）。"""
    t = s.replace(",", "").replace("，", "").replace(" ", "")
    cn = {"零": "0", "一": "1", "二": "2", "两": "2", "三": "3"}
    t = "".join(cn.get(c, c) for c in t)
    yin = yang = None
    m = re.search(r"(\d)阴", t)
    if m:
        yin = int(m.group(1))
    m = re.search(r"(\d)阳", t)
    if m:
        yang = int(m.group(1))
    if yin is None and yang is not None:
        yin = 3 - yang
    if yang is None and yin is not None:
        yang = 3 - yin
    if yin is None or yang is None or yin + yang != 3:
        return None
    key = "%d阴%d阳" % (yin, yang) if 0 < yin < 3 else ("%d阴" % yin if yin == 3 else "%d阳" % yang)
    return TOSS_MAP.get(key)


def lines_from_args(args, required=True):
    """从 --toss（N阴N阳 六掷）或 --lines（爻值六数）解析六爻，初爻在前。"""
    if getattr(args, "toss", None):
        parts = [p for p in args.toss.split(";") if p.strip()]
        if len(parts) != 6:
            _die("--toss 须为六掷，分号分隔，如「3阴;2阴1阳;1阴2阳;3阳;2阴1阳;1阴2阳」（初爻在前）")
        lines = []
        for p in parts:
            v = parse_toss(p)
            if v is None:
                _die("无法解析第 %d 掷：%s（应为 3阴/2阴1阳/1阴2阳/3阳）" % (len(lines) + 1, p))
            lines.append(v)
        return lines, True
    if getattr(args, "lines", None):
        try:
            lines = [int(x) for x in args.lines.split(",")]
        except ValueError:
            _die("--lines 须为逗号分隔的 6 个整数（6/7/8/9）")
        if len(lines) != 6 or any(v not in LINE_NAMES for v in lines):
            _die("--lines 须为 6 个 6/7/8/9 值（初爻在前）")
        return lines, True
    if required:
        _die("需要 --toss 或 --lines")
    return None, False


def cmd_cast(args):
    if args.toss or args.lines:
        lines, hand = lines_from_args(args)
    else:
        rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
        lines = cast_hexagram(rng)
        hand = False
    pb, cb = primary_bits(lines), changed_bits(lines)
    ch = changing_positions(lines)
    _out({
        "lines": lines,
        "line_names": [LINE_NAMES[v] for v in lines],
        "diagram": build_diagram(lines),
        "hand": hand,
        "primary": {"bits": pb, "name": hex_name(pb), "seq": hex_of(pb).get("seq")},
        "changed": {"bits": cb, "name": hex_name(cb)} if ch else None,
        "changing_positions": ch,
        "tier": tier(lines),
        "tier_label": TIER_LABEL[tier(lines)],
        "score": round(score(lines), 1),
    })


def cmd_judge(args):
    lines, _hand = lines_from_args(args)
    pb = primary_bits(lines)
    h = hex_of(pb)
    t = tier(lines)
    topic = args.topic if args.topic in TOPICS else ""
    ying = ""
    if topic and h.get("ying"):
        ying = h["ying"].get(topic, "")
    _out({
        "lines": lines,
        "diagram": build_diagram(lines),
        "primary": {"bits": pb, "name": hex_name(pb), "guaci": h.get("guaci", ""),
                    "baihua": h.get("baihua", ""), "yi": h.get("yi", ""),
                    "metaphor": h.get("metaphor", ""), "tone": h.get("tone", "ping"),
                    "detail_level": h.get("detail_level", 0)},
        "changed": {"bits": changed_bits(lines), "name": hex_name(changed_bits(lines))}
                   if changing_positions(lines) else None,
        "changing_positions": changing_positions(lines),
        "verdict": verdict(lines),
        "tier": t, "tier_label": TIER_LABEL[t], "score": round(score(lines), 1),
        "topic": topic, "note": args.note or "", "ying": ying,
    })


def cmd_study(args):
    d = study_data(args.bits)
    if not d:
        _out({"bits": args.bits, "name": hex_name(args.bits), "available": False,
              "hint": "此卦注疏未入库（文件缺失或损坏）"})
        return
    secs = d.get("sections", [])
    if args.section:
        secs = [s for s in secs if s.get("key") == args.section]
        if not secs:
            _die("无此节：%s（可用 --list 查看）" % args.section)
    if args.list:
        _out({"bits": args.bits, "name": d.get("name"),
              "sections": [{"key": s["key"], "title": s["title"]} for s in d.get("sections", [])],
              "sources": d.get("sources", [])})
        return
    out_secs = []
    for s in secs:
        blocks = s.get("blocks", [])
        if args.src:
            blocks = [b for b in blocks if b.get("src") == args.src]
        out_secs.append({"key": s["key"], "title": s["title"], "blocks": blocks})
    _out({"bits": args.bits, "name": d.get("name"), "note": d.get("note", ""),
          "available": True, "sections": out_secs})


def cmd_record(args):
    c = load_codex()
    if args.action == "save":
        if not (args.lines or args.toss):
            _die("save 需要 --lines 或 --toss")
        lines, _hand = lines_from_args(args)
        pb = primary_bits(lines)
        rec = {"bits": pb, "lines": lines, "name": hex_name(pb),
               "topic": args.topic or "", "note": args.note or "",
               "hand": bool(args.hand), "tier": tier(lines),
               "date": str(date.today())}
        c["casts"].append(rec)
        c["casts"] = c["casts"][-64:]
        if pb not in c["codex"]:
            c["codex"].append(pb)
        c["visits"] = int(c.get("visits", 0)) + 1
        save_codex(c)
        _out({"saved": rec, "visits": c["visits"], "codex_count": len(c["codex"])})
    elif args.action == "list":
        _out({"visits": c.get("visits", 0), "codex_count": len(c.get("codex", [])),
              "casts": c.get("casts", [])[-10:]})
    else:
        _die("record 仅支持 save / list")


def main():
    p = argparse.ArgumentParser(description="我不是大师 · 卜算内核")
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("cast", help="起卦")
    pc.add_argument("--seed", type=int, default=None)
    pc.add_argument("--lines", default=None, help="亲手掷出的六爻，如 9,8,7,6,7,8（初爻在前）")
    pc.add_argument("--toss", default=None,
                    help="亲手掷出的六掷报法，分号分隔，如 3阴;2阴1阳;1阴2阳;3阳;2阴1阳;1阴2阳（初爻在前）")
    pc.set_defaults(func=cmd_cast)

    pj = sub.add_parser("judge", help="断卦")
    pj.add_argument("--lines", default=None)
    pj.add_argument("--toss", default=None)
    pj.add_argument("--topic", default="")
    pj.add_argument("--note", default="")
    pj.set_defaults(func=cmd_judge)

    ps = sub.add_parser("study", help="学卦（四源注疏）")
    ps.add_argument("--bits", type=int, required=True)
    ps.add_argument("--section", default=None)
    ps.add_argument("--src", default=None, choices=["jing", "zhengyi", "benyi", "yizhuan"])
    ps.add_argument("--list", action="store_true")
    ps.set_defaults(func=cmd_study)

    pr = sub.add_parser("record", help="卦册")
    pr.add_argument("action", choices=["save", "list"])
    pr.add_argument("--lines", default=None)
    pr.add_argument("--toss", default=None)
    pr.add_argument("--topic", default="")
    pr.add_argument("--note", default="")
    pr.add_argument("--hand", action="store_true")
    pr.set_defaults(func=cmd_record)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
