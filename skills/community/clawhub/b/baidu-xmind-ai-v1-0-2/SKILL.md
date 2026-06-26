---
name: baidu-xmind-ai
version: 1.0.0
description: 百度智能文档分析平台API调用技能。支持文档抽取、文档解析、文档解析(PaddleOCR-VL)、文档比对、合同审查、文档格式转换等功能。当用户需要：(1) 从文档中提取特定字段信息，(2) 解析文档内容，(3) 比对两份文档差异，(4) 审查合同风险，(5) 转换文档格式时使用此技能。触发词：文档抽取、文档解析、PaddleOCR、文档比对、合同审查、格式转换、智能文档分析、百度文档AI。
license: MIT
permissions:
  network:
    - https://aip.baidubce.com  # 百度智能文档分析API
  credentials:
    - BAIDU_DOC_AI_API_KEY
    - BAIDU_DOC_AI_SECRET_KEY
  files:
    read: user-provided files only
---

# 百度智能文档分析平台 API 技能

百度智能文档分析平台提供多种文档处理能力，包括文档抽取、文档解析、文档比对、合同审查、文档格式转换等功能。

## 功能概览

| 功能 | 说明 | 适用场景 |
|------|------|---------|
| **文档抽取** | 自定义字段抽取，精准定位字段值 | 合同、票据、订单等结构化抽取 |
| **文档解析** | 通用文档解析，提取文本和表格 | 各类文档的内容提取 |
| **文档解析(PaddleOCR-VL)** | 多模态文档解析SOTA方案 | 复杂文档、跨页表格、多语言文档 |
| **文档比对** | 两份文档差异对比 | 合同修订、版本对比 |
| **合同审查** | 合同风险点识别 | 合同审核、合规检查 |
| **文档格式转换** | 文档格式转换 | PDF转Word、图片转PDF等 |

## ⚠️ 安全说明

### 凭证配置

所有API调用需要百度API凭证（API Key 和 Secret Key）：

**方式1：环境变量（推荐）**
```bash
export BAIDU_DOC_AI_API_KEY="您的API_KEY"
export BAIDU_DOC_AI_SECRET_KEY="您的SECRET_KEY"
```

**方式2：配置文件**
```bash
# 创建 ~/.baidu_doc_ai_config
[credentials]
api_key = 您的API_KEY
secret_key = 您的SECRET_KEY
```

### 网络安全

- 此技能仅与百度官方API通信：`aip.baidubce.com`
- 不与任何第三方服务器通信

## API调用模式

### 异步API

所有API均为异步接口，需要两步操作：

1. **提交请求** - 获取 taskId/task_id
2. **轮询结果** - 根据 taskId 查询处理结果

**建议轮询时间**：
- 文档抽取：**5秒**后开始轮询
- 文档解析：5-10秒后开始轮询
- 合同审查：1-2分钟后开始轮询
- 文档比对：5-10秒后开始轮询

## 使用脚本

技能提供了Python脚本，简化API调用：

### 统一命令行工具

所有功能集成在一个脚本中：

```bash
# 文档抽取
python scripts/baidu_doc_cli.py extract \
  --file document.pdf \
  --fields '[{"key": "合同名称"}, {"key": "合同金额"}]'

# 文档解析
python scripts/baidu_doc_cli.py parse --file document.pdf

# 文档解析VL
python scripts/baidu_doc_cli.py parse-vl \
  --file document.pdf \
  --analysis-chart --merge-tables

# 文档比对
python scripts/baidu_doc_cli.py compare \
  --base-file doc1.pdf \
  --compare-file doc2.pdf

# 合同审查
python scripts/baidu_doc_cli.py contract-review \
  --file contract.pdf \
  --template Sales_PartyA_V2

# 格式转换
python scripts/baidu_doc_cli.py convert --file document.pdf
```

### Python API

```python
from scripts.baidu_api_client import BaiduDocAIClient

# 初始化客户端
client = BaiduDocAIClient()

# 文档抽取
result = client.extract(
    file_data=file_data,
    manifest=[{"key": "合同名称"}, {"key": "合同金额"}]
)

# 文档解析
result = client.parse(
    file_data=file_data,
    file_name="document.pdf"
)

# 合同审查
result = client.contract_review(
    file_data=file_data,
    template_name="Sales_PartyA_V2"
)
```

## 合同类型模板

合同审查支持的合同类型：

| 模板名称 | 说明 |
|---------|------|
| Sales_PartyA_V2 | 买卖合同-买方 |
| Sales_PartyB_V2 | 买卖合同-卖方 |
| Lease_PartyA_V2 | 租赁合同-出租方 |
| Lease_PartyB_V2 | 租赁合同-承租方 |
| TechDev_PartyA_V2 | 技术开发合同-委托方 |
| TechDev_PartyB_V2 | 技术开发合同-受托方 |
| Labor_PartyA_V2 | 劳动合同-用人单位 |
| Labor_PartyB_V2 | 劳动合同-劳动者 |

完整模板列表见：`references/contract_review.md`

## 错误处理

常见错误码及处理方式：

| 错误码 | 错误信息 | 解决方案 |
|--------|---------|---------|
| 110/111 | access_token无效或过期 | 重新获取token |
| 216200 | 文件或文件路径为空 | 检查文件URL |
| 216201 | 文件格式错误 | 确认文件格式支持 |
| 216202 | 文件大小异常 | 文件需小于限制 |
| 282000 | 内部错误 | 重试或联系技术支持 |
| 283016 | 请求参数不合法 | 检查参数格式 |

## 配额和限制

| API | QPS限制 | 文件大小限制 | 支持格式 |
|-----|---------|-------------|---------|
| 文档抽取 | 提交2/查询10 | 50MB | PDF、图片、Word、Excel、OFD |
| 文档解析 | 提交2/查询10 | 10MB | PDF、图片、Word、Excel |
| 文档解析(VL) | 提交2/查询10 | 100MB/500页 | PDF、图片 |
| 文档比对 | 提交2/查询10 | 50MB | PDF、图片、Word |
| 合同审查 | 提交2/查询10 | 10MB | PDF、Word |
| 格式转换 | 提交2/查询10 | 4-10MB | PDF、图片 |

## 参考文档

详细的API文档请参考 `references/` 目录：
- `doc_extract.md` - 文档抽取API详细文档
- `doc_parse.md` - 文档解析API详细文档
- `doc_parse_vl.md` - 文档解析(PaddleOCR-VL)API详细文档
- `doc_compare.md` - 文档比对API详细文档
- `contract_review.md` - 合同审查API详细文档
- `doc_convert.md` - 文档格式转换API详细文档

## 相关链接

- [智能文档分析平台控制台](https://console.bce.baidu.com/textmind/application/textExtract)
- [API文档](https://ai.baidu.com/ai-doc/OCR/klzkwzdch)
