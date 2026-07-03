# AI Product Strategy Document Template

## Document Information

| Field | Content |
|------|------|
| Product Name | [AI Product Name] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |
| AI Product Type | AI-Native / AI-Enhanced / AI-Infrastructure |

---

## 1. Executive Summary

[Describe in one paragraph: what AI product we are building, why now, and the expected business outcomes]

## 2. AI Opportunity Assessment

### 2.1 Problem Definition

- **Who is the user**:
- **What is their pain point** (quantified):
- **Why traditional software/manual approaches cannot solve it well**:

### 2.2 AI Feasibility Score

| Dimension | Score (1-5) | Weight | Weighted Score | Basis |
|------|----------|------|--------|------|
| User Pain Point Intensity | | 25% | | |
| AI Solution Feasibility | | 25% | | |
| Data Availability | | 15% | | |
| Business Return | | 15% | | |
| Competitive Urgency | | 10% | | |
| Technical Difficulty (inverse) | | 10% | | |
| **Total Score** | | | | ≥3.5 Proceed |

### 2.3 Task Characteristics Analysis

| Characteristic | Assessment | AI Suitability |
|------|------|---------|
| Task Repetitiveness | High/Medium/Low | Higher = more suitable for AI |
| Error Tolerance | High/Medium/Zero Tolerance | Zero tolerance = assist only |
| Creativity Requirement | High/Medium/Low | High → GenAI advantage |
| Determinism Requirement | High/Medium/Low | High → traditional software is better |

---

## 3. Market & Competition

### 3.1 Market Overview

- **Market Size (TAM/SAM/SOM)**:
- **Growth Trends**:
- **Key Drivers**:

### 3.2 AI Competitive Analysis

| Competitor | Product Type | Model Used | Pricing Model | Strengths | Weaknesses |
|------|---------|---------|---------|------|------|
| | | | | | |

### 3.3 Competitive Moat Assessment (Hamilton Helmer AI Edition)

| Force | Score | Implementation Path |
|------|------|---------|
| Data Network Effects | | |
| Switching Costs | | |
| Proprietary Data | | |

---

## 4. Product Strategy

### 4.1 Wedge Strategy

- **Narrow Scenario Chosen**:
- **Target Users**:
- **Core Value**:
- **Path to Adjacent Scenarios**:

### 4.2 DHM Score

| Dimension | Score (1-10) | Description |
|------|----------|------|
| Delightful | | |
| Hard-to-copy | | |
| Margin-enhancing | | |

### 4.3 Data Flywheel Design

```
User Usage → Collect [XX Data] → AI Improves via [XX Method] → Better Experience → More Users
```

- Core Data Assets:
- Data Collection Mechanism:
- AI Improvement Mechanism:

---

## 5. Technical Strategy

### 5.1 Model Strategy

| Decision | Choice | Rationale |
|------|------|------|
| Build/Buy/Fine-tune | | |
| Preferred Model | | |
| Model Routing Strategy | | |
| Context Window Requirements | | |
| Latency Requirements | | |

### 5.2 Data Strategy

| Decision | Plan |
|------|------|
| Training Data Sources | |
| Data Annotation Strategy | |
| Evaluation Dataset Construction | |
| User Feedback Collection | |

### 5.3 Key Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|--------|------|------|
| Model Hallucination | | | RAG + Guardrails + Confidence Display |
| Upstream Model Changes | | | Evaluation Baseline + Fast Switching |
| Excessive Inference Costs | | | Model Routing + Caching + Optimization |
| Security/Compliance | | | Guardrails + Red Team Testing + Compliance Review |

---

## 6. Business Model

### 6.1 Pricing Strategy

| Decision | Plan |
|------|------|
| Pricing Model | Hybrid (Base Fee + Usage) / Outcome-Based / Tiered + AI Quota |
| Plan Structure | |
| Free Tier Strategy | |
| Target AI Gross Margin | >60% |

### 6.2 Token Economics

