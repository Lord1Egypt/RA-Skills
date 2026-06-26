#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运势计算模块 - 基于农历日历的每日运势分析
"""

import datetime as dt
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any, List, Dict, Optional

try:
    from lunar_python import Solar
except ImportError:
    raise ImportError("请安装 lunar_python: pip install lunar-python")


# =========================
# 配置
# =========================

import os

# 获取用户数据目录（跨平台兼容）
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw")
BIRTHDAY_FILE = os.path.join(USER_DATA_DIR, "fortune_birthday.json")


# =========================
# 生日存储
# =========================

def load_birthday() -> Optional[dict]:
    """加载保存的生日"""
    try:
        with open(BIRTHDAY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def save_birthday(birth_date: str, calendar_type: str) -> None:
    """保存生日

    Args:
        birth_date: 生日 YYYY-MM-DD
        calendar_type: 历法类型 "solar"(阳历) 或 "lunar"(阴历)
    """
    data = {
        "birth_date": birth_date,
        "calendar_type": calendar_type,  # solar 或 lunar
    }
    with open(BIRTHDAY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_ask_birthday_prompt() -> str:
    """获取询问生日的提示语"""
    return """🎂 请告诉我你的生日，我帮你算今日运势～

请按以下格式输入：
- 阳历生日：1990-01-15
- 阴历生日：1990-01-15（阴历）

