#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cn_ref_normalizer.py — 中文库（CNKI / 万方 / SinoMed）导入与 CJK 归一化（升级项 I，2026-11-02）.

两条纪律，缺一不可：

1. **只走"用户合法导出 → 导入"**。本模块不访问知网/万方/SinoMed 任何站点，
   不含爬虫、不含浏览器驱动、不含 Cookie —— 与 ct-literature FAQ「no crawler」
   红线一致。用户在自己的机构权限下导出（RIS / JSON），本模块只读该文件。

2. **中文题名先归一再去重**。同一篇中文论文经不同库导出时，全半角、繁简、
   标点、空格写法常不一致（"非小细胞肺癌" vs "非小細胞肺癌"、"ＰＤ－１" vs "PD-1"），
   直接按原文做 title key 会把一篇拆成两条。本模块提供受限归一：
   - 全角 ASCII / 全角空格 → 半角
   - 中文标点 → 半角（书名号、引号等直接剥离）
   - 高频繁体 → 简体（**受控小表**，未收录字符原样保留，不臆造）
   - 大小写与空白归一

   ⚠️ 归一只用于**生成去重 key 与显示排序**，不回写 work 的 title 原文
   （原文保真优先；见 LRN-20260921-001 关于 NFKC 破坏字符的教训 —— 因此这里
   不用 `unicodedata.normalize("NFKC")` 整段处理，而是逐字符受控映射）。

CLI:
    python adapters/cn_ref_normalizer.py --in cnki_export.ris --source CNKI --out cn.json
    python adapters/cn_ref_normalizer.py --title "非小細胞肺癌ＰＤ－１抑制剂研究"
