# AI Product Case Library / AI PM Case Library

> This directory contains complete cases of real AI product scenarios, showcasing the full chain from AI opportunity identification to commercial monetization.
> All cases are compiled from real materials such as public bidding announcements, official company reports, and industry case studies.

## Case List

| No. | Case Name | AI Product Type | Core Methodology |
|------|----------|-----------|-----------|
| C01 | Huatai Securities × Emotibot: Intelligent Customer Service Robot "Xiao Le" | NLP Conversational AI + Knowledge Graph | Multi-channel Access + FAQ Knowledge Base + Agent Assistance + RPA Digital Employees |
| C02 | Mininglamp Technology DeepMiner Agent Cluster Product | Agentic AI Platform | Model Selection + RaaS Commercialization + Multi-Agent Collaboration |
| C03 | CSC Financial: Full-Scenario Digital-Intelligent Integrated Customer Service Platform | Large Model + Specialized Small Model Fusion | Self-developed + Large Model Transformation + Knowledge Middle Platform + Full Process Intelligentization |

---

## Case C01: Huatai Securities × Emotibot — Intelligent Customer Service Robot "Xiao Le"

### Background

**Real Case Source**: Official public reports from Emotibot and public interviews with Ms. Wang Ling, Co-Head of the Information Technology Department at Huatai Securities. As a technology-driven comprehensive securities group, Huatai Securities has continuously invested in AI, big data, blockchain, cloud computing, and other fields, with R&D personnel accounting for over 20% and four major R&D bases in Nanjing, Shanghai, Beijing, and Shenzhen. Emotibot is an AI ecosystem partner of Huatai Securities, and the two parties have jointly completed a series of cutting-edge implementation projects including intelligent customer service robots, real-time agent assistants, and enterprise employee assistants.

**Core Data** (Source: Official Emotibot reports):
- Since going live, the intelligent customer service robot "Xiao Le" has cumulatively served **tens of millions of customers**, ranking among the top in securities apps
- Covering **over 10 domains** with **5,000+ FAQs**, multiple product knowledge graphs, and multi-turn conversation scenarios for high-frequency business
- Effective interception rate exceeds **70%**
- The real-time agent assistant serves customer service staff daily with a high effective knowledge recommendation rate
- Huatai Securities' ZhangLe Wealth Management APP had over 50 million users in 2023, with AI customer service handling an average of over 30,000 inquiries per day and a problem resolution rate of 92%

**Project Background**:
- Huatai Securities has a massive customer base, and customer service faced challenges such as high labor costs, uneven service quality, and insufficient response during peak hours
- Launched digital transformation in 2017, and took the lead in launching the digital transformation strategy in 2019
- In 2023, under the AI wave, exploration and application of large model technology began — not building foundational large models, but waiting for the application side to mature before leveraging third-party foundational large models for application scenario implementation

### AI Opportunity Identification

| Dimension | Assessment |
|------|------|
| **Business Value** | The securities industry has high customer inquiry volumes and a high proportion of standardized issues (product inquiries, transaction guidance, account management, secondary business processing, etc.). AI replaces manual handling of high-frequency standardized issues, freeing up human resources to focus on high-value services |
| **Technical Feasibility** | NLP intent recognition, knowledge graphs, and multi-turn conversation technologies are mature; Emotibot's three product lines — Bot Factory conversational AI platform, AICC+ solution platform, and Gemini knowledge engineering platform — form a complete technology stack |
| **Data Readiness** | Securities business SOPs are clear, and knowledge assets such as product documentation, trading rules, and compliance requirements are highly structured; 10+ domain FAQs and knowledge graphs have already been accumulated |
| **Compliance & Security** | The securities industry is strictly regulated, and customer service content requires compliance quality checks; intelligent quality inspection + real-time agent assistance meet compliance requirements |

**Decision**: Procure mature products + custom development, select Emotibot as AI ecosystem partner, with multi-phase project continuous iteration

