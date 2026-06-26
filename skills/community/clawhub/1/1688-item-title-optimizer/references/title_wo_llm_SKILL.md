---
name: title_wo_llm
description: 1688商品标题优化助手，无需LLM即可智能优化标题。通过三步流程（获取关键词信息 → 获取分词器列表并选择 → 使用选定分词器优化标题）提升标题质量。支持自定义关键词、选择分词器。使用场景：优化商品标题、自定义关键词优化。
---

# 标题优化助手 (Title Optimization Assistant)

为 1688 商品提供智能标题优化服务，基于规则和统计方法（无需 LLM），帮助商家快速提升标题质量、增加曝光和转化。

## 核心优化流程

标题优化采用三步流程，确保优化质量和效率：

### 步骤1：获取关键词信息
使用 `get_keyword_info` 获取优化所需的所有数据：
- 类目热搜词（基于真实搜索数据）
- 高曝光词（该商品的历史曝光关键词）
- 类目信息和商品属性

### 步骤2：获取分词器列表并选择
使用 `get_tokenizers` 获取所有可用的分词器：
- 获取所有预定义的分词器类型和说明
- 根据用户需求或prompt选择合适的分词器
- 如果用户没有指定，选择默认分词器（列表第一个）

### 步骤3：调用优化服务
使用 `optimize_title` 生成优化后的标题：
- 删除重复词和低频词
- 添加高相关性热搜词
- 生成优化说明和推荐词

## 快速开始

### 完整优化流程示例

```bash
# 步骤1：获取关键词信息
python3 scripts/interface.py --function get_keyword_info --item_id 123456789

# 步骤2：获取分词器列表
python3 scripts/interface.py --function get_tokenizers

# 步骤3：优化标题
python3 scripts/interface.py --function optimize_title --item_id 123456789 --use_llm
```

### 一键优化（跳过步骤1-2）

如果不需要查看中间结果，可直接调用优化服务：

```bash
python3 scripts/interface.py --function optimize_title --item_id 123456789
```

## 功能详解

### 1. get_keyword_info - 获取关键词信息

获取标题优化所需的全部关键词数据。**支持用户自定义关键词输入。**

**命令行：**
```bash
python3 scripts/interface.py --function get_keyword_info --item_id <商品ID> [--include_expo_words] [--include_hot_words] [--custom_keywords "关键词1;关键词2;关键词3"]
```

**参数：**
- `--item_id` (必需): 商品ID
- `--include_expo_words`: 包含高曝光词（默认True）
- `--include_hot_words`: 包含类目热搜词（默认True）
- `--custom_keywords` (可选): 用户自定义关键词，**使用分号分隔**，例如："保温杯;不锈钢;便携"

**使用示例：**
```bash
# 基础用法：获取系统推荐的关键词
python3 scripts/interface.py --function get_keyword_info --item_id 123456789

# 添加自定义关键词
python3 scripts/interface.py --function get_keyword_info --item_id 123456789 --custom_keywords "保温杯;不锈钢;大容量;便携"

# 只使用自定义关键词（不获取系统推荐）
python3 scripts/interface.py --function get_keyword_info --item_id 123456789 --custom_keywords "保温杯;不锈钢" --no-include_hot_words
```

**返回结果：**
```json
{
  "success": true,
  "data": {
    "item_id": 123456789,
    "cate_id": 50000001,
    "cate_name": "保温杯/保温瓶",
    "hot_words": ["不锈钢", "保温杯", "便携", "大容量"],
    "expo_words": {"保温": 150, "水杯": 120},
    "custom_keywords": ["保温杯", "不锈钢", "大容量", "便携"],
    "cpv": "材质:不锈钢;容量:500ml",
    "original_title": "304不锈钢水杯"
  }
}
```

### 2. get_tokenizers - 选择分词器

获取所有分词器列表，并根据用户prompt选择分词器。如果用户没有对分词器进行描述，则选择默认分词器（第一个分词器）。

**命令行：**
```bash
python3 scripts/interface.py --function get_tokenizers
```

**参数：**
（空）

**返回结果：**
[{"tokenizer": "qwen-flash", "desc": "使用qwen-flash模型进行分词"}]

获取上述结果后，按照用户prompt选择最匹配的分词器。

### 3. optimize_title - 优化标题

执行标题优化，生成优化后的标题。

**命令行：**
```bash
python3 scripts/interface.py --function optimize_title --item_id <商品ID> [--use_llm]
```

**参数：**
- `--item_id` (必需): 商品ID
- `--use_llm`: 使用LLM进行热词相关性判断（可选，提升准确性但增加耗时）

**返回结果：**
```json
{
  "success": true,
  "data": {
    "item_id": 123456789,
    "old_title": "304不锈钢水杯",
    "new_title": "304不锈钢保温杯便携",
    "optimize_reason": "添加热词:保温杯,便携",
    "new_title_words": [
      {"word": "304", "tag": "属性词", "type": null},
      {"word": "不锈钢", "tag": "属性词", "type": null},
      {"word": "保温杯", "tag": "热词", "type": "add"}
    ],
    "other_words": [
      {"word": "大容量", "tag": "热词", "description": "类目热搜词，排名5"}
    ]
  }
}
```

## 使用场景

### 场景1：新商品发布
为新上架商品生成优质标题

```bash
# 步骤1：获取关键词信息
python3 scripts/interface.py --function get_keyword_info --item_id 123456789

# 步骤2：获取分词器列表
python3 scripts/interface.py --function get_tokenizers
# 假设返回: [{"tokenizer": "qwen-flash", "desc": "..."}, {"tokenizer": "jieba", "desc": "..."}]
# 用户根据描述选择分词器，例如选择 "qwen-flash"

# 步骤3：使用选定的分词器优化标题
python3 scripts/interface.py --function optimize_title --item_id 123456789 --tokenizer_type qwen-flash --use_llm
```

### 场景2：自定义关键词优化
商家想使用特定的关键词优化标题（例如品牌词、活动词等）

```bash
# 使用自定义关键词
python3 scripts/interface.py --function get_keyword_info --item_id 123456789 \
  --custom_keywords "双十一;爆款;旗舰店;限时特惠"

# 然后进行优化
python3 scripts/interface.py --function optimize_title --item_id 123456789
```

**使用自定义关键词的优势：**
- 可以添加品牌词、活动词等特殊关键词
- 适合有特定营销需求的场景
- 结合系统推荐词和自定义词，实现精准优化

## 优化策略

### 删除策略
- **重复词**：标题中出现多次的词
- **低频词**：类目中搜索量极低的词
- **无效词**：对搜索无帮助的词

### 添加策略
- **高热度词**：类目热搜词，排名靠前
- **高曝光词**：该商品历史高曝光的词
- **高相关性**：与商品强相关的词（使用LLM判断）
- **自定义词**：用户指定的关键词（品牌词、活动词等）

### 长度控制
优化后标题长度不超过 60 个字符（中文按2计，英文按1计）

## 技术特点

### 无需LLM的快速优化
- 基于规则和统计的方法
- 优化速度快（< 1秒）
- 成本低，适合大规模应用

### 可选LLM增强
- 使用 `--use_llm` 参数启用
- 提升热词相关性判断准确率
- 耗时增加约0.5-1秒

### 数据驱动
- IGrpah图数据库：类目热搜词、词频统计
- Hologres数据仓库：商品曝光数据
- 实时计算：相似度分析、权重计算