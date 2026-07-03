---
name: ecommerce-interest-analyzer
description: "电商商品兴趣度分析助手。输入用户浏览行为数据（CSV/JSON/手动录入），通过多维度加权算法分析商品兴趣度，结合NLP文案质量评估，诊断价格/文案问题，生成交互式HTML可视化诊断报告。适用于抖音电商、淘宝、拼多多等平台。Triggers: 电商兴趣度分析, 商品兴趣分析, 用户兴趣度, 浏览行为分析, 商品诊断, 转化率分析, ecommerce interest, 抖音电商分析, 电商商品分析, 帮我分析商品."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
    emoji: "🛍️"
    homepage: https://github.com/bettermen/ecommerce-interest-analyzer
---

# 电商商品兴趣度分析技能

基于多维度用户行为数据和 NLP 文案分析，自动诊断电商商品的核心问题（价格/文案/综合），输出可操作的优化建议。

## 功能概述

1. **数据接收**：CSV/JSON 文件或手动描述用户浏览行为
2. **兴趣度评分**：10维加权模型（浏览/停留/详情/深度/点赞/评论/分享/加购/收藏/复访）
3. **文案分析**：NLP 评估（CTA检测、卖点覆盖、情感倾向、可读性）
4. **智能诊断**：3×3 兴趣-转化交叉矩阵，精准判定 price/copy/both/none
5. **报告生成**：交互式 HTML（Chart.js 雷达图 + 诊断卡片 + 优化建议）

## 适用场景

- 抖音电商/直播带货商品复盘
- 淘宝/拼多多/京东店铺商品诊断
- 新品上线后的用户反馈分析
- 多商品横向对比，识别优化优先级
- 广告投放效果归因（用户来了但不买 → 原因是什么？）

## 输入数据格式

### CSV 示例（最常用）

```csv
product_id,product_name,product_price,product_description,category,view_count,view_duration_avg,detail_page_view_rate,scroll_depth_avg,like_count,comment_count,share_count,add_to_cart_rate,favorite_rate,revisit_rate,purchase_rate,total_users
P001,无线蓝牙耳机,199.00,"高品质降噪耳机 超长续航48小时 舒适佩戴 限时特价",数码,8500,45.2,0.72,65.3,320,45,89,0.15,0.08,0.12,0.035,1200
P002,智能手表,599.00,"时尚运动智能手表 心率血氧监测 IP68防水",数码,12000,38.5,0.65,55.0,210,32,56,0.09,0.05,0.08,0.018,2000
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| product_id | str | 商品ID | P001 |
| product_name | str | 商品名称 | 无线蓝牙耳机 |
| product_price | float | 售价(元) | 199.00 |
| product_description | str | 商品描述文案 | 高品质降噪耳机... |
| category | str | 品类 | 数码 |
| view_count | int | 浏览次数 | 8500 |
| view_duration_avg | float | 平均停留时长(秒) | 45.2 |
| detail_page_view_rate | float | 详情页打开率(0-1) | 0.72 |
| scroll_depth_avg | float | 浏览深度(0-100) | 65.3 |
| like_count | int | 点赞数 | 320 |
| comment_count | int | 评论数 | 45 |
| share_count | int | 分享数 | 89 |
| add_to_cart_rate | float | 加购率(0-1) | 0.15 |
| favorite_rate | float | 收藏率(0-1) | 0.08 |
| revisit_rate | float | 复访率(0-1) | 0.12 |
| purchase_rate | float | 购买转化率(0-1) | 0.035 |
| total_users | int | 样本用户数 | 1200 |

### JSON 格式

与 CSV 相同字段的 JSON 数组，每个对象代表一个商品。若字段缺失，自动填充默认值。

### 手动录入模式

如果用户没有文件，可以手动描述商品情况，整理成 CSV 或 JSON 后继续分析。例如用户说：

> "我的蓝牙耳机卖了199，浏览8500人，详情页打开率72%，加购率15%，转化率3.5%，帮我分析"

根据用户描述，生成对应的 CSV 文件，缺失字段用合理默认值填充。

## 工作流

### Step 1: 接收数据

1. 若用户提供文件路径 → 直接读取
2. 若用户描述商品情况 → 提取关键数据，生成临时 CSV
3. 若用户不确定数据格式 → 展示上面的字段说明，引导提供

### Step 2: 确认分析范围

- 用户可能只需要分析特定商品 → 确认要分析的 product_id
- 用户可能想对比多个商品 → 全部纳入分析
- 默认：分析所有提供的商品

### Step 3: 运行分析引擎

```bash
python scripts/interest_analyzer.py --input <data.csv> --output <result.json>
```

此脚本会：
1. 加载行为数据
2. 计算每个商品的 10 维兴趣度评分
3. 对商品描述进行 NLP 文案质量分析
4. 执行 3×3 诊断矩阵判定
5. 输出结构化分析结果 JSON

**无需安装额外依赖**（纯 Python 标准库实现）。

### Step 4: 生成 HTML 报告

```bash
python scripts/report_generator.py --data <result.json> --output <report.html>
```

生成的 HTML 报告包含：
- 概要统计卡片（价格问题/文案问题/综合问题/优秀）
- 每个商品的雷达图（Chart.js CDN 加载）
- 诊断结论 + 价格/文案建议
- 文案质量指标（CTA/卖点/情感/可读性）
- 详细优化建议清单
- 响应式布局，支持移动端查看

### Step 5: 展示结果

- 使用 `preview_url` 打开 HTML 报告
- 使用 `deliver_attachments` 交付分析结果 JSON 和 HTML 报告
- 口头总结关键发现：哪些商品是价格问题、哪些是文案问题、优先调整哪个

### Step 6: 给出行动建议

基于分析结果，生成简明的操作清单，例如：

```
📋 优化优先级：
1. [P003] 价格问题（兴趣78分→转化2.1%）→ 先降价20%测一周
2. [P002] 文案问题（兴趣45分→无CTA/缺卖点）→ 重写文案加限时优惠
3. [P001] 综合问题（兴趣55分→转化6%）→ 文案+价格同步优化
4. [P004] 表现优秀 → 保持，可提价5%测试
```

## 算法说明

### 兴趣度评分（10维加权模型）

| 维度 | 权重 | 说明 |
|------|------|------|
| 浏览(view) | 0.10 | 曝光量基数 |
| 停留(duration) | 0.20 | **最高权重**，反映真实兴趣 |
| 详情页(detail) | 0.10 | 深度了解意愿 |
| 浏览深度(scroll) | 0.10 | 内容沉浸度 |
| 点赞(like) | 0.10 | 情感认可 |
| 评论(comment) | 0.05 | 互动深度 |
| 分享(share) | 0.10 | 社交传播意愿 |
| 加购(cart) | 0.15 | **第二高权重**，购买意向 |
| 收藏(favorite) | 0.10 | 长期兴趣 |
| 复访(revisit) | 0.10 | 持续关注度 |

> 停留时长和加购行为权重最高，因为它们与购买决策的因果关系最强。

### 诊断矩阵（3×3）

```
              转化率低(<10%)    转化率中(10-30%)   转化率高(>30%)
