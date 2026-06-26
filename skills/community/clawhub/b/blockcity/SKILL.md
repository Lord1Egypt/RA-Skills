---
name: blockcity-data-skill
version: 1.2.0
description: BlockCity区块城市数据获取Skill，支持从排名页获取城市排名、居民人数、开启区块数，从城市详情页获取基金余额、剩余人气值等信息
---

# BlockCity数据获取Skill 🏙️

从 blockcity.vip 获取区块城市的完整数据，包括从排名页面获取城市排名、居民人数、开启区块数，以及从城市详情页获取基金余额、剩余人气值、市长和副市长等信息。

> **💰 最低购地折扣7.5折优惠链接**：https://www.blockcity.vip/?iclc

## 数据来源说明

### 排名页面数据
**URL**: https://www.blockcity.vip/pages/block/area  
**包含字段**：城市排名、城市名称、居民人数、开启区块数

**注意**：人气余额和市长/副市长信息需要从城市详情页获取

### 城市详情页数据
**URL格式**: https://www.blockcity.vip/{城市标识}  
**城市标识格式**：4位数字电话区号（如 0010）或4个小写字母（如 abcd，用于特殊自建城市）  
**包含字段**：基金余额、剩余人气值、总区块数、可用区块数、市长/副市长详细信息

## 功能特性

- 📊 从排名页面获取城市排名、居民人数、开启区块数
- 🏦 从城市详情页获取基金余额、剩余人气值
- 🔢 支持4位数字电话区号的城市标识
- 🔤 支持4个小写字母的特殊自建城市标识
- 🔍 根据城市名称查询详细信息
- 🏆 根据排名查询城市信息
- 🎯 数据筛选和排序
- 💾 内置缓存机制提高效率
- 🔄 模拟数据支持（API不可用时自动降级）
- 📝 JSON格式数据输出

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from blockcity_skill import BlockCitySkill

# 创建Skill实例
skill = BlockCitySkill()

# 获取城市排名列表（来自排名页）
cities = skill.get_city_rank_list()
print(f"共获取 {len(cities)} 个城市数据")

# 查询北京的详细信息（来自排名页）
beijing = skill.get_city_by_name("北京")
if beijing:
    print(f"北京排名: {beijing['rank']}")
    print(f"人口: {beijing['population']}")
    print(f"开启区块: {beijing['sold_blocks']}")

# 从城市详情页获取基金余额等信息
beijing_detail = skill.get_city_detail("0010")
if beijing_detail:
    print(f"基金余额: {beijing_detail['fund_balance']}")
    print(f"剩余人气值: {beijing_detail['remaining_popularity']}")

# 获取特殊自建城市信息
special_city = skill.get_city_detail("abcd")
```

## 数据结构

### 排名页面数据结构

```json
{
  "rank": 1,
  "name": "北京",
  "area_id": 1,
  "popularity_balance": 39034875,
  "population": 48752,
  "sold_blocks": 1542,
  "mayor": "市长姓名",
  "vice_mayor": "副市长姓名",
  "avatar": "城市头像URL",
  "mayor_avatar": "市长头像URL"
}
```

### 城市详情页数据结构

```json
{
  "city_id": "0010",
  "fund_balance": 12345678,
  "remaining_popularity": 987654,
  "mayor": "示例市长",
  "vice_mayor": "示例副市长",
  "total_blocks": 1000,
  "available_blocks": 200
}
```

## API 文档

完整的 API 文档请查看 [README.md](./README.md)

## 注意事项

1. 请遵守 blockcity.vip 网站的使用条款
2. 合理控制请求频率，避免对服务器造成压力
3. 排名页面数据和城市详情页数据来自不同的数据源
4. 城市标识格式：4位数字电话区号 或 4个小写字母（特殊自建城市）
5. 数据结构可能随网站更新而变化
6. 模拟数据基于公开的网页参考信息
7. 建议合理使用缓存以减少网络请求
8. 需要安装 beautifulsoup4 和 lxml 库来解析HTML页面
