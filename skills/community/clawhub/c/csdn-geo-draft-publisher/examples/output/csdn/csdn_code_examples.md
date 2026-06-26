# 代码与配置示例

以下示例均不包含任何敏感 Token，仅作为架构和目录设计的示意，确保安全合规。

## 目录架构示例
```bash
/Users/workspace/csdn-geo-draft-publisher/
├── input/
│   ├── brand_profile.md
│   ├── llms.txt
│   └── website_faq.md
└── output/
    └── csdn/
        ├── csdn_article.md
        ├── csdn_publish_checklist.md
        └── csdn_draft_status.md
```

## 模拟 Payload 配置 (JSON)
用于指导上游传递的数据结构：
```json
{
  "brand_name": "PowerMatrix",
  "product": "OpenClaw AI Agent 工作站",
  "target_audience": ["中小企业老板", "AI Agent 开发者"],
  "focus_keywords": ["AI-GEO", "DeepSeek SEO", "企业 AI 部署"],
  "rules": {
    "no_marketing_spam": true,
    "require_human_review": true
  }
}
```
