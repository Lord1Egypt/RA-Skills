#!/usr/bin/env python3
"""
国学占卜公共函数库
提供天干地支查询、五行生克、农历日期转换等基础功能。
"""

# ============================================================
# 天干
# ============================================================

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
TIANGAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}
TIANGAN_YINYANG = {
    '甲': '阳', '丙': '阳', '戊': '阳', '庚': '阳', '壬': '阳',
    '乙': '阴', '丁': '阴', '己': '阴', '辛': '阴', '癸': '阴',
}

# 天干寄宫（大六壬核心：天干需映射到地支方可查天地盘）
# 甲→寅 乙→辰 丙→巳 丁→未 戊→巳 己→未 庚→申 辛→戌 壬→亥 癸→丑
TIANGAN_JIGONG = {
    '甲': '寅', '乙': '辰', '丙': '巳', '丁': '未',
    '戊': '巳', '己': '未', '庚': '申', '辛': '戌',
    '壬': '亥', '癸': '丑',
}

# ============================================================
# 地支
# ============================================================

DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}
# 五行统一映射：地支+八卦 → 五行
WUXING = {
    **DIZHI_WUXING,
    '乾': '金', '兑': '金', '离': '火', '震': '木',
    '巽': '木', '坎': '水', '艮': '土', '坤': '土',
}
DIZHI_YINYANG = {
    '子': '阳', '寅': '阳', '辰': '阳', '午': '阳', '申': '阳', '戌': '阳',
    '丑': '阴', '卯': '阴', '巳': '阴', '未': '阴', '酉': '阴', '亥': '阴',
}
DIZHI_SHENGXIAO = {
    '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
    '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
    '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪',
}
DIZHI_SHICHEN = {
    '子': '23:00-01:00', '丑': '01:00-03:00', '寅': '03:00-05:00',
    '卯': '05:00-07:00', '辰': '07:00-09:00', '巳': '09:00-11:00',
    '午': '11:00-13:00', '未': '13:00-15:00', '申': '15:00-17:00',
    '酉': '17:00-19:00', '戌': '19:00-21:00', '亥': '21:00-23:00',
}

# ============================================================
# 五行生克
# ============================================================

WUXING_SHENG = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
}

WUXING_KE = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
}


def get_wuxing_relation(a: str, b: str) -> str:
    """返回 a 对 b 的五行关系：生/克/被生/被克/同"""
    if a == b:
        return '同'
    if WUXING_SHENG.get(a) == b:
        return '生'
    if WUXING_KE.get(a) == b:
        return '克'
    if WUXING_SHENG.get(b) == a:
        return '被生'
    return '被克'


# ============================================================
# 地支关系
# ============================================================

LIUHE = [
    ('子', '丑'), ('寅', '亥'), ('卯', '戌'),
    ('辰', '酉'), ('巳', '申'), ('午', '未'),
]

LIUCHONG = [
    ('子', '午'), ('丑', '未'), ('寅', '申'),
    ('卯', '酉'), ('辰', '戌'), ('巳', '亥'),
]

SANHE = [
    ('申', '子', '辰'),  # 水局
    ('亥', '卯', '未'),  # 木局
    ('寅', '午', '戌'),  # 火局
    ('巳', '酉', '丑'),  # 金局
]


def get_liuhe(zhi: str) -> str:
    """返回某地支的六合地支"""
    for a, b in LIUHE:
        if a == zhi:
            return b
        if b == zhi:
            return a
    return None


def get_liuchong(zhi: str) -> str:
    """返回某地支的六冲地支"""
    for a, b in LIUCHONG:
        if a == zhi:
            return b
        if b == zhi:
            return a
    return None


# ============================================================
# 旬空计算
# ============================================================

XUNKONG_MAP = {
    '甲子': ('戌', '亥'), '甲戌': ('申', '酉'),
    '甲申': ('午', '未'), '甲午': ('辰', '巳'),
    '甲辰': ('寅', '卯'), '甲寅': ('子', '丑'),
}


def get_xunkong(ri_tiangan: str, ri_dizhi: str) -> tuple:
    """根据日干支计算空亡地支"""
    # 找旬首
    tg_idx = TIANGAN.index(ri_tiangan)
    dz_idx = DIZHI.index(ri_dizhi)
    xunshou_dz = DIZHI[(dz_idx - tg_idx) % 12]
    xunshou = '甲' + xunshou_dz
    return XUNKONG_MAP.get(xunshou, ('?', '?'))


# ============================================================
# 八卦
# ============================================================

BAGUA_XIANTIAN = {
    1: ('乾', '☰', '金'),
    2: ('兑', '☱', '金'),
    3: ('离', '☲', '火'),
    4: ('震', '☳', '木'),
    5: ('巽', '☴', '木'),
    6: ('坎', '☵', '水'),
    7: ('艮', '☶', '土'),
    8: ('坤', '☷', '土'),
}

# 八卦自然象
BAGUA_NATURE = {1: '天', 2: '泽', 3: '火', 4: '雷', 5: '风', 6: '水', 7: '山', 8: '地'}

# 八卦名称→符号映射（供 liuyao_yaogua 等模块使用）
GUA_SYMBOL_MAP = {info[0]: info[1] for info in BAGUA_XIANTIAN.values()}