### Technology Architecture (Reconstructed from Public Reports)

**Three-Platform Collaboration**:

| Platform | Positioning | Core Capabilities |
|------|------|----------|
| **Bot Factory** | Conversational AI Platform | Connects to Huatai CC system, WeChat Official Account, ZhangLe APP, official website, mini-programs and other channels; creates the intelligent customer service robot "Xiao Le"; supports FAQ + knowledge graph + multi-turn conversations |
| **AICC+** | Intelligent Customer Service Solution Platform | Intelligent agent assistance, process guidance, intelligent coaching, real-time quality inspection; intelligent outbound calls and IVR functions (TTS speech synthesis + ASR speech transcription + NLP intent recognition) |
| **Gemini** | Knowledge Engineering Platform | RPA digital employee full lifecycle management; automated knowledge graph construction; ticket fault tracing and business process optimization |

**Multi-Channel Unified Access Architecture**:
```
Customer Channel Layer: 400 Hotline / ZhangLe Wealth Management APP / WeChat Official Account / WeCom / Official Website / Mini-Programs
              ↓
        CC System Unified Routing
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
 Bot Factory  AICC+    Gemini
 (Intelligent Customer Service)   (Agent Assistance)  (Knowledge Engineering)
    ↓         ↓         ↓
  FAQ + Knowledge Graph   Real-time Quality Inspection   RPA Digital Employees
  Multi-turn Conversations    Intelligent Coaching   Knowledge Graph Construction
```

**Key Technical Features** (Based on Public Reports):
- Build an enterprise-grade service operating system centered on NLP technology
- Knowledge graph + standard Q&A dual-engine to enhance the intelligent knowledge base
- Human-machine hybrid service model: AI handles standardized issues, complex issues seamlessly transfer to human agents
- Structured processing of hundreds of business process-related knowledge documents
- Enables natural semantic search queries for data such as tickets, versions, and processes

### Intelligent Customer Service Core Capabilities

**"Xiao Le" Robot Capability Matrix**:

| Capability Dimension | Implementation | Performance Data |
|----------|----------|----------|
| FAQ Coverage | 10+ domains, 5,000+ FAQs | Effective interception rate >70% |
| Knowledge Graph | Multiple product knowledge graphs | Supports complex relational reasoning |
| Multi-turn Conversations | Multi-turn conversation scenarios for high-frequency business | Covers product inquiries, transaction guidance, account management, etc. |
| Multi-Channel Access | CC System / WeChat / APP / Official Website / Mini-Programs | Unified routing + unified knowledge base |
| Human-Machine Collaboration | Intelligent online consultation + intelligent outbound call follow-ups | 7×24 online service |

**Agent Assistance System** (AICC+ Platform):
- Real-time knowledge recommendation: Automatically pushes relevant knowledge entries based on conversation content
- Process guidance: Step prompts for complex business processes and compliance key point reminders
- Intelligent coaching: Simulated conversation training for new hire training scenarios
- Real-time quality inspection: Real-time detection of compliance risk points during calls
- Intelligent outbound calls: TTS + ASR + NLP enables human-machine interactive follow-ups, covering stock revitalization, business processing result notifications, MOT task notifications, etc.

### Evaluation System (Based on Public Reports + Industry Practice Inference)

| Metric | Public Data | Source |
|------|----------|------|
| Cumulative Customers Served | Tens of Millions | Emotibot Official Reports |
| FAQ Effective Interception Rate | >70% | Emotibot Official Reports |
| ZhangLe APP AI Customer Service Problem Resolution Rate | 92% | 21st Century Business Herald (July 2025) |
| AI Customer Service Average Daily Inquiry Volume | >30,000 times | Industry Analysis Report Citation |
| Agent Assistant Knowledge Recommendation Effectiveness Rate | "Very High" (specific value not disclosed) | Emotibot Official Reports |
| Customer Satisfaction | >92% (ZhangLe APP) | 21st Century Business Herald (July 2025) |

