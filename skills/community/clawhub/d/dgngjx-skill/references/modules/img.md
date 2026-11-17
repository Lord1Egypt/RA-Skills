# 🖼️ 模块 6：图片工具

---

#### 6.1 img 统一入口 ⭐ v3.9.0 合并为子命令

> v3.9.0 将图片 5 功能合并为 `img` 统一入口，通过子命令调用：`compress`（压缩）、`convert`（格式转换）、`removebg`（抠图）、`idphoto`（证件照）、`repair`（修复）。

<details>
<summary>📋 img.compress（图片压缩）</summary>

```python
from PIL import Image, ImageFile
import os, multiprocessing
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = 180_000_000

def _fix_path(p):
    return p.strip().strip('"').strip("'").replace("\\","/").replace("//","/")

def _auto_workers():
    cpus = multiprocessing.cpu_count() or 2
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
    except ImportError:
        ram_gb = 8
    if ram_gb < 4 or cpus <= 2:
        return 1
    elif ram_gb < 8 or cpus <= 4:
        return min(cpus - 1, 2)
    else:
        return min(cpus, 4)

EXTS = {".jpg",".jpeg",".png",".webp",".bmp",".tiff",".gif"}
OUT_FMT = {"JPEG":".jpg", "PNG":".png", "WEBP":".webp", "BMP":".bmp"}

path = _fix_path(input("图片路径或目录:").strip() or "photos")
if not os.path.exists(path):
    print(f"❌ 不存在: {path}")
else:
    if os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path)
                 if os.path.splitext(f)[1].lower() in EXTS]
    else:
        files = [path]
    if not files:
        print("⚠️ 未找到图片文件")
    else:
        print(f"📁 共 {len(files)} 张图片")
        q = int(input("质量(1-100,建议75-85):") or 80)
        q = max(1, min(q, 100))
        fmt = input("输出格式(JPEG/PNG/WebP/BMP,默认JPEG):").strip().upper() or "JPEG"
        if fmt not in OUT_FMT:
            print(f"❌ 不支持 {fmt}，使用 JPEG")
            fmt = "JPEG"
        workers = _auto_workers()
        print(f"⚡ 并发数: {workers}（自动硬件适配）")
        ok = fail = saved_total = 0
        for i, f in enumerate(files, 1):
            try:
                img = Image.open(f)
                if img.mode in ('RGBA','PA') and fmt != 'PNG':
                    img = img.convert('RGB')
                base = os.path.splitext(os.path.basename(f))[0]
                out = os.path.join(os.path.dirname(f), f"{base}_compressed{OUT_FMT[fmt]}")
                save_opts = {"quality": q, "optimize": True} if fmt == "JPEG" else {}
                img.save(out, format=fmt, **save_opts)
                o, c = os.path.getsize(f)/1024, os.path.getsize(out)/1024
                saved_total += max(0, o - c)
                ok += 1
                if len(files) <= 20 or i % 5 == 0:
                    print(f"  [{i}/{len(files)}] {os.path.basename(f)}: {o:.0f}KB→{c:.0f}KB")
            except Exception as e:
                fail += 1
                print(f"  [{i}/{len(files)}] {os.path.basename(f)} ❌ {e}")
        print(f"\n✅ 成功 {ok} / 失败 {fail}")
        print(f"   累计节省 {saved_total/1024:.1f} MB")
```

</details>

<details>
<summary>📋 img.convert（格式转换 JPEG/PNG/WebP/BMP）</summary>

```python
from PIL import Image
import os

def _fix_path(p):
    return p.strip().strip('"').strip("'").replace("\\","/").replace("//","/")

EXTS = {".jpg",".jpeg",".png",".webp",".bmp",".tiff",".gif"}
OUT_FMT = {"JPEG":".jpg", "PNG":".png", "WEBP":".webp", "BMP":".bmp"}

path = _fix_path(input("图片路径:").strip() or "photo.jpg")
if not os.path.exists(path):
    print(f"❌ 不存在: {path}")
else:
    fmt = input("目标格式(JPEG/PNG/WebP/BMP):").strip().upper() or "PNG"
    if fmt not in OUT_FMT:
        print(f"❌ 不支持 {fmt}")
    else:
        img = Image.open(path)
        if img.mode in ('RGBA','PA') and fmt != 'PNG':
            img = img.convert('RGB')
        base = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(os.path.dirname(path), f"{base}_converted{OUT_FMT[fmt]}")
        img.save(out, format=fmt)
        print(f"✅ 已转换: {out}")
```

</details>

<details>
<summary>📋 img.removebg（人像抠图）</summary>

```python
from rembg import remove
import os
try:
    inp = input("图片:").strip().strip('"').replace("\\","/") or "portrait.jpg"
    if not os.path.exists(inp):
        print(f"❌ 文件不存在: {inp}")
    else:
        out = f"bg_removed_{os.path.basename(inp)}.png"
        result = remove(open(inp,"rb").read())
        open(out,"wb").write(result)
        print(f"✅ 完成: {out}")
except ImportError: print("❌ 缺少 rembg: pip install rembg")
except Exception as e: print(f"❌ {e}")
```

</details>

<details>
<summary>📋 img.idphoto（证件照生成）</summary>

```python
from PIL import Image
try:
    f = input("照片:").strip().strip('"').replace("\\","/") or "face.jpg"
    sz = input("尺寸(一寸/二寸):").strip()或 "一寸"
    bg = input("背景色(白色/蓝色/红色):").strip()或 "白色"
    sizes = {"一寸":(295,413),"二寸":(413,579)}
    bgs = {"白色":(255,255,255),"蓝色":(0,0,255),"红色":(255,0,0)}
    w,h = sizes.get(sz, sizes["一寸"])
    img = Image.open(f).resize((w,h),Image.LANCZOS)
    canvas = Image.new("RGB",(w,h),bgs.get(bg, (255,255,255)))
    canvas.paste(img,(0,0),img if img.mode=="RGBA" else None)
    canvas.save(f"证件照_{sz}_{bg}.png")
    print(f"✅ 证件照_{sz}_{bg}.png ({w}x{h})")
except Exception as e: print(f"❌ {e}")
```

</details>

<details>
<summary>📋 img.repair（图片修复）</summary>

```python
from PIL import Image, ImageEnhance
try:
    f = input("老照片路径:").strip().strip('"').replace("\\","/") or "old.jpg"
    img = Image.open(f)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img.save("repaired.jpg")
    print("✅ 完成: repaired.jpg")
except Exception as e: print(f"❌ {e}")
```

</details>
