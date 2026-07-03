
## 11-Stage Complete Product Lifecycle

> Each stage follows a unified structure: **Inputs → Core Process → Methodology → Outputs → Quality Standards → AI Acceleration**

---

### Stage 1: Strategy & Market Insight

**Role Hat: Industry Insight Scout**

#### Inputs
- Corporate strategic planning / executive intent
- Industry reports / financial reports / brokerage research reports
- Initial market awareness

#### Core Process (6-Step Cycle)

```
Market Scan → Competitive Landscape Analysis → Track Opportunity Identification → Product Positioning → Business Model Design → Roadmap Planning
   ↑                                                              ↓
   └──────────────── Quarterly Review Update ─────────────────────────────────────┘
```

#### Methodology Toolbox (8+1)

| Method | Purpose | When to Use | Output |
|------|------|--------|--------|
| **PESTLE Analysis** | Macro environment scanning | New market entry, annual strategy | One-page macro environment assessment |
| **Porter's Five Forces** | Industry competitive structure | Competitive landscape unclear | Five forces scoring radar chart |
| **SWOT Analysis** | Internal capabilities + external environment | Quarterly/annual strategy review | SWOT matrix → Strategy conversion |
| **Business Model Canvas (BMC)** | Business logic visualization | New product initiation | 9-module canvas |
| **Lean Canvas** | Rapid validation of business hypotheses | 0-1 stage | Problem-Solution-Customer-Channel-Revenue |
| **Value Proposition Canvas** | Product-customer fit | Positioning unclear | Customer profile + Value map |
| **Ansoff Matrix** | Growth direction selection | Annual planning | 4-quadrant growth strategy |
| **BCG Matrix** | Product portfolio management | Multi-product lines | Stars/Cash Cows/Question Marks/Dogs |
| **Technology Hype Cycle** | Technology adoption timing | AI / new technology planning | Technology introduction timing recommendations |

#### B2B-Specific Dimensions of Market Insight

```
B2B Market Signal Collection Channels:
├── Bidding websites (Government Procurement Network / Bid Radar) — most authentic demand signals
├── Gartner/Forrester/IDC Magic Quadrants and reports
├── Competitor job postings (reverse-engineer tech stack/business direction/team size)
├── Public company financial reports/prospectuses (market size, growth rate, customer count)
├── Industry conference presentation PPTs (product direction, technical architecture)
├── Customer purchasing behavior (RFQ/RFP/bidding budget)
├── Regulatory policy changes (biggest driver for compliance products)
└── Investment institution industry research reports (industry chain analysis, market sizing)
```

#### Outputs

1. **Industry Analysis Report** (15-25 page PPT, use `pptx-2`)
2. **Competitive Analysis Report** (detailed template: `references/templates/competitive-analysis-b2b.md`)
3. **Product Strategy One-Pager** (A4, can clearly explain product positioning in 3 minutes)
4. **Product Roadmap** (Now/Next/Later three-horizon format, draw.io Gantt chart)

#### AI Acceleration
- Use Claude for competitive feature matrix comparison (paste competitor help documentation)
- Use AI to analyze competitor pricing pages → generate pricing comparison table
- Search competitor job postings → AI reverse-engineers tech stack and team size
- Have AI generate SWOT strategy recommendations (SO/WO/ST/WT strategies)

---

### Stage 2: Requirement Discovery & Management

**Role Hat: Requirement Detective**

> The most core capability of a B2B product manager is not "writing PRDs," but "digging out the real requirements."
> 80% of what users say are solutions, not the actual requirements.

#### Inputs
- Customer feedback (tickets/NPS/customer service records/CSM feedback)
- Sales feedback (loss reasons/customer demands/competitor comparisons)
- Implementation & delivery feedback (go-live resistance/data migration blockers)
- Product usage data (feature adoption rate/abnormal behavior/churn funnel)

#### B2B Requirement Source Panorama

| Source | Acquisition Method | Signal Strength | Priority Judgment |
|------|----------|---------|-----------|
| **KA Customer Paid Customization** | Business negotiation/SOW agreement | ⭐⭐⭐⭐⭐ | Highest (has clear budget) |
| **Sales Loss Analysis** | CRM records/sales interviews | ⭐⭐⭐⭐ | High (affects deal closure) |
| **CSM Renewal Risk** | Customer health/renewal prediction | ⭐⭐⭐⭐ | High (affects NRR) |
| **User High-Frequency Tickets** | Customer service system/NPS comments | ⭐⭐⭐ | Medium-High |
| **Product Usage Data** | Product analytics tools | ⭐⭐⭐ | Medium |
| **Competitor Feature Comparison** | Competitive analysis reports | ⭐⭐⭐ | Medium |
| **Industry/Regulatory Changes** | Regulation updates/compliance requirements | ⭐⭐⭐ | Medium (but can suddenly spike) |
| **Internal Strategic Planning** | Executive intent | ⭐⭐ | Medium-Low (long-term reserve) |

#### Deep Requirement Discovery Methods

##### JTBD (Jobs To Be Done) — B2B Adapted Version

```
┌─────────────────────────────────────────────────────────┐
│ When [a specific role in the organization]_               │
│ I want to [complete a specific business task]_            │
│ So that [achieve business metric / meet KPI / pass audit / avoid fine]_     │
│                                                         │
│ Current pain: [How painful is the current way of completing this task? Quantify]              │
│ Importance: [How much weight does this task have in the user's KPIs?]                   │
│ Frequency: [How often is it done?]                                 │
└─────────────────────────────────────────────────────────┘

B2B JTBD Examples:
- Finance Manager: Complete consolidated financial statements for 3 subsidiaries within 3 days at month-end, ensuring zero audit issues
- IT Administrator: Batch-create 200 employee accounts and assign roles, ensuring least-privilege principle, meeting information security classification requirements
- Procurement Manager: Compare quotes from 3 suppliers → complete approval → generate purchase order, ensuring compliance with group procurement policies
- Legal: Auto-remind relevant departments 30 days before contract expiration to renew or terminate, avoiding compliance risks
```

##### SPIN Requirement Discovery Method (Specifically for B2B Consultative Interviews)

| Question Type | Purpose | B2B Example |
|---------|------|---------|
| **S - Situation** | Understand existing process | "How does the current monthly reconciliation process run? Which roles are involved?" |
| **P - Problem** | Amplify the pain point | "What's the error rate of manual reconciliation? How much loss does one audit issue cause?" |
| **I - Implication** | Quantify the consequence chain | "If this issue is exposed during an IPO audit, what impact would it have on the company?" |
| **N - Need-Payoff** | Stimulate action | "If reconciliation efficiency improves by 80%, how much of your team's energy could be freed up for financial analysis?" |

##### 5 Whys

```
User: "I need a batch import feature"
First Why: Why do you need batch import?    → "Need to import hundreds of records at a time"
Second Why: Why so many records?            → "Exported from ERP monthly and manually entered"
Third Why: Why not integrate directly?      → "IT says ERP is too old, no API"
Fourth Why: Does ERP have an upgrade plan?  → "Planned for next year but uncertain"
Fifth Why: What to do before the upgrade?   → "Temporary solution: export Excel monthly"
→ Conclusion: Short-term batch import is a reasonable transition plan, but must plan API integration
   to eliminate the root cause. If only doing import without planning integration, same problem in a year.
```

#### Requirement Management 4-Level Maturity

| Level | Characteristics | Identification Method |
|------|------|---------|
| **L1: Do Whatever They Say** | Do whatever users say | Backlog is full of "user wants to add XX feature" |
| **L2: Selective Execution** | PM has preset answers | PM is always persuading others during requirement reviews |
| **L3: Dig for Root Cause** | Distinguish requirements vs solutions, equal dialogue | PM asks "why" as often as "how" |
| **L4: Balance Interests** | Identify departmental interests, balance multi-party demands | PM can name which department is pushing each requirement |

