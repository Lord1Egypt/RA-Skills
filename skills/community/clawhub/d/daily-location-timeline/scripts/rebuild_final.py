# -*- coding: utf-8 -*-
"""
rebuild_final.py — 每日所在城市·最终整合版 重建脚本（时间感知判定引擎）

把「消费层逐日梳理」+「出行腿(travel_legs.json)」+「实地证据」整合成
「每日所在城市_最终整合版.xlsx」（6 表）与「每日所在城市_逐日明细.csv」。

核心判定思想（时间感知）：
1) 每日有效时段 = 07:00–24:00（排除睡眠段）；按当日出行腿时刻把一天切成片段，
   停留最久的城市胜出为主城市；在途时间不计入任何城市。
2) 全天在途（跨夜长途，无有效停留）→ 归到达城市。
3) transit_leg 跟踪：只接受「当前在途腿」的到达事件，过滤被后续出发覆盖的陈旧到达
   （防止前一天的到达污染后一天，例：青藏铁路 7/24 出发 → 7/25 到拉萨，
   期间另一条腿的估算到达时刻不能把 7/25 判成西宁）。
4) 行程连续填充(chain-gap) 双安全闸：链不断(A.to==B.from) 且 1<=gap<=MAX_GAP；
   超长空档（缺腿的数年间隔）回落消费层，不强行顺延。
5) carry-in 按当日首个事件本地判定：首个事件是出发 → 早晨在出发地；是到达 → 在途。

【用户配置】换人使用只需改下方「个人常量配置块」，引擎逻辑不动。
"""
import json, os
from collections import defaultdict, Counter
from datetime import date, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# ============================================================
# 【个人常量配置块】—— 换人使用只改这一块，其余引擎逻辑不动
# ============================================================
WS = os.path.dirname(os.path.abspath(__file__)) + '/'
CONS_FILE  = WS + '每日所在城市_梳理.xlsx'          # 消费层逐日梳理表(含"每日城市"工作表)
MERGE_FILE = WS + '微信支付宝合并消费地梳理.xlsx'    # 合并明细(含"合并明细(含消费地)"工作表)
LEGS_FILE  = WS + 'travel_legs.json'
OUT_FINAL  = WS + '每日所在城市_最终整合版.xlsx'
OUT_LITE   = WS + '每日所在城市_梳理.xlsx'

MAX_GAP = 14  # 行程连续填充的最大空档天数（覆盖 2 周长途旅行/大环线；安全闸防止误覆盖真实异地消费）

# 老家/常驻城市集合（按"region/city"两级短格式，国内如 '浙江/杭州'，海外如 'Japan/Tokyo'）
HOME_CITIES = {'省/城市A', '省/城市B'}

# 中转城市约束：老家附近的交通枢纽（真实停留从不超 2 天，>2 天的连续段只保留有证据当天）。
# 例：{'省/枢纽A', '省/枢纽B'}；无此需求则留空 set()。
TRANSIT_CITIES = set()
HOME_CITY = None   # 中转超额日归属的老家城市；与 TRANSIT_CITIES 配套使用

# 特殊滞留时期（疫情封城等）：区间内整段强制归 HOME_CITY。无则保持 (None, None)。
LOCKDOWN_START = None   # 例：date(2020, 1, 24)
LOCKDOWN_END   = None   # 例：date(2020, 4, 8)

# 商户注册地城市黑名单：从未真实到访、却频繁出现在账单里的城市（订票平台注册地等）。
# 例：{'天津'}。命中后剔除并用邻日推算补回。
MERCHANT_CITY_BLACKLIST = set()

# 用户逐日核实校正：{'YYYY-MM-DD': '省/正确城市'}；初次运行为空 {}
CORRECTIONS = {}
# 校正外补充的"当日全部城市"：{'YYYY-MM-DD': ['省/城市', ...]}
EXTRA_CITIES = {}
# 城市关键词提示规则(跨境口岸/货币计价等场景,见 §1.5 说明)：默认空=禁用
CITY_HINT_RULES = []
# 地名别称→城市映射：账单/订单里出现的非标准地名归并到统一城市。
# 例：{'横琴': '广东/珠海', 'Kowloon': 'Hong Kong/香港'}；默认空 {}
CITY_ALIAS = {}
# ============================================================

def norm_full(prov, city):
    """把「浙江省/杭州市」「广西/南宁市」「新疆维吾尔/乌鲁木齐」统一成「浙江/杭州」「广西/南宁」「新疆/乌鲁木齐」，
    保持与出行/消费层一致的"省/市"短格式（消除同一城市因省写法不同被拆成两行）。"""
    if not city:
        return None
    p = str(prov or '').strip(); c = str(city).strip()
    # 全称（带"自治区/省/市"后缀）
    for long, short in [('维吾尔自治区', '新疆'), ('壮族自治区', '广西'),
                        ('回族自治区', '宁夏'), ('自治区', '')]:
        if long in p:
            p = short if short else p.replace(long, '')
            break
    # 半截写法（存库里偶尔出现的截断形式）
    half = {'新疆维吾尔': '新疆', '广西壮族': '广西', '西藏自治区': '西藏', '宁夏回族': '宁夏'}
    if p in half:
        p = half[p]
    if p.endswith('省') or p.endswith('市'):   # 浙江省->浙江；北京市->北京
        p = p[:-1]
    if c.endswith('市'):
        c = c[:-1]
    return f"{p}/{c}" if p else c