# 八卦完整字典（供 meihua_qigua 等模块使用）
BAGUA_DICT = {}
for _num, (_name, _symbol, _wuxing) in BAGUA_XIANTIAN.items():
    BAGUA_DICT[_num] = {'name': _name, 'symbol': _symbol, 'wuxing': _wuxing, 'nature': BAGUA_NATURE[_num]}


def num_to_gua(num: int) -> dict:
    """数字(1-8) → 卦名、符号、五行"""
    n = num % 8
    if n == 0:
        n = 8
    info = BAGUA_XIANTIAN[n]
    return {'name': info[0], 'symbol': info[1], 'wuxing': info[2]}


# ============================================================
# 六十四卦简表
# ============================================================

LIUSHISI_GUA = {
    (1, 1): '乾为天', (1, 2): '天泽履', (1, 3): '天火同人', (1, 4): '天雷无妄',
    (1, 5): '天风姤', (1, 6): '天水讼', (1, 7): '天山遁', (1, 8): '天地否',
    (2, 1): '泽天夬', (2, 2): '兑为泽', (2, 3): '泽火革', (2, 4): '泽雷随',
    (2, 5): '泽风大过', (2, 6): '泽水困', (2, 7): '泽山咸', (2, 8): '泽地萃',
    (3, 1): '火天大有', (3, 2): '火泽睽', (3, 3): '离为火', (3, 4): '火雷噬嗑',
    (3, 5): '火风鼎', (3, 6): '火水未济', (3, 7): '火山旅', (3, 8): '火地晋',
    (4, 1): '雷天大壮', (4, 2): '雷泽归妹', (4, 3): '雷火丰', (4, 4): '震为雷',
    (4, 5): '雷风恒', (4, 6): '雷水解', (4, 7): '雷山小过', (4, 8): '雷地豫',
    (5, 1): '风天小畜', (5, 2): '风泽中孚', (5, 3): '风火家人', (5, 4): '风雷益',
    (5, 5): '巽为风', (5, 6): '风水涣', (5, 7): '风山渐', (5, 8): '风地观',
    (6, 1): '水天需', (6, 2): '水泽节', (6, 3): '水火既济', (6, 4): '水雷屯',
    (6, 5): '水风井', (6, 6): '坎为水', (6, 7): '水山蹇', (6, 8): '水地比',
    (7, 1): '山天大畜', (7, 2): '山泽损', (7, 3): '山火贲', (7, 4): '山雷颐',
    (7, 5): '山风蛊', (7, 6): '山水蒙', (7, 7): '艮为山', (7, 8): '山地剥',
    (8, 1): '地天泰', (8, 2): '地泽临', (8, 3): '地火明夷', (8, 4): '地雷复',
    (8, 5): '地风升', (8, 6): '地水师', (8, 7): '地山谦', (8, 8): '坤为地',
}


def get_64gua_name(up_num: int, down_num: int) -> str:
    """上下卦数 → 六十四卦名"""
    up = up_num % 8
    if up == 0:
        up = 8
    down = down_num % 8
    if down == 0:
        down = 8
    return LIUSHISI_GUA.get((up, down), '未知卦')


# 六十四卦名称→名称查找表（供 liuyao_yaogua 等模块使用）
# Key: (上卦名, 下卦名) → 卦名
LIUSHISI_GUA_BY_NAME = {}
for (_up_num, _down_num), _gua_name in LIUSHISI_GUA.items():
    _up_name = BAGUA_XIANTIAN[_up_num][0]
    _down_name = BAGUA_XIANTIAN[_down_num][0]
    LIUSHISI_GUA_BY_NAME[(_up_name, _down_name)] = _gua_name


# ============================================================
# 时辰转换
# ============================================================

def hour_to_shichen(hour: float) -> tuple:
    """24小时制（支持小数） → (地支名, 序数1-12)"""
    h = hour % 24
    if h >= 23.0 or h < 1.0:
        return ('子', 1)
    # 寅=3, 卯=4, ..., 丑=2; start 依次对应 DIZHI[1]..DIZHI[10]
    for i, start in enumerate([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]):
        if float(start) <= h < float(start + 2):
            return (DIZHI[i + 1], i + 2)
    return ('子', 1)


# ============================================================
# 季节旺衰
# ============================================================

SEASON_WANG = {
    '春': {'旺': '木', '相': '火', '休': '水', '囚': '金', '死': '土'},
    '夏': {'旺': '火', '相': '土', '休': '木', '囚': '水', '死': '金'},
    '秋': {'旺': '金', '相': '水', '休': '土', '囚': '火', '死': '木'},
    '冬': {'旺': '水', '相': '木', '休': '金', '囚': '土', '死': '火'},
    '季春': {'旺': '土', '相': '金', '休': '火', '囚': '木', '死': '水'},
    '季夏': {'旺': '土', '相': '金', '休': '火', '囚': '木', '死': '水'},
    '季秋': {'旺': '土', '相': '金', '休': '火', '囚': '木', '死': '水'},
    '季冬': {'旺': '土', '相': '金', '休': '火', '囚': '木', '死': '水'},
}


