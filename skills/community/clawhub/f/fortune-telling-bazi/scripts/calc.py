#!/usr/bin/env python3
"""
BaZi Core Calculator v6 — Refactored

Architecture (5 layers):
  [1] Constants  — stem/branch/ten-god/na-yin tables (pure data)
  [2] Data model — Pillar, Fate dataclasses
  [3] Helpers    — pure lookup functions
  [4] Core logic — element strength, vitality, afflictions, pillars
  [5] Public API — calculate_fate(), dict_to_fate()

No remote API. Lunar calendar via embedded single-file lunar_core.
"""
import os, sys
from dataclasses import dataclass, field
from typing import List, Dict

# ─── Layer 1: Lunar lib bootstrap ──────────────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

def _lazy_lunar():
    from lunar_core import Lunar
    return Lunar

Lunar = _lazy_lunar()
from lunar_core import Solar


# ════════════════════════════════════════════════════════════════════════════════
# Layer 1: Constants — 天干/地支/五行/神煞/十神/纳音/旬空
# ════════════════════════════════════════════════════════════════════════════════

STEM_ALL = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCH_ALL = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# Stem → element / yin-yang
STEM_ELEMENT = {
    '甲':'木', '乙':'木', '丙':'火', '丁':'火', '戊':'土',
    '己':'土', '庚':'金', '辛':'金', '壬':'水', '癸':'水',
}
STEM_YINYANG = {g: ('阳' if i % 2 == 0 else '阴') for i, g in enumerate(STEM_ALL)}

# Branch → element / yin-yang / hidden-stems
BRANCH_ELEMENT = {
    '子':'水', '丑':'土', '寅':'木', '卯':'木', '辰':'土', '巳':'火',
    '午':'火', '未':'土', '申':'金', '酉':'金', '戌':'土', '亥':'水',
}
BRANCH_YINYANG = {z: ('阳' if i % 2 == 0 else '阴') for i, z in enumerate(BRANCH_ALL)}
BRANCH_HIDDEN: Dict[str, List[str]] = {
    '子':['癸'], '丑':['己','癸','辛'], '寅':['甲','丙','戊'],
    '卯':['乙'], '辰':['戊','乙','癸'], '巳':['丙','庚','戊'],
    '午':['丁','己'], '未':['己','丁','乙'], '申':['庚','壬','戊'],
    '酉':['辛'], '戌':['戊','辛','丁'], '亥':['壬','甲'],
}

# Ten gods (十神) — keyed by day-stem × month-stem → full name
TEN_GOD = {
    '甲':{'甲':'比肩','乙':'劫财','丙':'食神','丁':'伤官','戊':'偏财','己':'正财','庚':'七杀','辛':'正官','壬':'偏印','癸':'正印'},
    '乙':{'甲':'劫财','乙':'比肩','丙':'伤官','丁':'食神','戊':'正财','己':'偏财','庚':'正官','辛':'七杀','壬':'正印','癸':'偏印'},
    '丙':{'甲':'偏印','乙':'正印','丙':'比肩','丁':'劫财','戊':'食神','己':'伤官','庚':'偏财','辛':'正财','壬':'七杀','癸':'正官'},
    '丁':{'甲':'正印','乙':'偏印','丙':'劫财','丁':'比肩','戊':'伤官','己':'食神','庚':'正财','辛':'偏财','壬':'正官','癸':'七杀'},
    '戊':{'甲':'七杀','乙':'正官','丙':'偏印','丁':'正印','戊':'比肩','己':'劫财','庚':'食神','辛':'伤官','壬':'偏财','癸':'正财'},
    '己':{'甲':'正官','乙':'七杀','丙':'正印','丁':'偏印','戊':'劫财','己':'比肩','庚':'伤官','辛':'食神','壬':'正财','癸':'偏财'},
    '庚':{'甲':'偏财','乙':'正财','丙':'七杀','丁':'正官','戊':'偏印','己':'正印','庚':'比肩','辛':'劫财','壬':'食神','癸':'伤官'},
    '辛':{'甲':'正财','乙':'偏财','丙':'正官','丁':'七杀','戊':'正印','己':'偏印','庚':'劫财','辛':'比肩','壬':'伤官','癸':'食神'},
    '壬':{'甲':'食神','乙':'伤官','丙':'偏财','丁':'正财','戊':'七杀','己':'正官','庚':'偏印','辛':'正印','壬':'比肩','癸':'劫财'},
    '癸':{'甲':'伤官','乙':'食神','丙':'正财','丁':'偏财','戊':'正官','己':'七杀','庚':'正印','辛':'偏印','壬':'劫财','癸':'比肩'},
}

