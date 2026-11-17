# 🛠️ 模块 9：实用小工具

---

#### 9.1 二维码生成 / 9.2 密码生成 / 9.3 正则测试

**✅ 开箱即用**

<details>
<summary>📋 二维码生成</summary>

```python
import urllib.parse
text = input("内容/URL:") or "https://www.example.com"
url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(text,safe='')}"
print(f"📱 复制到浏览器下载: {url}")
```

</details>

<details>
<summary>📋 密码生成器</summary>

```python
import random, string, math
length = int(input("密码长度(16):") or 16)
chars = string.ascii_letters + string.digits + "!@#$%^&*"
pwd = ''.join(random.choice(chars) for _ in range(length))
entropy = length * math.log2(len(chars))
print(f"🔐 {pwd}")
print(f"强度: {'★★★★★' if entropy>=80 else '★★★★☆' if entropy>=60 else '★★★☆☆'} ({entropy:.1f} bits)")
```

</details>

<details>
<summary>📋 正则测试器</summary>

```python
import re
p = input("正则:") or r"\b\w+@\w+\.\w+\b"
t = input("文本:") or "test@example.com"
try:
    m = re.findall(p, t)
    print(f"✅ 找到 {len(m)} 个: {m}" if m else "❌ 无匹配")
except re.error as e: print(f"❌ 语法错误: {e}")
```

</details>

---

#### 9.4 文件哈希校验 ⭐ v3.6.0 新增

**✅ 开箱即用**（纯 Python 标准库 hashlib，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import hashlib, os

path = input("文件路径:").strip().strip('"').strip("'")
if not path or not os.path.isfile(path):
    print(f"❌ 文件不存在: {path}")
else:
    algos = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256()}
    size = os.path.getsize(path)
    chunk = 8 * 1024 * 1024
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            for h in algos.values():
                h.update(data)
    print(f"📄 文件: {os.path.basename(path)}  ({size/1024:.1f} KB)")
    for name, h in algos.items():
        print(f"  {name.upper():7}: {h.hexdigest()}")
    expect = input("粘贴期望哈希值比对(可留空回车跳过):").strip().lower()
    if expect:
        matched = [n for n, h in algos.items() if h.hexdigest().lower() == expect]
        print(f"✅ 校验通过（{matched[0].upper()}）" if matched else "❌ 校验失败：哈希值不匹配，文件可能已损坏或被篡改")
```

</details>

---

#### 9.5 UUID 生成器 ⭐ v3.6.0 新增

**✅ 开箱即用**（纯 Python 标准库 uuid，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import uuid

mode = input("类型(uuid4随机/uuid1时间/nodash无横线):").strip() or "uuid4"
try:
    count = int(input("生成数量(默认1):") or 1)
except ValueError:
    count = 1
count = max(1, min(count, 100))

for _ in range(count):
    if mode == "uuid1":
        u = str(uuid.uuid1())
    elif mode == "nodash":
        u = uuid.uuid4().hex
    else:
        u = str(uuid.uuid4())
    print(u)
print(f"✅ 已生成 {count} 个 UUID（{mode}）")
```

</details>

---

#### 9.6 时间戳转换 ⭐ v3.6.0 新增

**✅ 开箱即用**（纯 Python 标准库 datetime，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import datetime, time