#### Outputs

1. **User Persona Cards** (B2B multi-role version, one page per role)
2. **User Journey Map** (B2B version: Awareness → Evaluation → Purchase → Implementation → Usage → Renewal)
3. **JTBD Cards** (Jobs To Be Done for each user type)
4. **Requirement Backlog Excel** (standard fields: ID/Source/Description/Role/Scenario/Priority/Status/KANO Classification)
5. **User Interview Records** (template: `references/templates/user-interview-b2b.md`)

#### AI Acceleration
- Use AI to analyze customer service ticket text → auto-cluster common issue types
- Use AI to generate interview guides (based on known customer information and industry)
- Interview recording transcription → AI summarizes key findings
- Multiple interview records → AI identifies cross-interview common issues

---

### Stage 3: Requirement Analysis & Prioritization

**Role Hat: Solution Architect + Requirement Detective**

#### Inputs
- Requirement backlog (Stage 2 output)
- Product roadmap (Stage 1 output)
- Technical resource constraints
- Current quarter OKR

#### Methodology

##### KANO Model — B2B Specialized Version

| Requirement Type | B2B Characteristics | Typical Examples | Strategy |
|---------|---------|---------|------|
| **Must-Be / Basic** | Product unusable without it, no bonus for having it | Login/Permissions/Audit Logs/Data CRUD | Achieve 80 points, no weak spots |
| **Performance / Satisfiers** | More is better, linear relationship | Batch operations/Import-Export/Reports/Mobile | Continuously improve, benchmark competitors |
| **Delighters / Excitement** | Delightful to have, fine without | AI smart recommendations/Automated workflows/Voice interaction | Differentiation highlights, 1-2 is enough |
| **Indifferent** | No feeling whether it's there or not | Over-designed aesthetics/Niche formats | **Cut decisively** |
| **Reverse** | Actually worse with it | Excessive popup notifications/Forced operation steps | **Remove immediately** |

##### B2B Weighted Priority Scoring Method

```
Composite Priority Score = 
  Customer Willingness to Pay (0-10) × 0.20 +
  Strategic Alignment (0-10) × 0.15 +
  Contribution to NRR (0-10) × 0.15 +
  Technical Feasibility (0-10) × 0.15 +
  Competitive Coverage (0-10) × 0.10 +
  Implementation Complexity (0-10, lower is better) × 0.10 +
  Contribution to NDR (0-10) × 0.10 +
  Compliance Necessity (0-10) × 0.05
```

##### RICE Model (Intercom Classic)

```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach: How many customers/users will be affected within a given time period?
  - Measure by customer count, not user count (B2B specific)
  - Distinguish between "affected" and "actively using"

Impact: How big is the impact on each customer?
  - 3 = Massive impact (customer KPI significantly improved)
  - 2 = High impact
  - 1 = Medium impact
  - 0.5 = Low impact
  - 0.25 = Minimal impact

Confidence: How certain are you about your estimates?
  - 100% = High confidence (data/clear user feedback)
  - 80% = Medium confidence (partial evidence)
  - 50% = Low confidence (intuition/guess)
  - 20% = Wild guess (hypothesis needing validation)

Effort: How many person-months are needed?
  - Use actual person-months rather than story points (easier for cross-functional communication)
```

##### MoSCoW (For Fixed-Deadline Projects)

| Type | Meaning | Proportion | Strategy |
|------|------|------|------|
| **Must Have** | Not complete without it | ≤60% | Must deliver in this version |
| **Should Have** | Important but replaceable | ~20% | Try to deliver, can downgrade if risks arise |
| **Could Have** | Nice to have | ~20% | Only if there's spare capacity |
| **Won't Have** | Explicitly not doing (this cycle) | 0% this cycle | Move to Next or Later |

#### B2B Requirement Four-Quadrant (By Value/Cost)

```
                    High Business Value
                        │
         ┌──────────────┼──────────────┐
         │   Strategic   │   Core       │
         │   Projects    │   Features   │
         │  (Long-term   │  (Do Now)    │
         │   investment) │              │
         │  e.g., AI     │  e.g.,       │
         │  capability   │  Approval    │
   High ───┼──────────────┼──────────────┼─── Low
   Impl.   │              │              │     Impl.
   Cost    │   Don't Do / │   Quick      │     Cost
         │   Watch      │   Iteration  │
         │  (Abandon)   │  (Small cost │
         │  e.g., Over- │  quick win)  │
         │  customization│  e.g., Batch │
         └──────────────┼──────────────┘
                        │
                    Low Business Value
```

#### Outputs

1. **Requirement Priority Ranking Table** (Excel, with scoring details)
2. **KANO Classification Results**
3. **Version Planning Recommendations** (Now / Next / Later)
4. **Requirement Review Materials** (PPT format, for requirement review meetings)

---

### Stage 4: Solution Design (B2B Core)

**Role Hat: Solution Architect + Process Designer**

> This is the most core, most professionally deep stage for B2B product managers.
> Solution design determines not just "what features to build," but "how the organization operates."
> Reference: Yang Kun's "Mastering B2B" five-module knowledge system: Business Diagnosis → Solution Design → Management Implementation → Architecture Advancement → Capability Growth.

#### B2B Solution Design 7 Pillars

---

##### Pillar 1: Multi-Role Permission Model Design

**Three Permission Model Selection:**

| Model | Description | Pros | Cons | Applicable Scenarios |
|------|------|------|------|---------|
| **RBAC** | Role-Based Access Control | Simple, intuitive, standard | Not flexible enough | 90% of enterprise scenarios |
| **ABAC** | Attribute-Based Access Control | Flexible, fine-grained | Complex, performance overhead | High security/compliance scenarios |
| **ReBAC** | Relationship-Based Access Control | Social/hierarchical scenarios | Complex implementation | Organizational hierarchy/approval chains |

**RBAC Design Steps (5-Step Method):**

```
Step 1: Enumerate all operations (pages/buttons/APIs/data scope)
Step 2: Define roles (start from organizational structure, not technical)
  ├── Super Admin - Global configuration, organization management
  ├── System Admin - Daily management, user permissions
  ├── Department Admin - Department-level management
  ├── Business Operator - Core business operations
  ├── Approver - Process approval
  ├── Auditor - Read-only + log viewing
  └── Custom Roles - Allow tenant customization
Step 3: Role-Operation mapping (permission matrix)
Step 4: User-Role binding (support one user with multiple roles)
Step 5: Data permission policy overlay (row-level/column-level)
```

**Permission Granularity Hierarchy:**
```
Menu Level → Page Level → Button Level → Data Level (Row) → Data Level (Column) → Field Level
  ↓         ↓         ↓         ↓            ↓          ↓
  Can see   Can access Can operate Which data  Which fields Can edit
  which menus which pages which buttons scope    can see    which fields
```

**Data Permission Strategy:**

| Strategy | Rule | Applicable Role |
|------|------|---------|
| All Data | No restrictions | Super Admin |
| Own Department & Subordinates | dept_path LIKE 'xxx%' | Department Admin |
| Self Only | creator_id = current_user_id | Regular Operator |
| Specified Scope | Via data permission configuration table | Custom Role |
| Same Organization | tenant_id = current_tenant_id | All Roles (baseline) |

**Outputs:** Role-Permission Matrix Table (Excel) + Data Permission Strategy Document

---

##### Pillar 2: Approval Flow & Workflow Design (BPMN 2.0)

**Complete Approval Node Type Catalog:**

