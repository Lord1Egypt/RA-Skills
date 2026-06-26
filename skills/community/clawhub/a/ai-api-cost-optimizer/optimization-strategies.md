# 成本优化策略库

> 从 5 大维度优化 AI API 成本，实战验证有效。

---

## 维度 1：Token 优化 📝

### 1.1 Prompt 精简
- **目标**：减少不必要的 token 消耗
- **方法**：
  - 删除礼貌用语（"请"、"谢谢"、"帮我"）
  - 用缩写替代完整描述（"JSON格式" → "json"）
  - 合并重复指令
  - 用 System Prompt 存放固定指令（可缓存）
  - 使用结构化格式（YAML/JSON 比自然语言更紧凑）

**示例：**
```
# 优化前（38 tokens）
你好，请帮我将以下英文文本翻译成中文，要求翻译准确、流畅、自然，保持原文的语义和语气：
[文本]

# 优化后（12 tokens，节省68%）
翻译为中文，保持原文语义和语气：
[文本]
```

### 1.2 System Message 复用
- 将固定指令放在 System Message 中
- 利用 Anthropic 的缓存机制（90% off 读取）
- 适合场景：客服机器人、代码审查、内容审核

### 1.3 输出控制
- 设置 `max_tokens` 限制输出长度
- 用 `stop` 序列提前终止
- 要求 JSON 格式输出时指定 schema（减少废话）

### 1.4 Few-shot → Zero-shot
- 优先尝试 zero-shot，不够再加 few-shot
- 每个 example 消耗 tokens，3 个 example 可能多消耗 30%
- 替代方案：用 System Message 描述规则 + 1 个 example

---

## 维度 2：缓存策略 🗄️

### 2.1 语义缓存（Semantic Cache）
- **原理**：相似问题直接返回缓存答案
- **工具**：Redis + 向量相似度、GPTCache
- **适用**：FAQ、客服、重复性查询
- **节省**：30-60% 调用量

```python
# 语义缓存示例（伪代码）
import redis
from openai import OpenAI

r = redis.Redis()
client = OpenAI()

def cached_chat(prompt, threshold=0.92):
    # 向量检索相似问题
    embedding = get_embedding(prompt)
    cached = r.vector_search("cache", embedding, threshold)
    
    if cached:
        return cached  # 缓存命中，省一次 API 调用
    
    # 缓存未命中，调用 API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # 存入缓存
    r.vector_store("cache", embedding, response)
    return response
```

### 2.2 Anthropic 缓存（原生支持）
- **缓存写入**：+25% 成本（首次）
- **缓存读取**：90% off（后续）
- **最佳实践**：System Prompt > 1024 tokens 时启用
- **TTL**：5 分钟（最低），可延长

```python
# Anthropic 缓存示例
import anthropic

client = anthropic.Anthropic()

# 固定的 System Prompt（会被缓存）
SYSTEM_PROMPT = """
你是一个专业的代码审查专家。请按以下维度审查代码：
1. 安全性：检查 SQL 注入、XSS 等安全漏洞
2. 性能：检查循环、数据库查询等性能问题
3. 可维护性：检查命名、注释、代码结构
4. 逻辑正确性：检查边界条件、异常处理
"""  # > 1024 tokens，适合缓存

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "审查这段代码: ..."}]
)
```

### 2.3 响应缓存（Response Cache）
- **适用**：完全相同的问题
- **实现**：Redis/Memcached，key = hash(prompt)
- **节省**：10-20% 调用量

---

## 维度 3：模型路由 🛤️

### 3.1 复杂度分级
根据任务复杂度路由到不同模型：

```
简单任务（分类/提取/翻译）→ GPT-4.1 nano / DeepSeek V3.1
中等任务（对话/写作/分析）→ GPT-4.1 mini / DeepSeek V4 Pro
复杂任务（推理/代码/创意）→ Claude Sonnet 4 / GPT-4.1
超复杂任务（研究/策略）→ Claude Opus 4 / o3
```

