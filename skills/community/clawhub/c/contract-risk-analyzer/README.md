# 合同风险智能审查 (Contract Risk Reviewer)

**Slug:** `contract-risk-reviewer`
**Platform:** ClawHub (clawhub.ai) + 腾讯Skillhub

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r scripts/requirements.txt

# For OCR support (recommended for scanned contracts):
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# macOS:
brew install tesseract tesseract-lang
```

### 2. 配置 API Key

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.minimax.chat/v1"  # or your custom endpoint
```

### 3. 运行分析

```bash
# Free tier (summary + risk list only)
python scripts/analyze_contract.py --pdf /path/to/contract.pdf

# Standard tier (with key terms table + CSV export)
python scripts/analyze_contract.py --pdf /path/to/contract.pdf --tier STD --export-csv

# Pro tier
python scripts/analyze_contract.py --pdf /path/to/contract.pdf --tier PRO --export-csv
```

### 4. OpenClaw Agent 调用

当用户触发"合同审查"时：
1. 使用 `doc_parse` 或对应工具获取 PDF 文件
2. 保存到 `/tmp/contracts/<uuid>.pdf`
3. 调用 `analyze_contract.py` 脚本
4. 将返回的 markdown 报告发送给用户

---

## 输出示例

```
## 📄 合同风险审查报告

**合同类型：** 劳动合同
**语言：** 中文
**整体风险评分：** 6/10 — 中风险

---

### 📋 文本摘要
[200字摘要]

---

### 🔑 关键条款
[表格 - STD+]

---

### ⚠️ 风险点列表

#### 🔴 高风险 (2项)
1. **未约定加班费计算基数**
   - 类别：liability
   - 条款来源：第X条
   - 风险描述：...
   - 建议措施：...

...

⚠️ **免责声明：** 本报告仅供参考，不构成法律建议。
```

---

## 支持的合同类型

| 类型 | 触发关键词 |
|------|-----------|
| 劳动合同 | 劳动合同、聘用、工资、社会保险 |
| 采购合同 | 采购、供应商、货物、供货 |
| 销售合同 | 销售、买方、出卖、产品 |
| 租赁合同 | 租赁、承租、租金、房屋 |
| 保密协议 | 保密、NDA、confidential、商业秘密 |
| 其他 | 默认分类 |

---

## 套餐对比

| 功能 | FREE (¥0) | STD (¥9.9) | PRO (¥29) | MAX (¥69) |
|------|-----------|-----------|-----------|-----------|
| 月限额 | 3份 | 30份 | 200份 | 不限 |
| 合同类型 | 其他 | 全部6类 | 全部6类 | 全部6类 |
| 文本摘要 | ✅ | ✅ | ✅ | ✅ |
| 风险列表 | ✅ | ✅ | ✅ | ✅ |
| 关键条款表 | ❌ | ✅ | ✅ | ✅ |
| Excel导出 | ❌ | ✅ | ✅ | ✅ |
| 批量处理 | ❌ | ❌ | ✅ | ✅ |
| 风险对比 | ❌ | ❌ | ✅ | ✅ |
| API优先 | ❌ | ❌ | ❌ | ✅ |

---

## Token 前缀

- `CONTRACT-FREE` — 免费版
- `CONTRACT-STD` — 标准版
- `CONTRACT-PRO` — Pro版
- `CONTRACT-MAX` — Max版

---

## 技术栈

- **PDF 文本提取：** PyMuPDF (fitz) + pdfplumber
- **OCR：** pytesseract + pdf2image（多语言支持：chi_sim + eng）
- **AI 分析：** OpenAI 兼容接口（支持 MiniMax / OpenAI / 自定义端点）
- **报告导出：** CSV (Excel 兼容)

---

## 免责说明

本技能输出的分析报告**仅供参考**，不构成法律建议。合同风险应由具有相关资质法律专业人士进行评估。

> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
