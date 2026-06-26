---
name: expense-reimbursement
description: 差旅报销票据整理 / Travel Expense Reimbursement：支持高德/Didi/滴滴/Uber打车、12306火车票、机票、酒店住宿；递归扫描含ZIP内部；OCR识别行程单；判断出差/公出类型；按行程自动归档；填写研发经费使用单；生成打印材料包PDF（粘贴单永远首页）；自动化PDF合并（图片+PDF混排，统一A4尺寸）；用户确认后才能继续。/ Supports taxi, train, flight, hotel receipts. Recursive ZIP scan, OCR, auto-classify, form filling, print package generation with checkpoints. macOS/Linux.
---

# 差旅报销整理技能 v3.0
# Travel Expense Reimbursement Assistant v3.0

---

## 这个技能能做到什么？

把报销从"手动分类归档"变成"AI自动完成"，再到最后一步"打印材料包生成"，全程每个关键节点需要你确认后才继续。

### 核心能力

- **Step 0-6**：票据扫描 → 分类归档 → 填写表单 → 汇报确认（必须等你说"确认"才完成）
- **Step 7**：粘贴单核查 → 生成打印材料包 PDF（粘贴单首页）→ 汇报页数 → 等你说"确认"
- **Step 8**：签字完成后收尾，更新最终版打印材料包

### 自动化合并（关键能力）

Python 代码支持：
- **表单 docx → PDF（python-docx + reportlab Table 重建，完全本地）**
- 所有票据 PDF → 直接合并（打印机自动适配 A4，不做强制缩放）
- 图片行程单截图 → 转为 PDF（等比缩放 A4 页面）
- 全程自动跳过申请截图、.DS_Store 等无关文件

---

## 能力前提

| 依赖 | 用途 |
|------|------|
| `python-docx` | 读 Word 表单内容 |
| `pypdf` | 合并多个 PDF |
| `reportlab` | 图片 → A4 PDF（等比缩放） |
| `Pillow` | 图片尺寸读取 |
| `tesseract`（Linux/Windows） | OCR；macOS 用内置 `qlmanage` |
| `zipfile`（标准库） | 解压 ZIP |

```bash
pip install python-docx pypdf reportlab Pillow
```

---

## 核心概念

### 出差 vs 公出

| 类型 | 判断 | 补贴 |
|------|------|------|
| **出差** | 外出 > 1天（在外过夜） | 有差旅补贴 |
| **公出** | 外出 ≤ 1天（当日往返） | 无补贴 |

> 以申请截图时间为准，不自作主张。

### 票据材料分类

| 类型 | 处理方式 |
|------|---------|
| 粘贴单（BEWG/截圖） | PDF，第1页固定 |
| 研发经费使用单 | python-docx + reportlab Table 渲染 PDF，第2页 |
| 打车发票 PDF | 第3页起，发票+行程单配对 |
| 火车票 PDF | 自带行程信息，无需配对，放在最后 |
| 申请截图 PNG | **跳过**，不加入打印包 |

---

## 标准工作流程

```
用户: "帮我整理报销"
  ↓
【阶段一：归档】
Step 0-6 → 汇报 → 等你说"确认" → 完成
  ↓
【阶段二：打印材料】
用户: "生成打印材料"
  ↓
Step 7.1 粘贴单核查 → 汇报完整性
  ⚠️ 等你说"确认"
  ↓
Step 7.3 生成打印材料包 → 汇报页数
  ⚠️ 等你说"确认"
  ↓
Step 7.4 创建扫描打印文件夹 → 汇报完成
  ↓
用户: "签字完成"
  ↓
【阶段三：收尾】
Step 8 → 更新签字版 → 汇报完成
```

---

## Step 0 — 读取申请截图

OCR 提取：出差/公出类型、出发日期、返回日期、目的地、事由。

---

## Step 1 — 递归扫描所有票据

含 ZIP 内部，完整扫描，不遗漏。

---

## Step 2 — 识别票据类型，解析内容

**打车发票**：XML 解析 `<SellerAddr>` 判断真实城市。
**火车票**：OCR 提取出发地/到达地/车次/时间/金额。
**行程单图片**：`qlmanage -t -s 1200` + image 工具 OCR。

---

## Step 3 — 判断出差/公出

出发日期和返回日期相差 > 1天 → 出差；≤ 1天 → 公出。

