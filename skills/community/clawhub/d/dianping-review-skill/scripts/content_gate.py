#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
content_gate.py — 发布前内容门禁（智能体铁律的代码化）

用法:
  content_gate.py --title "标题" --body "正文" [--kind note|review] [--facts facts.json]
                  [--per-capita 55] [--shop 店名] [--writer-dir DIR] [--json]

两级检查：
  block（任一不过 → 退出码 1，拒绝发布）
    1. 广告法极限词（「第一次」「最好提前」等日常表达已豁免）
    2. 站外导流（微信号/二维码/私聊/手机号…）
    3. 网感堆砌词（AI 味）
    4. 数字有出处：正文/标题里的每个数字都必须出现在事实卡 facts 中（防编造）
    5. 第一人称锚点 ≥ 2
    6. 正文字数硬区间；笔记标题必填
    7. 人均一致：正文写的「人均 X」必须和人均栏（--per-capita 或 facts.per_capita）对得上
    8. 硬推销词（赶紧冲、错过后悔…）：引导消费靠信息，不靠喊
    9. 商家口吻（限时优惠、本店、为您打造…）：消费者不替商家传话
   10. AI 腔套话（值得一提的是、总的来说、不仅…更是…）
   11. 写作规范（运行时依赖 hekouwang-writer-skill >= 1.1.0，见 writer_bridge.py）：
       锯末词超密度、必拆长句、身份证号/手机号、结构硬错误、算术对账；依赖缺失也拦
  warn（提示修改，不拦截）
    信息密度（数字 ≥ 2）、感叹号 ≤ 1、emoji ≤ 3、推荐字数区间、推荐标题长度、
    结尾提问、开头卖点与同店已发内容重复（--shop 时读发布回执）、
    品类必写信息（按 facts.category 查 references/category_rules.json）、
    行动信息（怎么买 / 什么时候去 / 怎么去）、写了不适合谁、
    破折号 ≤ 1、排比三连、句长过于整齐、
    写作规范的长句告警、分句堆叠、分号密度、未超密度的锯末词

事实卡 facts：访谈 + 照片识别得到的结构化事实（任意 JSON），例如
  {"shop": "莫摧咖啡（三圣乡店）", "per_capita": 38, "items": ["脏脏拿铁 32 元"],
   "notes": ["等位 15 分钟", "两个人", "2 楼有露台"]}
facts 里的中文数字会换算后参与匹配（「两个人」允许正文写「2 个人」）。

退出码: 0=PASS 1=FAIL 2=参数错误
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from textmatch import fuzzy_in, normalize, split_shop  # noqa: E402
from writer_bridge import writer_checks  # noqa: E402

RECEIPTS = Path.home() / ".dianping-companion" / "receipts"
CATEGORY_RULES = Path(__file__).parent.parent / "references" / "category_rules.json"

ABSOLUTE_WORDS = [
    "最好吃", "最好", "最佳", "最优", "最强", "最低价", "最便宜",
    "第一", "全网第一", "销量第一", "排名第一", "TOP1", "top1",
    "顶级", "极致", "极品", "绝无仅有", "独一无二", "空前绝后",
    "全国领先", "世界领先", "领先全球", "行业领先",
    "秒杀全网", "秒杀同行", "碾压", "吊打",
    "百分百", "100%有效", "包治", "根治", "立竿见影",
    "国家级", "世界级", "宇宙级", "全国首家", "全网首家",
    "独家", "独家秘方", "史上最", "史上全",
]

# 含极限词字面、但在点评里是日常表达的短语，匹配前先剔除
ABSOLUTE_EXEMPT = [
    "第一次", "第一口", "第一个", "第一天", "第一眼", "第一份", "第一道", "第一杯",
    "第一印象", "第一批", "第一层", "第一排", "第一站", "第一波", "第一轮", "第一桌",
    "最好提前", "最好早", "最好别", "最好避开", "最好预约", "最好错峰", "最好带",
    "最好先", "最好不要", "最好是",
]

# VX/vx 简写只在有联系意图的语境里才拦：加VX / VX号 / VX: 内容；光秃秃一个 VX 不拦
DIVERSION_RE = re.compile(
    r"微信号|加微信|加\s*[vV]\b|加\s*[vV][xX]|[vV][xX]\s*号|[vV][xX]\s*[:：]\s*\S|[wW][xX]号"
    r"|二维码|私聊|私信我|加我|[qQ][qQ]\s*\d|1[3-9]\d{9}"
)

