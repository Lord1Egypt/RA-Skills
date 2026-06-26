#!/usr/bin/env python3
"""
Citywalk Map Generator — 零成本生成真实 OSM 城市步行路线图

Usage:
    python3 generate.py "路线标题" "lat1,lon1,name1,desc1|lat2,lon2,name2,desc2|..."
    COLOR=hex python3 generate.py ...          # 自定义主题色（默认 #e94560）
    python3 generate.py --help                # 查看完整帮助

Options:
    --output PATH     输出 HTML 路径（默认 /tmp/citywalk_map.html）
    --visit-time N    每站停留分钟数（默认 30）
    --no-tips         隐藏实用贴士
    --lang LANG       界面语言：zh / en（默认 zh）
    --weather         查询并显示目的地天气（wttr.in 免费接口）
    --validate        用 Nominatim 验坐标有效性

依赖: 仅 Python 3 标准库（无需 pip install）
"""
import sys
import os
import json
import math
import time
import subprocess
import argparse

# ── Formatting helpers ────────────────────────────────────────────────────────

def fmt_d(m):
    return f"{m / 1000:.1f}km" if m >= 1000 else f"{int(m)}m"

def fmt_t(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    return f"{h}h{m}m" if h > 0 else f"{m}min"

def darken(hex_color):
    """把颜色加深 25%，处理极端值防止溢出"""
    if hex_color.startswith('#'):
        try:
            r = min(255, int(int(hex_color[1:3], 16) * 0.75))
            g = min(255, int(int(hex_color[3:5], 16) * 0.75))
            b = min(255, int(int(hex_color[5:7], 16) * 0.75))
            return f'#{r:02x}{g:02x}{b:02x}'
        except ValueError:
            return '#e94560'
    return '#e94560'

# ── OSRM routing (with retry + backoff) ──────────────────────────────────────

def get_osrm_route(waypoints, retries=2):
    """并发调用 OSRM 步行路由，失败自动退避重试"""
    total_distance = 0
    total_duration = 0
    full_route_coords = []

    for i in range(len(waypoints) - 1):
        p1, p2 = waypoints[i], waypoints[i + 1]
        lon1, lat1 = p1['lon'], p1['lat']
        lon2, lat2 = p2['lon'], p2['lat']
        url = f"https://router.project-osrm.org/route/v1/foot/{lon1},{lat1};{lon2},{lat2}"

        for attempt in range(retries + 1):
            cmd = [
                'curl', '-s', '--max-time', '10',
                url, '-G',
                '--data-urlencode', 'overview=full',
                '--data-urlencode', 'geometries=geojson'
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
                data = json.loads(result.stdout)
                if data.get('code') == 'Ok':
                    route = data['routes'][0]
                    total_distance += route['distance']
                    # OSRM duration 是骑行速度，改用步行速度 5 km/h 换算
                    total_duration += route['distance'] / 1.39
                    coords = route['geometry']['coordinates']
                    full_route_coords.extend([[c[1], c[0]] for c in coords])
                    break
                # 429 / 限流，等待后重试
                if data.get('code') in ('Busy', 'Too Many Requests') and attempt < retries:
                    wait = 2 ** attempt
                    print(f"  OSRM 限流，{wait}s 后重试...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise ValueError(f"OSRM error: {data.get('code')}")
            except Exception as e:
                if attempt < retries:
                    wait = 2 ** attempt
                    print(f"  OSRM error: {e}，{wait}s 后重试...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                # 最后一次也失败了，用直线 fallback
                print(f"  OSRM 失败，使用直线 fallback: {e}", file=sys.stderr)
                dlat = (lat2 - lat1) * 111000
                dlon = (lon2 - lon1) * 111000 * math.cos(math.radians(lat1))
                dist = math.sqrt(dlat ** 2 + dlon ** 2)
                total_distance += dist * 1.3
                total_duration += dist * 1.3 / 1.1
                full_route_coords.append([lat1, lon1])
                full_route_coords.append([lat2, lon2])

    return total_distance, total_duration, full_route_coords

# ── Weather (wttr.in — free, no API key) ──────────────────────────────────────

def get_weather(lat, lon, lang='zh'):
    """用 wttr.in 获取目的地当前天气描述"""
    url = f"https://wttr.in/{lat},{lon}?format=j1&lang={lang}"
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '8', url],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(result.stdout)
        current = data.get('current_condition', [{}])[0]
        temp = current.get('temp_C', '?')
        desc = current.get('weatherDesc', [{}])[0].get('value', '')
        icon = current.get('weatherCode', '113')
        # wttr.in 图标码映射到 emoji
        code_map = {
            '113': '☀️', '116': '⛅', '119': '☁️', '122': '☁️',
            '143': '🌫️', '176': '🌦️', '179': '🌨️', '182': '🌨️',
            '200': '⛈️', '227': '🌨️', '230': '❄️', '248': '🌫️',
            '260': '🌫️', '263': '🌧️', '266': '🌧️', '281': '🌨️',
        }
        emoji = code_map.get(icon, '🌡️')
        return f"{emoji} {temp}°C {desc}", temp, desc, emoji
    except Exception as e:
        print(f"  天气查询失败: {e}", file=sys.stderr)
        return None, None, None, None

# ── Nominatim coordinate validation ─────────────────────────────────────────

def validate_coords(lat, lon, name):
    """用 Nominatim 验证坐标是否落在有效陆地区域"""
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '6', '-H', 'User-Agent: CitywalkMap/2.0',
             url],
            capture_output=True, text=True, timeout=8
        )
        data = json.loads(result.stdout)
        addr = data.get('address', {})
        # 排除纯海域 / 未知区域
        klass = addr.get('landuse', '') or addr.get('place', '')
        if not data.get('display_name'):
            return False, f"未知区域（{name}）"
        return True, None
    except Exception:
        return True, None  # 验证失败不阻塞，允许放行

# ── CLI ───────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(
    description='Citywalk Map Generator — 零成本生成真实 OSM 步行路线图',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=__doc__
)
parser.add_argument('title', nargs='?', help='路线标题')
parser.add_argument('waypoints', nargs='?', help='站点列表，格式: lat,lon,name,desc|...')
parser.add_argument('--output', '-o', default='/tmp/citywalk_map.html',
                    help='输出 HTML 路径（默认 /tmp/citywalk_map.html）')
