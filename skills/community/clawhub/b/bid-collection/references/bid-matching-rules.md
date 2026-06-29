# Tender Lead Matching Rules & Priority Scoring

> This file configures business track matching rules and priority scoring. Users should adjust according to their actual business scope.

## 1. Core Business Tracks & Matching Keywords

| # | Track | Weight | Match Level | Keywords |
|---|-------|--------|-------------|----------|
| 1 | **AI Technical Services** | 20% | High — Core capability | AI, artificial intelligence, machine learning, deep learning, NLP, natural language, computer vision, CV, speech recognition, OCR, intelligent customer service, intelligent interaction, knowledge graph, recommendation system, intelligent analytics |
| 2 | **Large Language Models** | 15% | Dedicated — Strategic direction | LLM, large language model, GPT, generative AI, AIGC, vector database, RAG, prompt, model fine-tuning, model deployment, model training, inference service, multimodal, text-to-image, text generation |
| 3 | **SuYan (Suzhou Research) Procurement** | 10% | Dedicated coverage | SuYan, Suzhou Research Center, China Mobile SuYan, Suzhou Software, China Mobile (Suzhou) Software |
| 4 | **System Construction/Development** | 15% | Core business | Software development, system development, platform development, system integration, application development, microservices, full-stack, backend development, frontend development, API development, API, middleware platform |
| 5 | **Computing Power & Model Services** | 10% | Core business | Computing power, GPU, smart computing, HPC, distributed computing, model training, model inference, AI computing, computing platform, computing cluster, computing scheduling |
| 6 | **Digital Transformation** | 15% | Core business | Digital transformation, data governance, data middle platform, data assets, data platform, data warehouse, data lake, data development, data visualization, BI, big data platform, data standards, data security |
| 7 | **Information Security** | 5% | Extended business | Cybersecurity, data security, classified protection, MLPS, cryptography, Xinchuang, localization, zero trust, security audit, situational awareness, SOC, vulnerability scanning, penetration testing |
| 8 | **Cloud Services** | 5% | Extended business | Cloud platform, public cloud, private cloud, hybrid cloud, IaaS, PaaS, SaaS, cloud migration, cloud-native, containers, K8S, Docker, cloud management platform |
| 9 | **Smart Applications** | 3% | Emerging area | Smart city, smart park, smart government, digital government, smart transportation, smart healthcare, smart education, digital village, smart tourism, smart community |
| 10 | **AI Vision/Content** | 2% | Emerging area | Digital human, virtual human, AIGC, video generation, video understanding, VR, AR, digital twin, 3D modeling, metaverse |

## 2. Key Buyer Focus List

| Buyer Category | Typical Organizations | Priority | Reason |
|----------------|----------------------|----------|--------|
| China Mobile Group | SuYan Research, provincial companies, subsidiaries | 🔴 Highest priority | Core client, long-term partnership |
| Telecom Operators | China Unicom, China Telecom, China Tower | 🔴 High priority | Similar industry, abundant opportunities |
| Government Big Data Bureaus | Provincial/Municipal Big Data Centers | 🔴 High priority | Dense digital transformation projects |
| Government S&T / Industry Bureaus | S&T Bureaus, Industry & IT Bureaus | 🟡 Medium priority | Special fund projects |
| Local SOEs / City Investment | City Investment Groups, State-owned Asset Companies | 🟡 Medium priority | Large digital transformation investment |
| Education / Healthcare | Universities, Hospitals, Education Bureaus | 🟢 Watch | Centralized IT procurement |

## 3. Irrelevant Information Filtering Rules

The following types of information are automatically filtered (low priority / excluded):

1. **Material Procurement**: Office supplies, furniture, printing, clothing, food, etc. (non-IT procurement)
2. **Construction Projects**: Civil engineering, decoration, landscaping, etc. (non-IT projects)
3. **Property Services**: Security, cleaning, catering, property management, etc.
4. **Vehicle Procurement**: Vehicle purchase, maintenance, etc. (non-business related)
5. **Expired (non-canceled)**: Deadline passed >7 days (canceled/abandoned projects are retained)
6. **Duplicates**: Deduplication by project ID / URL
7. **Low Budget**: < ¥100,000 minor purchases (adjustable threshold)

## 4. Priority Scoring Algorithm

```
Score = Track Weight × Budget Factor × Timeliness Factor × Buyer Factor

Track Weight: See table above (core business: 0.05 ~ 0.20)
Budget Factor:
- Budget ≥¥10M: 1.5 (Large project)
- Budget ¥5M–¥10M: 1.2 (Medium project)
- Budget ¥1M–¥5M: 1.0 (Regular project)
- Budget ¥100K–¥1M: 0.7 (Small project)
- Unknown / no budget: 0.5 (Watch)
- Budget <¥100K or non-IT: 0 (Auto-filter)

Timeliness Factor:
- Deadline <7 days: 1.5 (Urgent response)
- Deadline 7–15 days: 1.3 (Rush preparation)
- Deadline 15–30 days: 1.0 (Normal bid prep)
- Deadline 30–60 days: 0.8 (Ample time)
- Deadline >60 days or no deadline: 0.6 (Long-term)
- Past deadline (non-canceled): 0 (Auto-filter)

Buyer Factor:
- 🔴 Highest priority buyers: 1.5
- 🔴 High priority buyers: 1.3
- 🟡 Medium priority buyers: 1.0
- 🟢 Watch buyers: 0.8
- Other buyers: 0.6
```

## 5. Output Priority Classification

| Score Range | Priority | Tag | Suggested Action |
|-------------|----------|-----|------------------|
| ≥40 | 🔴 **Urgent** | Immediate response | Assemble bid team, start bidding process |
| 20–39 | 🟡 **Important** | Evaluate this week | Request tender docs, internal feasibility review |
| 8–19 | 🟢 **Watch** | Add to tracking | Log in lead tracking sheet, continuous follow-up |
| <8 | ⚪ **Reference** | Info reference | Competitor analysis, market insight archive |

## 6. Project Stage Tagging Rules

| Stage | Detection Keywords | Tag |
|-------|--------------------|-----|
| Pre-tender Notice | "procurement意向", "requirements publicity", "RFP notice", "pre-announcement" | `[Pre-tender]` |
| Open Tender | "tender announcement", "competitive磋商", "competitive negotiation", "public tender", "invitation to bid" | `[Open Tender]` |
| Amendment | "correction", "change", "amendment", "supplement", "Q&A", "clarification" | `[Amendment]` |
| Awarded | "winning bid", "awarded", "candidate", "result announcement", "deal" | `[Awarded]` |
| Canceled | "tender cancellation", "abandoned", "terminated", "canceled" | `[Canceled]` |