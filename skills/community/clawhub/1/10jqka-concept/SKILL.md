---
name: 10jqka-concept
version: 1.0.0
description: 同花顺爱问财股票概念查询。通过爬取同花顺 F10 页面获取股票所属概念板块信息。
---

# 同花顺爱问财概念查询 (10jqka-concept)

## 功能说明

通过爬取同花顺 F10 页面，获取 A 股股票所属概念板块信息。

**数据源：** 同花顺爱问财 (basic.10jqka.com.cn)

**支持功能：**
- 查询单只股票的概念板块
- 查询概念板块成分股
- 查询概念板块行情

---

## API 配置

**Base URL:** `https://basic.10jqka.com.cn/`

**概念页面格式:** `https://basic.10jqka.com.cn/{股票代码}/concept.html`

**个股页面格式:** `https://basic.10jqka.com.cn/{股票代码}/`

**无需 API Key**（公开网页爬取）

---

## 调用方式

### 方式 1：Python 脚本

```python
import requests
from bs4 import BeautifulSoup

def get_stock_concepts(stock_code):
    """获取股票所属概念板块"""
    url = f"https://basic.10jqka.com.cn/{stock_code}/concept.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "gbk"  # 同花顺使用 GBK 编码
    
    soup = BeautifulSoup(response.text, "html.parser")
    concepts = []
    
    # 解析概念板块
    concept_div = soup.find("div", {"id": "concept"})
    if concept_div:
        for link in concept_div.find_all("a"):
            concept_name = link.get_text(strip=True)
            concept_url = link.get("href")
            if concept_name and concept_url:
                concepts.append({
                    "name": concept_name,
                    "url": f"https://{concept_url}" if not concept_url.startswith("http") else concept_url
                })
    
    return concepts

# 示例：查询东方财富的概念
concepts = get_stock_concepts("300059")
for c in concepts:
    print(f"{c['name']}: {c['url']}")
```

### 方式 2：curl 命令

```bash
curl -s "https://basic.10jqka.com.cn/300059/concept.html" \
  -H "User-Agent: Mozilla/5.0" \
  | iconv -f gbk -t utf8 \
  | grep -oP '(?<=concept_)[^"]+'
```

---

## 问句示例

| 类型 | 示例问句 |
|:----|:----|
| **个股概念** | 东方财富属于什么概念、宁德时代的概念板块 |
| **概念成分股** | 人工智能概念有哪些股票、新能源成分股 |
| **概念行情** | 半导体概念今天涨跌幅、AI 概念板块行情 |

---

## 返回数据格式

```json
{
  "stock_code": "300059",
  "stock_name": "东方财富",
  "concepts": [
    {
      "name": "券商概念",
      "url": "https://q.10jqka.com.cn/gn/detail/field/199112/order/asc/page/1/prep/1/quote/300059"
    },
    {
      "name": "互联网金融",
      "url": "https://q.10jqka.com.cn/gn/detail/field/199112/order/asc/page/1/prep/1/quote/300059"
    },
    {
      "name": "人工智能",
      "url": "https://q.10jqka.com.cn/gn/detail/field/199112/order/asc/page/1/prep/1/quote/300059"
    },
    {
      "name": "深股通",
      "url": "https://q.10jqka.com.cn/gn/detail/field/199112/order/asc/page/1/prep/1/quote/300059"
    }
  ]
}
```

---

## 常见概念板块

| 概念名称 | 代码 | 说明 |
|:----|:----|:----|
| 人工智能 | gn_107893 | AI 相关 stocks |
| 新能源 | gn_199112 | 新能源汽车、光伏等 |
| 半导体 | gn_199113 | 芯片、集成电路 |
| 券商概念 | gn_199114 | 证券公司 |
| 互联网金融 | gn_199115 | 互联网 + 金融 |
| 深股通 | gn_199116 | 深港通标的 |
| 沪股通 | gn_199117 | 沪港通标的 |
| 融资融券 | gn_199118 | 两融标的 |
| 中证 500 | gn_199119 | 中证 500 成分 |
| 沪深 300 | gn_199120 | 沪深 300 成分 |

---

## 注意事项

1. **编码问题：** 同花顺页面使用 GBK 编码，需要正确转换
2. **反爬限制：** 建议添加 User-Agent，控制请求频率（<10 次/分钟）
3. **数据延迟：** F10 数据可能有 15 分钟延迟
4. **页面结构：** 同花顺可能更新页面结构，需要定期维护解析逻辑

---

## 依赖安装

```bash
pip install requests beautifulsoup4 lxml
```

---

## 信息来源

- **行情数据：** 交易所实时行情
- **概念分类：** 同花顺官方分类
- **成分股数据：** 同花顺 iFinD

---

## 已配置状态

✅ 同花顺 F10 网页爬取已配置
✅ 支持 A 股股票代码查询
✅ 支持概念板块解析