parser.add_argument('--visit-time', '-t', type=int, default=30,
                    help='每站停留分钟数（默认 30）')
parser.add_argument('--no-tips', action='store_true',
                    help='隐藏实用贴士栏')
parser.add_argument('--lang', '-l', choices=['zh', 'en'], default='zh',
                    help='界面语言（默认 zh）')
parser.add_argument('--weather', '-w', action='store_true',
                    help='查询并显示目的地天气')
parser.add_argument('--validate', action='store_true',
                    help='用 Nominatim 验证坐标有效性')
parser.add_argument('--color', '-c', dest='color', default=None,
                    help='主题色（覆盖 COLOR 环境变量）')
parser.add_argument('--tile-url', default=None,
                    help='自定义地图 Tile URL，带 {z}/{x}/{y} 占位符（默认 OSM）')
parser.add_argument('--tile-attrib', default='© OpenStreetMap contributors',
                    help='Tile 版权信息（默认 © OpenStreetMap contributors）')

args = parser.parse_args()

# 读取环境变量作为默认值
ACCENT = args.color or os.environ.get('COLOR', '#e94560')

# ── Input parsing ─────────────────────────────────────────────────────────────

if not args.title or not args.waypoints:
    parser.print_help()
    sys.exit(1)

title = args.title
parts = args.waypoints.split('|')
waypoints = []
for i, p in enumerate(parts):
    s = p.split(',')
    if len(s) < 3:
        print(f"⚠️  站点 #{i+1} 格式错误（需 lat,lon,name[,desc]）: {p}", file=sys.stderr)
        sys.exit(1)
    lat, lon = float(s[0].strip()), float(s[1].strip())
    if args.validate:
        ok, err = validate_coords(lat, lon, s[2].strip())
        if not ok:
            print(f"⚠️  {err}", file=sys.stderr)
        else:
            print(f"  ✓ 坐标有效: {s[2].strip()} ({lat},{lon})")
    waypoints.append({
        'num': str(i + 1),
        'lat': lat,
        'lon': lon,
        'name': s[2].strip(),
        'desc': s[3].strip() if len(s) > 3 else ''
    })