def get_season(month: int) -> dict:
    """农历月 → 季节信息（含四季月土旺标记）

    辰(3)、未(6)、戌(9)、丑(12) 为四季月，土旺。
    返回: {'season': str, 'season_name': str, 'is_ji_month': bool, 'wang_wuxing': str}
    """
    # 四季月（辰戌丑未对应农历3/6/9/12月）
    ji_months = {3: '季春', 6: '季夏', 9: '季秋', 12: '季冬'}
    if month in ji_months:
        return {
            'season': ji_months[month],
            'season_name': ji_months[month],
            'is_ji_month': True,
            'wang_wuxing': '土',
        }
    season_map = {1: '春', 2: '春', 4: '夏', 5: '夏',
                  7: '秋', 8: '秋', 10: '冬', 11: '冬'}
    s = season_map.get(month, '冬')
    wang = SEASON_WANG.get(s, {}).get('旺', '?')
    return {
        'season': s,
        'season_name': s,
        'is_ji_month': False,
        'wang_wuxing': wang,
    }


def get_wuxing_status(wuxing: str, season_info) -> str:
    """返回某五行在特定季节的旺衰状态

    season_info: get_season() 的返回值(dict) 或 纯季节字符串(str, 兼容旧调用)
    """
    if isinstance(season_info, dict):
        season = season_info['season']
    else:
        season = season_info
    season_data = SEASON_WANG.get(season, {})
    for status, wx in season_data.items():
        if wx == wuxing:
            return status
    return '囚'


# ============================================================
# 真太阳时校正：城市坐标 + 均时差 + 经度修正
# ============================================================

import math
import json
import os
from datetime import date, datetime, timedelta

# 中国主要城市经纬度（东经, 北纬）
_CITY_COORDS = {
    '成都': (104.06, 30.67), '绵阳': (104.73, 31.47), '德阳': (104.38, 31.13),
    '宜宾': (104.62, 28.77), '乐山': (103.77, 29.57), '南充': (106.11, 30.80),
    '泸州': (105.44, 28.87), '自贡': (104.78, 29.35), '内江': (105.06, 29.58),
    '广元': (105.83, 32.44), '遂宁': (105.57, 30.53), '眉山': (103.85, 30.08),
    '达州': (107.47, 31.21), '攀枝花': (101.72, 26.58),
    '重庆': (106.55, 29.57),
    '北京': (116.41, 39.90),
    '上海': (121.47, 31.23),
    '广州': (113.26, 23.13), '深圳': (114.07, 22.62),
    '东莞': (113.75, 23.05), '佛山': (113.12, 23.02),
    '珠海': (113.58, 22.27),
    '杭州': (120.15, 30.28), '宁波': (121.54, 29.87),
    '温州': (120.70, 28.00),
    '南京': (118.79, 32.06), '苏州': (120.59, 31.30),
    '无锡': (120.30, 31.57),
    '武汉': (114.30, 30.60),
    '西安': (108.94, 34.26),
    '天津': (117.20, 39.13),
    '长沙': (112.97, 28.23),
    '郑州': (113.65, 34.76),
    '济南': (117.00, 36.65), '青岛': (120.38, 36.07),
    '大连': (121.61, 38.91),
    '沈阳': (123.43, 41.80),
    '哈尔滨': (126.53, 45.80),
    '长春': (125.32, 43.90),
    '昆明': (102.83, 24.88),
    '贵阳': (106.71, 26.57),
    '南宁': (108.37, 22.82),
    '海口': (110.33, 20.03), '三亚': (109.51, 18.25),
    '福州': (119.30, 26.07), '厦门': (118.08, 24.48),
    '合肥': (117.23, 31.86),
    '南昌': (115.86, 28.68),
    '石家庄': (114.50, 38.04),
    '太原': (112.55, 37.87),
    '呼和浩特': (111.67, 40.82),
    '银川': (106.27, 38.47),
    '西宁': (101.78, 36.62),
    '兰州': (103.83, 36.06),
    '拉萨': (91.13, 29.65),
    '乌鲁木齐': (87.62, 43.83),
    '中国香港': (114.17, 22.28), '香港': (114.17, 22.28),
    '中国澳门': (113.55, 22.20), '澳门': (113.55, 22.20),
    '中国台北': (121.53, 25.05), '台北': (121.53, 25.05),
}


def get_city_coordinates(city_name: str, timeout: float = 3.0) -> dict:
    """
    城市名 → 经纬度（本地查表优先，网络查询降级）。

    查找顺序:
      1. 本地 _CITY_COORDS 精确/模糊匹配（0ms）
      2. 本地缓存 _geo_cache.json（0ms）
      3. Open-Meteo Geocoding API 网络查询（0.3~0.8s）
      4. 全部失败 → 返回 None

    返回 {'name': 城市名, 'longitude': 东经, 'latitude': 北纬, 'source': 来源} 或 None。
    source 字段: 'local' | 'cache' | 'geocode'
    """
    name = city_name.strip()

    # 1. 精确匹配
    if name in _CITY_COORDS:
        lon, lat = _CITY_COORDS[name]
        return {'name': name, 'longitude': lon, 'latitude': lat, 'source': 'local'}

    # 2. 模糊匹配
    for key, (lon, lat) in _CITY_COORDS.items():
        if name in key or key in name:
            return {'name': key, 'longitude': lon, 'latitude': lat, 'source': 'local'}

    # 3. 本地缓存
    cache = _load_geo_cache()
    cache_key = name.lower()
    if cache_key in cache:
        entry = cache[cache_key]
        return {'name': entry['name'], 'longitude': entry['longitude'],
                'latitude': entry['latitude'], 'source': 'cache'}

    # 4. 网络查询
    result = geocode_city(name, timeout=timeout)
    if result:
        # 写入缓存
        cache[cache_key] = result
        _save_geo_cache(cache)
        return {'name': result['name'], 'longitude': result['longitude'],
                'latitude': result['latitude'], 'source': 'geocode'}

    return None