高兴趣(>70)     价格问题         文案优化          表现优秀
中兴趣(40-70)   综合问题         文案优化          价格可上调
低兴趣(<40)     文案/选品问题     文案/受众问题     性价比驱动
```

### NLP 文案分析维度

1. **CTA检测**：正则匹配"立即购买""限时抢购"等行动号召
2. **卖点覆盖**：内置 30+ 电商高频卖点词库
3. **情感分析**：正向/负向词统计，输出 -1 到 1 的情感分
4. **可读性**：句子长度分布，理想电商文案 15-30 字/句

## 示例数据

如果用户想快速体验，可以用这个测试数据：

```csv
product_id,product_name,product_price,product_description,category,view_count,view_duration_avg,detail_page_view_rate,scroll_depth_avg,like_count,comment_count,share_count,add_to_cart_rate,favorite_rate,revisit_rate,purchase_rate,total_users
P001,无线降噪耳机,299.00,"高品质降噪耳机 超长续航 舒适佩戴 限时特惠",数码,15200,55.3,0.82,72.5,520,78,145,0.22,0.12,0.18,0.028,2500
P002,便携充电宝,89.00,"10000mAh大容量 快充 小巧便携",数码,8800,18.2,0.45,38.0,95,28,35,0.06,0.03,0.05,0.015,1800
P003,智能台灯,159.00,"护眼台灯 LED 三档调光 学生用",家居,6500,42.0,0.68,60.8,180,52,42,0.14,0.09,0.11,0.042,1200
```

保存为 `test_data.csv`，运行：
```bash
python scripts/interest_analyzer.py -i test_data.csv -o result.json
python scripts/report_generator.py -d result.json -o report.html
```

## 注意事项

- 样本量 < 100 时，置信度自动降低（乘以 0.7），报告中会显示警告
- 所有数据本地处理，不上传任何服务器
- HTML 报告依赖 Chart.js CDN（首次需联网加载）
- 适用于抖音电商、淘宝、拼多多等平台，算法通用
- 分析结果仅供参考，最终决策需结合业务经验
