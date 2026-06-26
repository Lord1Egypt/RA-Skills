# eastmoney_fin_search - 妙想资讯搜索

基于东方财富妙想搜索能力，基于金融场景进行信源智能筛选，用于获取涉及时效性信息或特定事件信息的任务，包括新闻、公告、研报、政策、交易规则、具体事件、各种影响分析等。

## 功能说明

根据用户问句搜索相关金融资讯，获取与问句相关的资讯信息（如研报、新闻、解读等），并返回可读的文本内容。

## API 接口

- **URL**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search`
- **Header**: `apikey: {MX_APIKEY}`, `Content-Type: application/json`
- **Body**: `{"query": "搜索问句"}`

### 示例

```bash
curl -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
  --header 'Content-Type: application/json' \
  --header 'apikey: YOUR_API_KEY' \
  --data '{"query": "立讯精密的资讯"}'
```

## 使用方式

1. 确认 `MX_APIKEY` 环境变量已配置
2. 构造自然语言搜索问句
3. 发送 POST 请求到上述接口
4. 解析返回的 JSON 数据

### Python 调用

```python
import requests, os

url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"
headers = {
    "Content-Type": "application/json",
    "apikey": os.getenv("MX_APIKEY")
}
data = {"query": "格力电器最新研报"}
response = requests.post(url, headers=headers, json=data, timeout=30)
result = response.json()
```

也可直接使用本套件提供的脚本 `scripts/mx_search.py`：

```bash
python scripts/mx_search.py "格力电器最新研报"
python scripts/mx_search.py "商业航天板块近期新闻" [输出目录]
```

## 问句示例

| 类型 | 示例问句 |
|------|---------|
| 个股资讯 | 格力电器最新研报、贵州茅台机构观点 |
| 板块/主题 | 商业航天板块近期新闻、新能源政策解读 |
| 宏观/风险 | A股具备自然对冲优势的公司、美联储加息对A股影响 |
| 综合解读 | 今日大盘异动原因、北向资金流向解读 |

## 返回结果字段释义

| 字段路径 | 类型 | 简短释义 |
|---------|------|---------|
| `title` | 字符串 | 信息标题，高度概括核心内容 |
| `secuList` | 数组 | 关联证券列表 |
| `secuList[].secuCode` | 字符串 | 证券代码（如 002475） |
| `secuList[].secuName` | 字符串 | 证券名称（如 立讯精密） |
| `secuList[].secuType` | 字符串 | 证券类型（如 股票/债券） |
| `trunk` | 字符串 | 信息核心正文/结构化数据块 |

### 搜索结果数据路径

```
result.data.data.llmSearchResponse.data[]
```

每条结果包含：
- `title` - 标题
- `content` - 正文内容
- `date` - 日期
- `insName` - 机构名称
- `informationType` - 类型（REPORT=研报, NEWS=新闻, ANNOUNCEMENT=公告）
- `rating` - 评级
- `entityFullName` - 关联证券全称
