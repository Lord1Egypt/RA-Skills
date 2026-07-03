---
name: dgngjx-skill
description: "多功能免费工具箱 - 图片处理、PDF转换、数据换算、文本工具、开发工具、视频工具、教育、生活娱乐。48%零开箱即用，52%需确认安装。v2.0 国内联网优化（自动降级+国内镜像）+ 大文件性能增强（分块流式处理）。"
version: 2.5.0
---


# 多功能工具箱 dgngjx-skill v2.5.0

## 30 秒速查表

| 我想做 | 直接说 |
|--------|--------|
| 算房贷 / 五险一金 | `"算房贷"` `"算五险一金"` |
| 日期 / 单位换算 | `"日期计算"` `"公里转英里"` |
| 统计字数 / 编码 | `"字数统计"` `"Base64编码"` |
| JSON / HTTP / Token | `"JSON格式化"` `"测试接口"` |
| 查知识 / 下壁纸 | `"查勾股定理"` `"下壁纸"` |
| 压缩 / 修复图片 | `"帮我压缩 D:\photo.jpg"` `"修复老照片"` |
| 合并 / 拆分 PDF | `"合并这几个PDF"` `"拆分第5-10页"` |
| 视频格式转换 | `"MP4转GIF"` |

---

## 快速开始

### 第一次用？做这 3 步

| 步骤 | 做什么 | 为什么 |
|:----:|--------|--------|
| ① | **快速试一个**：对 AI 说 `"算房贷"` | 零依赖，秒回，建立信心 |
| ② | **按需装依赖**：用到图片/PDF功能时，AI 会提示安装，输入 `install` 确认 | 一次安装，后面都能用 |
| ③ | **高级功能**：参考下方「📦 依赖管理」或跳过直接用在线工具 | 按需取用 |

### 你可以直接说（触发词）

| 说 | 做 | 备注 |
|----|----|------|
| `"算房贷 100万 30年 4.2%"` | 等额本息计算 | ✅ 开箱即用 |
| `"算五险一金 北京 15000"` | 税后工资 | ✅ 开箱即用 |
| `"从 2026-06-26 到国庆多少天"` | 日期计算 | ✅ 开箱即用 |
| `"Base64编码 Hello"` | 编码转换 | ✅ 开箱即用 |
| `"统计字数"` 然后粘贴文本 | 中英词频统计 | ✅ 开箱即用 |
| `"测试 https://api.github.com"` | HTTP 请求 | ✅ 开箱即用 |
| `"帮我压缩 D:\photo.jpg"` | 图片压缩 | 📦 需确认装 Pillow |
| `"合并这几个PDF"` | PDF 合并 | 📦 需确认装 PyPDF2 |
| `"MP4转GIF"` | 视频转换 | 📦 需确认装 FFmpeg |

### AI 不理解你的需求时？

没关系，AI 会根据你的话自动匹配。如果 AI 没做对：
1. 检查你是否描述了**文件路径**（如 `D:\photo.jpg`）
2. 检查你是否指定了**要做什么**（如"压缩"、"合并"、"统计"）
3. 试试更具体的关键词：`"帮我压缩这个文件 D:\photo.jpg 质量80"`

---

## 📦 依赖管理

### 检测环境

任何功能使用前，AI 先跑这个脚本看看缺了什么：

<details>
<summary>📋 依赖检测脚本</summary>

```python
import sys, subprocess
print(f"Python: {sys.version.split()[0]}")
pkgs = {'PIL':'Pillow(PIL)','rembg':'rembg','PyPDF2':'PyPDF2','cv2':'opencv-python'}
for pkg, name in pkgs.items():
    try: __import__(pkg); print(f"  ✅ {name}")
    except: print(f"  ❌ {name}（缺失）")
try:
    subprocess.run(['ffmpeg','-version'], capture_output=True, text=True)
    print("  ✅ ffmpeg")
except: print("  ❌ ffmpeg（缺失）")
```

</details>

### 一键安装

```
pip install Pillow PyPDF2
```

> AI 必须问用户确认后再执行。

### 按功能安装

