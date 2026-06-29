## BA3 格式转换域 范本

本文件包含 BA3 域（BA3-01 ~ BA3-04）的纯范本内容。

**与脚本的关系**：本域的标准化操作已由 `scripts/render_svg_to_png.py`（渲染+缩小+ICO构建）和 `scripts/verify_assets.py`（质量校验+完整性校验）完整覆盖，可直接执行。本范本不再重复脚本中已有的函数代码，只提供：
1. 脚本调用方式与参数说明
2. 脚本内部逻辑的概念性说明（便于理解与定制）
3. 脚本未覆盖场景的代码片段
4. 技术坑详解

---

### BA3-01 SVG→PNG渲染 · HTML包装概念说明

**脚本调用**：`render_svg_to_png.py` 的 `render_svg_to_png(svg_path, target_w, target_h, tmp_dir, timeout)` 函数已封装完整渲染流程，直接调用即可。

**内部逻辑概念**（便于定制修改）：

Edge headless 不按 `<img src="file.svg">` 缩放SVG，必须将SVG内嵌到HTML并设置width/height属性。脚本内部的HTML包装结构：

```html
<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1024px;height:1024px;overflow:hidden}</style>
</head><body>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="-15 -15 270 270"
     width="1024" height="1024"
     preserveAspectRatio="xMidYMid meet">
  <!-- SVG内容（width/height已被脚本替换为目标尺寸） -->
</svg>
</body></html>
```

**Edge headless渲染命令**（脚本内部执行）：
```bash
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" \
  --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --screenshot=output.png \
  --window-size=1024,1024 \
  --default-background-color=00000000 \
  file:///path/to/wrapper.html
```

**关键约束**：必须内嵌SVG并设置width/height属性，不能用`<img src="file.svg">`。

---

### BA3-02 多尺寸位图生成 · 脚本调用说明

**脚本调用**：`render_svg_to_png.py` 的 `resize_png(src_path, dst_path, target_w, target_h)` 函数已封装Pillow LANCZOS缩小，直接调用即可。

**渲染策略**（脚本main()内部实现）：
- 小尺寸（16/32/64/128px）：从简化版SVG渲染的1024大图缩小
- 大尺寸（256/512px）：从完整版SVG渲染的1024大图缩小
- 480px展示版：从完整版大图缩小，无尺寸后缀

**完整执行**：直接运行 `python render_svg_to_png.py <project_root>` 即可生成全部6个尺寸+1个展示版。

**预期文件大小参考**（用于质量评估）：

| 尺寸 | 预期大小 | 用途 |
|------|---------|------|
| 16×16 | ~600B | Favicon 小 |
| 32×32 | ~1.4KB | Favicon 标准 |
| 64×64 | ~4KB | Favicon 大 |
| 128×128 | ~10KB | App 小 |
| 256×256 | ~35KB | App 中 |
| 512×512 | ~85KB | App 标准 |

**ICO内嵌PNG提取**：ICO构建完成后，用上述`extract_ico_pngs()`函数从ICO二进制提取4个PNG（16×16/32×32/48×48/64×64），文件名将作为`favicon_16x16.png`等存入01_核心标志目录，供HTML展示页使用。

---

### BA3-02A 横版/竖版多尺寸生成

**脚本调用**（推荐）：`render_svg_to_png.py --all` 已内置横版/竖版多尺寸生成，一键完成。

```bash
python render_svg_to_png.py <项目根目录> --all
# 自动渲染：纯图标多尺寸(6) + 展示版(1) + 横版(4) + 竖版(4) + 批量VI(18) + 品牌规范(3) + 扩展应用(9) + favicon.ico
```

**横版标志多尺寸**（标准版 600×240 → 2.5:1 纵横比）：

```python
from PIL import Image
std = Image.open("01_核心标志/01_横版标志.png").convert("RGBA")
for suffix, ratio in [("_1200", 2.0), ("_300", 0.5), ("_150", 0.25), ("_75", 0.125)]:
    w, h = round(std.width * ratio), round(std.height * ratio)
    std.resize((w, h), Image.LANCZOS).save(f"01_横版标志{suffix}.png")
```