def norm_cs(s):
    """把"省/市"完整串（可能带后缀）归一为短格式；无斜杠时按市处理。"""
    if not s:
        return s
    p, _, c = str(s).partition('/')
    return norm_full(p, c) if c else norm_full('', p)

WS = os.path.dirname(os.path.abspath(__file__)) + '/'
CONS_FILE = WS + '每日所在城市_梳理.xlsx'   # 旧定义行已并入顶部配置块(保留此行以兼容早期路径写法)
MERGE_FILE = WS + '微信支付宝合并消费地梳理.xlsx'
LEGS_FILE = WS + 'travel_legs.json'
OUT_FINAL = WS + '每日所在城市_最终整合版.xlsx'
OUT_LITE = WS + '每日所在城市_梳理.xlsx'

# ---------- 1. 消费层基线（来自梳理版，剔除商户注册地黑名单城市） ----------
cons = {}  # date -> {'city':..,'all':set,'n':int,'basis':..}
wb = openpyxl.load_workbook(CONS_FILE, read_only=True)
ws = wb['每日城市']
for r in ws.iter_rows(min_row=2, values_only=True):
    d = str(r[0]); city = r[1]; allc = r[2]; n = r[3]; basis = r[4]
    if city and any(b and b in str(city) for b in MERCHANT_CITY_BLACKLIST):
        city = None
    ac = set()
    if allc:
        for p in str(allc).split('、'):
            if p and not any(b and b in p for b in MERCHANT_CITY_BLACKLIST):
                ac.add(norm_cs(p))
    cons[d] = {'city': norm_cs(city) if city else None, 'all': ac, 'n': (n or 0), 'basis': basis}
wb.close()

dates = sorted(cons.keys())

# 邻日推算：把被黑名单城市剔除后变成“无”的日子，用最近的有消费地日子补回
located = [(d, cons[d]['city']) for d in dates if cons[d]['city']]
loc_dates = [date.fromisoformat(d) for d, _ in located]
loc_cities = [c for _, c in located]
tianjin_dropped = [d for d in dates if cons[d]['city'] is None]
for d in tianjin_dropped:
    dt = date.fromisoformat(d)
    best = None; bestd = 10 ** 9
    for ld, lc in zip(loc_dates, loc_cities):
        dd = abs((ld - dt).days)
        if dd < bestd:
            bestd = dd; best = lc
    cons[d]['city'] = best
    cons[d]['basis'] = '推算'
    cons[d]['all'] = {best}

# ---------- 1.5 城市关键词提示规则（CITY_HINT_RULES 配置，默认空=禁用） ----------
# 用途：某些城市无法从「商品」字段直接提取（如跨境口岸城市、货币计价异地），需要按
# 「关键词 → 目标城市」规则从线下消费记录中识别为 L1 硬证据。
# 规则结构（在顶部配置块按需添加）：
#   CITY_HINT_RULES = [
#     {
#       'city': 'X省/X市',            # 命中后记入的目标城市(归一化短格式)
#       'any_keywords': ['A', 'B'],   # 命中任一关键词即满足(可空)
#       'require_venue': True,        # True=还需同时含场所词(酒店/餐厅等实体到访特征)
#       'exclude': ['有限公司'],       # 含排除词则不算(防公司注册地误判)
#       'currency_codes': ['MOP'],    # 账单含此货币代码也算命中(如跨境城市,可空)
#       'neighbor_fill': 1,           # 口岸联动:相邻N天内出现相邻城市提示时补为途经地(可空)
#     },
#   ]
# 典型场景：内地用户去港澳(口岸词"拱北/横琴"+澳元MOP计价)、跨国陆路口岸、
#           免税区购物(货币代码与所在国不同)等。
EXCLUDE_WORDS = ['股份有限公司', '有限公司', '科技有限公司', '集团', '商城', '旗舰店', '网店']
VENUE_WORDS = ['酒店', '宾馆', '民宿', '客栈', '餐厅', '美食', '火锅', '餐', '饭店', '小吃', '海鲜', '大排档']

hint_days = defaultdict(set)   # date -> {city, ...}
if CITY_HINT_RULES:
    wbH = openpyxl.load_workbook(MERGE_FILE, read_only=True)
    wsH = wbH['合并明细(含消费地)']
    hh = [c.value for c in wsH[1]]
    ih = {h: i for i, h in enumerate(hh)}
    for r in wsH.iter_rows(min_row=2, values_only=True):
        cat = r[ih.get('消费性质')]
        if cat not in ('线下消费', '线下-连锁'):
            continue
        blob = f"{r[ih.get('交易对方')] or ''} {r[ih.get('商品')] or ''}"
        dd = str(r[ih.get('交易时间')])[:10]
        for rule in CITY_HINT_RULES:
            hit = any(k and k in blob for k in rule.get('any_keywords', []))
            if not hit and any(k and k in blob for k in rule.get('currency_codes', [])):
                hit = True
            if not hit:
                continue
            if any(e in blob for e in rule.get('exclude', EXCLUDE_WORDS)):
                continue
            if rule.get('require_venue') and not any(v in blob for v in VENUE_WORDS):
                continue
            hint_days[dd].add(rule['city'])
    wbH.close()

