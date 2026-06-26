# DocPilot — 智能文档处理专家

> OpenClaw Skill - 高精度文档解析、信息抽取、文档分类

从 PDF、图片、Word、Excel 文档中提取结构化数据，支持信息抽取和文档分类。

## 为什么选择 DocPilot？

### 三层能力 + 六大核心优势

**三层能力**
1. **解析** — 高精度识别文档内容，保留版面结构
2. **抽取** — 按需求提取关键字段，每条结果都能溯源到原文位置
3. **分类** — 自动识别文档类型，混合文档也能自动切分

**六大核心优势**

#### 1. 证据溯源 — 每个字段都有"身份证" ⭐ 独家
```json
{
  "key": "合同金额",
  "value": "¥1,200,000",
  "confidence": "high",
  "evidence": [{
    "text": "合同总金额：¥1,200,000",
    "page": 2,
    "quad": [[120, 350], [480, 350], [480, 380], [120, 380]]
  }]
}
```
> 审计、法务、财务场景必备 — 知道数据从哪来，才能相信数据是对的。

#### 2. 混合文档切分 — 一份文件，多种类型 ⭐ 独家
上传一份包含"合同+发票+报价单"的混合文件，自动识别边界并逐段分类。

#### 3. 印章检测 — 公章/签名章/骑缝章自动识别 ⭐ 独家
自动检测文档中的印章和签章，返回位置和类型信息，适用于合同审查、资质验证。

#### 4. 跨页表格合并 — 断裂表格智能还原 ⭐ 独家
自动识别跨页断裂的表格，智能合并表头和表体，输出完整结构。

#### 5. 手写字体识别 — 印刷+手写混合识别 ⭐ 独家
支持印刷体和手写体混合识别，覆盖表单填写、手写批注、签字确认等场景。

#### 6. 全格式支持 — 一个技能全部搞定
PDF · 图片 · Word · Excel · CSV — 无需组合多个工具。

---

## 功能特性

- ✅ **多格式支持**: PDF、图片 (JPG/PNG)、Word、Excel、CSV
- ✅ **版面分析**: 自动检测和解析文档结构元素
- ✅ **表格识别**: 提取表格并输出 HTML 和 Markdown 格式，支持跨页合并
- ✅ **信息抽取**: 按 schema 提取结构化字段，带证据溯源
- ✅ **文档分类**: 单文档分类或混合文档切分分类
- ✅ **印章检测**: 检测文档中的印章和签章
- ✅ **手写识别**: 印刷体+手写体混合识别
- ✅ **多种输出格式**: structured JSON、markdown、纯文本

---

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
openclaw skills install DocPilot

# 或手动安装（本地开发）
cd E:\skills\document-parser
pip install -r requirements.txt
```

### 配置

**方式一：环境变量**
```bash
# Windows PowerShell
$env:DOCPilot_BASE_URL="https://docpilot.token-ai.com.cn"
$env:DOCPilot_API_KEY="your_api_key"
```

**方式二：配置文件**
```bash
cd E:\skills\DocPilot
copy config.example.json config.json
# 编辑 config.json 填入你的 API 地址和 API Key
```

**方式二：配置文件**
```bash
cd E:\skills\document-parser
copy config.example.json config.json
# 编辑 config.json 填入你的 API 地址
```

### 使用方法

#### 解析文档
```bash
# 基础解析
DocPilot parse "C:\docs\report.pdf"

# Markdown 输出
DocPilot parse "C:\docs\scan.jpg" --output markdown

# 启用印章检测和边界框
DocPilot parse "C:\docs\contract.pdf" --seal --bbox

# 解析 Excel
DocPilot parse "C:\docs\data.xlsx"
```

#### 信息抽取
```bash
# 按 schema 抽取字段
DocPilot extract "C:\docs\contract.pdf" --schema "{\"fields\":[{\"key\":\"甲方\",\"type\":\"string\"},{\"key\":\"乙方\",\"type\":\"string\"}]}"

# 使用 schema 文件
DocPilot extract "C:\docs\invoice.pdf" --schema schema.json
```

#### 文档分类
```bash
# 单文档分类
DocPilot classify "C:\docs\doc.pdf"

