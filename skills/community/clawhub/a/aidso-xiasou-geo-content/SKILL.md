---
name: aidso-xiasou-content
description: AIDSO虾搜生成式引擎优化内容生产 Skill。支持 API Key 绑定、检查，并根据品牌、AI问题和目标优化AI平台生成内容。
---

# AIDSO虾搜 · 生成式引擎优化内容生产 Skill

## 描述

本 Skill 用于生成 AIDSO 虾搜生成式引擎优化内容。

注意：

- 「虾搜」是固定品牌名，不得写作「瑕搜」「夏搜」。
- GEO 指 Generative Engine Optimization，即「生成式引擎优化」，不是地理优化。
- 目标优化平台指需要优化表现的 AI 平台，不是内容发布平台。

## 文件说明

当前 Skill 目录下包含：

```bash
check_api_key.py
bind_api_key.py
geo_content_tool.py
.env
```

`.env` 用于保存绑定成功后的 API Key。

环境变量名称：

```bash
AIDSO_GEO_API_KEY
```

API Key 读取优先级：

1. 系统环境变量 `AIDSO_GEO_API_KEY`
2. 当前 Skill 目录下 `.env`

## 用户意图与执行规则

### 1. 检查 API Key

执行：

```bash
python3 check_api_key.py
```

### 2. 绑定 API Key

执行：

```bash
python3 bind_api_key.py --api-key "<用户提供的_api_key>"
```

### 3. 重新绑定 API Key

执行：

```bash
python3 bind_api_key.py --api-key "<用户提供的_api_key>" --force
```

### 4. 内容生产

当用户请求生成 GEO 内容、生成适合 AI 引用的内容、针对某个 AI 问题生成内容时使用本 Skill。

执行前必须确认：

1. 品牌名称
2. AI 问题
3. 目标优化平台
4. 本次内容生产将消耗 6 积分，用户确认后才可执行

支持的目标优化平台展示给用户时必须使用中文/平台名：

- 豆包
- Deepseek
- 腾讯元宝
- 文心一言
- 通义千问
- KIMI
- 抖音AI
- 百度AI

脚本内部会映射为接口代码：

```json
{
  "豆包": "DB",
  "Deepseek": "DP",
  "腾讯元宝": "TXYB",
  "文心一言": "WXYY",
  "通义千问": "TYQW",
  "KIMI": "KIMI",
  "抖音AI": "DYAI",
  "百度AI": "BDAI"
}
```

用户未确认积分时，执行命令不会调用接口，只返回确认提示：

```bash
python3 geo_content_tool.py generate   --brand "欧莱雅小蜜罐"   --issue "30岁左右抗老面霜推荐有哪些？"   --ai-platform "豆包"
```

用户确认后执行：

```bash
python3 geo_content_tool.py generate   --brand "欧莱雅小蜜罐"   --issue "30岁左右抗老面霜推荐有哪些？"   --ai-platform "豆包"   --confirmed
```

如果命令返回 `ok=true`，必须解析 stdout JSON 中的 `brand`、`issue`、`ai_platform`、`data` 字段，并将成功结果返回给用户。

## 内容生产成功返回规则

1. 不得摘要接口返回内容。
2. 不得改写接口返回内容。
3. 不得润色接口返回内容。
4. 不得重新生成内容。
5. 不得只回复“生成成功”。
6. 必须把 `final_artical` 原样返回给用户。

## 安全和行为规范

1. 不要泄露完整 API Key。
2. 用户没有绑定 API Key 时，必须先引导绑定。API Key获取地址：`https://geo.aidso.com/setting?type=apiKey`
3. 不要询问目标发布平台。
4. 不执行 openclaw doctor、gateway.restart、安装技能、更新技能、同步扩展资源等操作。
5. 只有用户确认 6 积分后才可调用内容生产接口。