AI_FLAVOR_WORDS = [
    "绝绝子", "yyds", "宝藏店铺", "谁懂啊", "家人们",
    "狠狠爱住", "狠狠心动", "无限回购", "神仙", "天花板",
    "被硬控", "硬控我", "拿捏了", "闭眼入",
    "无脑冲", "冲就完了", "听我的", "求求了", "救命!!", "救命！！",
]

HARD_SELL_WORDS = [
    "赶紧冲", "快去买", "快冲", "速冲", "冲鸭", "赶紧下单", "抓紧下单", "手慢无", "先到先得",
    "错过后悔", "错过等一年", "不去血亏", "不买后悔", "不来后悔", "必须安排", "一定要去", "强烈推荐",
]

MERCHANT_VOICE_WORDS = [
    "限时优惠", "限时特价", "下单立减", "下单即送", "到店即送", "欢迎光临", "欢迎大家",
    "本店", "我们店", "为您带来", "为您打造", "竭诚", "敬请", "期待您的光临",
]

AI_CLICHE_WORDS = [
    "值得一提的是", "总的来说", "总而言之", "综上所述", "不得不说", "毫无疑问",
    "让人流连忘返", "回味无穷", "满满的幸福感", "氛围感拉满", "性价比超高", "体验感很好",
    "生活态度", "治愈心灵", "匠心", "沉浸式", "打造", "一场味蕾的", "味蕾的盛宴", "视觉盛宴",
]
AI_SUBLIME_RE = re.compile(r"不仅仅?是.{0,16}更是|不只是.{0,16}更是|这不是.{0,12}而是一种")

ACTION_SLOTS = {
    "怎么买": ["团购", "套餐", "原价", "必点", "点了", "点的", "建议点", "买了", "人均", "元", "免费"],
    "什么时候去": ["工作日", "周末", "上午", "下午", "中午", "晚上", "人少", "错峰", "预约", "排队", "等位", "点前", "点后", "点以后"],
    "怎么去": ["地铁", "公交", "停车", "自驾", "打车", "步行", "公里", "号门", "出口", "导航"],
}
NOT_FOR_RE = re.compile(r"不适合|不太适合|不建议|不推荐|介意.{0,8}(的话|慎)|慎重|慎选|避雷|别点|不用点")
DASH_LIMIT = 1
CLAUSE_SPLIT_RE = re.compile(r"[，,。；;！!？?\n]")
SENTENCE_SPLIT_RE = re.compile(r"[。！!？?\n]")

FIRST_PERSON_RE = re.compile(r"我们|我|本人")
EXCLAMATION_LIMIT = 1
EMOJI_LIMIT = 3

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F02F"
    "\U00002600-\U000026FF\U0001F1E6-\U0001F1FF]"
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
QUESTION_RE = re.compile(r"[?？]")
PER_CAPITA_RE = re.compile(
    r"人均\s*约?\s*[¥￥]?\s*(\d+(?:\.\d+)?)(?:\s*[-–—~～至到]\s*(\d+(?:\.\d+)?))?")
AUDIENCE_WORDS = ["亲子", "带娃", "遛娃", "宝宝", "小朋友", "情侣", "约会", "一个人", "独自",
                  "打工人", "学生", "家庭", "朋友", "闺蜜", "老人", "团建", "办公"]
HOOK_SHARED_NUMBERS = 2
HOOK_SHARED_BIGRAMS = 4

# hard: 出界即 block；soft: 推荐区间，出界 warn
KIND_RULES = {
    "review": {"body_hard": (140, 600), "body_soft": (200, 400), "title_hard": None, "title_soft": None},
    "note":   {"body_hard": (300, 1500), "body_soft": (400, 1000), "title_hard": (6, 22), "title_soft": (15, 20)},
}

_CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
              "六": 6, "七": 7, "八": 8, "九": 9}
_CN_NUM_RE = re.compile(r"[零一二两三四五六七八九十百]+")


def _cn_to_int(s: str):
    if not s:
        return None
    total, cur = 0, 0
    for ch in s:
        if ch in _CN_DIGITS:
            cur = _CN_DIGITS[ch]
        elif ch == "十":
            total += (cur or 1) * 10
            cur = 0
        elif ch == "百":
            total += (cur or 1) * 100
            cur = 0
    return total + cur