for d, cities in hint_days.items():
    if d not in cons:
        continue
    cons[d]['all'] |= cities
    if cons[d]['city'] is None or cons[d]['city'] in tuple(HOME_CITIES):
        pick = sorted(cities)[0]
        cons[d]['city'] = pick
        cons[d]['all'].add(pick)
        cons[d]['basis'] = '当日记录'
# 口岸联动：某城市命中日的前后 neighbor_fill 天内若出现规则链上的关联城市提示，补为途经地
for rule in CITY_HINT_RULES:
    nf = rule.get('neighbor_fill')
    if not nf:
        continue
    for d in list(hint_days.keys()):
        if rule['city'] in hint_days[d]:
            for off in range(-nf, nf + 1):
                nb = (date.fromisoformat(d) + timedelta(days=off)).isoformat()
                if nb in hint_days and nb in cons:
                    for c2 in hint_days[nb]:
                        if c2 != rule['city']:
                            cons[nb]['all'].add(c2)

# ---------- 1.6 酒店/门票/美团团购订餐 实地消费硬证据（与飞机火车同级） ----------
# 用户规则：订酒店=必去住、订门票=必去玩、美团团购订餐=必去吃 → 商户名/商品里的明确所在地
# 即当日所在，覆盖老家锚点。关键教训（天津误判）：城市只从「商品」字段提取，交易对方是公司/
# OTA注册地（如「汉庭星空(上海)」「酷飞在线信息科技南京」）会误带注册城市，必须排除。
# 美团餐饮另需排除菜系误判（如「淄博烧烤」是风味不是城市，真实门店在「(盐田店)」=深圳）。
import re as _re
ONSITE = defaultdict(set)            # date -> set of "省/市"
wbO = openpyxl.load_workbook(MERGE_FILE, read_only=True)
wsO = wbO['合并明细(含消费地)']
hzO = [c.value for c in wsO[1]]; izO = {h: i for i, h in enumerate(hzO)}
_raw = set()
for r in wsO.iter_rows(min_row=2, values_only=True):
    c = r[izO['市']]
    if c and str(c).strip(): _raw.add(str(c).strip())
def norm_prov(p):
    """省份归一：广西/广西壮族自治区/广西壮族 → 广西；新疆/新疆维吾尔自治区/新疆维吾尔 → 新疆 等。"""
    p = str(p).strip()
    # 全称（带"自治区/省/市"后缀）
    for long, short in [('维吾尔自治区', '新疆'), ('壮族自治区', '广西'),
                        ('回族自治区', '宁夏'), ('自治区', ''), ('省', ''), ('市', '')]:
        if long in p:
            return short if short else p.replace(long, '')
    # 半截写法（存库里偶尔出现的截断形式）
    half = {'新疆维吾尔': '新疆', '广西壮族': '广西', '西藏自治区': '西藏',
            '宁夏回族': '宁夏', '内蒙古': '内蒙古'}
    if p in half:
        return half[p]
    return p

def norm_cs(city):
    """把「省/市」字符串的省份部分归一为简称（城市部分不动），消除同一城市因省写法不同被拆成两行。"""
    if not city or '/' not in city:
        return city
    prov, ct = city.split('/', 1)
    return f"{norm_prov(prov)}/{ct}"
CITY_FORMS = set(); CITY_FULL = {}
for c in _raw:
    CITY_FORMS.add(c)
    if c.endswith('市'): CITY_FORMS.add(c[:-1])
for r in wsO.iter_rows(min_row=2, values_only=True):
    prov = r[izO['省']]; c = r[izO['市']]
    if prov and c and str(c).strip():
        base = str(c).strip()[:-1] if str(c).strip().endswith('市') else str(c).strip()
        p = str(prov).strip()
        pbase = norm_prov(p)
        CITY_FULL.setdefault(base, f"{pbase}/{base}")   # 去掉省市后缀，与消费层"省/市"格式一致
EXTRA_FULL = dict(CITY_ALIAS)   # 地名别称→城市映射(配置块 CITY_ALIAS,默认空)

CUISINE = ['烧烤','火锅','菜','小吃','料理','粉','面','大排档','烤鱼','串','自助','小龙虾','麻辣','风味','江湖菜','湘菜','川菜','粤菜','杭帮','本帮','日料','西餐','快餐','便当','茶饮','咖啡','甜品','烘焙']

