---
name: dgngjx-skill
description: "多功能免费工具箱 - 图片处理、PDF转换、数据换算、文本工具、开发工具、视频工具、教育、生活娱乐。48%零开箱即用，52%需确认安装。所有命令都有中文报错+解决方案+在线替代。"
---

# 多功能工具箱 dgngjx-skill v1.7.0

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
| 不支持的城市的报错 | 城市名不在列表内 | 四个城市输全称，不要输"广州市" |
| 个税收计算为0 | 收入减去社保后≤5000 | 正常，说明不用交个税 |

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
| `ValueError` | 格式不对 | 用英文横杠分隔：2026-6-26 |
| 结果负数 | 目标日期已经过去 | 正常，说明X天前 |

---

#### 1.4 单位换算器

```
输出: 100 公里 = 62.1371 英里
```

<details>
<summary>📋 展开查看命令</summary>

```python
c = {"km_mi":(.621371,"公里","英里"),"mi_km":(1/.621371,"英里","公里"),
     "c_f":(lambda x:x*9/5+32,"°C","°F"),"f_c":(lambda x:(x-32)*5/9,"°F","°C"),
     "kg_lb":(2.20462,"kg","lb"),"lb_kg":(1/2.20462,"lb","kg")}
try:
    m = input("类型:").strip() or "km_mi"
    v = float(input("数值: ") or 100)
    if m not in c:
        print(f"❌ 不支持的换算。从以下选一个：{', '.join(c.keys())}")
    else:
        r,uf,ut = c[m]
        print(f"{v} {uf} = {r(v):.4f} {ut}")
except ValueError:
    print("❌ 数值输入错误。请输入纯数字，例如：100")
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
| "没有检测到输入" | 运行时没输入任何文字 | 输入一段文字再运行 |

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
| 解码失败 | 输入了非Base64字符 | 解码前确认是标准Base64字符串 |
| 不识别的方法 | 输入了中文名 | 输英文：Base64 |

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
| 没有有效词 | 只有数字或符号 | 输入中文文章或英文段落 |

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
import urllib.request, urllib.parse, json
try:
    q = input("关键词:") or "勾股定理"
    if not q.strip():
        print("❌ 关键词不能为空。请输入要查询的内容，例如：勾股定理")
    else:
        url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(q)}&format=json&srlimit=3"
        req = urllib.request.Request(url, headers={"User-Agent":"dgngjx/1.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        results = data.get("query",{}).get("search",[])
        if not results:
            print(f"❌ 没有找到关于「{q}」的内容。换个关键词试试")
        for r in results:
            print(f"\n📖 {r['title']}\n   {r['snippet'].replace('<span class=searchmatch>','').replace('</span>','')[:200]}...")
except urllib.error.URLError:
    print("❌ 网络故障（Wikipedia 国内可能被墙）")
    print("   解决: 1) 检查网络连接 2) 用代理/VPN 3) 改用 https://www.baidu.com/s?wd=关键词")
except json.JSONDecodeError:
    print("❌ 返回数据异常，Wikipedia API 暂时不可用。请稍后重试或用其他网站")
except Exception as e:
    print(f"❌ 发生预料之外的错误: {e}")
```

</details>

