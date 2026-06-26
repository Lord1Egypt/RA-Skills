---
name: "ai-summary-enhanced"
version: "2.0.0"
description: "AI智能内容总结和项目复盘工具，支持多个大模型API"
author: "AI Skills Team"
tags: ["总结", "复盘", "AI", "GPT", "Claude", "智谱"]
requires: []
---

# AI总结复盘技能 v2.0 - 增强版

智能内容总结和项目复盘工具，支持多个大模型API，提供AI增强的总结能力。

## 技能描述

在基础总结功能之上，支持多个大模型API（智谱AI、OpenAI、Claude、DeepSeek、通义千问、Moonshot），提供更强大的AI总结和复盘能力。当无API时自动降级到基础总结。

## 使用场景

- 用户："用AI总结今天的工作" → AI智能提取关键要点
- 用户："用GPT-4复盘这个项目" → 深度分析项目经验
- 用户："用Claude总结这篇文章" → 高质量文章总结
- 用户："对比不同模型的总结效果" → 多模型对比

## 工具和依赖

### 工具列表

- `scripts/summary_review_llm.py`：AI增强总结复盘模块

### API密钥

**可选**（有API时AI增强，无API时降级到基础总结）：

```bash
# 智谱AI（推荐，性价比高）
export ZHIPU_API_KEY="your-key"

# OpenAI
export OPENAI_API_KEY="your-key"

# Anthropic Claude
export ANTHROPIC_API_KEY="your-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-key"

# 通义千问
export DASHSCOPE_API_KEY="your-key"

# Moonshot
export MOONSHOT_API_KEY="your-key"
```

### 外部依赖

- Python 3.7+
- openai（使用OpenAI时）
- anthropic（使用Claude时）

## 配置说明

### API密钥获取

**智谱AI**（推荐）：
1. 访问：https://open.bigmodel.cn/usercenter/apikeys
2. 创建新的API密钥
3. 新用户有免费额度

**OpenAI**：
1. 访问：https://platform.openai.com/api-keys
2. 创建API密钥

**Anthropic Claude**：
1. 访问：https://console.anthropic.com/
2. 获取API密钥

### 配置文件

创建 `~/.ai_llm_config.json`：
```json
{
  "zhipu": {
    "api_key": "your-zhipu-key"
  },
  "openai": {
    "api_key": "your-openai-key"
  }
}
```

## 使用示例

### 基本用法

```python
from summary_review_llm import AISummaryReview

# 使用智谱AI
system = AISummaryReview(provider="zhipu")

# 内容总结
summary = system.summarize_content(
    "今天完成了用户模块开发...",
    content_type="daily",
    title="工作日报"
)

# 项目复盘
review = system.review_project({
    'name': 'AI助手项目',
    'goals': ['实现对话', '添加知识库'],
    'results': ['对话已实现', '知识库完成80%']
})
```

### 场景1：使用智谱AI总结

用户："用智谱AI总结我的日报"

AI：
```python
system = AISummaryReview(provider="zhipu")
summary = system.summarize_content(daily_content, 'daily', '工作日报')
# 使用GLM-4模型进行智能总结
```

### 场景2：切换模型

用户："用Claude总结这篇文章"

AI：
```python
system_claude = AISummaryReview(provider="anthropic")
summary = system_claude.summarize_content(article, 'article', '文章标题')
# 使用Claude模型进行总结
```

### 场景3：无API时自动降级

用户："总结这段内容"（未配置API）

AI：
```python
system = AISummaryReview(provider="zhipu")
result = system.summarize_content(content, 'daily')
# 检测到无API密钥，自动降级到基础总结
# result['method'] = 'basic'
```

### 场景4：对比不同模型

用户："对比智谱和Claude的总结效果"

AI：
```python
providers = ['zhipu', 'anthropic']
for p in providers:
    system = AISummaryReview(provider=p)
    result = system.summarize_content(content)
    print(f"{p}: {result['summary'][:100]}...")
```

## 支持的总结类型

| 类型 | 说明 | AI提示优化 |
|------|------|-----------|
| daily | 日报 | ✓ 提取任务/问题/计划 |
| meeting | 会议记录 | ✓ 提取议题/决策/行动 |
| project | 项目总结 | ✓ 目标/经验/问题 |
| article | 文章总结 | ✓ 观点/论据/结论 |
| general | 通用内容 | ✓ 关键要点提取 |

## 故障排除

### 问题1：API调用失败

**现象**：提示API错误

**解决**：
1. 检查API密钥是否正确
2. 确认API配额充足
3. 检查网络连接
4. 或使用其他提供商

### 问题2：无API时能否使用

**现象**：没有配置API密钥

**解决**：
- 可以！系统会自动降级到基础总结功能
- 虽然总结质量略低，但仍可用

### 问题3：如何获取智谱API密钥

**现象**：不知道如何获取密钥

**解决**：
1. 访问：https://open.bigmodel.cn/usercenter/apikeys
2. 注册账号
3. 创建API密钥
4. 新用户有免费额度

## v1.0 vs v2.0 对比

| 功能 | v1.0 (基础版) | v2.0 (增强版) |
|------|---------------|---------------|
| 总结方式 | 规则提取 | AI智能总结 |
| 支持模型 | 无 | 智谱/OpenAI/Claude等 |
| 复盘质量 | 基础统计 | AI深度分析 |
| API依赖 | 无 | 可选（有API时AI增强） |
| 降级方案 | - | ✓ 无API时自动降级 |

## 注意事项

1. **API选择**：智谱AI性价比高，新用户有免费额度
2. **自动降级**：无API时仍可使用基础总结功能
3. **成本控制**：注意API使用量，避免超额费用
4. **版本兼容**：与v1.0数据库兼容
5. **模型切换**：切换模型无需重新安装，只需修改provider参数