# 月支主气藏干表（12地支的本气）
# 十神 → 格局名
TEN_GOD_TO_GE = {
    '正官':'正官格', '七杀':'七杀格',
    '正财':'正财格', '偏财':'偏财格',
    '正印':'正印格', '偏印':'偏印格',
    '食神':'食神格', '伤官':'伤官格',
    '比肩':'比肩格', '劫财':'阳刃格',
}

def calc_mingge(day_stem: str, month_stem: str) -> str:
    """
    Compute 命格 (Ming Ge — fate pattern) from day stem and month stem.

    Standard 格局派 algorithm — 月干十神决定命格：
      1. Look up TEN_GOD[day_stem][month_stem] → ten_god full name.
      2. Map ten_god → 格局 name via TEN_GOD_TO_GE.

    This is the standard 格局派 algorithm: 月干十神决定命格。
    """
    ten_god = TEN_GOD[day_stem][month_stem]
    return TEN_GOD_TO_GE.get(ten_god, ten_god)

# NaYin table (纳音) — (stem,branch) → label
NAYIN = {
    ('甲子','甲午'):'海中金', ('乙丑','甲午'):'海中金',
    ('丙寅','丙申'):'炉中火', ('丁卯','丁酉'):'炉中火',
    ('戊辰','戊戌'):'木大林',   ('己巳','己亥'):'木大林',
    ('庚午','庚子'):'路旁土',   ('辛未','辛丑'):'路旁土',
    ('壬申','壬寅'):'剑锋金',   ('癸酉','癸卯'):'剑锋金',
    ('甲戌','甲辰'):'山头火',   ('乙亥','乙巳'):'山头火',
    ('丙子','丙午'):'涧下水',   ('丁丑','丁未'):'涧下水',
    ('戊寅','戊申'):'城墙土',   ('己卯','己酉'):'城墙土',
    ('庚辰','庚戌'):'白蜡金',   ('辛巳','辛亥'):'白蜡金',
    ('壬午','壬子'):'杨柳木',   ('癸未','癸丑'):'杨柳木',
    ('甲申','甲寅'):'井泉水',   ('乙酉','乙卯'):'井泉水',
    ('丙戌','丙辰'):'屋上土',   ('丁亥','丁巳'):'屋上土',
    ('戊子','戊午'):'霹雳火',   ('己丑','己未'):'霹雳火',
    ('庚寅','庚申'):'松柏木',   ('辛卯','辛酉'):'松柏木',
    ('壬辰','壬戌'):'长流水',   ('癸巳','癸亥'):'长流水',
    ('甲辰','甲戌'):'覆灯火',   ('乙巳','乙亥'):'覆灯火',
    ('丙午','丙子'):'天河水',   ('丁未','丁丑'):'天河水',
    ('戊申','戊寅'):'大驿土',   ('己酉','己卯'):'大驿土',
    ('庚戌','庚辰'):'石榴木',   ('辛亥','辛巳'):'石榴木',
    ('壬子','壬午'):'桑柘木',   ('癸丑','癸未'):'桑柘木',
    ('甲寅','甲申'):'大溪水',   ('乙卯','乙酉'):'大溪水',
    ('丙辰','丙戌'):'砂石土',   ('丁巳','丁亥'):'砂石土',
    ('戊午','戊子'):'天上火',   ('己未','己丑'):'天上火',
    ('庚申','庚寅'):'城头土',   ('辛酉','辛卯'):'城头土',
    ('壬戌','壬辰'):'大海水',   ('癸亥','癸巳'):'大海水',
}

# XunKong table (旬空) — day-pillar → void branches
XUN_KONG = {
    '甲子':'戌亥','甲戌':'申酉','甲申':'午未','甲午':'辰巳','甲辰':'寅卯','甲寅':'子丑',
    '乙丑':'戌亥','乙卯':'申酉','乙巳':'午未','乙未':'辰巳','乙酉':'寅卯','乙亥':'子丑',
    '丙子':'戌亥','丙寅':'申酉','丙辰':'午未','丙午':'辰巳','丙申':'寅卯','丙戌':'子丑',
    '丁丑':'戌亥','丁卯':'申酉','丁巳':'午未','丁未':'辰巳','丁酉':'寅卯','丁亥':'子丑',
    '戊子':'戌亥','戊寅':'申酉','戊辰':'午未','戊午':'辰巳','戊申':'寅卯','戊戌':'子丑',
    '己丑':'戌亥','己卯':'申酉','己巳':'午未','己未':'辰巳','己酉':'寅卯','己亥':'子丑',
    '庚子':'戌亥','庚寅':'申酉','庚辰':'午未','庚午':'辰巳','庚申':'寅卯','庚戌':'子丑',
    '辛丑':'戌亥','辛卯':'申酉','辛巳':'午未','辛未':'辰巳','辛酉':'寅卯','辛亥':'子丑',
    '壬子':'戌亥','壬寅':'申酉','壬辰':'午未','壬午':'辰巳','壬申':'寅卯','壬戌':'子丑',
    '癸丑':'戌亥','癸卯':'申酉','癸巳':'午未','癸未':'辰巳','癸酉':'寅卯','癸亥':'子丑',
}

