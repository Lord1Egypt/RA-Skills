---
name: DocPilot
description: 智能文档处理专家，支持文档解析、信息抽取、文档分类
version: 2.0.0
author: TokenAI
tags:
  - pdf
  - document
  - extraction
  - ocr
  - table
  - parser
  - classify
commands:
  - parse
  - extract
  - classify
---

# DocPilot — 智能文档处理专家

高精度文档处理技能，支持文档解析、信息抽取、文档分类。

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

## 命令

### 解析文档
```
DocPilot parse <文件路径> [选项]
```

示例：
```
DocPilot parse C:\docs\report.pdf
DocPilot parse C:\docs\scan.jpg --output markdown
DocPilot parse C:\docs\data.xlsx
DocPilot parse C:\docs\contract.pdf --seal --bbox
```

### 信息抽取
```
DocPilot extract <文件路径> --schema <JSON>
```

示例：
```
DocPilot extract C:\docs\contract.pdf --schema "{\"fields\":[{\"key\":\"甲方\",\"type\":\"string\"},{\"key\":\"乙方\",\"type\":\"string\"}]}"
DocPilot extract C:\docs\invoice.pdf --schema schema.json
```

### 文档分类
```
DocPilot classify <文件路径> [选项]
```

示例：
```
DocPilot classify C:\docs\mixed.pdf
DocPilot classify C:\docs\docs.pdf --mode classify_and_split --categories "[{\"name\":\"合同\",\"description\":\"合同协议\"},{\"name\":\"发票\",\"description\":\"发票单据\"}]"
```

---

## 参数说明

### parse 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| 文件路径 | PDF/图片/Word/Excel 文件路径 | `C:\docs\report.pdf` |
| --output | 输出格式 (structured/markdown/text) | `--output markdown` |
| --layout | 启用版面分析 | `--layout` |
| --table | 启用表格识别（含跨页合并） | `--table` |
| --seal | 启用印章识别 | `--seal` |
| --dpi | DPI (72/144/200/216) | `--dpi 200` |
| --pages | 页码范围 | `--pages 1-5,8,10-12` |
| --bbox | 包含边界框坐标 | `--bbox` |
| --normalize | 返回格式化解析数据 (默认开启) | `--normalize` |
| --raw | 返回原始解析格式 | `--raw` |
| --include-image | markdown 中包含图片 | `--include-image` |
| --image-format | 图片格式 (url/base64) | `--image-format url` |

### extract 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| 文件路径 | 文档文件路径 | `C:\docs\contract.pdf` |
| --schema | 字段 schema（必填） | `--schema '{"fields":[...]}'` |
| --prompt | 提示词模式 schema | `--prompt '{"fields":[...]}'` |
| --schema-ref | 模板引用 | `--schema-ref DocPilot/contract/v1` |
| --options | 扩展配置 | `--options '{"mode":"fast"}'` |

### classify 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| 文件路径 | 文档文件路径 | `C:\docs\mixed.pdf` |
| --mode | 分类模式 | `--mode classify_and_split` |
| --categories | 分类 schema | `--categories '[{"name":"合同","description":"..."}]'` |

---

## 配置

### 方式一：环境变量
```
DOCPilot_BASE_URL=https://docpilot.token-ai.com.cn
DOCPilot_API_KEY=your_api_key
```

### 方式二：配置文件
在技能目录创建 `config.json`：
```json
{
  "base_url": "https://docpilot.token-ai.com.cn",
  "api_key": "your_api_key"
}
```

---

## 输出格式

### parse 输出
- **document_id**: 文档唯一标识
- **page_count**: 页数
- **file_type**: 文件类型
- **pages**: 页面数组（含 elements）
- **sheets**: 工作表数组（Excel/CSV）
- **markdown**: Markdown 格式文本

### extract 输出
- **extraction_id**: 抽取任务 ID
- **fields**: 提取的字段列表（含 evidence 溯源）
- **unfound_fields**: 未找到的字段
- **metadata**: 元数据（耗时、token 数等）

### classify 输出
- **mode**: 分类模式
- **classification**: 分类结果（classify_only 模式）
- **segments**: 文档片段列表（classify_and_split 模式）
- **metadata**: 元数据

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

## 依赖
- requests

## 错误码

| 错误码 | 消息 | 说明 |
|--------|------|------|
| 10000 | Success | 成功 |
| 10001 | Missing parameter | 参数缺失 |
| 10002 | Invalid parameter | 非法参数 |
| 10003 | Invalid file | 文件格式非法 |
| 10004 | Failed to recognize | 识别失败 |
| 10005 | Internal error | 内部错误 |
