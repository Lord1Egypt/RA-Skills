"""
快递状态全量报告脚本
用法: python report.py
查询所有追踪中的快递最新状态，生成详细日报
配合 cron 定时推送: 每天 8:00 / 12:00 / 18:00
"""
import sys, json, os, re
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track import query_express, load_packages, save_packages

def status_emoji(status):
    m = {"已签收": "✅", "待揽收": "⏳", "已揽收": "📦",
         "运输中": "🚚", "派送中": "🏃", "疑难": "⚠️", "退回": "↩️"}
    return m.get(status, "📦")

def extract_cities(traces):
    """同 map.py 的城市提取逻辑"""
    cities = []
    for trace in traces:
        ctx = trace.get("context", "")
        for m in re.findall(r'省([\u4e00-\u9fa5a-zA-Z]{2,3})市', ctx):
            if m not in cities: cities.append(m)
    if not cities:
        for trace in traces:
            ctx = trace.get("context", "")
            for m in re.findall(r'([\u4e00-\u9fa5a-zA-Z]{2})市', ctx):
                if m not in cities: cities.append(m)
    return cities

def map_url(tn, traces):
    """生成地图链接"""
    cities = extract_cities(traces)
    if len(cities) >= 2:
        return f"https://ditu.amap.com/dir?from={cities[0]}&to={cities[-1]}"
    elif cities:
        return f"https://www.amap.com/search?query={cities[0]}"
    else:
        return f"https://m.kuaidi100.com/index_all.html?type=auto&postid={tn}"

def generate_report():
    data = load_packages()
    packages = data["packages"]
    
    if not packages:
        print("📭 暂无快递追踪记录\n\n💡 发单号给我查询 | 转发快递短信自动追踪")
        return
    
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d %H:%M")
    hour = now.hour
    period = "☀️ 早上好" if hour < 10 else ("🌤️ 中午好" if hour < 14 else "🌙 下午好")
    
    # 刷新所有快递状态
    status_changes = []
    for pkg in packages:
        tn = pkg["tracking_number"]
        old_status = pkg.get("last_status", "")
        result = query_express(tn)
        
        if "error" not in result:
            pkg["last_status"] = result["status"]
            pkg["last_update"] = datetime.now().isoformat()
            pkg["traces"] = result.get("traces", [])
            pkg["delivered"] = result.get("delivered", False)
            pkg["courier_code"] = result.get("courier_code", pkg.get("courier_code"))
            pkg["courier_name"] = result.get("courier", pkg.get("courier_name"))
            
            if old_status and old_status != result["status"]:
                status_changes.append((pkg, old_status, result["status"]))
    
    save_packages(data)
    
    in_transit = [p for p in packages if not p.get("delivered")]
    delivered = [p for p in packages if p.get("delivered")]
    total = len(packages)
    
    lines = []
    lines.append(f"{period}！📦 快递追踪日报")
    lines.append(f"🕐 {today_str}")
    lines.append("")
    lines.append("━" * 25)
    lines.append(f"📊 {total} 个快递 | 🚚 在途 {len(in_transit)} | ✅ 签收 {len(delivered)}")
    lines.append("━" * 25)
    lines.append("")
    
    # 状态变更提醒
    if status_changes:
        for pkg, old, new in status_changes:
            emoji = status_emoji(new)
            label = f" [{pkg.get('label')}]" if pkg.get("label") else ""
            lines.append(f"🔔 **{pkg['courier_name']}**{label} `{pkg['tracking_number'][:6]}..`")
            lines.append(f"   {old} → {new}")
        lines.append("")
    
    # 在途快递
    if in_transit:
        lines.append("🚚 在途快递\n")
        for i, pkg in enumerate(in_transit, 1):
            courier = pkg.get("courier_name", "")
            tn = pkg["tracking_number"]
            status = pkg.get("last_status", "")
            emoji = status_emoji(status)
            label = f" [{pkg['label']}]" if pkg.get("label") else ""
            
            lines.append(f"{emoji} **{i}. {courier}**{label}")
            lines.append(f"   单号: `{tn}`  状态: {status}")
            
            traces = pkg.get("traces", [])
            if traces:
                # 只显示最新 3 条轨迹（日报要精简）
                for trace in traces[:3]:
                    t = trace.get("time", trace.get("ftime", "?"))
                    c = trace.get("context", "")
                    lines.append(f"   {t}  {c[:60]}")
            else:
                lines.append(f"   💡 待揽收")
            
            lines.append(f"   🗺️ {map_url(tn, traces)}")
            lines.append("")
    else:
        lines.append("🎉 全部快递已签收！\n")
    
    # 已签收
    if delivered:
        lines.append("✅ 已签收\n")
        for i, pkg in enumerate(reversed(delivered[-5:]), 1):
            courier = pkg.get("courier_name", "")
            tn = pkg["tracking_number"]
            traces = pkg.get("traces", [])
            sign_time = traces[0].get("time", "") if traces else pkg.get("last_update", "")[:16]
            lines.append(f"   {i}. **{courier}** `{tn}` {sign_time}")
        lines.append("")
    
    lines.append("━" * 25)
    lines.append("发单号查物流 | 快递地图 | 转发短信自动追踪")
    
    print("\n".join(lines))

def main():
    generate_report()

if __name__ == "__main__":
    main()