| Node Type | Description | Example |
|---------|------|------|
| **Manual Approval** | Specified person/role/position approval | Department manager approval |
| **Auto-Approval** | Auto-pass when conditions met | Amount < 500 auto-pass |
| **Conditional Branch** | Different branches based on conditions | Amount > 5000 goes to finance approval |
| **Countersign** | All must approve to pass | All VPs agree |
| **Or-Sign** | Any one approves to pass | Duty approval |
| **Progressive Approval** | Escalate by organizational level | Team Lead → Manager → Director → VP |
| **Transfer** | Transfer to another approver | When approver is unavailable |
| **Add Approver** | Add additional approver | Need extra legal confirmation |
| **CC** | Notify but not participate in approval | Inform relevant departments |
| **Withdraw** | Initiator withdraws | Discover error after submission |
| **Reject** | Reject (reject to where?) | Initiator/Previous node/Specified node |

**Approval Efficiency Design Principles:**

```
1. Approval nodes ≤ 5 (must justify if more)
2. Approvers per node ≤ 3
3. Must have timeout strategy (remind/escalate/auto-pass/auto-reject)
4. Mobile must support approval (WeCom/DingTalk/Feishu integration)
5. Approval detail page includes: complete info + approval history + action buttons + attachments
6. Support batch approval (one-click approval for similar requests)
7. Approver view: pending approval list + approved list
8. Initiator view: my applications + approval progress + withdraw/urge
```

**Exception Flow Handling (The most easily overlooked part in B2B!):**

| Exception Scenario | Handling Strategy |
|---------|---------|
| Approver resigned/transferred | Auto-transfer to superior or proxy approver |
| Approval timeout | Remind (24h) → Escalate (48h) → Auto-pass/reject (72h) |
| Approver is also initiator | Auto-skip that node |
| Org structure changes during process | Use org structure at time of initiation |
| Concurrent approval conflict | First-come-first-served, notify the later one |
| Approval system downtime | Auto-recover flow after status restoration |

**State Machine Diagram (Core Deliverable):**
Use draw.io to draw complete state machine, including all states' entry conditions/exit conditions/executable operations.

**Outputs:** Approval Flow State Machine Diagram (draw.io) + Approval Rule Configuration Table (Excel) + Exception Scenario Handling Table

---

##### Pillar 3: Multi-Tenant Architecture Design

**Four Isolation Strategies & Decision Matrix:**

| Strategy | Isolation Strength | Cost | Implementation Complexity | Applicable Scenarios |
|------|---------|------|-----------|---------|
| **Database per Tenant** | ⭐⭐⭐⭐⭐ | Highest | Medium | Finance/Healthcare with strong compliance requirements |
| **Schema per Tenant** | ⭐⭐⭐⭐ | High | Medium-High | Head customers with customization needs |
| **Shared Table + tenant_id** | ⭐⭐ | Lowest | Low | Standardized SaaS, SMB customers |
| **Hybrid Model** | ⭐⭐⭐ | Medium-High | High | Head customers independent + long-tail shared |

**Tenant Isolation Decision Tree:**
```
Customer compliance requirements high? → Yes → Database per Tenant
                                     → No → Customer customization needs high? → Yes → Schema per Tenant
                                                                              → No → Customer count large? → Yes → Shared Table
                                                                                                        → No → Hybrid
```

**Tenant-Level Configurable Items Checklist:**

| Configuration Category | Configurable Items | Implementation Method |
|---------|---------|---------|
| Branding | Logo/Theme Color/Name | Tenant configuration table |
| Organization | Department hierarchy/Positions/Roles | Tree configuration |
| Process | Approval rules/Process templates | Workflow engine configuration |
| Data | Custom fields/Numbering rules/Print templates | Extension fields + Rule engine |
| Permissions | Custom roles/Data scope | Permission engine |
| Reports | Custom reports/Dashboards | Report engine |
| Integration | SSO configuration/API Key/Webhook | Integration configuration |

**Outputs:** Multi-Tenant Architecture Design Document + Tenant Configuration Checklist---

##### Pillar 4: Data Dictionary & Master Data Management (MDM)

**Data Dictionary Standard Template (one per table):**

| Field Name | Field Code | Type | Length | Required | Default | Unique | Index | Enum Values | Validation Rules | Configurable | Description |
|--------|---------|------|------|------|--------|------|------|--------|---------|--------|------|
| ID | id | bigint | - | Yes | auto | PK | - | - | - | No | Primary key |
| Name | name | varchar | 100 | Yes | - | No | - | - | ≤100 chars | No | Name |
| Status | status | varchar | 20 | Yes | 'draft' | No | idx_status | See appendix | - | No | Status |
| Tenant ID | tenant_id | bigint | - | Yes | - | No | idx_tenant | - | - | No | Multi-tenant isolation |

**MDM Core Entities:**

B2B products must manage these master data entities:
- Organizational Structure (Company → Department → Position → Employee)
- Customer/Supplier Master Data
- Product/Material Master Data
- Account/Project/Cost Center
- Contract/License

**Database Naming Conventions:**
```
Table: t_{module_prefix}_{table_name}  → Example: t_pur_purchase_request
Field: snake_case                      → Example: created_at, creator_id
Index: idx_{field_name}                → Example: idx_tenant_id, idx_status
Unique Index: uk_{field_name}          → Example: uk_request_no
Foreign Key: fk_{table}_{field}        → Example: fk_user_creator_id
Boolean: is_xxx / has_xxx              → Example: is_deleted, has_attachment
Time: xxx_at                           → Example: created_at, approved_at
Amount: xxx_amount (in cents)          → Example: total_amount → DECIMAL(18,0)
```

**Outputs:** Complete Data Dictionary (Excel) + ER Diagram (draw.io)

---

##### Pillar 5: Integration & Open Capability Design

**Enterprise Integration Patterns (EIP) Selection Guide:**

| Integration Pattern | Real-time | Coupling | Applicable Scenarios |
|---------|--------|--------|---------|
| File Transfer (SFTP) | Low | Low | Batch data sync, reconciliation |
| RESTful API | High | Medium | Standard integration, external exposure |
| Message Queue (MQ) | High | Low | Async decoupling, event-driven |
| Webhook | High | Medium-Low | Event push, notifications |
| gRPC | High | High | Internal microservices |
| Shared Database | Highest | Highest | Legacy system integration (not recommended) |

**Enterprise Integration Maturity Ladder:**

```
L1: File Import/Export (CSV/Excel)           ← MVP must achieve at least this level
L2: Webhook + Message Notifications           ← Achieve this level at GTG stage
L3: RESTful API (with API documentation)      ← Required for scaling
L4: SSO + Org Structure Sync                  ← Standard for enterprise customers
L5: Deep Integration (bidirectional sync + embedded components) ← Industry-leading solution
```

**Must-Support Integration Checklist:**
- SSO/Identity Authentication: SAML 2.0, OAuth 2.0/OIDC, LDAP/AD Domain, CAS
- Message Notifications: WeCom/DingTalk/Feishu, Email (SMTP), SMS
- Electronic Signature: DocuSign/eSign providers
- Enterprise Payment: Bank direct connection/Corporate bank transfer/Supply chain finance
- Electronic Invoicing: E-invoice platform integration
- Data Integration: ETL/Data sync/Master data distribution

**OpenAPI Design Standards (if product provides an open platform):**

| Element | Standard |
|------|------|
| Versioning | URL path versioning: /api/v1/ |
| Authentication | Bearer Token + API Key + App Secret |
| Rate Limiting | Token bucket algorithm, per API Key |
| Documentation | OpenAPI 3.0 specification, Swagger auto-generated |
| Error Codes | Unified 4-digit error code + message + details |
| Pagination | pageNum + pageSize, return total |
| Format | JSON, UTF-8 encoding |

**Outputs:** Integration Architecture Diagram (draw.io) + API Design Document

---

##### Pillar 6: Compliance & Audit Design

**Compliance Frameworks B2B Products Must Consider:**