---

## Step 4 — 按行程分类归档

```
报销/
├── 00_原始资料/               ← 备份，不参与主流程
├── 01_3月11日无锡出差/
│   ├── 申请截图/
│   ├── 交通票据/
│   │   ├── 01_出发打车/
│   │   ├── 02_火车票/
│   │   └── 03_返程打车/
│   ├── 研发经费使用单_北水科技_XXX.docx
│   ├── [粘贴单]/
│   └── 扫描打印文件/          ← Step 7.4 新建
├── ...
└── 领导签字用/               ← 表单签字前集中放这里
```

---

## Step 5 — 填写研发经费使用单

**必须先问用户使用哪个专项项目（课题编号），确认后填写。**

```python
from docx import Document

doc = Document(template_path)
table = doc.tables[0]

def set_cell(cell, text):
    for p in cell.paragraphs:
        for r in p.runs:
            r.text = ""
    if cell.paragraphs[0].runs:
        cell.paragraphs[0].runs[0].text = str(text)
    else:
        cell.paragraphs[0].add_run(str(text))

# 费用明细（只写有费用的项目，金额=0不写入）
items = []
if taxi_total > 0:
    items.append(f"其中市内交通费共计 {taxi_total}元")
if train_total > 0:
    items.append(f"高铁费用 {train_total}元")
if hotel_total > 0:
    items.append(f"住宿费用 {hotel_total}元")
if allowance > 0:
    items.append(f"差旅补贴 {allowance}元")
detail = "因课题研发需要，产生交通费用\n" + "\n".join(items) + f"\n共计{total}元"
for col in [1, 2, 3, 4]:
    set_cell(table.rows[2].cells[col], detail)

for col in [1, 2, 3, 4]:
    set_cell(table.rows[3].cells[col], f"{total}元（大写：...）")

doc.save(output_path)
```

---

## Step 5.5 — 归档完成汇报（必须等确认）

汇报所有行程的：类型、金额、票据数量、归档路径。

```
✅ 归档完成，请确认：
  01_3月2日杭州公出:    ¥130.24  |  4 PDF
  02_3月11日无锡出差:  ¥556.61  |  8 PDF + 2火车票
  04_3月23日哈尔滨公出: ¥285.62  |  8 PDF
  05_3月30日北京公出:   ¥168.92  |  6 PDF
  06_4月2日上海公出:     ¥236.70  |  6 PDF + 2火车票
  合计: ¥1,378.09

⚠️ 回复「确认」后完成归档。
```

---

## Step 5.6 — 原始文件清理（需用户授权）

> "原始文件已备份在 00_原始资料/。回复『删除』清理 ZIP 和临时文件，回复『保留』保留全部。"

---

## Step 6 — 创建对话摘要

路径：`~/memory/YYYY-MM-DD_报销整理.md`

---

## Step 7 — 打印材料生成（分段确认）

### Step 7.1 — 检查粘贴单据完整性

**自动执行，立即汇报：**

```python
import os, glob

def check_paste_lists(reimburs_dir):
    """批量检查所有行程的粘贴单"""
    results = {}
    trip_dirs = sorted([d for d in os.listdir(reimburs_dir)
                        if d.startswith(("0","1","2")) and ("出差" in d or "公出" in d)])
    for trip in trip_dirs:
        trip_dir = os.path.join(reimburs_dir, trip)
        found = None
        for pat in ["BEWG*.pdf", "截圖*.pdf", "截圖 *.pdf"]:
            files = glob.glob(os.path.join(trip_dir, "*粘贴单*", pat), recursive=True)
            files += glob.glob(os.path.join(trip_dir, "**", pat), recursive=True)
            files = [f for f in files if f.endswith('.pdf') and os.path.getsize(f) > 50000]
            if files:
                found = max(files, key=lambda f: os.path.getsize(f))
                break
        results[trip] = found
    return results
```

**汇报格式：**

```
╔══════════════════════════════════════════════════════╗
║              粘贴单据完整性核查                    ║
╚══════════════════════════════════════════════════════╝

✅ 01_3月2日杭州公出:      BEWG-差旅报销单-粘贴单.pdf（55KB）
✅ 02_3月11日无锡出差:    BEWG-差旅报销单-粘贴单.pdf（55KB）
✅ 04_3月23日哈尔滨公出:  截圖 2026-03-28 下午5.53.04.pdf（55KB）
✅ 05_3月30日北京公出:    BEWG-差旅报销单-粘贴单.pdf（55KB）
✅ 06_4月2日上海公出:      BEWG-差旅报销单-粘贴单.pdf（55KB）

结论：5/5 完整。
```