**✅ 开箱即用** ｜ 🌐 [百度替代](https://www.baidu.com/s?wd=关键词)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 网络故障 | Wikipedia 被墙 | 用代理或 VPN；或改用百度链接 |
| 没有找到结果 | 关键词太冷门 | 换更常见的词 |
| JSON 解析失败 | 网站 API 挂了 | 稍后重试 |

---

### 🎮 模块 4：生活娱乐

---

#### 4.1 娱乐小工具

随机笑话 / 一言 / 运势。需要联网。

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, json
try:
    c = input("选择(1笑话/2一言/3运势):").strip() or "1"
    if c == "1":
        r=urllib.request.urlopen("https://official-joke-api.appspot.com/random_joke",timeout=5)
        d=json.loads(r.read()); print(f"{d['setup']}\n  {d['punchline']}")
    elif c == "2":
        r=urllib.request.urlopen("https://v1.hitokoto.cn/",timeout=5)
        d=json.loads(r.read()); print(f"{d['hitokoto']}\n —— {d.get('from','')}")
    elif c == "3":
        import random; print(random.choice(["大吉","中吉","小吉","吉","末吉","凶","大凶"]))
    else:
        print(f"❌ 选项 {c} 不存在。请输入 1、2 或 3")
except urllib.error.URLError:
    print("❌ 网络连接失败")
    print("   解决: 检查网络是否通畅；如果网络受限，可能是网站被墙")
except json.JSONDecodeError:
    print("❌ 服务器返回异常数据。请稍后重试")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**✅ 开箱即用**

---

#### 4.2 壁纸中心

从 Unsplash 下载壁纸。**国内可能被墙**。

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, json
try:
    k = input("关键词(英文):").strip() or "nature"
    if not k:
        print("❌ 关键词不能为空")
    else:
        url = f"https://api.unsplash.com/photos/random?query={k}&count=1"
        r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"dgngjx/1.0"}),timeout=10)
        d=json.loads(r.read())
        if d:
            print(f"📷 {d[0]['user']['name']}\n   下载: {d[0]['urls']['full']}")
        else:
            print("⚠️ 无结果（DEMO_KEY 可能过期）。去 https://unsplash.com 手动选")
except urllib.error.URLError:
    print("❌ 网络不通（Unsplash 国内可能被墙）")
    print("   解决: 用代理/VPN 或访问 https://unsplash.com/s/photos/" + k)
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
| JSON 错误 | 语法问题 | 检查：键有没有加引号、有没有多逗号 |

---

#### 5.2 HTTP 接口测试

```
输出: ✅ 状态码: 200 | 响应体(1256字符): {"current_user_url":"..."}
```

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request
try:
    u = input("URL:").strip() or "https://api.github.com"
    if not u:
        print("❌ URL不能为空")
    elif not u.startswith("http"):
        print("❌ URL格式不对。应以 http:// 或 https:// 开头，如 https://api.github.com")
    else:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"dgngjx/1.0"}),timeout=15)
        print(f"✅ 状态码: {r.status}\n({len(r.read())} bytes)")
except urllib.error.URLError as e:
    print(f"❌ 网络错误: {e.reason}")
    print("   解决: 1) 检查网络连接 2) URL是否正确 3) 网站可能需要代理")
except TimeoutError:
    print("❌ 请求超时（超过15秒）。网站可能太慢或网络太差，换个URL试试")
except ValueError:
    print("❌ URL格式不正确。请输完整的URL，包括 http:// 或 https://")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**✅ 开箱即用**

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 网络错误 | URL不通或没网 | 检查网络；URL是否有拼写错误 |
| 超时 | 网站响应太慢 | 换个响应快的网站测试 |
| URL格式错误 | 少了协议头 | 加上 https:// |

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

**✅ 开箱即用**

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

输入代码，输出时序图（由用户自行渲染）。

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
from PIL import Image
import os
try:
    f = input("图片路径:").strip() or "photo.jpg"
    if not os.path.exists(f):
        print(f"❌ 文件不存在: {f}")
        print("   检查: 路径是否正确，如 C:\\Users\\用户名\\photo.jpg")
    else:
        q = int(input("质量(1-100):") or 80)
        if q < 1 or q > 100:
            print("❌ 质量必须为1-100之间的数字，已自动设为80")
            q = 80
        img = Image.open(f)
        out = f"compressed_{os.path.basename(f)}"
        img.save(out, quality=q, optimize=True)
        o, c = os.path.getsize(f)/1024, os.path.getsize(out)/1024
        print(f"✅ {o:.0f}KB → {c:.0f}KB (降{100-c/o*100:.0f}%) | 原图未修改")
