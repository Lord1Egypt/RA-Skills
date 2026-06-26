# 使用示例

## 示例1：基本使用
```python
from scripts.collect_categories import collect_category_links

# 定义分类链接
links = [
    "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops",
    "https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear",
    "https://lulumonclick-eu.shop/collections/men-men-clothes-t-shirts"
]

# 采集数据
csv_path = collect_category_links(links)

print(f"文件已保存: {csv_path}")
```

## 示例2：自定义输出目录
```python
from scripts.collect_categories import collect_category_links

links = [
    "https://example.com/collections/category-subcategory"
]

# 使用自定义输出目录
csv_path = collect_category_links(
    links, 
    output_dir="/path/to/your/custom/directory"
)
```

## 示例3：从文本文件读取链接
```python
from scripts.collect_categories import collect_category_links

# 从文件读取链接
def read_links_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    return links

# 读取链接并处理
links = read_links_from_file("links.txt")
csv_path = collect_category_links(links)
```

## 示例4：命令行使用
```bash
# 运行脚本
python scripts/collect_categories.py

# 使用自定义输出目录
python scripts/collect_categories.py /path/to/output

# 批量处理链接文件
python -c "
from scripts.collect_categories import collect_category_links
links = ['https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops']
collect_category_links(links)
"
```

## 输出示例
生成的CSV文件内容示例：

```csv
完整链接,分类路径,一级分类,二级分类,域名
https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops,women-women-clothes-tank-tops,Women,Tank Tops,lulumonclick-eu.shop
https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear,women-women-clothes-bras-underwear,Women,Bras Underwear,lulumonclick-eu.shop
https://lulumonclick-eu.shop/collections/men-men-clothes-t-shirts,men-men-clothes-t-shirts,Men,T Shirts,lulumonclick-eu.shop
```

## 扩展功能示例

### 添加时间戳
```python
import pandas as pd
from datetime import datetime

def add_timestamp_to_csv(csv_path):
    df = pd.read_csv(csv_path)
    df['采集时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
```

### 批量处理多个网站
```python
def process_multiple_websites(website_links):
    """
    处理多个网站的分类链接
    website_links: {'网站1': [链接列表], '网站2': [链接列表]}
    """
    for website_name, links in website_links.items():
        csv_path = collect_category_links(links)
        print(f"{website_name}: {csv_path}")
```

### 验证链接格式
```python
import re

def validate_category_link(url):
    """验证链接是否为有效的分类链接"""
    pattern = r'^https?://[^/]+/collections/[^/?]+$'
    return bool(re.match(pattern, url))

# 过滤有效链接
valid_links = [link for link in links if validate_category_link(link)]
```