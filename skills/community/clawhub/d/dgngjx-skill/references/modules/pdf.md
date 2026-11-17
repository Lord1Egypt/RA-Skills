# 📄 模块 7：PDF 转换

---

#### 7.1 PDF 合并

📦 **需 PyPDF2**

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfMerger
import os
files = []
total_mb = 0
try:
    while True:
        f = input(f"文件{len(files)+1}(回车结束):").strip().strip('"').replace("\\","/")
        if not f: break
        if not os.path.exists(f): print(f"❌ 跳过: {f}"); continue
        size_mb = os.path.getsize(f)/1024/1024
        total_mb += size_mb
        if size_mb > 500: print(f"⚠️ {size_mb:.0f}MB 大文件，合并可能较慢")
        files.append(f)
    if len(files) < 2: print("❌ 至少2个PDF")
    else:
        if total_mb > 100: print(f"⚠️ 总大小 {total_mb:.0f}MB，需1-5分钟...")
        m = PdfMerger()
        ok = 0
        for f in files:
            try: m.append(f); ok+=1
            except: print(f"⚠️ 跳过损坏文件: {f}")
        if len(m.pages)==0: print("❌ 全部损坏")
        else:
            m.write("merged.pdf"); m.close()
            print(f"✅ merged.pdf ({ok}/{len(files)} 文件, {os.path.getsize('merged.pdf')/1024/1024:.1f}MB)")
except Exception as e: print(f"❌ {e}")
```

</details>

---

#### 7.2 PDF 拆分

📦 **需 PyPDF2**

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
import os
try:
    inp = input("PDF路径:").strip().strip('"').replace("\\","/") or "source.pdf"
    pgs = input("页码(如 1-3):").strip() or "1-3"
    if not os.path.exists(inp): print("❌ 文件不存在")
    else:
        r = PdfReader(inp)
        if r.is_encrypted: print("❌ 已加密，请先解密！")
        else:
            w = PdfWriter(); total = len(r.pages); added = 0
            for p in pgs.split(","):
                if "-" in p:
                    s,e = map(int, p.split("-"))
                    if s>e: s,e = e,s
                    for i in range(max(0,s-1),min(e,total)):
                        w.add_page(r.pages[i]); added+=1
                else:
                    idx = int(p)-1
                    if 0<=idx<total: w.add_page(r.pages[idx]); added+=1
            w.write("extracted.pdf")
            print(f"✅ extracted.pdf ({added}页)")
except Exception as e: print(f"❌ {e}")
```

</details>

---

#### 7.3 PDF 加密 / 7.4 PDF 解密

📦 **需 PyPDF2**

<details>
<summary>📋 展开查看命令</summary>

```python
from PyPDF2 import PdfReader, PdfWriter
# 加密
inp = input("PDF路径:").strip().strip('"') or "source.pdf"
pwd = input("密码:").strip()
if len(pwd)<4: print("⚠️ 密码太短")
else:
    r=PdfReader(inp); w=PdfWriter()
    for p in r.pages: w.add_page(p)
    w.encrypt(pwd); w.write("encrypted.pdf")
    print("✅ encrypted.pdf (密码丢失无法恢复!)")

# 解密
inp = input("加密PDF:").strip().strip('"') or "encrypted.pdf"
pwd = input("密码:").strip()
r=PdfReader(inp)
if r.is_encrypted: r.decrypt(pwd)
w=PdfWriter()
for p in r.pages: w.add_page(p)
w.write("decrypted.pdf"); print("✅ decrypted.pdf")
```

</details>