**⚠️ 停顿，等待用户回复「确认」后继续生成打印材料包。**

---

### Step 7.2 — 检查表单签字状态

**汇报签字状态：**

```
╔══════════════════════════════════════════════════════╗
║              表单签字状态核查                       ║
╚══════════════════════════════════════════════════════╝

⚠️ 01_3月2日杭州公出:      表单在「领导签字用」文件夹，尚未签字
⚠️ 02_3月11日无锡出差:    表单在「领导签字用」文件夹，尚未签字
⚠️ 04_3月23日哈尔滨公出:  表单在「领导签字用」文件夹，尚未签字
⚠️ 05_3月30日北京公出:    表单在「领导签字用」文件夹，尚未签字
⚠️ 06_4月2日上海公出:      表单在「领导签字用」文件夹，尚未签字

→ 签字后再执行 Step 8 收尾。
```

---

### Step 7.3 — 生成打印材料包 PDF

**用户回复「确认」后执行，自动合并所有材料为一个 PDF：**

**Python 实现（核心合并逻辑）：**

```python
import os, glob
from pypdf import PdfMerger, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image as PILImage

W, H = A4                       # 210 × 297mm
MARGIN = 12 * mm               # 边距 12mm

# ── 图片 → A4 PDF（等比缩放，不超边距，居中）─────────────
def img_to_pdf(img_path, out_path):
    img = PILImage.open(img_path)
    iw, ih = img.size
    avail_w = W - 2 * MARGIN
    avail_h = H - 2 * MARGIN
    ratio = min(avail_w / iw, avail_h / ih)
    nw, nh = iw * ratio, ih * ratio
    x = (W - nw) / 2
    y = (H - nh) / 2
    c = canvas.Canvas(out_path, pagesize=A4)
    c.drawImage(img_path, x, y, nw, nh)
    c.save()

# ── Word → PDF（python-docx + reportlab Table 渲染）────────────
# 使用 python-docx 读取表单内容 + reportlab Table 重建为 PDF
# 使用 macOS STHeiti 字体渲染中文，无需 Word/LibreOffice
# 完全本地处理，跨平台兼容

# ── 跳过无关文件 ────────────────────────────────────────
SKIP_NAMES = {'申请截图.png', 'ds_store', '.ds_store'}

def should_skip(fname):
    return fname.lower() in SKIP_NAMES or fname.startswith('.')

# ── 核心合并函数 ────────────────────────────────────────
def merge_print_package(trip_dir, out_path):
    """
    按规定顺序合并为打印材料包 PDF
    第1页：粘贴单（强制）
    第2页：研发经费使用单
    第3页起：交通票据（发票+行程单配对，火车票放最后）
    自动跳过：申请截图、.DS_Store 等无关文件
    """
    writer = PdfWriter()
    page = 1
    report_lines = []

    def add_page(src, label):
        nonlocal page
        fname = os.path.basename(src)
        reader = PdfReader(src if src.endswith('.pdf') else src)
        page_obj = reader.pages[0]
        # 票据 PDF 直接合并，打印机自动适配 A4（不做强制缩放，避免变形）
        if src.endswith('.pdf'):
            writer.add_page(page_obj)
        else:
            tmp = src + ".pdf"
            img_to_pdf(src, tmp)
            tmp_reader = PdfReader(tmp)
            tmp_page = tmp_reader.pages[0]
            writer.add_page(tmp_page)
            os.remove(tmp)
        report_lines.append(f"  第{page}页 [{label}] {fname}")
        page += 1

    # ── 第1页：粘贴单 ──────────────────────────────
    for pat in ["BEWG*.pdf", "截圖*.pdf", "截圖 *.pdf"]:
        files = glob.glob(os.path.join(trip_dir, "*粘贴单*", pat), recursive=True)
        files += glob.glob(os.path.join(trip_dir, "**", pat), recursive=True)
        files = [f for f in files if f.endswith('.pdf') and os.path.getsize(f) > 50000]
        if files:
            add_page(max(files, key=lambda f: os.path.getsize(f)), "粘贴单")
            break
    else:
        raise FileNotFoundError(f"❌ {trip_dir}: 粘贴单缺失")

    # ── 第2页：研发经费使用单 ──────────────────────
    docx_files = glob.glob(os.path.join(trip_dir, "*.docx"))
    for d in docx_files:
        if "研发经费使用单" in d:
            # 优先用已签字PDF版
            signed_pdf = d.replace(".docx", "_已签字.pdf")
            if os.path.exists(signed_pdf):
                add_page(signed_pdf, "表单-已签字")
            else:
                # 用 python-docx + reportlab 重建表单 PDF
                tmp = d.replace(".docx", "_rendered.pdf")
                try:
                    docx_to_pdf(d, tmp)
                    with open(tmp, 'rb') as f:
                        page_obj = PdfReader(f).pages[0]
                        writer.add_page(page_obj)
                        report_lines.append(f"  第{page}页 [表单-自动生成] {os.path.basename(tmp)}")
                        page += 1
                except Exception as e:
                    report_lines.append(f"  ⚠️ 表单 PDF 生成失败: {e}")
                    report_lines.append(f"     请在 Word 中打开表单另存为 PDF，命名: {os.path.basename(d.replace('.docx','_已签字.pdf'))}")
            break

    # ── 第3页起：交通票据 ──────────────────────────
    t_dir = os.path.join(trip_dir, "交通票据")
    if os.path.exists(t_dir):
        all_p = []
        for r, ds, fs in os.walk(t_dir):
            for f in fs:
                if should_skip(f):
                    continue
                full = os.path.join(r, f)
                if full.endswith('.pdf') or full.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_p.append(full)

        non_tr  = sorted([p for p in all_p if "火车票" not in p],
                         key=lambda p: os.path.getmtime(p))
        trains  = sorted([p for p in all_p if "火车票" in p],
                         key=lambda p: os.path.getmtime(p))

        for p in non_tr + trains:
            fname = os.path.basename(p)
            if "行程单" in fname:
                label = "行程单"
            elif "火车票" in fname:
                label = "火车票"
            else:
                label = "发票"
            add_page(p, label)

    with open(out_path, "wb") as f:
        writer.write(f)
    total_pages = page - 1
    report_lines.insert(0, f"\n{'='*50}")
    report_lines.insert(1, f"【{os.path.basename(trip_dir)}】打印材料包已生成（共 {total_pages} 页）")
    report_lines.append(f"  📄 {out_path}\n")
    return report_lines


def batch_merge_print_packages(reimburs_dir):
    """批量为所有行程生成打印材料包"""
    trip_dirs = sorted([d for d in os.listdir(reimburs_dir)
                        if d.startswith(("0","1","2")) and ("出差" in d or "公出" in d)])
    all_reports = []
    for trip in trip_dirs:
        trip_dir = os.path.join(reimburs_dir, trip)
        out = os.path.join(trip_dir, "打印材料包.pdf")
        print(f"\n{'='*50}")
        print(f"【{trip}】")
        try:
            lines = merge_print_package(trip_dir, out)
            all_reports.extend(lines)
        except FileNotFoundError as e:
            print(f"  {e}")
            all_reports.append(f"❌ {trip}: {e}")
        except Exception as e:
            print(f"  ⚠️ {e}")
            all_reports.append(f"⚠️ {trip}: {e}")
    return all_reports
```