s = input("输入时间戳 或 日期(YYYY-MM-DD HH:MM:SS)，留空取当前:").strip()
if not s:
    now = time.time()
    print(f"⏰ 当前时间: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"   秒级时间戳: {int(now)}")
    print(f"   毫秒级时间戳: {int(now*1000)}")
elif s.replace(".", "").isdigit():
    ts = float(s)
    if ts > 1e12:
        ts /= 1000
    try:
        dt = datetime.datetime.fromtimestamp(ts)
        print(f"✅ 时间戳 {s} →")
        print(f"   本地时间: {dt:%Y-%m-%d %H:%M:%S}")
        print(f"   星期: {'一二三四五六日'[dt.weekday()]}")
    except (ValueError, OSError):
        print("❌ 时间戳超出有效范围")
else:
    parsed = None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
        try:
            parsed = datetime.datetime.strptime(s, fmt)
            break
        except ValueError:
            continue
    if parsed:
        print(f"✅ 日期 {s} →")
        print(f"   秒级时间戳: {int(parsed.timestamp())}")
        print(f"   毫秒级时间戳: {int(parsed.timestamp()*1000)}")
    else:
        print("❌ 无法识别，请用 时间戳 或 YYYY-MM-DD HH:MM:SS 格式")
```

</details>

---

#### 9.7 IP 工具 ⭐ v3.6.0 新增

**✅ 开箱即用**（纯 Python 标准库 ipaddress/socket，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import ipaddress, socket

s = input("输入IP或网段(如192.168.1.0/24)，留空查本机:").strip()
if not s:
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"🖥️ 主机名: {hostname}")
        print(f"   本机IP: {local_ip}")
    except socket.error as e:
        print(f"❌ 获取本机IP失败: {e}")
else:
    try:
        if "/" in s:
            net = ipaddress.ip_network(s, strict=False)
            print(f"✅ 网段: {net}")
            print(f"   网络地址: {net.network_address}")
            print(f"   广播地址: {net.broadcast_address}")
            print(f"   子网掩码: {net.netmask}")
            print(f"   可用主机数: {net.num_addresses}")
        else:
            ip = ipaddress.ip_address(s)
            print(f"✅ IP: {ip}  (IPv{ip.version})")
            print(f"   私有地址: {'是' if ip.is_private else '否'}")
            print(f"   回环地址: {'是' if ip.is_loopback else '否'}")
            print(f"   多播地址: {'是' if ip.is_multicast else '否'}")
    except ValueError as e:
        print(f"❌ 无效的IP或网段: {e}")
```

</details>

---

#### 9.8 CSV 查看器 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 csv，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import csv, os

path = input("CSV文件路径:").strip().strip('"').strip("'")
if not path or not os.path.isfile(path):
    print(f"❌ 文件不存在: {path}")
else:
    enc = "utf-8"
    for try_enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            with open(path, encoding=try_enc) as f:
                f.read(4096)
            enc = try_enc; break
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, encoding=enc) as f:
        head = f.read(2048)
    try:
        dialect = csv.Sniffer().sniff(head, delimiters=",\t;|")
    except csv.Error:
        dialect = csv.excel
    with open(path, encoding=enc, newline="") as f:
        reader = csv.reader(f, dialect)
        rows = list(reader)
    if not rows:
        print("⚠️ 文件为空")
    else:
        max_cols = max(len(r) for r in rows)
        widths = [0] * max_cols
        for r in rows:
            for i, c in enumerate(r):
                widths[i] = max(widths[i], len(c))
        widths = [min(w, 30) for w in widths]
        total = len(rows)
        page = 20
        for start in range(0, total, page):
            print(f"\n--- 第 {start+1}-{min(start+page, total)} 行 / 共 {total} 行 ---")
            for r in rows[start:start+page]:
                line = " | ".join((c if len(c)<=w else c[:w-1]+"…").ljust(w) for c, w in zip(r, widths))
                print(line)
            if start + page < total:
                more = input("按回车继续 / q 退出: ").strip().lower()
                if more == "q":
                    break
```

</details>

---

#### 9.9 密码强度检测 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import re, hashlib

COMMON_PASSWORDS = {
    "123456","password","12345678","qwerty","123456789","letmein","1234567","football","iloveyou",
    "admin","welcome","monkey","login","abc123","111111","123123","password123","1234","000000",
    "1qaz2wsx","qwerty123","123qwe","password1","sunshine","princess","dragon","flower","shadow",
    "superman","michael","master","photoshop","112233","654321","trustno1","batman","passw0rd"
}

pwd = input("待检测密码:").strip()
if not pwd:
    print("❌ 请输入密码")
else:
    score = 0
    tips = []
    if len(pwd) >= 8: score += 1
    else: tips.append("长度不足8位")
    if len(pwd) >= 12: score += 1
    if len(pwd) >= 16: score += 1
    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"\d", pwd))
    has_symbol = bool(re.search(r"[^a-zA-Z\d]", pwd))
    diversity = sum([has_lower, has_upper, has_digit, has_symbol])
    score += diversity
    if not has_lower: tips.append("缺少小写字母")
    if not has_upper: tips.append("缺少大写字母")
    if not has_digit: tips.append("缺少数字")
    if not has_symbol: tips.append("缺少特殊符号")
    if re.search(r"(.)\1{2,}", pwd):
        score -= 2; tips.append("含3+连续重复字符(如aaa)")
    if re.search(r"(012|123|234|345|456|567|678|789|890)", pwd):
        score -= 2; tips.append("含连续数字序列(如123)")
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)", pwd.lower()):
        score -= 2; tips.append("含连续字母序列(如abc)")
    if pwd.lower() in COMMON_PASSWORDS:
        score = 0; tips.append("⚠️ 在常见弱密码字典中！")
    score = max(0, min(score, 10))
    stars = "★" * (score // 2) + "☆" * (5 - score // 2)
    labels = {0:"极弱",1:"极弱",2:"极弱",3:"弱",4:"弱",5:"中等",6:"中等",7:"强",8:"强",9:"很强",10:"极强"}
    print(f"长度: {len(pwd)} | 字符类: {diversity}/4")
    print(f"评分: {score}/10  {stars}  [{labels[score]}]")
    if tips:
        print("建议:")
        for t in tips[:5]:
            print(f"  • {t}")
    if score >= 8:
        print("✅ 密码强度优秀")
    elif score >= 5:
        print("💡 尚可，但有提升空间")
    else:
        print("❌ 建议立即修改")
```