**竖版标志多尺寸**（标准版 400×480 → 5:6 纵横比）：

```python
from PIL import Image
std = Image.open("01_核心标志/02_竖版标志.png").convert("RGBA")
for suffix, ratio in [("_960", 2.0), ("_240", 0.5), ("_120", 0.25), ("_60", 0.125)]:
    w, h = round(std.width * ratio), round(std.height * ratio)
    std.resize((w, h), Image.LANCZOS).save(f"02_竖版标志{suffix}.png")
```

**尺寸用途对照**：

| 横版 | 尺寸 | 用途 | 竖版 | 尺寸 | 用途 |
|------|------|------|------|------|------|
| _1200 | 1200×480 | 高清大屏/印刷海报 | _960 | 800×960 | 高清大屏/竖版海报 |
| (标准) | 600×240 | 网站页眉/文档封面 | (标准) | 400×480 | 竖版海报/立牌 |
| _300 | 300×120 | 中等应用/PPT页脚 | _240 | 200×240 | 中等应用/名片 |
| _150 | 150×60 | 小尺寸水印/信纸 | _120 | 100×120 | 小尺寸图标/头像 |
| _75 | 75×30 | 极小尺寸/社交媒体 | _60 | 50×60 | 极小尺寸/头像小 |

---

### BA3-02B 批量VI系统渲染

**脚本调用**（推荐）：`render_svg_to_png.py --all` 已内置批量VI系统渲染。

```bash
python render_svg_to_png.py <项目根目录> --all --timeout 120
# 遍历02~09目录，逐一渲染VI系统+品牌规范+扩展应用SVG
# --timeout 120 增大超时时间（默认90s），大图自动延长
```

**遍历策略**（脚本内部实现）：

```python
import os, re
subdirs = ["02_商标注册", "03_数字化应用", "04_办公文具", "05_宣传物料",
           "06_品牌规范", "07_环境应用", "08_产品周边", "09_多媒体模板"]
for subdir in subdirs:
    dirpath = os.path.join(project_root, subdir)
    for f in os.listdir(dirpath):
        if not f.endswith(".svg"):
            continue
        # 跳过01_核心标志目录（已由纯图标逻辑处理）
        # 跳过03_纯图标.svg、03_纯图标_小尺寸版.svg（已由专用脚本处理）
        svg_path = os.path.join(dirpath, f)
        # 按viewBox自动计算渲染尺寸（商标945×945、名片1800×1080等）
        # 已存在且非空→跳过
        # Edge headless超时→切换--headless重试
```

**关键点**：
- 跳过 `01_核心标志` 目录（已由纯图标+横版/竖版逻辑处理）
- 已存在的PNG（大小>0）自动跳过，支持增量渲染
- Edge headless 超时后自动切换 `--headless` 模式重试（默认90s，大图自动延长）

---

### BA3-03 ICO多尺寸构建 · 二进制结构说明

**脚本调用**：`render_svg_to_png.py` 的 `build_ico(ico_path, png_sources)` 函数已封装手动ICO构建，直接调用即可。

**为什么需要手动构建**：PIL的 `Image.save(ico, sizes=[...])` 只保存第一帧，必须手动构建ICO二进制结构。

**ICO文件二进制结构**（概念说明，便于理解脚本逻辑）：
```
[6字节 Header]
  reserved:  2字节  固定0x0000
  type:      2字节  固定0x0001（ICO格式）
  count:     2字节  图像数量

[16字节 × count 个 Entry]
  width:     1字节  宽度（≥256时填0）
  height:    1字节  高度（≥256时填0）
  palette:   1字节  调色板数（0=无调色板）
  reserved:  1字节  固定0x00
  planes:    2字节  颜色平面数（1）
  bpp:       2字节  每像素位数（32=RGBA）
  size:      4字节  PNG数据大小
  offset:    4字节  PNG数据偏移量（从文件起始）

[PNG数据 × count 个]
  每个尺寸的PNG数据，顺序与Entry一致
```

