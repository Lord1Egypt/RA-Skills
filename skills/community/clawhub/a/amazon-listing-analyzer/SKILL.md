# Amazon Listing Analyzer

## 1. Overview

Amazon Listing Analyzer 为 Amazon 卖家提供 Listing 健康度诊断、关键词研究和竞品对标分析，输出结构化的优化建议包。面向月销售额 $5k–$200k、1–5 年运营经验的中阶卖家。不依赖实时 API，所有数据基于内置规则库和模板生成。

## 2. Trigger

用户通过对话发起以下类型的分析请求：
- "分析这个 Listing：..."
- "帮我检查这个 Amazon Listing 的健康度"
- "关键词分析：[产品名称/类目]"
- "竞品对标：[ASIN 或产品描述]"
- "给我一个 Amazon Listing 优化建议"

## 3. Workflow

```
用户输入 → 解析意图（健康度评分 | 关键词分析 | 竞品对标 | 优化建议包）
         → 调用对应分析模块
         → 聚合结果 → 输出结构化报告
```

### 3.1 Listing 健康度评分
1. 解析标题、五点、描述、Search Terms、Backend Keywords
2. 按以下维度打分（每项 0-100）：
   - 标题质量（长度、关键词、前缀品牌词）
   - 五点描述（数量、长度、特征覆盖）
   - 描述质量（结构化程度、可读性）
   - 图片描述（Alt 文本覆盖）
   - 关键词填充（无重复、合理密度）
   - 合规性检查（禁止词、过敏词）
3. 综合得分 = 加权平均
4. 输出诊断结论 + 分项问题列表

### 3.2 关键词分析
1. 基于产品信息生成种子关键词列表
2. 对每个关键词从内置词库查询：
   - 搜索量等级（High/Medium/Low/Unknown）
   - 竞争度等级（High/Medium/Low/Unknown）
   - 相关性评级（1-5）
3. 输出关键词矩阵表 + 建议优先词列表

### 3.3 竞品对标分析
1. 输入竞品 ASIN 或产品描述
2. 从内置竞品模板库匹配相似产品
3. 对比维度：标题结构、价格区间、评分分布、评论数、核心卖点
4. 输出对标表 + 差异化机会点

### 3.4 优化建议包
1. 综合健康度评分 + 关键词分析 + 竞品对标
2. 生成结构化建议：
   - 标题优化建议
   - 五点描述优化建议
   - 描述优化建议
   - 关键词补全建议
   - 图片建议清单
3. 按优先级排序输出

## 4. I/O Specification

### 输入（JSON dict 或对话文本）
```json
{
  "intent": "health_score | keyword_analysis | competitor_benchmark | full_optimization",
  "product_title": "string (optional)",
  "bullet_points": ["string"] * 5 (optional)",
  "product_description": "string (optional)",
  "search_terms": "string (optional)",
  "backend_keywords": "string (optional)",
  "competitor_asin": "string (optional)",
  "product_category": "string (optional)",
  "product_features": ["string"] (optional)"
}
```

### 输出（JSON dict）
```json
{
  "status": "success | partial | error",
  "module": "string",
  "result": {
    "health_score": {
      "total": 0-100,
      "dimensions": {
        "title": {"score": 0-100, "issues": []},
        "bullets": {"score": 0-100, "issues": []},
        "description": {"score": 0-100, "issues": []},
        "keywords": {"score": 0-100, "issues": []},
        "compliance": {"score": 0-100, "issues": []}
      },
      "summary": "string"
    },
    "keyword_analysis": {
      "matrix": [
        {"keyword": "string", "volume": "string", "competition": "string", "relevance": 1-5}
      ],
      "priority_keywords": ["string"],
      "long_tail_keywords": ["string"]
    },
    "competitor_benchmark": {
      "comparisons": [
        {"dimension": "string", "you": "string", "competitor": "string", "opportunity": "string"}
      ],
      "gaps": ["string"]
    },
    "optimization_package": {
      "title": {"current": "string", "suggested": "string", "priority": "high|medium|low"},
      "bullets": [{"current": "string", "suggested": "string", "priority": "string"}],
      "description": {"current": "string", "suggested": "string", "priority": "string"},
      "keywords": {"missing": [], "redundant": [], "suggested": []}
    }
  },
  "errors": ["string"] (optional)
}
```

## 5. Safety

- 不请求或存储用户的真实 Amazon 账户凭证
- 不调用任何外部 API（数据来自内置规则库）
- 所有分析输出为参考建议，不构成 Amazon 平台合规承诺
- 输入文本进行基础长度校验，拒绝超长输入（>10,000 字符）
- 不处理任何涉及个人信息的内容

## 6. Examples

### Example 1: 健康度评分
**输入：**
```json
{"intent": "health_score", "product_title": "Premium Wireless Bluetooth Headphones with Noise Cancellation", "bullet_points": ["High quality sound", "30-hour battery life", "Comfortable fit", "Fast charging", "Foldable design"], "product_description": "Experience music like never before...", "search_terms": "wireless headphones bluetooth noise cancellation"}
```
**输出：**
```json
{
  "status": "success",
  "module": "health_score",
  "result": {
    "health_score": {
      "total": 72,
      "dimensions": {
        "title": {"score": 75, "issues": ["缺少核心关键词搜索量验证", "品牌词位置偏后"]},
        "bullets": {"score": 70, "issues": ["卖点不够具体，缺少数据支撑"]},
        "description": {"score": 68, "issues": ["缺少品牌故事和使用场景描述"]},
        "keywords": {"score": 78, "issues": ["Search Terms 未充分利用"]},
        "compliance": {"score": 90, "issues": []}
      },
      "summary": "Listing 健康度中等偏上，主要改进空间在标题关键词精准度和五点描述的具体性。"
    }
  }
}
```

### Example 2: 关键词分析
**输入：**
```json
{"intent": "keyword_analysis", "product_category": "Electronics > Headphones", "product_features": ["wireless", "noise cancellation", "bluetooth", "long battery life", "comfortable"]}
```
**输出：**
```json
{
  "status": "success",
  "module": "keyword_analysis",
  "result": {
    "keyword_analysis": {
      "matrix": [
        {"keyword": "wireless headphones", "volume": "High", "competition": "High", "relevance": 5},
        {"keyword": "bluetooth headphones", "volume": "High", "competition": "High", "relevance": 5},
        {"keyword": "noise cancelling headphones", "volume": "High", "competition": "Medium", "relevance": 4},
        {"keyword": "long battery life headphones", "volume": "Medium", "competition": "Low", "relevance": 4},
        {"keyword": "comfortable headphones", "volume": "Medium", "competition": "Medium", "relevance": 3}
      ],
      "priority_keywords": ["wireless headphones", "bluetooth headphones", "noise cancelling headphones"],
      "long_tail_keywords": ["long battery life wireless headphones", "comfortable noise cancelling headphones"]
    }
  }
}
```

## 7. Acceptance Criteria

1. **SKILL.md 完整** — 包含 Overview/Trigger/Workflow/I/O/Safety/Examples/Acceptance 全部 7 个模块
2. **handler.py 可独立运行** — `python3 handler.py` 直接执行并输出有效 JSON 结果
3. **测试通过** — `python3 tests/test_handler.py` 至少 3 个测试用例全部通过
4. **元数据完整** — `skill.json` 和 `.claw/identity.json` 字段齐全
5. **无实时 API 依赖** — 所有数据来自内置规则库和模板
6. **输入校验** — 拒绝超长输入（>10,000 字符）并返回错误
7. **输出格式一致** — 所有模块返回统一 JSON 结构
