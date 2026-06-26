---
name: aidso-xiasou
description: AIDSO虾搜 GEO 一体化 Skill，支持统一 API Key 绑定、检查、品牌诊断报告、品牌知识库、GEO 内容生产、GEO 问题挖掘。
---

# AIDSO虾搜 GEO 一体化 Skill

## 功能范围

本 Skill 将以下 4 个能力合并到同一个 Skill 包中：

1. GEO 品牌诊断报告
2. GEO 内容生产
3. 品牌知识库添加
4. GEO 监测问题挖掘

## API Key 统一规则

当前 Skill 使用统一 API Key：

```bash
AIDSO_GEO_API_KEY
```

API Key 读取优先级：

1. 系统环境变量 `AIDSO_GEO_API_KEY`
2. 当前 Skill 目录下 `.env`

绑定后会在当前 Skill 根目录生成 `.env`，内容生产、知识库、品牌诊断、问题挖掘四个能力都会直接读取该 `.env`。

问题挖掘脚本 `prompt_research.py` 已改为读取统一 API Key 配置；`.state/prompt_research_bindings.json` 仅用于保存问题挖掘任务状态，不再保存 API Key。

## 通用 API Key 操作

### 检查 API Key

```bash
python3 check_api_key.py
```

### 绑定 API Key

```bash
python3 bind_api_key.py --api-key "<用户提供的_api_key>"
```

### 重新绑定 API Key

```bash
python3 bind_api_key.py --api-key "<用户提供的_api_key>" --force
```

如果未绑定 API Key，提示用户：

```text
使用虾搜 GEO 功能前，需要先绑定 AIDSO API Key。
API Key 获取地址：https://geo.aidso.com/setting?type=apiKey
请发送：绑定 api-key：你的_api_key
```

## 功能一：GEO 品牌诊断报告

### 触发场景

- 帮我生成某品牌的 GEO 报告
- 给我一份某品牌的品牌诊断报告
- 某品牌的 GEO 表现如何
- 获取某品牌的诊断问题

### 执行流程

1. 先检查 API Key：

```bash
python3 check_api_key.py
```

2. 获取诊断问题：

```bash
python3 geo_report_tool.py questions --brand-name "<品牌名称>"
```

3. 将问题列表展示给用户，允许用户替换、删除、追加问题。

4. 用户确认问题后，计算积分：

```text
消耗积分数 = 问题数 × 4
```

5. 用户确认积分后执行：

```bash
python3 geo_report_tool.py report --brand-name "<品牌名称>" --questions-json '<JSON数组字符串>'
```

### 品牌诊断强制规则

1. 发起诊断任务前必须先让用户确认诊断问题。
2. 发起诊断任务前必须先让用户确认消耗积分数。
3. 成功后必须返回接口返回的 `brand_name` 和 `report_url`。
4. 只有 `report_url` 返回 URL 时才算成功。
5. 不得把任务 ID 当成报告地址。

## 功能二：GEO 内容生产

### 触发场景

- 生成 GEO 内容
- 针对某个 AI 问题生成内容
- 生成适合 AI 引用的内容
- 为某品牌生成内容优化文章

### 必要参数

1. 品牌名称
2. AI 问题
3. 目标优化平台
4. 用户确认消耗 6 积分

### 支持平台

- 豆包
- Deepseek
- 腾讯元宝
- 文心一言
- 通义千问
- KIMI
- 抖音AI
- 百度AI

查看平台：

```bash
python3 geo_content_tool.py platforms
```

未确认积分时：

```bash
python3 geo_content_tool.py generate --brand "<品牌名称>" --issue "<AI问题>" --platform "<平台名称>"
```

用户确认后：

```bash
python3 geo_content_tool.py generate --brand "<品牌名称>" --issue "<AI问题>" --platform "<平台名称>" --confirmed
```

### 内容生产返回规则

1. 不得摘要接口返回内容。
2. 不得改写接口返回内容。
3. 不得润色接口返回内容。
4. 不得重新生成内容。
5. 不得只回复“生成成功”。
6. 必须把接口返回内容原样返回给用户。

## 功能三：品牌知识库添加

### 触发场景

- 添加品牌知识
- 写入品牌知识库
- 保存某品牌的知识内容
- 给某品牌补充知识库内容

### 执行命令

```bash
python3 knowledge_tool.py add --brand-name "<品牌名称>" --content "<知识内容>"
```

### 知识库规则

1. 只支持添加知识库内容。
2. 不支持删除、修改、查询知识库。
3. 返回成功后明确告知用户知识已添加。

## 功能四：GEO 监测问题挖掘

### 触发场景

- 帮我生成某品牌的 GEO 问题
- 帮我挖掘某品牌的 AI 搜索问题
- 给某品牌生成 30 / 50 / 100 个问题
- 帮我做问题挖掘

### 必要参数

1. 品牌名称 `brand_name`
2. 产品词 `product_names`，可为空
3. 生成问题数量 `gen_question_num`，仅支持 30、50、100

### 积分规则

| 生成问题数量 | 消耗积分 |
|---|---:|
| 30 个问题 | 18 积分 |
| 50 个问题 | 20 积分 |
| 100 个问题 | 25 积分 |

### 执行流程

1. 先检查 API Key：

```bash
python3 check_api_key.py
```

2. 用户未选择数量时，引导用户选择 30 / 50 / 100。

3. 用户确认积分后执行：

```bash
python3 prompt_research.py "<用户原始问题挖掘请求>"
```

示例：

```bash
python3 prompt_research.py "帮我给京东生成 50 个问题"
```

4. 查询任务结果时执行：

```bash
python3 prompt_research.py "继续"
```

### 问题挖掘返回规则

1. 如果接口返回 `success`，完整返回问题列表。
2. 不得自行补充接口未返回的问题。
3. 不得用二次总结替代接口结果。
4. 可以整理成 Markdown 表格，但不得改变字段含义。

## 全局安全规则

1. 不要在回复中泄露完整 API Key。
2. 如果需要展示 API Key，只能展示脱敏版本。
3. 不得默认使用企业版预授权。
4. 用户没有绑定 API Key 时，必须先引导绑定。
5. 「虾搜」不得写作「瑕搜」「夏搜」。
6. GEO 指生成式引擎优化，不是地理优化。
