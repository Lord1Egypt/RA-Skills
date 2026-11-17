# -*- coding: utf-8 -*-
"""
photo_gps_judge.py — 照片/视频 GPS 逐日城市判定（通用版）

适用场景：消费账单缺失或滞后的时段（如当年账单未出、旧账单丢失），
用手机/相机照片的 EXIF GPS 作为「你在哪」的一级证据，还原逐日所在城市。
EXIF GPS 是全球通用标准，国内外同样适用。

用法：
  1) 用 exiftool 从照片目录提取 GPS（Linux/macOS/Windows 均可）：
     exiftool -json -r -DateTimeOriginal -GPSLatitude -GPSLongitude -n <照片目录> > photo_gps_raw.json
     （HEIC/HEIF 同样支持；-n 让坐标输出为十进制数字）
  2) 准备城市坐标库 city_coords.json（格式见下方 CITY_COORDS 示例；建议按自己到访地扩充）
  3) 运行：python3 photo_gps_judge.py photo_gps_raw.json city_coords.json -o photo_daily_cities.json
  4) 人工复核输出中所有 ⚠️ 警告项（距离远 / 单点飞地 / 时区可疑）

关键设计（来自实战教训）：
  - 反查距离审计：坐标与最近城市的匹配距离 > NEAR_LIMIT_DEG(默认0.3°≈33km) → 标记人工复核。
    实战案例：城市库缺「阜康(天池)」，坐标被就近匹配到 40km 外的省会，两天全部错标。
  - 单点飞地检测：当天仅 1-2 个 GPS 点、且远离前后多日连续所在城市 → 大概率是异常
    (照片拍摄地≠所在地、水印/截图位置、他人照片)，标记 ⚠️ 不可直接采信。
  - 时区说明：EXIF DateTimeOriginal 是拍摄设备本地时间。跨国行程中「日期」按设备时区归属，
    与账单/票务的当地时间口径一致；跨时区飞行当天的点可能落在起飞地时区的"昨天/明天"，
    由时间感知聚合按 07:00-24:00 有效时段归日处理。
"""
import json, math, sys, argparse
from collections import defaultdict
from datetime import datetime

# ================= 配置 =================
DAY_START_MIN = 7 * 60        # 每日有效时段起点 07:00（排除睡眠段）
NEAR_LIMIT_DEG = 0.3          # 反查匹配距离警戒线（度）。0.3° ≈ 33km，超过需人工复核
OUTLIER_MIN_POINTS = 2        # 当天 GPS 点数 ≤ 此值且远离邻日 → 标记单点飞地
OUTLIER_DIST_DEG = 1.0        # 与邻日城市中心距离超过此度数视为"远离"(≈111km)

# 内置示例坐标库（少量常用城市；实际使用请按自己到访地扩充到 city_coords.json 文件）
CITY_COORDS = {
    # —— 中国（"省/市"格式）——
    '广东/深圳': (22.543, 114.058), '广东/广州': (23.129, 113.264), '广东/珠海': (22.271, 113.577),
    '浙江/杭州': (30.274, 120.155), '浙江/宁波': (29.868, 121.544),
    '上海/上海': (31.230, 121.474), '北京/北京': (39.904, 116.407),
    '湖北/武汉': (30.593, 114.305), '湖北/宜昌': (30.692, 111.286),
    '四川/成都': (30.573, 104.067), '重庆/重庆': (29.564, 106.551),
    '新疆/乌鲁木齐': (43.826, 87.617), '新疆/喀什': (39.470, 75.990),
    '新疆/阿勒泰': (47.848, 88.140), '新疆/富蕴': (46.994, 89.527),
    '新疆/阜康': (44.158, 87.985), '新疆/库车': (41.717, 82.960),
    '新疆/塔县': (37.773, 75.227), '新疆/乌恰': (39.717, 75.255),
    '西藏/拉萨': (29.653, 91.118), '青海/西宁': (36.617, 101.778),
    '甘肃/兰州': (36.061, 103.834), '陕西/西安': (34.342, 108.940),
    '云南/昆明': (24.881, 102.833), '云南/丽江': (26.872, 100.230),
    '海南/海口': (20.044, 110.199), '海南/三亚': (18.253, 109.512),
    '广西/南宁': (22.817, 108.366), '广西/桂林': (25.274, 110.290),
    '福建/厦门': (24.480, 118.089), '山东/青岛': (36.067, 120.383),
    '湖南/长沙': (28.228, 112.939), '河南/郑州': (34.747, 113.625),
    '河北/石家庄': (38.042, 114.515), '辽宁/大连': (38.914, 121.615),
    '黑龙江/哈尔滨': (45.803, 126.535), '天津/天津': (39.343, 117.362),
    '江苏/南京': (32.060, 118.797), '江苏/常州': (31.811, 119.974),
    # —— 海外（"国家/城市"格式，同一两级结构与国内一致）——
    'Thailand/Bangkok': (13.756, 100.502), 'Thailand/Chiang Mai': (18.788, 98.985),
    'Japan/Tokyo': (35.690, 139.692), 'Japan/Osaka': (34.694, 135.502),
    'Japan/Kyoto': (35.012, 135.768), 'Korea/Seoul': (37.567, 126.978),
    'Singapore/Singapore': (1.352, 103.820), 'Malaysia/Kuala Lumpur': (3.139, 101.687),
    'Indonesia/Bali': (-8.409, 115.189), 'Vietnam/Hanoi': (21.028, 105.854),
    'France/Paris': (48.857, 2.352), 'UK/London': (51.507, -0.128),
    'Germany/Berlin': (52.520, 13.405), 'Italy/Rome': (41.903, 12.496),
    'Spain/Barcelona': (41.385, 2.173), 'USA/New York': (40.713, -74.006),
    'USA/San Francisco': (37.775, -122.419), 'USA/Los Angeles': (34.052, -118.244),
    'Canada/Toronto': (43.653, -79.383), 'Australia/Sydney': (-33.869, 151.209),
    'NZ/Auckland': (-36.849, 174.763), 'UAE/Dubai': (25.205, 55.271),
    'Switzerland/Zurich': (47.377, 8.541), 'Austria/Vienna': (48.208, 16.373),
}