| Standard/Regulation | Applicable Domain | Core Requirements |
|-----------|---------|---------|
| **Information Security Classification (China)** | Systems within China | 5-level protection, general enterprises need Level 3 |
| **GDPR** | Involving EU user data | Data subject rights, DPO, cross-border data transfer restrictions |
| **PIPL (Personal Information Protection Law)** | Personal information within China | Informed consent, separate consent for sensitive info, data localization |
| **SOC 2 Type II** | SaaS going global | Security/Availability/Processing Integrity/Confidentiality/Privacy — five trust services |
| **ISO 27001** | General information security | ISMS framework, risk assessment, continuous improvement |
| **Trusted Computing (China)** | Government/State-owned enterprises | Domestic CPU/OS/DB/Middleware compatibility |
| **HIPAA** | Healthcare (US) | PHI protection, BA agreements |
| **PCI DSS** | Payment card industry | Cardholder data protection |

**Audit Log Design Standards:**

```
Every audit log entry must contain:
├── Who (operator_id + operator_name + operator_role)
├── When (timestamp, precise to milliseconds)
├── What action (action: CREATE/READ/UPDATE/DELETE/EXPORT/APPROVE)
├── On what resource (resource_type + resource_id + resource_name)
├── Before data (before_snapshot, JSON)
├── After data (after_snapshot, JSON)
├── From where (IP + User-Agent + Session ID)
├── Result (success/failure + error_detail)
└── Audit log itself: cannot be deleted, modified, or manually inserted
```

**Data Security Baseline:**
- Transport: Full-site HTTPS, API signing
- Storage: AES-256 encryption for sensitive fields, key management via KMS
- Access: RBAC least privilege, IP whitelist, login time restrictions
- Masking: Auto-mask phone/ID/bank card numbers on display
- Backup: Daily full + incremental, off-site backup
- Disaster Recovery: RPO < 1h, RTO < 4h

---

##### Pillar 7: B2B Product Architecture Design

**Evolution Path from Monolith to Middle Platform (Yang Kun Framework):**

```
Stage 1: Excel → Single System → Multiple Independent Systems → System Integration → Platformization
  │          │           │            │           │
  Startup    Growth      Expansion    Mature      Platform Stage

Middle Platform Architecture (Ultimate form of enterprise products):
├── Business Middle Platform: Reusable business capabilities (User/Permission/Approval/Notification/Payment/Signature)
├── Data Middle Platform: Unified data assets (Master Data/Metrics System/Data Services/Data Governance)
├── Technical Middle Platform: Technical infrastructure (Microservices/Containers/CI-CD/Monitoring/Logging)
└── Organizational Middle Platform: Organizational capability accumulation (Methodology/Toolchain/Training System)
```

---

### Stage 5: AI Product Design

**Role Hat: AI Product Designer**

> AI is reshaping B2B product management. AI PM is no longer optional — it's mandatory.
> B2B products are upgrading from "System of Record" to "System of Action,"
> and AI is the core engine of this transformation.

**References:**
- O'Reilly "The Future of PM is AI-Native" (2025)
- Stanford "Getting Beyond the Sandbox" (2024)
- Marty Cagan / Teresa Torres product methodology in the AI era
- Chinese Enterprise AI Product Design 10-Lesson Framework

---

#### 5.1 AI PM Capability Model (3 Types of AI PM)

| Type | Description | Core Skills |
|------|------|---------|
| **AI Builder PM** | Builds AI models/infrastructure products | Model literacy, training pipelines, MLOps, evaluation |
| **AI Experience PM** | Designs AI interaction experiences | UX patterns, HCI-AI, conversation design, trust design |
| **AI-Enhanced PM** | Uses AI to amplify traditional PM work | AI toolchain, automation, data-driven decision-making |

> This Skill covers AI-Enhanced PM and AI Experience PM (the two most common types in B2B).

---

#### 5.2 AI Product Design 10 Modules (Complete Framework)

##### Module 1: Model Selection & Strategy

**Model Selection Decision Matrix:**

| Dimension | Closed-source API (e.g., Claude/GPT) | Open-source Model | Self-trained Model |
|------|---------------------|---------|-----------|
| Capability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | Pay-per-use (can be high or low) | Inference cost controllable | Training + inference cost high |
| Data Security | Data sent externally | Fully local | Fully local |
| Compliance | Needs evaluation | Good | Best |
| Iteration Speed | Fastest (auto model upgrades) | Medium | Slowest |
| Customizability | Prompt + RAG | RAG + Fine-tuning | Fully customizable |
| B2B Scenarios | General scenarios, rapid validation | Data-sensitive, private deployment | Vertical industry, extreme customization |

**B2B Model Selection Decision Tree:**
```
Can data leave the enterprise?
├── Yes → Large data volume?
│       ├── Yes → Closed-source API + RAG (cost controllable)
│       └── No → Closed-source API direct call
└── No → Must be privately deployed
          ├── General scenario → Open-source model + RAG
          └── Special scenario (e.g., medical/legal) → Open-source model + Fine-tuning
```

**Model Capability Boundaries (Every AI PM Must Know):**

| What Models Do Well | What Models Don't Do Well | How to Compensate |
|---------|---------|------------|
| Text understanding & generation | Precise mathematical calculation | Supplement with tools (function calling) |
| Summarization & classification | Real-time information | Supplement with RAG |
| Translation & rewriting | Long document precise recall | Context window limitations |
| Code generation | Overly long reasoning chains | Chain-of-Thought improvement |
| Sentiment analysis | Image spatial relationships | Not suitable for pure vision tasks |
| Format conversion | Factual accuracy | RAG + source citation |

---

##### Module 2: RAG Architecture Design

**RAG is the core architecture of current B2B AI products.**

```
RAG Standard Pipeline:
┌──────────────────────────────────────────────┐
│ 1. Document Ingestion                         │
│    ├── Document parsing (PDF/Word/HTML/Image OCR)        │
│    ├── Chunking: by paragraph/by semantic/by fixed length │
│    └── Metadata extraction (doc name/date/author/permission tags)     │
├──────────────────────────────────────────────┤
│ 2. Embedding (Vectorization)                 │
│    ├── Text → Vector (text-embedding-3-large, etc.)   │
│    └── Store in vector DB (Pinecone/Weaviate/Milvus)│
├──────────────────────────────────────────────┤
│ 3. Retrieval                                 │
│    ├── Hybrid retrieval: dense vector + sparse (BM25)        │
│    ├── Reranking: secondary sort of recalled results    │
│    └── Filtering: by permission/date/tag             │
├──────────────────────────────────────────────┤
│ 4. Generation                                │
│    ├── Context assembly: System Prompt + Retrieved Context + User Query │
│    ├── Call LLM to generate answer                         │
│    └── Citation annotation: mark information sources in answer             │
├──────────────────────────────────────────────┤
│ 5. Evaluation & Iteration                    │
│    ├── Answer quality evaluation (accuracy/relevance/completeness)        │
│    ├── Bad Case analysis → Tuning                      │
│    └── Chunking strategy/retrieval strategy iteration                    │
└──────────────────────────────────────────────┘
```

**RAG Design Key Decisions:**

| Decision Point | Options | Recommendation |
|--------|------|------|
| Chunk size | 256/512/1024/2048 tokens | 512 as primary, 1024 for key paragraphs |
| Overlap | 0/10%/20%/25% | 10-20% (avoid semantic cuts) |
| Retrieval count (top-k) | 3/5/10/20 | 5-10 items |
| Embedding model | text-embedding-3-large/small, bge-large-zh | Chinese scenarios choose bge |
| Vector database | Pinecone/Milvus/Weaviate/Qdrant/pgvector | Production >1M vectors use Milvus |
| Reranking | Cohere Rerank/bge-reranker | Significant retrieval quality improvement |

