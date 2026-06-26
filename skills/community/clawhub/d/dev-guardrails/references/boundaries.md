# Capability Boundaries — 能力边界参考

This reference defines what an individual developer + AI agent combination can and cannot realistically deliver. Use it when deciding whether to accept, modify, or refuse a development request.

---

## ✅ Within Capability (3-6 months, solo + AI)

### Tier 1: Lightweight Enterprise Applications

| Project Type | Example Scope | Key Constraints |
|-------------|---------------|-----------------|
| Lightweight IM + Collaboration | Slack/企业微信精简版 | <10k concurrent users, text + basic file sharing |
| Regional E-commerce (Full Stack) | Shopify/有赞完整版 | Single region, <100k SKUs, standard payment gateway |
| Enterprise RAG + AI Assistant | Notion AI + 飞书智能助手 | Private deployment, <1TB document corpus |
| Low-Code Platform (Lite) | Simple Mendix/OutSystems | Form builder + workflow engine, no custom DSL |
| In-Vehicle Infotainment Stack | Tesla infotainment (stripped) | Media, nav, settings, voice — no ADAS integration |
| Quant Trading Platform (Full Stack) | TradingView + 聚宽精简版 | Single market, backtesting + live, no HFT |

### Tier 2: Specialized Tools & Platforms

| Project Type | Example Scope | Key Constraints |
|-------------|---------------|-----------------|
| Private Cloud Drive | OwnCloud/NextCloud lite | Single tenant, <100TB |
| Vertical Community Platform | Stack Overflow for X domain | Q&A + reputation + moderation |
| IoT Management Backend | Device registry + telemetry + rules | <10k devices |
| CI/CD Pipeline + Dashboard | Jenkins lite + custom UI | Standard build/test/deploy |
| Content Management System | Headless CMS for specific domain | RESTful/GraphQL API + admin UI |
| Real-Time Dashboard | Grafana lite for specific data source | WebSocket + charting, <100 metrics |

### Tier 3: Libraries & Frameworks

| Project Type | Example Scope | Key Constraints |
|-------------|---------------|-----------------|
| Domain-Specific SDK | Payment SDK for specific gateway | Single gateway integration |
| UI Component Library | 20-50 components with theming | React/Vue/Web Components |
| Data Processing Pipeline | ETL framework for specific format | Single data source type |
| Testing Framework Extension | Custom assertions + reporters | Extends existing framework |
| CLI Tool Suite | Dev workflow automation | <20 commands |

---

## ❌ Red Lines (Absolutely Cannot Deliver)

Refuse immediately. Do not negotiate. The technical reasons below are non-negotiable.

### 1. Nation-Scale Consumer Products

| Request | Why Impossible |
|---------|---------------|
| 完整版微信 / WeChat Clone | 1000+ engineer team, distributed database sharding, CDN + edge computing, regulatory compliance (ICP, real-name verification, content moderation) |
| 原版12306 / Railway Ticketing | Billion-level concurrent ticket queries, distributed inventory with ACID, seat allocation algorithm, national railway data integration |
| 抖音 / Douyin Clone | Video transcoding pipeline at petabyte scale, recommendation algorithm training on billion-user data, CDN edge caching across continents |
| 淘宝 / Taobao Clone | Multi-tenant marketplace, payment settlement, logistics integration, fraud detection, seller ecosystem |
| 美团 / Meituan Clone | Real-time location services, rider dispatch algorithm, merchant onboarding + verification, payment + settlement |

### 2. Foundational Infrastructure Software

| Request | Why Impossible |
|---------|---------------|
| 自研数据库内核 | Storage engine, query optimizer, transaction manager, replication — each is a PhD-level team project |
| 操作系统 | Kernel, driver model, memory management, process scheduler — Linux took 30 years and thousands of contributors |
| 大型分布式中间件 | Consensus algorithms (Raft/Paxos), partition tolerance, exactly-once semantics — requires distributed systems expertise |
| 3A游戏引擎 | Rendering pipeline, physics engine, asset pipeline, editor tooling — Unreal Engine has 200+ full-time engineers |
| 编程语言编译器 | Lexer, parser, type checker, code generator, standard library — Rust took 10+ years of community effort |

### 3. Compliance-Heavy Systems

| Request | Why Impossible |
|---------|---------------|
| 持牌支付系统 | Requires payment business license from PBOC, PCI-DSS compliance, anti-money laundering (AML) systems |
| 全国医疗挂号平台 | HIPAA/data privacy compliance, hospital system integration (HL7/FHIR), government healthcare data access |
| 网约车平台 | Transportation network company license, real-time background checks, insurance integration, regional regulations |
| 银行核心系统 | Banking license, regulatory reporting (BASEL), core banking system integration, audit trail requirements |

### 4. AI Systems at Scale

| Request | Why Impossible |
|---------|---------------|
| 通用大模型训练 | Requires thousands of GPUs, months of training time, curated petabyte-scale datasets, RLHF pipeline |
| AI内容风控集群 | Real-time inference at million-QPS, multi-modal content analysis, regulatory compliance, continuous model updates |
| 自动驾驶 Full Self-Driving | Sensor fusion (camera/lidar/radar), real-time path planning, safety certification (ISO 26262 ASIL-D), billions of miles of validation |

### 5. Complex Hardware + Software Integration

| Request | Why Impossible |
|---------|---------------|
| 智能手机整机 | Hardware design (PCB, antenna, thermal), Android/iOS porting, carrier certification, supply chain |
| 智能汽车整车 | Vehicle dynamics, safety systems, CAN bus integration, homologation, crash testing |
| 工业机器人 | Motor control, kinematics, safety interlocks, industrial certifications |

---

## ⚠️ Gray Zone (Feasible with Constraints)

These are achievable but require explicit scope negotiation:

| Request | Feasible Scope | Must Negotiate |
|---------|---------------|----------------|
| 视频会议系统 | WebRTC-based, <50 participants, no recording/transcription | Confirm scale, features, infrastructure |
| 游戏 (非3A) | 2D or simple 3D, single-platform, <10 hours content | Genre, art pipeline, platform targets |
| 微服务架构改造 | Gradual migration, <20 services | Existing codebase quality, team capacity |
| 数据中台 | Specific domain, <100 data sources | Data schema complexity, governance requirements |
| 实时协作编辑 | OT/CRDT-based, <10 concurrent editors per doc | Conflict resolution strategy, offline support |

---

## Decision Protocol

When encountering a borderline request:

1. **Classify** it against this reference (Within / Gray / Red Line)
2. **If Red Line**: Hard stop. Use L4 response from SKILL.md
3. **If Gray Zone**: Acknowledge feasibility, then negotiate scope:
   - "I can build X if we limit scope to Y and Z. Does that work?"
   - "Version 1 can include A, B, C. D and E would require team expansion. Agree?"
4. **If Within**: Proceed with Principle 5 (confirm approach before building)
