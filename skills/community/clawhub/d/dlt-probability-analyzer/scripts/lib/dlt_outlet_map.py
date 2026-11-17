# -*- coding: utf-8 -*-
"""
大乐透网点雷达 (Outlet Radar)
=============================

定位 (务必读):
    本工具帮彩民"就近购彩"——给出所在城市、一键打开地图搜最近的体彩网点
    (距离/导航由地图APP提供)、以及一个可自己维护的"网点台账"(含中奖情况备注)。

它【不能】做的事 (诚实声明):
    - 不采集你的精确住址/GPS。定位只到"城市级", 且默认需你手动确认或显式授权。
    - 不内置实时门店数据库。真实的"最近网点+距离+导航"交给高德/百度地图APP
      (点击生成的链接即可, 由APP基于你的实时位置排序)。
    - "某网点中奖情况"属公开传闻/锦上添花, **不影响你任一注的中奖概率**。
      网点中不中、中多大多独立事件, 选网点≠选号, 选旺铺不提高头奖概率。

数据源稳定性兜底:
    - 城市地理用内置"主要城市坐标表"(离线可用); 联网时可用 ipapi.co 自动识别城市
      (带超时与失败兜底, 失败则回退到用户手动输入/默认城市)。
    - 任何外部请求失败都不阻断报告生成, 仅降级为"请手动输入城市"。

用法:
    python3 dlt_outlet_map.py --auto          # 尝试自动识别城市
    python3 dlt_outlet_map.py --city 杭州     # 指定城市
    python3 dlt_outlet_map.py --city 杭州 --out radar
"""
from __future__ import annotations
import argparse
import json
import urllib.request
import urllib.parse
from datetime import datetime

try:
    import ssl
    _CTX = ssl.create_default_context()
    _CTX.check_hostname = False
    _CTX.verify_mode = ssl.CERT_NONE
except Exception:
    _CTX = None

# 主要城市坐标表 (城市级, 仅用于生成地图搜索链接与距离估算的锚点; 非精确门店位置)
CITY_COORDS = {
    "北京": (39.9042, 116.4074), "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644), "深圳": (22.5431, 114.0579),
    "杭州": (30.2741, 120.1551), "南京": (32.0603, 118.7969),
    "成都": (30.5728, 104.0668), "武汉": (30.5928, 114.3055),
    "西安": (34.3416, 108.9398), "重庆": (29.5630, 106.5516),
    "苏州": (31.2989, 120.5853), "天津": (39.3434, 117.3616),
    "长沙": (28.2282, 112.9388), "郑州": (34.7466, 113.6254),
    "青岛": (36.0671, 120.3826), "沈阳": (41.8057, 123.4315),
    "大连": (38.9140, 121.6147), "厦门": (24.4798, 118.0894),
    "福州": (26.0745, 119.2965), "济南": (36.6512, 117.1201),
    "合肥": (31.8206, 117.2272), "昆明": (24.8801, 102.8329),
    "哈尔滨": (45.8038, 126.5349), "长春": (43.8171, 125.3235),
    "石家庄": (38.0428, 114.5149), "太原": (37.8706, 112.5489),
    "南昌": (28.6829, 115.8579), "南宁": (22.8170, 108.3665),
    "贵阳": (26.6470, 106.6302), "兰州": (36.0611, 103.8343),
    "海口": (20.0444, 110.1990), "宁波": (29.8683, 121.5440),
    "温州": (27.9938, 120.6994), "东莞": (23.0210, 113.7518),
    "佛山": (23.0218, 113.1219), "无锡": (31.4912, 120.3119),
}

DEFAULT_CITY = "杭州"


