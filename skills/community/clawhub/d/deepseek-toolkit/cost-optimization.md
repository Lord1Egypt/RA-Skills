# DeepSeek API 成本优化策略库

> V4 Pro 降价 75% 后，DeepSeek 已成最具性价比的 AI API 之一。但仍需优化避免浪费。

## 五大优化维度

### 1. 模型选择优化 💎

**核心原则：用最便宜的模型完成当前任务**

| 任务类型 | 推荐模型 | 为什么 |
|---------|---------|--------|
| 日常对话/闲聊 | deepseek-chat (V3) | 最便宜，质量够用 |
| 翻译/摘要/分类 | deepseek-chat (V3) | 这些任务不需要推理 |
| 代码生成/Debug | deepseek-v4-pro | 编码能力最强 |
| 复杂推理/数学 | deepseek-reasonix | 专用推理模型 |
| 结构化数据提取 | deepseek-chat (V3) | 加 JSON mode 即可 |
| 长文档分析 | deepseek-v4-pro | 128K 上下文 |

**省钱公式：**
```
if 任务不需要推理:
    model = "deepseek-chat"      # 最便宜
elif 需要编码:
    model = "deepseek-v4-pro"    # 性价比最优
elif 需要复杂推理:
    model = "deepseek-reasonix"  # 最强但最贵
```

### 2. Prompt 缓存优化 📦

**这是最大的省钱杠杆！缓存命中的 token 按 1 折计费。**

#### 策略 2.1：固定前缀

```python
# ❌ 错误：每次不同的 system prompt
messages = [
    {"role": "system", "content": f"今天是{date}，你是助手"},  # 每天不同 → 缓存失效
    {"role": "user", "content": query}
]

# ✅ 正确：固定 system prompt
SYSTEM_PROMPT = "你是一个有帮助的AI助手。"  # 永远不变 → 缓存命中
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"今天是{date}，{query}"}  # 变化放后面
]
```

#### 策略 2.2：知识库前置

```python
# 把长文档放在 system prompt 前部，每次查询只改 user message
messages = [
    {"role": "system", "content": LONG_KNOWLEDGE_BASE},  # 被缓存
    {"role": "system", "content": "基于以上知识回答用户问题"},
    {"role": "user", "content": user_question}  # 只这部分变化
]
```

#### 策略 2.3：批量相似请求

```python
# ❌ 100次独立调用，缓存利用率低
for question in questions:
    response = call_api([{"role": "user", "content": question}])

# ✅ 合并成 1 次调用，前缀完全复用
batch_prompt = "\n".join([f"Q{i+1}: {q}" for i, q in enumerate(questions)])
response = call_api([
    {"role": "system", "content": SYSTEM_PROMPT},  # 缓存
    {"role": "user", "content": f"回答以下所有问题：\n{batch_prompt}"}
])
```

### 3. Token 管理优化 📊

#### 策略 3.1：精简 Prompt

```python
# ❌ 冗长 Prompt（~200 tokens）
prompt = """
请你作为一个专业的翻译专家，将以下英文内容翻译成中文。
翻译要求：
1. 保持原文的意思不变
2. 语言流畅自然
3. 专业术语要准确
4. 不要遗漏任何内容
翻译以下内容：
{text}
"""

# ✅ 精简 Prompt（~50 tokens，省 75%）
prompt = f"翻译为中文，保持术语准确：\n{text}"
```

#### 策略 3.2：控制输出长度

```python
# ❌ 不限制输出，可能输出 2000 tokens
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

# ✅ 按需限制
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    max_tokens=200  # 简短回答只需 200 tokens
)
```

#### 策略 3.3：Token 计数预估

```python
def estimate_tokens(text):
    """粗略估算 token 数（中文约 1.5 字/token，英文约 4 字符/token）"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.5 + other_chars / 4)

def estimate_cost(input_tokens, output_tokens, model="deepseek-chat"):
    """估算成本（元）"""
    prices = {
        "deepseek-chat": (1, 2),        # ¥1/M input, ¥2/M output
        "deepseek-v4-pro": (2, 8),      # 降价后估算
        "deepseek-reasonix": (4, 16),   # 推理模型
        "deepseek-reasoner": (4, 16),   # R1
    }
    in_price, out_price = prices.get(model, (1, 2))
    cost = (input_tokens * in_price + output_tokens * out_price) / 1_000_000
    return cost
```

### 4. 批处理优化 🔄

#### 策略 4.1：合并同类请求