clat = sum(w['lat'] for w in waypoints) / len(waypoints)
clon = sum(w['lon'] for w in waypoints) / len(waypoints)

# ── Weather ───────────────────────────────────────────────────────────────────

weather_info = None
if args.weather:
    dest = waypoints[-1]  # 用终点城市查天气
    print(f"正在查询天气: {dest['name']} ({dest['lat']},{dest['lon']})...")
    desc, temp, desc_str, emoji = get_weather(dest['lat'], dest['lon'], args.lang)
    if desc:
        weather_info = desc
        print(f"  天气: {desc}")

# ── Routing ───────────────────────────────────────────────────────────────────

print(f"正在查询 OSRM 步行路由 ({len(waypoints)} 个站点)...")
td, walk_sec, route_coords = get_osrm_route(waypoints)

visit_sec = len(waypoints) * args.visit_time * 60
total_sec = walk_sec + visit_sec

# ── Build HTML ────────────────────────────────────────────────────────────────

route_html_lines = []
for i, w in enumerate(waypoints):
    cls = 's1' if i == 0 else ('sN' if i == len(waypoints) - 1 else 'sx')
    route_html_lines.append(f'          <li><span class="route-num {cls}">{w["num"]}</span>{w["name"]}</li>')
route_html = '\n'.join(route_html_lines)

TIPS = {
    'zh': ['建议提前出发，合理安排时间', '穿着舒适的步行鞋', '携带水瓶和防晒用品', '注意安全，遵守当地规定'],
    'en': ['Start early and plan your time well', 'Wear comfortable walking shoes',
           'Bring water and sun protection', 'Stay safe and follow local rules'],
}
tips_list = [] if args.no_tips else TIPS.get(args.lang, TIPS['zh'])
if weather_info:
    tips_list.insert(0, f"📍 终点天气: {weather_info}")
tips_html = '\n'.join(f'          <li>{t}</li>' for t in tips_list)

stats_extra = ''
stats_col = 'repeat(4, 1fr)'

HTML = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  background: {accent};
  min-height: 100vh;
  padding: 16px 0;
  display: flex;
  align-items: flex-start;
}}
.card {{
  width: 100%;
  max-width: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}}