---

##### Module 3: Agent & Multi-Agent Systems

**Agent = LLM + Memory + Planning + Tools**

**When to Use Agent vs Simple LLM Call:**

| Scenario | Simple LLM | Agent |
|------|---------|-------|
| Answering questions | ✅ | Overkill |
| Executing multi-step tasks | ❌ | ✅ |
| Needing to call external tools | ❌ | ✅ |
| Needing planning and reflection | ❌ | ✅ |
| Cost-sensitive | ✅ | ❌ (multi-turn calls costly) |
| Latency-sensitive | ✅ | ❌ (multi-turn calls high latency) |

**Agent Architecture Patterns:**

```
Pattern 1: ReAct (Reasoning + Acting)
  Thought → Action → Observation → Thought → ... → Final Answer

Pattern 2: Plan-and-Execute
  Plan → Execute Step 1 → Execute Step 2 → ... → Summarize

Pattern 3: Multi-Agent Orchestration
  Orchestrator → Agent A (Research) ↘
               → Agent B (Analyze) → Orchestrator → Response
               → Agent C (Write) ↗

Pattern 4: Human-in-the-Loop (HITL)
  Agent Execute → Human Approve → Agent Continue
  Key: At which nodes does human approval need to be required? (Payment/Publishing/Deletion/External Sending)
```

**HITL Design (Compliance Essential for B2B Agents):**

| Operation Risk Level | Agent Behavior | Human Role | Example |
|------------|----------|---------|------|
| **Low Risk** | Agent executes autonomously | Post-hoc spot check | Adding tags, generating summaries |
| **Medium Risk** | Agent generates → Human confirms | Pre-execution confirmation | Sending notifications, changing status |
| **High Risk** | Agent suggests → Human executes | Human operates | Deleting data, approving |
| **Not Allowed** | Agent operation prohibited | Human only | Payments, contract signing, permission changes |

---

##### Module 4: Prompt Engineering

**Prompt engineering is the new fundamental skill for PMs. Prompt = the "UI" of B2B AI products.**

**Structured Prompt Design Pattern:**

```
┌─────────────────────────────────────────────┐
│ [System Prompt] - System-level role and capability definition          │
│ You are [role], your task is [task], your constraints are [...]   │
├─────────────────────────────────────────────┤
│ [Context] - Contextual information (from RAG retrieval/user state)  │
│ Current user: [role/department/permissions]                      │
│ Relevant data: [...]                               │
├─────────────────────────────────────────────┤
│ [Task] - Specific task instruction                          │
│ Please execute: [...]                                 │
│ Steps: 1. ... 2. ... 3. ...                   │
├─────────────────────────────────────────────┤
│ [Output Schema] - Output format constraints                 │
│ Please output in the following JSON format: { ... }                  │
├─────────────────────────────────────────────┤
│ [Few-Shot Examples] - Examples (optional but recommended)        │
│ Example input: [...] Example output: [...]                │
├─────────────────────────────────────────────┤
│ [Constraints] - Prohibited items                       │
│ Do not: [...] If you don't know: [...]                  │
└─────────────────────────────────────────────┘
```

**B2B Product Prompt Design Principles:**
1. Role setting must be precise (not "you are an assistant," but "you are a financial auditor with 10 years of experience")
2. Output format must be structured (JSON Schema first, easy for downstream consumption)
3. Constraints must be explicit ("do not fabricate data," "if you don't know, say you don't know")
4. Examples must be realistic (use real business scenario examples, not generic examples)
5. Security must have guardrails ("refuse to answer questions unrelated to XX")

---

##### Module 5: Context Engineering

> Context Engineering is a deeper design layer than Prompt Engineering.
> Core question: "What information to give the model, in what structure, at what timing?"

**Context Window Budget Management:**

```
Total budget: 128K tokens (using Claude as example)

Allocation strategy:
├── System Prompt: 2-5K tokens (role + rules + format)
├── Conversation history: 10-20K tokens (recent conversation)
├── RAG retrieval results: 20-40K tokens (most relevant documents)
├── User current query: 0.5-2K tokens
├── User profile/preferences: 2-5K tokens
├── Tool definitions: 5-10K tokens (function definitions)
└── Reserved buffer: ~20K tokens (for model thinking/generation)
```

**Dynamic Context Assembly:**
- Load different System Prompts based on user role
- Load different retrieval strategies based on current task type
- Personalize context based on user behavior history
- Key information front-loading (most important info at the beginning and end of prompt)---

##### Module 6: Memory Engineering

**Upgrade AI from "one-time conversations" to "continuous partnership."**

| Memory Type | Storage Content | Lifespan | Example |
|---------|---------|------|------|
| **Short-term Memory** | Current conversation context | Current session | Requirement details just discussed |
| **Long-term Memory - User** | User preferences/habits/history | Persistent | "This user prefers concise answers" |
| **Long-term Memory - Business** | Business knowledge/rules/patterns | Persistent | "This customer's contract expires on XX" |
| **Working Memory** | Current task state | During task | "Currently on step 3 of the approval process" |

---

##### Module 7: Evaluation System Design

**No evaluation = no AI product iteration.**

**Evaluation Dimension Matrix:**

| Dimension | Metric | Measurement Method |
|------|------|---------|
| **Accuracy** | Factual correctness rate | Golden Dataset manual annotation + auto comparison |
| **Relevance** | Answer-to-question relevance | Manual scoring + semantic similarity |
| **Completeness** | Information coverage | Check if key information points are covered |
| **Safety** | Harmful content rate | Auto scanning + red team testing |
| **Latency** | P50/P95/P99 response time | Auto monitoring |
| **Cost** | Token consumption per call | Auto statistics |
| **User Satisfaction** | Thumbs up/down/CSAT | User feedback collection |

**Golden Dataset Construction Process:**
```
1. Collect 100+ real user queries
2. Manually annotate standard answers
3. Establish scoring criteria (Rubric)
4. Regularly update (add new queries monthly)
5. Bad Case → Analysis → Tuning → Validation
```

---

##### Module 8: AI UX Pattern Design

**6 Interaction Patterns for B2B AI Products ("Six Meridians Sword" Framework):**

| Pattern | Description | Applicable Scenarios | Example |
|------|------|---------|------|
| **API Wrapper** | AI works in background, user unaware | High determinism, high frequency | Smart sorting, auto classification |
| **GUI Embedded CUI** | Embed conversation in graphical interface | Medium frequency, needs flexibility | Salesforce Agentforce |
| **Chat Mode** | Pure conversation interface | Strong exploratory | Notion AI |
| **Co-pilot Mode** | Sidebar AI assistant | Assisted creation/analysis | GitHub Copilot |
| **Autonomous Execution** | Agent autonomously completes tasks | Complex multi-step tasks | Auto-generate reports |
| **Human-Machine Collaboration** | AI suggests → Human confirms → Execute | High-risk operations | Contract review → Human signs |

**B2B AI UX Principles:**
1. **Progressive Trust**: Start with low-risk features, gradually open up high-risk ones
2. **Reversible**: AI operations should be undoable
3. **Explainable**: Why did AI do this? Cite sources
4. **Overridable**: Users can manually take over at any time
5. **Show Uncertainty**: Display confidence level when uncertain, rather than pretending certainty

---

##### Module 9: AI Product Data Flywheel

```
More Users → More Interaction Data → Better AI → More Users
    ↑                                              ↓
    └──────── Better Data Quality ← Better Product Experience ←──────┘

Flywheel Design Key Points:
1. Every user interaction should produce data usable for improvement
2. Implicit feedback (clicks/dwell/adoption) >> Explicit feedback (thumbs up/ratings)
3. Bad Cases are gold mines: every failure is an opportunity for improvement
4. Data labeling should be embedded in product flow (e.g., "Was this answer helpful?")
```

