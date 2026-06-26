# 百度文档AI技能 - 快速开始

## 🚀 首次使用配置

### 第一步：获取AK和SK

1. 访问 [百度智能云控制台](https://console.bce.baidu.com/ai-engine/old/#/ai/ocr/app/list)
2. 创建应用或选择已有应用
3. 开通「智能文档分析平台」API
4. 复制 **AK** 和 **SK**

### 第二步：配置凭证

**方式1：配置文件（推荐）**

```bash
cat > ~/.baidu_doc_ai_config << 'EOF'
[credentials]
api_key = 您的API_KEY
secret_key = 您的SECRET_KEY
EOF
```

**方式2：环境变量**

```bash
export BAIDU_DOC_AI_API_KEY=您的API_KEY
export BAIDU_DOC_AI_SECRET_KEY=您的SECRET_KEY
```

### 第三步：安装依赖

```bash
pip install requests
```

---

## 命令速查

### 文档抽取
```bash
python scripts/baidu_doc_cli.py extract \
  --file document.pdf \
  --fields '[{"key": "合同名称"}, {"key": "合同金额"}]'
```

### 文档解析
```bash
python scripts/baidu_doc_cli.py parse --file document.pdf
```

### 文档解析VL
```bash
python scripts/baidu_doc_cli.py parse-vl \
  --file document.pdf \
  --analysis-chart --merge-tables
```

### 文档比对
```bash
python scripts/baidu_doc_cli.py compare \
  --base-file base.pdf \
  --compare-file compare.pdf
```

### 合同审查
```bash
python scripts/baidu_doc_cli.py contract-review \
  --file contract.pdf \
  --template Sales_PartyA_V2
```

### 格式转换
```bash
python scripts/baidu_doc_cli.py convert --file document.pdf
```

---

## 合同模板速查

| 模板 | 说明 |
|------|------|
| Sales_PartyA_V2 | 买卖合同-买方 |
| Sales_PartyB_V2 | 买卖合同-卖方 |
| Lease_PartyA_V2 | 租赁合同-出租方 |
| ConstCtrl_PartyA_V2 | 建设工程施工合同-发包方 |
| ConstCtrl_PartyB_V2 | 建设工程施工合同-承包方 |

完整模板列表见: `references/contract_review.md`

---

## Python API

```python
from scripts.baidu_api_client import BaiduDocAIClient

client = BaiduDocAIClient()

# 文档抽取
result = client.extract(
    file_data=file_data,
    manifest=[{"key": "字段"}]
)

# 文档解析VL
result = client.parse_vl(
    file_data=file_data,
    analysis_chart=True
)

# 合同审查
result = client.contract_review(
    file_data=file_data,
    template_name="Sales_PartyA_V2"
)
```

---

## 更多信息

- 完整文档: `USAGE.md`
- API参考: `references/`
