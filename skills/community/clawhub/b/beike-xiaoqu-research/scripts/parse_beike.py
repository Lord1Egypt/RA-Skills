#!/usr/bin/env python3
"""
贝壳找房页面文本解析器 v2.2

用法：
    python3 parse_beike.py xiaoqu      < /tmp/xiaoqu.txt      # 解析小区详情页（innerText）
    python3 parse_beike.py ershou      < /tmp/ershou.txt      # 解析在售二手房
    python3 parse_beike.py chengjiao   < /tmp/chengjiao.txt   # 解析成交记录
    python3 parse_beike.py region_list < /tmp/region.txt      # 解析板块小区列表页
    python3 parse_beike.py css_merge   < /tmp/css.json        # P1-2: 合并 CSS 提取结果（优先）与 innerText 兜底
    python3 parse_beike.py check       < /tmp/page.txt        # 仅检测验证码

输出：JSON 格式结构化数据
退出码：
  0 = 成功
  2 = 验证码检测
  3 = 关键字段解析失败（结构可能已变更）
  4 = headless 模式遇到验证码
"""

import sys
import re
import json
from typing import Optional


# ──────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────

def check_captcha(text: str) -> bool:
    return bool(re.search(r'请在下图|请按语序', text))


PARSE_ERRORS: list = []  # 全局解析错误收集


def g(pattern: str, text: str, default: str = '', field: str = '') -> str:
    """普通正则提取。匹配失败时记录到 PARSE_ERRORS，不静默返回空字符串。"""
    m = re.search(pattern, text)
    if m:
        return m.group(1).strip()
    if field:
        PARSE_ERRORS.append(f'PARSE_MISS: field={field!r} pattern={pattern!r}')
    return default


def g_next_line(label: str, text: str, default: str = '') -> str:
    """贝壳详情页格式：字段名\\n值，需跨行提取。匹配失败时记录错误。"""
    pattern = re.escape(label) + r'\n([^\n]+)'
    m = re.search(pattern, text)
    if m:
        return m.group(1).strip()
    PARSE_ERRORS.append(f'PARSE_MISS: label={label!r}')
    return default


# ──────────────────────────────────────────
# 解析器
# ──────────────────────────────────────────

def parse_xiaoqu(text: str) -> dict:
    """解析小区详情页（贝壳 /xiaoqu/{ID}/）

    贝壳详情页格式：字段名和值分两行，且字段名中有 \\xa0 非断行空格。
    """
    PARSE_ERRORS.clear()
    result = {
        # 均价在同行：73859元/㎡2月参考均价
        'avg_price': g(r'(\d+)元/㎡\d+月参考均价', text, field='avg_price'),
        # 以下字段格式：字段名\n值
        'building_type':   g_next_line('建筑类型', text),
        'total_units':     re.sub(r'\D', '', g_next_line('房屋总数', text)),
        'total_buildings': re.sub(r'\D', '', g_next_line('楼栋总数', text)),
        'green_rate':      g_next_line('绿化率', text),
        'far':             g_next_line('容积率', text),
        'ownership':       g_next_line('交易权属', text),
        'built_year':      g_next_line('建成年代', text),
        'mgmt_fee':        g_next_line('物业费', text),
        'mgmt_company':    g_next_line('物业公司', text)[:25],
        'developer':       g_next_line('开发商', text)[:25],
        'followers':       g(r'(\d+)人关注', text),
        # 在售/成交/带看在小区卡片中
        'on_sale':         g(r'二手房源\n?(\d+)套', text),
        'sold_90d':        g(r'近90天成交\n?(\d+)套', text),
        'views_30d':       g(r'近30天带看\n?(\d+)次', text),
    }

    # P0-2: 关键字段缺失时显式标记，不静默通过
    critical_fields = ['avg_price', 'built_year', 'building_type']
    missing = [f for f in critical_fields if not result.get(f)]
    if missing:
        result['_parse_warnings'] = PARSE_ERRORS[:]
        result['_missing_critical'] = missing
        # 不抛异常（页面可能正常但字段格式变化），但调用方可检查此字段

    # 地铁（可能有 \xa0）
    metros = re.findall(r'(\d+)米[\s\xa0]*(地铁\d+号线\S*|嘉闵线\S*|金山铁路\S*)', text)
    result['metros'] = [
        {'distance_m': int(m[0]), 'line': m[1].strip()[:30]}
        for m in metros[:6]
    ]

    # 出租参考
    rentals = re.findall(r'整租[^\n]*?(\d+)室[^\n]*?(\d+)元/月', text)
    result['rentals'] = [{'rooms': r[0], 'monthly_rent': int(r[1])} for r in rentals[:4]]

    return result


