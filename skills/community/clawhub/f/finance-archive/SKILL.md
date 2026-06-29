---
name: finance-archive
description: 上市公司财务文件归档与整理技能包，自动整理凭证、合同、附件，按标准目录结构归档，支持PDF处理、批量重命名、MD5查重、会计档案保管期限管理及审计支持。
metadata:
  openclaw:
    author: "@AOLIKEJI"
    version: 1.0.0
    category: finance
    tags:
      - 财务归档
      - 凭证归档
      - 档案整理
      - archive
      - 合同归档
      - 附件整理
      - 文件归档
      - 会计档案
      - 审计支持
    emoji: "📁"
    homepage: "https://www.clawhub.com/skills/finance-archive"
    triggers:
      - 财务归档
      - 凭证归档
      - 档案整理
      - archive
      - 合同归档
      - 附件整理
      - 文件归档
---

# 财务归档技能包 (Finance Archive)

## 概述

本技能包面向上市公司财务部门，提供完整的文件归档与整理解决方案。涵盖凭证、账簿、报表、合同、发票、银行对账单、税务资料、审计底稿等各类财务文件的规范化管理，确保符合《会计档案管理办法》要求，支持电子化归档与长期保管。

---

## 一、归档目录标准

### 1.1 目录树结构模板

```
财务档案/
├── 01_凭证档案/
│   ├── 20XX年/
│   │   ├── 01月/
│   │   ├── 02月/
│   │   └── .../
│   └── 扫描件/
│       ├── 凭证_{凭证号}_{摘要}_{日期}.pdf
│       └── 附件_{原始文件名}.pdf
├── 02_账簿档案/
│   ├── 总账/
│   ├── 明细账/
│   ├── 日记账/
│   └── 辅助账/
├── 03_报表档案/
│   ├── 年度报表/
│   │   ├── 资产负债表
│   │   ├── 利润表
│   │   ├── 现金流量表
│   │   └── 所有者权益变动表
│   ├── 季度报表/
│   └── 月度报表/
├── 04_发票档案/
│   ├── 增值税专用发票/
│   ├── 增值税普通发票/
│   └── 其他票据/
├── 05_合同档案/
│   ├── 采购合同/
│   ├── 销售合同/
│   ├── 服务合同/
│   ├── 租赁合同/
│   └── 劳动合同/
├── 06_银行档案/
│   ├── 银行回单/
│   ├── 银行对账单/
│   └── 银企对账调节表/
├── 07_税务档案/
│   ├── 纳税申报表/
│   ├── 完税凭证/
│   ├── 发票认证资料/
│   └── 税收优惠备案/
├── 08_审计档案/
│   ├── 内部审计/
│   ├── 外部审计/
│   ├── 审计报告/
│   └── 审计底稿/
└── 09_其他档案/
    ├── 董事会文件/
    ├── 股东会文件/
    └── 其他重要文件/
```

### 1.2 命名规范

| 类别 | 命名格式 | 示例 |
|------|----------|------|
| 凭证 | `凭证_{凭证号}_{摘要}_{YYYYMMDD}.pdf` | `凭证_记001_支付货款_20240115.pdf` |
| 合同 | `合同_{合同编号}_{对方单位}_{合同类型}_{起止日期}.pdf` | `合同_HT2024001_供应商A_采购_20240101-20241231.pdf` |
| 发票 | `发票_{发票号码}_{日期}_{金额}.pdf` | `发票_12345678_20240115_10000.00.pdf` |
| 银行回单 | `回单_{银行_{交易日期}_{流水号}.pdf` | `回单_工行_20240115_TX20240115001.pdf` |
| 报表 | `报表_{报表类型}_{期间}_{编制日期}.pdf` | `报表_资产负债表_2024Q1_20240415.pdf` |

---

## 二、凭证归档规则

### 2.1 归档流程

1. **凭证审核** → 2. **附件完整性检查** → 3. **扫描电子化** → 4. **命名归档** → 5. **装订入库**

### 2.2 命名规范

```
凭证号_摘要_日期_附件数量
```

- **凭证号**：账务系统凭证编号，4位数字，如 `记0001`
- **摘要**：业务内容简要描述，不超过20个字符
- **日期**：YYYYMMDD格式
- **附件数量**：N个附件

**示例**：`记0001_支付办公室租金_20240115_3.pdf`

### 2.3 附件整理规则

| 附件类型 | 整理要求 |
|----------|----------|
| 发票 | 按凭证顺序排列，发票联在前，记账联在后 |
| 合同 | 复印件归档，原件由法务部保管 |
| 审批单 | 领导签批页在前，附件清单在后 |
| 其他单据 | 按单据日期顺序排列 |