# 混合文档分类和切分
DocPilot classify "C:\docs\mixed.pdf" --mode classify_and_split --categories "[{\"name\":\"合同\",\"description\":\"合同协议\"},{\"name\":\"发票\",\"description\":\"发票单据\"}]"
```

---

## 参数说明

### parse 命令

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | string | 是 | PDF/图片/Word/Excel 文件路径 |
| --output | string | 否 | 输出格式：structured/markdown/text |
| --layout | flag | 否 | 启用版面分析 |
| --table | flag | 否 | 启用表格识别（含跨页合并） |
| --seal | flag | 否 | 启用印章检测 |
| --dpi | int | 否 | DPI：72/144/200/216 |
| --pages | string | 否 | 页码范围，如 "1-5,8,10-12" |
| --bbox | flag | 否 | 包含边界框坐标 |
| --normalize | flag | 否 | 返回格式化解析数据（默认开启） |
| --raw | flag | 否 | 返回原始解析格式 |
| --include-image | flag | 否 | markdown 中包含图片 |
| --image-format | string | 否 | 图片格式：url/base64 |

### extract 命令

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | string | 是 | 文档文件路径 |
| --schema | JSON | 是 | 字段 schema 定义 |
| --prompt | JSON | 否 | 提示词模式 schema |
| --schema-ref | string | 否 | 模板引用 |
| --options | JSON | 否 | 扩展配置 |

### classify 命令

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | string | 是 | 文档文件路径 |
| --mode | string | 否 | classify_only / classify_and_split |
| --categories | JSON | 否 | 分类 schema 定义 |

---

## 输出格式

### parse 响应
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "document_id": "dp-8a3f-xxxx",
    "page_count": 25,
    "file_type": "pdf",
    "pages": [...],
    "markdown": "..."
  }
}
```

### extract 响应
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "extraction_id": "ext-xxxx",
    "fields": [
      {
        "key": "甲方",
        "value": "某某公司",
        "confidence": "high",
        "evidence": [...]
      }
    ],
    "unfound_fields": [],
    "metadata": {...}
  }
}
```

### classify 响应
```json
{
  "code": 10000,
  "message": "Success",
  "data": {
    "mode": "classify_only",
    "classification": {
      "category": "合同",
      "confidence": 0.95,
      "reasoning": "..."
    },
    "metadata": {...}
  }
}
```

---

## 支持的文档元素

| 类型 | 说明 |
|------|------|
| DocumentTitle | 文档标题 |
| LevelTitle | 层级标题 |
| Paragraph | 段落 |
| Table | 表格（支持跨页合并） |
| Image | 图片 |
| Seal | 印章 |
| FigureTitle | 图表标题 |
| Handwriting | 手写文字 |

---

## 典型应用场景

| 场景 | 使用方式 | 核心能力 |
|------|----------|----------|
| **合同审查** | 抽取关键字段 + 印章检测 | 证据溯源 + 印章识别 |
| **财务审计** | 跨页表格合并 + 字段抽取 | 跨页合并 + 溯源 |
| **档案整理** | 混合文档自动分类切分 | 文档分类 |
| **招投标文件** | 识别报价单/资质/方案并分别处理 | 文档分类 + 解析 |
| **表单处理** | 手写内容识别 + 结构化抽取 | 手写识别 + 信息抽取 |
| **合规检查** | 检测印章、签章，验证文档完整性 | 印章检测 |

---

## 错误码

| 错误码 | 消息 | 说明 |
|--------|------|------|
| 10000 | Success | 成功 |
| 10001 | Missing parameter | 参数缺失 |
| 10002 | Invalid parameter | 非法参数 |
| 10003 | Invalid file | 文件格式非法 |
| 10004 | Failed to recognize | 识别失败 |
| 10005 | Internal error | 内部错误 |

---

## 依赖

- Python 3.8+
- requests>=2.28.0

---

## 许可证

MIT License

---

## 支持

如有问题请提交 Issue 或联系 TokenAI。
