import requests

# 获取科技/物流新闻
tech_news = requests.get('https://ai.6551.io/open/free_hot?category=tech').json()

print("【搜索京东物流相关新闻】")
print()

# 搜索京东物流相关内容
keywords = ['JD Logistics', '京东物流', '2618', 'logistics', 'delivery']

found = []
if tech_news.get('success'):
    for item in tech_news['news']['items']:
        title = item.get('title', '')
        summary = item.get('summary_en', '')
        text = title + ' ' + summary
        for kw in keywords:
            if kw.lower() in text.lower():
                found.append(item)
                break

if found:
    print(f"找到 {len(found)} 条相关新闻:")
    for i, item in enumerate(found[:5], 1):
        print(f"  {i}. [{item['source']}] {item['title'][:60]}...")
else:
    print("暂无直接相关新闻，列出最新科技热点:")
    for i, item in enumerate(tech_news['news']['items'][:5], 1):
        print(f"  {i}. [{item['source']}] {item['title'][:60]}...")

print()
print("="*50)
print("【京东物流(02618.HK) 基本信息】")
print("="*50)
print()
print("  京东物流是中国领先的物流服务提供商，")
print("  隶属于京东集团(JD.com)。")
print()
print("  股票代码: 02618.HK (港股)")
print("  上市时间: 2021年5月28日")
print("  业务范围: 仓储、配送、供应链管理")
print()
print("  注: 港股数据暂时无法获取实时报价")
print("  建议通过券商APP查看实时行情")
print()