def _onsite_cat(blob):
    if _re.search(r'(酒店|民宿|客栈|宾馆|青旅|旅舍|度假村|公寓酒店|如家|汉庭|全季|锦江|亚朵|希尔顿|万豪|洲际|凯悦|香格里拉|丽笙|温德姆|布丁|城市便捷|维也纳|格林豪泰|首旅|华住|东呈|酷飞|和美|信用住|酒店订单|酒店预订|住宿)', blob):
        if not _re.search(r'(枕|被|床品|毛巾|浴巾|洗漱|拖鞋|一次性|用品|四件套|被子|被套|浴袍|床单)', blob):
            return '酒店'
    if _re.search(r'(门票|入园|景区|景点|乐园|主题公园|滑雪场|海洋馆|动物园|博物馆门票|缆车|游船票|演出票|演唱会|话剧|展览|观光|游船|景区门票|入园门票)', blob):
        if not _re.search(r'(电影|电热毯|长城牌|枕头|电影票)', blob):
            return '门票'
    if '美团' in blob and _re.search(r'(团购|套餐|代金券|美食|餐厅|火锅|烧烤|自助|烤肉|日料|西餐|中餐|小吃|奶茶|咖啡|烘焙|到店|核销|券|饭店|酒楼|餐馆|大排档|餐饮)', blob):
        if not _re.search(r'(外卖|跑腿|电影|买菜|闪购)', blob):
            return '美团'
    return None

def _extract_city(goods, cat):
    g = str(goods or '')
    for loc, full in EXTRA_FULL.items():
        if loc in g:
            return full
    for cf in CITY_FORMS:
        if cf and len(cf) >= 2 and cf in g:
            base = cf[:-1] if cf.endswith('市') else cf
            if cat == '美团' and _re.search(_re.escape(base) + r'(烧烤|火锅|菜|小吃|料理|粉|面|大排档|烤鱼|串|自助|小龙虾|麻辣|风味|江湖菜|湘菜|川菜|粤菜|杭帮|本帮|日料|西餐|快餐|便当|茶饮|咖啡|甜品|烘焙)', g):
                continue   # 菜系风味，不是地点
            return CITY_FULL.get(base, f'?/{base}')
    return None

for r in wsO.iter_rows(min_row=2, values_only=True):
    party = str(r[izO['交易对方']] or ''); goods = str(r[izO['商品']] or '')
    cat = _onsite_cat(f"{party} {goods}")
    if not cat:
        continue
    full = _extract_city(goods, cat)   # 只从商品字段提取城市
    if full:
        ONSITE[str(r[izO['交易时间']])[:10]].add(full)
wbO.close()
for d, cities in ONSITE.items():
    if d in cons:
        cons[d]['all'] |= {norm_cs(c) for c in cities}

# ---------- 2. L0 硬地标（用作安全闸） ----------
l0 = defaultdict(set)
wb2 = openpyxl.load_workbook(MERGE_FILE, read_only=True)
ws2 = wb2['合并明细(含消费地)']
hdr = [c.value for c in ws2[1]]
idx = {h: i for i, h in enumerate(hdr)}
for r in ws2.iter_rows(min_row=2, values_only=True):
    if r[idx['判定层级']] == 'L0':
        t = str(r[idx['交易时间']])[:10]
        c = str(r[idx['市']] or '')
        if c and not any(b and b in c for b in MERCHANT_CITY_BLACKLIST):
            l0[t].add(norm_full(r[idx['省']] or '', c))
wb2.close()

# ---------- 3. 出行层：day_travel(供 all-cities/real_cities) + 时间感知物理轨迹 ----------
legs = json.load(open(LEGS_FILE, encoding='utf-8'))
all_legs = legs['flights'] + legs['trains']
day_travel = defaultdict(list)  # date -> [(city, kind, raw)]

def add(d, city, kind, raw):
    day_travel[d.isoformat()].append((city, kind, raw))

for L in all_legs:
    typ = '飞机' if L['type'] == 'flight' else '火车'
    dd = date.fromisoformat(L['dep_date'])
    da = date.fromisoformat(L['arr_date'])
    add(dd, L['from'], f'{typ}_dep', L['raw'])
    add(da, L['to'], f'{typ}_arr', L['raw'])
    for st in L.get('stops', []):
        add(da, st, '经停', f"经停:{st}({L.get('no','')})")
    cur = dd + timedelta(days=1)
    while cur < da:  # 跨夜腿中间天(供 all-cities/real_cities)
        add(cur, L['to'], f'{typ}_arr', L['raw'])
        cur += timedelta(days=1)

# 酒店/门票/美团 实地消费硬证据并入（与出行腿同权重，供 all-cities/real_cities）
for d, cities in ONSITE.items():
    for c in cities:
        day_travel[d].append((c, 'onsite', f"实地消费:{c}"))

# ---- 时间感知物理轨迹：每日"有效时段 07:00~24:00(排除睡眠)"内停留最久的城市为主城市 ----
# 规则(用户要求)：
#   1) 每日有效时段 = 07:00~24:00(排除 00:00~07:00 睡眠)；该时段停留最久的城市即当日主城市。
#   2) 离开常住城市必有"去+回"两条腿(直来直去 或 绕大圈回)；腿间空档按"当前所在城市"顺延(行程连续)。
#   3) 在途(飞行/行车)时间不计入任何城市；跨夜长途当天若全天在途，归到达城市(与既有SOP一致)。
#   4) 腿时刻缺失时：到达缺失→同城按 出发+3h(火车)/+2h(飞机) 估、跨城按 12:00 估；出发缺失→10:00 估。
#   5) 国际线跨时区导致"同城到达≤出发"时，按出发+估算时长修正，避免到达跑到出发前。
import datetime as _dt
EFF_LO, EFF_HI = 7 * 60, 24 * 60  # 有效时段(分钟)