> ⚠️ Some specific metric values are indirect citations from public reports; precise measurement standards are subject to Huatai Securities' internal data.

### Project Evolution Roadmap (Inferred from Public Reports)

| Phase | Timeline | Milestone |
|------|------|--------|
| Phase 1 | ~2020-2021 | Bot Factory platform went live, created "Xiao Le" robot, covering core FAQs + knowledge graph |
| Phase 2 | ~2021-2022 | AICC+ platform went live, agent assistance + intelligent quality inspection + intelligent outbound calls implemented |
| Phase 3 | ~2022-2023 | Gemini platform went live, RPA digital employee full lifecycle management; promoted to HR/operations/custody departments and subsidiaries such as Huatai International |
| Phase 4 | 2023-Present | Large model technology exploration and application, comprehensive AI empowerment for intelligent customer service + investment banking + institutional business |

### Commercialization Analysis

**Cooperation Model**: Multi-phase project-based, with Emotibot as AI ecosystem partner continuously delivering and iterating

**Emotibot Product Line Commercialization Characteristics**:
- **High Degree of Productization**: Three standardized platforms — Bot Factory, AICC+, Gemini — can quickly adapt to different customers
- **Ecosystem Lock-in Depth**: From intelligent customer service → agent assistance → RPA digital employees → knowledge engineering, covering the full customer service chain with high replacement costs
- **Industry Replicability**: Securities industry benchmark case (Huatai) → replicable to banking, insurance, funds, and other financial sub-sectors

**Huatai Securities AI Investment Characteristics** (Source: 21st Century Business Herald):
- R&D personnel account for over 20%, with four major R&D bases
- 2024 technology investment exceeded 1 billion RMB (top tier in the industry)
- Strategy: "Do not build foundational large models; wait for the application side to mature, then leverage third-party foundational large models for application scenario implementation"

### Lessons Learned

1. **"Mature Products + Deep Customization" is an effective path for financial AI implementation**: Huatai did not choose to self-develop a conversational AI platform, but instead deeply cooperated with Emotibot, with the former focusing on business scenarios and the latter providing the technology platform
2. **Knowledge graphs are an upgrade from FAQs**: 5,000+ FAQs solve high-frequency standardized issues, while knowledge graphs solve complex relational reasoning problems; the two complement each other to form a complete knowledge system
3. **Agent assistance is an AI value amplifier**: AI not only replaces human labor (interception rate >70%) but also empowers human labor (real-time knowledge recommendation, process guidance), improving overall service efficiency through a dual approach
4. **Multi-channel unified access is a differentiated competitive advantage**: CC system / WeChat / APP / official website / mini-programs unified routing + unified knowledge base, avoiding channel fragmentation
5. **From single-point intelligence to full-chain intelligence**: From customer service robots → agent assistance → RPA digital employees → knowledge engineering, gradually covering the full customer service chain
6. **Large models are an incremental overlay rather than a disruptive replacement**: Huatai's strategy of "not building foundational large models, but leveraging third parties once the application side matures" reflects a pragmatic AI implementation philosophy

---

## Case C02: Mininglamp Technology DeepMiner Agent Cluster Product

### Background

**Real Case Source**: Mininglamp Technology (02718.HK) 2025 annual report and public reports. Mininglamp Technology strategically transformed from data intelligence to agentic services, self-developing the enterprise-grade AI agent platform DeepMiner, achieving the leap from "helping customers understand data" to "helping customers get results."

**Core Data** (Source: 2025 Annual Report):
- 2025 revenue of 1.426 billion RMB, gross profit of 790 million RMB (55.4% gross margin), adjusted net profit of 42.04 million RMB (turning losses into profits)
- Agentic Services first-year revenue exceeded 100 million RMB, with 30%+ of new major clients coming from this segment
- Major client renewal rate of 96%, serving approximately 2,100 well-known brands + 240,000 enterprise users
- 100% of all employees onboarded to the DeepMiner platform

