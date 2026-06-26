# OpenAlex API 字段说明

## 搜索接口

```
GET https://api.openalex.org/works?search=QUERY&per_page=N
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `search` | 关键词搜索 | `search=multi-agent control` |
| `per_page` | 每页数量 | `per_page=10` |
| `page` | 页码 | `page=1` |
| `filter` | 筛选条件 | `filter=publication_year:2023` |
| `sort` | 排序 | `sort=cited_by_count:desc` |

### Filter 语法

```
filter=field:value          # 精确匹配
filter=field:>value         # 大于
filter=field:<value         # 小于
filter=field:value1|value2  # 或
filter=field1:value1,field2:value2  # 且
```

### 常用 filter 字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `publication_year` | 发表年份 | `publication_year:2020-2025` |
| `cited_by_count` | 被引量 | `cited_by_count:>50` |
| `primary_location.source.id` | 期刊ID | `primary_location.source.id:S12345` |
| `open_access.is_oa` | 是否开放获取 | `open_access.is_oa:true` |
| `type` | 文献类型 | `type:article` |

## 返回字段

### Work 对象

```json
{
  "id": "https://openalex.org/W1234567890",
  "doi": "https://doi.org/10.1109/xxx",
  "title": "Paper Title",
  "publication_year": 2023,
  "cited_by_count": 100,
  "open_access": {
    "is_oa": true,
    "oa_url": "https://example.com/paper.pdf"
  },
  "authorships": [
    {
      "author": {
        "id": "https://openalex.org/A12345",
        "display_name": "John Doe"
      },
      "institutions": [...]
    }
  ],
  "primary_location": {
    "source": {
      "display_name": "IEEE Transactions on...",
      "issn": "1234-5678"
    }
  },
  "concepts": [...],
  "referenced_works": [...],
  "related_works": [...]
}
```

### 获取单篇论文

```
GET https://api.openalex.org/works/doi:10.1109/xxx
GET https://openalex.org/W1234567890
```

### 搜索作者

```
GET https://api.openalex.org/authors?search=John+Doe
```

### 搜索期刊/来源

```
GET https://api.openalex.org/sources?search=IEEE+Transactions
```

## Rate Limits

- 无需API Key：100,000次/天，10次/秒
- 有API Key：无限制
- 注册地址：https://openalex.org/#api-key

## 中国机构ID

| 机构 | OpenAlex ID |
|------|-------------|
| 清华大学 | I12345... |
| 北京大学 | I12345... |
| 浙江大学 | I12345... |

可通过机构筛选论文：
```
filter=authorships.institutions.id:I12345
```