def _est_dep_min(L):
    return L['dep_min'] if L.get('dep_min') is not None else 10 * 60

def _est_arr_min(L):
    am = L.get('arr_min')
    if am is not None:
        return am
    dd = date.fromisoformat(L['dep_date']); da = date.fromisoformat(L['arr_date'])
    dm = _est_dep_min(L)
    if da == dd:
        return min(dm + (120 if L['type'] == 'flight' else 180), 1439)
    return 12 * 60  # 跨夜到达日按正午估

# 全局事件序列：(date, minute, 'dep'/'arr', city, to_city, leg)
_evs = []
for L in all_legs:
    dd = date.fromisoformat(L['dep_date']); da = date.fromisoformat(L['arr_date'])
    dm = _est_dep_min(L); am = _est_arr_min(L)
    if da == dd and am <= dm:  # 时区artifact：到达跑到出发前，按出发+估算时长修正
        am = min(dm + (120 if L['type'] == 'flight' else 180), 1439)
    _evs.append((dd, dm, 'dep', L['from'], L['to'], L))
    _evs.append((da, am, 'arr', L['to'], L['to'], L))
_evs.sort(key=lambda e: (e[0], e[1], 0 if e[2] == 'arr' else 1))  # 同时刻先到后走
_evs_by_day = defaultdict(list)
for e in _evs:
    _evs_by_day[e[0]].append(e)

phys = {}; phys_src = {}      # date_str -> 主城市 / '飞机'/'火车'/'行程连续'
# 跨夜中间天(单条腿内,无事件)：归到达城市
xo_days = {}
for L in all_legs:
    dd = date.fromisoformat(L['dep_date']); da = date.fromisoformat(L['arr_date'])
    c = dd + timedelta(days=1)
    while c < da:
        xo_days[c.isoformat()] = L['to']
        c += timedelta(days=1)
# 相邻腿间空档：A.to==B.from(链不断)→行程连续记 A.to；链断(缺回程腿)→不记(回落消费层)
leg_sorted = sorted(all_legs, key=lambda L: (L['dep_date'], _est_dep_min(L)))
chain_gap = {}; broken_gap = set()
for i in range(len(leg_sorted) - 1):
    A = leg_sorted[i]; B = leg_sorted[i + 1]
    da = date.fromisoformat(A['arr_date']); db = date.fromisoformat(B['dep_date'])
    gap = (db - da).days
    intact = (A['to'] == B['from']) and (1 <= gap <= MAX_GAP)  # 链不断且空档≤MAX_GAP才顺延；超长空档(如缺腿的数年间隔)回落消费层
    c = da + timedelta(days=1)
    while c < db:
        if intact:
            chain_gap[c.isoformat()] = A['to']
        else:
            broken_gap.add(c.isoformat())
        c += timedelta(days=1)

first_d = min(e[0] for e in _evs); last_d = max(e[0] for e in _evs)
transit_leg = None   # 当前在途腿(跨日持续，用于匹配到达事件、过滤被后续出发覆盖的陈旧到达)
d = first_d
while d <= last_d:
    ds = d.isoformat()
    evs_today = sorted(_evs_by_day.get(d, []), key=lambda e: (e[1], 0 if e[2] == 'arr' else 1))
    if evs_today:
        # 当日首个事件是出发→早晨在出发地；否则(首个是到达)→在途
        carry_in = evs_today[0][3] if evs_today[0][2] == 'dep' else None
        segs = []; prev = 0; pos = carry_in
        for (_, minute, typ, c1, c2, L) in evs_today:
            segs.append((prev, minute, pos))
            if typ == 'dep':
                if pos != c1:          # 缺腿导致不一致，以出发地为准
                    pos = c1
                pos = None             # 出发后进入在途
                transit_leg = L
            else:                      # arr：仅接受当前在途腿的到达，跳过陈旧到达(估算误差)
                if transit_leg is L:
                    pos = c1; transit_leg = None
            prev = minute
        segs.append((prev, 1440, pos))
        city_min = defaultdict(int)
        for (s, e, c) in segs:
            lo = max(s, EFF_LO); hi = min(e, EFF_HI)
            if hi > lo and c is not None:
                city_min[c] += (hi - lo)
        if city_min:
            phys[ds] = max(city_min, key=lambda k: city_min[k])
        else:
            # 全天在途(跨夜长途)→归到达城市
            dest = next((c2 for (_, _, typ, c1, c2, L) in evs_today if typ == 'dep'), None)
            if dest is None:
                arrs = [c for c, k, _ in day_travel.get(ds, []) if k.endswith('_arr')]
                dest = arrs[-1] if arrs else None
            phys[ds] = dest
        _ts = [L['type'] for *_, L in evs_today]
        phys_src[ds] = '火车' if _ts.count('train') >= _ts.count('flight') else '飞机'
    elif ds in xo_days:
        phys[ds] = xo_days[ds]; phys_src[ds] = '行程连续'
        day_travel[ds].append((phys[ds], '行程连续', f"行程连续:{phys[ds]}(跨夜)"))
    elif ds in chain_gap:
        phys[ds] = chain_gap[ds]; phys_src[ds] = '行程连续'
        day_travel[ds].append((phys[ds], '行程连续', f"行程连续:{phys[ds]}"))
    # else: broken_gap(缺回程腿) 或 段外 → phys=None(回落消费层)
    d += timedelta(days=1)