**Technical Milestones** (Source: Public Reports):
- Mano model: 2nd globally on the OSWorld leaderboard (behind Anthropic), 1st on the Mind2Web leaderboard
- Cito model: Ranked 1st in the BFCL small-size model category
- DeepMiner V2 adopts a "Dispatch—Decision—Execution" multi-agent layered collaboration architecture

### AI Opportunity Identification

| Dimension | Assessment |
|------|------|
| **Business Value** | Shift from tool delivery to result delivery (RaaS), where customers pay for quantifiable business results (marketing ROI improvement, doubled content output efficiency) |
| **Technical Feasibility** | Self-developed Mano + Cito dual-model system, with OSWorld/Mind2Web/BFCL three major leaderboards verifying the technical moat |
| **Data Readiness** | Long-term accumulation of massive marketing data, customer scenario understanding, and industry know-how forms a data moat |
| **Market Timing** | Enterprise AI demand shifting from "using AI tools" to "AI directly producing results," opening the market window for Agentic AI |

**Decision**: Build (self-developed platform), using DeepMiner as the unified infrastructure to drive agent-based transformation across all business lines

### Model Selection Decision

**Self-Developed Dual-Model System**:

| Model | Positioning | Core Capabilities | Leaderboard Performance |
|------|------|----------|----------|
| **Mano** | Execution Model (GUI-VLA) | Visual understanding + interface operation, autonomously completing complex software interaction tasks | OSWorld global 2nd (behind Anthropic), Mind2Web 1st |
| **Cito** | Reasoning Model | Task planning, logical reasoning, decision-making | BFCL 1st in small-size model category |

**Selection Logic**:
- The "Dispatch—Decision—Execution" three-layer architecture naturally requires dual engines for reasoning + execution
- Open-sourced Mano-P 1.0 (April 2026), achieving SOTA on 13 authoritative leaderboards, building a developer ecosystem
- Small-size model strategy reduces inference costs, adapting to enterprise-grade large-scale deployment needs

### DeepMiner Platform Architecture (Source: Annual Report + Public Reports)

**Three-Layer Collaboration Architecture**:

```
User Intent → Foundation Agent (Dispatch Layer)
              ├── Cito (Decision Layer): Task Understanding → Path Planning → Tool Selection
              └── Mano (Execution Layer): GUI Operation → Data Acquisition → Result Output
              
Multi-Agent Collaboration: Data Insight Agent × Content Production Agent × Marketing Placement Agent × Analysis Report Agent
```

**Key Platform Capabilities** (Source: Annual Report Disclosure):
- Marketing Intelligence: Delivery efficiency improved up to 4x
- Operational Intelligence: Single ticket resolution time reduced by 30%+
- Miaozhen Systems: Full-chain AI auto-completion rate of 90%, deep review report efficiency improved 20x
- Employee self-service Agent creation: 100% employee onboarding, can independently create dedicated business Agents based on business scenarios

### RaaS Commercialization Model (Result as a Service)

**Model Definition** (Source: Annual Report): Agentic Services no longer stays at tool output or single-point capability delivery, but provides end-to-end result delivery services oriented toward customers' quantifiable business objectives.

| Dimension | Traditional SaaS | RaaS (Agentic Services) |
|------|----------|--------------------------|
| **Deliverable** | Software Features/Tools | Quantifiable Business Results |
| **Pricing Logic** | Per Seat/Usage | Pay-for-Performance |
| **Customer Decision** | "Is this tool easy to use?" | "How much did ROI improve?" |
| **Marginal Cost** | Fixed (Human Delivery) | Decreasing (AI-Driven Automation) |
| **Competitive Moat** | Feature Comparison | Result Commitment + Data Flywheel |