# ============================================================
# 网络地理编码（Open-Meteo Geocoding API）
# ============================================================

_GEO_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_geo_cache.json')

# 常见中文城市名 → 英文名映射（Open-Meteo 不识别中文别名时使用）
_CN_TO_EN_CITY = {
    '纽约': 'New York City', '旧金山': 'San Francisco', '洛杉矶': 'Los Angeles',
    '伦敦': 'London', '巴黎': 'Paris', '柏林': 'Berlin', '莫斯科': 'Moscow',
    '东京': 'Tokyo', '首尔': 'Seoul', '新加坡': 'Singapore',
    '悉尼': 'Sydney', '墨尔本': 'Melbourne',
    '多伦多': 'Toronto', '温哥华': 'Vancouver', '蒙特利尔': 'Montreal',
    '芝加哥': 'Chicago', '华盛顿': 'Washington', '波士顿': 'Boston',
    '西雅图': 'Seattle', '休斯顿': 'Houston',
    '罗马': 'Rome', '马德里': 'Madrid', '阿姆斯特丹': 'Amsterdam',
    '法兰克福': 'Frankfurt', '慕尼黑': 'Munich',
    '曼谷': 'Bangkok', '吉隆坡': 'Kuala Lumpur', '雅加达': 'Jakarta',
    '迪拜': 'Dubai', '开罗': 'Cairo', '孟买': 'Mumbai', '德里': 'Delhi',
    '奥克兰': 'Auckland', '惠灵顿': 'Wellington',
    '圣保罗': 'Sao Paulo', '布宜诺斯艾利斯': 'Buenos Aires',
    '墨西哥城': 'Mexico City', '利马': 'Lima',
}

# 常见中文国家名 → ISO 3166-1 alpha2 代码（用于消除重名歧义）
_CN_TO_COUNTRY = {
    '日本': 'JP', '韩国': 'KR', '美国': 'US', '英国': 'GB',
    '法国': 'FR', '德国': 'DE', '意大利': 'IT', '西班牙': 'ES',
    '澳大利亚': 'AU', '加拿大': 'CA', '新西兰': 'NZ', '新加坡': 'SG',
    '泰国': 'TH', '马来西亚': 'MY', '印度': 'IN', '俄罗斯': 'RU',
    '巴西': 'BR', '阿根廷': 'AR', '墨西哥': 'MX', '埃及': 'EG',
    '阿联酋': 'AE', '印尼': 'ID', '荷兰': 'NL',
}