**执行后汇报：**

```
╔══════════════════════════════════════════════════════╗
║              打印材料包生成完毕                     ║
╚══════════════════════════════════════════════════════╝

【01_3月2日杭州公出】共 4 页
  第1页 [粘贴单] BEWG-差旅报销单-粘贴单.pdf
  第2页 [表单-自动渲染] 研发经费使用单..._rendered.pdf
  第3页 [发票] 高德打车发票.pdf
  第4页 [行程单] 高德打车行程单.pdf

【02_3月11日无锡出差】共 10 页
  ...

⚠️ 请确认打印材料包内容正确。
确认后创建扫描打印文件文件夹（回复「确认」），
签字完成后回复「签字完成」。
```

---

### Step 7.4 — 创建扫描打印文件文件夹

**用户回复「确认」后执行：**

```python
import os, glob, shutil
from pypdf import PdfReader, PdfWriter

def create_scan_print_folder(trip_dir):
    """创建扫描打印文件文件夹，每页一个 PDF，顺序排放"""
    scan_dir = os.path.join(trip_dir, "扫描打印文件")
    os.makedirs(scan_dir, exist_ok=True)
    return scan_dir


def populate_scan_print_folder(trip_dir):
    """
    向扫描打印文件文件夹填充单页 PDF
    顺序：粘贴单 → 表单 → 发票+行程单 → 火车票
    """
    scan_dir = create_scan_print_folder(trip_dir)
    counter = [1]

    def num():
        n = counter[0]
        counter[0] += 1
        return f"0{n}" if n < 10 else str(n)

    def copy_page(src, label):
        dst = os.path.join(scan_dir, f"{num()}_{label}.pdf")
        try:
            reader = PdfReader(src if src.endswith('.pdf') else src)
            writer = PdfWriter()
            writer.add_page(reader.pages[0])
            with open(dst, 'wb') as out:
                writer.write(out)
            print(f"  ✅ {os.path.basename(dst)}")
            return dst
        except Exception as e:
            print(f"  ⚠️ 复制失败 {src}: {e}")
            return None

    # 1. 粘贴单
    for pat in ["BEWG*.pdf", "截圖*.pdf"]:
        files = glob.glob(os.path.join(trip_dir, "*粘贴单*", pat), recursive=True)
        files += glob.glob(os.path.join(trip_dir, "**", pat), recursive=True)
        files = [f for f in files if f.endswith('.pdf') and os.path.getsize(f) > 50000]
        if files:
            copy_page(max(files, key=lambda f: os.path.getsize(f)), "粘贴单")
            break

    # 2. 表单
    for d in glob.glob(os.path.join(trip_dir, "*.docx")):
        if "研发经费使用单" in d:
            signed = d.replace(".docx", "_已签字.pdf")
            if os.path.exists(signed):
                copy_page(signed, "研发经费使用单_已签字")
            break

    # 3. 交通票据
    t_dir = os.path.join(trip_dir, "交通票据")
    if os.path.exists(t_dir):
        all_p = []
        for r, ds, fs in os.walk(t_dir):
            for f in fs:
                if f.lower() in ('申请截图.png', 'ds_store'):
                    continue
                full = os.path.join(r, f)
                if full.endswith('.pdf') or full.lower().endswith(('.png', '.jpg', '.jpeg')):
                    all_p.append(full)

        non_tr = sorted([p for p in all_p if "火车票" not in p],
                        key=lambda p: os.path.getmtime(p))
        trains = sorted([p for p in all_p if "火车票" in p],
                        key=lambda p: os.path.getmtime(p))

        for p in non_tr + trains:
            fname = os.path.basename(p)
            label = fname.replace(".pdf", "")
            copy_page(p, label)

    pages = counter[0] - 1
    print(f"\n  📁 扫描打印文件/ 已创建，共 {pages} 页")
    return scan_dir
```

