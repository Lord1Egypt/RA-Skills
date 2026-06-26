# Hero Query Set

Core user scenarios for regression testing. Each query represents a distinct user intent that should route to `kai-business-blueprint`.

## Coverage Matrix

| Dimension | Covered by |
|-----------|-----------|
| Chinese queries | hero-01, 02, 04, 05, 07, 08, 10 |
| English queries | hero-06, 09 |
| Industry: common | hero-01, 06 |
| Industry: retail | hero-04 |
| Industry: finance | hero-07 |
| Industry: manufacturing | hero-08 |
| Industry: cross-border-ecommerce | hero-02 |
| Architecture blueprint | hero-01, 04, 05, 06, 07, 08 |
| Domain-knowledge blueprint | hero-02, 09 |
| --export | hero-03 |
| --refine | hero-10 |

## Queries

### hero-01: 售前需求 → 通用蓝图
- Input: "根据这份售前需求文档生成商业蓝图"
- Expected: route to kai-business-blueprint, industry=common, architecture mode
- Verify: AI reads seed template, extracts entities, writes valid JSON

### hero-02: 跨境电商领域知识
- Input: "生成跨境电商的领域知识大图，包含痛点和策略"
- Expected: route to kai-business-blueprint, industry=cross-border-ecommerce, domain-knowledge mode
- Verify: AI reads domain-knowledge-extraction.md, extracts knowledge entities

### hero-03: 纯导出
- Input: "把这个方案导出为 SVG 架构图"
- Expected: route to kai-business-blueprint, --export command
- Verify: AI skips entity extraction, runs export directly

### hero-04: 零售行业
- Input: "生成零售行业的业务能力蓝图"
- Expected: route to kai-business-blueprint, industry=retail
- Verify: AI reads retail seed template

### hero-05: 微服务架构图
- Input: "帮我画一个微服务架构图"
- Expected: route to kai-business-blueprint, architecture-template route
- Verify: AI reads architecture-design-system.md + microservices.md

### hero-06: English meeting notes
- Input: "Generate a business capability blueprint from these meeting notes"
- Expected: route to kai-business-blueprint, industry=common
- Verify: English triggers work correctly

### hero-07: 金融行业
- Input: "金融行业风控系统蓝图"
- Expected: route to kai-business-blueprint, industry=finance
- Verify: AI reads finance seed template

### hero-08: 制造业
- Input: "生成制造业的生产管理能力蓝图"
- Expected: route to kai-business-blueprint, industry=manufacturing
- Verify: AI reads manufacturing seed template

### hero-09: English strategy canvas
- Input: "Create a strategy canvas showing our competitive advantages"
- Expected: route to kai-business-blueprint
- Verify: "strategy canvas" triggers blueprint skill, not report-creator

### hero-10: Refine
- Input: "这个蓝图的能力层太粗了，帮我细化一下"
- Expected: route to kai-business-blueprint, --refine command
- Verify: AI uses refine flow, not re-generation
