# batch-format-converter · 格式批量互转

> 批量文件格式转换：CSV↔Excel↔JSON↔PDF/Markdown/DOCX/HTML/PNG，一键批量转换。

## 功能概述

支持多种格式之间的批量转换，免费版全功能开放（限10个文件绝对计数）。

### 支持的转换方向

| 源格式 | 目标格式 |
|--------|----------|
| CSV | Excel (.xlsx)、JSON |
| Excel (.xlsx/.xls) | JSON、CSV、PNG（表格图片） |
| JSON | Excel（多Sheet） |
| Markdown | DOCX、HTML |
| DOCX | Markdown |
| HTML | Markdown |
| PDF | PNG/JPG（图片） |
| 图片 (PNG/JPG) | PDF |
| TXT | CSV |

### 套餐分级

| 套餐 | 价格 | 文件额度 |
|------|------|----------|
| 免费版 | ¥0 | **共10个文件，绝对累计计数，非每日清零** |
| 标准版 | ¥9.9/月 | 每天100个文件 |
| Pro版 | ¥29/月 | 不限数量 + AI自定义转换 |
| Max版 | ¥69/月 | 不限一切，API优先 |

### Token 前缀
`CONV-FREE` / `CONV-STD` / `CONV-PRO` / `CONV-MAX`

---

## 使用方式

### 普通转换

```
转换以下文件：
[上传文件列表]
目标格式：XLSX
```

### AI自定义转换（Pro/Max）

```
把这个CSV的字段名改成英文，然后转成JSON
把这份DOCX里的表格提取成Excel，其他内容转成Markdown
```

---

## 技术实现

| 类别 | 技术栈 |
|------|--------|
| 表格类 | pandas（CSV/Excel/JSON） |
| PDF类 | PyMuPDF + pdfplumber |
| 文档类 | pandoc + python-docx |
| 图片类 | Pillow (PIL) |
| 编码处理 | UTF-8/GBK/ISO 自动识别 |

---

## 文件结构

```
batch-format-converter/
├── SKILL.md
└── scripts/
    └── converter.py    # 核心转换引擎
```

---

## 计费逻辑

### 免费版（绝对累计计数）
- `total_converted_count` 永久累计，不重置
- 每转换1个文件，`remaining = 10 - total_converted_count`
- 用尽后提示升级，无法继续使用

### 标准版（每日清零）
- 每天重置为100个文件

### Pro/Max（不限）
- 无限制

---

## 飞书集成

- ✅ 转换完成 → 飞书卡片推送通知
- ✅ 结果文件 → 附件发送到飞书

---

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 编码错误 | 自动尝试 UTF-8 → GBK → ISO-8859-1 |
| 格式不支持 | 返回友好提示 + 建议格式 |
| 文件损坏 | 跳过并报告，跳到下一个 |
| 超出额度 | 卡片提示升级方案 |
-e 
> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
