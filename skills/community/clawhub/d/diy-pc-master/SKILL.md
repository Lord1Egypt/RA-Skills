---
name: diy-pc-master
description: 电脑DIY装机大师技能。用于帮助用户进行电脑配置推荐、装机方案分析、配件兼容性判断。当用户询问装机配置、电脑推荐、预算配置、配件分析、配置测评等问题时触发此技能。
---

# 电脑装配大师 Skill

## 概述

本技能分为四个步骤执行：
1. **用户意图分析** - 判断用户场景
2. **装机大师** - 生成SQL查询语句
3. **配件查询** - 调用API获取配件数据
4. **装机分析大师** - 生成配置方案并判断兼容性

---

## 第一步：用户意图分析

### 判断规则

**DIY装机场景** - 满足以下任一条件：
- 用户明确表达预算（如：4500元、5000预算）
- 用户表达功能需求（如：打游戏、工作、设计）
- 用户咨询包含：预算、价格、推荐、配置、增加配置、替换等相关问题

**装机测评场景** - 满足以下任一条件：
- 用户要求分析配置（如：帮我分析这个配置怎么样）
- 用户要求测评（如：请分析这套配置的性能、性价比、兼容性）
- 问题包含：分析、测评、怎么样

**无明确场景** - 无法匹配上述场景

### 输出格式

只输出以下三个场景之一：
- DIY装机场景
- 装机测评场景  
- 无明确场景

---

## 第二步：装机大师 - SQL生成

### 数据库表结构参考

```sql
CREATE TABLE `goods` (
 `time` date NOT NULL DEFAULT '2025-05-06',
 `category` int NOT NULL COMMENT '分类ID对应:
CPU:11,
主板:12,
内存:13,
显卡:14,
硬盘:15,
电源:16,
机箱:18,
显示器:19,
配件:20,
外设(键盘\鼠标）:21,
散热:22',
 `secondlevel` int NOT NULL COMMENT '子分类id:
51 Intel CPU
52 AMD CPU
53 英特尔主板
54 AMD 主板
55 DDR3
56 DDR4
57 DDR5
58 N卡
59 A卡
60 SSD固态
61 机械硬盘
62 m2硬盘
63 全模组
64 非全模组
65 风冷
66 水冷
67 E-ATX
68 ATX
69 M-ATX
70 MINI-ATX
71 1k显示器
72 2k显示器
73 2k以下显示器
74 机箱风扇
75 机箱灯条
76 显卡支架
77 显卡延长线
78 ARGB集线器
79 网卡
80 硅脂
81 键盘
82 鼠标
83 耳机
84 手柄
85 键鼠套装',
 `power` int DEFAULT NULL COMMENT '功率 单位W',
 `id` int NOT NULL COMMENT '配件id',
 `IMG` varchar(255) DEFAULT NULL COMMENT '商品主图',
 `sale` decimal(10,2) DEFAULT NULL COMMENT '售价',
 `cangshu` text COMMENT '参数信息(JSON格式)',
 `ProductName` varchar(255) DEFAULT NULL COMMENT '商品名称',
 `url` varchar(255) DEFAULT NULL COMMENT '京东链接',
 `fengshu` int DEFAULT NULL COMMENT '分数',
 `recommend_yes` int DEFAULT '0' COMMENT '推荐',
 `recommend_no` int DEFAULT '0' COMMENT '不推荐',
 `golinkjd` varchar(255) DEFAULT NULL COMMENT '京东联盟链接',
 `brand_recommend` tinyint(1) NOT NULL DEFAULT '0' COMMENT '品牌推荐',
 `is_on_sale` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否上架：0-未上架，1-已上架',
 `user_id` int DEFAULT NULL COMMENT '关联的用户ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 价格区间分配规则

根据用户预算，合理分配各配件预算比例（参考值）：

| 配件 | 预算占比 | 说明 |
|------|----------|------|
| CPU | 20-25% | 核心组件 |
| 主板 | 15-20% | 决定扩展性 |
| 内存 | 8-12% | 16GB起步 |
| 显卡 | 25-35% | 游戏关键 |
| 硬盘 | 8-12% | SSD优先 |
| 电源 | 5-10% | 保障稳定性 |
| 散热 | 3-8% | 可用原配 |
| 机箱 | 5-10% | 适中即可 |
| 显示器 | 10-15% | 可外设 |
| 外设 | 5-10% | 键鼠耳机 |

### SQL生成模板

**必须包含 `is_on_sale = 1` 筛选条件**
**必须包含 `golinkjd` 字段用于获取京东购买链接**

```json
{
 "CPU": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =11 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "主板": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =12 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "内存": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =13 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "显卡": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =14 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "硬盘": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =15 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "电源": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =16 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "散热": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =22 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "机箱": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =18 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "显示器": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =19 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "配件": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =20 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;",
 "外设": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =21 AND is_on_sale = 1 AND sale BETWEEN 下限价格 AND 上限价格 LIMIT?;"
}
```

### 特殊SQL生成

**名称精确检索**：
```json
{
 "名称检索": "SELECT * FROM `goods` WHERE `ProductName` LIKE '%AMD Ryzen7 9700X%' AND is_on_sale = 1"
}
```

### 智能配件选择规则

1. **预算有限时**：可省略散热器（使用CPU自带散热器）
2. **游戏为主**：显卡预算占比提高
3. **生产力为主**：CPU和内存预算占比提高
4. **普通办公**：可适当降低显卡预算

---

## 第三步：配件查询API

### API信息

- **URL**: `https://www.diyzp.cn/api/sql_api.php`
- **方法**: POST
- **Content-Type**: `application/json`