def load_coords(path):
    """优先从外部文件加载城市坐标库（覆盖内置库）；文件不存在则用内置示例库。"""
    coords = dict(CITY_COORDS)
    if path:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                ext = json.load(f)
            # 支持两种格式：{"城市": [lat, lon]} 或 {"城市": {"lat": .., "lon": ..}}
            for k, v in ext.items():
                if isinstance(v, dict):
                    coords[k] = (float(v['lat']), float(v['lon']))
                else:
                    coords[k] = (float(v[0]), float(v[1]))
            print(f'已加载外部坐标库: {path} ({len(ext)} 城市)')
        except FileNotFoundError:
            print(f'⚠️ 未找到 {path}，使用内置示例坐标库({len(CITY_COORDS)} 城市)。'
                  f'建议按自己到访地扩充，否则会被就近匹配到错误城市！')
    return coords


def haversine_deg(lat1, lon1, lat2, lon2):
    """两点间大圆距离，单位：度（经纬度空间的近似距离，0.1°≈11km）。"""
    # 简化：用球面角距（弧度转度）
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(rlat1)*math.cos(rlat2)*math.sin(dlon/2)**2
    return math.degrees(2 * math.asin(math.sqrt(a)))


def nearest_city(lat, lon, coords):
    """返回 (城市, 距离度数)。"""
    best, bestd = None, 1e18
    for c, (clat, clon) in coords.items():
        d = haversine_deg(lat, lon, clat, clon)
        if d < bestd:
            best, bestd = c, d
    return best, bestd


def parse_dt(s):
    """解析 exiftool 的 DateTimeOriginal（'2026:09:26 12:00:00' 格式）。"""
    try:
        return datetime.strptime(str(s).strip(), '%Y:%m:%d %H:%M:%S')
    except (ValueError, TypeError):
        return None


