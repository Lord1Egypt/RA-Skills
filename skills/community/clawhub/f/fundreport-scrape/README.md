# fundreport-scrape 技能说明

## 📦 技能信息

| 项目 | 内容 |
|------|------|
| **技能名称** | fundreport-scrape |
| **版本** | 1.0.0 |
| **作者** | ymzhang |
| **创建日期** | 2026-03-14 |
| **来源** | 基于 mutual-fund-monthly-update v3.0.0 重构 |

---

## 🎯 技能定位

**fundreport-scrape** 是一个专注于基金月报数据提取的技能，从 PDF 月报中自动提取数据并填充到 Excel 模板中。

**与 mutual-fund-monthly-update 的关系：**
- fundreport-scrape 是 mutual-fund-monthly-update 的精简重构版
- 删除了失效和多余的脚本
- 保留了核心功能（OCR 双重提取、双月对比）
- 版本重新从 1.0.0 开始

---

## ✅ 保留的核心脚本

| 脚本 | 用途 |
|------|------|
| `scripts/auto_update_two_months.py` | ⭐ 双月对比处理（推荐使用） |
| `scripts/auto_update_ocr.py` | OCR 增强版单月处理 |
| `scripts/install_ocr_deps.sh` | OCR 依赖一键安装 |

---

## ❌ 已删除的脚本

| 脚本 | 删除原因 |
|------|---------|
| `update_fund_excel.py` | 旧版脚本，功能已被替代 |
| `auto_update_final.py` | 不支持 OCR，功能不完整 |

---

## 🚀 快速使用

### 安装依赖

```bash
cd ~/.agents/skills/fundreport-scrape
sudo ./scripts/install_ocr_deps.sh
```

### 运行处理

```bash
python3 scripts/auto_update_two_months.py \
  "互认基金月度更新_202512vs202601.xlsx" \
  "月报数据/202512/" \
  "月报数据/202601/" \
  "互认基金月度更新_202512vs202601_最终版.xlsx"
```

---

## 📊 核心功能

1. **文本+OCR 双重提取** - 确保图表数据不遗漏
2. **双月自动对比** - 一次处理两个月份
3. **智能日期解析** - 支持 YYYYMM 和 YYMM 格式
4. **批量处理** - 一次处理 10+ 只基金

---

## 📁 完整文件列表

```
fundreport-scrape/
├── SKILL.md                  # 技能说明文档
├── SECURITY_REVIEW.md        # 安全评估报告
├── _meta.json                # 元数据（版本、作者）
├── requirements.txt          # Python 依赖
├── scripts/
│   ├── auto_update_two_months.py # 双月处理（推荐）
│   ├── auto_update_ocr.py       # OCR 增强版
│   └── install_ocr_deps.sh      # 依赖安装
└── references/
    ├── extraction_templates.json
    ├── ocr_rules.md
    ├── field_mapping.md
    ├── template_learning.md
    ├── batch_processing.md
    └── interaction_rules.md
```

---

## 📝 版本历史

### v1.0.0 (2026-03-14)

**初始版本，包含：**
- ✅ 文本+OCR 双重提取
- ✅ 双月对比处理
- ✅ 智能日期解析
- ✅ 批量处理支持
- ✅ 完整的文档和参考材料

---

**技能位置：** `~/.agents/skills/fundreport-scrape/`