# Branch relations
BRANCH_HEX = {
    ('子','丑'):'子丑合', ('寅','亥'):'寅亥合', ('卯','戌'):'卯戌合',
    ('辰','酉'):'辰酉合', ('巳','申'):'巳申合', ('午','未'):'午未合',
}
BRANCH_CLASH = {
    ('子','午'):'子午冲', ('丑','未'):'丑未冲', ('寅','申'):'寅申冲',
    ('卯','酉'):'卯酉冲', ('辰','戌'):'辰戌冲', ('巳','亥'):'巳亥冲',
}
BRANCH_PUNISHMENT = {
    ('寅','巳','申'):'寅巳申三刑', ('丑','戌','未'):'丑戌未三刑',
    ('子','卯'):'子卯相刑',
    ('辰','辰'):'辰辰自刑', ('午','午'):'午午自刑',
    ('酉','酉'):'酉酉自刑', ('亥','亥'):'亥亥自刑',
}

# Affliction tables (神煞)
PEACH_BLOSSOM = {
    '寅':'卯', '午':'卯', '戌':'卯', '申':'酉', '子':'酉', '辰':'酉',
    '亥':'子', '卯':'子', '未':'子', '巳':'午', '酉':'午', '丑':'午',
}
TIANYI_NOBLE = {
    '甲':['丑','未'], '戊':['丑','未'], '庚':['丑','未'],
    '乙':['子','申'], '己':['子','申'],
    '丙':['亥','酉'], '丁':['亥','酉'],
    '壬':['卯','巳'], '癸':['卯','巳'],
    '辛':['寅','午'],
}
YIMA_HORSE = {
    '申':'寅', '子':'寅', '辰':'寅',
    '亥':'巳', '卯':'巳', '未':'巳',
    '寅':'申', '午':'申', '戌':'申',
    '巳':'亥', '酉':'亥', '丑':'亥',
}
JIANGXING = {
    '子':'子', '午':'子', '辰':'子', '申':'子', '寅':'子',
    '卯':'酉', '酉':'酉', '丑':'酉', '未':'酉', '巳':'酉', '亥':'酉',
}
JIESHA = {
    '申':'亥', '子':'巳', '丑':'寅', '寅':'申', '卯':'亥',
    '辰':'巳', '巳':'寅', '午':'申', '未':'亥', '酉':'寅',
    '戌':'申', '亥':'巳',
}


# ════════════════════════════════════════════════════════════════════════════════
# Layer 2: Data model
# ════════════════════════════════════════════════════════════════════════════════

@dataclass
class Pillar:
    """
    Single pillar (年/月/日/时).
    stem=天干  branch=地支  stem_el=天干五行  branch_el=地支五行
    yinyang=阴阳  ten_god=十神  na_yin=纳音
    hidden=藏干列表  vacant=旬空
    """
    stem:      str
    branch:    str
    stem_el:   str
    branch_el: str
    yinyang:   str
    ten_god:   str
    na_yin:    str
    hidden:    List[str]
    vacant:    str = ''


@dataclass
class Fate:
    """
    Complete baZi result.
    """
    name:           str
    gender:         str
    birth:          Dict

    year_pillar:    Pillar
    month_pillar:   Pillar
    day_pillar:     Pillar
    hour_pillar:    Pillar
    bazi_str:       str

    lunar_str:      str
    shengxiao:      str

    wuxing_count:   Dict[str, float]

    vitality:       str
    favorable:      str
    mingge:         str
    day_stem:       str
    afflictions:    List[str]
    taiyuan:        str
    taixi:          str
    minggong:       str
    shengong:       str
    qiyun:          Dict
    dayun:          List[Dict]

    # Compatibility aliases
    xiyong:         str = ''
    void:           str = ''
    vacant:         str = ''
    _lunar:         object = field(default=None, repr=False)


# ════════════════════════════════════════════════════════════════════════════════
# Layer 3: Pure helper functions
# ════════════════════════════════════════════════════════════════════════════════

def stem_yinyang(s: str) -> str:
    return STEM_YINYANG.get(s, '')

def branch_yinyang(b: str) -> str:
    return BRANCH_YINYANG.get(b, '')