**Commercialization Results** (Source: 2025 Annual Report):
- Agentic Services first-year revenue exceeded 100 million RMB
- Marketing scenarios: Nearly 3x operational efficiency achieving an average 20% marketing effectiveness increase
- 30%+ of new major clients from the Agentic Services segment
- Major client renewal rate of 96%

### Engineering Practice of a 5-Person Team with 370,000 Lines of Code (Source: Public Reports)

> ⚠️ Specific engineering practice details are inferred based on industry practice.

**Core Insights**:

| Dimension | Practice (Inferred from Industry Practice) |
|------|------|
| **AI-Assisted Coding Rate** | Estimated 85%+ of code generated by AI, with humans focusing on architecture design + code review + testing |
| **Development Paradigm** | Prompt-driven Development: Requirements → Prompt → AI Generation → Review → Merge |
| **Quality Assurance** | 100% human review of AI-generated code + automated test coverage |
| **Team Structure** | 5 people = 1 architect + 3 full-stack (AI-assisted) + 1 QA (AI-assisted testing) |

**Key Insight**: The essence of 370,000 lines of code / 5-person team is not a subversion of the "Mythical Man-Month," but a fundamental shift in development paradigm from "humans writing code" to "humans reviewing code" (inferred from industry practice).

### Evaluation System (Source: Annual Report + Public Reports + Industry Practice Inference)

**Model-Layer Evaluation**:

| Metric | Target/Performance | Evaluation Benchmark |
|------|----------|----------|
| GUI Operation Capability | Global 2nd | OSWorld |
| Web Navigation Capability | Global 1st | Mind2Web |
| Function Calling Capability | 1st in Small-Size | BFCL |
| Open-Source Model General Capability | 13 SOTAs | Mano-P 1.0 Public Leaderboards |

**Business-Layer Evaluation** (Source: Annual Report):

| Metric | Performance | Measurement Method |
|------|------|----------|
| Marketing Effectiveness Improvement | Average +20% | Customer A/B Testing |
| Operational Efficiency Improvement | Nearly 3x | Delivery Cycle Comparison |
| Delivery Efficiency Improvement | Up to 4x | Marketing Intelligence Business Line |
| Ticket Resolution Time | Reduced by 30%+ | Operational Intelligence Business Line |
| AI Auto-Completion Rate | 90% | Miaozhen Systems Full Chain |

### Lessons Learned

1. **RaaS is the ultimate form of AI commercialization**: Customers don't pay for tools, they pay for results. First-year revenue exceeding 100 million verified the market's real demand for this model
2. **Self-developed models are the moat**: The rankings of the Mano + Cito dual-model system on three major leaderboards constitute a technical barrier that competitors cannot easily cross in the short term
3. **Use it internally first**: 100% employee onboarding to DeepMiner, employees independently creating Agents — "eating your own dog food" is the most honest PMF verification
4. **The secret of 96% renewal rate**: When AI services are embedded in customers' core business flows and deliver quantifiable results, replacement costs are extremely high, and renewals happen naturally
5. **Small team + AI leverage**: 5 people and 370,000 lines of code prove that in the AI era, team size is no longer the ceiling for output; the key is architecture design + AI collaboration capability
6. **Open source is an ecosystem strategy**: Mano-P 1.0 open source (13 SOTAs) is not charity — it's building a developer ecosystem and lowering customer adoption barriers

---

## Case C03: CSC Financial — Full-Scenario Digital-Intelligent Integrated Customer Service Platform

### Background

**Real Case Source**: Case study released by FintechInChina in June 2025, and public information from CSC Financial. As a leading securities firm (with over 10 million securities brokerage customers), CSC Financial faced the dual challenge of a massive customer base and insufficient customer service capacity. Led by the information department's self-development, it built a full-scenario digital-intelligent integrated customer service platform, reconstructing the customer service system based on large model technology.

