---
name: food-expiry-reminder
description: 食品过期提醒技能。用于记录、管理和提醒食品过期情况。当用户需要记录食品信息、检查食品是否过期、查看即将过期的食品或管理食品库存时使用此技能。数据存储在food_data.json文件中。
---

# 食品过期提醒技能

本技能帮助用户记录、管理和提醒食品过期情况。所有食品数据存储在`food_data.json`文件中。

## 功能概述

1. **记录食品信息** - 添加新的食品记录
2. **检查过期状态** - 检查食品是否已过期或即将过期
3. **查看所有食品** - 列出所有食品及其状态
4. **提醒功能** - 提醒一周内将过期的食物
5. **数据管理** - 更新或删除食品记录

## 数据结构

食品数据存储在`food_data.json`文件中，格式如下：

```json
{
  "foods": [
    {
      "id": "唯一标识符",
      "name": "食品名称",
      "production_date": "生产日期 (YYYY-MM-DD)",
      "expiry_days": "保质期天数",
      "expiry_date": "过期日期 (自动计算)",
      "location": "存放位置",
      "quantity": "数量",
      "notes": "备注",
      "created_at": "创建时间",
      "updated_at": "更新时间"
    }
  ]
}
```

## 使用方法

### 1. 添加新食品

使用以下命令添加新食品：

```bash
python scripts/add_food.py "食品名称" "生产日期" "保质期天数" "存放位置" "数量" "备注"
```

或手动编辑`food_data.json`文件。

### 2. 检查过期状态

运行检查脚本查看过期和即将过期的食品：

```bash
python scripts/check_expiry.py
```

### 3. 查看所有食品

查看当前存储的所有食品：

```bash
python scripts/list_foods.py
```

### 4. 获取提醒

获取一周内将过期的食品提醒：

```bash
python scripts/get_reminders.py
```

## 脚本说明

### `scripts/add_food.py`

添加新食品到数据库。参数：
- 食品名称
- 生产日期 (YYYY-MM-DD)
- 保质期天数 (整数)
- 存放位置
- 数量 (可选，默认1)
- 备注 (可选)

### `scripts/check_expiry.py`

检查所有食品的过期状态，显示：
- 已过期的食品
- 一周内将过期的食品
- 两周内将过期的食品
- 安全的食品

### `scripts/list_foods.py`

列出所有食品的详细信息，包括状态。

### `scripts/get_reminders.py`

专门获取一周内将过期的食品提醒。

### `scripts/init_data.py`

初始化food_data.json文件（如果不存在）。

## 工作流程

1. **初始化数据文件** - 首次使用时运行`init_data.py`
2. **添加食品记录** - 购买新食品后立即记录
3. **定期检查** - 每天或每周运行`check_expiry.py`
4. **处理提醒** - 根据提醒处理即将过期的食品

## 注意事项

1. 生产日期格式必须为YYYY-MM-DD
2. 保质期天数为整数
3. 过期日期会自动计算
4. 建议每天运行一次检查脚本
5. 数据文件位于`data/food_data.json`

## 参考文件

- [数据结构说明](references/data_structure.md)
- [使用示例](references/examples.md)
- [常见问题](references/faq.md)