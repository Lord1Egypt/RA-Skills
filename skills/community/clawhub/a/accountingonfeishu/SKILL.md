---
name: AccountingOnFeishu
description: 帮用户快速记录日常支出和收入到飞书多维表格。支持文字记账和图片小票 OCR 解析。首次使用时会学习用户已有的记账本习惯，或引导新建记账本。
---

# AccountingOnFeishu

## 描述

帮用户快速记录日常支出和收入到飞书多维表格。支持文字记账和图片小票 OCR 解析（每个项目单独生成一条记录）。

**核心特性**：
- 首次使用时，先询问用户是否有现成记账本
- 如有：读取并学习其字段结构、分类习惯，后续按用户习惯记账
- 如无：引导用户新建记账本（支持自定义分类体系）
- 所有配置持久化到本地 `config.json`

## 使用场景

用户说以下类似的话时触发：
- "记账 吃饭 50"
- "记一笔 200 支出 购物"
- "收入 5000 工资"
- 发送图片小票说"记账"
- "这个月花了多少"
- "我要记账"（首次使用触发初始化）

## Skill 名称

`AccountingOnFeishu`

## 配置文件

文件路径：`~/.openclaw/workspace/skills/AccountingOnFeishu/config.json`

首次使用时如果不存在，进入**初始化流程**。

## 初始化流程（首次使用）

### 步骤 1：检查配置

检查 `config.json` 是否存在。
- 存在 → 直接读取配置，进入记账流程
- 不存在 → 进入步骤 2

### 步骤 2：询问用户

用自然语言问用户：

> 还没有配置记账本，你有现成的飞书多维表格记账本吗？
> 
> 1. **有** → 请提供多维表格链接或 app_token + table_id，我来学习你的记账习惯
> 2. **没有** → 我来帮你新建一个记账本

### 分支 A：用户有现成记账本

#### A1. 获取用户提供的链接或 token

用户可能提供：
- 飞书多维表格链接（如 `https://xxx.feishu.cn/base/APP_TOKEN`）
- 或直接说 app_token 和 table_id

从链接中提取 `app_token`。

#### A2. 学习记账本结构

**获取表结构：**
```
feishu_bitable_app_table_field > list
- app_token: <用户提供>
- table_id: <用户提供>
```

**获取记录样本（学习分类习惯）：**
```
feishu_bitable_app_table_record > list
- app_token: <用户提供>
- table_id: <用户提供>
- page_size: 20
```

#### A3. 分析并保存配置

从表结构中提取关键信息：

| 学习项 | 说明 |
|--------|------|
| `fields` | 所有字段名和类型 |
| `amount_field` | 金额字段名（通常是"金额"或"钱数"） |
| `note_field` | 备注字段名（通常是"备注"、"说明"、"描述"） |
| `type_field` | 收支类型字段名（通常是"收支"、"类型"、"收入/支出"） |
| `date_field` | 日期字段名（如果有） |
| `category_field` | 一级分类字段名（如果有） |
| `sub_category_field` | 二级分类字段名（如果有） |
| `category_options` | 一级分类的所有选项值（单选/多选字段的 options） |
| `sub_category_options` | 二级分类的所有选项值 |
| `income_value` | 收入类型的选项值（如"收入"、"进账"） |
| `expense_value` | 支出类型的选项值（如"支出"、"出账"） |

**保存到 config.json：**
```json
{
  "app_token": "xxx",
  "table_id": "xxx",
  "table_name": "用户记账本",
  "fields": {
    "amount": "金额",
    "note": "备注",
    "type": "收支",
    "date": "日期",
    "category": "分类",
    "sub_category": "二级分类"
  },
  "type_options": {
    "income": "收入",
    "expense": "支出"
  },
  "category_options": ["餐饮", "交通", "购物", ...],
  "sub_category_options": ["早餐", "午餐", "晚餐", ...]
}
```

#### A4. 向用户确认

告诉用户已学习到的结构：
> 已学习你的记账习惯！
> - 金额字段：「金额」
> - 备注字段：「备注」
> - 分类字段：「分类」（有 15 个选项）
> - 收支字段：「收支」
> 
> 以后直接说"记账 吃饭 50"就能按你的习惯记录了 ✅