**Core Data** (Source: FintechInChina Case Study):
- Customer service hotline (4008-888-108) average daily call volume grew from 500 calls in 2019 to 2,000 calls in 2024, with a single-day peak of 15,000 calls in October 2024
- Customer follow-up call volume (95587) grew from an average of 8,500 calls per day in 2019 to 23,000 calls per day in 2024, with a single-day maximum outbound call volume of 55,000 calls
- Intelligent quality inspection coverage increased from 3% to 100%, with 60,000 calls fully inspected weekly, replacing 95% of manual quality inspection
- The agent assistance system has cumulatively provided 455,000 assists to human customer service agents and 3.91 million assists to follow-up personnel
- Average call handling time optimized from 9.74 minutes to 8.51 minutes
- Customer satisfaction improved from 97.62% to 98.81%
- A total of 12 papers published, 3 national invention patents obtained, 9 software copyrights, and 11 industry awards

**Project History** (Source: FintechInChina Case Study):
- 2019: Implemented intelligent outbound call and intelligent quality inspection systems
- 2020: Implemented intelligent phone customer service system
- 2021: Implemented intelligent voice platform
- 2022: Implemented employee empowerment platform and agent assistance system (introducing Recurrent AI), built an employee knowledge base based on knowledge graphs
- 2023-2025: Entered the "All in AI" phase, carrying out full-line large model transformation of existing customer service systems

### AI Opportunity Identification

| Dimension | Assessment |
|------|------|
| **Business Value** | Securities customer service faces the dual challenge of "massive customer base + insufficient service capacity." AI replaces standardized services (average 2,000 incoming calls/day), empowers complex services (agent assistance), achieving cost reduction and efficiency improvement |
| **Technical Feasibility** | From 2019-2022, a complete infrastructure of intelligent outbound calls + intelligent customer service + intelligent voice + agent assistance + intelligent quality inspection was already built, providing a solid foundation for the large model transformation starting in 2023 |
| **Data Readiness** | Years of accumulated full call data, customer service tickets, and knowledge base documents; already built a 100,000+ intelligent customer service scenario fine-tuning dataset |
| **Market Timing** | Large model technology matured from 2023 onward, providing a generational leap opportunity for the intelligent upgrade of existing customer service systems |

**Decision**: Primarily self-developed + ecosystem cooperation (Recurrent AI providing agent assistance system), phased construction, infrastructure first then large model transformation

### Technology Architecture (Source: FintechInChina Case Study)

**"Large Model + Specialized Small Model" Fusion Architecture**:

```
┌─────────────────────────────────────────────────┐
│              Large Model Core Decision & Dispatch Layer                │
│  ┌─────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Tongyi Qianwen │  │   Kimi   │  │  DeepSeek     │  │
│  └─────────┘  └──────────┘  └───────────────┘  │
│         Multiple Base Model Selection and Deployment                     │
├─────────────────────────────────────────────────┤
│              Specialized Small Model Layer                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │Speech Recognition │ │Intent Extraction │ │Knowledge Base  │ │Intelligent Quality Inspection│ │
│  └─────────┘ └─────────┘ └─────────┘ └───────┘ │
├─────────────────────────────────────────────────┤
│              Intelligent Knowledge Middle Platform                          │
│  Knowledge Graph + LLM Generalization + ES Optimization + Vector Knowledge Base + Re-ranking  │
├─────────────────────────────────────────────────┤
│              Application Layer                               │
│  Intelligent Customer Service │ Intelligent Outbound Calls │ Agent Assistance │ Intelligent Quality Inspection │ WeCom Group Bot │
│  Intelligent Coaching │ Conversation Summary │ Intelligent Tickets │ Customer Profile │ Announcement Extraction   │
└─────────────────────────────────────────────────┘
```

**Key Technical Decisions** (Source: FintechInChina Case Study):