except FileNotFoundError:
    print(f"❌ 文件不存在。检查路径")
except ValueError:
    print("❌ 质量参数错误。请输入数字，如：80")
except Exception as e:
    print(f"❌ 压缩失败: {e}")
```

</details>

**📦 需确认** ｜ 🌐 [TinyPNG替代](https://tinypng.com/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 文件不存在 | 路径错 | 检查路径，用完整路径 |
| `No module named 'PIL'` | 未装 | pip install Pillow |
| 输出文件更大 | 原图已压缩 | 降低质量值（60或更低）|

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
files = []
try:
    while True:
        f = input(f"文件{len(files)+1}(回车结束):").strip()
        if not f: break
        if not f.lower().endswith('.pdf'):
            print(f"⚠️ {f} 可能不是PDF文件，仍尝试添加")
        if not __import__('os').path.exists(f):
            print(f"❌ 文件不存在: {f}，跳过")
            continue
        files.append(f)
    if len(files) < 2:
        print("❌ 至少需要2个PDF文件合并")
    else:
        m = PdfMerger()
        for f in files:
            try: m.append(f)
            except Exception as e: print(f"⚠️ 无法读取: {f} ({e})")
        if len(m.pages) == 0:
            print("❌ 所有文件都已损坏或加密。无法继续合并")
        else:
            m.write("merged.pdf"); m.close()
            print(f"✅ 合并完成: merged.pdf ({len(files)}个)")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF合并](https://www.ilovepdf.com/merge-pdf)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 文件不存在 | 路径错 | 检查文件位置 |
| 文件损坏或加密 | PDF本身问题 | 打开确认文件是否完整 |
| PyPDF2缺失 | 没装 | pip install PyPDF2 |
| 文件不是PDF | 扩展名不是.pdf | 重命名为.pdf或用工具转换 |

---

#### 7.2 PDF 拆分

按页码提取指定页面。**需 PyPDF2**。

> 📦 需要确认安装：`pip install PyPDF2`

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
try:
    inp = input("PDF路径:").strip() or "source.pdf"
    pgs = input("页码(如 1-3 或 2,5):").strip() or "1-3"
    if not inp.lower().endswith('.pdf'):
        print("⚠️ 文件可能不是PDF格式")
    if not __import__('os').path.exists(inp):
        print(f"❌ 文件不存在: {inp}")
    else:
        r = PdfReader(inp)
        w = PdfWriter()
        total = len(r.pages)
        for p in pgs.split(","):
            if "-" in p:
                s,e = map(int, p.split("-"))
                if s < 1 or e > total:
                    print(f"⚠️ 页码超范围 (1-{total})")
                else:
                    for i in range(s-1, e):
                        w.add_page(r.pages[i])
            else:
                idx = int(p)-1
                if 0 <= idx < total:
                    w.add_page(r.pages[idx])
        w.write("extracted.pdf")
        print(f"✅ 完成: extracted.pdf ({len(w.pages)}页)")
except ImportError:
    print("❌ 缺少 PyPDF2。安装: pip install PyPDF2")
except FileNotFoundError:
    print(f"❌ 文件不存在: {inp}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [iLovePDF拆分](https://www.ilovepdf.com/split-pdf)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| 页码超范围 | 输入了不存在的页码 | 检查PDF总页数 |
| 文件不存在 | 路径错 | 检查完整路径 |
| PyPDF2缺失 | 没装 | pip install PyPDF2 |

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
    r = subprocess.run(["ffmpeg","-i",f,"-y",out], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"✅ 完成: {out} ({os.path.getsize(out)/1024:.0f}KB)")
    else:
        print(f"❌ 转换失败: {r.stderr[:200]}")
        print("   可能原因: 格式不支持 / 编码问题")
except FileNotFoundError:
    print("❌ ffmpeg 未安装")
    print("   解决: 参考 https://ffmpeg.org/download.html")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [CloudConvert替代](https://cloudconvert.com/)

**⚠️ 可能遇到的坑：**

| 报错/问题 | 原因 | 解决 |
|---------|------|------|
| ffmpeg未安装 | 没装 | 按上方安装命令安装 |
| 转换失败 | 格式不支持 | 换用支持的格式 |
| 文件不存在 | 路径错 | 检查完整路径 |

---

#### 8.2 视频编辑工具

裁剪、拼接、提取音频。**需 FFmpeg**。

<details>
<summary>📋 展开查看命令</summary>

```python
import subprocess
try:
    act = input("操作(裁剪/拼接/提取音频):").strip() or "裁剪"
    if act == "裁剪":
        f = input("文件:") or "video.mp4"
        s = input("开始时间(HH:MM:SS):") or "00:01:00"
        t = input("时长(HH:MM:SS):") or "00:02:00"
        subprocess.run(["ffmpeg","-i",f,"-ss",s,"-t",t,"-c","copy","clipped.mp4"])
    elif act == "拼接":
        fs = input("文件(逗号):") or "a.mp4,b.mp4"
        with open("files.txt","w") as tf:
            for x in fs.split(","): tf.write(f"file '{x}'\n")
        subprocess.run(["ffmpeg","-f","concat","-i","files.txt","-c","copy","joined.mp4"])
    else:
        f = input("文件:") or "video.mp4"
        subprocess.run(["ffmpeg","-i",f,"-vn","audio.mp3"])
    print("✅ 完成")
