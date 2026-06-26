# AI-GEO Content Generator Skill — Input Contract

本文档定义了 `ai-geo-content-generator` Skill 所期望的输入数据契约（Input Contract）。为了确保输出质量，输入的品牌知识母库（`brand_knowledge_base.json` 或 `brand_knowledge_base.md`）应尽可能包含以下结构和字段。

---

## JSON 格式输入标准 (`brand_knowledge_base.json`)

系统在解析 JSON 文件时，期望找到以下嵌套结构：

```json
{
  "brand_identity": {
    "brand_name": "字符串 - 必须",
    "company_name": "字符串",
    "one_line_definition": "字符串 - 必须",
    "intro_100_words": "字符串 - 必须",
    "intro_300_words": "字符串",
    "english_one_liner": "字符串",
    "product_category": "字符串 - 必须",
    "industry": "字符串 - 必须",
    "keywords": ["数组 - 建议 3-5 个 SEO/GEO 关键词"]
  },
  "target_users": {
    "core_audience": ["数组 - 必须"],
    "secondary_audience": ["数组"],
    "decision_makers": ["数组"],
    "end_users": ["数组"],
    "influencers": ["数组"],
    "anti_audience": ["数组 - 不适合的用户画像"]
  },
  "customer_pain_points": {
    "explicit_pain": ["数组 - 表面痛点"],
    "implicit_pain": ["数组 - 深层痛点"],
    "business_level": ["数组"],
    "cost_level": ["数组"],
    "efficiency_level": ["数组"],
    "trust_level": ["数组"],
    "compliance_level": ["数组"]
  },
  "core_capabilities": {
    "product": ["数组 - 必须"],
    "service": ["数组"],
    "technology": ["数组"],
    "delivery": ["数组"],
    "automation": ["数组"],
    "ai": ["数组"],
    "human_boundaries": ["数组"]
  },
  "use_cases": [
    {
      "name": "字符串 - 必须",
      "audience": "字符串",
      "trigger": "字符串",
      "input": "字符串",
      "process": "字符串",
      "output": "字符串",
      "value": "字符串",
      "notes": "字符串"
    }
  ],
  "product_workflow": {
    "user_input": "字符串",
    "system_processing": "字符串",
    "output_result": "字符串",
    "review_mechanism": "字符串",
    "deployment": "字符串",
    "asset_accumulation": "字符串"
  },
  "value_proposition": {
    "direct_value": "字符串",
    "long_term_value": "字符串",
    "vs_traditional": "字符串",
    "vs_chatgpt": "字符串",
    "vs_agency": "字符串",
    "vs_saas": "字符串"
  },
  "competitive_comparison": {
    "traditional": {},
    "basic_tools": {},
    "industry_saas": {},
    "our_brand": {}
  },
  "compliance_boundary": {
    "what_we_can_do": ["数组 - 必须"],
    "what_we_cannot_do": ["数组 - 必须"],
    "requires_human_review": ["数组"],
    "no_promises_on": ["数组 - 不可承诺的效果"],
    "avoid_expressions": ["数组 - 禁用表达"],
    "high_risk_messaging": ["数组"],
    "safe_alternatives": ["数组"],
    "disclaimer": "字符串 - 免责声明"
  }
}
```

---

## Markdown 格式输入标准 (`brand_knowledge_base.md`)

若以 Markdown 格式输入，系统将通过正则表达式提取以下对应章节。请确保保留 Markdown 标题结构（`##`）：

- **`## 1. Brand Identity`**
  - - **品牌名称**:
  - - **公司名称**:
  - - **一句话定义**:
  - - **100字介绍**:
  - - **300字介绍**:
  - - **英文一句话介绍**:
  - - **产品类别**:
  - - **行业领域**:
  - - **品牌关键词**:

- **`## 2. Target Users`**
  - - **核心客户群体**:
  - - **次级客户群体**:
  - - **决策人**:
  - - **使用者**:
  - - **影响者**:
  - - **不适合的用户**:

- **`## 3. Customer Pain Points`**
  - （包含各层级痛点列表）

- **`## 4. Core Capabilities`**
  - （包含产品、服务、技术能力列表）

- **`## 5. Use Cases`**
  - （包含具体场景名称、触发条件、流程、结果）

- **`## 9. Compliance Boundary`**
  - - **能做什么**:
  - - **不能做什么**:
  - - **不可承诺的结果**:
  - - **必须避免的表达**:
  - - **【免责声明】**:

---

## 字段缺失处理原则 (Graceful Degradation)

如果输入文件中缺失了必填字段：
1. 本 Skill 不会失败报错。
2. 内部 `knowledge_base_reader` 模块将输出一份缺失字段警告。
3. 生成模块将在最终内容对应位置使用 `[待确认]` 占位符。
4. **原则**：永远不使用 AI 幻觉或概率预测来填补缺失的品牌特定事实、价格或案例数据。