| Technical Dimension | Specific Solution |
|----------|----------|
| Base Model | Multiple base models including Tongyi Qianwen, Kimi, DeepSeek, deployed according to scenario |
| Fine-tuning Strategy | Built 100,000+ intelligent customer service scenario dataset, accumulated full fine-tuning, LoRA, P-Tuning and other efficient fine-tuning techniques |
| Fine-tuning Effect | Intelligent customer service scenario fine-tuning accuracy improved to over 90% |
| Knowledge Middle Platform | Knowledge graph + LLM generalization + ES optimization (multi-field fuzzy query/filters/field weights) + vector knowledge base + re-ranking |
| Agent Capabilities | Encapsulated general Agent capabilities such as search agent, web agent, supporting scenario Agents for intelligent quality inspection/intelligent investment advisory/multimodal customer service/intelligent search |
| WeCom Group Bot | Multi-format text parsing + automatic document chunking + large model query generalization + ES recall + RAG Q&A + intent classification + entity extraction + SQL completion |

### Full Process Intelligentization Service Model

**"Pre-Event → In-Event → Post-Event" Three-Stage Empowerment**:

| Stage | Intelligentization Capability | Large Model Upgrade |
|------|-----------|-----------|
| **Pre-Event (Wisdom)** | Customer profile generation, intelligent outbound call strategy optimization | Large model integrates multi-dimensional customer information to generate precise profiles; extracts call script templates from excellent outbound call recordings |
| **In-Event (Smart Assistance)** | Intelligent customer service auto-response, agent assistance real-time recommendation | FAQ automated expansion; large model predicts customer follow-up needs, providing precise suggestions to agents |
| **Post-Event (Smart Learning)** | Intelligent quality inspection full coverage, conversation analysis optimization | Large model comprehensively analyzes call content, extracts excellent scripts, identifies hot topics, optimizes service processes |

### Cost Reduction and Efficiency Improvement Quantified Results (Source: FintechInChina Case Study)

| Intelligent Assistant | Quantified Effect | Human Replacement |
|----------|----------|----------|
| Intelligent Outbound Call Robot | Completes ~4.4 million calls annually | Saves ~103 person-days/workday |
| Intelligent Customer Service Robot | Handles 2,000 incoming calls daily | Saves ~33 person-days/workday |
| Large Model Conversation Summary Assistant | Full review of all intelligent phone customer service recordings | Saves ~20 person-days/workday |
| Listed Company Announcement Extraction Assistant | Produces 50 effective information items daily | Saves 5h/day |
| Message Group Push Intelligent Assistant | Scheduled stock market calendar/exchange announcements/financing announcement pushes | Replaces 7h/day |
| Agent Assistance Module | Conversation summary/ticket routing/speech-to-text/information integration | Full chain saves 283h/day (~35 person-days) |
| Intelligent Quality Inspection Module | Quality inspection coverage 3%→100%, replaces 95% manual | Replaces 990h/day (~124 person-days) |

### Evaluation System (Source: FintechInChina Case Study + Industry Practice Inference)

| Metric | Data | Measurement Method |
|------|------|----------|
| Intelligent Customer Service Scenario Fine-tuning Accuracy | >90% | 100,000+ test set evaluation |
| Speech Recognition Accuracy | >90% (as of end of 2022) | System automated evaluation |
| Quality Inspection Coverage | 3%→100% | Full machine quality inspection |
| Manual Quality Inspection Replacement Rate | 95% | Machine quality inspection replacing manual |
| Average Call Handling Time | 9.74→8.51 min (-12.6%) | System statistics |
| Customer Satisfaction | 97.62%→98.81% | Customer evaluation |
| AI-Managed Agent Work Ratio | 25% (as of end of 2022) | System statistics |

### Lessons Learned