def parse_ershou(text: str) -> dict:
    """解析在售二手房列表（贝壳 /ershoufang/rs{名}/）"""
    parking_notes = len(re.findall(r'产权车位', text))
    elevator_notes = len(re.findall(r'有电梯', text))

    # 挂牌总价（万元）
    prices = [int(p) for p in re.findall(r'\n(\d{3,4})\n万\n', text)]

    # 三房/四房房源
    listings_3br = []
    pat = re.compile(
        r'(3室\d厅|4室\d厅)\n(\w+楼层[^\n]+)\n[^\n]*\n'
        r'.*?(\d{3,4})\n万\n\s*([\d,]+)元/平',
        re.DOTALL
    )
    for m in pat.finditer(text):
        listings_3br.append({
            'type': m.group(1),
            'floor': m.group(2)[:30],
            'price_wan': int(m.group(3)),
            'unit_price': m.group(4).replace(',', ''),
        })

    return {
        'parking_mention_count':  parking_notes,
        'elevator_mention_count': elevator_notes,
        'all_prices_wan':         sorted(prices),
        'price_min':              min(prices) if prices else None,
        'price_max':              max(prices) if prices else None,
        'price_median':           sorted(prices)[len(prices)//2] if prices else None,
        'listings_3br':           listings_3br[:10],
        'total_listings_approx':  len(prices),
    }


def parse_chengjiao(text: str) -> dict:
    """解析成交记录（贝壳 /chengjiao/rs{名}/）"""
    dates   = re.findall(r'(\d{4}\.\d{2}\.\d{2})', text)
    periods = [int(p) for p in re.findall(r'成交周期(\d+)天', text)]
    types   = re.findall(r'(\d+室\d+厅|车位)', text)

    parking_sales = len([t for t in types if t == '车位'])
    cutoff        = '2025.03'
    recent_dates  = [d for d in dates if d >= cutoff]

    fast   = [p for p in periods if p <= 60]
    medium = [p for p in periods if 60 < p <= 180]
    slow   = [p for p in periods if p > 180]

    return {
        'total_records':       len(dates),
        'recent_12m_count':    len(recent_dates),
        'monthly_avg':         round(len(recent_dates) / 12, 1) if recent_dates else 0,
        'parking_sales_count': parking_sales,
        'has_parking_sales':   parking_sales > 0,
        'period_avg_days':     round(sum(periods) / len(periods)) if periods else 0,
        'period_min_days':     min(periods) if periods else None,
        'period_max_days':     max(periods) if periods else None,
        'fast_sales_count':    len(fast),
        'medium_sales_count':  len(medium),
        'slow_sales_count':    len(slow),
        'recent_dates':        dates[:10],
        'recent_periods':      periods[:10],
        'all_types':           types[:20],
    }


def parse_region_list(text: str, filters: Optional[dict] = None) -> dict:
    """解析贝壳板块小区列表页（/xiaoqu/minhang/{板块}/）

    贝壳列表页结构（每8行一个小区）：
        行 i-1:  小区名
        行 i:    ' 90天成交N套'（标志行）
        行 i+1:  ' 闵行\xa0板块\xa0 /\xa0年份'
        行 i+2:  '近地铁XXX'（可选）
        行 i+3:  均价元/m2
        行 i+4:  月份参考均价
        行 i+5:  N套
        行 i+6:  '在售二手房'

    filters: {
        'min_year': 2005,        # 最新建成年份 >=
        'min_price': 40000,      # 均价 >=
        'max_price': 110000,     # 均价 <=
        'min_on_sale': 2,        # 在售套数 >=
        'exclude_kw': ['别墅','公寓','银座','大厦','写字楼'],
    }
    """
    if filters is None:
        filters = {
            'min_year':    2005,
            'min_price':   40000,
            'max_price':   110000,
            'min_on_sale': 2,
            'exclude_kw':  ['别墅', '公寓', '银座', '大厦', '写字楼'],
        }

    lines = text.split('\n')
    all_xiaoqu = []
    filtered    = []

    for i, line in enumerate(lines):
        if '90天成交' not in line or i == 0:
            continue

        name = lines[i - 1].strip()
        if not name or len(name) < 2 or len(name) > 25:
            continue
        # 排除导航栏干扰行
        if any(kw in name for kw in ['共找到', '筛选', '清空', '均价', '在售', '元/', '地铁', '闵行', '浦东']):
            continue

        ctx_lines = lines[i:min(i + 9, len(lines))]
        ctx       = '\n'.join(ctx_lines)

        sold_m  = re.search(r'90天成交(\d+)套', line)
        year_m  = re.search(r'/[\s\xa0]*([\d\-年]+)', ctx)
        price_m = re.search(r'(\d+)元/m2', ctx)
        metro_m = re.search(r'近地铁(\S+)', ctx)

        on_sale = 0
        for cl in ctx_lines:
            cl = cl.strip()
            m  = re.match(r'^(\d+)套?$', cl)
            if m and '在售二手房' in '\n'.join(ctx_lines[ctx_lines.index(lines[i]):]):
                on_sale = int(m.group(1))
                break
        # 备用：找"在售二手房"前一行
        if on_sale == 0:
            for j, cl in enumerate(ctx_lines):
                if '在售二手房' in cl and j > 0:
                    prev = ctx_lines[j - 1].strip()
                    m    = re.match(r'^(\d+)套?$', prev)
                    if m:
                        on_sale = int(m.group(1))
                    break

        if not (year_m and price_m):
            continue

        year_str = year_m.group(1).replace('年', '')
        price    = int(price_m.group(1))
        sold     = int(sold_m.group(1)) if sold_m else 0

        # 计算最新建成年份
        years    = re.findall(r'\d{4}', year_str)
        max_year = max(int(y) for y in years) if years else 0

        entry = {
            'name':     name,
            'year':     year_str,
            'max_year': max_year,
            'price':    price,
            'on_sale':  on_sale,
            'sold_90d': sold,
            'metro':    metro_m.group(1)[:25] if metro_m else '',
        }
        all_xiaoqu.append(entry)

        # 应用过滤条件
        if (filters['min_price'] <= price <= filters['max_price']
                and max_year >= filters['min_year']
                and on_sale >= filters['min_on_sale']
                and not any(kw in name for kw in filters['exclude_kw'])):
            filtered.append(entry)

    filtered.sort(key=lambda x: (-x['sold_90d'], -x['on_sale'], x['price']))

    return {
        'total_found': len(all_xiaoqu),
        'filtered_count': len(filtered),
        'filters_applied': filters,
        'candidates': filtered,
        'all': all_xiaoqu,
    }


# ──────────────────────────────────────────
# 入口
# ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: parse_beike.py [xiaoqu|ershou|chengjiao|region_list|check]", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    text = sys.stdin.read()

    # P1-2: css_merge 模式 — 直接解析 stdin 为 JSON，不做 captcha 文本检测
    if mode == 'css_merge':
        try:
            css_data = json.loads(text)
        except json.JSONDecodeError:
            print('[ERROR] css_merge 需要 JSON 输入（来自 read_css_json 函数）', file=sys.stderr)
            sys.exit(1)

        if css_data.get('captcha'):
            print('[CAPTCHA] CSS 提取检测到验证码', file=sys.stderr)
            sys.exit(2)

        empty_fields = [k for k, v in css_data.items()
                        if not str(v) and not k.startswith('_') and k != 'captcha']
        if empty_fields:
            css_data['_css_empty_fields'] = empty_fields

        critical = ['avg_price', 'built_year', 'building_type']
        missing = [f for f in critical if not css_data.get(f)]
        if missing:
            css_data['_missing_critical'] = missing
            print(f'[WARN] CSS 关键字段缺失: {missing}，建议追加 innerText 兜底', file=sys.stderr)

        print(json.dumps(css_data, ensure_ascii=False, indent=2))
        return

    if check_captcha(text):
        print(json.dumps({
            'error':   'captcha',
            'message': '检测到验证码，请在 Chrome 中手动完成点击，完成后告知 Agent 继续'
        }, ensure_ascii=False, indent=2))
        sys.exit(2)

    if mode == 'check':
        print(json.dumps({'status': 'ok', 'length': len(text)}, ensure_ascii=False))
        return

    # region_list 支持通过命令行传 JSON filters
    if mode == 'region_list':
        filters = None
        if len(sys.argv) >= 3:
            try:
                filters = json.loads(sys.argv[2])
            except Exception:
                pass
        result = parse_region_list(text, filters)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    parsers = {
        'xiaoqu':    parse_xiaoqu,
        'ershou':    parse_ershou,
        'chengjiao': parse_chengjiao,
    }

    if mode not in parsers:
        print(f"未知模式: {mode}，可用: {list(parsers.keys()) + ['region_list', 'css_merge']}", file=sys.stderr)
        sys.exit(1)

    result = parsers[mode](text)

    # P0-2: 打印解析警告到 stderr，不污染 JSON stdout
    if PARSE_ERRORS:
        import sys as _sys
        for warn in PARSE_ERRORS:
            print(f'[WARN] {warn}', file=_sys.stderr)

    # P0-2: 关键字段缺失时以非零退出码标记（方便调用方检测）
    missing = result.get('_missing_critical', [])
    if missing:
        import sys as _sys
        print(f'[ERROR] 关键字段解析失败: {missing}（贝壳页面结构可能已变更）', file=_sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        _sys.exit(3)  # exit 3 = 解析部分失败

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