</details>

---

#### 9.10 颜色值转换 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯数学运算，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import re

s = input("输入颜色值(如#FF0000 / rgb(255,0,0) / 255,0,0):").strip()
if not s:
    print("❌ 请输入颜色值")
else:
    r = g = b = None
    s_clean = s.strip()
    hex_m = re.match(r"^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$", s_clean)
    if hex_m:
        hx = hex_m.group(1)
        if len(hx) == 3:
            r, g, b = int(hx[0]*2,16), int(hx[1]*2,16), int(hx[2]*2,16)
        else:
            r, g, b = int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)
    rgb_m = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", s_clean, re.I)
    if rgb_m and r is None:
        r, g, b = int(rgb_m.group(1)), int(rgb_m.group(2)), int(rgb_m.group(3))
    num_m = re.match(r"^(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})$", s_clean)
    if num_m and r is None:
        r, g, b = int(num_m.group(1)), int(num_m.group(2)), int(num_m.group(3))
    if r is None or not all(0 <= v <= 255 for v in (r, g, b)):
        print("❌ 无法识别。支持格式: #FF0000 / #F00 / rgb(255,0,0) / 255,0,0")
    else:
        hex_out = f"#{r:02X}{g:02X}{b:02X}"
        rn, gn, bn = r/255, g/255, b/255
        mx, mn = max(rn, gn, bn), min(rn, gn, bn)
        l = (mx + mn) / 2
        if mx == mn:
            h = s = 0
        else:
            d = mx - mn
            s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
            if mx == rn:
                h = (gn - bn) / d + (6 if gn < bn else 0)
            elif mx == gn:
                h = (bn - rn) / d + 2
            else:
                h = (rn - gn) / d + 4
            h /= 6
        h_deg = round(h * 360)
        s_pct = round(s * 100)
        l_pct = round(l * 100)
        print(f"✅ {s_clean} →")
        print(f"   HEX : {hex_out}  (小写: {hex_out.lower()})")
        print(f"   RGB : rgb({r}, {g}, {b})")
        print(f"   HSL : hsl({h_deg}, {s_pct}%, {l_pct}%)")
```

</details>

---

#### 9.11 随机数生成器 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 random，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import random, string

mode = input("模式(整数/小数/硬币/骰子/打乱/抽样/字符串):").strip() or "整数"
if mode == "整数":
    try:
        a = int(input("最小值(默认1):") or 1)
        b = int(input("最大值(默认100):") or 100)
        n = int(input("数量(默认1):") or 1)
        if a > b: a, b = b, a
        res = [random.randint(a, b) for _ in range(max(1, min(n, 100)))]
        print(f"✅ {res}")
    except ValueError: print("❌ 请输入整数")
elif mode == "小数":
    try:
        a = float(input("最小值(默认0):") or 0)
        b = float(input("最大值(默认1):") or 1)
        if a > b: a, b = b, a
        res = [round(random.uniform(a, b), 6) for _ in range(3)]
        print(f"✅ {res}")
    except ValueError: print("❌ 请输入数字")
elif mode == "硬币":
    n = int(input("次数(默认1):") or 1)
    res = ["正面" if random.random() < 0.5 else "反面" for _ in range(max(1, min(n, 100)))]
    h = res.count("正面")
    print(f"✅ {res}")
    print(f"   正面{h}次 / 反面{len(res)-h}次")
elif mode == "骰子":
    n = int(input("骰子数(默认1):") or 1)
    res = [random.randint(1, 6) for _ in range(max(1, min(n, 20)))]
    print(f"✅ {res}  合计: {sum(res)}")
elif mode == "打乱":
    items = input("输入列表(逗号分隔):").split(",")
    items = [x.strip() for x in items if x.strip()]
    random.shuffle(items)
    print(f"✅ {items}")
elif mode == "抽样":
    items = input("列表(逗号分隔):").split(",")
    items = [x.strip() for x in items if x.strip()]
    try:
        k = int(input(f"抽取数(1-{len(items)}):") or 1)
        k = max(1, min(k, len(items)))
    except ValueError: k = 1
    print(f"✅ {random.sample(items, k)}")
elif mode == "字符串":
    length = int(input("长度(默认16):") or 16)
    chars = ""
    if input("字母(y/n 默认y):").strip().lower() != "n": chars += string.ascii_letters
    if input("数字(y/n 默认y):").strip().lower() != "n": chars += string.digits
    if input("符号(y/n 默认n):").strip().lower() == "y": chars += "!@#$%^&*"
    if not chars: chars = string.ascii_letters + string.digits
    print(f"✅ {''.join(random.choice(chars) for _ in range(max(1, min(length, 256))))}")
else:
    print(f"❌ 不支持 {mode}。可选: 整数/小数/硬币/骰子/打乱/抽样/字符串")
```

</details>