def stem_element(s: str) -> str:
    return STEM_ELEMENT.get(s, '')

def branch_element(b: str) -> str:
    return BRANCH_ELEMENT.get(b, '')

def branch_hidden(b: str) -> List[str]:
    return BRANCH_HIDDEN.get(b, [])

def lookup_nayin(stem: str, branch: str) -> str:
    """纳音查询"""
    return NAYIN.get((stem, branch),
           NAYIN.get((branch, stem), '土'))

def lookup_xunkong(day_stem: str, day_branch: str) -> str:
    """旬空查询"""
    return XUN_KONG.get(day_stem + day_branch, '')


# ════════════════════════════════════════════════════════════════════════════════
# Layer 4: Core computation
# ════════════════════════════════════════════════════════════════════════════════

# Element strength tables
STEM_STRENGTH = {
    '甲': {'子':1.20,'丑':1.06,'寅':1.14,'卯':1.20,'辰':1.10,'巳':1.00,'午':1.00,'未':1.04,'申':1.06,'酉':1.00,'戌':1.00,'亥':1.20},
    '乙': {'子':1.20,'丑':1.06,'寅':1.14,'卯':1.20,'辰':1.10,'巳':1.00,'午':1.00,'未':1.04,'申':1.06,'酉':1.00,'戌':1.00,'亥':1.20},
    '丙': {'子':1.00,'丑':1.00,'寅':1.20,'卯':1.20,'辰':1.06,'巳':1.14,'午':1.20,'未':1.10,'申':1.00,'酉':1.00,'戌':1.04,'亥':1.00},
    '丁': {'子':1.00,'丑':1.00,'寅':1.20,'卯':1.20,'辰':1.06,'巳':1.14,'午':1.20,'未':1.10,'申':1.00,'酉':1.00,'戌':1.04,'亥':1.00},
    '戊': {'子':1.00,'丑':1.10,'寅':1.06,'卯':1.00,'辰':1.10,'巳':1.14,'午':1.20,'未':1.16,'申':1.00,'酉':1.00,'戌':1.14,'亥':1.00},
    '己': {'子':1.00,'丑':1.10,'寅':1.06,'卯':1.00,'辰':1.10,'巳':1.14,'午':1.20,'未':1.16,'申':1.00,'酉':1.00,'戌':1.14,'亥':1.00},
    '庚': {'子':1.00,'丑':1.14,'寅':1.00,'卯':1.00,'辰':1.10,'巳':1.06,'午':1.00,'未':1.10,'申':1.14,'酉':1.20,'戌':1.16,'亥':1.00},
    '辛': {'子':1.00,'丑':1.14,'寅':1.00,'卯':1.00,'辰':1.10,'巳':1.06,'午':1.00,'未':1.10,'申':1.14,'酉':1.20,'戌':1.16,'亥':1.00},
    '壬': {'子':1.20,'丑':1.10,'寅':1.00,'卯':1.00,'辰':1.04,'巳':1.06,'午':1.00,'未':1.00,'申':1.20,'酉':1.20,'戌':1.06,'亥':1.14},
    '癸': {'子':1.20,'丑':1.10,'寅':1.00,'卯':1.00,'辰':1.04,'巳':1.06,'午':1.00,'未':1.00,'申':1.20,'酉':1.20,'戌':1.06,'亥':1.14},
}