### 分支 B：用户没有记账本（新建）

#### B1. 询问分类需求

> 我来帮你新建一个记账本，需要几个分类字段？
> 
> 1. **简单版**：备注、金额、收支、日期（4个字段）
> 2. **标准版**：+ 一级分类（餐饮/交通/购物等）
> 3. **完整版**：+ 一级分类 + 二级分类

根据用户选择，调用建表流程。

#### B2. 创建多维表格

```
feishu_bitable_app > create
- name: "个人记账本"
```

返回 `app_token`。

#### B3. 创建数据表（带字段）

```
feishu_bitable_app_table > create
- app_token: <上一步返回的>
- name: "记账明细"
- fields: [
    {"field_name": "备注", "type": 1},
    {"field_name": "金额", "type": 2, "property": {"formatter": "0.00"}},
    {"field_name": "收支", "type": 3, "property": {"options": [
      {"name": "收入", "color": 0},
      {"name": "支出", "color": 1}
    ]}},
    {"field_name": "日期", "type": 5, "property": {"auto_fill": true, "date_formatter": "yyyy-MM-dd"}},
    {"field_name": "分类", "type": 3, "property": {"options": [
      {"name": "餐饮", "color": 0},
      {"name": "交通", "color": 1},
      {"name": "购物", "color": 2},
      {"name": "娱乐", "color": 3},
      {"name": "住房", "color": 4},
      {"name": "医疗", "color": 5},
      {"name": "教育", "color": 6},
      {"name": "通讯", "color": 7},
      {"name": "服装", "color": 8},
      {"name": "社交", "color": 9},
      {"name": "旅行", "color": 10},
      {"name": "数码", "color": 11},
      {"name": "日用", "color": 12},
      {"name": "其他", "color": 13}
    ]}}
  ]
```

**注意**：
- 如果用户选择"完整版"，再添加 `二级分类` 字段
- 二级分类可以选项根据`~/.openclaw/workspace/skills/AccountingOnFeishu/config.json.example`来预设，或者也可以先留空让用户自己添加
- `日期` 字段设置 `auto_fill: true`，自动填充创建日期

#### B4. 保存配置

将新建的信息写入 `config.json`，格式同分支 A。

#### B5. 返回确认

