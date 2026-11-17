# 💻 模块 5：开发工具

---

#### 5.1 JSON 工具

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
import json
try:
    r = input("输入JSON:").strip() or '{"key":"value"}'
    if not r: print("❌ 没有输入")
    else:
        p = json.loads(r)
        print(f"✅ 合法\n格式化: {json.dumps(p,ensure_ascii=False,indent=2)}")
        print(f"压缩: {json.dumps(p,ensure_ascii=False,separators=(',',':'))}")
except json.JSONDecodeError as e:
    print(f"❌ JSON错误: {e}")
```

</details>

---

#### 5.2 HTTP 接口测试

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
import urllib.request, socket, ssl
try:
    u = input("URL:").strip() or "https://api.github.com"
    if not u: print("❌ URL不能为空")
    elif not u.startswith("http"): print("❌ 应以 http:// 或 https:// 开头")
    else:
        req = urllib.request.Request(u, headers={"User-Agent":"dgngjx/3.5"})
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        body = resp.read()
        print(f"✅ 状态: {resp.status} ({len(body)} bytes)")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP {e.code}: {e.reason}")
except urllib.error.URLError as e:
    print(f"❌ 网络错误: {e.reason}")
except Exception as e:
    print(f"❌ {e}")
```

</details>

---

#### 5.3 Token 计算器

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
t = input("文本:") or "计算Token数"
if not t.strip(): print("❌ 请输入文字")
else:
    cn = sum(1 for c in t if '一' <= c <= '鿿')
    en = len(t) - cn
    print(f"中文: {cn} ≈{int(cn/1.5)} | 英文: {en} ≈{int(en/4)} | 总计 ≈{int(cn/1.5+en/4)}")
```

</details>

---

#### 5.4 在线 Photoshop

📦 **需 Pillow**

<details>
<summary>📋 展开查看命令</summary>

```python
from PIL import Image, ImageEnhance
try:
    f = input("图片路径:").strip().strip('"').replace("\\","/") or "photo.jpg"
    img = Image.open(f)
    w,h = map(int, input("裁剪 宽,高:").strip() or "200,200").split(","))
    if w > img.width or h > img.height: w,h = min(w,img.width), min(h,img.height)
    img2 = img.crop(((img.width-w)//2,(img.height-h)//2,w+img.width//2,h+img.height//2))
    img2.save("cropped.jpg")
    e = ImageEnhance.Brightness(img).enhance(float(input("亮度(1.2):") or 1.2))
    e.save("bright.jpg")
    print("✅ 已保存 cropped.jpg, bright.jpg")
except Exception as e: print(f"❌ {e}")
```

</details>

---

#### 5.5 Mermaid 时序图

**✅ 开箱即用**

<details>
<summary>📋 展开查看命令</summary>

```python
seq = input("时序图代码:").strip() or "A->B: Hello"
if seq: print(f"sequenceDiagram\n{seq}")
else: print("❌ 代码不能为空")
```

</details>
