# 百度智能文档分析平台 - 完整使用指南

## 🚀 首次使用配置

### 第一步：获取AK和SK

1. 访问 [百度智能云控制台](https://console.bce.baidu.com/ai-engine/old/#/ai/ocr/app/list)
2. 登录百度账号
3. 创建应用或选择已有应用
4. 在「全部AI能力」中找到「智能文档分析平台」
5. 点击开通服务
6. 在「应用详情」复制 **AK**（API Key）和 **SK**（Secret Key）

### 第二步：配置凭证

**方式1：配置文件（推荐）**

创建配置文件 `~/.baidu_doc_ai_config`：

```ini
[credentials]
api_key = 您的API_KEY
secret_key = 您的SECRET_KEY
```

**方式2：环境变量**

```bash
export BAIDU_DOC_AI_API_KEY=您的API_KEY
export BAIDU_DOC_AI_SECRET_KEY=您的SECRET_KEY
```

### 第三步：开始使用

凭证配置好后，直接使用即可：

```python
from scripts.baidu_api_client import BaiduDocAIClient

client = BaiduDocAIClient()
result = client.extract(file_data=file_data, manifest=[{"key": "姓名"}])
```

---

## 完整API参数说明

### 文档抽取 (Extract)

**功能**：从文档中提取指定字段信息

**命令**：
```bash
python scripts/baidu_doc_cli.py extract \
  --file /path/to/document.pdf \
  --fields '[{"key": "合同名称", "description": "合同的名称"}]' \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | string | 是* | 本地文件路径（与--file-url二选一） |
| `--file-url` | string | 是* | 文件URL（与--file二选一） |
| `--fields` | JSON | 是* | 抽取字段列表，JSON格式（与--manifest-version-id二选一） |
| `--manifest-version-id` | string | 是* | 清单版本ID（与--fields二选一） |
| `--remove-duplicates` | bool | 否 | 开启字段值去重 |
| `--page-range` | string | 否 | 指定页抽取，如: `1,5-10,15` |
| `--extract-seal` | bool | 否 | 开启印章抽取 |
| `--erase-watermark` | bool | 否 | 开启水印去除 |
| `--doc-correct` | bool | 否 | 开启图像矫正 |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**字段配置格式**：
```json
[
  {
    "key": "字段名称",
    "description": "字段说明（可选）",
    "parentKey": "root"  // 单字段时为root，组合字段时为组合名称
  }
]
```

**示例**：
```bash
# 基础用法
python scripts/baidu_doc_cli.py extract \
  --file /Users/shenjunyu/Desktop/测试case/文档抽取/00d56136-47d6-4f02-867c-257d989d77c2.jpg \
  --fields '[{"key": "合同名称"}, {"key": "合同金额"}]'

# 使用所有参数
python scripts/baidu_doc_cli.py extract \
  --file document.pdf \
  --fields '[{"key": "合同名称"}]' \
  --extract-seal \
  --erase-watermark \
  --page-range "1-5" \
  --output result.json
```

---

### 文档解析 (Parse)

**功能**：通用文档解析，提取文本和表格

**命令**：
```bash
python scripts/baidu_doc_cli.py parse \
  --file /path/to/document.pdf \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | string | 是* | 本地文件路径（与--file-url二选一） |
| `--file-url` | string | 是* | 文件URL（与--file二选一） |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**示例**：
```bash
python scripts/baidu_doc_cli.py parse \
  --file /Users/shenjunyu/Desktop/测试case/文档解析:文档解析VLM/rag-公式.pdf \
  --output parse_result.json
```

---

### 文档解析 VL (Parse VL) ⭐ 推荐

**功能**：多模态文档解析，支持复杂文档、跨页表格、多语言

**命令**：
```bash
python scripts/baidu_doc_cli.py parse-vl \
  --file /path/to/document.pdf \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | string | 是* | 本地文件路径（与--file-url二选一） |
| `--file-url` | string | 是* | 文件URL（与--file二选一） |
| `--file-name` | string | 否 | 文件名（使用--file-url时建议提供） |
| `--analysis-chart` | bool | 否 | 解析统计图表 |
| `--merge-tables` | bool | 否 | 合并跨页表格 |
| `--relevel-titles` | bool | 否 | 标题分级 |
| `--recognize-seal` | bool | 否 | 识别印章内容 |
| `--return-span-boxes` | bool | 否 | 返回行坐标 |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**示例**：
```bash
# 基础用法
python scripts/baidu_doc_cli.py parse-vl \
  --file /Users/shenjunyu/Desktop/测试case/文档解析:文档解析VLM/rag-公式.pdf

# 使用所有参数
python scripts/baidu_doc_cli.py parse-vl \
  --file document.pdf \
  --analysis-chart \
  --merge-tables \
  --relevel-titles \
  --recognize-seal \
  --return-span-boxes \
  --output result.json
```

---

### 文档比对 (Compare)

**功能**：两份文档差异对比

**命令**：
```bash
python scripts/baidu_doc_cli.py compare \
  --base-file /path/to/base.pdf \
  --compare-file /path/to/compare.pdf \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--base-file` | string | 是* | 主版文件路径（与--base-file-url二选一） |
| `--base-file-url` | string | 是* | 主版文件URL（与--base-file二选一） |
| `--compare-file` | string | 是* | 副版文件路径（与--compare-file-url二选一） |
| `--compare-file-url` | string | 是* | 副版文件URL（与--compare-file二选一） |
| `--seal-recognition` | bool | 否 | 识别印章差异 |
| `--hand-writing-recognition` | bool | 否 | 识别手写体差异 |
| `--font-family-recognition` | bool | 否 | 识别字体差异 |
| `--font-size-recognition` | bool | 否 | 识别字号差异 |
| `--full-width-half-width-recognition` | bool | 否 | 识别中英文符号差异 |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**示例**：
```bash
# 基础用法
python scripts/baidu_doc_cli.py compare \
  --base-file /Users/shenjunyu/Desktop/测试case/文档比对/合同.pdf \
  --compare-file /Users/shenjunyu/Desktop/测试case/文档比对/合同-审核.docx

# 使用所有参数
python scripts/baidu_doc_cli.py compare \
  --base-file base.pdf \
  --compare-file compare.pdf \
  --seal-recognition \
  --hand-writing-recognition \
  --font-family-recognition \
  --font-size-recognition \
  --full-width-half-width-recognition \
  --output result.json
```

---

### 合同审查 (Contract Review)

**功能**：合同风险点识别

**命令**：
```bash
python scripts/baidu_doc_cli.py contract-review \
  --file /path/to/contract.pdf \
  --template Sales_PartyA_V2 \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | string | 是* | 本地文件路径（与--file-url二选一） |
| `--file-url` | string | 是* | 文件URL（与--file二选一） |
| `--template` | string | 是 | 合同类型模板（见下表） |
| `--risk-level` | string | 否 | 风险等级筛选：`normal`/`major`/`all` |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**支持的合同类型模板**：

| 模板名称 | 说明 |
|---------|------|
| `Sales_PartyA_V2` | 买卖合同-买方 |
| `Sales_PartyB_V2` | 买卖合同-卖方 |
| `Lease_PartyA_V2` | 租赁合同-出租方 |
| `Lease_PartyB_V2` | 租赁合同-承租方 |
| `TechDev_PartyA_V2` | 技术开发合同-委托方 |
| `TechDev_PartyB_V2` | 技术开发合同-受托方 |
| `Labor_PartyA_V2` | 劳动合同-用人单位 |
| `Labor_PartyB_V2` | 劳动合同-劳动者 |
| `Entrustment_PartyA_V2` | 委托合同-委托方 |
| `Entrustment_PartyB_V2` | 委托合同-受托方 |

**示例**：
```bash
# 基础用法
python scripts/baidu_doc_cli.py contract-review \
  --file /Users/shenjunyu/Desktop/测试case/合同审查/地方市政配套工程下穿铁路技术合同书.pdf \
  --template TechDev_PartyA_V2

# 筛选风险等级
python scripts/baidu_doc_cli.py contract-review \
  --file contract.pdf \
  --template Sales_PartyA_V2 \
  --risk-level major \
  --output result.json
```

---

### 文档格式转换 (Convert)

**功能**：文档格式转换（PDF转Word、图片转PDF等）

**命令**：
```bash
python scripts/baidu_doc_cli.py convert \
  --file /path/to/document.pdf \
  [可选参数]
```

**所有参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--file` | string | 是* | 本地文件路径（与--file-url二选一） |
| `--file-url` | string | 是* | 文件URL（与--file二选一） |
| `--callback-url` | string | 否 | 回调URL |
| `--output` | string | 否 | 输出文件路径 |

**示例**：
```bash
python scripts/baidu_doc_cli.py convert \
  --file document.pdf \
  --output result.json
```

---

## 文件路径自动转Base64

所有命令都支持使用本地文件路径，工具会自动将文件转换为Base64编码：

```bash
# 使用本地文件路径（自动转Base64）
python scripts/baidu_doc_cli.py extract \
  --file /path/to/document.pdf \
  --fields '[{"key": "字段"}]'

# 等价于手动转Base64后使用URL
# 但使用本地路径更方便！
```

---

## 高级用法

### 1. 使用Python API客户端

```python
from scripts.baidu_api_client import BaiduDocAIClient

# 初始化客户端
client = BaiduDocAIClient(api_key="xxx", secret_key="xxx")

# 文档抽取
result = client.extract(
    file_url="https://example.com/document.pdf",
    manifest=[{"key": "合同名称"}]
)

# 或使用本地文件
file_data = client.file_to_base64("/path/to/document.pdf")
result = client.extract(
    file_data=file_data,
    file_name="document.pdf",
    manifest=[{"key": "合同名称"}]
)
```

### 2. 批量处理

```bash
# 处理目录中的所有PDF文件
for file in /path/to/documents/*.pdf; do
  python scripts/baidu_doc_cli.py parse \
    --file "$file" \
    --output "${file%.pdf}_result.json"
done
```

### 3. 使用回调URL

```bash
python scripts/baidu_doc_cli.py extract \
  --file document.pdf \
  --fields '[{"key": "字段"}]' \
  --callback-url "https://your-server.com/callback"
```

---

## 常见问题

### Q: 如何设置环境变量？

```bash
# 临时设置（仅当前终端有效）
export BAIDU_DOC_AI_API_KEY="your_api_key"
export BAIDU_DOC_AI_SECRET_KEY="your_secret_key"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export BAIDU_DOC_AI_API_KEY="your_api_key"' >> ~/.zshrc
echo 'export BAIDU_DOC_AI_SECRET_KEY="your_secret_key"' >> ~/.zshrc
source ~/.zshrc
```

### Q: 支持哪些文件格式？

| API | 支持格式 | 最大大小 |
|-----|---------|---------|
| 文档抽取 | PDF、图片、Word、Excel、OFD | 50MB |
| 文档解析 | PDF、图片、Word、Excel | 10MB |
| 文档解析VL | PDF、图片 | 100MB/500页 |
| 文档比对 | PDF、图片、Word | 50MB |
| 合同审查 | PDF、Word | 10MB |
| 格式转换 | PDF、图片 | 4-10MB |

### Q: 轮询超时怎么办？

合同审查通常需要1-2分钟，其他API需要5-10秒。如果超时，可以：
1. 增加轮询超时时间
2. 使用回调URL异步获取结果

### Q: 如何处理错误？

所有错误都会打印到stderr，可以通过检查返回码判断：
```bash
python scripts/baidu_doc_cli.py extract ... || echo "执行失败"
```

---

## 参考文档

- [文档抽取API](https://ai.baidu.com/ai-doc/OCR/klzkwzdch)
- [文档解析API](https://ai.baidu.com/ai-doc/OCR/llxst5nn0)
- [文档解析VL API](https://ai.baidu.com/ai-doc/OCR/3mi73at9o)
- [文档比对API](https://ai.baidu.com/ai-doc/OCR/Glqd7jgmf)
- [合同审查API](https://ai.baidu.com/ai-doc/OCR/olqc085rg)
- [文档格式转换API](https://ai.baidu.com/ai-doc/OCR/Elf3sp7cz)