> 记账本已创建！✅
> 
> 📋 [查看记账表格](https://my.feishu.cn/base/APP_TOKEN)
> 
> 以后直接说"记账 吃饭 50"就能记了

## 工作流程

### 流程 1：文字记账

**前提**：`config.json` 已存在。

1. **解析用户输入**
   - 提取备注描述
   - 提取金额（数字或数学表达式）
     - 如果金额是表达式（如 `50-41.83`、`100*0.8`、`60+30`），先计算结果
     - 支持 + - * / 和括号
     - 计算后取绝对值（避免负数）
   - 判断收支类型：
     - 有"收入"/"进账"/"到账"等关键词 → 收支 = `config.type_options.income`
     - 其他情况 → 收支 = `config.type_options.expense`
   - 备注 = 用户描述中的消费内容

2. **智能分类（可选）**
   - 如果配置中有 `category_field`，尝试根据备注关键词匹配分类：
     - 关键词包含 "饭"/"餐"/"吃"/"外卖" → 餐饮
     - 关键词包含 "车"/"地铁"/"公交"/"打车"/"油" → 交通
     - 关键词包含 "买"/"购"/"淘宝"/"京东" → 购物
     - 关键词包含 "电影"/"游戏"/"唱" → 娱乐
     - ...（其他关键词匹配）
   - 如果无法匹配，分类字段留空

3. **写入多维表格**
   使用 `config.json` 中学习到的字段名：
   ```
   feishu_bitable_app_table_record > create
   - app_token: <config.app_token>
   - table_id: <config.table_id>
   - fields:
       <config.fields.note>: <备注>
       <config.fields.amount>: <金额>
       <config.fields.type>: <收入/支出>
       <config.fields.category>: <智能分类结果>（如果有）
   ```
   - 日期字段如果设置了 auto_fill，无需手动写入

4. **返回确认**
   - 简要告诉用户已记录
   - 附上多维表格链接：`https://my.feishu.cn/base/<config.app_token>`

### 流程 2：图片小票记账

1. **下载并分析图片**
   - 如果图片在消息中，先用 `feishu_im_bot_image` 或 `feishu_im_user_fetch_resource` 下载
   - 用 `image` 工具（Kimi vision）分析图片内容

2. **OCR 解析每个项目**
   - 提示词应要求：列出小票上每个商品/项目，单独一行
   - 格式：`<价格> <项目描述>`
   - 忽略店名、总计、找零等无关信息

3. **批量写入多维表格**
   使用 `config.json` 中学习到的字段名：
   ```
   feishu_bitable_app_table_record > batch_create
   - app_token: <config.app_token>
   - table_id: <config.table_id>
   - records: [
       { fields: { <note_field>: "项目描述1", <amount_field>: <价格>, <type_field>: <expense_value> } },
       { fields: { <note_field>: "项目描述2", <amount_field>: <价格>, <type_field>: <expense_value> } },
       ...
     ]
   ```

4. **返回确认**
   - 告诉用户共解析出 N 个项目
   - 总金额是多少
   - 附上多维表格链接

## 字段格式参考

| 字段名 | 类型 | 格式 | 示例 |
|--------|------|------|------|
| 备注/描述 | 文本 (type=1) | 字符串 | "吃饭"、"小票-咖啡" |
| 金额 | 数字 (type=2) | 数字，不带货币符号 | 50 或 128.5 |
| 收支/类型 | 单选 (type=3) | 字符串，值从 config 读取 | "支出" 或 "收入" |
| 日期 | 日期 (type=5) | 毫秒时间戳 | 自动填充时可不写 |
| 分类 | 单选 (type=3) | 字符串，值从 config 读取 | "餐饮" |
| 二级分类 | 单选 (type=3) | 字符串，值从 config 读取 | "午餐" |

**重要**：
- 所有字段名都从 `config.json` 中读取，不要假设固定名称
- 金额只写数字，不带 `¥` 或 `元`
- 日期字段如设置了 auto_fill，无需手动写入

## 智能分类关键词映射

如果用户记账本有分类字段，可尝试按关键词匹配：

| 关键词 | 分类 |
|--------|------|
| 饭、餐、吃、外卖、食堂、火锅、烧烤 | 餐饮 |
| 车、地铁、公交、打车、滴滴、油费、停车、高速 | 交通 |
| 买、购、淘宝、京东、拼多多、天猫、商场 | 购物 |
| 电影、游戏、唱K、酒吧、剧本杀、游乐场 | 娱乐 |
| 房租、水电、物业、燃气、宽带 | 住房 |
| 药、医院、诊所、体检、医保 | 医疗 |
| 书、课、培训、考试、学费 | 教育 |
| 话费、流量、宽带、电话 | 通讯 |
| 衣服、鞋、包、化妆品、护肤品 | 服装 |
| 朋友、聚会、送礼、红包 | 社交 |
| 酒店、机票、火车票、景点、签证 | 旅行 |
| 手机、电脑、耳机、键盘、鼠标 | 数码 |
| 纸巾、洗发水、洗衣液、牙膏 | 日用 |

匹配失败时分类留空，不强制填写。

## 财务建议生成（可选）

记录完成后，可以根据以下情况给出简短建议：

| 情况 | 建议类型 |
|------|---------|
| 单笔 > 500 元 | "这笔开支不小哦，考虑一下是否真的必要？" |
| 同一类别当天多笔 | "今天在[X分类]花了[N]次，要不要合并一下？" |
| 图片识别出多个项目 | "小票解析出[N]项，总共[X]元，平均每项[Y]元" |
| 金额异常（过大或过小） | "这个金额有点奇怪，确定没记错吗？" |
| 无特别情况 | 直接确认即可 |

**原则**：建议要简短、自然、不啰嗦，可以偶尔调皮一下。

## 注意事项

- `config.json` 是核心配置文件，所有字段映射和 token 都在这里
- 金额需要是数字类型，不是字符串
- 单次批量创建最多 500 条（图片小票一般不会超）
- 图片下载后保存在 `/tmp/openclaw/` 下
- 解析图片时，prompt 要明确要求输出每个项目的价格和描述
- 学习现有记账本时，如果字段类型不匹配（如金额字段是文本而非数字），向用户说明并询问是否需要调整