### 3.2 路由决策器
用一个极小的模型判断任务复杂度：

```python
def route_task(user_input):
    """用 nano 模型做路由决策（成本 ~$0.00001/次）"""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{
            "role": "user",
            "content": f"""判断这个任务的复杂度（简单/中等/复杂/超复杂），只回答一个词：
            
任务：{user_input}"""
        }],
        max_tokens=5
    )
    
    complexity = response.choices[0].message.content.strip()
    
    MODEL_MAP = {
        "简单": "deepseek-v3.1",
        "中等": "deepseek-v4-pro", 
        "复杂": "claude-sonnet-4",
        "超复杂": "claude-opus-4"
    }
    
    return MODEL_MAP.get(complexity, "deepseek-v4-pro")  # 默认中等
```

### 3.3 级联路由（Cascade）
先用便宜模型试，不满意再升级：

```
DeepSeek V3.1 ($0.17/10K) → 满意？→ 返回
                              ↓ 不满意
GPT-4.1 mini ($0.32/10K) → 满意？→ 返回  
                              ↓ 不满意
Claude Sonnet 4 ($1.95/10K) → 返回
```

**成本分析**：如果 70% 的问题被 V3.1 解决，20% 被 mini 解决，10% 需要 Sonnet：
- 加权成本：$0.17×0.7 + $0.32×0.2 + $1.95×0.1 = $0.12 + $0.064 + $0.195 = $0.38/10K
- 比全用 Sonnet 4 省 80%

---

## 维度 4：批量处理 📦

### 4.1 OpenAI Batch API
- **折扣**：50% off
- **延迟**：24 小时内返回
- **适用**：非实时场景（数据处理、内容生成、翻译）

```python
from openai import OpenAI

client = OpenAI()

# 创建批量任务
batch = client.batches.create(
    input_file_id="file-xxx",
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

# 50% off — GPT-4.1 mini 批量价 $0.20/1M（原价 $0.40）
```

### 4.2 DeepSeek 批量折扣
- 大量调用可联系商务获取批量折扣
- 缓存命中 > 70% 时实际成本已极低

### 4.3 合并请求
- 多个小任务合并为一个大请求
- 例：10 条翻译合并为 1 次 API 调用
- 节省：10 次请求 overhead → 1 次

---

## 维度 5：架构优化 🏗️

### 5.1 降频策略
- 去重：相同输入不重复调用
- 防抖：用户快速输入时延迟调用
- 增量更新：只处理变化部分

### 5.2 流式处理 + 提前终止
- 流式输出后，发现质量不够好 → 提前中断
- 节省输出 tokens（输出 tokens 通常比输入贵 2-5 倍）

### 5.3 预计算 + 物化视图
- 预计算常见问题的答案
- 热门查询用缓存，冷门查询才调 API
- 类似数据库的物化视图思路

### 5.4 异步 vs 同步
- 实时交互 → 用流式
- 后台处理 → 用 Batch API（50% off）
- 定时任务 → 用 Batch API

---

## 成本优化检查清单

对每个项目，检查以下项目：

- [ ] 是否使用了 Prompt 精简？（目标：减少 30% tokens）
- [ ] 是否启用了缓存？（语义缓存 or API 原生缓存）
- [ ] 是否按复杂度路由模型？（不要用大模型做简单任务）
- [ ] 是否使用了 Batch API？（非实时任务 50% off）
- [ ] 是否设置了 max_tokens？（防止输出爆炸）
- [ ] 是否实现了去重/防抖？（防止重复调用）
- [ ] 是否考虑了开源模型自部署？（高频+固定场景）
- [ ] 是否在监控 API 用量？（每周 review 一次）
- [ ] 是否在用最便宜的模型完成任务？（不是越贵越好）
- [ ] 是否合并了小请求？（10 次 → 1 次）
