---
name: diet-log
description: 饮食记录与营养分析助手。当用户提到"饮食记录"、"记下我吃了"、"营养分析"、"统计饮食"、"最近X天吃了什么"等关键词时触发。功能包括：(1) 解析用户输入的饮食内容并查询营养数据；(2) 计算并记录全部营养素（热量、宏量营养素、脂肪酸、矿物质、维生素）；(3) 将饮食记录存入 meal_log.json；(4) 支持阶段性营养统计（按日/周/月）。食物营养数据文件 food_data.json 需单独下载（见 SKILL.md 同目录下的说明或 GitHub 仓库）。食物匹配采用三级策略：精确匹配 → 同类参考 → 提问确认。
---

# 饮食记录 (diet-log)

## ⚠️ 首次使用：下载食物营养数据

本 Skill 需要下载食物营养数据库文件（约 3.7MB），请在 GitHub 仓库中下载 `references/food_data.json` 放置到本 Skill 的 `references/` 目录下：

- GitHub 仓库：https://github.com/sj13818161942/diet-log
- 直接下载：点击 `references/food_data.json` → 点击 Download 按钮

下载后确保文件路径为：
```
diet-log/references/food_data.json
```

## 数据来源

- 文件：`references/food_data.json`（1643条食物记录，**需手动下载**）
- 原始数据来自 foodwake.com，通过 LuckyHookin/foodwake 项目获取（Apache-2.0 授权）
- 食物分类：谷类/薯类/豆类/蔬菜/菌类/藻类/水果/坚果/畜肉/禽肉/乳类/蛋类/河海鲜/茶类/酒类/油类/调味品类/零食饮料

## 食物匹配策略（三级）

当用户输入食物名称时，按以下顺序处理：

### 第一级：精确匹配
在数据库中搜索名字或别名**包含**用户输入的食物名称的记录，取第一条结果。

### 第二级：同类参考
若精确匹配无结果，在**同一类别**中查找最接近的食物作为参考，并在记录中标注「参考值」。

常见类别映射：
- 用户说"鸡腿/鸡肉" → 参考数据库中畜肉/禽肉类的鸡肉数据
- 用户说"猪肉/排骨" → 参考畜肉类
- 用户说"河鱼/草鱼" → 参考河海鲜类

### 第三级：提问确认
若同类参考也无法找到（如罕见食材），向用户提问：
> "我没有找到【XXX】的精确数据。请问它的类别是？例如：肉类/鱼类/蔬菜/豆制品/主食/其他？"或"你说的XXX是指YYY吗？"

## 营养分析维度（全字段）

分析并记录以下所有可用营养素（若数据缺失则记为0）：

### 宏量营养素（核心）
| 字段 | 说明 | 单位 |
| :--- | :--- | :--- |
| energy_kcal | 能量 | 千卡 (kcal) |
| protein_g | 蛋白质 | 克 (g) |
| fat_g | 脂肪 | 克 (g) |
| carbs_g | 碳水化合物 | 克 (g) |
| fiber_g | 粗纤维 | 克 (g) |

### 脂肪酸
| 字段 | 说明 |
| :--- | :--- |
| saturated_fat_g | 饱和脂肪酸 |
| monounsaturated_fat_g | 单不饱和脂肪酸 |
| polyunsaturated_fat_g | 多不饱和脂肪酸 |
| trans_fat_g | 反式脂肪酸 |

### 矿物质
| 字段 | 说明 |
| :--- | :--- |
| calcium_mg | 钙 (mg) |
| magnesium_mg | 镁 (mg) |
| sodium_mg | 钠 (mg) |
| potassium_mg | 钾 (mg) |
| phosphorus_mg | 磷 (mg) |
| iron_mg | 铁 (mg) |
| zinc_mg | 锌 (mg) |
| selenium_mg | 硒 (mg) |
| copper_mg | 铜 (mg) |
| manganese_mg | 锰 (mg) |

### 维生素
| 字段 | 说明 |
| :--- | :--- |
| vitamin_a_mcg | 维生素A (μg) |
| vitamin_c_mg | 维生素C (mg) |
| vitamin_d_mcg | 维生素D (μg) |
| vitamin_e_mg | 维生素E (mg) |
| vitamin_k_mcg | 维生素K (μg) |
| vitamin_b1_mg | 维生素B1 硫胺素 (mg) |
| vitamin_b2_mg | 维生素B2 核黄素 (mg) |
| vitamin_b3_mg | 维生素B3 烟酸 (mg) |
| vitamin_b5_mg | 维生素B5 泛酸 (mg) |
| vitamin_b6_mg | 维生素B6 (mg) |
| vitamin_b7_mcg | 维生素B7 生物素 (μg) |
| vitamin_b9_mcg | 维生素B9 叶酸 (μg) |
| vitamin_b12_mcg | 维生素B12 (μg) |

## 工作流程

### 流程一：记录饮食 & 全营养分析

**触发**：用户输入饮食内容并请求记录或分析。