1. **"Infrastructure first, then large model transformation" is a pragmatic path**: From 2019-2022, built complete infrastructure for intelligent outbound calls/customer service/voice/quality inspection/agent assistance, only then began large model transformation from 2023, avoiding "looking for nails with a hammer"
2. **"Large model + specialized small model" fusion architecture is the best practice for financial AI**: Large models handle decision dispatch and complex reasoning, specialized small models handle deterministic tasks like speech recognition/intent extraction, balancing capability and cost
3. **Primarily self-developed + ecosystem cooperation as supplement**: Core platform self-developed (by information department), agent assistance and other modules introduced via ecosystem partners (Recurrent AI), balancing autonomous control and rapid implementation
4. **Knowledge middle platform is the soul of intelligent customer service**: The comprehensive search solution of knowledge graph + LLM generalization + ES + vector database + re-ranking is key to upgrading intelligent customer service from "FAQ matching" to "semantic understanding"
5. **Quantify the value of every AI investment**: From person-days saved to satisfaction improvement, CSC Financial has precise input-output quantification for every intelligent module — this is a required skill for AI PMs
6. **Intelligent quality inspection is a rigid need for financial compliance**: The leap in quality inspection coverage from 3% to 100% not only reduces costs (replacing 95% manual), but is a qualitative change in risk prevention and control

---

## Source Attribution

### Case C01 Sources
- Emotibot Brings Advanced Intelligent Customer Service Technology to Help Huatai Securities Leap Forward, Sohu/China Shandong Network, January 2022, https://www.sohu.com/a/516846952_114775
- Emotibot Joins Hands with Huatai Securities to Serve Tens of Millions of Customers with New Intelligent Customer Service Robot, Qudong/Ifeng, January 2022, https://news.qudong.com/article/788999.shtml
- How AI+ is Reshaping the Securities Industry Ecosystem? Taking Leading Securities Firm Huatai Securities as an Example to See Technological Change, 21st Century Business Herald, July 25, 2025, https://m.21jingji.com/article/20250725/herald/f71512b3f89309847f14c1fd1aba9bff.html
- Content marked "inferred from industry practice" (specific evaluation system parameters, project evolution timeline, etc.) represents reasonable inferences by the author based on public reports combined with common industry practices

### Case C02 Sources
- Mininglamp Technology 2025 Annual Performance Announcement, March 26, 2026, Hong Kong Stock Exchange
- Mininglamp Technology 2025 Annual Report Analysis and Interpretation, Xueqiu, https://xueqiu.com/8781923796/382333321
- Mininglamp Technology Releases 2025 Fiscal Year Performance: Fully Entering the AI-Native Operations Era, Baijiahao/Hexun Finance, March 27, 2026, https://baijiahao.baidu.com/s?id=1860785928772510097
- Mininglamp Technology-W (02718.HK): After Annual Report Turns Profitable, Agentic AI Begins to Realize Revenue, East Money, April 29, 2026, https://caifuhao.eastmoney.com/news/1701299003
- Content marked "inferred from industry practice" (5-person team engineering practice details, specific development paradigms, etc.) represents reasonable inferences by the author based on public data combined with common industry practices

### Case C03 Sources
- CSC Financial: Full-Scenario Digital-Intelligent Integrated Customer Service Platform Based on Digital Finance, FintechInChina, June 2025, https://www.fintechinchina.com/cases/8429
- Recurrent AI Wins Bid with CSC Financial to Jointly Build Intelligent Agent Assistance System, Recurrent AI Official Website, November 2022, https://www.rcrai.com/about-us/news/company/data_165.html
- CSC Financial Intelligent Customer Service Platform, Zhiding, April 2026, https://m.zhiding.cn/article/3154543.htm
- Content marked "inferred from industry practice" (specific measurement standards for some evaluation metrics, etc.) represents reasonable inferences by the author based on public case studies combined with common industry practices

---

> **Disclaimer**: The cases in this document are compiled from public information and are for AI product management learning reference only. Content marked "inferred from industry practice" does not represent the actual technical proposals or internal decisions of the relevant enterprises. All factual data is subject to the original public reports, bidding announcements, and official company disclosures.