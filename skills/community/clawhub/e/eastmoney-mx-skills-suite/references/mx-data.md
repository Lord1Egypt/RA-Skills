# eastmoney_fin_data - 妙想金融数据查询

基于东方财富权威数据库及最新行情底层数据构建，支持通过自然语言查询以下三类数据：

1. **行情类数据** - 股票、行业、板块、指数、基金、债券的实时行情、主力资金流向、估值等
2. **财务类数据** - 上市公司基本信息、财务指标、高管信息、主营业务、股东结构、融资情况等
3. **关系与经营类数据** - 关联关系数据、企业经营相关数据

## API 接口

- **URL**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/query`
- **Header**: `apikey: {MX_APIKEY}`, `Content-Type: application/json`
- **Body**: `{"toolQuery": "查询问句"}`

### 示例

```bash
curl -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
  --header 'Content-Type: application/json' \
  --header 'apikey: YOUR_API_KEY' \
  --data '{"toolQuery": "东方财富最新价"}'
```

## 使用方式

1. 确认 `MX_APIKEY` 环境变量已配置
2. 构造自然语言查询问句（如 "贵州茅台最近3年每日收盘价"）
3. 发送 POST 请求到上述接口
4. 解析返回的 JSON 数据

### Python 调用

```python
import requests, os

url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"
headers = {
    "Content-Type": "application/json",
    "apikey": os.getenv("MX_APIKEY")
}
data = {"toolQuery": "东方财富最新价"}
response = requests.post(url, headers=headers, json=data, timeout=30)
result = response.json()
```

也可直接使用本套件提供的脚本 `scripts/mx_data.py`：

```bash
python scripts/mx_data.py "东方财富最新价"
python scripts/mx_data.py "贵州茅台最近3年每日收盘价" [输出目录]
```

## 返回结果字段释义

### 一级核心路径：`data`

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `data.questionId` | 字符串 | 查数请求唯一标识 ID |
| `data.dataTableDTOList` | 数组 | 【核心】标准化后的证券指标数据列表 |
| `data.rawDataTableDTOList` | 数组 | 原始未加工的证券指标数据列表 |
| `data.condition` | 对象 | 本次查询条件 |
| `data.entityTagDTOList` | 数组 | 关联证券主体汇总信息 |

### 二级核心路径：`data.dataTableDTOList[]`

#### 证券基础信息

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `.code` | 字符串 | 证券完整代码（如 300059.SZ） |
| `.entityName` | 字符串 | 证券全称（如 东方财富 (300059.SZ)） |
| `.title` | 字符串 | 指标数据标题（如 东方财富最新价） |

#### 表格数据核心

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `.table` | 对象 | 【核心】标准化表格数据，键=指标编码，值=指标数值数组；`headName`为时间列 |
| `.rawTable` | 对象 | 原始表格数据，未做标准化处理 |
| `.nameMap` | 对象 | 【核心】列名映射，将指标编码转为中文（如 f2 → 最新价） |
| `.indicatorOrder` | 数组 | 指标列展示排序 |

#### 指标元信息

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `.dataType` | 字符串 | 数据来源类型 |
| `.dataTypeEnum` | 字符串 | 枚举值（HQ=行情，DATA_BROWSER=数据浏览器） |
| `.field` | 对象 | 指标详细元信息（编码、名称、时间范围、粒度等） |

#### 证券标签

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `.entityTagDTO.secuCode` | 字符串 | 证券纯代码（如 300059） |
| `.entityTagDTO.marketChar` | 字符串 | 市场标识（.SZ=深交所，.SH=上交所） |
| `.entityTagDTO.entityTypeName` | 字符串 | 证券类型（如 A股/港股/债券） |
| `.entityTagDTO.fullName` | 字符串 | 证券中文名 |
| `.entityTagDTO.className` | 字符串 | 证券大类（如 沪深京股票/创业板股票） |

### 三级：`field` 元信息

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `.returnCode` | 字符串 | 指标唯一编码 |
| `.returnName` | 字符串 | 指标中文名（如 最新价/收盘价） |
| `.returnSourceCode` | 字符串 | 原始来源编码（如 f2/CLOSE） |
| `.startDate/.endDate` | 字符串 | 查询时间范围 |
| `.dateGranularity` | 字符串 | 数据粒度（DAY/MIN等） |

## 注意事项

- 避免查询大数据范围（如某股票3年每日最新价），可能导致返回内容过多
- 数据结果为空时，提示用户到东方财富妙想 AI 查询
- 请求失败时，检查 API Key 是否正确、网络是否正常