### 2.4 装订顺序

1. 凭证封面
2. 凭证汇总表
3. 记账凭证（按凭证号顺序）
4. 原始凭证（发票→合同→审批单→其他）
5. 凭证封底

**装订要求**：
- 每本凭证不超过200张原始凭证
- 使用防潮、防虫档案盒
- 凭证盒脊标注：年度、月份、起止凭证号

---

## 三、合同归档规则

### 3.1 合同台账字段

| 字段 | 说明 |
|------|------|
| 合同编号 | 唯一标识 |
| 合同名称 | 全称 |
| 合同类型 | 采购/销售/服务/租赁/劳动等 |
| 甲方/乙方 | 合同双方 |
| 签约日期 | YYYY-MM-DD |
| 生效日期 | YYYY-MM-DD |
| 到期日期 | YYYY-MM-DD |
| 合同金额 | 精确到分 |
| 付款方式 | 分期/一次性等 |
| 经办部门 | 签订部门 |
| 经办人 | 责任人 |
| 保管期限 | 合同终止后X年 |
| 存放位置 | 档案盒编号 |
| 电子扫描件 | PDF文件路径 |
| 备注 | 特殊说明 |

### 3.2 到期提醒机制

| 提醒节点 | 说明 |
|----------|------|
| 到期前180天 | 初步审查是否续约 |
| 到期前90天 | 启动续约谈判 |
| 到期前30天 | 最终决策 |
| 到期当日 | 合同归档确认 |

### 3.3 合同保管期限

| 合同类型 | 保管期限 |
|----------|----------|
| 重大合同（亿元以上） | 永久 |
| 一般采购/销售合同 | 合同终止后15年 |
| 服务类合同 | 合同终止后10年 |
| 劳动合同 | 解除/终止后2年 |
| 简易合同（口头） | 2年 |

---

## 四、电子档案管理

### 4.1 PDF处理

#### 合并PDF
```python
from PyPDF2 import PdfMerger
import os

def merge_pdfs(pdf_list, output_path):
    """合并多个PDF文件"""
    merger = PdfMerger()
    for pdf in pdf_list:
        if os.path.exists(pdf):
            merger.append(pdf)
    with open(output_path, 'wb') as f:
        merger.write(f)
    return output_path
```

#### 拆分PDF
```python
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_dir, pages_per_file=10):
    """按页数拆分PDF"""
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    for i in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        for j in range(i, min(i + pages_per_file, total_pages)):
            writer.add_page(reader.pages[j])
        
        output_path = os.path.join(output_dir, f"part_{i//pages_per_file + 1}.pdf")
        with open(output_path, 'wb') as f:
            writer.write(f)
```

#### 添加水印
```python
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_watermark(input_path, output_path, watermark_text):
    """为PDF添加文字水印"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.saveState()
        c.setFont('Helvetica', 40)
        c.setFillColorRGB(0.5, 0.5, 0.5, 0.3)
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        c.translate(width/2, height/2)
        c.rotate(45)
        c.drawCentredString(0, 0, watermark_text)
        c.restoreState()
        c.save()
        
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        page.merge_page(watermark_pdf.pages[0])
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
```

### 4.2 批量重命名

```python
import os
import re

def batch_rename(directory, pattern, replacement):
    """批量重命名文件"""
    for filename in os.listdir(directory):
        new_filename = re.sub(pattern, replacement, filename)
        if new_filename != filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
```

**常用重命名规则**：
- 日期格式统一：`YYYY-MM-DD` → `YYYYMMDD`
- 去除特殊字符：空格→下划线
- 添加前缀：按类型添加 `INV_`、`CON_`、`REC_`

### 4.3 MD5查重

```python
import hashlib
import os
from collections import defaultdict

def get_file_md5(file_path):
    """计算文件MD5"""
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def find_duplicates(directory):
    """查找重复文件"""
    hash_dict = defaultdict(list)
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                file_hash = get_file_md5(file_path)
                hash_dict[file_hash].append(file_path)
    
    duplicates = {k: v for k, v in hash_dict.items() if len(v) > 1}
    return duplicates
```

### 4.4 压缩归档

```python
import zipfile
import os
from datetime import datetime

def archive_files(source_dir, archive_name=None, format='zip'):
    """压缩归档文件"""
    if archive_name is None:
        archive_name = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    archive_path = os.path.join(os.path.dirname(source_dir), f"{archive_name}.{format}")
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    
    return archive_path
```

