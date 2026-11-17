# 🎮 模块 4：生活娱乐

> ⚠️ v4.1.0 起，本模块移至 `ent`（娱乐）可选包，默认不加载。

---

#### 4.1 娱乐小工具

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, json, random

def _joke_cn():
    apis = [
        ("https://api.apiopen.top/getJoke?page=1&count=1&type=txt", lambda d: d.get("result",[{}])[0].get("content","")),
        ("https://v1.hitokoto.cn/?c=a", lambda d: f"{d.get('hitokoto','')} —— {d.get('from','')}")),
        ("https://api.oioweb.cn/api/common/Hitokoto", lambda d: f"{d.get('result',{}).get('content','')} —— {d.get('result',{}).get('from','')}")),
    ]
    for url, extract in apis:
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/3.5"}), timeout=5)
            data = json.loads(r.read())
            text = extract(data)
            if text.strip(): return text
        except: continue
    return ""

try:
    c = input("选择(1笑话/2一言/3运势):").strip() or "1"
    if c == "1":
        joke = _joke_cn()
        if joke: print(f"😄 {joke}")
        else:
            jokes = [
                ("程序员为什么喜欢用暗色主题？", "因为光明会引来 bug！"),
                ("老婆问程序员丈夫：你到底爱不爱我？", "当然爱。老婆：那你能不能不在'当然爱'后面加分号？感觉像执行完就结束。"),
            ]
            s, p = random.choice(jokes)
            print(f"📶 联网失败，给你讲个本地笑话：\n   {s}\n   → {p}")
    elif c == "2":
        for url, extract in [
            ("https://v1.hitokoto.cn/", lambda d: f"{d.get('hitokoto','')} —— {d.get('from','')}"),
            ("https://tenapi.cn/v2/yiyan", lambda d: d.get("data","") or d.get("content","")),
        ]:
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/3.5"}), timeout=5)
                t = extract(json.loads(r.read()))
                if t: print(f"✨ {t}"); break
            except: continue
        else: print("📶 一言API不可用，试试 https://hitokoto.cn/")
    elif c == "3":
        print(random.choice(["大吉","中吉","小吉","吉","末吉","凶","大凶"]))
    else: print("❌ 请输入 1、2 或 3")
except Exception as e: print(f"❌ {e}")
```

</details>

---

#### 4.2 壁纸中心

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, urllib.parse, json

def _wallpaper_cn():
    for url, src in [
        ("https://imgapi.cn/api.php?zd=pc&fl=fengjing&gs=jpg", "风景随机"),
        ("https://picsum.photos/1920/1080", "随机摄影"),
    ]:
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/3.5"}), timeout=8)
            final = r.geturl()
            if final and final != url: return (final, src)
        except: continue
    return None

try:
    _ = input("关键词:").strip() or "nature"
    result = _wallpaper_cn()
    if result:
        print(f"📷 来源: {result[1]}\n   下载: {result[0]}")
        print("   💡 右键→图片另存为")
    else:
        print("❌ 壁纸源不可用")
        print("   • https://unsplash.com/s/photos/nature")
        print("   • https://pixabay.com/zh/images/search/nature/")
except Exception as e: print(f"❌ {e}")
```

</details>

---

#### 4.3 BMI 计算器 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯数学运算，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
try:
    w = float(input("体重(kg):"))
    h = float(input("身高(cm):"))
    if w <= 0 or h <= 0:
        print("❌ 体重和身高必须大于0")
    elif h > 300 or w > 700:
        print("❌ 请输入合理的体重(kg)和身高(cm)")
    else:
        bmi = w / ((h/100) ** 2)
        if bmi < 18.5:
            label = "偏瘦"; advice = "适当增加营养摄入"
        elif bmi < 24:
            label = "正常"; advice = "保持良好生活习惯"
        elif bmi < 28:
            label = "偏胖"; advice = "建议控制饮食+增加运动"
        else:
            label = "肥胖"; advice = "建议就医评估+制定减重计划"
        ideal_low = 18.5 * (h/100)**2
        ideal_high = 24 * (h/100)**2
        print(f"✅ BMI: {bmi:.1f}  [{label}]")
        print(f"   理想体重范围: {ideal_low:.1f} - {ideal_high:.1f} kg")
        print(f"   建议: {advice}")
        print(f"   ⚠️ BMI 仅供筛查，不替代医学诊断")
except ValueError:
    print("❌ 请输入数字，如 70 和 175")
```

</details>

---

#### 4.4 番茄钟 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 time，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import time, sys

print("🍅 番茄工作法：专注25分钟 + 休息5分钟")
print("   Ctrl+C 可随时退出")
try:
    work_min = int(input("专注时长(分钟,默认25):") or 25)
    rest_min = int(input("休息时长(分钟,默认5):") or 5)
    rounds = int(input("轮数(默认4):") or 4)
except ValueError:
    print("❌ 请输入整数"); sys.exit()

work_sec = max(1, work_min) * 60
rest_sec = max(1, rest_min) * 60

def _countdown(seconds, label):
    for remaining in range(seconds, 0, -1):
        m, s = divmod(remaining, 60)
        print(f"\r   {label}: {m:02d}:{s:02d}", end="", flush=True)
        time.sleep(1)
    print()

try:
    for r in range(1, rounds + 1):
        print(f"\n=== 第 {r}/{rounds} 轮 ===")
        _countdown(work_sec, "⏳ 专注中")
        print("🔔 时间到！休息一下吧~")
        try:
            print("\a", end="", flush=True)
        except Exception:
            pass
        if r < rounds:
            _countdown(rest_sec, "☕ 休息中")
            print("✅ 休息结束，准备下一轮")
        else:
            print(f"🎉 全部完成！共专注 {rounds * work_min} 分钟")
except KeyboardInterrupt:
    print("\n\n⏹️ 已手动退出")
```

</details>