"""
import argparse
import json
import os
import re
import sys

# ── 受控繁体→简体映射（**仅单字键**：to_simplified 逐字符查表，多字键永远命中不到）
# 只收高频临床/通用字；未收录字符原样保留，不臆造。
_T2S = {
    "細": "细", "證": "证", "據": "据", "隨": "随", "機": "机", "對": "对",
    "試": "试", "驗": "验", "組": "组", "療": "疗", "評": "评", "結": "结",
    "顯": "显", "統": "统", "計": "计", "學": "学", "進": "进", "藥": "药",
    "劑": "剂", "發": "发", "臨": "临", "醫": "医", "觀": "观", "隊": "队",
    "顧": "顾", "雙": "双", "開": "开", "標": "标", "籤": "签", "納": "纳",
    "準": "准", "則": "则", "識": "识", "綜": "综", "檢": "检", "數": "数",
    "庫": "库", "獻": "献", "質": "质", "價": "价", "實": "实", "踐": "践",
    "與": "与", "為": "为", "這": "这", "個": "个", "們": "们", "來": "来",
    "時": "时", "間": "间", "關": "关", "於": "于", "國": "国", "內": "内",
    "際": "际", "華": "华", "東": "东", "區": "区", "會": "会", "長": "长",
    "總": "总", "體": "体", "無": "无", "轉": "转", "歸": "归", "風": "风",
    "險": "险", "獲": "获", "負": "负", "擔": "担", "費": "费", "經": "经",
    "濟": "济", "衛": "卫", "資": "资", "終": "终", "點": "点", "變": "变",
    "線": "线", "訪": "访", "網": "网", "絡": "络", "戶": "户", "帶": "带",
    "並": "并", "舉": "举", "僅": "仅", "夠": "够", "擬": "拟",
    "應": "应", "該": "该", "減": "减", "燒": "烧", "腫": "肿", "瘤": "瘤",
}

# 需要整体剥离的中文标点（在 key 里不承载语义，反而是去重噪音来源）
_CJK_PUNCT = "，。；：！？、（）【】〔〕「」『』《》〈〉“”‘’…—－·／＼　"

# 文件名 → 数据源规范名（用于 source 推断；推断失败必须显式报错，不猜）
_SOURCE_HINTS = (
    ("cnki", "CNKI"), ("知网", "CNKI"),
    ("wanfang", "WanFang"), ("万方", "WanFang"),
    ("sinomed", "SinoMed"), ("cbm", "SinoMed"), ("中国生物医学", "SinoMed"),
    ("vip", "VIP"), ("维普", "VIP"),
)


def _halfwidth_char(ch):
    o = ord(ch)
    if o == 0x3000:                      # 全角空格
        return " "
    if 0xFF01 <= o <= 0xFF5E:             # 全角 ASCII
        return chr(o - 0xFEE0)
    return ch


def to_halfwidth(s):
    """全角 ASCII / 全角空格 → 半角（逐字符，不用 NFKC 整段归一）。"""
    return "".join(_halfwidth_char(c) for c in (s or ""))


def to_simplified(s):
    """高频繁体 → 简体（受控小表；未收录字符原样保留）。"""
    return "".join(_T2S.get(c, c) for c in (s or ""))


def normalize_cn_title(title):
    """中文题名归一：全半角 + 繁简 + 标点剥离 + 空白/大小写归一。

    只用于生成去重 key，**不**回写原文。英文题名同样适用（幂等）。
    """
    if not title:
        return ""
    s = to_halfwidth(title)
    s = to_simplified(s)
    for ch in _CJK_PUNCT:
        s = s.replace(ch, " ")
    s = s.lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s)
    return " ".join(s.split())


def has_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s or ""))


def title_key(work):
    """work 的去重 title key（DOI 缺失时使用）。"""
    return normalize_cn_title(work.get("title") or "")


def infer_source(path, explicit=None):
    """推断数据源名：显式参数 > 文件名特征 > 报错（不猜）。"""
    if explicit:
        return explicit
    base = os.path.basename(path or "").lower()
    for hint, name in _SOURCE_HINTS:
        if hint in base:
            return name
    raise ValueError(
        "无法从文件名推断中文库来源（%s）。请显式指定 source：CNKI / WanFang / "
        "SinoMed / VIP。" % os.path.basename(path or "(unknown)"))


# ── RIS 解析（CNKI / 万方 / SinoMed 均支持导出 RIS）────────────────────────
def parse_ris(text):
    """极简 RIS 解析器 → [{title, doi, authors, year, publication, abstract_snippet}]。

    只认书目层需要的标签；TY=JOUR/BOOK 等类型信息保留在 pub_types。
    """
    recs, cur = [], {}
    key = None
    for raw in (text or "").splitlines():
        line = raw.rstrip("\r")
        if len(line) >= 2 and line[:2].isupper() and line[2:5] == "  -":
            key = line[:2]
            val = line[5:].strip()
            if key == "TY":
                cur = {"pub_types": [val]}
                continue
            if key == "ER":
                if cur:
                    recs.append(cur)
                cur, key = {}, None
                continue
            if not cur:
                cur = {}
            if key in ("TI", "T1"):
                cur["title"] = val
            elif key in ("AU", "A1"):
                cur.setdefault("authors", []).append(val)
            elif key in ("DO",):
                cur["doi"] = val
            elif key in ("PY", "Y1"):
                cur["year"] = val
            elif key in ("JO", "JF", "T2", "JA"):
                cur.setdefault("publication", val)
            elif key in ("AB", "N2"):
                cur["abstract_snippet"] = (cur.get("abstract_snippet") or "") + val
            elif key in ("UR", "L2"):
                cur.setdefault("url", val)
            elif key in ("LA",):
                cur["language"] = val
        elif key and line.strip():
            # 续行（RIS 长摘要会换行续写）
            if key in ("AB", "N2"):
                cur["abstract_snippet"] = (cur.get("abstract_snippet") or "") + " " + line.strip()
            elif key in ("TI", "T1"):
                cur["title"] = (cur.get("title") or "") + " " + line.strip()
    if cur:
        recs.append(cur)
    return recs


def load_cn_export(path, source=None):
    """读用户导出的中文库文件（RIS / JSON）→ ct-literature work 列表。

    支持：
      - RIS 文本（.ris / .txt）
      - JSON：{"works":[...]} / {"records":[...]} / 裸列表（CNKI 批量导出的常见形态）
    其它格式（NoteExpress .nel、EndNote .enw、Excel）**显式报错**并给出转换建议，
    不静默返回空列表（否则"导入成功但 0 条"会被误读成"库里没有文献"）。
    """
    src = infer_source(path, source)
    if not os.path.isfile(path):
        raise ValueError("文件不存在：%s" % path)
    ext = os.path.splitext(path)[1].lower()
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        raw = f.read()

    if ext == ".json" or raw.lstrip().startswith(("{", "[")):
        try:
            data = json.loads(raw)
        except ValueError as e:
            raise ValueError("JSON 解析失败（%s）：%s" % (path, e))
        if isinstance(data, dict):
            recs = data.get("works") or data.get("records") or data.get("items") or []
        elif isinstance(data, list):
            recs = data
        else:
            raise ValueError("JSON 顶层既非对象也非数组：%s" % path)
        if not isinstance(recs, list):
            raise ValueError("JSON 中 works/records 不是数组：%s" % path)
    elif ext in (".ris", ".txt") or raw.lstrip().startswith("TY  -"):
        recs = parse_ris(raw)
    else:
        raise ValueError(
            "不支持的中文库导出格式（%s）。请从 CNKI/万方/SinoMed 选择「导出 → RIS」"
            "或「导出 → JSON」。NoteExpress(.nel)/EndNote(.enw)/Excel 需先转换。"
            % (ext or "unknown"))

    works = []
    for r in recs:
        if not isinstance(r, dict):
            continue
        t = (r.get("title") or r.get("题名") or r.get("TI") or "").strip()
        if not t:
            continue
        w = {
            "title": t,
            "doi": (r.get("doi") or r.get("DOI") or "").strip() or None,
            "authors": r.get("authors") or r.get("作者") or [],
            "publication": r.get("publication") or r.get("刊名") or r.get("journal"),
            "abstract_snippet": (r.get("abstract_snippet") or r.get("abstract")
                                 or r.get("摘要") or "")[:1200] or None,
            "url": r.get("url") or None,
            "type": "article",
            "study_type": None,
            "source": src,
            "language": "zh" if has_cjk(t) else (r.get("language") or None),
        }
        y = r.get("year") or r.get("年")
        if y:
            m = re.search(r"(1[6-9]\d{2}|20\d{2})", str(y))
            if m:
                w["year"] = int(m.group(1))
        if isinstance(w["authors"], str):
            w["authors"] = [a.strip() for a in re.split(r"[;；,，]", w["authors"]) if a.strip()]
        works.append({k: v for k, v in w.items() if v not in (None, "", [])})
    return works, src


def annotate(works):
    """给每条 work 打 `title_norm`（CJK 归一 key）与 `cn_ref=True`（幂等）。"""
    n = 0
    for w in works:
        if not isinstance(w, dict):
            continue
        tn = title_key(w)
        if tn:
            w["title_norm"] = tn
            w["cn_ref"] = True
            n += 1
    return n


def payload_from_file(path, source=None, query=None):
    """→ ct-literature source payload（可直接并入 normalize.merge 的 payloads 列表）。"""
    works, src = load_cn_export(path, source=source)
    annotate(works)
    return {
        "source": src,
        "query": query or os.path.basename(path),
        "count": len(works),
        "works": works,
        "imported_from": os.path.abspath(path),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Import a user-exported Chinese-database file (RIS/JSON) as a "
                    "ct-literature source payload. Offline: no site access, no crawling.")
    ap.add_argument("--in", dest="inp", help="exported RIS/JSON file")
    ap.add_argument("--source", default=None, choices=["CNKI", "WanFang", "SinoMed", "VIP"],
                    help="explicit source name (else inferred from filename)")
    ap.add_argument("--out", default=None, help="write payload JSON here")
    ap.add_argument("--title", default=None, help="just normalize one title and print it")
    args = ap.parse_args()

    if args.title:
        print(normalize_cn_title(args.title))
        return 0
    if not args.inp:
        ap.error("需要 --in 或 --title")
    try:
        payload = payload_from_file(args.inp, source=args.source)
    except ValueError as e:
        print("[ERROR] %s" % e, file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] %s import: %d works -> %s" % (payload["source"], payload["count"], args.out))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
