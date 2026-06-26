# Kimi/DeepSeek 自然语言洞察生成指南

## 调用方式

在数据分析 Skill 中，Agent 应在图表生成后调用 Kimi 或 DeepSeek API 生成自然语言洞察。

### 推荐模型

| 模型 | 适用场景 | API 端点 |
|------|---------|---------|
| Kimi (moonshot-v1-8k) | 中文洞察、业务解读 | https://api.moonshot.cn/v1/chat/completions |
| DeepSeek (deepseek-chat) | 中文洞察、深度分析 | https://api.deepseek.com/v1/chat/completions |

### Prompt 模板

```
你是一位资深数据分析师。请根据以下数据分析结果，生成简洁、专业的自然语言洞察报告。

【数据概览】
- 行数: {shape[0]}
- 列数: {shape[1]}
- 数值列: {numeric_columns}
- 分类列: {categorical_columns}

【描述性统计】
{numeric_stats_json}

【分类列 Top5】
{categorical_stats_json}

【数据清洗记录】
{clean_log}

【图表描述】
{charts_description}

请输出：
1. 数据质量评估（缺失值、异常值、重复值）
2. 核心发现（3-5 条关键洞察）
3. 分布特征（数值列分布、分类列占比）
4. 异常点识别（离群值、极端值）
5. 业务建议（基于数据的行动建议）

要求：语言简洁专业，避免过度技术化，突出业务价值。
```

### 调用示例（Python）

```python
import os
import json
import requests

def generate_insight(summary: dict, model: str = "kimi") -> str:
    """调用 Kimi/DeepSeek 生成洞察"""
    api_key = os.environ.get("KIMI_API_KEY") if model == "kimi" else os.environ.get("DEEPSEEK_API_KEY")
    endpoint = "https://api.moonshot.cn/v1/chat/completions" if model == "kimi" else "https://api.deepseek.com/v1/chat/completions"
    
    prompt = build_prompt(summary)  # 使用上述模板
    
    resp = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "moonshot-v1-8k" if model == "kimi" else "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

### 环境变量配置

Agent 应提示用户配置 API Key：

```bash
# Kimi
export KIMI_API_KEY="your-kimi-api-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

或在 `~/.zshrc` / `~/.bashrc` 中永久配置。

## 洞察输出格式

生成的洞察应为 Markdown 格式，包含：

```markdown
### 一、数据质量评估
...

### 二、核心发现
1. ...
2. ...

### 三、分布特征
...

### 四、异常点识别
...

### 五、业务建议
...
```

此内容将直接插入 Word 报告的「AI 数据洞察」章节。
