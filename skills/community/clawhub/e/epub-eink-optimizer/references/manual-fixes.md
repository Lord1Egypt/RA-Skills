# epub 手动处理补充指南

## 场景一：图片为 base64 内嵌

部分 epub 生成工具会将图片以 base64 直接写入 XHTML，而非独立图片文件。

**识别方法：**
```python
import zipfile, re
with zipfile.ZipFile('book.epub', 'r') as z:
    for name in z.namelist():
        if name.endswith('.xhtml'):
            content = z.read(name).decode('utf-8', errors='replace')
            if 'data:image/' in content:
                print(f"发现base64图片: {name}")
```

**处理方案：**
1. 用正则提取 base64 数据 → 解码为图片 → 压缩 → 重新编码写回
2. 或者用 `ebooklib` 库重建 epub，将 base64 提取为独立图片文件

---

## 场景二：非标准目录结构

`optimize_epub.py` 假设图片在 `OEBPS/Images/` 目录，且 XHTML 中引用格式为 `src="Images/xxx.jpg"`。

如遇不同结构，先诊断：

```python
import zipfile
with zipfile.ZipFile('book.epub', 'r') as z:
    imgs = [n for n in z.namelist() if n.lower().endswith('.jpg')]
    print('\n'.join(imgs[:10]))
```

然后调整脚本中的路径匹配逻辑。

---

## 场景三：转为灰度图进一步减体积

墨水屏本身是黑白/灰度显示，彩色图转灰度可节省额外 30-50%（对于颜色丰富的照片）。

**注意：**转为灰度是有损操作，JPEG 灰度图保存后无法恢复彩色，务必备份原文件。

```python
from PIL import Image
import io

img = Image.open('photo.jpg')
gray = img.convert('L')  # L = 8-bit 灰度
buf = io.BytesIO()
gray.save(buf, format='JPEG', quality=70, optimize=True)
print(f"原始: {len(img.tobytes())} -> 灰度: {len(buf.getvalue())}")
```

在 `optimize_epub.py` 中可以增加 `--grayscale` 选项：
```python
parser.add_argument('--grayscale', action='store_true', help='转为灰度图')
# 在 recompress_jpegs 中加入:
# if args.grayscale: img = img.convert('L')
```

---

## 场景四：微信公众号特有装饰图识别

微信公众号文章末尾通常包含以下固定小图（可用 MD5 哈希识别并批量过滤）：

- **阅读原文**按钮图标
- **在看/点赞**图标（约 2KB）
- **公众号二维码**（各账号不同，但固定出现）
- **广告分隔图**

这类图片特征：文件大小通常 < 5KB，且在大量文章中 MD5 完全相同。`--min-size 10240` 参数可覆盖大多数此类图片。

---

## 常用 epub 结构诊断命令

```bash
# 查看epub内所有文件
python -c "import zipfile; z=zipfile.ZipFile('book.epub'); [print(n) for n in z.namelist()]"

# 统计图片数量和总大小
python -c "
import zipfile
z = zipfile.ZipFile('book.epub')
imgs = [(n, len(z.read(n))) for n in z.namelist() if n.lower().endswith('.jpg')]
print(f'JPEG: {len(imgs)} 张, {sum(s for _,s in imgs)//1024}KB')
"

# 查找悬空的img引用（引用了不存在的图片）
python -c "
import zipfile, re
z = zipfile.ZipFile('book.epub')
names = set(z.namelist())
for xhtml in [n for n in names if n.endswith('.xhtml')]:
    content = z.read(xhtml).decode('utf-8', errors='replace')
    for ref in re.findall(r'src=\"(Images/[^\"]+)\"', content):
        if 'OEBPS/'+ref not in names:
            print(f'悬空: {xhtml} -> {ref}')
"
```