---

##### Module 10: AI Product Strategy

**Wedge Strategy (Recommended by O'Reilly):**

```
Traditional path: Build platform → Find scenarios → Acquire users
AI era path: Find one pain point → Solve it extremely well → Gain trust → Capture data → Expand

Core principles:
1. Start with one "hero user's" one pain point
2. Go narrow and deep, not broad and shallow
3. Simple tools are more trustworthy than complex agents
4. Data is the moat, models are not
```

**B2B AI Product Value Proposition Design:**

```
Framework: Technical Feature × Business Scenario × Quantified Benefit

Example:
"Using large language models (technical feature) to auto-generate procurement comparison reports (business scenario),
 reducing procurement decision time from 3 days to 30 minutes (quantified benefit)"
```

#### AI Product Design Outputs

1. **AI Product Strategy Document** (including model selection/data strategy/flywheel design)
2. **RAG Architecture Design Diagram**
3. **Agent Design Document** (including HITL decision matrix)
4. **Prompt Template Library**
5. **Evaluation System Design** (including Golden Dataset design)
6. **AI UX Interaction Specification**

---

### Stage 6: Prototyping & Interaction

**Role Hat: Solution Architect**

> B2B Prototype Core Principle: **Efficiency > Aesthetics**.
> Reference: Marty Cagan "Design from Day One," Yang Kun "Interface Design" chapter.

#### B2B Prototype Design 10 Principles

```
1. List pages must have: search/filter/sort/pagination/batch operations/export
2. Forms must have: required field indicators/validation hints/save draft/submit confirmation
3. Detail pages must have: basic info/related info/operation history/back
4. Every operation must have feedback (loading → success/error Toast)
5. Dangerous operations must have a secondary confirmation dialog
6. Batch operations must have a progress bar
7. Large data volumes: virtual scrolling/lazy loading (over 1000 records)
8. Keyboard shortcuts (Enter to submit/Esc to cancel/↑↓ to select/Ctrl+S to save)
9. Error messages tell users "what to do" not just "something went wrong"
10. Empty states have guidance ("No data yet, click to create your first one")
```

#### B2B Standard Page Templates (4 Types)

##### 1. Dashboard

```
┌──────────────────────────────────────────────────────┐
│ [Logo] Nav Bar                    [Notifications][Avatar][Settings]    │
├─────────┬────────────────────────────────────────────┤
│         │ ┌──────────┬──────────┬──────────┬──────┐ │
│ Sidebar │ │ Pending  │ In Progress│ Completed │ Error  │ │
│ Nav     │ │   128    │   506   │  3,240  │  12  │ │
│         │ └──────────┴──────────┴──────────┴──────┘ │
│ Workspace│ ┌──────────────────┐ ┌──────────────────┐ │
│ Procurement│ │   Trend (Line)   │ │   Category (Pie) │ │
│ Approval │ └──────────────────┘ └──────────────────┘ │
│ Reports │ ┌──────────────────┐ ┌──────────────────┐ │
│ Settings │ │   My Tasks (List) │ │   Quick Links (Cards)  │ │
└─────────┴─┴──────────────────┴─┴──────────────────┴─┘
```

##### 2. CRUD List Page

```
┌─────────────────────────────────────────────────────┐
│ [Search:______] [Status▼] [Date Range▼] [Search] [Reset]    │
│                                                     │
│ [New] [Batch Import] [Batch Export] [Batch Delete]              │
│                                                     │
│ ☐ |No. |Name  |Status   |Owner|Created |Actions        │
│ ☐ |001  |...  |In Progress  |Zhang San  |06-07   |Edit  Delete   │
│ ☐ |002  |...  |Completed  |Li Si  |06-06   |Edit  Delete   │
│                                                     │
│ 3 Selected [Batch Approve]   Total 2,345 records  < 1 2 3 ... 118 >   │
└─────────────────────────────────────────────────────┘
```

##### 3. Form Page

```
┌─────────────────────────────────────────────────────┐
│  Basic Info ▸                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │ [*] Name: [_____________________________]    │   │
│  │ [*] Type: [Dropdown▼]                        │   │
│  │      Description: [_____________________________]    │   │
│  └─────────────────────────────────────────────┘   │
│  Detail Info ▸                                         │
│  ┌─────────────────────────────────────────────┐   │
│  │      Date: [Date Picker]                        │   │
│  │      Attachment: [Choose File]  No file selected               │   │
│  └─────────────────────────────────────────────┘   │
│                              [Save Draft] [Submit]      │
└─────────────────────────────────────────────────────┘
```

##### 4. Approval Detail Page

```
┌─────────────────────────────────────────────────────┐
│ Approval No.: AP20260607001  Status: In Approval (2/3)           │
├─────────────────────────────────────────────────────┤
│ Application Info                                            │
│ Applicant: Zhang San | Dept: Tech | Time: 2026-06-07      │
│ Amount: ¥50,000.00                                │
├─────────────────────────────────────────────────────┤
│ Approval Progress                                            │
│ Initiated ──✅── Dept Manager ──⏳── Finance Director ──⭕── CEO  │
│ Zhang San     Li Si (Approved)   In Progress...    Pending           │
├─────────────────────────────────────────────────────┤
│ Approval History                                            │
│ 06-07 10:00 Initiator Zhang San submitted application                      │
│ 06-07 11:30 Dept Manager Li Si approved Comment: "Approved"       │
├─────────────────────────────────────────────────────┤
│ Approval Comment: [_______________]                          │
│                              [Reject] [Transfer] [Approve]   │
└─────────────────────────────────────────────────────┘
```

#### Prototype Output Methods

**Method 1: HTML Interactive Prototype (Recommended, zero tool dependency, most flexible)**
- Complete HTML + Tailwind CSS + Alpine.js/Vue3 CDN
- Real data and interactions, runs directly in browser
- Includes all page states (loading/empty/error/edge cases)
- Includes simulated permission control (switch roles to view different views)
- Approval flow interaction visualization (can simulate approve/reject flow)

**Method 2: Penpot (Open-source Figma/Mockplus alternative)**
- Open-source (MPL-2.0), Web-based, can self-host
- Supports: vector editing/interactive prototypes/components/design tokens/real-time collaboration
- Has Plugin API, REST API (read), MCP Server
- Chinese-friendly, community support

**Method 3: JsDesign (Domestic Figma alternative)**
- Free Web version, native Chinese
- Has D2C (Design to Code) functionality
- Has BoardMix collaborative whiteboard

#### Prototype Tool Call Table

| Need | Tool Call | Command/Method |
|------|---------|---------|
| HTML Interactive Prototype | Direct generation | Generate HTML file, open in browser |
| Wireframes/Low-fidelity | `excalidraw-diagram` | "Draw a wireframe of XX page" |
| Page Flow Diagram | `drawio-skill` | "Draw XX page flow diagram" |
| High-fidelity Design Reference | Penpot/JsDesign | Export Figma format reference |

---

### Stage 7: Diagrams & Architecture

**Role Hat: Solution Architect + Process Designer**

> Diagrams are the universal language of B2B PMs. One picture is worth a thousand words — professional diagrams directly determine the approval rate of solution reviews.

---

#### 12 Types of Must-Draw B2B Diagrams (with Tools & Commands)

| # | Diagram Type | Purpose | Recommended Tool | Example Command |
|---|---------|------|---------|---------|
| 1 | **Business Process Diagram (Swimlane)** | Cross-role process | `drawio-skill` | "Draw XX business swimlane diagram, roles: Initiator/Approver/System" |
| 2 | **System Architecture Diagram (C4)** | System overview | `drawio-coderknock` | "Draw XX system C4 container diagram" |
| 3 | **Functional Architecture Diagram** | Functional module tree | `drawio-skill` | "Draw XX product functional architecture diagram" |
| 4 | **Data Architecture Diagram (ER Diagram)** | Data modeling | `drawio-generator-pro` | "Draw XX module ER diagram" |
| 5 | **Integration Architecture Diagram** | System integration relationships | `drawio-skill` | "Draw XX system integration architecture diagram" |
| 6 | **Deployment Architecture Diagram** | Cloud/Data center deployment | `drawio-coderknock` | "Draw XX deployment architecture diagram" |
| 7 | **Approval Flow State Machine** | Approval/Status transitions | `drawio-skill` | "Draw XX approval state machine diagram" |
| 8 | **User Role Matrix** | Permission relationships | `drawio-skill` | "Draw XX system role-permission matrix diagram" |
| 9 | **Product Roadmap (Gantt Chart)** | Timeline planning | `drawio-skill` | "Draw XX product H2 roadmap" |
| 10 | **Organizational Structure Diagram** | Org hierarchy | `drawio-skill` | "Draw XX company organizational structure diagram" |
| 11 | **Service Blueprint** | Front-backend linkage | `excalidraw-diagram` | "Draw XX scenario service blueprint" |
| 12 | **User Journey Map** | Full lifecycle | `excalidraw-diagram` | "Draw XX role's user journey map" |

#### Available Diagram Tool Matrix

| Tool | Output Format | Advantages | Applicable Scenarios |
|------|---------|------|---------|
| **drawio-skill** | .drawio (editable) | Official support, auto layout, professional colors | Architecture/Flow/ER diagrams |
| **drawio-coderknock** | .drawio | Python-driven, built-in templates | System architecture/Deployment architecture |
| **drawio-generator-pro** | .drawio | JSON→draw.io, structured | When precise layout control is needed |
| **excalidraw-diagram** | .excalidraw + PNG | Hand-drawn style, fast | Wireframes/Journey maps/Service blueprints |
| **processon-diagram** | ProcessOn online | Good Chinese ecosystem, many templates | When online collaboration is needed |
| **Mermaid (via code)** | SVG/PNG | Code as diagram, version controllable | Sequence diagrams/Class diagrams/State diagrams |

#### Diagram Output Self-Check Checklist

```
□ Who is the audience? (Executives = minimal / Technical = detailed / Customers = product value-oriented)
□ Can the core message be stated in one sentence?
□ Are legends/colors/symbols consistent? (Same system uses same color)
□ Is there a title + version + date?
□ Are arrow directions correct?
□ Are key decision points/exception branches annotated?
□ Are there any missing roles/systems/entities?
□ Are colors suitable for black-and-white printing?
```

#### B2B Diagram Color Specifications

```
Corporate Steady (Default):
- Primary: #1a56db (Blue - core systems)
- Secondary: #0e9f6e (Green - external systems)
- Warning: #e3a008 (Yellow - needs optimization)
- Danger: #e02424 (Red - risk points)
- Neutral: #6b7280 (Gray - non-key)
- Background: #f9fafb
- Text: #111827

Tech Blue Series:
- Primary: #2563eb
- Secondary: #7c3aed (Purple - differentiation)
- Emphasis: #06b6d4 (Cyan - highlights)
```

---

### Stage 8: Documentation Engineering

**Role Hat: Solution Architect + Product Evangelist**

> B2B PM's documentation capability = cross-team collaboration efficiency lever.
> Reference: Cagan "Writing is the operating system," Yang Kun "BRD/PRD/MRD" chapters.

#### Document Matrix

| Document | Reader | Length | Detailed Template |
|------|------|------|---------|
| **BRD Business Requirements Document** | Management/Investors | 15-25 pages | `references/templates/brd-template.md` |
| **MRD Market Requirements Document** | Product/Marketing teams | 15-20 pages | `references/templates/mrd-template.md` |
| **PRD Product Requirements Document** | Dev/QA/UED | 20-40 pages | `references/templates/prd-template-b2b.md` |
| **FRD Functional Requirements Document** | Backend/Frontend dev | 15-25 pages | `references/templates/frd-template.md` |
| **Competitive Analysis Report** | Product/Marketing/Management | 20-30 pages | `references/templates/competitive-analysis-b2b.md` |
| **User Research Report** | Product/UED/Management | 15-20 pages | `references/templates/user-research-report.md` |
| **Product Roadmap Report** | All staff/Customers | 1-page diagram + 10-page explanation | `references/templates/roadmap-report.md` |
| **Backlog & Version Planning** | Product/Dev | Excel | `references/templates/backlog-plan.md` |
| **Sales Enablement Kit** | Sales/Customers | 1-pager + Whitepaper + Demo | `references/templates/sales-enablement.md` |

#### B2B PRD Must Include 10 Modules

```
1. Version history and change log
2. Requirement background and business objectives (with BRD link, data support)
3. User roles and permission matrix ← B2B unique
4. Core business process diagrams (swimlane, normal + exceptions) ← B2B unique
5. Detailed feature specifications (with prototypes/field tables/interaction specs/permissions/statuses)
6. Approval flow and workflow design ← B2B unique
7. Data model design (ER diagram + data dictionary) ← B2B unique
8. Integration and interface requirements (internal + external + OpenAPI) ← B2B unique
9. Non-functional requirements (performance/security/availability/scalability/internationalization)
10. Acceptance criteria and test points (each AC can be verified item by item)
```

#### Document Generation Workflow

```
You describe requirements → AI confirms structure → Generate Markdown first draft → 
You confirm → Format as final version → Optional: Convert to DOCX/PDF/PPT

To DOCX: use word-docx skill (standard formatting, compliant with GB/T)
To PDF: use minimax-pdf skill (Chinese typesetting, beautiful design)
To PPT: use pptx-2 skill (extract key points, auto layout)
```

#### Document Quality Self-Check (4-Level Standard)

| Level | Standard |
|------|------|
| **Bronze (Usable)** | Content complete, logic clear, format standard |
| **Silver (Standardized)** | Standard template, consistent terminology, ready for review |
| **Gold (Excellent)** | Data-supported, deep analysis, management can directly make decisions |
| **Diamond (Outstanding)** | Methodological innovation, industry insight, can be cited as a whitepaper |

> Core deliverables at least Silver level; key decision documents strive for Gold level.---

### Stage 9: Development Collaboration

**Role Hat: Project Manager**

#### Standard Development Collaboration SOP

```
Requirement Review → Technical Solution Review → Task Breakdown (WBS) → Sprint Planning → 
Daily Standup → Progress Tracking → Test Acceptance → Release → Retrospective
```

#### Bi-Weekly Iteration Rhythm (B2B Standard)

```
Day 1-2:  PRD writing/refinement
Day 3:    Requirement review meeting (Product + Dev + QA + UED)
Day 4-6:  Technical solution design
Day 7:    Technical solution review + Task breakdown
Day 8-13: Development (including integration)
Day 12-15: Testing
Day 16:   Product acceptance
Day 17:   Launch preparation (release notes/help docs/canary strategy)
Day 18:   Full rollout
Day 19-20: Online monitoring + Retrospective
```

#### B2B Requirement Review Checklist

```
□ Every role considered? (Not just core users)
□ Exception flows complete? (Timeout/Reject/Withdraw/Insufficient permissions/Concurrent conflicts)
□ Large data volume performance? (100K+ records list/1000+ batch operations)
□ Data consistency? (Transaction boundaries/distributed consistency)
□ Historical data compatibility/migration plan?
□ Permission control covers all operations? (Read/Write/Batch/Export/Approve)
□ Audit logs cover all CUD operations?
□ Notification/reminder triggers correct?
□ Multi-language/multi-timezone/multi-currency?
□ Mobile approval adapted?
□ Any technical risks needing pre-research?
```

#### Acceptance Criteria (AC) Writing

```
Format: Given [precondition] When [user action] Then [expected result]

Example:
AC-001: Given the user is a procurement requester with create permission
        When the user fills in all required fields and clicks [Submit]
        Then the system creates a procurement request record, status is "In Approval,"
             and triggers the approval flow, next node approver receives notification
        
AC-002: Given the procurement request status is "In Approval" and current approver is Zhang San
        When Zhang San clicks [Reject] and fills in the rejection reason
        Then the procurement request status changes to "Rejected,"
             the initiator receives a rejection notification,
             the initiator can edit and resubmit
```

#### Pre-Launch Checklist

```
□ All P0 test cases passed
□ All P0 bugs fixed
□ Data migration scripts ready (if applicable)
□ Rollback plan ready
□ Help documentation updated
□ Release announcement prepared
□ Customer notification sent (if involving existing customers)
□ Monitoring alerts configured
□ Canary release plan determined
```

---

### Stage 10: Data & Growth

**Role Hat: Data Strategist**

#### B2B Core Metrics System (5-Level Pyramid)

```
L1: North Star Metric (1)
    └── L2: Primary Metrics (4-6)
         ├── Acquisition: MQL→SQL→Win Rate→CAC→CAC Payback
         ├── Activation: Onboarding Completion Rate → Time to First Value
         ├── Usage: DAU/WAU/MAU → Feature Adoption Rate → Stickiness Coefficient
         ├── Revenue: ARR/MRR → ARPU → LTV → NRR → NDR
         └── Quality: NPS/CSAT/CES → Churn Rate
              └── L3: Secondary Metrics (10-20, operational level)
                   └── L4: Tertiary Metrics (diagnostic level, as needed)
```

#### B2B North Star Metric Selection Guide

| Product Type | Common North Star | Why |
|---------|-----------|--------|
| SaaS Collaboration | WAU completing core tasks ratio | Measures team dependency |
| Transaction Platform | GMV / Matchmaking success rate | Measures platform value |
| Tool-type | DAU × Core feature usage depth | Measures usage stickiness |
| Middle Platform | API call count × Success rate | Measures service value |
| AI Product | AI adoption rate × Task completion rate | Measures AI actual value |

#### B2B-Specific Metrics Deep Dive

| Metric | Formula | Healthy Benchmark | What It Tells |
|------|------|---------|--------|
| **NRR** | (Beginning ARR + Expansion - Churn - Contraction) / Beginning ARR | >100% Good, >120% Excellent | Customer value growth |
| **NDR** | Same as NRR, but excluding new customers | >100% | Existing customer health |
| **TTV** | Days from contract signing to first value realization | <7 days Excellent | Onboarding efficiency |
| **Feature Adoption Rate** | Accounts using feature / Total active accounts | >30% Healthy | Feature penetration |
| **CES** | Customer Effort Score (1-7) | <3 | Product usability |
| **Expansion MRR** | MRR from existing customer upsells | >20% share | Upsell capability |
| **CAC Payback** | CAC / Monthly ARPU (months) | <18 months | Acquisition efficiency |
| **Logo Churn vs Rev Churn** | Customer count churn rate vs Revenue churn rate | Logo <5% annual, Rev <10% annual | Large vs small customer churn |

#### B2B Product Stage & Metric Focus

| Stage | ARR Range | Core Metrics | Focus |
|------|---------|---------|---------|
| **PMF Exploration** | <$100K | WAU, NPS, Activation | Find PMF, survive |
| **PMF Validation** | $100K-$1M | MRR, Churn, LTV/CAC | Validate replicability |
| **Efficiency Expansion** | $1M-$10M | MRR efficiency, NRR, Burn | Efficient growth |
| **Scale** | $10M+ | ARR + Rule of 40, FCF | Sustainable profitability |

#### Dashboard Design Principles

```
1. One screen viewable (no scrolling needed)
2. 7-10 core metrics, no more
3. With comparison (vs last week/last month/same period last year)
4. With alert thresholds (Red/Yellow/Green)
5. With drill-down entry (click to enter details)
6. Weekly auto-push reports
```

---

### Stage 11: Commercialization & GTM

**Role Hat: Commercialization Operator + Product Evangelist**

#### B2B Pricing Strategy Deep Dive

##### Pricing Model Decision Tree

```
What is your product?
├── Collaborative (value only with multiple users) → Per user/seat
├── Large feature differentiation → Feature tiered (Good/Better/Best)
├── Usage-driven → Per usage/API call/storage
├── Transaction platform → GMV commission / Flat rate
└── Hybrid → Base fee + Usage fee or Base fee + Feature tiers
```

##### Plan Design Iron Rules

```
1. 3 plans are optimal: Basic / Professional (Recommended) / Enterprise
2. Middle plan is the anchor: highest profit, most recommended
3. Enterprise plan must have "Contact Sales": lead capture entry, let large customers proactively reach out
4. Free Trial > Free Plan
5. Annual payment 20% discount is standard (reduce churn, improve cash flow)
6. Pricing psychology: $9,999 > $10,000
```

##### Pricing Number Strategy

```
Monthly → Annual discount: Monthly × 10 (≈17% off)
Tiered pricing: more users, lower marginal unit price
Anchoring effect: display Enterprise plan high price, making Professional plan "look like great value"
Pricing page design: highlight recommended plan ("Most Popular" tag), feature comparison table, FAQ section
```

#### GTM Strategy One-Pager

```
1. ICP (Ideal Customer Profile): Target customer persona
2. One-sentence value proposition
3. Pricing & plans
4. Sales channels: Direct/Channel/PLG/Hybrid
5. Sales material kit: One-pager/Whitepaper/Demo script/Competitive comparison table/ROI calculator
6. Onboarding process (Customer 90-day health plan)
7. Marketing plan
8. Key milestones & targets
```

#### Sales Enablement Kit Full Checklist

| Material | Format | Purpose |
|------|------|------|
| Product One-Pager | PDF/A4 | Sales can explain product in 30 seconds |
| Competitive Comparison Table | Excel | Handle customer horizontal comparisons |
| Demo Standard Script | Markdown | Standardize demo process |
| FAQ Handbook | Markdown | Handle 90% of customer questions |
| ROI Calculator | Excel | Help customers do the math |
| Customer Success Cases | PPT/PDF | Build trust |
| Technical Whitepaper | PDF | Deep understanding for technical customers |
| Objection Handling Handbook | Markdown | Handle rejections and doubts |

---

### Stage 12: Operations & Iteration

**Role Hat: Customer Success Partner + Product Evangelist**

#### B2B Customer Lifecycle Management

```
Acquisition → Onboarding → Adoption → Value → Expansion → Renewal/Advocacy
  ↑                                                          ↓
  └────────────────── Continuous Feedback Loop ──────────────────────────┘
```

#### Customer Health Score Model

```
Customer Health Score = 
  Product Usage Depth × 0.30 +
  Key Person Activity × 0.20 +
  NPS/CSAT × 0.15 +
  Ticket Frequency (inverse) × 0.15 +
  Upsell Signals × 0.10 +
  Contract Remaining Time × 0.10

Red/Yellow/Green Thresholds:
- Green (>75): Healthy, maintain regular rhythm
- Yellow (50-75): Warning, CSM proactively intervenes
- Red (<50): High risk, escalate, develop rescue plan
```

#### B2B Product Operations Framework

```
Product Operations 4 Modules:
├── Customer Operations: Onboarding → Adoption → Regular value review → Renewal
├── Feature Operations: Feature usage analysis → Low adoption investigation → Training/optimization → Deprecation
├── Content Operations: Help docs/Best practices/Product blog/Training videos
└── Data Operations: Metric monitoring → Anomaly alerts → Data insights → Drive iteration
```

---