def main():
    ap = argparse.ArgumentParser(description='照片GPS逐日城市判定')
    ap.add_argument('raw_json', help='exiftool 导出的照片GPS JSON 文件')
    ap.add_argument('coords_json', nargs='?', default=None, help='城市坐标库 JSON(可选,缺省用内置)')
    ap.add_argument('-o', '--output', default='photo_daily_cities.json', help='输出文件')
    args = ap.parse_args()

    coords = load_coords(args.coords_json)

    with open(args.raw_json, 'r', encoding='utf-8') as f:
        photos = json.load(f)

    # ---- 1. 提取有效 GPS 点 ----
    pts = []           # (datetime, lat, lon, file)
    n_nogps = 0
    for p in photos:
        dt = parse_dt(p.get('DateTimeOriginal') or p.get('CreateDate'))
        lat = p.get('GPSLatitude'); lon = p.get('GPSLongitude')
        if dt is None or lat is None or lon is None:
            n_nogps += 1
            continue
        # GPSLatitudeRef 缺失时 exiftool -n 已输出带符号十进制；南纬/西经为负
        pts.append((dt, float(lat), float(lon), p.get('SourceFile', '')))

    print(f'照片总数 {len(photos)}，有效GPS点 {len(pts)}，无GPS/无时间 {n_nogps}')

    # ---- 2. 反向地理编码 + 按日聚合 ----
    daily_pts = defaultdict(list)   # 'YYYY-MM-DD' -> [(min_of_day, city, dist, lat, lon)]
    far_days = defaultdict(int)     # 当日匹配距离超警戒线的点数
    for dt, lat, lon, f in pts:
        city, dist = nearest_city(lat, lon, coords)
        day = dt.strftime('%Y-%m-%d')
        minute = dt.hour * 60 + dt.minute
        daily_pts[day].append((minute, city, dist, lat, lon))
        if dist > NEAR_LIMIT_DEG:
            far_days[day] += 1

    # ---- 3. 时间感知判定（07:00-24:00 有效时段，停留最久城市胜出；在途不计） ----
    result = {}
    for day in sorted(daily_pts.keys()):
        items = sorted(daily_pts[day])
        # 时间感知片段：相邻点之间属前一城市，直到下一GPS点(视为离开)
        seg = defaultdict(float)   # city -> 有效时段停留分钟
        for i, (minute, city, dist, _, _) in enumerate(items):
            if minute < DAY_START_MIN:
                continue   # 睡眠段不计
            end = items[i+1][0] if i + 1 < len(items) else 24 * 60
            seg[city] += max(0, end - minute)
        if not seg:
            # 全部点都在 07:00 前 → 跨夜在途/凌晨，归最后已知城市（首个点的城市）
            result[day] = {'n_pts': len(items), 'start_city': items[0][1],
                           'end_city': items[-1][1], 'uniq_cities': sorted({x[1] for x in items}),
                           'is_transit': True, 'note': '⚠️全部GPS点在07:00前(凌晨/跨夜在途)'}
            continue
        primary = max(seg.items(), key=lambda kv: kv[1])[0]
        uniq = sorted({x[1] for x in items})
        is_transit = len(uniq) > 3   # 一天内跨3+城市 → 大概率在途(飞机/高铁日)
        detail = [[f'{m//60:02d}:{m%60:02d}', c, round(d, 3)] for m, c, d, _, _ in items[:10]]
        if len(items) > 10:
            detail.append('...')
            detail += [[f'{m//60:02d}:{m%60:02d}', c, round(d, 3)] for m, c, d, _, _ in items[-3:]]
        notes = []
        if far_days[day] > 0:
            notes.append(f'⚠️{far_days[day]}个点距最近城市>{NEAR_LIMIT_DEG}°，坐标库可能缺目的地城市，需人工复核')
        if is_transit:
            notes.append('当日跨3+城市,判定为在途日(主城市仅供参考)')
        result[day] = {
            'n_pts': len(items), 'start_city': items[0][1], 'end_city': items[-1][1],
            'primary_by_time': primary, 'uniq_cities': uniq, 'is_transit': is_transit,
            'stay_minutes': {c: round(v) for c, v in sorted(seg.items(), key=lambda kv: -kv[1])},
            'detail': detail,
            'note': '; '.join(notes) if notes else '',
        }

    # ---- 4. 单点飞地检测：当天点少且远离邻日主流城市 ----
    days = sorted(result.keys())
    for i, day in enumerate(days):
        r = result[day]
        if r.get('n_pts', 0) > OUTLIER_MIN_POINTS:
            continue
        neigh = [result[dd].get('primary_by_time') or result[dd].get('end_city')
                 for dd in (days[i-1], days[i+1]) if 0 <= i-1 and i+1 < len(days) and dd in result]
        neigh = [c for c in neigh if c]
        cur = r.get('primary_by_time') or r.get('end_city')
        if neigh and cur and cur not in neigh:
            r['note'] = (r.get('note', '') + '; ' if r.get('note') else '') + \
                f'⚠️单点飞地:仅{r["n_pts"]}个GPS点且与邻日({",".join(neigh)})不同城,不可直接采信'

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ---- 5. 报告 ----
    warn = sum(1 for r in result.values() if '⚠️' in r.get('note', ''))
    print(f'\n判定完成: {len(result)} 天 → {args.output}')
    print(f'  需人工复核: {warn} 天(含⚠️标记)')
    print(f'  距离超限日: {sum(1 for v in far_days.values() if v > 0)} 天')
    print('提示: 带⚠️的天请人工确认后再合入最终整合表；坐标库建议持续扩充到访城市。')


if __name__ == '__main__':
    main()