except FileNotFoundError:
    print("❌ ffmpeg 未安装")
except Exception as e:
    print(f"❌ {e}")
```

</details>

**📦 需确认** ｜ 🌐 [ClipConverter替代](https://www.clipconverter.cc/)

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

### 场景 2：网络不好时

```
你: "帮我查勾股定理"
AI: ❌ Wikipedia 被墙 → 自动用百度替代
```

### 场景 3：不确定能不能做时

```
你: "能帮我恢复删除的文件吗？"
AI: ❌ 不支持（超出工具范围）
```

---

## ❓ 常见问题

### Q1: 第一次使用怎么做？
直接说一句话。零依赖功能直接跑。需安装功能会提示。

### Q2: 提示安装依赖怎么办？
跑一行 `pip install Pillow PyPDF2`，装完即可。

### Q3: 下载壁纸被墙 / Wikipedia 查不了？
国内网络问题。解决：用代理，或改用在线工具（已列在每个功能下方）。

### Q4: PDF 加密后忘记密码怎么办？
无法恢复。密码只在加密时展示一次，请截图保存。

### Q5: 图片压缩会损坏原图吗？
不会。另存为新文件（compressed_开头），原图不动。

### Q6: 视频转换失败？
大概率是 FFmpeg 没装或版本不对。确认 `ffmpeg -version` 有输出。

### Q7: 怎么升级 dgngjx-skill？
```bash
clawhub install dgngjx-skill
clawhub update dgngjx-skill
```

---

## 功能分类统计

| 类别 | 数量 | 开箱即用 |
|------|:----:|:--------:|
| ✅ 零依赖即可运行 | 14 | ✅ |
| 📦 需确认安装后运行 | 15 | ❌（有引导+在线替代） |
| **总计** | **29** | **48%** |

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
  - v1.7.0：每个命令加详细中文报错+解决方案+可能遇到的坑表格/网络错误处理/文件路径检查
  - v1.6.0：详细安装引导/中文报错/最佳实践/边界情况说明
  - v1.5.0：图片修复用Pillow重写/一键安装脚本/网络错误中文提示
  - v1.4.0：命令折叠隐藏/概览页精简
  - v1.3.0：30秒速查表/报错说明
  - v1.2.0：含可运行命令/FAQ
  - v1.1.0：去除人脸年龄变换
  - v1.0.0：初始版，8大模块
