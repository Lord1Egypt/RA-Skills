# 混合路由方案

> 用多个模型组合，在质量和成本之间找到最优平衡。

---

## 方案 1：三级路由（推荐）

适合：大多数应用场景

```
用户请求
    ↓
┌─────────────────────┐
│  级别 1：快速模型     │  DeepSeek V3.1 / GPT-4.1 nano
│  成本：$0.08-0.17/10K│  处理 70% 的请求
│  延迟：< 500ms       │  分类、提取、简单问答
└────────┬────────────┘
         ↓ 不满意/复杂
┌─────────────────────┐
│  级别 2：均衡模型     │  DeepSeek V4 Pro / GPT-4.1 mini
│  成本：$0.20-0.32/10K│ 处理 20% 的请求
│  延迟：< 1s          │  对话、写作、分析
└────────┬────────────┘
         ↓ 仍不满意
┌─────────────────────┐
│  级别 3：高端模型     │  Claude Sonnet 4 / GPT-4.1
│  成本：$1.60-1.95/10K│ 处理 10% 的请求
│  延迟：< 3s          │  推理、创意、代码审查
└─────────────────────┘
```

**加权成本**：$0.12 + $0.064 + $0.195 = **$0.38/10K 请求**
**对比全用 Sonnet 4**：省 **80%**

### 路由判断规则

```python
def classify_complexity(prompt: str) -> str:
    """基于规则的快速分类（0 API 成本）"""
    
    # 超复杂信号
    complex_signals = [
        "分析", "策略", "研究", "设计",
        "架构", "优化", "评估", "对比分析",
        "debug", "refactor", "review"
    ]
    
    # 中等信号  
    medium_signals = [
        "写", "生成", "翻译", "总结",
        "解释", "如何", "为什么",
        "write", "generate", "explain"
    ]
    
    # 简单信号
    simple_signals = [
        "分类", "提取", "格式化", "是/否",
        "翻译这句话", "改写",
        "classify", "extract", "format"
    ]
    
    prompt_lower = prompt.lower()
    
    # 字数判断
    if len(prompt) > 2000:
        return "complex"
    
    # 信号匹配
    for s in complex_signals:
        if s in prompt_lower:
            return "complex"
    for s in medium_signals:
        if s in prompt_lower:
            return "medium"
    
    return "simple"
```

---

## 方案 2：双语路由

适合：中英文混合场景

```
输入语言检测
    ↓
┌──────────────┐    ┌──────────────┐
│   中文输入     │    │   英文输入     │
│      ↓        │    │      ↓        │
│  DeepSeek     │    │  GPT-4.1     │
│  V4 Pro       │    │  mini        │
│  (中文最强)    │    │  (英文均衡)    │
└──────────────┘    └──────────────┘
```

**原因**：DeepSeek 中文能力远超同价位英文模型，但英文场景 GPT 系更稳定。

---

## 方案 3：任务类型路由

适合：多任务型应用

```python
TASK_MODEL_MAP = {
    # 编码任务
    "code_generation": "deepseek-v4-pro",   # 编码能力强
    "code_review": "claude-sonnet-4",        # 审查需要深度理解
    "code_explain": "deepseek-v3.1",         # 解释用便宜模型
    
    # 内容任务
    "write_article": "claude-sonnet-4",      # 写作质量好
    "write_email": "gpt-4.1-mini",           # 邮件用便宜模型
    "translate": "deepseek-v3.1",            # 翻译用便宜模型
    "summarize": "gpt-4.1-nano",             # 摘要用最便宜模型
    
    # 分析任务
    "data_analysis": "gpt-4.1",              # 分析需要准确
    "sentiment": "gpt-4.1-nano",             # 情感分类简单
    "extract": "gpt-4.1-nano",               # 信息提取简单
    
    # 推理任务
    "reasoning": "claude-opus-4",            # 深度推理
    "math": "o3",                            # 数学专用
    "strategy": "claude-opus-4",             # 策略分析
}
```

---

## 方案 4：时间路由

适合：有高峰低谷的应用

```
高峰时段（工作日 9:00-18:00）
    → 用便宜模型（DeepSeek V3.1）
    → 保证响应速度

低谷时段（夜间/周末）
    → 用 Batch API（50% off）
    → 处理非实时任务

紧急请求
    → 用高端模型
    → 不计成本
```

---

## 方案 5：质量自适应路由

适合：对质量有要求但也要控制成本

```python
def adaptive_route(prompt, user_tier):
    """根据用户等级自适应路由"""
    
    if user_tier == "free":
        return "gpt-4.1-nano"        # 免费用户用最便宜
    elif user_tier == "basic":
        return "deepseek-v3.1"       # 基础用户用低成本
    elif user_tier == "pro":
        return "deepseek-v4-pro"     # Pro 用户用中档
    elif user_tier == "enterprise":
        return "claude-sonnet-4"     # 企业用户用高端
```

---

## 成本对比

### 场景：日均 10K 请求的 SaaS 应用

| 方案 | 月成本 | 质量 | 推荐场景 |
|------|--------|------|---------|
| 全用 Claude Opus 4 | $2,610 | ⭐⭐⭐⭐⭐ | 不差钱 |
| 全用 Claude Sonnet 4 | $585 | ⭐⭐⭐⭐ | 高质量要求 |
| 全用 GPT-4.1 | $480 | ⭐⭐⭐⭐ | OpenAI 生态 |
| 全用 DeepSeek V4 Pro | $90 | ⭐⭐⭐⭐ | 成本优先 |
| **三级路由（推荐）** | **$114** | **⭐⭐⭐⭐** | **最佳性价比** |
| 全用 DeepSeek V3.1 | $51 | ⭐⭐⭐ | 极低预算 |
| 全用 GPT-4.1 nano | $24 | ⭐⭐ | 测试/原型 |

### 关键洞察
1. **三级路由是最优解** — 成本接近 DeepSeek V4 Pro 全用，但复杂任务质量大幅提升
2. **DeepSeek V4 Pro 是性价比之王** — 质量接近 GPT-4.1，价格仅 1/5
3. **Claude Opus 4 只在必要时用** — 10% 的高端请求就够了
4. **nano 模型被严重低估** — 简单任务用 nano 足够，成本几乎为零

---

## 实施建议

### 第一阶段：基础路由（1天）
1. 部署 DeepSeek V4 Pro 作为默认模型
2. 添加长度 + 关键词路由规则
3. 接入 Anthropic 作为复杂任务后端

### 第二阶段：智能路由（3天）
1. 训练/部署复杂度分类器
2. 实现语义缓存
3. 添加成本监控面板

### 第三阶段：精细化（1周）
1. 按用户等级路由
2. A/B 测试不同模型组合
3. 实现自动降级（配额用完自动切换便宜模型）