BRANCH_HIDDEN_STRENGTH = {
    '子': {'癸': {'子':1.20,'丑':1.10,'寅':1.00,'卯':1.00,'辰':1.04,'巳':1.06,'午':1.00,'未':1.00,'申':1.20,'酉':1.20,'戌':1.06,'亥':1.14}},
    '丑': {'癸': {'子':0.36,'丑':0.33,'寅':0.30,'卯':0.30,'辰':0.312,'巳':0.318,'午':0.30,'未':0.30,'申':0.36,'酉':0.36,'戌':0.318,'亥':0.342},
           '辛': {'子':0.20,'丑':0.228,'寅':0.20,'卯':0.20,'辰':0.23,'巳':0.212,'午':0.20,'未':0.22,'申':0.228,'酉':0.248,'戌':0.232,'亥':0.20},
           '己': {'子':0.50,'丑':0.55,'寅':0.53,'卯':0.50,'辰':0.55,'巳':0.57,'午':0.60,'未':0.58,'申':0.50,'酉':0.50,'戌':0.57,'亥':0.50}},
    '寅': {'丙': {'子':0.30,'丑':0.30,'寅':0.36,'卯':0.36,'辰':0.318,'巳':0.342,'午':0.36,'未':0.33,'申':0.30,'酉':0.30,'戌':0.342,'亥':0.318},
           '甲': {'子':0.84,'丑':0.742,'寅':0.798,'卯':0.84,'辰':0.77,'巳':0.70,'午':0.70,'未':0.728,'申':0.742,'酉':0.70,'戌':0.70,'亥':0.84}},
    '卯': {'乙': {'子':1.20,'丑':1.06,'寅':1.14,'卯':1.20,'辰':1.10,'巳':1.00,'午':1.00,'未':1.04,'申':1.06,'酉':1.00,'戌':1.00,'亥':1.20}},
    '辰': {'乙': {'子':0.36,'丑':0.318,'寅':0.342,'卯':0.36,'辰':0.33,'巳':0.30,'午':0.30,'未':0.312,'申':0.318,'酉':0.30,'戌':0.30,'亥':0.36},
           '癸': {'子':0.24,'丑':0.22,'寅':0.20,'卯':0.20,'辰':0.208,'巳':0.20,'午':0.20,'未':0.20,'申':0.24,'酉':0.24,'戌':0.212,'亥':0.228},
           '戊': {'子':0.50,'丑':0.55,'寅':0.53,'卯':0.50,'辰':0.55,'巳':0.60,'午':0.60,'未':0.58,'申':0.50,'酉':0.50,'戌':0.57,'亥':0.50}},
    '巳': {'庚': {'子':0.30,'丑':0.342,'寅':0.30,'卯':0.30,'辰':0.33,'巳':0.30,'午':0.30,'未':0.33,'申':0.342,'酉':0.36,'戌':0.348,'亥':0.30},
           '丙': {'子':0.70,'丑':0.70,'寅':0.84,'卯':0.84,'辰':0.742,'巳':0.84,'午':0.84,'未':0.798,'申':0.70,'酉':0.70,'戌':0.728,'亥':0.742}},
    '午': {'丁': {'子':1.00,'丑':1.00,'寅':1.20,'卯':1.20,'辰':1.06,'巳':1.14,'午':1.20,'未':1.10,'申':1.00,'酉':1.00,'戌':1.04,'亥':1.06}},
    '未': {'丁': {'子':0.30,'丑':0.30,'寅':0.36,'卯':0.36,'辰':0.318,'巳':0.342,'午':0.36,'未':0.33,'申':0.30,'酉':0.30,'戌':0.312,'亥':0.318},
           '乙': {'子':0.24,'丑':0.212,'寅':0.228,'卯':0.24,'辰':0.22,'巳':0.20,'午':0.20,'未':0.208,'申':0.212,'酉':0.20,'戌':0.20,'亥':0.24},
           '己': {'子':0.50,'丑':0.55,'寅':0.53,'卯':0.50,'辰':0.55,'巳':0.57,'午':0.60,'未':0.58,'申':0.50,'酉':0.50,'戌':0.57,'亥':0.50}},
    '申': {'壬': {'子':0.36,'丑':0.33,'寅':0.30,'卯':0.30,'辰':0.312,'巳':0.318,'午':0.30,'未':0.30,'申':0.36,'酉':0.36,'戌':0.318,'亥':0.342},
           '庚': {'子':0.70,'丑':0.798,'寅':0.70,'卯':0.70,'辰':0.77,'巳':0.742,'午':0.70,'未':0.77,'申':0.798,'酉':0.84,'戌':0.812,'亥':0.70}},
    '酉': {'辛': {'子':1.00,'丑':1.14,'寅':1.00,'卯':1.00,'辰':1.10,'巳':1.06,'午':1.00,'未':1.10,'申':1.14,'酉':1.20,'戌':1.16,'亥':1.00}},
    '戌': {'辛': {'子':0.30,'丑':0.342,'寅':0.30,'卯':0.30,'辰':0.33,'巳':0.318,'午':0.30,'未':0.33,'申':0.342,'酉':0.36,'戌':0.348,'亥':0.30},
           '丁': {'子':0.20,'丑':0.20,'寅':0.24,'卯':0.24,'辰':0.212,'巳':0.228,'午':0.24,'未':0.22,'申':0.20,'酉':0.20,'戌':0.208,'亥':0.212},
           '戊': {'子':0.50,'丑':0.55,'寅':0.53,'卯':0.50,'辰':0.55,'巳':0.57,'午':0.60,'未':0.58,'申':0.50,'酉':0.50,'戌':0.57,'亥':0.50}},
    '亥': {'甲': {'子':0.36,'丑':0.318,'寅':0.342,'卯':0.36,'辰':0.33,'巳':0.30,'午':0.30,'未':0.312,'申':0.318,'酉':0.30,'戌':0.30,'亥':0.36},
           '壬': {'子':0.84,'丑':0.77,'寅':0.70,'卯':0.70,'辰':0.728,'巳':0.742,'午':0.70,'未':0.70,'申':0.84,'酉':0.84,'戌':0.724,'亥':0.798}},
}