1. **解析食物列表**：从用户输入中提取所有食物名称和估计份量。
2. **检查数据文件**：确认 `references/food_data.json` 已存在，若缺失提示用户下载。
3. **匹配食物数据**：按三级匹配策略查询每种食物。
4. **计算份量营养**：将食物营养数据按用户估计的份量进行比例换算。
5. **汇总全部营养素**：分别求和各宏量、微量营养素的总和。
6. **输出完整分析报告**（格式见下方）。
7. **保存记录**：追加写入 `references/meal_log.json`。

### 流程二：阶段性营养统计

**触发**：用户请求"最近N天"、"上周"、"本月"等时间段的统计。

1. **确定日期范围**：根据当前日期和用户指定周期。
2. **读取记录**：从 `references/meal_log.json` 筛选日期范围内所有记录。
3. **计算周期总计+日均**：对全部营养字段进行汇总。
4. **与参考标准对比**：给出偏离度评价。
5. **输出统计报告**。

---

## 输出格式模板

### 单餐全营养分析

```
🍽️ 【{meal} · {date}】

食物列表：
• {food_name}（{type}，{weight}）…… 能量 {energy}kcal
  蛋白 {protein}g | 脂肪 {fat}g | 碳水 {carbs}g | 纤维 {fiber}g
  维A {vitA}μg | 维C {vitC}mg | 铁 {iron}mg | 钙 {calcium}mg | ...
• ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
合计摄入（当日 {meal}）：
⚡ 能量：{total_energy} kcal
💪 蛋白质：{total_protein} g
🧈 脂肪：{total_fat} g
🍞 碳水化合物：{total_carbs} g
🌾 膳食纤维：{total_fiber} g

🧪 矿物质：
钙 {calcium}mg | 铁 {iron}mg | 锌 {zinc}mg | 钾 {potassium}mg | 钠 {sodium}mg

💊 维生素：
维A {vitA}μg | 维C {vitC}mg | 维E {vitE}mg | 维B1 {vitB1}mg | 维B2 {vitB2}mg

💡 营养评估与建议：{基于各营养素平衡的专业建议}
```

### 阶段性统计报告（按营养类别分组）

```
📊 【{period} 全营养统计 · {start_date}~{end_date}】
总天数：{days} 天

━━━ 🔥 宏量营养素 ━━━
⚡ 能量：{total_energy} kcal（日均 {avg_energy} kcal）
💪 蛋白质：{total_protein} g（日均 {avg_protein} g）
🧈 脂肪：{total_fat} g（日均 {avg_fat} g）
🍞 碳水：{total_carbs} g（日均 {avg_carbs} g）

━━━ 🧪 关键矿物质 ━━━
钙 {calcium} mg | 铁 {iron} mg | 锌 {zinc} mg

━━━ 💊 关键维生素 ━━━
维A {vitA} μg | 维C {vitC} mg | 维E {vitE} mg

━━━ 📅 每日能量明细 ━━━
Day 1（{date}）：{energy} kcal
...

💡 综合评估：{对比参考标准的营养摄入评价与建议}
```

---

## 参考标准（成年人日常基础需求）

| 营养素 | 日推荐量 | 备注 |
| :--- | :--- | :--- |
| 能量 | 1800~2400 kcal | 取决于性别、活动量 |
| 蛋白质 | 50~80 g | 占总热量 15~20% |
| 脂肪 | 40~70 g | 占总热量 20~30% |
| 碳水 | 200~300 g | 占总热量 50~65% |
| 钙 | 800~1000 mg |  |
| 铁 | 12~20 mg | 女性高于男性 |
| 锌 | 12~15 mg |  |
| 维生素A | 700~800 μg |  |
| 维生素C | 80~100 mg |  |
| 维生素E | 14 mg |  |

## 记录文件格式

`references/meal_log.json` 每条记录格式：

```json
{
  "date": "2026-04-14",
  "meal": "breakfast",
  "foods": [
    {
      "name": "面条（富强粉）",
      "energy_kcal": 283, "protein_g": 8.5, "fat_g": 1.6, "carbs_g": 59.5,
      "fiber_g": 0.5, "calcium_mg": 13, "iron_mg": 2.6, "zinc_mg": 1.07,
      "vitamin_a_mcg": 0, "vitamin_c_mg": 0, "vitamin_e_mg": 0.47,
      "vitamin_b1_mg": 0.35, "vitamin_b2_mg": 0.1, ...
    }
  ],
  "total": {
    "energy_kcal": 678, "protein_g": 51.6, "fat_g": 24.2, "carbs_g": 62.4,
    "fiber_g": 3.1, "calcium_mg": 95, "iron_mg": 5.8, ...
  },
  "note": "鸡腿为参考估算值"
}
```

## 注意事项

- **首次使用必须下载** `food_data.json`（太大无法嵌入到 ClawHub 包中）
- 食物数据为 **2020年快照**，来自 foodwake.com，可能与中国最新食物成分表有差异
- 营养计算为**估算值**，实际摄入因烹饪方式、食材产地等因素可能有偏差
- 对于无匹配食物，**必须向用户确认同类替代方案**，不能擅自使用不相关数据
- 数据授权为 Apache-2.0，可商用但需标注来源
