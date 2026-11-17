# 📊 模块 1：数据换算

---

#### 1.1 房贷计算器

**✅ 开箱即用** ｜ 🌐 [在线房贷计算器](https://www.zhujisuanqi.com/)

<details>
<summary>📋 展开查看命令</summary>

```python
import math
try:
    P = float(input("贷款总额(万元): ") or 100) * 10000
    n = int(float(input("贷款年限: ") or 30) * 12)
    r = float(input("年利率(%): ") or 4.2) / 100 / 12
    method = input("方式(等额本息/等额本金): ").strip() or "等额本息"
    if n <= 0:
        print("❌ 贷款年限必须大于0")
    elif r <= 0:
        print("❌ 年利率必须大于0")
    elif method == "等额本息":
        m = P*r*(1+r)**n / ((1+r)**n-1)
        total = m * n
        print(f"月供: {m:.2f}元 | 总利息: {total-P:.2f}元 | 还款总额: {total:.2f}元")
    else:
        tot = sum(P/n + (P-P*i/n)*r for i in range(n))
        print(f"首月: {P/n+P*r:.2f}元 | 末月: {P/n+r*(P/n):.2f}元 | 总利息: {tot-P:.2f}元")
except ValueError:
    print("❌ 输入错误：请输入有效数字。例如：贷款100万输 100，年限30年输 30")
```

</details>

---

#### 1.2 五险一金计算器 ⭐ v4.0.0 查表累进引擎

**✅ 开箱即用** ｜ 🌐 [个税计算器](https://www.taxcalculator.com)

> v4.0 重写计算引擎：数据与引擎分离，读取 `references/tax_2026.yaml` 数据驱动计算。支持 13 个城市，查表确定基数上下限，7 级超额累进个税。

<details>
<summary>📋 五险一金 + 个税计算器（查表 + 分段累进）</summary>

```python
import os, yaml, math

def calc_insurance_tax(salary, city_code="beijing"):
    """读取 tax_2026.yaml，查表+分段累进计算五险一金和个税"""
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "references", "tax_2026.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    meta = data.get("meta", {})
    bases = data.get("social_insurance_bases", {})
    rates = data.get("insurance_rates", {})
    overrides = rates.get("overrides", {})
    tax_brackets = data.get("individual_income_tax", {}).get("brackets", [])
    monthly_threshold = data.get("individual_income_tax", {}).get("monthly_threshold", 5000)
    
    if city_code not in bases:
        city_name = city_code
        supported = [f"{v.get('name', k)} ({k})" for k, v in bases.items()]
        return None, f"❌ 不支持的城市: {city_name}。支持: {', '.join(supported)}"
    
    city_data = bases[city_code]
    city_name = city_data.get("name", city_code)
    
    city_overrides = overrides.get(city_code, {})
    personal_rates = {**rates.get("default", {}).get("personal", {}), **city_overrides.get("personal", {})}
    company_rates = {**rates.get("default", {}).get("company", {}), **city_overrides.get("company", {})}
    
    def get_base(insurance_type):
        base_info = city_data.get(insurance_type, {})
        lower = base_info.get("lower", 0)
        upper = base_info.get("upper", float("inf"))
        return max(lower, min(salary, upper))
    
    personal_items = {}
    personal_total = 0
    for insurance_type in ["pension", "medical", "unemployed", "injury", "maternity"]:
        base = get_base(insurance_type)
        rate = personal_rates.get(insurance_type, 0)
        amount = base * rate
        if amount > 0:
            names = {"pension": "养老", "medical": "医疗", "unemployed": "失业", "injury": "工伤", "maternity": "生育"}
            personal_items[names.get(insurance_type, insurance_type)] = round(amount, 2)
        personal_total += amount
    
    hf_base = get_base("housing_fund")
    hf_rate = personal_rates.get("housing_fund", 0.12)
    hf_amount = hf_base * hf_rate
    personal_items["公积金"] = round(hf_amount, 2)
    personal_total += hf_amount
    
    taxable_income = max(0, salary - personal_total - monthly_threshold)
    
    tax = 0
    tax_detail = None
    for bracket in tax_brackets:
        if taxable_income <= 0:
            break
        taxable_at_bracket = min(taxable_income, bracket["limit"])
        tax += taxable_at_bracket * bracket["rate"]
        taxable_income -= taxable_at_bracket
        if taxable_at_bracket > 0:
            tax_detail = f"{bracket['rate']*100:.0f}%"
    
    net_salary = salary - personal_total - tax
    
    company_total = 0
    for insurance_type in ["pension", "medical", "unemployed", "injury", "maternity"]:
        base = get_base(insurance_type)
        rate = company_rates.get(insurance_type, 0)
        company_total += base * rate
    company_total += hf_base * company_rates.get("housing_fund", 0.12)
    
    return {
        "city": city_name,
        "data_version": meta.get("version", "unknown"),
        "data_effective": meta.get("effective_date", "unknown"),
        "salary": salary,
        "personal_insurance": personal_items,
        "personal_total": round(personal_total, 2),
        "housing_fund_employee": round(hf_amount, 2),
        "housing_fund_employer": round(hf_base * company_rates.get("housing_fund", 0.12), 2),
        "tax": round(tax, 2),
        "tax_rate_used": tax_detail,
        "net_salary": round(net_salary, 2),
        "company_total": round(company_total, 2),
    }, None

CITY_MAP = {
    "北京": "beijing", "上海": "shanghai", "广州": "guangzhou", "深圳": "shenzhen",
    "杭州": "hangzhou", "成都": "chengdu", "南京": "nanjing", "武汉": "wuhan",
    "西安": "xian", "重庆": "chongqing", "天津": "tianjin", "苏州": "suzhou",
    "郑州": "zhengzhou", "长沙": "changsha"
}

try:
    s = float(input("税前月薪: ") or 15000)
    city_input = input("城市(北京/上海/广州/深圳/杭州/成都/南京/武汉/西安/重庆/天津/苏州/郑州/长沙): ").strip() or "北京"
    
    if s <= 0:
        print("❌ 月薪必须大于0")
    else:
        city_code = CITY_MAP.get(city_input, city_input.lower())
        result, err = calc_insurance_tax(s, city_code)
        if err:
            print(err)
        else:
            print(f"=== {result['city']} 五险一金计算明细 (数据版本: {result['data_version']}, 生效: {result['data_effective']}) ===")
            print(f"税前月薪: ¥{result['salary']:,.2f}")
            print(f"\n--- 个人缴纳 ---")
            for name, amount in result["personal_insurance"].items():
                if name == "公积金":
                    print(f"  {name}: ¥{amount:,.2f} (单位另缴 ¥{result['housing_fund_employer']:,.2f})")
                else:
                    print(f"  {name}: ¥{amount:,.2f}")
            print(f"  个人社保合计: ¥{result['personal_total']:,.2f}")
            print(f"\n--- 个税 ---")
            print(f"  应缴个税: ¥{result['tax']:,.2f}")
            print(f"\n实发工资: ¥{result['net_salary']:,.2f}")
            print(f"  (相当于税前 {result['net_salary']/result['salary']*100:.1f}%)")
            print(f"\n--- 单位缴纳（供参考）---")
            print(f"  单位社保公积金合计: ¥{result['company_total']:,.2f}")
except ValueError:
    print("❌ 输入错误：月薪请输入纯数字。例如：15000")
except Exception as e:
    print(f"❌ 计算失败: {e}")
```

</details>

---

#### 1.2.1 个税计算器（单独查询）

**✅ 开箱即用**

<details>
<summary>📋 个税计算器</summary>

```python
import os, yaml

def calc_personal_tax_only(salary, social_insurance_deduction=0, special_deduction=0):
    """单独计算个税（7级超额累进）"""
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "references", "tax_2026.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    monthly_threshold = data.get("individual_income_tax", {}).get("monthly_threshold", 5000)
    tax_brackets = data.get("individual_income_tax", {}).get("brackets", [])
    
    taxable_income = max(0, salary - social_insurance_deduction - special_deduction - monthly_threshold)
    tax = 0
    bracket_used = "0%"
    for bracket in tax_brackets:
        if taxable_income <= 0:
            break
        taxable_at_bracket = min(taxable_income, bracket["limit"])
        tax += taxable_at_bracket * bracket["rate"]
        taxable_income -= taxable_at_bracket
        if taxable_at_bracket > 0:
            bracket_used = f"{bracket['rate']*100:.0f}%"
    
    return round(tax, 2), bracket_used

try:
    s = float(input("税前月薪: ") or 20000)
    ins = float(input("社保公积金扣除(默认0): ") or 0)
    special = float(input("专项附加扣除(默认0): ") or 0)
    
    if s <= 0:
        print("❌ 月薪必须大于0")
    else:
        tax, bracket = calc_personal_tax_only(s, ins, special)
        net = s - ins - tax
        print(f"应纳税: ¥{tax:,.2f} (适用 {bracket} 税率)")
        print(f"税后工资: ¥{net:,.2f}")
except ValueError:
    print("❌ 请输入数字")
```

</details>

---

#### 1.3 日期计算器

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
from datetime import date
try:
    a = date.today()
    b = input("目标日期 YYYY-MM-DD: ").strip() or "2026-10-01"
    y,m,d = map(int, b.split("-"))
    target = date(y,m,d)
    diff = (target - a).days
    print(f"相差: {diff} 天 ({diff//7} 周)")
    if diff < 0:
        print("⚠️ 目标日期已经过去了")
except ValueError:
    print("❌ 日期格式错误。正确格式：年-月-日，例如：2026-10-01")
```

</details>

---

#### 1.4 单位换算器

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
c = {
    # 长度
    "km_mi":  (lambda v: v*0.621371,  "公里", "英里"),
    "mi_km":  (lambda v: v/0.621371,  "英里", "公里"),
    "m_ft":   (lambda v: v*3.28084,   "米",   "英尺"),
    "ft_m":   (lambda v: v/3.28084,   "英尺", "米"),
    "cm_in":  (lambda v: v/2.54,      "厘米", "英寸"),
    "in_cm":  (lambda v: v*2.54,      "英寸", "厘米"),
    # 重量
    "kg_lb":  (lambda v: v*2.20462,   "公斤", "磅"),
    "lb_kg":  (lambda v: v/2.20462,   "磅",   "公斤"),
    "g_oz":   (lambda v: v/28.3495,   "克",   "盎司"),
    "oz_g":   (lambda v: v*28.3495,   "盎司", "克"),
    # 温度
    "c_f":    (lambda v: v*9/5+32,    "°C",   "°F"),
    "f_c":    (lambda v: (v-32)*5/9,  "°F",   "°C"),
    "c_k":    (lambda v: v+273.15,    "°C",   "K"),
    "k_c":    (lambda v: v-273.15,    "K",    "°C"),
    # 面积
    "sqm_sqft": (lambda v: v*10.7639, "平方米", "平方英尺"),
    "mu_sqm":   (lambda v: v*666.667, "亩",     "平方米"),
    "ha_mu":    (lambda v: v*15,       "公顷",   "亩"),
    # 速度
    "kmh_mph":  (lambda v: v*0.621371, "km/h",  "mph"),
    "ms_kmh":   (lambda v: v*3.6,      "m/s",   "km/h"),
    "knot_kmh": (lambda v: v*1.852,    "节",    "km/h"),
    # 数据存储
    "mb_gb":  (lambda v: v/1024,       "MB",   "GB"),
    "gb_mb":  (lambda v: v*1024,       "GB",   "MB"),
    "gb_tb":  (lambda v: v/1024,       "GB",   "TB"),
    "byte_mb":(lambda v: v/1048576,    "字节", "MB"),
    # 压力
    "bar_psi":(lambda v: v*14.5038,    "bar",  "psi"),
    "atm_kpa":(lambda v: v*101.325,    "atm",  "kPa"),
    # 能量
    "kcal_kj":(lambda v: v*4.184,      "千卡", "千焦"),
    "kwh_kj": (lambda v: v*3600,       "度电", "千焦"),
}
try:
    m = input("类型(如km_mi/mb_gb/mu_sqm):").strip() or "km_mi"
    v = float(input("数值: ") or 100)
    if m not in c:
        print(f"❌ 不支持的换算：'{m}'")
        print(f"支持的类型：{', '.join(c.keys())}")
    else:
        r, uf, ut = c[m]
        print(f"✅ {v} {uf} = {r(v):.4f} {ut}")
except ValueError:
    print("❌ 请输入纯数字，例如：100")
```

</details>

---

#### 1.5 汇率查询 ⭐ v4.0.0 时效治理

**✅ 开箱即用**（零依赖：内置常见汇率缓存 + 联网实时查询可选）

> v4.0 时效治理：缓存条目带抓取时间戳，超 72 小时标注陈旧 + 警示横幅。在线刷新失败保留旧值 + 陈旧标注，绝不静默用旧值冒充新值。

<details>
<summary>📋 汇率查询（时效感知版）</summary>

```python
import urllib.request, json, os, time
from datetime import datetime, timedelta

CACHE = {
    "USD": 1.0, "CNY": 7.24, "EUR": 0.92, "GBP": 0.79, "JPY": 157.35, "KRW": 1385.0,
    "HKD": 7.81, "TWD": 32.37, "SGD": 1.34, "AUD": 1.53, "CAD": 1.37, "CHF": 0.89,
    "INR": 83.45, "RUB": 91.5, "THB": 36.2, "VND": 25100, "MYR": 4.72, "PHP": 58.6,
    "IDR": 16250, "BRL": 5.43, "MXN": 17.15, "ZAR": 18.75, "AED": 3.67, "SAR": 3.75,
    "NZD": 1.65, "SEK": 10.6, "NOK": 10.9, "DKK": 6.88, "PLN": 4.05, "TRY": 32.8,
    "UAH": 40.5, "EGP": 48.5
}

CACHE_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_exchange_cache.json")
TTL_HOURS = 72

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def is_stale(timestamp_str):
    try:
        ts = datetime.fromisoformat(timestamp_str)
        return datetime.now() - ts > timedelta(hours=TTL_HOURS)
    except (ValueError, TypeError):
        return True

def get_cached_rate(cur):
    cache = load_cache()
    entry = cache.get(cur)
    if entry:
        rate = entry.get("rate")
        ts = entry.get("timestamp")
        if rate and ts:
            stale = is_stale(ts)
            return rate, ts, stale
    return None, None, False

def fetch_live_rate(fr, to):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{fr}"
        req = urllib.request.Request(url, headers={"User-Agent": "dgngjx/4.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=6).read())
        if "rates" in data and to in data["rates"]:
            rate = data["rates"][to]
            cache = load_cache()
            cache[to] = {"rate": rate, "timestamp": datetime.now().isoformat(), "base": fr}
            cache[fr] = {"rate": 1.0, "timestamp": datetime.now().isoformat(), "base": fr}
            save_cache(cache)
            return rate, True
    except Exception:
        pass
    return None, False

def convert_currency(amt, fr, to):
    fr = fr.upper()
    to = to.upper()
    rate, live = fetch_live_rate(fr, to)
    if live:
        return rate, "实时汇率", False, None
    if fr == to:
        return 1.0, "同币种", False, None
    fr_rate, fr_ts, fr_stale = get_cached_rate(fr)
    to_rate, to_ts, to_stale = get_cached_rate(to)
    if fr_rate and to_rate:
        cross_rate = to_rate / fr_rate
        stale = fr_stale or to_stale
        older_ts = min(fr_ts, to_ts) if fr_ts and to_ts else (fr_ts or to_ts)
        days_old = (datetime.now() - datetime.fromisoformat(older_ts)).days if older_ts else "?"
        tag = f"缓存汇率({days_old}天前)"
        return cross_rate, tag, stale, older_ts
    if fr in CACHE and to in CACHE:
        cross_rate = CACHE[to] / CACHE[fr]
        return cross_rate, "静态缓存(离线)", True, None
    return None, None, False, None

s = input("输入(如 100 USD CNY，或回车查汇率表):").strip()
if not s:
    print("=== 常见货币汇率 (1 USD 基准) ===")
    cache = load_cache()
    for cur, rate in sorted(CACHE.items()):
        cached_rate, ts, stale = get_cached_rate(cur)
        if cached_rate and not stale:
            print(f"  1 USD = {cached_rate:>10.2f} {cur}  (实时)")
        elif cached_rate:
            days = (datetime.now() - datetime.fromisoformat(ts)).days
            print(f"  1 USD = {cached_rate:>10.2f} {cur}  ({days}天前)")
        else:
            print(f"  1 USD = {rate:>10.2f} {cur}  (静态)")
else:
    parts = s.split()
    try:
        amt = float(parts[0])
        fr = (parts[1] if len(parts) > 1 else "USD").upper()
        to = (parts[2] if len(parts) > 2 else "CNY").upper()
        rate, tag, stale, ts = convert_currency(amt, fr, to)
        if rate is None:
            print(f"❌ 不支持 {fr}→{to}。可用：{', '.join(sorted(CACHE.keys()))}")
        else:
            result = amt * rate
            print(f"✅ {amt:.2f} {fr} = {result:.2f} {to}  ({tag})")
            if stale:
                print(f"   ⚠️ 数据更新于 {ts[:10] if ts else 'N/A'}，可能已过期")
                print(f"   💡 联网后可获取实时汇率")
    except (ValueError, IndexError):
        print("❌ 格式：100 USD CNY（金额 源货币 目标货币）")
```

</details>