# Vitality classification
SAME_KIND  = {'金':['金','土'], '木':['木','水'], '水':['水','金'], '火':['火','木'], '土':['土','火']}
DIFF_KIND  = {'金':['木','水','火'],'木':['金','火','土'],'水':['木','火','土'],'火':['金','水','土'],'土':['金','木','水']}
STEM_EL    = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}


def _calc_wuxing_strength(yr_gan, yr_zhi, mo_gan, mo_zhi,
                          dy_gan, dy_zhi, hr_gan, hr_zhi) -> Dict[str, float]:
    """Compute five-element strength scores."""
    strength = {'木':0.0, '火':0.0, '土':0.0, '金':0.0, '水':0.0}
    for stem in [yr_gan, mo_gan, dy_gan, hr_gan]:
        strength[STEM_EL[stem]] += STEM_STRENGTH[stem][mo_zhi]
    for branch in [yr_zhi, mo_zhi, dy_zhi, hr_zhi]:
        if branch in BRANCH_HIDDEN_STRENGTH:
            for h, table in BRANCH_HIDDEN_STRENGTH[branch].items():
                strength[STEM_EL[h]] += table[mo_zhi]
    return {k: round(v, 3) for k, v in strength.items()}


def _assess_vitality_and_favorable(yr_gan, yr_zhi, mo_gan, mo_zhi,
                                    dy_gan, dy_zhi, hr_gan, hr_zhi):
    """
    Assess body-strength (旺衰) and favorable elements (喜用).
    same_kind (self + birth mother) > diff_kind (conqueror + child + exhaustor)
      → strong body → drain (取异类泄)
    same_kind < diff_kind
      → weak body → support (取同类扶)
    Returns: (vitality_label, favorable_string, strength_dict)
    """
    day_el = STEM_EL[dy_gan]
    strength = _calc_wuxing_strength(yr_gan, yr_zhi, mo_gan, mo_zhi,
                                      dy_gan, dy_zhi, hr_gan, hr_zhi)
    same = SAME_KIND[day_el]
    diff = DIFF_KIND[day_el]
    score_same = sum(strength[el] for el in same)
    score_diff = sum(strength[el] for el in diff)

    if score_same > score_diff:
        vitality = '强'
        favorable = diff
    elif score_same < score_diff:
        vitality = '弱'
        favorable = same
    else:
        vitality = '中'
        favorable = same + diff

    return vitality, ' '.join(favorable), strength


def _collect_afflictions(yr_zhi, mo_zhi, dy_zhi, all_branches, dy_gan) -> List[str]:
    """Collect affliction list (神煞)."""
    result = []

    for b in [yr_zhi, dy_zhi]:
        target = PEACH_BLOSSOM.get(b, '')
        if target in all_branches and '桃花' not in result:
            result.append('桃花')

    for nb in TIANYI_NOBLE.get(dy_gan, []):
        if nb in all_branches:
            if '天乙贵人' not in result:
                result.append('天乙贵人')
            break

    for b in [yr_zhi, mo_zhi]:
        horse = YIMA_HORSE.get(b, '')
        if horse and horse in all_branches and '驿马' not in result:
            result.append('驿马')

    for b in [yr_zhi, dy_zhi]:
        general = JIANGXING.get(b, '')
        if general and general in all_branches and '将星' not in result:
            result.append('将星')

    for b in [yr_zhi, mo_zhi]:
        robbery = JIESHA.get(b, '')
        if robbery and robbery in all_branches and '劫煞' not in result:
            result.append('劫煞')

    return result


def _build_pillar(stem, branch, na_yin_val, hidden_list, vacant_val,
                   dy_gan, pillar_name) -> Pillar:
    """Build a Pillar dataclass."""
    return Pillar(
        stem      = stem,
        branch    = branch,
        stem_el   = stem_element(stem),
        branch_el = branch_element(branch),
        yinyang   = stem_yinyang(stem),
        ten_god   = '日主' if pillar_name == 'day' else TEN_GOD.get(dy_gan, {}).get(stem, ''),
        na_yin    = na_yin_val,
        hidden    = hidden_list,
        vacant    = vacant_val,
    )


# ════════════════════════════════════════════════════════════════════════════════
# Layer 5: Public API
# ════════════════════════════════════════════════════════════════════════════════

def _get_lunar_data(year, month, day, hour, minute):
    """Fetch raw lunar data from the local lunar_core module."""
    solar = Solar.fromYmdHms(int(year), int(month), int(day), int(hour), int(minute), 0)
    lunar = solar.getLunar()
    ba    = lunar.getEightChar()
    return solar, lunar, ba


