# 美食探店助手 v1.0.0

🍜 像探店搭子一样，陪你发现附近的美食！

## 功能特点

- 📍 **智能定位**：支持自然语言地址输入（如"杭州西湖断桥"）
- 🕐 **用餐场景**：根据时间自动判断早/午/晚餐场景
- 🍜 **类型丰富**：支持火锅、日料、川菜、烧烤等各种类型
- 💰 **预算筛选**：经济型到精致体验，满足不同需求
- 🔄 **兜底方案**：API不可用时使用本地数据兜底
- 💡 **详细推荐**：评分、人均、距离、地址、电话、推荐理由

## 快速开始

### 1. 配置API KEY

```bash
# Linux/Mac
export BAIDU_MAP_API_KEY='你的百度地图API_KEY'

# Windows PowerShell
$env:BAIDU_MAP_API_KEY='你的百度地图API_KEY'

# Windows CMD
set BAIDU_MAP_API_KEY=你的百度地图API_KEY
```

获取API KEY：https://lbsyun.baidu.com/apiconsole/key

### 2. 运行测试

```bash
# 进入skill目录
cd .opencode/skills/food-explorer-1.0.0

# 测试API客户端
python baidu_map_client.py

# 测试推荐功能
python food_recommender.py
```

### 3. 在代码中使用

```python
from food_recommender import FoodRecommender

# 初始化（自动读取环境变量BAIDU_MAP_API_KEY）
recommender = FoodRecommender()

# 推荐餐厅
result = recommender.recommend(
    address="杭州西湖断桥",
    food_type="杭帮菜",
    budget="100-200",
    radius=2000
)

# 格式化输出
output = recommender.format_recommendation(result)
print(output)
```

## 文件结构

```
food-explorer-1.0.0/
├── SKILL.md                    # Skill定义文档
├── _meta.json                  # 元数据
├── baidu_map_client.py         # 百度地图API客户端
├── food_recommender.py         # 推荐器核心逻辑
├── data/
│   └── city_food_db.json       # 本地兜底数据
├── references/
│   ├── baidu_map_api.md        # API文档参考
│   └── city_food_db.md         # 数据格式说明
└── README.md                   # 本文件
```

## API说明

### 使用百度地图API

本Skill使用百度地图的两个API：

1. **地理编码API**：将地址转换为经纬度坐标
2. **周边搜索API**：根据坐标搜索附近餐厅

详细的API参数说明见 [references/baidu_map_api.md](references/baidu_map_api.md)

### 本地兜底数据

当API不可用时，使用 `data/city_food_db.json` 中的本地数据推荐。

目前已覆盖城市：杭州、成都、上海、北京、广州

## 使用场景示例

| 用户输入 | 推荐类型 |
|---------|---------|
| "我在杭州西湖附近，有什么好吃的？" | 自动推荐当前时段美食 |
| "成都春熙路附近有什么特色火锅？" | 按类型推荐火锅 |
| "上海陆家嘴商务午餐，人均150" | 按场景+预算推荐 |
| "北京烤鸭哪里好吃？" | 按菜系推荐 |

## 工作流程

```
用户询问
    ↓
问候 + 询问位置
    ↓
地理编码 → 获取坐标
    ↓
询问用餐类型/预算
    ↓
周边搜索 → 获取餐厅列表
    ↓
智能排序 + 格式化输出
    ↓
展示TOP 5推荐
```

## 后续扩展计划（V2.0）

- [ ] 个性化口味记录：记录用户偏好，越用越懂你
- [ ] 历史探店记录：追踪去过的店和评价
- [ ] 收藏清单：标记想去的店
- [ ] 本地缓存：减少API调用，提高响应速度
- [ ] 更多城市数据：扩展兜底数据覆盖范围

## 注意事项

1. **API KEY安全**：不要在代码中硬编码，使用环境变量
2. **隐私保护**：位置信息仅用于查询，不存储（V1.0）
3. **数据准确性**：餐厅信息可能有滞后，出行前请电话确认
4. **网络依赖**：需要联网使用百度地图API

## 技术支持

- 百度地图API文档：https://lbsyun.baidu.com/
- API控制台：https://lbsyun.baidu.com/apiconsole/key

## License

MIT