# ---------- 4. 逐日判定(时间感知：物理轨迹优先；腿未覆盖处用实地→消费层) ----------
def resolve(d):
    ct = cons.get(d)
    cons_city = ct['city'] if ct else None
    cons_all = ct['all'] if ct else set()
    cons_basis = ct['basis'] if ct else ''
    tv = day_travel.get(d, [])
    allc = set(cons_all) | set(c for c, k, _ in tv)
    cc = norm_cs(cons_city)
    primary = phys.get(d)               # 时间感知主城市(可能 None)
    if primary is not None:
        src = '出行(行程连续)' if phys_src.get(d) == '行程连续' else f'出行({phys_src.get(d, "行程连续")})'
        note = None
        if cc and cc != primary and cons_basis == '当日记录':
            note = f'⚠️消费记录({cons_city})冲突'
        elif l0.get(d) and primary not in l0[d]:
            note = f'⚠️与L0地标({"/".join(sorted(l0[d]))})冲突'
        return primary, src, '、'.join(sorted(allc)), note
    ons = [c for c, k, _ in tv if k == 'onsite']
    if ons:
        primary = ons[-1]; allc.add(primary)
        note = f'⚠️实地消费(酒店/门票/美团)纠正:原消费层标{cons_city}' if (cc and cc != primary) else None
        return primary, '实地(酒店/门票/美团)', '、'.join(sorted(allc)), note
    if cons_city:
        src = '当日记录' if cons_basis == '当日记录' else '推算'
        allc_s = '、'.join(sorted(allc)) if allc else cons_city
        return cons_city, src, allc_s, None
    return None, '无记录', '', None

daily = []
for d in dates:
    city, src, allc, note = resolve(d)
    daily.append({'date': d, 'city': city, 'src': src, 'all': allc, 'note': note})

filled_gaps = [ds for ds in phys if phys_src.get(ds) == '行程连续']  # 行程连续填充天数(供报告)

# ---------- 4.5 中转城市约束 + 特殊滞留时期强制归老家 ----------
# (1) 中转城市约束（TRANSIT_CITIES 配置，默认空=禁用）：老家附近的交通枢纽（枢纽之于老家），
#     真实停留从不超 2 天 → >2 天连续段仅保留有出行腿(arr/dep)或实地证据的日，其余归 HOME_CITY。
# (2) 特殊滞留时期（LOCKDOWN_START/END 配置，默认 None=禁用）：疫情封城等不可抗力滞留，
#     区间内整段强制归 HOME_CITY。
# 两项均为可选规则：配置留空/None 时整段逻辑自动跳过，不影响其他判定。

def _transit_evidence(d, city):
    """当日是否有出行腿(到达/出发)或实地(酒店/门票/美团)命中该中转城市。"""
    for c, k, _ in day_travel.get(d, []):
        if c == city and (k.endswith('_arr') or k.endswith('_dep') or k == 'onsite'):
            return True
    return False

transit_fixed = []
if TRANSIT_CITIES and HOME_CITY:
    _i = 0; _N = len(daily)
    while _i < _N:
        if daily[_i]['city'] in TRANSIT_CITIES:
            _j = _i
            while _j + 1 < _N and daily[_j + 1]['city'] == daily[_i]['city']:
                _j += 1
            _seg = daily[_i:_j + 1]
            _sd = date.fromisoformat(_seg[0]['date'])
            if LOCKDOWN_START and LOCKDOWN_END and LOCKDOWN_START <= _sd <= LOCKDOWN_END:
                _i = _j + 1; continue   # 封城期内由下方强制归老家处理，跳过
            if (_j - _i + 1) > 2:
                _keep = [k for k in range(len(_seg)) if _transit_evidence(_seg[k]['date'], _seg[k]['city'])]
                if len(_keep) > 2:      # 证据日也超 2 天则只保留首尾
                    _keep = [0, len(_seg) - 1]
                _keep = set(_keep)
                for k in range(len(_seg)):
                    if k not in _keep:
                        _d = _seg[k]
                        transit_fixed.append(_d['date'])
                        _d['city'] = HOME_CITY
                        _d['src'] = '推算(中转城市归老家)'
                        _d['all'] = HOME_CITY
                        _d['note'] = '⚠️中转城市仅出发/到达日计入,其余归老家'
            _i = _j + 1
        else:
            _i += 1

# 特殊滞留时期：区间内强制归老家
ld_fixed = []
if LOCKDOWN_START and LOCKDOWN_END and HOME_CITY:
    for _d in daily:
        _dt = date.fromisoformat(_d['date'])
        if LOCKDOWN_START <= _dt <= LOCKDOWN_END:
            _d['city'] = HOME_CITY
            _d['src'] = '推算(特殊时期滞留老家)'
            _d['all'] = HOME_CITY
            _d['note'] = '⚠️特殊滞留时期:强制归老家'
            ld_fixed.append(_d['date'])

