# Baidu Ecosystem Map

Use this file to route a request before you recommend tools or workflows.

## Product Families

| Family | Typical user goal | Primary surfaces | Route here when |
|--------|--------------------|------------------|-----------------|
| Search and discovery | Find current pages, official statements, or trends | `baidu.com` | The request starts as search, fact finding, or SERP interpretation |
| Knowledge and documents | Retrieve encyclopedia-style context or long-form materials | `baike.baidu.com`, `wenku.baidu.com` | The user needs background, explanation, or document-style references |
| Maps and location | Geocoding, routing, nearby search, or local business context | `map.baidu.com`, `lbsyun.baidu.com` | The task is location-aware or map-platform specific |
| AI Cloud and Qianfan | Use models, agents, evaluation, or cloud AI workflows | `cloud.baidu.com`, `qianfan.cloud.baidu.com` | The request is about Baidu AI platform capabilities or implementation |
| Corporate and ecosystem research | Understand Baidu as a vendor, business unit, or partner | `baidu.com` and official business pages | The task is strategic, vendor-related, or ecosystem wide |

## Fast Routing Questions

Ask the smallest set that removes ambiguity:

1. Is this about consumer search, maps, knowledge content, or AI platform work?
2. Is the target context mainland China, Chinese-language research, or a broader global workflow?
3. Does the user need planning only, or do they expect account-level execution?
4. Is the real center of gravity public-web research or cloud-platform implementation?

## Misroutes To Avoid

- "Baidu" when the real request is Baidu Maps Open Platform setup
- "Baidu search" when the task is actually Baike or Wenku source gathering
- "Qianfan" when the user only needs public-web research and no platform work
- "China market research" when the user only needs vendor or product verification

## Output Contract

After routing, state:
- chosen product family
- why it fits
- what it explicitly excludes for this task

If the task spans two families, split the plan into separate sections and owners.