| Metric | Estimate |
|------|------|
| Average Cost Per Interaction | |
| Monthly Active Users | |
| Monthly Inference Total Cost | |
| Monthly Revenue | |
| AI Gross Margin | |

### 6.3 Milestones

| Phase | Timeline | Goal | Success Criteria |
|------|------|------|---------|
| Alpha | | Internally usable | Team daily usage |
| Beta | | Friendly customer validation | 3 customers paying |
| GA | | Official commercial launch | Product stable + sales ready |
| Scale | | Scaled growth | ARR target met |

---

## 7. Roadmap (Now-Next-Later)

### Now (This Quarter)
| Item | Goal | Dependencies |
|------|------|------|
| | | |

### Next (Next Quarter)
| Item | Goal | Dependencies |
|------|------|------|
| | | |

### Later (Future)
| Direction | What to Validate/Prepare |
|------|-----------------|
| | |

---

## v1.1.0 New: Model Selection Strategy

### Model Selection Decision Framework
| Dimension | Closed-source Models (GPT-4/Claude) | Open-source Models (Llama/Qwen) | Self-developed Models |
|---------|---------------------|-------------------|---------|
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | $$ | $ | $$$$ |
| Data Security | Requires evaluation | Controllable | Fully controllable |
| Customization | Limited | Fine-tunable | Fully customizable |
| Maintenance Cost | Low | Medium | High |
| Go-live Speed | Fast (API) | Medium (Deploy + Fine-tune) | Slow (Training + Deploy) |

### Model Routing Strategy
```
User Request → Classifier Determines
  ├── Simple Q&A → Small Model (GPT-3.5/Qwen-7B)
  ├── Complex Reasoning → Large Model (GPT-4/Claude)
  ├── Specialized Domain → Fine-tuned Model
  ├── Real-time Requirements → Edge-deployed Small Model
  └── Sensitive Data → Privately Deployed Model
```

### LLM Industry Chain Selection Considerations
| Layer | Selection Key Points | Representative Solutions |
|------|---------|---------|
| Compute Layer | GPU supply stability, cost | NVIDIA / Domestic GPU |
| Platform Layer | MLOps maturity, multi-model management | LangChain / Dify / MLflow |
| Model Layer | Performance/cost/security balance | GPT-4 / Claude / Qwen / Llama |
| Application Layer | Scenario fit, user experience | Industry-specific solutions |

---

## 8. Model Selection Trend Considerations (V1.1.0 New)

### 8.1 LLM Industry Chain Positioning

| Positioning | Our Choice | Rationale |
|------|---------|------|
| Upstream Dependency | GPU/Cloud platform selection | |
| Midstream Model | Closed-source API / Open-source model / Self-trained | |
| Downstream Application | AI Native / AI Copilot / AI Agent | |

### 8.2 Model Selection Trend Assessment

| Trend | Impact on Us | Response Strategy |
|------|------------|---------|
| Open-source model capabilities rapidly approaching closed-source | | |
| Small models (1B-8B) capabilities significantly improving | | |
| Multimodal becoming standard | | |
| MoE architecture becoming mainstream | | |
| Models as commodities | | |
| China model ecosystem maturing | | |

### 8.3 Model Supplier Strategy

| Strategy | Plan |
|------|------|
| Primary Supplier | |
| Backup Supplier | |
| Open-source Fallback | |
| Switching Cost Assessment | |
| Supplier Lock-in Risk Assessment | |

### 8.4 Compliance Selection Considerations

| Scenario | Recommended Model Approach | Compliance Basis |
|------|------------|---------|
| Domestic Government/Enterprise Clients | Domestic models (Qwen/DeepSeek) + Local Deployment | Data Localization |
| Overseas SaaS | Claude/GPT API + Open-source fallback | Global coverage |
| Privacy-sensitive Scenarios | On-device small models | Data never leaves device |
| High-compliance Industries (Finance/Healthcare) | Private Deployment + Audit | Industry regulation |