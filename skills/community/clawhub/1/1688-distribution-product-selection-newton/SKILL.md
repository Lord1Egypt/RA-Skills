---
name: 1688-distribution-product-selection-newton
description: 1688 分销选品助手 - 提供关键词选品、图搜选品等核心选品能力，以及分销参谋查询、推荐决策分析等深度评估功能。当用户需要搜索货源、以图搜货、筛选包邮/一件代发商品、分析商品分销价值或评估铺货风险时使用此技能。
metadata: {"openclaw": {"emoji": "📦", "requires": {"bins": ["python3"]}, "primaryEnv": "ALI_1688_AK"}}
---

# 1688 分销选品助手

## 背景说明

AK（Access Key）通过 clawhub 获取，通过命令 `python3 scripts/capabilities/configure/cmd.py <提取到的AK>` 来设置 `ALI_1688_AK`。AK 已绑定用户身份，无需任何额外的身份参数。

**完整流程：选品 → 选品决策分析**

## 功能概述

### 🔥 核心选品功能
- **关键词选品** - 根据筛选条件检索适合铺货的商品，支持多维度筛选和排序
- **图搜选品** - 通过图片搜索相似的分销商品，支持以图搜货、区域圈选

### 选品决策分析功能
- **分销参谋查询** - 查询商品的分销价、包邮、渠道支持、体验分、履约率等详细数据
- **推荐分析生成** - 综合多维度数据生成推荐指数、推荐理由和风险提示

### 辅助功能（待实现）
- 市场趋势分析、竞品对比分析、利润空间评估、选品建议生成等

## 前置检查：确认 AK 已配置

**skill 触发前，第一步必须立即检查 AK，不得先执行任何接口调用。** 运行以下命令：

```bash
python3 scripts/capabilities/configure/cmd.py
```

- **显示 "✅ AK 已配置"**：直接进入后续步骤，不要向用户提及此检查。
- **显示 "❌ 尚未配置 AK"**：输出下方 **AK 引导话术**，然后**停止，等待用户回复，不要做任何其他操作**。
  - 用户回复后，从消息中提取 AK 字符串，执行：
    ```bash
    python3 scripts/capabilities/configure/cmd.py <提取到的AK>
    ```
  - 配置完成后，直接继续执行用户最初的需求，无需额外说明。

### AK 引导话术

```text
需要先配置 AK，获取方式：
1. 打开 [ClawHub](https://clawhub.1688.com)，点击右上角**钥匙图标**获取 AK
2. 或者在 [AI工作台](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent)发送指令「给我AK」获取

获取后告诉我：「我的AK是 xxxxxx」
```

## ISV Token（可选，调用外部 ISV skill 时使用）

当业务需要调用 ISV（独立软件开发商）提供的外部 skill 时，必须先获取对应的 ISV Token。如果只调用 1688 内部接口（通过 `api_post`），则**不需要** ISV Token。

```bash
# 获取 token（自动缓存，24小时有效）
python3 scripts/cli.py isv_token fetch --app_key=你的AppKey

# 强制刷新 token
python3 scripts/cli.py isv_token fetch --app_key=你的AppKey --force_refresh=true

# 检查 token 状态
python3 scripts/cli.py isv_token status --app_key=你的AppKey
```

Token 保存在 `~/.isv_tokens.json`，按 appKey 索引，多个 skill 共享同一份缓存。

---

## 执行步骤

### ⚠️ 重要：执行任何选品操作前，必须先读取参考文档！

**在调用选品接口之前，第一步必须加载参考文档获取字段定义和规则，否则会导致参数错误、搜索无结果等问题。**

```
read_file: scripts/biz/product_selection/reference.md
```

参考文档包含：
- 所有支持的筛选字段名称（如 `title`、`is_free_post`、`is_yjdf` 等）
- 每个字段的数据类型和枚举值（如包邮用 `"Y"` 而不是 `"true"`）
- 正确的操作符名称（如 `contains_any`、`equal`、`range`）
- 参数格式示例和返回结构说明

**不读取参考文档直接调用接口 = 盲目猜测参数格式 = 高概率失败**

---

### 第一步：选品（用户有商品 ID 时可跳过）

根据用户输入类型自动选择模式：

- **用户提供图片链接或图片文件** → 图搜选品（`same_img_offer_search`）
- **用户提供文字描述**（如"帮我找一些包邮的垃圾袋"） → 关键词选品（`fx_keyword_search_selection`）

**关键词选品**：按参考文档中的规则将用户自然语言转换为 `retrieveFilters`，调用选品接口。

**图搜选品**：用户提供图片链接时使用 `imageAddress`，提供图片文件时转 Base64 使用 `imageBase64`，可选传入辅助关键词和主体圈选区域。

选品结果取前 3-5 个商品。

### 第二步：选品决策分析（选品后自动执行）

选品返回结果后，**自动**对候选商品批量查询分销参谋数据，综合分析后给出推荐理由。

**⚠️ 重要：执行决策分析前，必须先加载分销参谋参考文档！**

```
read_file: scripts/capabilities/offer_info/reference.md
```

该文档包含：分销参谋接口的返回字段说明、决策因素的提取规则、推荐维度和风险维度的判断标准、展示格式模板。

流程：
1. 读取参考文档获取决策分析规则
2. 对选品返回的每个候选商品，调用分销参谋接口查询详细数据：
   ```bash
   python3 scripts/capabilities/offer_info/cmd.py --offer-id "{offerId}" --decision
   ```
3. 提取决策因素（分销价、包邮、渠道匹配、体验分、履约率、服务保障、品牌授权等）
4. 综合选品数据 + 参谋数据，为每个商品生成推荐指数和推荐/风险分析
5. 按推荐指数排序，展示给用户，附带推荐理由和风险提示
6. 询问用户确认要铺货的商品后进入下一步

---

## 接口调用示例

通过 `cli.py` 统一入口调用业务接口：

```bash
# 基础调用格式
python3 scripts/cli.py <业务域> <动作> [--参数名=参数值]

# 关键词选品示例
# ⚠️ 字段名和操作符必须参考 scripts/biz/product_selection/reference.md
python3 scripts/cli.py product_selection fx_keyword_search_selection --retrieve_filters='[{"code":"title","value":["垃圾袋"],"queryType":"contains_any"},{"code":"is_free_post","value":"Y","queryType":"equal"}]' --page_no=1 --page_size=20

# 图搜选品示例
python3 scripts/cli.py product_selection image_search_offer --image_url=https://example.com/image.jpg --page_index=1 --page_size=20

# 分销参谋查询示例
python3 scripts/capabilities/offer_info/cmd.py --offer-id "855772330851" --decision
```

所有命令统一输出 JSON：
```json
{
  "success": true,
  "markdown": "✅ 调用成功",
  "data": { ... }
}
```

- `success=true`：直接使用 `markdown` 展示给用户，`data` 包含结构化数据
- `success=false`：`markdown` 包含错误描述

## 错误处理

| 错误信息 | 原因 | 处理方式 |
|---------|------|----------|
| AK 未配置 | 未设置环境变量 ALI_1688_AK | 执行 AK 配置流程 |
| 参数错误 | 传入的参数不正确 | 检查参数格式，参考 reference.md |
| 网络异常 | 接口调用失败 | 稍后重试 |

## 依赖包

```bash
pip install requests
```

## 语言要求

**⚠️ 重要：本技能的所有输出、提示、消息必须使用中文！**