### 请求体

```json
{
  "VALID_TOKEN": "456645654121ssssqqqqq",
  "sql": "生成的SQL语句"
}
```

### 调用示例

**调用CPU查询**：
```
POST https://www.diyzp.cn/api/sql_api.php
Content-Type: application/json

{"VALID_TOKEN": "456645654121ssssqqqqq", "sql": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =11 AND is_on_sale = 1 AND sale BETWEEN 800 AND 1000 LIMIT 10"}
```

**调用主板查询**：
```
POST https://www.diyzp.cn/api/sql_api.php
Content-Type: application/json

{"VALID_TOKEN": "456645654121ssssqqqqq", "sql": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =12 AND is_on_sale = 1 AND sale BETWEEN 600 AND 800 LIMIT 10"}
```

### 执行流程

1. 根据第二步生成的SQL，逐一调用API获取配件数据
2. 每个配件SQL需要单独调用
3. 收集所有返回的配件数据（包括 `golinkjd` 京东购买链接）

---

## 第四步：装机分析大师 - 配置生成与兼容性判断

### 分类名称对照表

| 字段 | 中文名 |
|------|--------|
| CPU | CPU |
| memory | 内存 |
| gpu | 显卡 |
| storage | 硬盘 |
| monitor | 显示器 |
| peripherals | 外设 |
| accessory | 配件 |
| psu | 电源 |
| case | 机箱 |
| cooler | 散热器 |
| motherboard | 主板 |

### 必需配件

以下配件必须包含在方案中：
- CPU
- 主板
- 内存
- 硬盘
- 机箱

### 可选配件

根据实际情况酌情添加：
- 显卡
- 电源
- 散热
- 显示器
- 外设
- 配件

### 兼容性判断规则

**CPU与主板兼容**：
- 判断依据：CPU的接口(jiekou) 与 主板的接口(jiekou) 必须一致
- 优先查询带详细参数(cangshu)的配件数据进行精确匹配

**内存与主板兼容**：
- 判断依据：内存的代次(daishu) 与 主板的内存类型(ddr) 必须一致
- 优先查询带详细参数(cangshu)的配件数据进行精确匹配

**机箱与主板兼容**：
- 判断依据：机箱的体型(tixing) 与 主板的板型(banxing) 必须匹配
- 匹配规则：E-ATX机箱 > ATX主板 > M-ATX主板 > MINI-ATX主板

### 获取购买链接

在API返回的数据中，每个配件都包含 `golinkjd` 字段，这是京东联盟购买链接：
- 选择配置单中的配件后，从API返回数据中提取对应的 `golinkjd` 值
- 如果 `golinkjd` 为空，使用 `url` 字段（京东原始链接）
- 输出时将链接格式化为可点击的链接形式

### 输出格式

输出一份电脑配件单，包含：

1. **配置单标题**
2. **总预算**
3. **各配件详情**（每个配件包含）：
   - 配件名称
   - 推荐理由
   - 价格
   - 购买链接（使用API返回的 `golinkjd` 字段）
4. **兼容性说明**
5. **总结建议**
6. **数据来源备注**：配件数据来源：DIYZP.cn仅供参考

---

## 完整工作流程

```
用户输入 → 意图分析 → 场景判断 → SQL生成 → API查询 → 兼容性判断 → 配置输出
```

### 示例

**用户输入**：预算4500元，打游戏

**第一步输出**：DIY装机场景

**第二步SQL生成**：
- CPU: 800-1000元
- 主板: 600-800元
- 内存: 300-400元
- 显卡: 1500-1800元
- 硬盘: 300-400元
- 电源: 300-400元
- 机箱: 200-300元

**第三步**：调用API获取各配件数据

**第四步**：生成配置单并检查兼容性

---

## 限制条件

1. 只输出JSON格式的SQL语句（第二步）
2. 只讨论电脑硬件装机相关话题
3. 生成配件价格区间上限值合计不能大于用户输入的总预算
4. CPU和外设的sale区间下限不超过100元
5. 必须确保所有配件之间兼容后再输出配置单

---

## 完整示例

**用户输入**：预算4500元，主要打游戏

### 第一步：意图分析
**输出**：DIY装机场景

### 第二步：SQL生成
```json
{
  "CPU": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =11 AND is_on_sale = 1 AND sale BETWEEN 800 AND 1000 LIMIT 10;",
  "主板": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =12 AND is_on_sale = 1 AND sale BETWEEN 600 AND 800 LIMIT 10;",
  "内存": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =13 AND is_on_sale = 1 AND sale BETWEEN 300 AND 400 LIMIT 10;",
  "显卡": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =14 AND is_on_sale = 1 AND sale BETWEEN 1500 AND 1800 LIMIT 10;",
  "硬盘": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =15 AND is_on_sale = 1 AND sale BETWEEN 300 AND 400 LIMIT 10;",
  "电源": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =16 AND is_on_sale = 1 AND sale BETWEEN 300 AND 400 LIMIT 10;",
  "机箱": "SELECT id, ProductName, sale, golinkjd FROM goods WHERE category =18 AND is_on_sale = 1 AND sale BETWEEN 200 AND 300 LIMIT 10;"
}
```

### 第三步：API调用
逐一调用API，获取各配件数据（包括 golinkjd 购买链接）

### 第四步：配置生成
根据返回数据生成兼容的配置单，包含购买链接

---

## ⚠️ 重要提示

**最终输出必须包含**：
1. 每个配件的京东购买链接（golinkjd字段）
2. 底部备注：**配件数据来源：DIYZP.cn仅供参考**

