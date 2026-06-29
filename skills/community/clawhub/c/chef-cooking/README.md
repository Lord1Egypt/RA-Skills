# 🍳 AI 智能家庭厨助

> 输入食材/想吃的菜/饮食偏好，自动推荐菜谱、输出烹饪步骤指导、食材替换建议、多日菜单规划、烹饪技巧问答，生成卡片式交互 HTML 报告。

## 核心能力

| 模块 | 功能 | 示例 |
|------|------|------|
| 智能菜谱推荐 | 输入食材，推荐 2-3 道可做菜品 | "冰箱里有鸡蛋、西红柿、青椒" |
| 烹饪步骤指导 | 四阶段详细步骤（备料→处理→烹饪→装盘） | "红烧肉怎么做" |
| 食材替换建议 | 28 种常见食材替代方案 + 通用规则 | "想做宫保鸡丁但没花生" |
| 多日菜单规划 | 按天规划菜单，考虑营养均衡、不重复、季节时令 | "帮我规划本周 5 天晚餐" |
| 烹饪技巧问答 | 100+ 条技巧，覆盖刀工/火候/调味/食材处理/器具 | "牛排怎么判断几分熟" |
| 厨房安全提示 | 20+ 条安全知识，油温预警/禁忌搭配/食物中毒预防 | "发芽的土豆能吃吗" |
| 交互式 HTML 报告 | 卡片式菜谱展示，食材清单+步骤时间轴 | 每次菜谱生成后自动提供 |

## 数据规模

- **219 道菜谱**，覆盖 12 菜系（川/粤/鲁/苏/浙/闽/湘/徽 + 家常/汤羹/凉菜/主食）
- **1,280 步**详细烹饪步骤
- **100+ 条**烹饪技巧（8 分类）
- **20+ 条**厨房安全知识（6 分类）
- **28 种**食材替代方案库

## 使用方法

```bash
# 食材→菜谱推荐
python scripts/recipe_generator.py --ingredients "鸡蛋,西红柿,青椒"

# 菜谱步骤指导
python scripts/cooking_guide.py --recipe "红烧肉"

# 食材替换
python scripts/ingredient_sub.py --missing "豆瓣酱" --recipe "鱼香肉丝"

# 多日菜单规划
python scripts/meal_planner.py --days 5 --people 2

# 烹饪技巧搜索
python scripts/cooking_tips.py --query "炒青菜"

# 厨房安全查询
python scripts/kitchen_safety.py --query "油锅起火"

# 生成 HTML 报告
python scripts/html_report.py --type recipes --ingredients "鸡蛋,西红柿,青椒"
```

## 技术栈

- Python 3
- 内置 JSON 数据库 + 联网搜索补充
- 交互式卡片 HTML 报告（CSS Grid + 响应式布局）

## License

MIT
