# BlockCity数据获取Skill

用于ClawHub的Skill技能，支持从blockcity.vip获取区块城市的信息，包括从排名页面获取城市排名、居民人数、开启区块数，以及从城市详情页获取基金余额、剩余人气值、市长和副市长等信息。

> **💰 最低购地折扣7.5折优惠链接**：https://www.blockcity.vip/?iclc

## 功能特性

- 从排名页面（https://www.blockcity.vip/pages/block/area）获取城市排名、居民人数、开启区块数
- 从城市详情页（如 https://www.blockcity.vip/0010）获取基金余额、剩余人气值等详细信息
- 支持4位数字电话区号和4个小写字母的特殊自建城市标识
- 根据城市名称查询详细信息
- 根据排名查询城市信息
- 数据筛选和排序
- 内置缓存机制提高效率
- 模拟数据支持（API不可用时自动降级）
- JSON格式数据输出

## 数据来源说明

### 排名页面数据
**URL**: https://www.blockcity.vip/pages/block/area  
**包含字段**：
- 城市排名
- 城市名称
- 居民人数
- 开启区块数

**注意**：人气余额和市长/副市长信息需要从城市详情页获取

### 城市详情页数据
**URL格式**：https://www.blockcity.vip/{城市标识}  
**城市标识格式**：
- 4位数字电话区号（如 0010 代表北京）
- 4个小写字母（如 abcd，用于特殊自建城市）

**包含字段**：
- 基金余额
- 剩余人气值
- 总区块数
- 可用区块数
- 市长/副市长详细信息

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from blockcity_skill import BlockCitySkill

# 创建Skill实例（默认启用缓存，5分钟有效期）
skill = BlockCitySkill()

# 获取城市排名列表（来自排名页）
cities = skill.get_city_rank_list()

# 根据城市名称获取详细信息（来自排名页）
beijing = skill.get_city_by_name("北京")

# 根据排名获取城市信息（来自排名页）
top_city = skill.get_city_by_rank(1)

# 从城市详情页获取基金余额等信息
beijing_detail = skill.get_city_detail("0010")

# 获取特殊自建城市信息
special_city = skill.get_city_detail("abcd")

# 筛选城市数据
filtered = skill.filter_cities(min_population=20000, limit=10)

# 转换为JSON格式
json_data = skill.to_json(cities)
```

### 高级配置

```python
# 禁用缓存
skill = BlockCitySkill(use_cache=False)

# 自定义缓存有效期（秒）
skill = BlockCitySkill(cache_ttl=600)  # 10分钟

# 出错时不使用模拟数据
try:
    cities = skill.get_city_rank_list(use_mock_on_error=False)
except Exception as e:
    print(f"错误: {e}")
```

### 数据结构

#### 排名页面数据结构

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

#### 城市详情页数据结构

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

## 示例代码

运行示例代码：

```bash
python blockcity_skill.py
```

## API 参考

### BlockCitySkill 类

#### `__init__(use_cache: bool = True, cache_ttl: int = 300)`
初始化Skill实例。

**参数：**
- `use_cache`: 是否启用缓存，默认为True
- `cache_ttl`: 缓存有效期（秒），默认为300秒（5分钟）

#### `get_city_rank_list(area_id: int = 0, use_mock_on_error: bool = True) -> List[Dict]`
从排名页面获取城市排名列表。

**参数：**
- `area_id`: 区域ID，默认为0获取全部城市
- `use_mock_on_error`: 出错时是否使用模拟数据，默认为True

**返回：**
- 城市列表，每个元素包含城市的详细信息

#### `get_city_by_name(city_name: str, use_mock_on_error: bool = True) -> Optional[Dict]`
根据城市名称获取城市详细信息（来自排名页）。

**参数：**
- `city_name`: 城市名称
- `use_mock_on_error`: 出错时是否使用模拟数据，默认为True

**返回：**
- 城市详细信息，如果未找到返回None

#### `get_city_by_rank(rank: int, use_mock_on_error: bool = True) -> Optional[Dict]`
根据排名获取城市详细信息（来自排名页）。

**参数：**
- `rank`: 城市排名（从1开始）
- `use_mock_on_error`: 出错时是否使用模拟数据，默认为True

**返回：**
- 城市详细信息，如果未找到返回None

#### `get_city_detail(city_id: str, use_mock_on_error: bool = True) -> Optional[Dict]`
从城市详情页获取城市详细信息。

**参数：**
- `city_id`: 城市标识（4位数字区号或单个字母）
- `use_mock_on_error`: 出错时是否使用模拟数据，默认为True

**返回：**
- 城市详情数据，包含基金余额、剩余人气值等

#### `get_complete_city_info(city_name: str, use_mock_on_error: bool = True) -> Optional[Dict]`
获取城市的完整信息（当前版本来自排名页）。

**参数：**
- `city_name`: 城市名称
- `use_mock_on_error`: 出错时是否使用模拟数据，默认为True

**返回：**
- 完整的城市信息

#### `filter_cities(min_population: Optional[int] = None, max_population: Optional[int] = None, min_popularity: Optional[int] = None, max_popularity: Optional[int] = None, limit: Optional[int] = None) -> List[Dict]`
筛选城市数据。

**参数：**
- `min_population`: 最小人口
- `max_population`: 最大人口
- `min_popularity`: 最小人气余额
- `max_popularity`: 最大人气余额
- `limit`: 返回结果数量限制

**返回：**
- 筛选后的城市列表

#### `to_json(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str`
将数据转换为JSON格式字符串。

**参数：**
- `data`: 要转换的数据
- `indent`: 缩进空格数
- `ensure_ascii`: 是否确保ASCII编码

**返回：**
- JSON格式字符串

## 注意事项

1. 请遵守blockcity.vip网站的使用条款
2. 合理控制请求频率，避免对服务器造成压力
3. 排名页面数据和城市详情页数据来自不同的数据源
4. 城市标识格式：4位数字电话区号 或 4个小写字母（特殊自建城市）
5. 数据结构可能随网站更新而变化
6. 模拟数据基于公开的网页参考信息
7. 建议合理使用缓存以减少网络请求
8. 需要安装 beautifulsoup4 和 lxml 库来解析HTML页面