或者直接说"我的生日是1990年1月15日（阳历/阴历）" """


# =========================
# 基础常量
# =========================

CONSTELLATION_RANGES = [
    ((1, 20), "摩羯座"), ((2, 19), "水瓶座"), ((3, 21), "双鱼座"),
    ((4, 20), "白羊座"), ((5, 21), "金牛座"), ((6, 22), "双子座"),
    ((7, 23), "巨蟹座"), ((8, 23), "狮子座"), ((9, 23), "处女座"),
    ((10, 24), "天秤座"), ((11, 23), "天蝎座"), ((12, 22), "射手座"),
    ((12, 32), "摩羯座"),
]

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ANIMAL_TO_BRANCH = {
    "鼠": "子", "牛": "丑", "虎": "寅", "兔": "卯", "龙": "辰", "龍": "辰",
    "蛇": "巳", "马": "午", "羊": "未", "猴": "申", "鸡": "酉", "狗": "戌", "猪": "亥",
}

STEM_TO_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

ELEMENT_PROFILE = {
    "木": {"colors": ["绿色", "青色"], "numbers": [3, 8], "directions": ["正东", "东南"]},
    "火": {"colors": ["红色", "紫色"], "numbers": [2, 7], "directions": ["正南"]},
    "土": {"colors": ["黄色", "棕色"], "numbers": [5, 10], "directions": ["中宫", "西南", "东北"]},
    "金": {"colors": ["白色", "金色", "银色"], "numbers": [4, 9], "directions": ["正西", "西北"]},
    "水": {"colors": ["黑色", "蓝色"], "numbers": [1, 6], "directions": ["正北"]},
}

CHONG_PAIRS = {
    frozenset(("子", "午")), frozenset(("丑", "未")), frozenset(("寅", "申")),
    frozenset(("卯", "酉")), frozenset(("辰", "戌")), frozenset(("巳", "亥")),
}
LIUHE_PAIRS = {
    frozenset(("子", "丑")), frozenset(("寅", "亥")), frozenset(("卯", "戌")),
    frozenset(("辰", "酉")), frozenset(("巳", "申")), frozenset(("午", "未")),
}
SANHE_GROUPS = [
    {"申", "子", "辰"}, {"寅", "午", "戌"}, {"亥", "卯", "未"}, {"巳", "酉", "丑"},
]

WEEKDAY_DELTA = {
    0: {"career": +3, "wealth": +1},  # 周一
    1: {"career": +2, "love": +1},    # 周二
    2: {"career": +2, "health": +1},  # 周三
    3: {"wealth": +2, "career": +1},   # 周四
    4: {"love": +2, "wealth": +1},     # 周五
    5: {"love": +3, "health": +2},    # 周六
    6: {"health": +3, "love": +1},    # 周日
}

# 星座幸运指数（西方占星）
CONSTELLATION_LUCK = {
    "白羊座": {"love": 80, "career": 85, "wealth": 75, "health": 70},
    "金牛座": {"love": 75, "career": 80, "wealth": 85, "health": 75},
    "双子座": {"love": 70, "career": 75, "wealth": 70, "health": 65},
    "巨蟹座": {"love": 85, "career": 70, "wealth": 65, "health": 80},
    "狮子座": {"love": 75, "career": 90, "wealth": 80, "health": 70},
    "处女座": {"love": 70, "career": 85, "wealth": 75, "health": 80},
    "天秤座": {"love": 85, "career": 75, "wealth": 70, "health": 70},
    "天蝎座": {"love": 90, "career": 80, "wealth": 75, "health": 65},
    "射手座": {"love": 70, "career": 75, "wealth": 70, "health": 80},
    "摩羯座": {"love": 65, "career": 90, "wealth": 85, "health": 75},
    "水瓶座": {"love": 70, "career": 75, "wealth": 65, "health": 70},
    "双鱼座": {"love": 85, "career": 65, "wealth": 60, "health": 75},
}

CATEGORY_KEYWORDS_POS = {
    "love": {"嫁娶", "纳采", "订婚", "会友", "祈福", "求嗣"},
    "career": {"开市", "交易", "立券", "开工", "上任", "求官", "赴任", "动土", "开市"},
    "wealth": {"纳财", "开市", "交易", "立券", "置产", "求财", "开市"},
    "health": {"求医", "疗病", "祈福", "斋醮", "沐浴"},
}
CATEGORY_KEYWORDS_NEG = {
    "love": {"嫁娶", "纳采"},
    "career": {"开市", "交易", "立券", "赴任", "上任", "开工"},
    "wealth": {"纳财", "交易", "立券", "置产"},
    "health": {"求医", "疗病", "沐浴"},
}


# =========================
# 数据类
# =========================

@dataclass
class FortuneResult:
    """运势计算结果"""
    query_date: str
    birth_date: str
    constellation: str
    zodiac: str
    lunar_date: str
    ganzhi_day: str
    day_tian_shen: str
    day_tian_shen_luck: str
    auspicious_label: str
    yi: List[str]
    ji: List[str]
    # 命理评分（基于生肖、五行、值神、宜忌）
    scores_mingli: Dict[str, int]
    # 星座评分（基于星座+当日星期）
    scores_constellation: Dict[str, int]
    # 综合评分
    scores_overall: Dict[str, int]
    lucky_color: str
    lucky_number: int
    lucky_direction: str
    advice: str

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def to_text(self, style: str = "simple") -> str:
        """转换为文本格式

        Args:
            style: simple(简单) / detailed(详细) / share(分享)
        """
        if style == "simple":
            return self._format_simple()
        elif style == "detailed":
            return self._format_detailed()
        elif style == "share":
            return self._format_share()
        else:
            return self._format_simple()

    def _format_simple(self) -> str:
        """简单格式"""
        lines = [
            f"📅 {self.query_date} 运势",
            f"🎂 {self.birth_date} | {self.constellation} | {self.zodiac}生肖",
            f"",
            f"💫 判断: {self.auspicious_label}",
            f"📊 总运: {self.scores_overall['overall']}/99",
            f"🍀 幸运: {self.lucky_color} | {self.lucky_number} | {self.lucky_direction}",
            f"💡 {self.advice[:50]}...",
        ]
        return "\n".join(lines)

    def _format_detailed(self) -> str:
        """详细格式"""
        lines = [
            "=" * 48,
            f"📅 查询日期: {self.query_date}",
            f"🎂 出生日期: {self.birth_date}",
            f"🎯 星座: {self.constellation} | 生肖: {self.zodiac}",
            f"📆 农历: {self.lunar_date}",
            f"🔯 干支日: {self.ganzhi_day}",
            f"✨ 值神: {self.day_tian_shen} ({self.day_tian_shen_luck})",
            f"📋 黄历判断: {self.auspicious_label}",
            "-" * 48,
            f"🎯 总运: {self.scores_overall['overall']}/99",
            f"💕 爱情: {self.scores_overall['love']}/99",
            f"💼 事业: {self.scores_overall['career']}/99",
            f"💰 财运: {self.scores_overall['wealth']}/99",
            f"❤️ 健康: {self.scores_overall['health']}/99",
            "-" * 48,
            f"🍀 幸运色: {self.lucky_color}",
            f"🔢 幸运数字: {self.lucky_number}",
            f"🧭 幸运方位: {self.lucky_direction}",
            f"✅ 宜: {('、'.join(self.yi[:5]) if self.yi else '无')}",
            f"❌ 忌: {('、'.join(self.ji[:5]) if self.ji else '无')}",
            "-" * 48,
            f"💡 建议: {self.advice}",
            "=" * 48,
        ]
        return "\n".join(lines)

    def _format_share(self) -> str:
        """分享格式（适合发朋友圈/社区）"""
        # 运势emoji
        score = self.scores_overall['overall']
        if score >= 85:
            score_emoji = "🌟🌟🌟🌟🌟"
        elif score >= 72:
            score_emoji = "🌟🌟🌟🌟"
        elif score >= 60:
            score_emoji = "🌟🌟🌟"
        else:
            score_emoji = "🌟🌟"

        # 命理评分
        ml = self.scores_mingli
        cs = self.scores_constellation

        lines = [
            f"📅 {self.query_date} 运势指南",
            "",
            f"🎂 {self.birth_date} | {self.constellation} | {self.zodiac}🐴",
            "",
            f"💫 今日判断: {self.auspicious_label}",
            "",
            f"📊 综合运势 {score_emoji}（总运: {self.scores_overall['overall']}/99）",
            "",
            f"🏮 命理评分（生肖+五行+值神）",
            f"   💕 爱情: {ml['love']} | 💼 事业: {ml['career']} | 💰 财运: {ml['wealth']} | ❤️ 健康: {ml['health']}",
            "",
            f"🌟 星座评分（{self.constellation}+星期）",
            f"   💕 爱情: {cs['love']} | 💼 事业: {cs['career']} | 💰 财运: {cs['wealth']} | ❤️ 健康: {cs['health']}",
            "",
            f"🍀 今日幸运",
            f"   颜色: {self.lucky_color} | 数字: {self.lucky_number} | 方位: {self.lucky_direction}",
            "",
            f"📋 宜忌提醒",
            f"   ✅ 宜: {('、'.join(self.yi[:4]) if self.yi else '无')}",
            f"   ⚠️ 忌: {('、'.join(self.ji[:4]) if self.ji else '无')}",
            "",
            f"💡 {self.advice[:80]}{'...' if len(self.advice) > 80 else ''}",
        ]
        return "\n".join(lines)


# =========================
# 工具函数
# =========================

def clamp(x: int, lo: int = 1, hi: int = 99) -> int:
    return max(lo, min(hi, x))


def parse_date(s: str) -> dt.date:
    """解析日期字符串"""
    if not s:
        return dt.date.today()
    return dt.datetime.strptime(s.strip(), "%Y-%m-%d").date()


def get_constellation(month: int, day: int) -> str:
    for (m_limit, d_limit), name in CONSTELLATION_RANGES:
        if (month, day) < (m_limit, d_limit):
            return name
    return "摩羯座"


def call_first(obj: Any, names: List[str], default=None):
    """尝试调用对象的多个方法，返回第一个非空结果"""
    for n in names:
        if hasattr(obj, n):
            try:
                v = getattr(obj, n)()
                if v is not None:
                    return v
            except Exception:
                pass
    return default


def normalize_items(v: Any) -> List[str]:
    """标准化宜忌列表"""
    if v is None:
        return []
    if isinstance(v, str):
        s = v.replace("，", " ").replace(",", " ").strip()
        return [x for x in s.split() if x and x != "无"]
    if isinstance(v, (list, tuple, set)):
        out = []
        for x in v:
            if isinstance(x, str):
                x = x.strip()
                if x and x != "无":
                    out.append(x)
        return out
    return []


def zodiac_relation_delta(birth_branch: str, day_branch: str) -> Dict[str, int]:
    """计算生肖与日支的关系影响"""
    if not birth_branch or not day_branch:
        return {}

    pair = frozenset((birth_branch, day_branch))
    delta = {}

    if pair in CHONG_PAIRS:
        delta = {"love": -8, "career": -6, "wealth": -6, "health": -4}
    elif pair in LIUHE_PAIRS:
        delta = {"love": +7, "career": +5, "wealth": +5, "health": +3}
    else:
        for g in SANHE_GROUPS:
            if birth_branch in g and day_branch in g:
                delta = {"love": +4, "career": +4, "wealth": +4, "health": +2}
                break

    if birth_branch == day_branch:
        delta = {k: delta.get(k, 0) + 2 for k in ["love", "career", "wealth", "health"]}

    return delta


def keyword_delta(yi: List[str], ji: List[str]) -> Dict[str, int]:
    """计算宜忌关键词影响"""
    res = {"love": 0, "career": 0, "wealth": 0, "health": 0}

    yi_set, ji_set = set(yi), set(ji)
    for cat in res.keys():
        pos_hit = len(yi_set & CATEGORY_KEYWORDS_POS[cat])
        neg_hit = len(ji_set & CATEGORY_KEYWORDS_NEG[cat])
        res[cat] += min(pos_hit * 2, 8)
        res[cat] -= min(neg_hit * 2, 8)

    return res


def choose_deterministic(options: List[Any], seed_key: str) -> Any:
    """确定性选择（给定种子总是返回相同结果）"""
    if not options:
        return None
    h = hashlib.sha256(seed_key.encode("utf-8")).hexdigest()
    idx = int(h[:8], 16) % len(options)
    return options[idx]


def build_advice(overall: int, luck: str, yi: List[str], ji: List[str]) -> str:
    """生成建议文案"""
    if overall >= 85:
        tone = "今日气场强，适合推进关键事项。"
    elif overall >= 72:
        tone = "今日整体顺，按计划执行即可。"
    elif overall >= 60:
        tone = "今日平稳，宜先易后难。"
    else:
        tone = "今日宜稳不宜激进，重大决策建议延后。"

    if "吉" in (luck or ""):
        luck_text = "值日偏吉，可处理合作、签约、见面沟通。"
    elif "凶" in (luck or ""):
        luck_text = "值日偏凶，尽量避免硬碰硬和高风险投入。"
    else:
        luck_text = "值日中性，重在执行与节奏管理。"

    yi_text = f"宜：{('、'.join(yi[:4]) if yi else '无特别')}"
    ji_text = f"忌：{('、'.join(ji[:4]) if ji else '无特别')}"

    return f"{tone}{luck_text}{yi_text}；{ji_text}。"


# =========================
# 核心类
# =========================

class FortuneCalculator:
    """运势计算器"""

    def get_saved_birthday(self) -> Optional[tuple]:
        """获取已保存的生日

        Returns:
            (birth_date, calendar_type) 或 None
        """
        data = load_birthday()
        if data:
            return (data.get("birth_date"), data.get("calendar_type", "solar"))
        return None

    def calculate(
        self,
        birth_date: Optional[str] = None,
        query_date: Optional[str] = None,
        calendar_type: str = "solar"
    ) -> FortuneResult:
        """计算运势

        Args:
            birth_date: 出生日期，格式 YYYY-MM-DD
            query_date: 查询日期，格式 YYYY-MM-DD（默认今天）

        Returns:
            FortuneResult: 运势计算结果
        """
        # 优先使用已保存的生日
        if not birth_date:
            saved = self.get_saved_birthday()
            if saved:
                birth_date, calendar_type = saved
            else:
                raise ValueError("NEED_BIRTHDAY")

        # 解析日期
        birth = parse_date(birth_date)
        query = parse_date(query_date) if query_date else dt.date.today()

        # 查询日历法
        solar_q = Solar.fromYmd(query.year, query.month, query.day)
        lunar_q = solar_q.getLunar()

        lunar_date = call_first(lunar_q, ["toFullString", "toString"], "")
        ganzhi_day = call_first(lunar_q, ["getDayInGanZhiExact", "getDayInGanZhi"], "")
        day_tian_shen = call_first(lunar_q, ["getDayTianShen"], "")
        day_tian_shen_luck = call_first(lunar_q, ["getDayTianShenLuck"], "")
        yi = normalize_items(call_first(lunar_q, ["getDayYi"], []))
        ji = normalize_items(call_first(lunar_q, ["getDayJi"], []))

        # 生日历法（用于生肖）
        # 如果是阴历，需要转换为阳历
        if calendar_type == "lunar":
            # 阴历生日转阳历
            try:
                from lunar_python import Lunar
                lunar_birth = Lunar.fromYmd(birth.year, birth.month, birth.day)
                solar_b = lunar_birth.getSolar()
                birth = dt.date(solar_b.getYear(), solar_b.getMonth(), solar_b.getDay())
            except:
                pass  # 转换失败时使用原始日期

        solar_b = Solar.fromYmd(birth.year, birth.month, birth.day)
        lunar_b = solar_b.getLunar()
        zodiac = call_first(lunar_b, ["getYearShengXiao"], "") or "未知"

        constellation = get_constellation(birth.month, birth.day)

        # ============ 命理评分（传统黄历）============
        # 基础分
        scores_ml = {"love": 68, "career": 70, "wealth": 67, "health": 72}

        # 1) 值神吉凶影响
        if "吉" in (day_tian_shen_luck or ""):
            for k in scores_ml:
                scores_ml[k] += 6
        elif "凶" in (day_tian_shen_luck or ""):
            for k in scores_ml:
                scores_ml[k] -= 6

        # 2) 生肖与日支关系
        day_branch = ganzhi_day[-1] if ganzhi_day and ganzhi_day[-1] in BRANCHES else ""
        birth_branch = ANIMAL_TO_BRANCH.get(zodiac, "")
        zr = zodiac_relation_delta(birth_branch, day_branch)
        for k, v in zr.items():
            scores_ml[k] += v

        # 3) 宜忌关键词影响
        kd = keyword_delta(yi, ji)
        for k, v in kd.items():
            scores_ml[k] += v

        # 归一
        for k in scores_ml:
            scores_ml[k] = clamp(scores_ml[k])

        # 命理总分
        overall_ml = clamp(int(
            scores_ml["love"] * 0.25 +
            scores_ml["career"] * 0.30 +
            scores_ml["wealth"] * 0.25 +
            scores_ml["health"] * 0.20
        ))

        # ============ 星座评分（西方占星）============
        # 基础分：取星座先天运势
        const_luck = CONSTELLATION_LUCK.get(constellation, {"love": 70, "career": 70, "wealth": 70, "health": 70})
        scores_cs = dict(const_luck)

        # 星期影响（当日能量）
        wd_delta = WEEKDAY_DELTA.get(query.weekday(), {})
        for k, v in wd_delta.items():
            scores_cs[k] = clamp(scores_cs[k] + v)

        # 归一
        for k in scores_cs:
            scores_cs[k] = clamp(scores_cs[k])

        # 星座总分
        overall_cs = clamp(int(
            scores_cs["love"] * 0.25 +
            scores_cs["career"] * 0.30 +
            scores_cs["wealth"] * 0.25 +
            scores_cs["health"] * 0.20
        ))

        # ============ 综合评分（两者平均）============
        overall = clamp(int((overall_ml + overall_cs) / 2))
        scores = {
            "love": clamp(int((scores_ml["love"] + scores_cs["love"]) / 2)),
            "career": clamp(int((scores_ml["career"] + scores_cs["career"]) / 2)),
            "wealth": clamp(int((scores_ml["wealth"] + scores_cs["wealth"]) / 2)),
            "health": clamp(int((scores_ml["health"] + scores_cs["health"]) / 2)),
        }

        # 黄道吉日标签
        if "吉" in (day_tian_shen_luck or "") and len(yi) >= len(ji):
            auspicious_label = "黄道吉日（宜办大事）"
        elif "吉" in (day_tian_shen_luck or ""):
            auspicious_label = "黄道日（偏吉）"
        elif "凶" in (day_tian_shen_luck or "") and len(ji) > len(yi):
            auspicious_label = "黑道日（诸事慎行）"
        else:
            auspicious_label = "平日（按宜忌行事）"

        # 幸运元素（基于日干五行）
        day_stem = ganzhi_day[0] if ganzhi_day else ""
        element = STEM_TO_ELEMENT.get(day_stem, "土")
        profile = ELEMENT_PROFILE[element]

        seed_base = f"{birth.isoformat()}|{query.isoformat()}|{ganzhi_day}|{zodiac}"
        lucky_color = choose_deterministic(profile["colors"], seed_base + "|color")
        lucky_number = choose_deterministic(profile["numbers"], seed_base + "|num")
        lucky_direction = choose_deterministic(profile["directions"], seed_base + "|dir")

        advice = build_advice(overall, day_tian_shen_luck, yi, ji)

        return FortuneResult(
            query_date=query.isoformat(),
            birth_date=birth.isoformat(),
            constellation=constellation,
            zodiac=zodiac,
            lunar_date=lunar_date,
            ganzhi_day=ganzhi_day,
            day_tian_shen=day_tian_shen or "未知",
            day_tian_shen_luck=day_tian_shen_luck or "平",
            auspicious_label=auspicious_label,
            yi=yi,
            ji=ji,
            scores_mingli={
                "overall": overall_ml,
                "love": scores_ml["love"],
                "career": scores_ml["career"],
                "wealth": scores_ml["wealth"],
                "health": scores_ml["health"],
            },
            scores_constellation={
                "overall": overall_cs,
                "love": scores_cs["love"],
                "career": scores_cs["career"],
                "wealth": scores_cs["wealth"],
                "health": scores_cs["health"],
            },
            scores_overall={
                "overall": overall,
                "love": scores["love"],
                "career": scores["career"],
                "wealth": scores["wealth"],
                "health": scores["health"],
            },
            lucky_color=lucky_color,
            lucky_number=lucky_number,
            lucky_direction=lucky_direction,
            advice=advice
        )


# =========================
# CLI 入口
# =========================

def main():
    print("=== 每日运势完整版（历法规则版）===")
    print("日期格式：YYYY-MM-DD")

    b = input("请输入生日：").strip()
    q = input("请输入查询日期（留空=今天）：").strip() or None

    try:
        calc = FortuneCalculator()
        result = calc.calculate(b, q)

        print("\n" + result.to_text(style="detailed"))

    except Exception as e:
        print(f"计算出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