.header {{
  background: linear-gradient(135deg, {accent} 0%, {accent_dark} 100%);
  padding: 18px 20px 16px;
  color: white;
}}
.header .tag {{
  display: inline-block;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  padding: 4px 12px;
  font-size: 10px;
  letter-spacing: 1px;
  margin-bottom: 6px;
}}
.header h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 4px; }}
.header p {{ font-size: 13px; opacity: 0.85; }}
#map {{ width: 100%; height: 520px; }}
#map .tile-error {{ padding: 40px; text-align: center; color: #888; font-size: 14px; }}
.info {{ padding: 16px 18px; }}
.stats {{
  display: grid;
  grid-template-columns: {stats_col};
  gap: 10px;
  margin-bottom: 14px;
}}
.stat {{
  background: #f5f7fa;
  border-radius: 10px;
  padding: 10px 6px;
  text-align: center;
}}
.stat .num {{ font-size: 20px; font-weight: 700; color: {accent}; }}
.stat .label {{ font-size: 11px; color: #888; margin-top: 3px; }}
.bottom {{ display: flex; gap: 12px; }}
.bottom-left {{ flex: 1.5; background: #f5f7fa; border-radius: 12px; padding: 12px 14px; }}
.bottom-right {{ flex: 1; background: #f5f7fa; border-radius: 12px; padding: 12px 14px; }}
.section-title {{ font-size: 11px; color: #888; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; font-weight: 600; }}
.route-list {{ list-style: none; padding: 0; margin: 0; }}
.route-list li {{ display: flex; align-items: center; gap: 10px; padding: 7px 0; font-size: 13px; color: #333; border-bottom: 1px solid #eee; }}
.route-list li:last-child {{ border-bottom: none; }}
.route-num {{ width: 22px; height: 22px; border-radius: 50%; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; }}
.route-num.s1 {{ background: {accent}; }}
.route-num.sx {{ background: #ff9f43; }}
.route-num.sN {{ background: #10b981; }}
.tips {{ list-style: none; padding: 0; margin: 0; }}
.tips li {{ font-size: 12px; color: #333; line-height: 1.6; padding: 6px 0; border-bottom: 1px solid #eee; }}
.tips li:last-child {{ border-bottom: none; }}
.popup-title {{ font-size: 14px; font-weight: 700; color: #222; margin-bottom: 4px; }}
.popup-desc {{ font-size: 12px; color: #666; }}
.popup-num {{ display: inline-block; width: 20px; height: 20px; background: {accent}; color: white; border-radius: 50%; text-align: center; line-height: 20px; font-size: 10px; font-weight: 700; margin-right: 6px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="tag">🚶 CITYWALK</div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
  <div id="map"></div>
  <div class="info">
    <div class="stats">
      <div class="stat"><div class="num">{dist}</div><div class="label">{lbl_dist}</div></div>
      <div class="stat"><div class="num">{dur}</div><div class="label">{lbl_dur}</div></div>
      <div class="stat"><div class="num">{n}站</div><div class="label">{lbl_n}</div></div>
      <div class="stat"><div class="num">{walk}</div><div class="label">{lbl_walk}</div></div>
      {stats_extra}
    </div>
    <div class="bottom">
      <div class="bottom-left">
        <div class="section-title">{lbl_route}</div>
        <ul class="route-list">
{route_html}
        </ul>
      </div>
      <div class="bottom-right">
        <div class="section-title">{lbl_tips}</div>
        <ul class="tips">
{tips_html}
        </ul>
      </div>
    </div>
  </div>
</div>
<script>
var waypoints = {waypoints_json};
var routeCoords = {route_json};
var map = L.map('map', {{zoomControl:true, scrollWheelZoom:false}}).setView([{center_lat},{center_lon}], 14);

// 多源瓦片：优先 OSM，5秒内失败则切换高德（国内可访问）
var osmUrl = "https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png";
var gaodeUrl = "https://wprd01.is.autonavi.com/appmaptile?x={{x}}&y={{y}}&z={{z}}&lang=zh_cn&size=1&style=7";
var tileLayer = L.tileLayer(osmUrl, {{maxZoom:19, attribution:"© OpenStreetMap contributors", subdomains:'abc', errorTileUrl:'https://unpkg.com/leaflet@1.9.4/dist/images/tile_404.png'}});
var osmFailed = false;

tileLayer.on('tileerror', function(e) {{
  if (osmFailed) return;
  osmFailed = true;
  console.log('OSM tiles failed, switching to 高德...');
  map.removeLayer(tileLayer);
  var gaodeLayer = L.tileLayer(gaodeUrl, {{maxZoom:18, attribution:"© 高德地图 | © OpenStreetMap contributors"}});
  gaodeLayer.addTo(map);
}});

// 超时回退：OSM 5秒内没成功全部加载则切高德
var loadedCount = 0;
var requiredTiles = 6;
setTimeout(function() {{
  if (loadedCount < requiredTiles && !osmFailed) {{
    osmFailed = true;
    console.log('OSM loading slow, switching to 高德...');
    try {{ map.removeLayer(tileLayer); }} catch(e) {{}}
    var gaodeLayer = L.tileLayer(gaodeUrl, {{maxZoom:18, attribution:"© 高德地图 | © OpenStreetMap contributors"}});
    gaodeLayer.addTo(map);
  }}
}}, 5000);

// OSM 加载计数
map.eachLayer(function(l) {{
  if (l instanceof L.TileLayer) {{
    l.on('load', function() {{ loadedCount++; }});
  }}
}});

tileLayer.addTo(map);
L.polyline(routeCoords, {{color:'{accent}', weight:5, opacity:0.85, dashArray:'10, 5'}}).addTo(map);
var ds = Math.max(1, Math.floor(routeCoords.length/12));
for(var i=0;i<routeCoords.length-1;i+=ds){{
  L.circleMarker(routeCoords[i], {{radius:4, color:'{accent}', fillColor:'{accent}', fillOpacity:0.9}}).addTo(map);
}}
waypoints.forEach(function(wp){{
  var last = waypoints[waypoints.length-1].num;
  var color = wp.num==='1'?'{accent}':(wp.num===last?'#10b981':'#ff9f43');
  L.circleMarker([wp.lat,wp.lon], {{radius:10, color:'white', weight:3, fillColor:color, fillOpacity:1}})
    .addTo(map).bindPopup('<div class="popup-title"><span class="popup-num" style="background:'+color+'">'+wp.num+'</span>'+wp.name+'</div><div class="popup-desc">'+(wp.desc||'')+'</div>');
  var lbl = L.divIcon({{html:'<div style="background:white;padding:3px 8px;border-radius:8px;font-size:11px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.2);white-space:nowrap;border-left:3px solid '+color+';">'+wp.name+'</div>', className:'', iconSize:[0,0], iconAnchor:[0,0]}});
  L.marker([wp.lat,wp.lon], {{icon:lbl}}).addTo(map);
}});
var b = L.latLngBounds(waypoints.map(function(wp){{return[wp.lat,wp.lon];}}));
map.fitBounds(b, {{padding:[10,10]}});
var n=L.control({{position:'bottomleft'}});n.onAdd=function(){{
  var d=L.DomUtil.create('div');
  d.innerHTML='<div style="background:white;padding:6px 8px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.2);text-align:center;font-size:10px;font-weight:700;color:#333;">⬆ N</div>';
  return d;
}};n.addTo(map);
</script>
</body>
</html>
"""

LANG_STRINGS = {
    'zh': dict(lbl_dist='步行距离', lbl_dur='游览时长', lbl_n='途经景点', lbl_walk='纯步行',
               lbl_route='途经景点', lbl_tips='实用贴士'),
    'en': dict(lbl_dist='Distance', lbl_dur='Total Time', lbl_n='Stops', lbl_walk='Walking',
               lbl_route='Route', lbl_tips='Tips'),
}

lang_str = LANG_STRINGS.get(args.lang, LANG_STRINGS['zh'])
total_dur_str = fmt_t(total_sec)
walk_str = fmt_t(walk_sec)
subtitle_parts = [f"{len(waypoints)}{lang_str['lbl_n']}", f"全程{fmt_d(td)}", f"{'约' if args.lang=='zh' else '~'}{total_dur_str}"]
if weather_info:
    subtitle_parts.append(weather_info)
subtitle = ' · '.join(subtitle_parts)

html = HTML.format(
    lang='zh-CN' if args.lang == 'zh' else 'en',
    title=title,
    subtitle=subtitle,
    accent=ACCENT,
    accent_dark=darken(ACCENT),
    waypoints_json=json.dumps(waypoints),
    route_json=json.dumps(route_coords),
    center_lat=clat,
    center_lon=clon,
    dist=fmt_d(td),
    dur=total_dur_str,
    n=len(waypoints),
    walk=walk_str,
    route_html=route_html,
    tips_html=tips_html,
    stats_col=stats_col,
    stats_extra=stats_extra,
    tile_url=args.tile_url or 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    tile_attrib=args.tile_attrib.replace("'", "\\'"),
    **lang_str,
)

with open(args.output, 'w', encoding='utf-8') as f:
    f.write(html)

ok_str = 'OK' if args.lang == 'en' else '完成'
print(f"{ok_str}: {title} | {ACCENT} | {len(waypoints)} pts | {fmt_d(td)} | {fmt_t(walk_sec)} walk | {total_dur_str} total")
print(f"输出: {args.output}")
