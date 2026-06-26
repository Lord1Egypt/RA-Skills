# 腾讯Skillhub 上架说明 — 合同风险智能审查

## 应用基础信息

- **Skill ID / Slug:** contract-risk-reviewer
- **名称:** 合同风险智能审查
- **副标题:** AI 驱动的合同风险分析工具
- **分类:** 办公效率 > 文档处理 > 合同管理
- **标签:** 合同审查、风险分析、AI、PDF、劳动合同、采购合同、保密协议
- **语言:** 中文（主要）、English（支持）

---

## 一句话简介

上传合同 PDF，AI 自动识别类型、提取关键条款、标注风险点，输出结构化审查报告。

---

## 功能介绍（详细）

### 核心功能
1. **PDF 文本提取** — 支持直接文本提取（PyMuPDF + pdfplumber）和 OCR 识别（扫描件）
2. **合同类型自动识别** — 6 大类型：劳动合同、采购合同、销售合同、租赁合同、保密协议、其他
3. **文本摘要** — 200 字内概括合同核心内容
4. **关键条款提取** — 当事人/金额/付款条件/期限/违约责任/解除条款/争议解决（STD 及以上）
5. **风险分级列表** — 🔴高 / 🟠中 / 🟡低三级，按风险严重程度排序
6. **Excel 报告导出** — CSV 格式，方便存档和分享（STD 及以上）
7. **双语支持** — 中文合同 + 英文合同（跨境场景）

### 适用场景
- 企业采购/法务部门快速审查合同
- HR 审核劳动合同条款
- 自由职业者/创业者签署合作合同前自检
- 跨境业务英文合同风险识别

### 套餐说明

| 套餐 | 价格 | 月限额 | 支持类型 | 功能 |
|------|------|--------|----------|------|
| 免费版 | ¥0 | 3份 | 其他 | 摘要 + 风险列表 |
| 标准版 | ¥9.9 | 30份 | 全部6类 | 摘要 + 风险列表 + 关键条款表 + Excel导出 |
| Pro版 | ¥29 | 200份 | 全部6类 | + 批量处理 + 风险对比 |
| Max版 | ¥69 | 不限 | 全部6类 | + API优先响应 |

---

## 使用方法

在 Agent 中发送"合同审查"或上传 PDF 文件即可触发。

```
用户：帮我审查这份合同 [上传PDF]
Agent：→ 自动提取文本 → AI分析 → 返回结构化风险报告
```

---

## 技术要求

### 环境依赖
```
Python >= 3.8
PyMuPDF >= 1.23.0
pdfplumber >= 0.10.0
pytesseract >= 0.3.10
pdf2image >= 1.16.0
openai >= 1.0.0
```

### OCR 语言包（如需处理扫描件）
- 中文：`tesseract-ocr-chi-sim`
- 英文：`tesseract-ocr-eng`（通常随主包自带）
- Ubuntu: `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim`
- macOS: `brew install tesseract tesseract-lang`

### API 配置
需要配置 OpenAI 兼容接口（支持 MiniMax / OpenAI / 其他兼容端点）。

---

## 风险提示

本工具输出的分析报告**仅供参考**，不构成法律建议。合同风险应由具有相关资质法律专业人士进行评估。

---

## 上架前清理命令

```bash
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
```

---

## 目录结构

```
contract-risk-reviewer/
├── SKILL.md          # 主技能定义
├── README.md         # 使用说明
├── CLAWHUB.md        # ClawHub 上架信息
├── SKILLHUB.md       # 腾讯Skillhub 上架信息
├── scripts/
│   ├── analyze_contract.py   # 主程序
│   └── requirements.txt       # Python 依赖
└── references/       # 参考资料目录（可选）
```

---

## 更新日志

### v1.0.0 (2026-04-20)
- 初始版本
- 支持 6 种合同类型自动识别
- 支持中文 + 英文双语
- PDF 文本提取（直接 + OCR 双模式）
- 风险分级报告输出
- 套餐分级功能控制