# ---------- 4.6 用户核实校正（覆盖解析结果）+ 商户误定位清洗 ----------
# 根因：合并明细里「商家注册地 / 商品产地 / 连锁门店分支地 / 线上商户(杭州通·滴滴·拼多多)」
#       被当成了用户当日所在城市（与商户注册地误判同类）。用户逐日核实后：
#  (A) 部分日期主城市判错 → 用 CORRECTIONS 显式纠正到真实城市（配置块，默认空）；
#  (B) 主城市正确、但"当日全部城市"里混入了商户注册地/产地伪城市 → 仅保留「主城市 +
#       有真实出行腿/L0/实地证据」的城市，其余剔除。
real_cities = defaultdict(set)    # date -> 有真实出行腿(arr/dep/onsite/行程连续)佐证的城市
for _d, _lst in day_travel.items():
    for _c, _k, _ in _lst:
        real_cities[_d].add(_c)

corrected = []
for _d in daily:
    _dt = date.fromisoformat(_d['date'])
    if _d['date'] in CORRECTIONS and CORRECTIONS[_d['date']] != _d['city']:
        _old = _d['city']
        _d['city'] = CORRECTIONS[_d['date']]
        _d['src'] = '校正(用户核实)'
        _d['note'] = f'⚠️用户核实:原{_old}→{_d["city"]}'
        corrected.append(_d['date'])
    # 清洗"当日全部城市"：仅保留主城市 + 有真实出行腿/L0/实地证据的城市
    _all = set()
    if _d['all']:
        for _p in str(_d['all']).split('、'):
            if _p:
                _all.add(_p)
    _new = {_d['city']}
    for _c in _all:
        if _c == _d['city']:
            continue
        if _c in real_cities.get(_d['date'], set()) or _c in l0.get(_d['date'], set()):
            _new.add(_c)
    for _c in EXTRA_CITIES.get(_d['date'], []):
        _new.add(_c)
    _d['all'] = '、'.join(sorted(_new))

# ---------- 5. 停留段 ----------
def seg_basis(sources):
    for want, label in [('出行(火车)', '出行(火车)'), ('出行(飞机)', '出行(飞机)'),
                        ('出行(行程连续)', '出行(行程连续)'), ('实地(酒店/门票/美团)', '实地'),
                        ('当日记录', '当日'), ('推算', '推算')]:
        if want in sources:
            return label
    return '推算'

segs = []
i = 0
N = len(daily)
while i < N:
    j = i
    while j + 1 < N and daily[j + 1]['city'] == daily[i]['city']:
        j += 1
    seg = {
        'start': daily[i]['date'], 'end': daily[j]['date'],
        'city': daily[i]['city'],
        'days': j - i + 1,
        'basis': seg_basis([daily[k]['src'] for k in range(i, j + 1)]),
    }
    segs.append(seg)
    i = j + 1

# ---------- 6. 城市汇总 ----------
total = len(daily)
cc = Counter(d['city'] for d in daily if d['city'])
first_seen = {}; last_seen = {}
for d in daily:
    if not d['city']:
        continue
    first_seen.setdefault(d['city'], d['date'])
    last_seen[d['city']] = d['date']
city_rows = [(c, n, first_seen[c], last_seen[c], n / total * 100) for c, n in cc.most_common()]

# ---------- 7. 出行明细 ----------
def short(city):
    return city.split('/')[-1] if city else ''
def hhmm(minute):
    if minute is None:
        return ''
    return f'{minute // 60:02d}:{minute % 60:02d}'

flight_rows = []
for i, L in enumerate(sorted(legs['flights'], key=lambda x: (x['dep_date'], x.get('dep_min') or 0)), 1):
    flight_rows.append([i, L['dep_date'], hhmm(L['dep_min']), hhmm(L['arr_min']),
                        short(L['from']), short(L['to']), L.get('no', ''), L.get('status', '')])
train_rows = []
for i, L in enumerate(sorted(legs['trains'], key=lambda x: (x['dep_date'], x.get('dep_min') or 0)), 1):
    dt = f"{L['dep_date']} {hhmm(L['dep_min'])}"
    train_rows.append([i, dt, short(L['from']), short(L['to']),
                       L.get('no', ''), L.get('seat', ''), L.get('status', '')])

# ---------- 8. 写出（最终整合版，5表） ----------
HEAD = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='4472C4')

def style_header(ws, ncol):
    for c in range(1, ncol + 1):
        ws.cell(1, c).font = HEAD
        ws.cell(1, c).fill = FILL
        ws.cell(1, c).alignment = Alignment(horizontal='center')

wb = openpyxl.Workbook()
# 每日城市
ws = wb.active; ws.title = '每日城市'
ws.append(['日期', '主城市', '当日全部城市', '数据来源', '备注'])
for d in daily:
    ws.append([d['date'], d['city'], d['all'], d['src'], d['note']])