def _load_geo_cache() -> dict:
    """加载本地地理编码缓存"""
    try:
        if os.path.exists(_GEO_CACHE_PATH):
            with open(_GEO_CACHE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_geo_cache(cache: dict):
    """保存本地地理编码缓存"""
    try:
        with open(_GEO_CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 缓存写入失败不影响主流程


def geocode_city(city_name: str, timeout: float = 3.0) -> dict:
    """
    通过 Open-Meteo Geocoding API 查询城市经纬度。

    参数:
      city_name:  城市名（中文或英文）
      timeout:    网络超时（秒），默认 3s

    返回:
      {'name': 显示名, 'longitude': 东经, 'latitude': 北纬} 或 None

    注意:
      - 无需 API Key
      - 免费额度: 10,000 次/天
      - 中文城市名对国内城市有效，海外城市建议用英文名
      - 内置常见中文别名 → 英文名映射
    """
    import urllib.request
    import urllib.parse

    # 查找中文别名映射
    query = _CN_TO_EN_CITY.get(city_name, city_name)

    # 尝试从城市名中提取国家限定（如"日本东京"→ country=JP, query=Tokyo）
    country_code = None
    for cn_country, code in _CN_TO_COUNTRY.items():
        if cn_country in city_name:
            country_code = code
            # 去掉国家前缀再查英文映射
            remaining = city_name.replace(cn_country, '').strip()
            if remaining in _CN_TO_EN_CITY:
                query = _CN_TO_EN_CITY[remaining]
            elif remaining:
                query = remaining
            break

    # 构建请求 URL
    params = {
        'name': query,
        'count': 1,
        'language': 'zh',
        'format': 'json',
    }
    if country_code:
        params['countryCode'] = country_code

    url = 'https://geocoding-api.open-meteo.com/v1/search?' + urllib.parse.urlencode(params)

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'comprehensive-divination-skill/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        results = data.get('results', [])
        if not results:
            return None

        r = results[0]
        lon = r['longitude']
        lat = r['latitude']
        display_name = r.get('name', city_name)

        # 优先使用带国家/地区信息的显示名
        country = r.get('country', '')
        admin1 = r.get('admin1', '')
        if admin1 and country:
            display_name = f"{display_name}，{admin1}，{country}"
        elif country:
            display_name = f"{display_name}，{country}"

        return {'name': display_name, 'longitude': lon, 'latitude': lat}

    except Exception:
        return None


def _eot_minutes(d: date) -> float:
    """
    均时差 (Equation of Time)，Spencer (1971) 公式。
    返回分钟数，正值表示真太阳时比平太阳时快。
    """
    n = d.timetuple().tm_yday
    B = 2 * math.pi * (n - 1) / 365.0
    eot = 229.18 * (
        0.000075
        + 0.001868 * math.cos(B) - 0.032077 * math.sin(B)
        - 0.014615 * math.cos(2 * B) - 0.040849 * math.sin(2 * B)
    )
    return eot


def correct_to_true_solar(hour: int, minute: int, longitude: float, d: date = None) -> tuple:
    """
    北京时间 → 当地真太阳时。
    公式：真太阳时 = 北京时间 + (经度 − 120°) × 4分钟 + 均时差
    返回 (corrected_hour_float, corrected_minute_int)
    """
    if d is None:
        d = date.today()

    # 经度偏差（分钟）
    lon_offset = (longitude - 120.0) * 4.0
    # 平太阳时分钟数 + 均时差
    total_minutes = hour * 60 + minute + lon_offset + _eot_minutes(d)

    # 约束在 [0, 1440) 即 0:00-23:59
    total_minutes = total_minutes % (24 * 60)

    corrected_hour = total_minutes / 60.0
    corrected_minute = int(total_minutes % 60)

    return (corrected_hour, corrected_minute)


# ============================================================
# 函数化 pipeline（当前实现：支持海外用户，强制取北京时间为基准）
# ============================================================

def get_beijing_time(dt: datetime = None) -> datetime:
    """
    获取当前（或指定）时刻的 **北京时间**（UTC+8），与用户所在地无关。

    这是函数化 pipeline 的第一步：**始终以北京时间为时间基准**，
    解决海外用户"datetime.now() 拿到的是本地挂钟时间"的根本问题。

    实现：取 UTC 时刻 + 8 小时 = 北京时间。零网络依赖。

    参数:
      dt: 指定的 datetime 对象（必须为 naive，无时区信息），
          None = 当前时刻。SKILL 调用时应在入口立即执行并冻结。

    返回:
      naive datetime，表示北京时间的"挂钟时刻"（年/月/日/时/分/秒 都是北京时间数值）。

    注意:
      - 本机系统时间必须准（如果用户手动改过系统时间，结果会错）。
      - 如需更高精度（不受本机时钟影响），未来可加网络 API 取时间。
    """
    if dt is not None:
        # 调用方传入了"已冻结的时刻"，假设它就是北京时间
        return dt
    # 取 UTC + 8h = 北京时间
    utc_now = datetime.now(tz=None)  # naive, 兼容旧版
    # 为避免 Python 3.12+ 的 datetime.utcnow() 弃用警告，
    # 使用 datetime.now() + timedelta 替代
    from datetime import timezone as _tz
    utc_now = datetime.now(_tz.utc).replace(tzinfo=None)
    return utc_now + timedelta(hours=8)


def longitude_to_true_solar(bj_dt: datetime, longitude: float) -> dict:
    """
    给定北京时间 + 当地经度，算出当地真太阳时（time object 形式）。

    公式：TST = 北京时间 + (经度 − 120°) × 4min + 均时差

    参数:
      bj_dt:      北京时间（naive datetime，函数化 pipeline 第一步的输出）
      longitude:  当地经度。东经为正（如成都 104.06），
                  西经为负（如纽约 -74.006）。
                  传 None = 不做 TST 校正，返回北京时间本身。

    返回:
      dict {
        'tst_hour':     真太阳时的小时数（0-23，含小数，浮点）,
        'tst_minute':   真太阳时的分钟数（0-59，整数）,
        'tst_datetime': 真太阳时对应的 datetime（naive，日期可能跨日）,
        'tst_offset_min': 相对北京时间的偏移分钟数（正=东，负=西）,
        'longitude':    入参经度（None 时不存）,
        'tst_corrected': 是否做了 TST 校正（longitude 非 None 时为 True）,
      }

    说明：
      - 经度=120.0（默认）时几乎无校正（仅 ±均时差）
      - 经度为负（西经）时 TST < 北京时间
      - 经度跨度大时（如纽约 6/15 凌晨），tst_datetime 可能落在前一天
    """
    if longitude is None:
        return {
            'tst_hour': float(bj_dt.hour),
            'tst_minute': bj_dt.minute,
            'tst_datetime': bj_dt,
            'tst_offset_min': 0.0,
            'tst_corrected': False,
        }

    d = bj_dt.date()
    # 统一计算路径：先算总分钟偏移，再同时得出 day_offset、tst_hour、tst_minute
    lon_offset_min = (longitude - 120.0) * 4.0
    eot_min = _eot_minutes(d)
    total_minutes = bj_dt.hour * 60 + bj_dt.minute + lon_offset_min + eot_min

    # 计算跨日偏移（用整数除法，保留符号）
    day_offset = int(total_minutes) // (24 * 60)
    # 约束到 [0, 1440) 得当日分钟数
    day_minutes = total_minutes % (24 * 60)
    tst_hour = day_minutes / 60.0
    tst_min = int(day_minutes % 60)

    tst_dt = bj_dt + timedelta(days=day_offset)
    tst_dt = tst_dt.replace(hour=int(tst_hour), minute=tst_min, second=0, microsecond=0)

    return {
        'tst_hour': tst_hour,
        'tst_minute': tst_min,
        'tst_datetime': tst_dt,
        'tst_offset_min': round((tst_hour - bj_dt.hour - bj_dt.minute / 60.0) * 60, 1),
        'longitude': longitude,
        'tst_corrected': True,
    }


def datetime_to_shichen(dt: datetime) -> tuple:
    """
    datetime → 十二时辰（地支名 + 1-12 整数索引）。

    传统时辰划分（按真太阳时）:
      子 23-01, 丑 01-03, 寅 03-05, 卯 05-07, 辰 07-09, 巳 09-11,
      午 11-13, 未 13-15, 申 15-17, 酉 17-19, 戌 19-21, 亥 21-23

    返回: (地支名字符串, 1-12 整数索引)
    """
    return hour_to_shichen(dt.hour)


def get_full_pipeline(dt: datetime = None, longitude: float = None) -> dict:
    """
    函数化 pipeline 的**一站式封装**：从"取北京时间"到"起卦前所有信息"。

    流程:
      [1] get_beijing_time(dt)              → 北京时间
      [2] longitude_to_true_solar(bj, lon)  → 当地真太阳时
      [3] datetime_to_shichen(tst)           → 当地十二时辰
      [4] solar_to_lunar_date(bj.date)      → 农历 + 干支（基于**北京时间的日期**）
      [5] 整合所有字段输出

    参数:
      dt:        冻结的 datetime（naive）。None = 当前时刻。
                 注意：无论传什么，都会被当作北京时间处理。
      longitude: 当地经度（东经正、西经负）。None = 不做 TST 校正。

    返回:
      dict，包含全部农历/干支/时辰/月将/TST 信息（字段同 get_current_lunar_info）。
    """
    # Step 1: 取北京时间
    bj_dt = get_beijing_time(dt)

    # Step 2: 当地真太阳时
    tst_info = longitude_to_true_solar(bj_dt, longitude)
    tst_dt = tst_info['tst_datetime']
    ts_hour = tst_info['tst_hour']

    # Step 3: 当地时辰（基于真太阳时）
    shichen_dz, shichen_idx = datetime_to_shichen(tst_dt)

    # Step 4: 农历 + 干支（按北京时间的日期）
    lunar = solar_to_lunar_date(bj_dt.year, bj_dt.month, bj_dt.day)

    # Step 5: 月将（按节气，按北京时间日期查）
    yuejiang_dz, yuejiang_name = get_yuejiang_by_solar_term(bj_dt.date())

    # 整合输出
    bj_hour = bj_dt.hour + bj_dt.minute / 60.0
    out = dict(lunar)
    out['bj_dt'] = bj_dt
    out['bj_hour'] = bj_hour
    out['tst_dt'] = tst_dt
    out['tst_hour'] = ts_hour
    out['hour'] = int(ts_hour)
    out['minute'] = tst_dt.minute
    out['shichen'] = shichen_dz
    out['shichen_idx'] = shichen_idx
    out['yuejiang_dz'] = yuejiang_dz
    out['yuejiang_name'] = yuejiang_name
    out['tst_offset_min'] = tst_info['tst_offset_min']
    if longitude is not None:
        out['longitude'] = longitude
        out['tst_corrected'] = tst_info['tst_corrected']

    return out


# 注意：以下原 get_current_lunar_info 函数保留（向后兼容），但内部改为调用 get_full_pipeline

# zhdate 提供农历转换，干支由本模块自行计算
try:
    from zhdate import ZhDate as _ZhDate
    _HAS_ZHDATE = True
except ImportError:
    _HAS_ZHDATE = False
    _ZhDate = None

# 六十甲子查找表
_LIUSHIFENJIA = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥',
]

# 日干支参考点：1900-01-01 = 甲戌日（六十甲子索引10）
_GANZHI_BASE_DATE = date(1900, 1, 1)
_GANZHI_BASE_INDEX = 10


def _get_days_from_base(d: date) -> int:
    """计算距 1900-01-01 的天数"""
    return (d - _GANZHI_BASE_DATE).days


def get_day_ganzhi(d: date = None) -> tuple:
    """
    获取指定日期的日干支。
    返回 (日干, 日支, 日干支)
    """
    if d is None:
        d = date.today()
    gz_idx = (_GANZHI_BASE_INDEX + _get_days_from_base(d)) % 60
    return (TIANGAN[gz_idx % 10], DIZHI[gz_idx % 12], _LIUSHIFENJIA[gz_idx])


def get_year_ganzhi(lunar_year: int) -> tuple:
    """
    获取农历年的年干支。
    返回 (年干, 年支, 年干支)
    """
    gz_idx = (lunar_year - 4) % 60
    return (TIANGAN[gz_idx % 10], DIZHI[gz_idx % 12], _LIUSHIFENJIA[gz_idx])


def _month_dz(lunar_month: int) -> str:
    """农历月 → 月支（正月=寅, 二月=卯, ...）"""
    return DIZHI[(lunar_month + 1) % 12]


def _month_tg(year_tg: str, lunar_month: int) -> str:
    """
    五虎遁：根据年干和农历月推算月干。
    口诀：甲己之年丙作首，乙庚之年戊为头，丙辛之年庚上起，丁壬壬位顺行流，戊癸之年甲寅。
    """
    tg_idx = TIANGAN.index(year_tg)
    # 正月月干起始索引
    month1_tg_idx = (tg_idx % 5) * 2 + 2  # 甲己=2(丙), 乙庚=4(戊), 丙辛=6(庚), 丁壬=8(壬), 戊癸=0(甲)
    return TIANGAN[(month1_tg_idx + lunar_month - 1) % 10]


def _tg_dz_to_gz(tg: str, dz: str) -> str:
    """天干+地支 → 六十甲子组合名（如 '甲子'）"""
    tg_idx = TIANGAN.index(tg)
    dz_idx = DIZHI.index(dz)
    if tg_idx % 2 != dz_idx % 2:
        return tg + dz  # 无效组合，但返回拼接作为 fallback
    for k in range(6):
        gz = dz_idx + k * 12
        if gz % 10 == tg_idx:
            return _LIUSHIFENJIA[gz % 60]
    return tg + dz


def get_month_ganzhi(year_tg: str, lunar_month: int) -> tuple:
    """
    根据年干和农历月推算月干支。
    返回 (月干, 月支, 月干支)
    """
    mtg = _month_tg(year_tg, lunar_month)
    mdz = _month_dz(lunar_month)
    gz = _tg_dz_to_gz(mtg, mdz)
    return (mtg, mdz, gz)


def solar_to_lunar_date(year: int, month: int, day: int) -> dict:
    """
    公历 → 农历 + 完整干支信息。
    依赖 zhdate 库进行农历转换。

    返回:
      {lunar_year, lunar_month, lunar_day, leap_month, is_current_month_leap,
       year_tg, year_dz, year_gz,
       month_tg, month_dz, month_gz,
       day_tg, day_dz, day_gz}
    """
    if not _HAS_ZHDATE:
        raise ImportError('zhdate library is required. Install: pip install zhdate')

    d = date(year, month, day)
    lunar = _ZhDate.from_datetime(datetime(year, month, day))
    is_leap = lunar.leap_month  # 0=无闰月，>0 表示该月是闰月号
    is_current_month_leap = (lunar.leap_month == lunar.lunar_month)

    # 年干支
    year_tg, year_dz, year_gz = get_year_ganzhi(lunar.lunar_year)
    # 月干支
    month_tg, month_dz, month_gz = get_month_ganzhi(year_tg, lunar.lunar_month)
    # 日干支
    day_tg, day_dz, day_gz = get_day_ganzhi(d)

    return {
        'solar_date': d.isoformat(),
        'lunar_year': lunar.lunar_year,
        'lunar_month': lunar.lunar_month,
        'lunar_day': lunar.lunar_day,
        'leap_month': is_leap if is_leap else None,  # 闰月号（如4表示闰四月），None=无闰月
        'is_current_month_leap': is_current_month_leap,  # 当前月是否为闰月
        'year_tg': year_tg,
        'year_dz': year_dz,
        'year_gz': year_gz,
        'month_tg': month_tg,
        'month_dz': month_dz,
        'month_gz': month_gz,
        'day_tg': day_tg,
        'day_dz': day_dz,
        'day_gz': day_gz,
    }


# ============================================================
# 节气与月将（大六壬核心依赖）
# ============================================================

# 节气 → 月将（地支, 名称），按近似阳历日期
_JIEQI_YUEJIANG = [
    # (阳历月, 阳历日, 节气名, 月将地支, 月将名)
    (1, 20, '大寒', '子', '神后'),
    (2, 19, '雨水', '亥', '登明'),
    (3, 21, '春分', '戌', '河魁'),
    (4, 20, '谷雨', '酉', '从魁'),
    (5, 21, '小满', '申', '传送'),
    (6, 21, '夏至', '未', '小吉'),
    (7, 22, '大暑', '午', '胜光'),
    (8, 23, '处暑', '巳', '太乙'),
    (9, 23, '秋分', '辰', '天罡'),
    (10, 23, '霜降', '卯', '太冲'),
    (11, 22, '小雪', '寅', '功曹'),
    (12, 22, '冬至', '丑', '大吉'),
]


def get_yuejiang_by_solar_term(d: date = None) -> tuple:
    """
    根据节气精确获取当前月将。
    返回 (月将地支, 月将名)
    """
    if d is None:
        d = date.today()

    m, day = d.month, d.day

    # 从大寒开始找：找到最后一个已过的节气
    # 扫描两次（跨年情况）
    candidates = []
    for i in range(len(_JIEQI_YUEJIANG)):
        jm, jd, jieqi, dz, name = _JIEQI_YUEJIANG[i]
        if (m > jm) or (m == jm and day >= jd):
            candidates.append((jm, jd, dz, name, jieqi))

    if candidates:
        return (candidates[-1][2], candidates[-1][3])
    # 如果还没到大寒（1月1日-1月19日），取上一年的冬至（即上一轮最后一个）
    return ('丑', '大吉')


# ============================================================
# 一站式当前信息获取
# ============================================================

def get_current_lunar_info(dt: datetime = None, longitude: float = None, latitude: float = None) -> dict:
    """
    获取当前（或指定）时刻的完整农历/干支/时辰/月将信息。
    所有涉时脚本的 --auto 模式统一调用此函数。

    当前实现:
      - 时间基准改为"北京时间"（UTC+8），不再用 datetime.now() 拿本地挂钟时间
      - 内部调用 get_full_pipeline()，行为可通过该函数理解
      - 向后兼容：入参/返回字段不变

    参数:
      dt:         冻结时间（naive datetime 对象，按"北京时间"处理），None = 当前时刻。
                  SKILL 调用时应在流程入口立即执行 snapshot = datetime.now() 并传入此处。
      longitude:  当地经度（东经正、西经负，如成都 = 104.06, 纽约 = -74.006），
                  传入 None 则不进行真太阳时修正。
      latitude:   当地北纬（保留参数，当前未使用）。

    返回字段:
      solar_date, lunar_year, lunar_month, lunar_day, leap_month, is_current_month_leap,
      year_tg, year_dz, year_gz,
      month_tg, month_dz, month_gz,
      day_tg, day_dz, day_gz,
      hour (修正后小时), bj_hour (北京时间小时), ts_hour (真太阳时小时),
      shichen (地支), shichen_idx (1-12),
      yuejiang_dz, yuejiang_name,
      (若启用 TST) longitude, tst_corrected: true, tst_offset_min

    警告:
      调用方传入的 dt 应当是"北京时间"的 naive datetime（早期 SKILL
      流程传入的可能是本地挂钟时间，结果会有差异）。SKILL 流程应改为：
        bj = get_beijing_time()
        info = get_current_lunar_info(dt=bj, longitude=104.06)
    """
    # 当前实现: 内部改用 get_full_pipeline
    out = get_full_pipeline(dt=dt, longitude=longitude)
    # 兼容旧调用方：补充 latitude 字段（如果传了）
    if latitude is not None and longitude is not None:
        out['latitude'] = latitude
    return out


# ============================================================
# 参数验证工具函数（供各脚本复用）
# ============================================================

def validate_int_range(value, name, min_val, max_val):
    """验证整数范围，不合法则抛出 ValueError"""
    if not isinstance(value, int) or value < min_val or value > max_val:
        raise ValueError(f'{name} 必须为 {min_val}-{max_val} 的整数，当前值: {value}')


def validate_month(month):
    validate_int_range(month, '月', 1, 12)

def validate_day(day):
    validate_int_range(day, '日', 1, 30)

def validate_hour(hour):
    validate_int_range(hour, '时', 0, 23)


if __name__ == '__main__':
    import json, argparse, sys

    parser = argparse.ArgumentParser(description='农历/干支/真太阳时信息查询')
    parser.add_argument('--snapshot', action='store_true',
                        help='冻结当前时间并输出完整 JSON（用于 SKILL 流程入口锚定）')
    parser.add_argument('--city', type=str, default='',
                        help='城市名用于真太阳时校准（如"成都"、"New York"、"纽约"），支持国内外城市')
    parser.add_argument('--lon', type=float, default=None,
                        help='直接指定东经（如 104.06），西经为负（如 -74.006）')
    args = parser.parse_args()

    if args.snapshot:
        # 冻结时间 + 城市坐标（使用 get_beijing_time() 确保海外用户也取到北京时间）
        snapshot_dt = get_beijing_time()
        lon = args.lon
        city_name = None
        geo_source = None
        if args.city:
            coord = get_city_coordinates(args.city)
            if coord:
                lon = coord['longitude']
                city_name = coord['name']
                geo_source = coord.get('source', 'unknown')

        info = get_current_lunar_info(dt=snapshot_dt, longitude=lon)
        info['frozen_at'] = snapshot_dt.isoformat()
        info['city'] = city_name
        if geo_source:
            info['geo_source'] = geo_source
        print(json.dumps(info, ensure_ascii=False, indent=2, default=str))
        sys.exit(0)

    # Default: interactive demo
    print("=== 当前时间农历/干支信息（北京时间） ===")
    info = get_current_lunar_info()
    print(json.dumps(info, ensure_ascii=False, indent=2, default=str))

    print("\n=== 当前时间农历/干支信息（成都真太阳时） ===")
    info_cd = get_current_lunar_info(longitude=104.06, latitude=30.67)
    print(json.dumps(info_cd, ensure_ascii=False, indent=2, default=str))

    print("\n=== 日干支验证 ===")
    today = date.today()
    day_tg, day_dz, day_gz = get_day_ganzhi(today)
    print(f"今日日干支: {day_gz} (日干={day_tg}, 日支={day_dz})")

    print("\n=== 月将验证 ===")
    yj_dz, yj_name = get_yuejiang_by_solar_term(today)
    print(f"当前月将: {yj_dz}({yj_name})")

    print("\n=== 均时差验证（今日） ===")
    eot = _eot_minutes(today)
    print(f"均时差: {eot:+.1f} 分钟")

    print("\n=== 城市坐标查询 ===")
    for c in ['成都', '四川成都', '重庆', '日喀则']:
        coord = get_city_coordinates(c)
        print(f"  {c}: {coord}")