def detect_city_via_ip(timeout: float = 3.0):
    """尝试用 ipapi.co 自动识别城市。失败/超时返回 None (不阻断)。"""
    try:
        req = urllib.request.Request(
            "https://ipapi.co/json/",
            headers={"User-Agent": "Mozilla/5.0 (compatible; dlt-outlet-radar/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
            data = json.loads(r.read().decode("utf-8", "ignore"))
        city = (data.get("city") or "").strip()
        if city and ("市" in city or city in CITY_COORDS):
            return city.replace("市", "")
    except Exception:
        return None
    return None


def normalize_city(name: str) -> str:
    """把用户输入规范成表内城市名 (容错: 去'市'、匹配前缀)。"""
    if not name:
        return ""
    s = name.strip().replace("市", "")
    if s in CITY_COORDS:
        return s
    for k in CITY_COORDS:
        if k.startswith(s) or s in k:
            return k
    return s  # 未知城市也原样返回, 地图搜索仍可工作


def build_map_links(city: str) -> dict:
    """生成地图搜索链接 (由地图APP提供真实最近网点/距离/导航)。"""
    kw = urllib.parse.quote("体育彩票")
    c = urllib.parse.quote(city)
    return {
        "amap_web": f"https://www.amap.com/search?query={kw}&city={c}",
        "amap_uri": f"https://uri.amap.com/search?keyword={kw}&city={c}&src=dlt_radar",
        "baidu": f"https://map.baidu.com/search/{kw}/?city={c}",
    }


def generate_radar(city: str, auto_city: str = None) -> dict:
    """生成网点雷达数据。

    返回 dict: {city, coords, map_links, generated_at, note, ledger_template}
    """
    norm = normalize_city(city) or normalize_city(auto_city or "") or DEFAULT_CITY
    coords = CITY_COORDS.get(norm)
    links = build_map_links(norm)
    meta = {
        "city": norm,
        "coords": list(coords) if coords else None,
        "map_links": links,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "auto_detected": bool(auto_city) and norm == normalize_city(auto_city or ""),
        "note": (
            "本雷达仅到城市级, 不采集精确位置。点击上方地图链接后, "
            "由高德/百度地图APP基于你的实时定位显示最近体彩网点、距离与导航。"
            "'网点中奖情况'为公开传闻/娱乐参考, 不影响你任一注的中奖概率。"
        ),
        # 可填写的网点台账模板 (用户自己维护; 系统不预置实时门店数据)
        "ledger_template": [
            {"name": "（自行填写，如：XX路体彩店）", "address": "", "distance_km": "",
             "win_note": "（可选：该店历史中奖传闻，仅供娱乐参考）"},
        ],
    }
    return meta


def render_radar_html(meta) -> str:
    """渲染为可嵌入报告的 HTML 片段 (复用 dlt_auto 报告 CSS 类)。"""
    L = []
    L.append('<div class="section">')
    L.append('<div class="section-title">网点雷达（就近购彩 · 城市级定位）</div>')
    L.append('<div class="info" style="border-color:#00dd88;">')
    L.append('<p style="color:#88ccff; font-size:14px; line-height:1.8;">')
    L.append(f'📍 当前城市：<strong>{meta["city"]}</strong>'
             f'{"（自动识别）" if meta.get("auto_detected") else "（手动指定）"}。')
    if meta["coords"]:
        L.append(f' 城市锚点坐标约 ({meta["coords"][0]:.3f}, {meta["coords"][1]:.3f})。')
    L.append('<br>点击下方链接，地图APP会基于你的实时位置显示<strong>最近的体彩网点、距离与导航</strong>：')
    L.append('</p>')
    L.append('<p style="font-size:14px; line-height:2;">')
    L.append(f'🔗 <a href="{meta["map_links"]["amap_uri"]}" target="_blank" '
             f'style="color:#88ccff;">高德地图·搜体彩网点</a>　')
    L.append(f'🔗 <a href="{meta["map_links"]["baidu"]}" target="_blank" '
             f'style="color:#88ccff;">百度地图·搜体彩网点</a>')
    L.append('</p></div>')

    # 网点台账 (可填写)
    L.append('<div class="group-card"><h3>我的网点台账（可自行补充）</h3>')
    L.append('<div style="font-size:13px; line-height:1.95; color:#cdd6f4;">')
    L.append('· 网点名：%s　地址：%s　距你：%s km　中奖情况：%s<br>' % (
        meta["ledger_template"][0]["name"],
        meta["ledger_template"][0]["address"] or "（填地址）",
        meta["ledger_template"][0]["distance_km"] or "（地图测距）",
        meta["ledger_template"][0]["win_note"]))
    L.append('</div></div>')

    L.append('<div class="warning"><h3>⚠️ 诚实声明（关于网点雷达）</h3>')
    L.append(
        '<p>本工具<strong>不采集你的精确住址/GPS</strong>，定位仅到城市级。'
        '真实"最近网点+距离+导航"由地图APP提供，系统不内置实时门店数据库。'
        '<strong>"某网点中奖情况"属公开传闻、仅供娱乐参考，不影响你任一注的中奖概率</strong>'
        '——选旺铺不等于选号，网点中不中与你手中的号码无关。彩票期望收益为负，请当娱乐、设预算上限。</p></div>')
    L.append('</div>')
    return "\n".join(L)


def render_radar_md(meta) -> str:
    L = []
    L.append(f"# 大乐透网点雷达（{meta['city']}）\n")
    L.append(f"> 生成时间：{meta['generated_at']}　"
             f"{'（自动识别）' if meta.get('auto_detected') else '（手动指定）'}\n")
    L.append("## 一键搜最近网点（距离/导航由地图APP提供）\n")
    L.append(f"- 高德：{meta['map_links']['amap_uri']}")
    L.append(f"- 百度：{meta['map_links']['baidu']}\n")
    L.append("## 我的网点台账（可自行补充）\n")
    L.append("- 网点名：（自行填写）　地址：（填地址）　距你：（地图测距）km　"
             "中奖情况：（可选，仅供娱乐参考）\n")
    L.append("## 诚实声明\n")
    L.append("- 本工具不采集精确位置，仅城市级。真实最近网点+距离+导航由地图APP提供。")
    L.append("- '网点中奖情况'属传闻、不影响中奖概率，选旺铺≠选号。彩票期望为负，请当娱乐、设预算。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="大乐透网点雷达 (城市级, 非精确定位)")
    ap.add_argument("--auto", action="store_true", help="尝试用IP自动识别城市")
    ap.add_argument("--city", type=str, default="", help="指定城市, 如 杭州")
    ap.add_argument("--out", type=str, default="dlt_outlet_radar", help="输出文件前缀")
    args = ap.parse_args()

    auto_city = detect_city_via_ip() if args.auto else None
    if args.auto and auto_city:
        print(f"🌐 自动识别城市: {auto_city}")
    meta = generate_radar(args.city, auto_city)

    md = render_radar_md(meta)
    with open(args.out + ".md", "w", encoding="utf-8") as f:
        f.write(md)
    with open(args.out + ".json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"✅ 网点雷达已生成: 城市={meta['city']} "
          f" coords={meta['coords']} 自动={meta.get('auto_detected')}")
    print(f"   高德: {meta['map_links']['amap_uri']}")
    print(f"   输出: {args.out}.md / {args.out}.json")


if __name__ == "__main__":
    main()