style_header(ws, 5)
ws.freeze_panes = 'A2'
for i, w in enumerate([12, 14, 28, 16, 26], 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
# 停留段
ws = wb.create_sheet('停留段')
ws.append(['起始日', '结束日', '主城市', '持续天数', '数据依据'])
for s in segs:
    ws.append([s['start'], s['end'], s['city'], s['days'], s['basis']])
style_header(ws, 5)
ws.freeze_panes = 'A2'
for i, w in enumerate([12, 12, 14, 10, 16], 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
# 城市汇总
ws = wb.create_sheet('城市汇总')
ws.append(['城市', '出现天数', '首次出现', '末次出现', '天数占比'])
for c, n, f, l, pct in city_rows:
    ws.append([c, n, f, l, f'{pct:.1f}%'])
style_header(ws, 5)
ws.freeze_panes = 'A2'
for i, w in enumerate([14, 10, 12, 12, 10], 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
# 飞机出行明细
ws = wb.create_sheet('飞机出行明细')
ws.append(['序号', '日期', '出发时间', '到达时间', '出发城市', '目的城市', '航班号', '状态'])
for r in flight_rows:
    ws.append(r)
style_header(ws, 8)
ws.freeze_panes = 'A2'
# 火车出行明细
ws = wb.create_sheet('火车出行明细')
ws.append(['序号', '日期时间', '出发城市', '目的城市', '车次', '席别', '状态'])
for r in train_rows:
    ws.append(r)
style_header(ws, 7)
ws.freeze_panes = 'A2'
wb.save(OUT_FINAL)

# ---------- 9. 写出（梳理版，消费层3表，剔除天津） ----------
wb = openpyxl.Workbook()
ws = wb.active; ws.title = '每日城市'
ws.append(['日期', '主城市', '当日全部城市', '交易笔数', '数据依据'])
for d in dates:
    ct = cons[d]
    cc = CORRECTIONS.get(d, ct['city'])   # 用户核实校正同步到消费层主城市
    if d in CORRECTIONS:
        allc = cc
    else:
        allc = '、'.join(sorted(ct['all'])) if ct['all'] else (ct['city'] or '')
    ws.append([d, cc, allc, ct['n'], ct['basis']])
style_header(ws, 5)
ws.freeze_panes = 'A2'
# 停留段（消费层）
segs2 = []
i = 0; N = len(dates)
while i < N:
    c0 = cons[dates[i]]['city']; j = i
    while j + 1 < N and cons[dates[j + 1]]['city'] == c0:
        j += 1
    segs2.append([dates[i], dates[j], c0, j - i + 1,
                  '当日' if any(cons[dates[k]]['basis'] == '当日记录' for k in range(i, j + 1)) else '推算'])
    i = j + 1
ws = wb.create_sheet('停留段')
ws.append(['起始日', '结束日', '主城市', '持续天数', '数据依据'])
for s in segs2:
    ws.append(s)
style_header(ws, 5)
# 城市汇总（消费层）
cc2 = Counter(cons[d]['city'] for d in dates if cons[d]['city'])
f2 = {}; l2 = {}
for d in dates:
    c = cons[d]['city']
    if c:
        f2.setdefault(c, d); l2[c] = d
ws = wb.create_sheet('城市汇总')
ws.append(['城市', '出现天数', '首次出现', '末次出现', '天数占比'])
for c, n in cc2.most_common():
    ws.append([c, n, f2[c], l2[c], f'{n / N * 100:.1f}%'])
style_header(ws, 5)
wb.save(OUT_LITE)

# ---------- 9.5 导出 逐日明细 CSV（便于按年/城市筛选查看，兼容 Excel/Numbers） ----------
import csv as _csv
CSV_OUT = WS + '每日所在城市_逐日明细.csv'
with open(CSV_OUT, 'w', newline='', encoding='utf-8-sig') as fh:
    w = _csv.writer(fh)
    w.writerow(['日期', '主城市', '当日全部城市', '数据来源', '备注'])
    for d in daily:
        w.writerow([d['date'], d['city'], d['all'], d['src'], d['note'] or ''])
print(f'已导出逐日明细CSV: {CSV_OUT}')

# ---------- 10. 报告 ----------
print(f'黑名单城市剔除日(邻日推算补回): {tianjin_dropped}')
print(f'行程连续填充天数: {len(filled_gaps)}')
print(f'  样例: {filled_gaps[:20]}')
print(f'中转城市超额日归老家: {len(transit_fixed)} 天')
print(f'  样例: {transit_fixed[:20]}')
print(f'特殊滞留时期归老家: {len(ld_fixed)} 天')
print(f'  样例: {ld_fixed[:10]}')
print(f'用户核实校正(商户误定位/主城市纠正)天数: {len(corrected)}')
print(f'  样例: {corrected[:30]}')
print(f'最终整合版 每日城市行数: {len(daily)}')
print(f'最终整合版 无记录天数: {sum(1 for d in daily if d["src"]=="无记录")}')
print(f'黑名单城市残留: {sum(1 for d in daily if d["city"] and any(b in d["city"] for b in MERCHANT_CITY_BLACKLIST))}')
print(f'城市TOP:')
for c, n, f, l, p in city_rows[:8]:
    print(f'  {c}: {n} ({p:.1f}%)')
print('\n完成。已写出:', OUT_FINAL, '和', OUT_LITE)