def cn_numerals_to_arabic(text: str) -> str:
    return _CN_NUM_RE.sub(lambda m: str(_cn_to_int(m.group(0))), text)


def _num_key(s: str) -> float:
    return float(s)


def fact_numbers(facts) -> set:
    raw = facts if isinstance(facts, str) else json.dumps(facts, ensure_ascii=False)
    raw = cn_numerals_to_arabic(raw)
    return {_num_key(n) for n in NUMBER_RE.findall(raw)}


def count_numbers(text: str) -> int:
    return len(NUMBER_RE.findall(text))


def count_first_person(text: str) -> int:
    return len(FIRST_PERSON_RE.findall(text))


def find_absolute_words(text: str) -> list:
    cleaned = text
    for p in ABSOLUTE_EXEMPT:
        cleaned = cleaned.replace(p, "")
    return sorted({w for w in ABSOLUTE_WORDS if w in cleaned})


def hook_of(title: str, body: str) -> str:
    """开头卖点：笔记取标题，评价取正文首行（评价卡片首行就是读者第一眼）。"""
    if title:
        return title
    first = next((line for line in (body or "").splitlines() if line.strip()), "")
    return first.strip()[:30]


def ends_with_question(body: str) -> bool:
    lines = [line for line in (body or "").splitlines() if line.strip()]
    return bool(lines) and bool(QUESTION_RE.search(lines[-1][-40:]))


def content_features(title: str, body: str, images=None) -> dict:
    title, body = title or "", body or ""
    hook = hook_of(title, body)
    return {
        "body_len": len(body), "title_len": len(title),
        "digits": count_numbers(title + body),
        "first_person": count_first_person(title + body),
        "images": len(images) if images is not None else None,
        "title_has_number": bool(NUMBER_RE.search(title)) if title else None,
        "title_audience": [w for w in AUDIENCE_WORDS if w in title] if title else None,
        "ends_with_question": ends_with_question(body),
        "hook": hook,
    }