def _compute_fate(name: str, year, month, day, hour, minute, gender) -> Fate:
    """Compute full baZi, return Fate object."""
    solar, lunar, ba = _get_lunar_data(year, month, day, hour, minute)
    gender_num  = 1 if gender in (1, '1', '男') else 0
    gender_str  = '男' if gender_num == 1 else '女'

    yr_stem, yr_zhi   = ba.getYearGan(),  ba.getYearZhi()
    mo_stem, mo_zhi   = ba.getMonthGan(), ba.getMonthZhi()
    dy_stem, dy_zhi   = ba.getDayGan(),   ba.getDayZhi()
    hr_stem, hr_zhi   = ba.getTimeGan(),  ba.getTimeZhi()
    dy_gan = dy_stem

    all_branches = [yr_zhi, mo_zhi, dy_zhi, hr_zhi]

    vitality, favorable, wuxing_strength = _assess_vitality_and_favorable(
        yr_stem, yr_zhi, mo_stem, mo_zhi, dy_stem, dy_zhi, hr_stem, hr_zhi)

    afflictions = _collect_afflictions(yr_zhi, mo_zhi, dy_zhi, all_branches, dy_gan)

    day_ganzhi   = dy_stem + dy_zhi
    void_branches = lookup_xunkong(dy_stem, dy_zhi)

    yr_p = _build_pillar(yr_stem, yr_zhi, ba.getYearNaYin(),
                         ba.getYearHideGan(), ba.getYearXunKong(), dy_gan, 'year')
    mo_p = _build_pillar(mo_stem, mo_zhi, ba.getMonthNaYin(),
                         ba.getMonthHideGan(), ba.getMonthXunKong(), dy_gan, 'month')
    dy_p = _build_pillar(dy_stem, dy_zhi, ba.getDayNaYin(),
                         ba.getDayHideGan(), ba.getDayXunKong(), dy_gan, 'day')
    hr_p = _build_pillar(hr_stem, hr_zhi, ba.getTimeNaYin(),
                         ba.getTimeHideGan(), ba.getTimeXunKong(), dy_gan, 'hour')

    try:
        yun      = ba.getYun(gender_num)
        qiyun_yr = yun.getStartYear()
        qiyun_mo = yun.getStartMonth()
        dayun_list = yun.getDaYun()
        dayun_data = [
            {"ganzhi": d.getGanZhi(), "start_age": d.getStartAge(),
             "end_age": d.getEndAge(), "start_year": d.getStartYear(),
             "vacant": d.getXunKong()}
            for d in dayun_list[:10]
        ]
    except Exception:
        qiyun_yr = qiyun_mo = 0
        dayun_data = []

    return Fate(
        name          = name,
        gender        = gender_str,
        birth         = {"year":int(year),"month":int(month),"day":int(day),
                        "hour":int(hour),"minute":int(minute)},
        year_pillar   = yr_p,
        month_pillar  = mo_p,
        day_pillar    = dy_p,
        hour_pillar   = hr_p,
        bazi_str      = f"{yr_stem}{yr_zhi} {mo_stem}{mo_zhi} {dy_stem}{dy_zhi} {hr_stem}{hr_zhi}",
        lunar_str     = lunar.toString(),
        shengxiao     = lunar.getYearShengXiao(),
        wuxing_count  = wuxing_strength,
        vitality      = vitality,
        favorable     = favorable,
        xiyong        = favorable,
        mingge        = calc_mingge(dy_stem, mo_stem),
        day_stem      = dy_stem,
        afflictions   = afflictions,
        void          = void_branches,
        vacant        = void_branches,
        taiyuan       = ba.getTaiYuan(),
        taixi         = ba.getTaiXi(),
        minggong      = ba.getMingGong(),
        shengong      = ba.getShenGong(),
        qiyun         = {"year": qiyun_yr, "month": qiyun_mo},
        dayun         = dayun_data,
        _lunar        = lunar,
    )