```python
# ❌ 100 个分类任务 = 100 次 API 调用
for text in texts:
    category = classify(text)  # 每次调用 API

# ✅ 批量分类 = 1 次 API 调用
batch = "\n---\n".join([f"[{i+1}] {t}" for i, t in enumerate(texts)])
prompt = f"对以下文本分类（返回 JSON 数组）：\n{batch}"
categories = call_api(prompt)  # 1 次搞定
```

#### 策略 4.2：并行请求

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI(
    api_key="sk-your-key",
    base_url="https://api.deepseek.com"
)

async def batch_process(tasks):
    """并行处理多个独立任务"""
    coroutines = [process_one(task) for task in tasks]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    return results

async def process_one(task):
    response = await async_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": task}],
        max_tokens=100
    )
    return response.choices[0].message.content
```

### 5. 上下文优化 ✂️

#### 策略 5.1：多轮对话裁剪

```python
def trim_conversation(messages, max_context_tokens=4000):
    """保留最近的对话轮次，裁剪早期内容"""
    total = sum(estimate_tokens(m["content"]) for m in messages)
    
    while total > max_context_tokens and len(messages) > 2:
        # 保留 system prompt（第一条）和最近的对话
        removed = messages.pop(1)  # 删除最早的非 system 消息
        total -= estimate_tokens(removed["content"])
    
    return messages
```

#### 策略 5.2：摘要替代原始上下文

```python
# ❌ 携带完整历史（token 爆炸）
messages = [
    system_prompt,
    *full_history_50_turns,  # 50000+ tokens
    new_question
]

# ✅ 先摘要历史，再回答新问题
summary = call_api("用 3 句话总结以下对话：\n" + str(full_history))
messages = [
    system_prompt,
    {"role": "system", "content": f"历史对话摘要：{summary}"},
    new_question  # 只需 ~500 tokens 上下文
]
```

## 成本计算器

### 场景 1：客服机器人（日均 1000 对话）
```
每对话平均：500 input + 300 output tokens
日均总量：500K input + 300K output tokens

模型对比：
- V3 (deepseek-chat):   ¥0.5/天 + ¥0.6/天 = ¥1.1/天 ≈ ¥33/月
- V4 Pro:               ¥1.0/天 + ¥2.4/天 = ¥3.4/天 ≈ ¥102/月
- R1 (deepseek-reasoner): ¥2.0/天 + ¥4.8/天 = ¥6.8/天 ≈ ¥204/月

推荐：V3 + Prompt 缓存 → 实际成本可降至 ¥15-20/月
```

### 场景 2：代码助手（日均 200 请求）
```
每请求平均：2000 input + 1000 output tokens
日均总量：400K input + 200K output tokens

模型对比：
- V3:   ¥0.4/天 + ¥0.4/天 = ¥0.8/天 ≈ ¥24/月
- V4 Pro: ¥0.8/天 + ¥1.6/天 = ¥2.4/天 ≈ ¥72/月
- Reasonix: ¥1.6/天 + ¥3.2/天 = ¥4.8/天 ≈ ¥144/月

推荐：V4 Pro（代码质量显著更好，多花的钱值得）
```

### 场景 3：内容生成（日均 50 篇文章）
```
每篇平均：1000 input + 2000 output tokens
日均总量：50K input + 100K output tokens

模型对比：
- V3:   ¥0.05/天 + ¥0.2/天 = ¥0.25/天 ≈ ¥7.5/月
- V4 Pro: ¥0.1/天 + ¥0.8/天 = ¥0.9/天 ≈ ¥27/月

推荐：V3（内容生成质量差异不大，V3 性价比最高）
```

## 优化检查清单

使用前过一遍这个清单：

- [ ] 是否选择了最合适的模型？（日常用 V3，编码用 V4 Pro）
- [ ] system prompt 是否固定？（启用缓存）
- [ ] 是否设置了 max_tokens？（避免浪费）
- [ ] Prompt 是否足够精简？（去掉废话）
- [ ] 是否可以批量处理？（减少调用次数）
- [ ] 多轮对话是否做了裁剪？（控制上下文长度）
- [ ] 是否使用了错误重试？（避免重复扣费）
- [ ] 是否监控了每日用量？（及时发现异常）

## 价格变动历史

| 日期 | 事件 | 影响 |
|------|------|------|
| 2025-05 | V4 Pro 永久降价 75% | 性价比暴涨，从 ¥8/32 降至约 ¥2/8 |
| 2025-05 | Reasonix 发布 | 原生编码 Agent，定位高端 |
| 2025-01 | V3 发布 | 首款超低成本模型 |
| 2025-01 | R1 发布 | 开源推理模型，引发行业震动 |