**汇报：**

```
╔══════════════════════════════════════════════════════╗
║              扫描打印文件文件夹已创建                ║
╚══════════════════════════════════════════════════════╝

✅ 01_3月2日杭州公出:      扫描打印文件/（4页）
✅ 02_3月11日无锡出差:    扫描打印文件/（10页）
✅ 04_3月23日哈尔滨公出:  扫描打印文件/（9页）
✅ 05_3月30日北京公出:    扫描打印文件/（7页）
✅ 06_4月2日上海公出:      扫描打印文件/（7页）

⚠️ 下一步：
1. 将「领导签字用」文件夹中的 5 份表单拿去给领导签字
2. 签字后：将已签字表单扫描为 PDF
   放入对应行程的「扫描打印文件/」文件夹
   命名规则：02_研发经费使用单_已签字.pdf
3. 回复「签字完成」，AI 将更新最终版打印材料包
```

---

## Step 8 — 签字完成收尾

**用户回复「签字完成」后执行：**

```python
import os, glob, shutil
from pypdf import PdfMerger, PdfReader

def post_signature_update(trip_dir):
    """
    1. 找到签字版表单，放入扫描打印文件/
    2. 重新生成打印材料包（用签字版替换）
    """
    scan_dir = os.path.join(trip_dir, "扫描打印文件")
    os.makedirs(scan_dir, exist_ok=True)

    results = []

    # 1. 查找签字版表单
    signed_files = glob.glob(os.path.join(trip_dir, "**", "*已签字*.pdf"), recursive=True)
    if signed_files:
        sf = signed_files[0]
        dst = os.path.join(scan_dir, "02_研发经费使用单_已签字.pdf")
        shutil.copy2(sf, dst)
        results.append(f"✅ 已签字表单已归档: {os.path.basename(sf)}")
    else:
        results.append(f"⚠️ 未找到签字版表单，跳过")

    # 2. 重新生成打印材料包
    pkg = os.path.join(trip_dir, "打印材料包.pdf")
    try:
        # 清空旧包，重新生成（merge_print_package 会自动用已签字PDF）
        merge_print_package(trip_dir, pkg)
        results.append(f"✅ 打印材料包已更新为签字版")
    except Exception as e:
        results.append(f"⚠️ 更新打印材料包失败: {e}")

    return results


def batch_post_signature(reimburs_dir):
    """批量处理所有行程签字收尾"""
    trip_dirs = sorted([d for d in os.listdir(reimburs_dir)
                        if d.startswith(("0","1","2")) and ("出差" in d or "公出" in d)])
    all_results = []
    for trip in trip_dirs:
        trip_dir = os.path.join(reimburs_dir, trip)
        print(f"\n{'='*50}")
        print(f"【{trip}】")
        lines = post_signature_update(trip_dir)
        all_results.extend(lines)
        for l in lines:
            print(f"  {l}")
    return all_results
```