def _fate_to_dict(f: Fate) -> dict:
    """Serialize Fate → dict for JSON storage."""
    return {
        "name":   f.name, "gender": f.gender, "birth": f.birth,
        "bazi": {
            "year":  f.year_pillar.stem  + f.year_pillar.branch,
            "month": f.month_pillar.stem + f.month_pillar.branch,
            "day":   f.day_pillar.stem   + f.day_pillar.branch,
            "hour":  f.hour_pillar.stem  + f.hour_pillar.branch,
        },
        "bazi_str":   f.bazi_str,
        "lunar_str":  f.lunar_str,
        "shengxiao":  f.shengxiao,
        "wuxing": ' '.join([
            f.year_pillar.stem_el  + f.year_pillar.branch_el,
            f.month_pillar.stem_el + f.month_pillar.branch_el,
            f.day_pillar.stem_el   + f.day_pillar.branch_el,
            f.hour_pillar.stem_el  + f.hour_pillar.branch_el,
        ]),
        "wuxing_count": f.wuxing_count,
        "mingge":      f.mingge,
        "wangshuai":   f.vitality,
        "xiyong":      f.favorable,
        "vitality":    f.vitality,
        "favorable":   f.favorable,
        "yinyang":     f.day_pillar.yinyang,
        "nayin": {
            "year":  f.year_pillar.na_yin,
            "month": f.month_pillar.na_yin,
            "day":   f.day_pillar.na_yin,
            "hour":  f.hour_pillar.na_yin,
        },
        "kongwang":  f.void,
        "shensha":   f.afflictions,
        "taiyuan":   f.taiyuan,
        "taixi":     f.taixi,
        "minggong":  f.minggong,
        "shengong":  f.shengong,
        "qiyun":     f.qiyun,
        "dayun":     f.dayun,
        "rizhu":     f.day_pillar.stem + f.day_pillar.branch,
        "me":        f.day_stem,
        "detail": {
            p_key: {
                "gan":      getattr(f, f'{p_key}_pillar').stem,
                "zhi":      getattr(f, f'{p_key}_pillar').branch,
                "wuxing":   getattr(f, f'{p_key}_pillar').stem_el,
                "yinyang":  getattr(f, f'{p_key}_pillar').yinyang,
                "shishen":  getattr(f, f'{p_key}_pillar').ten_god,
                "nayin":    getattr(f, f'{p_key}_pillar').na_yin,
                "canggan":  getattr(f, f'{p_key}_pillar').hidden,
                "xunkong":  getattr(f, f'{p_key}_pillar').vacant,
            }
            for p_key in ('year', 'month', 'day', 'hour')
        },
    }


def dict_to_fate(bazi_dict: dict, birth: dict, gender) -> Fate:
    """Reconstruct Fate from stored dict (for view/joint commands)."""
    det = bazi_dict.get('detail', {})

    def _rebuild(p_key: str) -> Pillar:
        d = det.get(p_key, {})
        return Pillar(
            stem      = d.get('gan', ''),
            branch    = d.get('zhi', ''),
            stem_el   = d.get('wuxing', ''),
            branch_el = '',
            yinyang   = d.get('yinyang', ''),
            ten_god   = d.get('shishen', ''),
            na_yin    = d.get('nayin', ''),
            hidden    = d.get('canggan', []),
            vacant    = d.get('xunkong', ''),
        )

    gender_str = '男' if gender in (1, '1', '男') else '女'
    bz = bazi_dict.get('bazi', {})
    bazi_str = ' '.join(bz.values()) if isinstance(bz, dict) else str(bz)

    return Fate(
        name          = bazi_dict.get('name', ''),
        gender        = gender_str,
        birth         = birth,
        year_pillar   = _rebuild('year'),
        month_pillar  = _rebuild('month'),
        day_pillar    = _rebuild('day'),
        hour_pillar   = _rebuild('hour'),
        bazi_str      = bazi_str,
        lunar_str     = bazi_dict.get('lunar_str', ''),
        shengxiao     = bazi_dict.get('shengxiao', ''),
        wuxing_count  = bazi_dict.get('wuxing_count', {}),
        vitality      = bazi_dict.get('wangshuai', ''),
        favorable     = bazi_dict.get('xiyong', ''),
        xiyong        = bazi_dict.get('xiyong', ''),
        mingge        = bazi_dict.get('mingge', ''),
        day_stem      = bazi_dict.get('me', ''),
        afflictions   = bazi_dict.get('shensha', []),
        void          = bazi_dict.get('kongwang', ''),
        vacant        = bazi_dict.get('kongwang', ''),
        taiyuan       = bazi_dict.get('taiyuan', ''),
        taixi         = bazi_dict.get('taixi', ''),
        minggong      = bazi_dict.get('minggong', ''),
        shengong      = bazi_dict.get('shengong', ''),
        qiyun         = bazi_dict.get('qiyun', {}),
        dayun         = bazi_dict.get('dayun', []),
        _lunar        = None,
    )


def calculate_fate(name: str, year, month, day, hour, minute, gender) -> dict:
    """
    Public entry point. Returns dict for JSON serialization.
    For in-memory Fate object, use dict_to_fate() to reconstruct.
    """
    fate_obj = _compute_fate(name, year, month, day, hour, minute, gender)
    return _fate_to_dict(fate_obj)