**脚本内部尺寸映射**：48px从64px缩小生成（`src_map = {16:16, 32:32, 48:64, 64:64}`）

**favicon.ico四尺寸用途说明**（用于HTML展示页）：

| 尺寸 | 使用场景 |
|------|---------|
| 16×16 | 浏览器标签页图标（标准尺寸，所有浏览器必用） |
| 32×32 | 高DPI/Retina屏幕、Windows任务栏 |
| 48×48 | Windows桌面快捷方式、地址栏图标 |
| 64×64 | 资源管理器大图标视图、Linux桌面环境 |

ICO是多尺寸容器，浏览器/操作系统自动按场景挑选最合适尺寸。HTML引用只需一行：`<link rel="icon" href="favicon.ico">`

---

### BA3-03 ICO多尺寸构建 · ICO内嵌PNG提取技术说明

ICO构建完成后，必须从ICO二进制提取4个内嵌PNG，供HTML展示页展示ICO的多尺寸效果。

**ICO内嵌PNG提取代码范本**：

```python
import os
import struct
from PIL import Image
from io import BytesIO

def extract_ico_pngs(ico_path, output_dir):
    """从ICO二进制提取内嵌PNG，返回提取的文件列表"""
    with open(ico_path, 'rb') as f:
        data = f.read()
    
    count = struct.unpack_from('<H', data, 4)[0]
    extracted = []
    
    pos = 6
    for i in range(count):
        w = data[pos] or 256
        h = data[pos+1] or 256
        img_size = struct.unpack_from('<I', data, pos+8)[0]
        img_offset = struct.unpack_from('<I', data, pos+12)[0]
        
        # 检查图像数据是否为PNG
        if data[img_offset:img_offset+4] == b'\x89PNG':
            png_blob = data[img_offset:img_offset+img_size]
            img = Image.open(BytesIO(png_blob))
            out_path = os.path.join(output_dir, f"favicon_{w}x{h}.png")
            img.save(out_path, "PNG")
            extracted.append(out_path)
        
        pos += 16
    
    return extracted
```

**关键点**：
- ICO中的图像数据本身就是完整PNG（`\x89PNG`签名），不是BMP
- 用PIL的`BytesIO`包裹PNG二进制即可直接用`Image.open()`
- 提取的PNG文件名格式：`favicon_16x16.png`、`favicon_32x32.png`、`favicon_48x48.png`、`favicon_64x64.png`
- 提取的PNG与ICO中的内嵌尺寸完全一致，可放心用于HTML展示

---

### BA3-04 渲染质量校验 · 脚本调用说明

**脚本调用**：`verify_assets.py --render-check` 已封装渲染质量校验（`check_render_quality()` 函数），包含PNG边缘截断检查和ICO结构有效性检查。

**校验内容**：
1. PNG四边像素检查——检测内容是否被裁切（边缘像素应全部为背景色或透明）
2. ICO header/entry解析——验证reserved、type、offset、size字段是否符合规范

**完整执行**：
```bash
python verify_assets.py <project_root> --render-check
```

输出示例：
```
Render quality check:
  ICO OK: 01_核心标志/favicon.ico (4 sizes: [16, 32, 48, 64])
  All PNGs edges clean, ICO structure valid
```

---

### BA3域技术坑

**坑1：SVG viewBox / 背景rect不匹配**
- 问题：SVG内容偏左上角，边缘被裁切
- 根因：viewBox（如`-15 -15 270 270`）定义270×270空间，但`<rect width="240" height="240"/>`只覆盖[0,0]→[240,240]
- 修复：背景rect必须覆盖整个viewBox

**坑2：Edge headless不按img标签缩放SVG**
- 问题：SVG渲染为PNG时保持固有尺寸，忽略img的width/height
- 修复：内嵌SVG到HTML，直接设置svg元素的width/height属性（脚本已实现）