**汇报：**

```
╔══════════════════════════════════════════════════════╗
║              签字收尾完成                          ║
╚══════════════════════════════════════════════════════╝

✅ 01_3月2日杭州公出:      签字版已归档，打印材料包已更新
✅ 02_3月11日无锡出差:    签字版已归档，打印材料包已更新
✅ 04_3月23日哈尔滨公出:  签字版已归档，打印材料包已更新
✅ 05_3月30日北京公出:    签字版已归档，打印材料包已更新
✅ 06_4月2日上海公出:      签字版已归档，打印材料包已更新

全部报销材料整理完成。
```

---

## 报销文件夹路径

| 用途 | 路径 |
|------|------|
| 报销根目录 | `~/报销/` |
| 原始资料备份 | `报销/00_原始资料/` |
| 领导签字用 | `报销/领导签字用/` |
| 打印材料包 | `报销/[行程]/打印材料包.pdf` |
| 扫描打印文件 | `报销/[行程]/扫描打印文件/` |
| 技能备份 | `报销/技能备份/expense_reimbursement_bak_YYYYMMDD_HHMMSS/` |

---

## 流程检查清单

**归档阶段：**
- [ ] 申请截图已 OCR，已确认出差/公出类型
- [ ] 专项项目已与用户确认
- [ ] 模板已就位
- [ ] 票据已递归扫描
- [ ] 研发经费使用单已填写
- [ ] 汇报后获得用户「确认」
- [ ] 清理操作已获用户授权（删除/保留）

**打印材料阶段：**
- [ ] Step 7.1 粘贴单核查已汇报
- [ ] 获得用户「确认」（第一次停顿）
- [ ] Step 7.3 打印材料包已生成，页数已汇报
- [ ] 获得用户「确认」（第二次停顿）
- [ ] Step 7.4 扫描打印文件文件夹已创建
- [ ] 用户已拿去签字
- [ ] 用户回复「签字完成」

**收尾阶段：**
- [ ] Step 8 已执行，签字版已归档
- [ ] 打印材料包 PDF 已更新为最终版
- [ ] 最终完成汇报已输出

---

## 重要规则

1. **原始文件保护** — 00_原始资料/ 始终保留，删除需明确授权
2. **模板首次需提供** — 缺失时必须暂停，不能跳过
3. **每步停顿确认** — Step 5.5、7.1、7.3、7.4、8 都是确认点，不说"确认"不继续
4. **清理需单独授权** — 不默认删除任何文件
5. **专项项目必须先确认** — 不自作主张
6. **粘贴单永远第一页** — 财务要求，不可调整
7. **火车票不配行程单** — 本身已含行程信息
8. **自动跳过无关文件** — 申请截图、.DS_Store 等不进入打印包
9. **签字版放入两个位置** — 扫描打印文件/ + 打印材料包.pdf 同时更新