def _bigrams(s: str) -> set:
    s = normalize(s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def hook_overlap(hook: str, other: str):
    """两条开头卖点是否在讲同一件事：共用 ≥2 个数字，或共用 ≥4 个双字片段。"""
    shared_nums = set(NUMBER_RE.findall(hook)) & set(NUMBER_RE.findall(other))
    if len(shared_nums) >= HOOK_SHARED_NUMBERS:
        return f"共用数字 {sorted(shared_nums, key=float)}"
    shared = _bigrams(hook) & _bigrams(other)
    if len(shared) >= HOOK_SHARED_BIGRAMS:
        return f"共用词 {sorted(shared)}"
    return None


def load_sibling_hooks(shop: str) -> list:
    """同品牌已发布内容的开头卖点（来自发布回执）。"""
    brand = split_shop(shop or "")[0]
    if not brand or not RECEIPTS.exists():
        return []
    out = []
    for f in sorted(RECEIPTS.rglob("receipt-*.json")):
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not fuzzy_in(brand, r.get("shop") or ""):
            continue
        hook = (r.get("features") or {}).get("hook") or r.get("title") or r.get("body_head")
        if hook:
            out.append({"type": r.get("type"), "hook": hook})
    return out


def load_category_rules() -> dict:
    data = json.loads(CATEGORY_RULES.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def resolve_category(hint: str, rules: dict = None):
    """事实卡 category（如「休闲娱乐·陶艺体验」）→ 规则表里第一个 alias 命中的品类。"""
    if not hint:
        return None
    rules = rules or load_category_rules()
    return next((name for name, r in rules.items()
                 if name in hint or any(a in hint for a in r["aliases"])), None)


def missing_category_info(text: str, category: str, rules: dict = None) -> list:
    rules = rules or load_category_rules()
    must = rules[category]["must"]
    return [item for item, words in must.items() if not any(w in text for w in words)]


def find_ai_cliches(text: str) -> list:
    hits = {w for w in AI_CLICHE_WORDS if w in text}
    hits |= {m.group(0) for m in AI_SUBLIME_RE.finditer(text)}
    return sorted(hits)


def missing_action_slots(text: str) -> list:
    return [slot for slot, words in ACTION_SLOTS.items() if not any(w in text for w in words)]


def parallel_runs(text: str) -> list:
    """连续 3 个以上分句用同样的两个字开头，读起来像排比模板。"""
    clauses = [c.strip() for c in CLAUSE_SPLIT_RE.split(text) if len(c.strip()) >= 4]
    runs, i = [], 0
    while i < len(clauses):
        j = i
        while j + 1 < len(clauses) and clauses[j + 1][:2] == clauses[i][:2]:
            j += 1
        if j - i >= 2:
            runs.append(clauses[i][:2])
        i = j + 1
    return runs


def uniform_sentences(text: str) -> bool:
    """5 句以上且句长几乎一样：真人写东西长短句交错。"""
    lens = [len(s.strip()) for s in SENTENCE_SPLIT_RE.split(text) if len(s.strip()) >= 4]
    if len(lens) < 5:
        return False
    mean = sum(lens) / len(lens)
    sd = (sum((n - mean) ** 2 for n in lens) / len(lens)) ** 0.5
    return sd / mean < 0.18


def per_capita_mismatches(text: str, per_capita) -> list:
    if per_capita is None:
        return []
    pc = float(per_capita)
    bad = []
    for m in PER_CAPITA_RE.finditer(text):
        lo = float(m.group(1))
        hi = float(m.group(2)) if m.group(2) else lo
        if not lo <= pc <= hi:
            bad.append(m.group(0))
    return bad


def check(title: str, body: str, kind: str, facts=None, per_capita=None, siblings=None,
          category: str = None, writer_dir: str = None) -> dict:
    title = title or ""
    body = body or ""
    rules = KIND_RULES.get(kind, KIND_RULES["note"])
    if isinstance(facts, dict):
        if per_capita is None:
            per_capita = facts.get("per_capita")
        category = category or resolve_category(facts.get("category", ""))
    text = title + "\n" + body
    results = []

    def add(name, passed, detail, level="block"):
        results.append({"check": name, "pass": bool(passed), "detail": detail, "level": level})

    hit_abs = find_absolute_words(text)
    add("广告法极限词", not hit_abs, f"命中: {hit_abs}" if hit_abs else "无")

    hit_div = sorted(set(DIVERSION_RE.findall(text)))
    add("站外导流", not hit_div, f"命中: {hit_div}" if hit_div else "无")

    hit_ai = sorted({w for w in AI_FLAVOR_WORDS if w.lower() in text.lower()})
    add("AI味堆砌词", not hit_ai, f"命中: {hit_ai}" if hit_ai else "无")

    hit_cliche = find_ai_cliches(text)
    add("AI腔套话", not hit_cliche,
        f"命中: {hit_cliche}（换成具体的事，见 references/style.md）" if hit_cliche else "无")

    hit_sell = sorted({w for w in HARD_SELL_WORDS if w in text})
    add("硬推销", not hit_sell,
        f"命中: {hit_sell}（改成读者能照着做的信息：点什么、几点去、怎么去）" if hit_sell else "无")

    hit_merchant = sorted({w for w in MERCHANT_VOICE_WORDS if w in text})
    add("商家口吻", not hit_merchant, f"命中: {hit_merchant}" if hit_merchant else "无")

    nums = NUMBER_RE.findall(text)
    if facts is None:
        add("数字有出处", False, "未提供事实卡 facts，无法校验数字是否编造", level="warn")
    else:
        allowed = fact_numbers(facts)
        orphan = sorted({n for n in nums if _num_key(n) not in allowed}, key=_num_key)
        add("数字有出处", not orphan,
            f"事实卡中找不到: {orphan}（补进 facts 或从正文删掉）" if orphan else f"{len(nums)} 处全部有出处")

    fp = count_first_person(text)
    add("第一人称锚点≥2", fp >= 2, f"共 {fp} 处")

    lo, hi = rules["body_hard"]
    add(f"正文字数 {lo}–{hi}", lo <= len(body) <= hi, f"实际 {len(body)}")

    if rules["title_hard"]:
        tlo, thi = rules["title_hard"]
        add(f"标题 {tlo}–{thi} 字", tlo <= len(title) <= thi, f"实际 {len(title)} 字")

    if per_capita is not None:
        bad = per_capita_mismatches(text, per_capita)
        add("人均一致", not bad,
            f"正文 {bad} 与人均栏 {float(per_capita):g} 对不上" if bad else f"人均栏 {float(per_capita):g}")

    add("信息密度: 数字≥2", len(nums) >= 2, f"共 {len(nums)} 处", level="warn")

    asks = ends_with_question(body)
    add("结尾提问", asks, "有" if asks else "结尾没有提问，读者不知道该回什么", level="warn")

    miss_action = missing_action_slots(text)
    add("行动信息", len(miss_action) <= 1,
        f"缺: {miss_action}（读者看完要能照着去）" if miss_action else "怎么买、什么时候去、怎么去都写到了",
        level="warn")

    add("写了不适合谁", bool(NOT_FOR_RE.search(text)),
        "写到了" if NOT_FOR_RE.search(text) else "没写不适合谁或避雷，推荐读起来像广告", level="warn")

    dashes = text.count("——") + text.replace("——", "").count("—")
    add(f"破折号≤{DASH_LIMIT}", dashes <= DASH_LIMIT, f"共 {dashes} 个", level="warn")

    runs = parallel_runs(body)
    add("无排比三连", not runs, f"连续同开头: {runs}" if runs else "无", level="warn")

    flat = uniform_sentences(body)
    add("长短句交错", not flat, "句子长短太整齐，拆一句长的或并两句短的" if flat else "有变化", level="warn")

    if category:
        miss = missing_category_info(text, category)
        add(f"品类必写（{category}）", not miss,
            f"缺: {miss}（事实卡里有就补上，没有就问用户）" if miss else "都写到了", level="warn")

    hook = hook_of(title, body)
    dup = [f"{s['type']}「{s['hook']}」{why}" for s in (siblings or [])
           if (why := hook_overlap(hook, s["hook"]))]
    if siblings is not None:
        add("开头卖点不与同店已发重复", not dup,
            f"与 {dup} 重复，换个角度" if dup else f"对比 {len(siblings)} 条同店内容", level="warn")

    ex = text.count("！") + text.count("!")
    add(f"感叹号≤{EXCLAMATION_LIMIT}", ex <= EXCLAMATION_LIMIT, f"共 {ex} 个", level="warn")

    emo = EMOJI_RE.findall(text)
    add(f"emoji≤{EMOJI_LIMIT}", len(emo) <= EMOJI_LIMIT, f"共 {len(emo)} 个", level="warn")

    slo, shi = rules["body_soft"]
    add(f"推荐字数 {slo}–{shi}", slo <= len(body) <= shi, f"实际 {len(body)}", level="warn")

    if rules["title_soft"]:
        slo, shi = rules["title_soft"]
        add(f"推荐标题 {slo}–{shi} 字", slo <= len(title) <= shi, f"实际 {len(title)} 字", level="warn")

    results.extend(writer_checks(text, writer_dir))

    return {
        "kind": kind,
        "pass": all(r["pass"] for r in results if r["level"] == "block"),
        "warnings": [r for r in results if r["level"] == "warn" and not r["pass"]],
        "results": results,
    }


def load_facts(path: str):
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def format_report(report: dict) -> str:
    lines = [f"门禁结果: {'✅ PASS' if report['pass'] else '⛔ FAIL'}  (kind={report['kind']})"]
    for r in report["results"]:
        mark = "✓" if r["pass"] else ("✗" if r["level"] == "block" else "!")
        lines.append(f"  {mark} [{r['level']}] {r['check']}  — {r['detail']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="点评发布前内容门禁")
    ap.add_argument("--title", default="")
    ap.add_argument("--body", required=True)
    ap.add_argument("--kind", default="note", choices=["note", "review"])
    ap.add_argument("--facts", help="事实卡 JSON 文件")
    ap.add_argument("--per-capita", type=float, help="人均栏要填的金额（默认取 facts.per_capita）")
    ap.add_argument("--shop", help="店名：读发布回执，检查开头卖点是否与同店已发内容重复")
    ap.add_argument("--category", help="品类（默认按 facts.category 匹配 references/category_rules.json）")
    ap.add_argument("--writer-dir", help="hekouwang-writer-skill 目录（默认自动查找，见 writer_bridge.py）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    siblings = load_sibling_hooks(args.shop) if args.shop else None
    report = check(args.title, args.body, args.kind, load_facts(args.facts),
                   per_capita=args.per_capita, siblings=siblings, category=args.category,
                   writer_dir=args.writer_dir)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_report(report))
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