**坑3：小尺寸PNG细节丢失**
- 问题：16/32/64/128px PNG细线、小点消失
- 根因：1024→64缩小16倍，stroke-width<1或r<6的元素变成亚像素
- 修复：先渲染1024大图再LANCZOS缩小；为小尺寸创建简化版SVG（BA2-05）

**坑4：PIL只保存ICO第一帧**
- 问题：`Image.save(ico, sizes=[...])`只生成单帧ICO
- 修复：手动构建ICO二进制结构（脚本 `build_ico()` 已实现）

**坑5：中文路径在Python中乱码**
- 问题：GBK终端下Python无法打开含中文的路径
- 说明：Python 3（3.13+）原生支持Unicode路径，此问题在当前环境中已不存在

**坑6：Windows venv路径**
- 问题：文档说`bin/python.exe`但Windows用`Scripts/python.exe`
- 修复：`C:\Users\<user>\.workbuddy\binaries\python\envs\default\Scripts\python.exe`

**坑7：GBK终端拒绝emoji输出**
- 问题：`print("✅ Done")`引发UnicodeEncodeError
- 修复：用ASCII字符替代（脚本已使用ASCII输出）

**坑8：PNG增量渲染跳过，SVG变更不生效**
- 问题：SVG内容（品牌文案、个人信息、颜色）已更新，但重新运行`--all`后PNG仍显示旧内容
- 根因：`render_svg_to_png.py --all`具有增量渲染能力，已存在的PNG文件自动跳过。SVG变更后必须手动删除旧PNG才能强制重新渲染
- 触发场景：品牌Slogan更新、个人信息替换后重新渲染
- 修复：先`rm`删除受影响的旧PNG，再运行`python render_svg_to_png.py . --all`
- **检查命令**：`ls -la *.svg *.png | paste - -` 查看SVG与PNG的修改时间是否一致

**坑9：SVG品牌文案与HTML不一致**
- 问题：HTML中的品牌Slogan已更新，但SVG中的文案仍为旧值
- 根因：品牌文案变更时只更新了HTML，未同步更新SVG中`<text>`元素的文案。SVG中承载品牌标语的典型位置：门头招牌、展会背景板、易拉宝、礼品袋、社交媒体配图、网站Banner、名片背面、A4信纸
- 触发场景：品牌Slogan变更、公司定位语更新
- 修复：先用`grep -rn`扫描所有SVG中的旧文案，再用`sed`批量替换，最后强制重新渲染PNG
- **检查命令**：`grep -rn '旧文案关键词' *.svg */*.svg */*/*.svg`
- **流程**：扫描旧文案 → sed批量替换 → rm旧PNG → 重新渲染

**坑10：ICO构建完成但未提取内嵌PNG**
- 问题：ICO文件已生成（含4尺寸），但01_核心标志目录中无`favicon_16x16.png`等4个独立PNG
- 根因：ICO构建后遗漏了内嵌PNG提取步骤
- 影响：HTML展示页中ICO多尺寸卡片引用4个不存在的PNG
- 修复：ICO构建后立即执行`extract_ico_pngs()`从ICO二进制提取4个PNG
- **检查命令**：`ls 01_核心标志/favicon_*.png | wc -l` 应为4

**坑11：SVG `<defs>` 外定义渐变导致HTML中破碎图标**
- 问题：PPT封面.svg、员工工牌.svg在HTML中显示为破碎图标
- 根因：SVG中`<linearGradient id="bg1">`定义在`<defs>`之外（如line 3），`<defs>`在line 5才打开，浏览器无法注册该渐变
- 修复：所有渐变定义必须放在`<defs>`内部，确保`<defs>`在第一个渐变之前打开
- **检查命令**：`for f in *.svg; do grep -n 'linearGradient\|<defs>\|</defs>' "$f" | head -5; done`，确保`<defs>`在第一个`linearGradient`之前