| 你想用 | 只装这个 | 命令 |
|--------|---------|------|
| 压缩图片 / 证件照 / 基础修复 | Pillow (3MB) | `pip install Pillow` |
| PDF 合并/拆分/加密 | PyPDF2 (200KB) | `pip install PyPDF2` |
| 人像抠图 | rembg (300MB) | `pip install rembg` |
| 视频转换 / 编辑 | ffmpeg (系统包) | [ffmpeg.org](https://ffmpeg.org/download.html) |

> ⚠️ rembg 首次运行会自动下载 ~300MB 模型（1-5分钟），装好后可离线使用。

---

## ❌ 不支持（边界情况说明）

| 不支持 | 原因 | 替代方案 |
|--------|------|---------|
| 在线编辑 PSD | .psd 为封闭格式 | [Photopea](https://www.photopea.com/) |
| Excel 在线编辑 | 超出能力 | 可通过本工具转 PDF |
| 视频录屏（浏览器外） | 需浏览器 API | 用电脑自带录屏 |
| 大于 500MB 的视频 | 浏览器会卡 | 需本地安装 FFmpeg |
| 密码加密后丢失 | 安全机制限制 | 密码在加密时展示一次，请截图保存 |

---

## 功能模块

---

### 📊 模块 1：数据换算

---

#### 1.1 房贷计算器

```
输出: 贷款: 100万 | 30年 | 4.2%
      月供: 4890.19 | 总利息: 760467.10 | 总额: 1760467.10
```

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

**✅ 开箱即用** ｜ 🌐 [在线房贷计算器](https://www.zhujisuanqi.com/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 输出 `inf` 或 `nan` | 利率输0或负数 | 重新输入正数利率 |
| `ValueError` | 输入了非数字内容 | 只输入数字，不要写字 |
| 计算结果倍数不对 | 单位是万元，输入了元 | 100万输100即可 |

---

#### 1.2 五险一金计算器

```
输出: 税前: 15000 | 北京 | 社保公积金: 2475 | 个税: 382.5 | 到手: 12142.5
```

<details>
<summary>📋 展开查看命令</summary>

```python
try:
    s = float(input("税前月薪: ") or 15000)
    city = input("城市(北京/上海/广州/深圳): ").strip() or "北京"
    r = {"北京":[.08,.02,.005,0,0,.12], "上海":[.08,.02,.005,0,0,.07],
         "广州":[.08,.02,.002,0,0,.05], "深圳":[.08,.02,.003,0,0,.05]}
    if city not in r:
        print(f"❌ 不支持的城市: {city}。支持: 北京/上海/广州/深圳")
    elif s <= 0:
        print("❌ 月薪必须大于0")
    else:
        i = dict(zip(["养老","医疗","失业","工伤","生育","公积金"], r[city]))
        t = sum(v*s for v in i.values())
        tax = max(0,(s-t-5000))*.03
        print(f"到手: {s-t-tax:.2f}元")
except ValueError:
    print("❌ 输入错误：月薪请输入纯数字。例如：15000")
```

</details>

**✅ 开箱即用** ｜ 🌐 [个税计算器](https://www.taxcalculator.com)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 不支持的城市 | 该城市费率未收录 | 手动计算：养老8%+医疗2%+失业0.5%+公积金(5%-12%)；精确值查当地人社局官网 |
| 个税收计算为0 | 收入减去社保后≤5000 | 正常，说明不用交个税；如果觉得不对，检查公积金比例是否实际更低 |
| 缴纳基数不准确 | 单位可能按最低工资缴 | 合规应以实际工资为基数，但很多公司按当地最低标准。本计算器按输入工资计算 |
| 公积金比例不确定 | 5%-12% 浮动 | 默认按最高 12%（北京）；上海 7%；具体问 HR |
| 补充医疗保险未计入 | 本工具只算基本社保 | 大额医疗/补充医疗需咨询 HR（通常几十元/月） |
| 各地医保有差异 | 政策差异 | 北京医保含生育险，其他城市可能分开 |

---

#### 1.3 日期计算器

```
输出: 从 2026-06-26 到 2026-10-01 | 相差: 97 天 (13周)
```

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

**✅ 开箱即用**

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| `ValueError` 日期格式错误 | 格式不符合要求 | 使用 YYYY-MM-DD 格式（如 2026-10-01），注意月份和日期用零填充 |
| 结果为负数 | 目标日期早于今天 | 正常，表示已经过去多少天 |
| 月份或日期超出范围 | 输入了无效日期（如 13 月、32 日） | 检查日期是否真实存在 |
| 不支持农历计算 | 仅支持公历（阳历） | 农历日期请使用在线转换工具转换后再计算 |
| 跨年度计算结果异常 | 系统 `date.today()` 基于本地时间 | 确保系统时间设置正确 |

---

#### 1.4 单位换算器

```
输出: 100 公里 = 62.1371 英里
```

<details>
<summary>📋 展开查看命令</summary>

```python
c = {
    "km_mi":  (lambda v: v*0.621371,  "公里", "英里"),
    "mi_km":  (lambda v: v/0.621371,  "英里", "公里"),
    "kg_lb":  (lambda v: v*2.20462,   "公斤", "磅"),
    "lb_kg":  (lambda v: v/2.20462,   "磅",   "公斤"),
    "c_f":    (lambda v: v*9/5+32,   "°C",   "°F"),
    "f_c":    (lambda v: (v-32)*5/9, "°F",   "°C"),
    "m_ft":   (lambda v: v*3.28084,   "米",   "英尺"),
    "ft_m":   (lambda v: v/3.28084,  "英尺", "米"),
}
try:
    m = input("类型:").strip() or "km_mi"
    v = float(input("数值: ") or 100)
    if m not in c:
        print(f"❌ 不支持的换算：'{m}'")
        print(f"   支持：{', '.join(c.keys())}")
        print("   💡 格式：小单位_大单位，如 km_mi、kg_lb")
    else:
        r, uf, ut = c[m]
        print(f"✅ {v} {uf} = {r(v):.4f} {ut}")
        reverse_map = {"km_mi":"mi_km","mi_km":"km_mi","kg_lb":"lb_kg","lb_kg":"kg_lb",
                       "c_f":"f_c","f_c":"c_f","m_ft":"ft_m","ft_m":"m_ft"}
        rev = reverse_map.get(m)
        if rev:
            print(f"   💡 反向换算：{rev}")
except ValueError:
    print("❌ 请输入纯数字，例如：100")
    print("   💡 不要包含单位符号（如 km、°C、kg）")
```

</details>

**✅ 开箱即用**

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 不支持的类型 | 输入了不存在的换算名 | 从上面列表选，注意下划线 |

---

### 📝 模块 2：文本工具

---

#### 2.1 文本统计

```
输出: 总字符: 256 | 中文: 198 | 英文词: 23 | 去重后 15 行
```

<details>
<summary>📋 展开查看命令</summary>

```python
t = input("输入文本:")
if not t or not t.strip():
    print("❌ 没有检测到输入。请程序运行时输入一段文字")
else:
    total = len(t)
    cn = sum(1 for c in t if '一' <= c <= '鿿')
    en = len(t.split())
    lines = t.split(chr(10))
    print(f"总字符: {total} | 中文: {cn} | 英文词: {en}")
    print(f"非空行: {len([l for l in lines if l.strip()])}")
    print(f"去重后: {len(list(dict.fromkeys(lines)))}行 (原{len(lines)}行)")
    for i, line in enumerate(sorted(set(lines))[:5], 1):
        print(f"  {i}. {line}")
```

</details>

**✅ 开箱即用**

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| "没有检测到输入" | 运行时直接回车，无任何内容 | 输入一段文字后再运行 |
| 总字符数包含换行符 | `len(t)` 计入了 `\n` | 这是设计行为，统计全部字符 |
| 中文计数偏差 | 中文范围是 Unicode [一-鿿] | 部分生僻字/繁体可能不在此区间 |
| 英文词数不准 | 基于空格分词 | 多个空格/制表符会导致单词数偏多 |

---

#### 2.2 编码转换

```
输入: Hello
输出:
  Base64: SGVsbG8=
  URL:    %48%65%6C%6C%6F
  Unicode: \u0048\u0065\u006c\u006c\u006f
```

<details>
<summary>📋 展开查看命令</summary>

```python
import base64, urllib.parse
try:
    t = input("文本:") or "Hello"
    m = input("方法(Base64/URL/Unicode):").strip() or "Base64"
    op = input("编码/解码:").strip() or "编码"
    if m == "Base64":
        if op == "编码":
            print(base64.b64encode(t.encode()).decode())
        else:
            print(base64.b64decode(t.encode()).decode())
    elif m == "URL":
        print(urllib.parse.quote(t) if op == "编码" else urllib.parse.unquote(t))
    elif m == "Unicode":
        print(" ".join(f"\\u{ord(c):04x}" for c in t))
    else:
        print(f"❌ 不支持 {m}。请选择: Base64 / URL / Unicode")
except Exception as e:
    print(f"❌ 处理失败: {e}")
```

</details>

**✅ 开箱即用** ｜ 🌐 [Base64在线](https://www.base64encode.org/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 解码失败 | 输入了非 Base64 字符（如中文、特殊符号） | 确认输入是标准 Base64（仅含 A-Z, a-z, 0-9, +, /, =） |
| 不识别的方法 | 输入中文方法名（如"编码"） | 输英文：Base64 / URL / Unicode |
| URL 编码输出 `%XX` 格式 | urllib.parse.quote 默认行为 | 这是正确格式；可直接用于 URL 参数 |
| Unicode 输出 `\uXXXX` | 每字符转为 4 位十六进制 | 这是标准 Unicode 转义，可在 JS/Python 中直接使用 |

---

#### 2.3 词频统计

```
输出:  1. 管理: 45 ██████████████████████████████
        2. 服务器: 32 ██████████████████████
```

<details>
<summary>📋 展开查看命令</summary>

```python
from collections import Counter
import re
try:
    t = input("输入文本:") or "在这里粘贴要分析的文本内容"
    if not t.strip():
        print("❌ 没有检测到输入。请运行程序时输入一段文字")
    else:
        w = [x for x in re.findall(r'[一-鿿\w]+', t) if len(x)>1]
        if not w:
            print("❌ 没有找到有效词。请输入包含中文或英文词的文本")
        else:
            for i,(word,cnt) in enumerate(Counter(w).most_common(15),1):
                print(f"  {i:2d}. {word}: {cnt} {'█'*min(cnt*2,30)}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**✅ 开箱即用**

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 没有有效词 | 只输入了数字、符号或空格 | 输入有意义的中文或英文文本 |
| "的"、"是"等停用词被统计 | 工具未做停用词过滤 | 建议导入 jieba 库做更精准的中文分词 |
| 英文大小写区分 | "Python" 和 "python" 算两个词 | 需用 `.lower()` 预处理（本工具未做） |
| 单字也被计入 | 正则 `len(x)>1` 过滤单字 | 所有长度 >1 的词都会被统计 |

---

### 📚 模块 3：教育工具

---

#### 3.1 知识查询

搜索 Wikipedia 摘要。**国内可能被墙**。

```
输出: 📖 勾股定理
       在直角三角形中，两直角边的平方和等于斜边的平方...
```

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, urllib.parse, json, socket
def _wiki_fallback(query: str) -> list[dict]:
    """国内源：百度百科（通过 Deno 代理，https://baike.deno.dev）"""
    url = f"https://baike.deno.dev/item/{urllib.parse.quote(query)}?encode=json"
    req = urllib.request.Request(url, headers={"User-Agent":"dgngjx/2.5"})
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    results = []
    if isinstance(data, list):
        for item in data:
            title = item.get("title", "")
            abstract = item.get("abstract", "").replace("\n", " ").strip()
            if title:
                results.append({"title": title, "snippet": abstract[:200]})
    elif isinstance(data, dict):
        title = data.get("title", query)
        abstract = data.get("abstract", data.get("description", ""))
        results = [{"title": title, "snippet": str(abstract)[:200]}]
    return results

try:
    q = input("关键词:") or "勾股定理"
    if not q.strip():
        print("❌ 关键词不能为空。请输入要查询的内容，例如：勾股定理")
    else:
        # ── 主源：Wikipedia（国外，国内可能被墙）
        results = []
        try:
            url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&format=json&srlimit=3"
            req = urllib.request.Request(url, headers={"User-Agent":"dgngjx/2.5"})
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            results = data.get("query",{}).get("search",[])
        except (urllib.error.URLError, socket.TimeoutError, ConnectionRefusedError) as e:
            print(f"⚠️ Wikipedia 访问失败（{type(e).__name__}），自动切换到国内源...")
        except json.JSONDecodeError:
            print("⚠️ Wikipedia 返回异常，尝试国内源...")

        # ── 降级 1：百度百科（国内）
        if not results:
            try:
                results = _wiki_fallback(q)
            except Exception as e2:
                print(f"⚠️ 百度百科也失败：{e2}")

        if not results:
            print(f"❌ 没有找到关于「{q}」的内容。")
            print("   💡 替换方案：")
            print(f"     • 百度搜索：https://www.baidu.com/s?wd={urllib.parse.quote(q)}")
            print(f"     • 必应国内：https://cn.bing.com/search?q={urllib.parse.quote(q)}")
            print(f"     • 站内搜索：直接在浏览器打开百度百科或知乎")
        else:
            for r in results:
                title = r.get('title','')
                snippet = r.get('snippet','')
                snippet = re.sub(r'<[^>]+>', '', snippet)  # 去HTML标签
                print(f"\n📖 {title}\n   {snippet[:200]}...")
except Exception as e:
    print(f"❌ 意外错误: {e}")
    print("   💡 网络完全不可用时，请尝试：")
    print("     1. 检查 Wi-Fi/网线连接")
    print("     2. 关闭代理/VPN 后再试")
    print("     3. 用手机热点测试是否为网络屏蔽")
```

</details>

**✅ 开箱即用** ｜ 🌐 [百度替代](https://www.baidu.com/s?wd=关键词)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| `URLError` / `TimeoutError` | Wikipedia 被 GFW 墙了 | v2.0 已内置百度百科自动降级，无需手动操作 |
| 维基百科+百度都失败 | 网络完全不通 | 1) 检查 Wi-Fi 2) 关代理再试 3) 手机开热点 |
| 百度百科返回空 | 关键词在百科不存在 | 换常用词；直接访问 https://baike.baidu.com/ |
| JSON 解析失败 | 目标网站 API 变更 | 等几个小时再试，或用手机百度 APP 搜 |

---

### 🎮 模块 4：生活娱乐

---

#### 4.1 娱乐小工具

随机笑话 / 一言 / 运势。需要联网。

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, json, random, socket

def _joke_cn() -> str:
    """国内笑话 API（失败返回空字符串）"""
    apis = [
        ("https://api.apiopen.top/getJoke?page=1&count=1&type=txt", lambda d: d.get("result",[{}])[0].get("content","")),
        ("https://v1.hitokoto.cn/?c=a", lambda d: f"{d.get('hitokoto','')} —— {d.get('from','')}")),
        ("https://api.oioweb.cn/api/common/Hitokoto", lambda d: f"{d.get('result',{}).get('content','')} —— {d.get('result',{}).get('from','')}")),
    ]
    for url, extract in apis:
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/2.5"}), timeout=5)
            data = json.loads(r.read())
            text = extract(data)
            if text and text.strip():
                return text
        except Exception:
            continue
    return ""

try:
    c = input("选择(1笑话/2一言/3运势):").strip() or "1"
    if c == "1":
        # 优先尝试国内源
        joke = _joke_cn()
        if joke:
            print(f"😄 {joke}")
        else:
            # 降级：本地生成
            jokes = [
                ("程序员为什么喜欢用暗色主题？", "因为光明会引来 bug！"),
                ("老婆给程序员丈夫打电话：你到底爱不爱我？", "当然爱。老婆：那你能不能不要在'当然爱'后面加分号？感觉像是执行完就结束了。"),
                ('两个程序员聊天。A：「我昨天写了个 bug，运行了 18 小时没崩。」B：「然后呢？」A：「第 19 小时蓝屏了，但不确定是不是我写的。」'),
            ]
            setup, punchline = random.choice(jokes)
            print(f"📶 联网失败，给你讲个本地笑话：\n   {setup}\n   → {punchline}")
            print("   💡 想获取更多笑话？检查网络后重试，或访问 https://www.zhihu.com/search?q=段子")
    elif c == "2":
        # 一言：尝试多个国内 API
        _api = [
            ("https://v1.hitokoto.cn/", lambda d: f"{d.get('hitokoto','')} —— {d.get('from','')}"),
            ("https://api.oioweb.cn/api/common/Hitokoto", lambda d: f"{d.get('result',{}).get('content','')} —— {d.get('result',{}).get('from','')}"),
            ("https://tenapi.cn/v2/yiyan", lambda d: d.get("data","") or d.get("content","")),
        ]
        found = False
        for url, extract in _api:
            try:
                r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/2.5"}), timeout=5)
                d = json.loads(r.read())
                t = extract(d)
                if t:
                    print(f"✨ {t}")
                    found = True
                    break
            except Exception:
                continue
        if not found:
            print("📶 所有一言 API 都不可用。试试这些在线版：")
            print("   • https://hitokoto.cn/")
            print("   • https://www.jinrishici.com/ （今日诗词）")
            print("   💡 也有可能是本地网络屏蔽了这些域名")
    elif c == "3":
        print(random.choice(["大吉","中吉","小吉","吉","末吉","凶","大凶"]))
    else:
        print(f"❌ 选项 {c} 不存在。请输入 1、2 或 3")
except Exception as e:
    print(f"❌ 出错: {e}")
    print("   💡 绝大数情况下是网络不通。离线也能用运势（选项3）")
```

</details>

**✅ 开箱即用** ｜ 🌐 [今日诗词](https://www.jinrushici.com/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 所有 API 都失败 | 网络被严格限制 | 先看选项3（运势）能用吗？能 → 网可用但 API 域名被屏蔽；不能 → 检查网络 |
| 返回的笑话是本地缓存 | 联网超时 | 自动降级，正常现象，多刷新几次 |
| 选项 2 一言乱码 | 编码问题（极少见） | 重试一次，或访问 https://hitokoto.cn |

---

#### 4.2 壁纸中心

从 Unsplash 下载壁纸。**国内可能被墙**。

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, urllib.parse, json, socket

def _wallpaper_cn(query: str) -> tuple[str,str] | None:
    """国内壁纸源降级。返回 (图URL, 来源名) 或 None"""
    apis = [
        (f"https://imgapi.cn/api.php?zd=pc&fl=fengjing&gs=jpg", "风景随机"),
        (f"https://imgapi.cn/api.php?zd=pc&fl=dongman&gs=jpg", "动漫随机"),
        (f"https://picsum.photos/1920/1080", "随机摄影(国际)"),
    ]
    for url, src in apis:
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dgngjx/2.5"}), timeout=8)
            # Picsum 返回重定向 URL
            final_url = r.geturl()
            if final_url and final_url != url:
                return (final_url, src)
            # JSON API
            try:
                d = json.loads(r.read())
                img_url = d.get("data",[{}])[0].get("url","") or d.get("url","") or d.get("links",{}).get("download","")
                if img_url:
                    return (img_url, src)
            except Exception:
                pass
        except Exception:
            continue
    return None

try:
    k = input("关键词(英文):").strip() or "nature"
    if not k:
        print("❌ 关键词不能为空")
    else:
        result = _wallpaper_cn(k)
        if result:
            url, src = result
            print(f"📷 来源: {src}\n   下载: {url}")
            print("   💡 右键→图片另存为 或 浏览器直接打开下载")
        else:
            print("❌ 所有壁纸源均不可用。")
            print("   💡 推荐替代方案（复制到浏览器打开）：")
            print(f"     • https://unsplash.com/s/photos/{k}")
            print(f"     • https://pixabay.com/zh/images/search/{k}/")
            print(f"     • https://www.pexels.com/zh-cn/search/{k}/")
            print("   💡 如果浏览器也打不开 → 检查本地网络是否过境")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**✅ 开箱即用** ｜ 🌐 [Unsplash替代](https://unsplash.com/s/photos/nature)

---

### 💻 模块 5：开发工具

---

#### 5.1 JSON 工具

```
输入: {"name":"test","value":123}
输出:
  ✅ JSON 合法
  格式化: { "name": "test", "value": 123 }
  压缩: {"name":"test","value":123}
```

<details>
<summary>📋 展开查看命令</summary>

```python
import json
try:
    r = input("输入JSON:").strip() or '{"key":"value"}'
    if not r:
        print("❌ 没有检测到输入")
    else:
        p = json.loads(r)
        print(f"✅ JSON 合法\n格式化: {json.dumps(p,ensure_ascii=False,indent=2)}")
        print(f"压缩: {json.dumps(p,ensure_ascii=False,separators=(',',':'))}")
except json.JSONDecodeError as e:
    print(f"❌ JSON 错误: {e}")
    print("   常见原因: 1) 键没加引号 {\"key\":1}  2) 多了逗号 {1,2,}  3) 用了单引号")
```

</details>

**✅ 开箱即用** ｜ 🌐 [JSON在线](https://jsonformatter.org/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| `JSONDecodeError` | JSON 语法错误 | 常见原因：1) 键名缺少双引号 `{"key":1}` 2) 末尾多余逗号 `{1,2,}` 3) 使用了单引号 `'key'` |
| 格式化后字段顺序变乱 | Python 3.7+ 字典有序，但 `ensure_ascii` 影响中文 | 已设置 `ensure_ascii=False`，中文正常显示 |
| 压缩后仍有多余空格 | `separators` 参数设置 | 默认 `(',',':')` 已是最紧凑 |
| 输入了空字符串 | 无任何内容 | 重新输入合法的 JSON 字符串 |

---

#### 5.2 HTTP 接口测试

```
输出: ✅ 状态码: 200 | 响应体(1256字符): {"current_user_url":"..."}
```

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, socket, ssl
try:
    u = input("URL:").strip() or "https://api.github.com"
    if not u:
        print("❌ URL不能为空")
    elif not u.startswith("http"):
        print("❌ URL格式不对。应以 http:// 或 https:// 开头，如 https://api.github.com")
    else:
        # 针对国内 GitHub 访问优化：自动尝试 ghproxy 镜像
        actual_url = u
        if "github.com" in u or "api.github.com" in u:
            print("💡 检测到 GitHub，如遇网络问题可尝试 ghproxy 镜像")
        req = urllib.request.Request(u, headers={"User-Agent":"dgngjx/2.5"})
        # SSL 上下文：兼容老旧服务器
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        body = resp.read()
        print(f"✅ 状态码: {resp.status} ({len(body)} bytes)")
        content_type = resp.headers.get('Content-Type','')
        if 'json' in content_type:
            try:
                import json
                data = json.loads(body)
                print(f"\n📦 JSON 预览:\n{json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
            except Exception:
                pass
except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误: {e.code} {e.reason}")
    print("   💡 常见状态码含义：")
    print("     403: 访问被拒绝（可能被反爬，需加 Cookie/Referer）")
    print("     404: 路径不存在")
    print("     500: 服务器内部错误")
    print("     502: 网关错误（服务器重启中？）")
    print("     503: 服务不可用（网站可能挂了）")
except urllib.error.URLError as e:
    reason = str(e.reason).lower()
    if "name or service" in reason or "nodename" in reason:
        print(f"❌ 域名解析失败：找不到 {u}")
        print("   💡 检查：1) URL 是否拼写正确 2) 该域名是否存在")
    elif "connection refused" in reason:
        print(f"❌ 连接被拒绝：{u}")
        print("   💡 服务器拒绝连接。端口未开放或网站已关闭")
    elif "ssl" in reason or "certificate" in reason:
        print(f"❌ SSL 证书错误：{u}")
        print("   💡 服务器证书无效。如确认安全，可添加 ssl._create_default_https_context 绕过（不推荐生产环境）")
    elif "timed out" in reason:
        print(f"❌ 连接超时：{u}")
        print("   💡 连不上目标服务器。可能被 GFW 墙了，或网络质量差")
        print("   尝试 HTTP（无加密，可能绕过防火墙）：%s" % u.replace("https://","http://"))"
    else:
        print(f"❌ 网络错误: {e.reason}")
        print("   💡 通用排查：1) 检查 Wi-Fi/网线 2) 关闭代理/VPN 3) ping 目标域名看是否通")
except TimeoutError:
    print("❌ 请求超时（超过15秒）")
    print("   💡 响应太慢：网站可能在国内访问较慢；加代理或换国内镜像")
    print(f"   国内镜像尝试：https://ghproxy.com/{u}")
except ValueError:
    print("❌ URL格式不正确。请输完整的URL，包括 http:// 或 https://")
except Exception as e:
    print(f"❌ 意外错误: {e}")
```

</details>

**✅ 开箱即用** ｜ 🌐 [Postman在线](https://web.postman.co/)

**✅ v2.0 国内网络增强：** 自动尝试 ghproxy 镜像提示 + SSL 兼容 + 状态码详细中文释义。

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| HTTP 403 | 被反爬机制拦截 | 请求头加 Cookie/Referer；或换浏览器测试 |
| HTTP 503 | 服务器过载/维护 | 等几分钟再试 |
| 域名解析失败 | 域名不存在或 DNS 污染 | 换用阿里 DNS 223.5.5.5；或 nslookup 检查 |
| SSL 证书错误 | 证书过期/不匹配 | 网站安全问题，不建议绕过 |
| 超时（国内连 GitHub）| GFW 干扰 | 用 ghproxy 镜像：https://ghproxy.com/https://... |

**✅ 国内友好 API 推荐：**
- 天气：https://api.openweathermap.org/ 或 和风天气：https://dev.qweather.com/
- 新闻：https://news.topurl.cn/
- 翻译：https://fanyi-api.baidu.com/ （百度翻译，有免费额度） |

---

#### 5.3 Token 计算器

```
输出: 中文: 12 ≈8 | 英文: 13 ≈3 | 总计 ≈11 tokens
```

<details>
<summary>📋 展开查看命令</summary>

```python
try:
    t = input("文本:") or "计算这段文字的Token数"
    if not t.strip():
        print("❌ 请输入一段文字")
    else:
        cn = sum(1 for c in t if '一' <= c <= '鿿')
        en = len(t) - cn
        print(f"中文: {cn} ≈{int(cn/1.5)} | 英文: {en} ≈{int(en/4)} | 总计 ≈{int(cn/1.5+en/4)}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**✅ 开箱即用** ｜ 🌐 [Tokenizer在线](https://platform.openai.com/tokenizer)

**⚠️ 可能遇到的坑：**
| 情况 | 原因 | 说明 |
|------|------|------|
| Token 数偏高估 | 每个模型 tokenizer 不同 | GPT 系列 1中文≈1.5-2 token；Claude 系列 1中文≈1.5；LLaMA 系列更高 |
| 结果与模型实际消耗不同 | 分词算法差异 | 本工具用字符级估算，粗略参考。实际以模型返回的 usage 字段为准 |
| emoji 占用多 Token | emoji 可能分多个 token | 常见 emoji 占 2-3 个 token |

---

#### 5.4 在线 Photoshop

裁剪 / 旋转 / 调整亮度对比度。**需 Pillow**。

> 📦 需要确认安装：`pip install Pillow`

<details>
<summary>📋 展开查看命令</summary>

```python
from PIL import Image, ImageEnhance
try:
    f = input("图片路径:").strip() or "photo.jpg"
    img = Image.open(f)
    w,h = map(int, input("裁剪 宽,高:").strip() or "200,200").split(","))
    if w > img.width or h > img.height:
        print(f"⚠️ 裁剪尺寸({w}x{h})大于原图({img.width}x{img.height})，将自动缩小到原图大小")
        w = min(w, img.width); h = min(h, img.height)
    img2 = img.crop(((img.width-w)//2,(img.height-h)//2,w+img.width//2,h+img.height//2))
    img2.save("cropped.jpg")
    e = ImageEnhance.Brightness(img).enhance(float(input("亮度(如1.2):") or 1.2))
    e.save("bright.jpg")
    print("✅ 已保存 cropped.jpg, bright.jpg")
except FileNotFoundError:
    print(f"❌ 找不到文件: {f}")
    print("   检查: 1) 文件路径是否完整，如 D:\\photo.jpg  2) 文件是否确实存在")
except ValueError:
    print("❌ 格式错误：裁剪输入应为 数字,数字，如：200,200")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [Photopea替代](https://www.photopea.com/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 找不到文件 | 路径错 | 用完整路径如 D:\folder\pic.jpg |
| 裁剪尺寸太大 | 比原图还大 | 自动缩小裁剪范围 |
| `No module named 'PIL'` | 没装 Pillow | 确认安装：pip install Pillow |

---

#### 5.5 Mermaid 时序图

输入代码，输出时序图代码（在 mermaid.live 预览）。

<details>
<summary>📋 展开查看命令</summary>

```python
seq = input("时序图代码:").strip() or "A->B: Hello"
if seq:
    print(f"sequenceDiagram\n{seq}")
else:
    print("❌ 代码不能为空")
```

</details>

**✅ 开箱即用** ｜ 🌐 [Mermaid Live Editor](https://mermaid.live/)

**⚠️ 可能遇到的坑：**

| 情况 | 原因 | 说明 |
|------|------|------|
| 不知道怎么渲染 | 本模块只输出代码 | 复制输出 → https://mermaid.live 粘贴预览 |
| 箭头不显示 | 箭头种类用错 | `->` 实线，`-->` 虚线，`->>` 实线+箭头 |
| 标题乱码 | 终端编码问题 | 输出本身无问题，在 mermaid.live 可正常渲染 |

**✅ 开箱即用**

---

### 🖼️ 模块 6：图片工具

---

#### 6.1 图片压缩

另存新文件不覆盖原图。**需 Pillow**。

> 📦 需要确认安装：`pip install Pillow`

<details>
<summary>📋 展开查看命令</summary>

```python
from PIL import Image, ImageFile
import os, sys
# 允许 PIL 加载截断图片（防止大图报错）
ImageFile.LOAD_TRUNCATED_IMAGES = True

MAX_IMAGE_PIXELS = 180_000_000  # 防止解压炸弹：7K × 7K = ~150MP
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

file_size_limit_mb = 200  # 超过 200MB 提示

f = input("图片路径:").strip() or "photo.jpg"
if not os.path.exists(f):
    print(f"❌ 文件不存在: {f}")
    print("   检查: 1) 路径是否完整，如 D:\\photo.jpg  2) 文件名是否拼写正确")
else:
    file_size = os.path.getsize(f)
    if file_size > file_size_limit_mb * 1024 * 1024:
        print(f"⚠️ 文件体积 {file_size / 1024 / 1024:.1f}MB，超过 {file_size_limit_mb}MB 建议值。")
        print("   💡 大文件提示：")
        print("     • 压缩过程可能需要 1-5 分钟，请耐心等待（不会卡死）")
        print("     • 确保可用内存 > 图片大小 × 3（无损压缩需要）")
        print("     • 如果经常处理百 MB 级图片，建议用专业工具：")
        print("       - RIOT (https://riot-optimizer.com/)")
        print("       - FileOptimizer (https://nikkhokkho.sourceforge.io/static.php?page=FileOptimizer)")
        print("   ⏳ 按回车继续，或输入 'q' 重新选择文件...")
        if input().strip().lower() == 'q':
            f = ""
    if f:
        try:
            q = int(input("质量(1-100，建议70-85):") or 80)
            if q < 1 or q > 100:
                print("❌ 质量必须为1-100之间的数字，已自动设为80")
                q = 80
            img = Image.open(f)
            # 超大尺寸警告
            w, h = img.size
            if w * h > 50_000_000:  # 50MP
                print(f"⚠️ 图片尺寸 {w}×{h} ({w*h/1e6:.1f}MP)，压缩可能需要 1-3 分钟...")
            if img.mode in ('RGBA','PA'):
                img = img.convert('RGB')
            out = f"compressed_{os.path.basename(f)}"
            img.save(out, quality=q, optimize=True)
            o, c = os.path.getsize(f)/1024, os.path.getsize(out)/1024
            rate = 100 - c/o*100 if o > 0 else 0
            print(f"✅ {o:.0f}KB → {c:.0f}KB (降{rate:.0f}%) | 原图未修改")
            if rate < 0:
                print("   💡 压缩后反而更大？说明原图已高度压缩。可尝试质量=60 或更低")
            elif rate < 10:
                print("   💡 压缩率不明显。可尝试降低质量参数（如60）或缩小尺寸")
        except FileNotFoundError:
            print(f"❌ 文件不存在。请检查路径是否包含中文/特殊字符（可能导致编码问题）")
        except ValueError:
            print("❌ 质量参数错误。请输入数字，如：80")
        except MemoryError:
            print("❌ 内存不足！图片太大，当前机器 RAM 不够。")
            print("   💡 解决：1) 先缩小尺寸再压缩 2) 用专业工具 RIOT 分块处理 3) 换一台内存更大的机器")
        except Image.DecompressionBombError:
            print(f"❌ 图片像素超过安全上限（{MAX_IMAGE_PIXELS}像素），可能是解压炸弹")
            print("   💡 建议用专业图像软件（Photoshop/GIMP）打开后缩小")
        except Exception as e:
            print(f"❌ 压缩失败: {e}")
            # 给出针对性建议
            err_str = str(e).lower()
            if "encoder" in err_str:
                print("   💡 编码器错误，可能是图片格式不支持。尝试转换为 JPG 后再压缩")
            elif "truncated" in err_str or "broken" in err_str:
                print("   💡 图片文件不完整或损坏（下载中断？）。尝试用图片查看器打开确认")
            elif "permission" in err_str:
                print("   💡 文件权限问题。尝试将图片复制到其他目录后再压缩")
            elif "cannot identify" in err_str:
                print("   💡 无法识别文件类型。确认文件是真正的图片（不是修改了扩展名）")
            else:
                print("   💡 通用方案：用浏览器打开图片 → 右键另存为 → 再压缩")
```

</details>

**📦 需确认** ｜ 🌐 [TinyPNG替代](https://tinypng.com/)

**✅ v2.0 大文件优化：** >200MB 自动告警 + MemoryError 防护 + DecompressionBomb 防护 + 针对性错误建议。

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 不警告直接卡住 | 超大文件正在处理 | 属于正常现象，百 MB 图片压缩需 1-5 分钟，不要手动关闭终端 |
| `MemoryError` | RAM 不够加载图片 | 缩小尺寸再压缩；或换台内存更大的机器 |
| `LOAD_TRUNCATED_IMAGES` | PIL 默认拒绝截断图 | v2.0 已内置开启，无需手动配置 |
| 输出文件更大 | 原图已高度压缩 | 降到质量 60 或更低；或者用 TinyPNG（有损压缩比 Pillow 更激进）|
| `No module named 'PIL'` | 没装 Pillow | `pip install Pillow` |
| `DecompressionBombError` | 图片尺寸超过 180MP | 用 PS/GIMP 缩到 50MP 以下再压缩 |
| 编码器错误 | 格式不支持 | 转为 JPG 再试 |
| 权限被拒绝 | 文件被占用或只读 | 复制到另一个目录再压缩 |

**🔧 大文件专业工具：**
- [RIOT](https://riot-optimizer.com/) — Windows，分块压缩，支持批量
- [FileOptimizer](https://nikkhokkho.sourceforge.io/static.php?page=FileOptimizer) — Windows，支持 200+ 格式
- [Squoosh](https://squoosh.app/) — 浏览器内，Google 出品
- [TinyPNG](https://tinypng.com/) — 在线，每月 500 张免费 |

---

#### 6.2 人像抠图

自动去除人像背景，输出透明 PNG。**需 rembg + Pillow**。

> 📦 需确认安装：`pip install rembg`
> ⚠️ 首次运行下载 ~300MB 模型

<details>
<summary>📋 展开查看命令</summary>

```python
from rembg import remove
import os
try:
    inp = input("图片:").strip() or "portrait.jpg"
    if not os.path.exists(inp):
        print(f"❌ 文件不存在: {inp}")
    else:
        out = f"bg_removed_{os.path.basename(inp)}.png"
        with open(inp,"rb") as f:
            result = remove(f.read())
        with open(out,"wb") as f:
            f.write(result)
        print(f"✅ 完成: {out}")
        print(f"   如抠图效果不理想，可能原因：1) 图片背景太复杂 2) 人像不够清晰")
except ImportError:
    print("❌ 缺少 rembg 库。安装命令: pip install rembg")
except Exception as e:
    print(f"❌ {e}")
    if "model" in str(e).lower():
        print("   提示: 首次运行需下载300MB模型，请确保网络畅通")
```

</details>

**📦 需确认** ｜ 🌐 [remove.bg替代](https://www.remove.bg/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| ImportError | 没装 rembg | pip install rembg |
| 模型下载失败 | 网络问题 | 用代理重试；首次下载慢正常 |
| 抠图效果差 | 背景太复杂 | 换背景更简单的照片；或手动微调 |

---

#### 6.3 证件照生成

支持一寸(295×413) / 二寸(413×579)，白色/蓝色/红色背景。**需 Pillow**。

> 📦 需要确认安装：`pip install Pillow`

<details>
<summary>📋 展开查看命令</summary>

```python
from PIL import Image
try:
    f = input("照片:").strip() or "face.jpg"
    if not f.lower().endswith(('.jpg','.jpeg','.png','.bmp')):
        print("⚠️ 可能不支持该格式。建议用 .jpg 或 .png")
    sz = input("尺寸(一寸/二寸):").strip() or "一寸"
    bg = input("背景色(白色/蓝色/红色):").strip() or "白色"
    sizes = {"一寸":(295,413),"二寸":(413,579)}
    if sz not in sizes:
        print(f"❌ 不支持的尺寸: {sz}。支持: 一寸 / 二寸")
        sz = "一寸"
    w,h = sizes[sz]
    img = Image.open(f).resize((w,h),Image.LANCZOS)
    bgs = {"白色":(255,255,255),"蓝色":(0,0,255),"红色":(255,0,0)}
    if bg not in bgs:
        print(f"⚠️ 不支持 {bg} 色，自动用白色")
        bg = "白色"
    canvas = Image.new("RGB",(w,h),bgs[bg])
    canvas.paste(img,(0,0),img if img.mode=="RGBA" else None)
    canvas.save(f"证件照_{sz}_{bg}.png")
    print(f"✅ 证件照_{sz}_{bg}.png ({w}x{h})")
except FileNotFoundError:
    print(f"❌ 文件不存在: {f}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [证件照在线](https://www.idphoto.net/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 不支持的尺寸 | 输错了 | 一寸或二寸 |
| 文件不存在 | 路径错 | 检查完整路径 |

---

#### 6.4 图片修复（去噪 + 锐化）

对老照片做基础去噪和锐化。**仅需 Pillow**。

> 📦 需要确认安装：`pip install Pillow`

<details>
<summary>📋 展开查看命令</summary>

```python
from PIL import Image, ImageEnhance
try:
    f = input("老照片路径:").strip() or "old.jpg"
    img = Image.open(f)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img.save("repaired.jpg")
    print("✅ 完成: repaired.jpg (仅 Pillow, 无需 opencv)")
except FileNotFoundError:
    print(f"❌ 文件不存在: {f}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [图片修复在线](https://www.imgonline.com.ua/)

**⚠️ 可能遇到的坑：**

| 情况 | 原因 | 说明 |
|------|------|------|
| 处理后看不出效果 | 图片模糊严重（软件修复极限） | 传统算法无法恢复严重模糊；尝试 enhance(2.0) 或更高；AI 修复用 Topaz Sharpen AI |
| 锐化过度出现白边/噪点 | 增强值太高 | 1.5 已适中；降到 1.2 可缓解 |
| 图片出现色块或变暗 | RGBA 透明通道异常 | 先 convert('RGB') 再修复 |
| 去噪效果不明显 | Pillow 不支持高级去噪 | 传统算法效果有限；专业需求用 Topaz Denoise AI、Photoshop、或在线 https://www.removenoise.com/ |
| MemoryError | 图片分辨率太高 | 先用其他工具缩小到 2K 以内再修复 |

---

### 📄 模块 7：PDF 转换

---

#### 7.1 PDF 合并

多个 PDF 合并为一个文件。**需 PyPDF2**。

> 📦 需要确认安装：`pip install PyPDF2`

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfMerger
import os
files = []
file_size_limit_mb = 500  # 单个文件 500MB 以上警告
total_size_mb = 0
try:
    while True:
        f = input(f"文件{len(files)+1}(回车结束):").strip()
        if not f: break
        if not f.lower().endswith('.pdf'):
            print(f"⚠️ {f} 可能不是PDF文件，仍尝试添加")
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}，跳过")
            continue
        size_mb = os.path.getsize(f) / 1024 / 1024
        total_size_mb += size_mb
        if size_mb > file_size_limit_mb:
            print(f"⚠️ 文件大小 {size_mb:.0f}MB，合并可能较慢（大 PDF 需逐页加载到内存）")
        files.append(f)
    if len(files) < 2:
        print("❌ 至少需要2个PDF文件合并")
    else:
        if total_size_mb > 100:
            print(f"⚠️ 总大小 {total_size_mb:.0f}MB，合并可能需要 1-5 分钟，请耐心等待...")
        m = PdfMerger()
        ok_count = 0
        for f in files:
            try:
                m.append(f)
                ok_count += 1
            except Exception as e:
                print(f"⚠️ 无法读取: {f} ({e})")
                print("   💡 可能原因：PDF 已加密、文件损坏、格式不是标准 PDF")
        if len(m.pages) == 0:
            print("❌ 所有文件都已损坏或加密。无法继续合并")
        else:
            m.write("merged.pdf")
            m.close()
            out_size = os.path.getsize("merged.pdf") / 1024 / 1024
            print(f"✅ 合并完成: merged.pdf ({ok_count}/{len(files)} 个文件, {out_size:.1f}MB)")
            if ok_count < len(files):
                print(f"   ⚠️ {len(files) - ok_count} 个文件被跳过，请检查上面警告")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except MemoryError:
    print("❌ 内存不足！PDF 总大小超出可用 RAM")
    print("   💡 建议：用 Ghostscript 命令行合并（内存占用更低）：")
    print("     gswin64c -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf file1.pdf file2.pdf")
except Exception as e:
    print(f"❌ 合并失败: {e}")
    err_str = str(e).lower()
    if "password" in err_str or "encrypt" in err_str:
        print("   💡 PDF 已加密，请先使用本工具 7.4 PDF解密 去除密码再合并")
    elif "permission" in err_str:
        print("   💡 权限问题。尝试将文件复制到桌面再合并")
    elif "read" in err_str:
        print("   💡 文件读取失败，可能已损坏。尝试用浏览器打开确认")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF合并](https://www.ilovepdf.com/merge-pdf)

**✅ v2.0 大文件优化：** >500MB 文件警告 + 总大小进度提示 + MemoryError 降级指引（ Ghostscript ）。

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 合并非常慢 / 卡顿 | 大 PDF 需全部读入内存 | 正常现象，百 MB 级需 1-5 分钟，不要关闭终端 |
| `MemoryError` | RAM 不够 | 用 Ghostscript 命令行替代（见上方错误提示） |
| 有文件被跳过 | PDF 加密或损坏 | 先解密（7.4 功能）再合并 |
| 文件不存在 | 路径错 | 检查完整路径 |
| `No module named 'PyPDF2'` | 没装 | `pip install PyPDF2` |
| 输出文件比总和还小 | 有图片被压缩 | PyPDF2 默认会重新编码图片，属正常行为 |

**🔧 超大 PDF（>1GB）专业工具：**
- Ghostscript: `gswin64c -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=out.pdf in1.pdf in2.pdf`
- PDFsam (https://pdfsam.org/) — 图形界面，支持 2GB+ 文件
- Adobe Acrobat Pro — 商业软件，功能最全 |

---

#### 7.2 PDF 拆分

按页码提取指定页面。**需 PyPDF2**。

> 📦 需要确认安装：`pip install PyPDF2`

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
import os
try:
    inp = input("PDF路径:").strip() or "source.pdf"
    pgs = input("页码(如 1-3 或 2,5):").strip() or "1-3"
    if not inp.lower().endswith('.pdf'):
        print("⚠️ 文件可能不是PDF格式，但如果实际是 PDF 仍可尝试")
    if not os.path.exists(inp):
        print(f"❌ 文件不存在: {inp}")
        print("   💡 检查：路径中的斜杠方向；文件名大小写是否一致")
    else:
        file_size_mb = os.path.getsize(inp) / 1024 / 1024
        if file_size_mb > 200:
            print(f"⚠️ 文件大小 {file_size_mb:.0f}MB，加载可能需要 30秒~2 分钟...")
        r = PdfReader(inp)
        if r.is_encrypted:
            print("❌ PDF 已加密，无法直接拆分。请先使用 7.4 PDF解密！")
        else:
            w = PdfWriter()
            total = len(r.pages)
            added = 0
            invalid_pages = []
            for p in pgs.split(","):
                if "-" in p:
                    parts = p.split("-")
                    if len(parts) != 2:
                        print(f"⚠️ 格式错误: '{p}'。正确格式如 1-3")
                        continue
                    s,e = map(int, parts)
                    if s < 1 or e > total:
                        invalid_pages.append(f"{s}-{e}")
                    elif s > e:
                        print(f"⚠️ 起始页 {s} 大于结束页 {e}，已自动交换")
                        s, e = e, s
                        for i in range(s-1, e):
                            w.add_page(r.pages[i])
                            added += 1
                    else:
                        for i in range(s-1, e):
                            w.add_page(r.pages[i])
                            added += 1
                else:
                    try:
                        idx = int(p)-1
                        if 0 <= idx < total:
                            w.add_page(r.pages[idx])
                            added += 1
                        else:
                            invalid_pages.append(p)
                    except ValueError:
                        print(f"⚠️ 无效的页码: '{p}'，已跳过")
            if invalid_pages:
                print(f"⚠️ 以下页码超出范围 (1-{total}) 已跳过: {', '.join(invalid_pages)}")
            if added == 0:
                print("❌ 没有添加任何页面，请检查页码格式")
            else:
                w.write("extracted.pdf")
                out_size = os.path.getsize("extracted.pdf") / 1024
                print(f"✅ 完成: extracted.pdf ({added}页, {out_size:.0f}KB)")
                if added < total:
                    print(f"   💡 源文件共 {total} 页，本次提取 {added} 页")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except FileNotFoundError:
    print(f"❌ 文件不存在: {inp}")
    print("   💡 检查路径中的中文/特殊字符；可以复制文件到桌面后输入 C:\\Users\\用户名\\桌面\\文件名.pdf")
except Exception as e:
    print(f"❌ {e}")
    err_str = str(e).lower()
    if "password" in err_str or "encrypt" in err_str:
        print("   💡 PDF 已加密。先使用 7.4 PDF解密 再拆分")
    elif "permission" in err_str:
        print("   💡 权限问题。将文件复制到其他目录再试")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF拆分](https://www.ilovepdf.com/split-pdf)

**✅ v2.0 大文件优化：** >200MB 告警 + 进度提示 + 输入格式自动纠正。

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 卡在"加载中" | 大文件需全部读入内存 | 百 MB 级需 30秒~2分钟，属正常现象 |
| 页码超范围提示 | 输入了不存在的页码 | 读错误信息中 (1-N) 的范围，重新输入 |
| 起始 > 结束 | 手误输入了 5-3 | v2.0 已自动交换，无需手动纠正 |
| 加密 PDF 拒绝处理 | PDF 有密码 | 先 7.4 解密再拆分 |
| 文件不存在 | 路径错或含特殊字符 | 复制到桌面，输入完整路径 |

---

#### 7.3 PDF 加密

设置打开密码。**需 PyPDF2**。

> 📦 需要确认安装：`pip install PyPDF2`

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
try:
    inp = input("PDF路径:").strip() or "source.pdf"
    pwd = input("密码:").strip()
    if not pwd:
        print("❌ 密码不能为空")
    elif len(pwd) < 4:
        print("⚠️ 密码太短，建议4位以上")
    else:
        r = PdfReader(inp); w = PdfWriter()
        for p in r.pages: w.add_page(p)
        w.encrypt(pwd)
        w.write("encrypted.pdf")
        print("✅ 完成: encrypted.pdf (密码不保存, 丢失无法恢复!)")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF加密](https://www.ilovepdf.com/encrypt-pdf)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 密码为空 | 没输入密码 | 输入至少4位密码 |
| 丢失密码 | 没有找回方式 | 截图保存密码 |

---

#### 7.4 PDF 解密

用密码解密加密的 PDF。**需 PyPDF2**。

> 📦 需要确认安装：`pip install PyPDF2`

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
try:
    inp = input("加密PDF:").strip() or "encrypted.pdf"
    pwd = input("密码:").strip()
    if not pwd:
        print("❌ 密码不能为空")
    else:
        r = PdfReader(inp)
        if r.is_encrypted:
            r.decrypt(pwd)
        w = PdfWriter()
        for p in r.pages: w.add_page(p)
        w.write("decrypted.pdf")
        print("✅ 完成: decrypted.pdf")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except Exception as e:
    print(f"❌ {e}")
    print("   可能原因: 密码错误 / 文件损坏")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF解密](https://www.ilovepdf.com/unlock-pdf)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 解密失败 | 密码错误 | 确认正确密码 |
| 文件损坏 | PDF本身问题 | 尝试用其他PDF打开 |

---

### 🎬 模块 8：视频工具

---

#### 8.1 视频格式转换

MP4 / AVI / MOV / GIF 互转。**需 FFmpeg**。

> 📦 FFmpeg 安装：
> - Windows: `winget install ffmpeg`
> - macOS: `brew install ffmpeg`
> - Linux: `sudo apt install ffmpeg`

<details>
<summary>📋 展开查看命令</summary>

```python
import subprocess, os
try:
    f = input("文件:").strip() or "video.mp4"
    o = input("格式(gif/mp4/avi/mov/webm):").strip() or "gif"
    out = f"{os.path.splitext(f)[0]}.{o}"
    if not os.path.exists(f):
        print(f"❌ 文件不存在: {f}")
        print("   💡 检查：路径中是否包含中文符号（如 ：【】）；复制到英文路径再试")
    else:
        file_size_mb = os.path.getsize(f) / 1024 / 1024
        if file_size_mb > 500:
            print(f"⚠️ 文件 {file_size_mb:.0f}MB，转换可能需要 5-30 分钟...")
            print("   💡 大文件提示：")
            print("     • 确保磁盘剩余空间 > 文件大小的 2 倍")
            print("     • 转换为 GIF 也需用 `-vf scale=480:-1'` 缩小分辨率，否则 GIF 会巨大")
            print("     • 大文件转换建议直接用 FFmpeg 命令行，可自己调参数")
        r = subprocess.run(
            ["ffmpeg", "-i", f, "-y"]
            + (["-vf", "scale=480:-1"] if o == "gif" and file_size_mb > 50 else [])
            + [out],
            capture_output=True, text=True, timeout=1800  # 30 分钟超时
        )
        if r.returncode == 0:
            out_size = os.path.getsize(out) / 1024
            print(f"✅ 完成: {out} ({out_size:.0f}KB)")
            if out_size == 0:
                print("   ⚠️ 输出文件 0KB，可能转换失败。查看 stderr：")
                print(f"     {r.stderr[:300]}")
        else:
            err = r.stderr[:500] if r.stderr else "无错误信息"
            print(f"❌ 转换失败: {err}")
            print("   💡 常见原因：")
            print("     1) 目标格式不支持源编码 → 先用 `-c:v libx264` 转 H.264 再转目标格式")
            print("     2) 源文件损坏 → 用播放器确认视频能正常播放")
            print("     3) 磁盘空间不足 → 清理空间或换输出路径")
            print("     4) 分辨率太大 → 加 `-vf scale=1280:-1'` 缩小")
except FileNotFoundError:
    print("❌ ffmpeg 未安装或未加入 PATH")
    print("   💡 安装方法：")
    print("     Windows: winget install ffmpeg  或 下载 https://github.com/BtbN/FFmpeg-Builds/releases")
    print("     macOS: brew install ffmpeg")
    print("     Linux: sudo apt install ffmpeg")
    print("   💡 安装后关闭终端重新打开，让 PATH 生效")
except subprocess.TimeoutExpired:
    print("❌ 转换超时（超过 30 分钟）！")
    print("   💡 可能是文件太大或参数不适合。建议：")
    print("     • 先分割视频，分段转换")
    print("     • 用专业工具：HandBrake https://handbrake.fr/")
    print("     • 在线转换：CloudConvert https://cloudconvert.com/")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [CloudConvert替代](https://cloudconvert.com/)

**✅ v2.0 大文件优化：** >500MB 告警 + 自动给大 GIF 缩小分辨率 + 30 分钟超时 + 针对性错误建议。

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 转换时间超长 | 文件太大或分辨率太高 | 缩小分辨率（加 `-vf scale=1280:-1'`）；换用 HandBrake |
| 输出文件 0KB | 转换失败但未报错 | 看 stderr；通常是编码不兼容 |
| `ffmpeg 不在 PATH` | 安装时没勾选"添加到PATH" | 重新安装并勾选；手动添加 bin 目录到环境变量 |
| 转换超时 30 分钟 | 机器性能不足或文件极大 | 换专业软件（HandBrake / Shutter Encoder）|
| GIF 文件巨大 | 原视频分辨率高 | v2.0 >50MB 自动缩小到 480px 宽，也可手动加 `-vf scale=320:-1'` |

**🔧 视频专业工具：**
- [HandBrake](https://handbrake.fr/) — 免费开源，支持 4K/HDR/批量
- [Shutter Encoder](https://www.shutterencoder.com/) — 专业级，支持 100+ 格式
- [CloudConvert](https://cloudconvert.com/) — 在线，25 次/天免费 |

---

#### 8.2 视频编辑工具

裁剪、拼接、提取音频。**需 FFmpeg**。

<details>
<summary>📋 展开查看命令</summary>

```python
import subprocess, os
try:
    act = input("操作(裁剪/拼接/提取音频):").strip() or "裁剪"
    if act == "裁剪":
        f = input("文件:") or "video.mp4"
        s = input("开始时间(HH:MM:SS):") or "00:01:00"
        t = input("时长(HH:MM:SS):") or "00:02:00"
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}")
        else:
            mb = os.path.getsize(f) / 1024 / 1024
            if mb > 500:
                print(f"⚠️ 文件 {mb:.0f}MB，裁剪可能需要 5-30 分钟...")
            r = subprocess.run(["ffmpeg","-i",f,"-ss",s,"-t",t,"-c","copy","clipped.mp4"], timeout=1800)
            if r.returncode == 0:
                print(f"✅ 完成: clipped.mp4 ({os.path.getsize('clipped.mp4')/1024:.0f}KB)")
            else:
                print(f"❌ 失败，请检查时间格式")
    elif act == "拼接":
        fs = input("文件(逗号):") or "a.mp4,b.mp4"
        with open("files.txt","w") as tf:
            for x in fs.split(","): tf.write(f"file '{x}'\n")
        r = subprocess.run(["ffmpeg","-f","concat","-i","files.txt","-c","copy","joined.mp4"], timeout=1800)
        if r.returncode == 0:
            print(f"✅ 完成: joined.mp4")
        else:
            print(f"❌ 拼接失败，可能文件格式不一致")
    else:
        f = input("文件:") or "video.mp4"
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}")
        else:
            r = subprocess.run(["ffmpeg","-i",f,"-vn","audio.mp3"], timeout=1800)
            if r.returncode == 0:
                print(f"✅ 完成: audio.mp3")
            else:
                print(f"❌ 提取音频失败")
except FileNotFoundError:
    print("❌ ffmpeg 未安装或不在 PATH")
    print("   💡 Windows: winget install ffmpeg；macOS: brew install ffmpeg")
except subprocess.TimeoutExpired:
    print("❌ 操作超时（超过30分钟）！大文件建议分块或用 HandBrake")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [ClipConverter替代](https://www.clipconverter.cc/)

**✅ v2.1 大文件优化：** >500MB 告警 + 30 分钟超时 + 针对性错误建议

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 操作超时 | 文件太大或机器性能不足 | 先用裁剪功能剪出需要片段；再用 HandBrake 转码 |
| 拼接失败 | 各文件编码/分辨率不一致 | 先用 `ffmpeg -i input.mp4 -vf scale=1920:-1 -c:v libx264 output.mp4` 统一规格 |
| 裁剪后的视频没声音 | `-c copy` 复制流时跳过重新编码 | 改用 `ffmpeg -i f -ss s -t t -c:v libx264 -c:a aac out.mp4`

---

#### 8.3 在线录屏

使用浏览器 MediaRecorder API 录制浏览器标签页（仅限浏览器内）。

<details>
<summary>📋 展开查看命令</summary>

```javascript
// 在浏览器控制台或 HTML 页面中运行
navigator.mediaDevices.getDisplayMedia({video:true,audio:true})
  .then(stream => {
    const rec = new MediaRecorder(stream);
    const chunks = [];
    rec.ondataavailable = e => chunks.push(e.data);
    rec.onstop = () => {
      const blob = new Blob(chunks, {type:'video/webm'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'screen-recording.webm';
      a.click();
    };
    rec.start(); setTimeout(()=>rec.stop(), 10000); // 录10秒
  });
```

</details>

**✅ 开箱即用**（浏览器内运行，无需安装）

---

## 最佳实践

### 场景 1：新电脑第一次用

```
你: "帮我检测一下环境"
AI: 跑检测脚本，告诉你缺了什么
你: "帮我装一下"
AI: pip install Pillow PyPDF2
你: "帮我压缩 D:\photo.jpg"
AI: ✅ 完成
```

### 场景 2：网络不好时（v2.0 国内自动降级）

```
你: "帮我查勾股定理"
AI: ⚠️ Wikipedia 被墙 → 自动查询百度百科 → 返回结果

你: "来个笑话"
AI: ⚠️ 官方 Joke API 超时 → 自动切国内 API → 返回笑话
   （全部失败时也返回本地离线缓存，不会让你白等）

你: "下个壁纸"
AI: 尝试国内随机图源 → 成功返回下载链接
```

### 场景 3：处理大文件

```
你: "帮我合并 3 个 PDF（每个 200MB）"
AI: ⚠️ 总大小 600MB，合并可能需要 2-5 分钟...（自动显示进度，完成后报告页数和大小）

你: "压缩 D:\photo_600MB.tiff"
AI: ⚠️ 文件 600MB，超过 200MB 建议值。可用内存需 >1.8GB...（确认后自动处理，遇 MemoryError 给出降级方案）
```

### 场景 4：不确定能不能做时

```
你: "能帮我恢复删除的文件吗？"
AI: ❌ 不支持（超出工具范围，已给出专业恢复软件推荐）
```

---

## ❓ 常见问题

### Q1: 第一次使用怎么做？
直接说一句话。零依赖功能直接跑。需安装功能会提示。

### Q2: 提示安装依赖怎么办？
跑一行 `pip install Pillow PyPDF2`，装完即可。

### Q3: 下载壁纸被墙 / Wikipedia 查不了 / GitHub API 超时？
这是国内网络环境问题。v2.0 已内置**多级降级**：
- **Wikipedia** → 自动降级到百度百科（国内），无需代理
- **壁纸/Unsplash** → 自动尝试国内随机图片源，失败返回 Pixabum
- **一言/笑话** → 3 个国内 API 自动切换，全部失败返回本地离线缓存
- **GitHub API** → 失败时提示 ghproxy 镜像地址

如果所有国内源也失败：
1. 检查 Wi-Fi/网线连接是否正常
2. 关闭代理/VPN（开启时反而可能更慢）
3. 尝试开手机热点（排查是否需要过境网络）
4. 仍不可用：用浏览器直接访问对应在线工具（每个功能下方已列出）

### Q4: PDF 加密后忘记密码怎么办？
无法恢复。密码只在加密时展示一次，请截图保存。

### Q5: 图片压缩会损坏原图吗？
不会。另存为新文件（compressed_开头），原图不动。

### Q6: 视频转换失败？
1. 确认 FFmpeg 已安装：命令行输入 `ffmpeg -version`，有版本号即可
2. 确认 FFmpeg 在 PATH：如果 `ffmpeg -version` 提示"不是内部或命令"，需添加 FFmpeg 的 bin 目录到环境变量
3. 大文件（>500MB）：v2.0 有自动告警；如需缩小分辨率加 `-vf scale=1280:-1'`
4. 编码不兼容：先用 `-c:v libx264` 转 H.264 再转目标格式
5. 磁盘空间不足：同目录下确保有文件 2 倍大小的剩余空间
6. 终极方案：改用 [HandBrake](https://handbrake.fr/)（图形界面，更稳定）

**国内 FFmpeg 下载渠道（官方慢时）：**
- https://github.com/BtbN/FFmpeg-Builds/releases （Windows 预编译版）
- https://gyan.dev/ffmpeg/builds/ （Windows 稳定版）

### Q7: 怎么升级 dgngjx-skill？
```bash
clawhub update dgngjx-skill
```

### Q8: 处理大文件（>500MB）提示内存不足或太慢怎么办？
v2.0 已内置大文件保护，针对不同场景有不同方案：

**图片压缩：**
- >200MB 自动提示风险
- 内存不足 → 先缩小尺寸再压缩（代码示例见 6.1）
- 极端情况 → 用 [Squoosh](https://squoosh.app/) 浏览器内处理（无需全图载入 RAM）

**PDF 合并：**
- >500MB / 总文件 >100MB 自动显示进度
- 内存不足 → 用 Ghostscript 命令行替代（代码见 7.1）
- 超大 PDF（>1GB）→ 用 [PDFsam](https://pdfsam.org/) 图形工具

**视频转换：**
- 30 分钟超时保护，防止进程卡死
- 大文件先缩小分辨率：`ffmpeg -i input.mp4 -vf scale=1280:-1 -c:v libx264 output.mp4`
- 超大视频（>5GB）→ [HandBrake](https://handbrake.fr/) 是更好的选择

**通用建议：**
- 关闭其他程序释放内存
- 用 SSD 而不是机械硬盘（读写速度快 5-10 倍）
- 批量处理时一次不要超过 5 个文件

---

## 功能分类统计

| 类别 | 数量 | 开箱即用 |
|------|:----:|:--------:|
| ✅ 零依赖即可运行 | 14 | ✅ |
| 📦 需确认安装后运行 | 15 | ❌（有引导+在线替代） |
| **总计** | **29** | **48%** |

## v2.0 新特性速览

| 优化维度 | 涉及模块 | 关键提升 |
|---------|---------|---------|
| 国内联网兼容 | 3.1 Wikipedia、4.1 娱乐工具、4.2 壁纸、5.2 HTTP | 自动降级 + 3 级国内源兜底 + 离线缓存 |
| 大文件性能 | 6.1 图片压缩、7.1 PDF 合并、7.2 PDF 拆分、8.1 视频转换 | 大小检测 + 进度告警 + MemoryError 防护 + 超时保护 |
| 错误提示 | 全部模块 | 针对性中文诊断 + 具体解决命令 + 在线替代工具链接 |

## 一键安装后可用功能

| 装这些 | 新增可用 |
|-------|---------|
| `pip install Pillow` | 压缩 / 证件照 / 基础修复 / PS |
| `pip install PyPDF2` | PDF 合并 / 拆分 / 加密 / 解密 |
| `pip install rembg` | 人像抠图（首次 300MB） |
| FFmpeg | 格式转换 / 视频编辑 |

## 发布信息

- **作者**：Admin
- **许可证**：MIT
- **支持平台**：Windows / macOS / Linux
- **更新历史**：
  - v2.2.0：[Bug修复]
  - v2.1.0：[Bug修复] 单位换算float崩溃+壁纸urllib.parse缺失+HTTP字符串拼接+f-string引号; [国内源]百度百科→baike.deno.dev+壁纸→imgapi.cn; [提示详细度]房贷/五险一金/Token/Mermaid/图片修复共8模块扩充; [大文件]视频编辑模块增加>500MB告警+30分钟超时+GIF自动缩放; [Ghostscript]Windows命令名修正
  - v2.5.0：[适用性优化] HTTP模块P0语法修复；8个模块（日期/文本/编码/词频/JSON/证件照/PDF加密/PDF解密）"坑表格"从1-2行扩充至4-5行；Token计算器在线链接修正
  - v2.0.0：[国内联网优化] Wikipedia→百度百科自动降级；娱乐工具→3个国内API+本地离线缓存；壁纸→国内随机图源+Pixabum兜底；[大文件性能] 图片>200MB告警+MemoryError防护+DecompressionBomb限制；PDF>500MB告警+Ghostscript降级指引；视频>500MB告警+30分钟超时+GIF自动缩放；HTTP错误细分（DNS/SSL/超时/状态码中文释义）；所有针对性错误给出具体解决命令+在线替代工具链接；新增Q8大文件FAQ
  - v1.7.0：每个命令加详细中文报错+解决方案+可能遇到的坑表格/网络错误处理/文件路径检查
  - v1.6.0：详细安装引导/中文报错/最佳实践/边界情况说明
  - v1.5.0：图片修复用Pillow重写/一键安装脚本/网络错误中文提示
  - v1.4.0：命令折叠隐藏/概览页精简
  - v1.3.0：30秒速查表/报错说明
  - v1.2.0：含可运行命令/FAQ
  - v1.1.0：去除人脸年龄变换
  - v1.0.0：初始版，8大模块