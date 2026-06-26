"""
快递地图追踪 - 高德地图版
用法: python map.py [单号]
"""
import sys, json, os, re

DATA_DIR = "G:/PC先生/express_data"
PACKAGES_FILE = os.path.join(DATA_DIR, "packages.json")

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def load_packages():
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"packages": []}

def extract_cities(traces):
    cities = []
    for trace in traces:
        ctx = trace.get("context", "")
        # 优先: 省XX市
        for m in re.findall(r'省([\u4e00-\u9fa5a-zA-Z]{2,3})市', ctx):
            if m not in cities: cities.append(m)
    if not cities:
        for trace in traces:
            ctx = trace.get("context", "")
            # 回退: XX市 (2字城市)
            for m in re.findall(r'([\u4e00-\u9fa5a-zA-Z]{2})市', ctx):
                if m not in cities: cities.append(m)
    return cities

def map_url(tracking_number, traces):
    cities = extract_cities(traces)
    if len(cities) >= 2:
        return f"https://ditu.amap.com/dir?from={cities[0]}&to={cities[-1]}"
    elif cities:
        return f"https://www.amap.com/search?query={cities[0]}"
    else:
        return f"https://m.kuaidi100.com/index_all.html?type=auto&postid={tracking_number}"

def main():
    data = load_packages()
    packages = data.get("packages", [])

    if len(sys.argv) > 1:
        tn = sys.argv[1].strip()
        for p in packages:
            if p["tracking_number"] == tn:
                cities = extract_cities(p.get("traces", []))
                print(f"{p.get('courier_name','')} {tn}")
                if len(cities) >= 2:
                    print(f"  {cities[0]} -> {cities[-1]}")
                elif cities:
                    print(f"  {cities[0]}")
                print(f"  {map_url(tn, p.get('traces',[]))}")
                return
        print(f"Not found: {tn}")
        return

    if not packages:
        print("No packages")
        return

    for i, pkg in enumerate(packages, 1):
        if pkg.get("delivered"): continue
        courier = pkg.get("courier_name", "")
        tn = pkg["tracking_number"]
        cities = extract_cities(pkg.get("traces", []))
        label = f" [{pkg['label']}]" if pkg.get("label") else ""
        
        print(f"  {i}. {courier} {tn}{label}")
        if len(cities) >= 2:
            print(f"     {cities[0]} -> {cities[-1]}")
        elif cities:
            print(f"     {cities[0]}")
        print(f"     {map_url(tn, pkg.get('traces',[]))}")
        print("")

if __name__ == "__main__":
    main()