---

## 五、会计档案保管期限

根据《会计档案管理办法》（财政部、国家档案局令第79号）规定：

### 5.1 企业会计档案保管期限表

| 档案类别 | 具体内容 | 保管期限 |
|----------|----------|----------|
| **凭证类** | 原始凭证、记账凭证 | 30年 |
| **账簿类** | 总账、明细账、日记账、其他辅助账簿 | 30年 |
| **财务报告类** | 月度、季度财务报告 | 10年 |
| **财务报告类** | 年度财务报告（会计年报） | 永久 |
| **其他类** | 银行存款余额调节表、银行对账单 | 10年 |
| **其他类** | 纳税申报表 | 10年 |
| **其他类** | 会计档案移交清册 | 30年 |
| **其他类** | 会计档案保管清册 | 永久 |
| **其他类** | 会计档案销毁清册 | 永久 |
| **其他类** | 销售合同、采购合同 | 15年 |
| **其他类** | 资本、基金凭证 | 永久 |
| **其他类** | 涉及未结清的债权债务原始凭证 | 40年 |

### 5.2 保管期限计算起点

- 会计凭证：从会计年度终了后第一天算起
- 会计账簿：从会计年度终了后第一天算起
- 财务报告：从编制完成之日算起
- 其他会计档案：从会计年度终了后第一天算起

### 5.3 销毁流程

```
1. 编制销毁清册 → 2. 单位负责人审批 → 3. 监销人签字确认 → 4. 销毁记录归档
```

**注意**：保管期满但未结清的债权债务原始凭证、涉及其他未了事项的原始凭证不得销毁。

---

## 六、审计支持

### 6.1 凭证检索

```python
def search_vouchers(voucher_dir, keywords, date_range=None):
    """搜索凭证"""
    results = []
    for filename in os.listdir(voucher_dir):
        if filename.endswith(('.pdf', '.xlsx')):
            filepath = os.path.join(voucher_dir, filename)
            # 关键词匹配
            for keyword in keywords:
                if keyword.lower() in filename.lower():
                    results.append(filepath)
                    break
    return results
```

### 6.2 底稿整理

| 审计阶段 | 底稿内容 | 归档要求 |
|----------|----------|----------|
| 计划阶段 | 总体审计策略、具体审计计划 | 永久保管 |
| 实施阶段 | 风险评估底稿、控制测试底稿、实质性程序底稿 | 永久保管 |
| 完成阶段 | 审计报告、管理建议书、声明书 | 永久保管 |
| 业务约定书 | 审计业务约定书、变更函 | 永久保管 |

### 6.3 函证归档

| 函证类型 | 归档内容 | 保管期限 |
|----------|----------|----------|
| 银行函证 | 发函原件、回函原件、银行流水 | 永久 |
| 往来函证 | 发函原件、回函原件、对账差异说明 | 永久 |
| 存货函证 | 发函原件、回函原件、盘点差异 | 永久 |

**函证编号规则**：`YF_{年份}_{类型}_{序号}`
**示例**：`YF_2024_YH_001`（2024年银行函证第1号）

---

## 七、使用流程

### 7.1 新凭证归档流程

```
1. 接收凭证 → 2. 审核完整性 → 3. 扫描电子化 → 4. 命名归档 → 5. 更新台账
```

### 7.2 合同归档流程

```
1. 合同签订 → 2. 移交档案室 → 3. 审核合同 → 4. 录入台账 → 5. 扫描归档 → 6. 设置到期提醒
```

### 7.3 年度归档流程

```
1. 年度结束 → 2. 凭证装订 → 3. 报表整理 → 4. 账簿归档 → 5. 编制移交清册 → 6. 入库保管
```

---

## 八、常见问题

### Q1: 电子档案与纸质档案冲突时以哪个为准？
**A**: 原则上以纸质档案为准，电子档案作为辅助参考。重要文件应同时保存纸质和电子版本。

### Q2: 保管期满的档案如何处理？
**A**: 编制销毁清册，经单位负责人审批后，由档案机构和会计机构共同派员监销。

### Q3: 员工离职时如何处理其经手的财务档案？
**A**: 必须完成档案交接手续，移交清单需由接收人、监交人签字确认。

### Q4: 如何保证电子档案的法律效力？
**A**: 建议使用电子签章、时间戳、数字签名等技术，并保存完整的光盘备份。

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2024-01-01 | 初始版本发布 |

---

**作者**: @AOLIKEJI  
**版权**: © 2024 AOLIKEJI. All rights reserved.
