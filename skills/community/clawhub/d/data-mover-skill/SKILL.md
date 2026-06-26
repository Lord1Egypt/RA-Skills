---
name: data-mover-skill
description: 跨系统数据自动搬运工 - OCR 识别 + 自动复制粘贴 + 多系统支持
version: 1.0.0
tags: [data-entry, automation, ocr, rpa, copy-paste, productivity]
user-invocable: true
---

# Data Mover Skill - 跨系统数据搬运工

自动识别屏幕数据，跨系统复制粘贴，支持 Excel→CRM、邮件→ERP、网页→数据库等场景。

## 触发条件

- **手动触发**: `/move-data` 或 "帮我搬运数据"
- **定时触发**: 每天固定时间执行
- **热键触发**: 配置全局热键（如 F12）

## 核心功能

### 1. 屏幕 OCR 识别
- 截图识别文字和表格
- 支持多语言（中文、英文、数字）
- 自动识别字段类型
- 准确率 > 95%

### 2. 自动复制粘贴
- 模拟键盘鼠标操作
- 智能字段映射
- 批量处理（100+ 条/分钟）
- 错误自动重试

### 3. 多系统支持
- **Excel/Google Sheets** → 任意系统
- **邮件** → CRM/ERP
- **网页表单** → 数据库
- **PDF** → Excel/数据库
- **图片** → 结构化数据

### 4. 智能映射
- 自动识别字段对应关系
- 学习用户操作习惯
- 自定义映射规则
- 支持复杂转换逻辑

### 5. 数据验证
- 格式校验（邮箱、电话、日期）
- 重复检测
- 完整性检查
- 异常值告警

## 配置参数

```yaml
ocr:
  engine: "paddleocr"  # paddleocr, tesseract, easyocr
  languages: ["ch", "en"]
  confidence_threshold: 0.9

automation:
  speed: "normal"  # slow, normal, fast
  retry_count: 3
  delay_between_actions: 0.5

mappings:
  - name: "Excel to CRM"
    source: "excel"
    target: "salesforce"
    fields:
      "姓名": "name"
      "电话": "phone"
      "邮箱": "email"
      "公司": "company"

validation:
  enabled: true
  rules:
    email: "^[\\w.-]+@[\\w.-]+\\.\\w+$"
    phone: "^1[3-9]\\d{9}$"
    required_fields: ["name", "phone"]
```

## 使用示例

### 示例 1: Excel → CRM
```bash
# 配置映射
data-mover config --mapping "excel-to-crm"

# 执行搬运
data-mover run --source excel --target crm --file data.xlsx
```

### 示例 2: 邮件 → Excel
```bash
# 从邮件提取数据到 Excel
data-mover extract --source email --target excel --output contacts.xlsx
```

### 示例 3: 截图识别
```bash
# 截图并识别
data-mover ocr --screenshot --output data.json

# 识别指定区域
data-mover ocr --region "100,100,500,300" --output data.json
```

### 示例 4: 批量处理
```bash
# 批量处理 100 个文件
data-mover batch --input ./invoices/ --output ./results/ --pattern "*.pdf"
```

## 输出示例

```
🚀 开始数据搬运
📂 源：Excel (data.xlsx)
🎯 目标：CRM (Salesforce)
📊 记录数：150 条

处理进度:
  ✅ 100/150 (66.7%)
  ⏱️  已用：2 分 30 秒
  📈 速度：60 条/分钟

验证结果:
  ✅ 成功：145 条
  ⚠️  警告：3 条（格式问题）
  ❌ 失败：2 条（重复数据）

💾 结果已保存到：results_20260316_160500.json
📋 详细日志：logs/data-mover.log
```

## 依赖

- PaddleOCR 或 Tesseract
- PyAutoGUI
- OpenCV
- Pandas

## 安全

- 本地处理，数据不出境
- 操作日志完整记录
- 支持 dry-run 模式
- 敏感数据加密存储

## 扩展

- 支持更多目标系统
- 自定义 OCR 引擎
- 工作流编排
- 云端同步
