#!/usr/bin/env python3
"""Write chunk 2: Stage 4 Solution Design (7 Pillars)"""
DEST = "/Users/macos/Desktop/【0616 skill升级工程】/international/b2b-pm-workbench-international/SKILL.md"

chunk2 = """### Stage 4: Solution Design (B2B Core)

**Role Hat: Solution Architect + Process Designer**

> This is the most core, most depth-demonstrating stage for B2B PMs.
> Solution design determines not just "what features to build" but "how the organization operates."
> Reference: Yang Kun's "Mastering B2B" five-module knowledge system: Business Diagnosis → Solution Design → Management Implementation → Architecture Advancement → Capability Growth.

#### B2B Solution Design — 7 Pillars

---

##### Pillar 1: Multi-Role Permission Model Design

**Three Permission Model Options:**

| Model | Description | Pros | Cons | Use Case |
|-------|-------------|------|------|----------|
| **RBAC** | Role-Based Access Control | Simple, intuitive, standard | Not flexible enough | 90% of enterprise scenarios |
| **ABAC** | Attribute-Based Access Control | Flexible, granular | Complex, performance overhead | High security / compliance scenarios |
| **ReBAC** | Relationship-Based Access Control | Social / hierarchical scenarios | Complex implementation | Org hierarchy / approval chains |

**RBAC Design Steps (5-Step Method):**

```
Step 1: Enumerate all operations (pages / buttons / APIs / data scopes)
Step 2: Define roles (start from org structure, not technical)
  ├── Super Admin - Global configuration, org management
  ├── System Admin - Daily management, user permissions
  ├── Department Admin - Department-level management
  ├── Business Operator - Core business operations
  ├── Approver - Process approval
  ├── Auditor - Read-only + log viewing
  └── Custom Roles - Allow tenant customization
Step 3: Role-Operation mapping (permission matrix)
Step 4: User-Role binding (support one user, multiple roles)
Step 5: Data permission policy overlay (row-level / column-level)
```

**Permission Granularity Hierarchy:**
```
Menu Level → Page Level → Button Level → Data Level (Row) → Data Level (Column) → Field Level
    ↓           ↓            ↓               ↓                   ↓                  ↓
  Which menus  Which pages  Which buttons  Which data          Which fields       Which fields
  are visible  are accessible are operable  ranges are visible  are visible        are editable
```

**Data Permission Policies:**

| Policy | Rule | Suitable Roles |
|--------|------|----------------|
| All Data | No restrictions | Super Admin |
| Own Dept & Subordinates | dept_path LIKE 'xxx%' | Department Admin |
| Own Only | creator_id = current_user_id | Regular Operator |
| Specified Scope | Via data permission config table | Custom Roles |
| Same Org | tenant_id = current_tenant_id | All Roles (baseline) |

**Output:** Role-Permission Matrix (Excel) + Data Permission Policy Document

---

##### Pillar 2: Approval Workflow & Workflow Design (BPMN 2.0)

**Complete Approval Node Type Catalog:**

| Node Type | Description | Example |
|-----------|-------------|---------|
| **Manual Approval** | Designated person / role / position approves | Department Manager Approval |
| **Auto-Approval** | Auto-pass when conditions met | Amount < $500 auto-approve |
| **Conditional Branch** | Different branches based on conditions | Amount > $5,000 goes to Finance Approval |
| **Countersign** | All must approve to pass | All VPs agree |
| **Or-Sign** | Any one approves to pass | On-duty approval |
| **Escalation Approval** | Escalate up org hierarchy | Team Lead → Manager → Director → VP |
| **Transfer** | Transfer to another approver | When approver is unavailable |
| **Add Approver** | Add extra approver | Need additional legal confirmation |
| **CC** | Notify but don't participate in approval | Inform relevant departments |
| **Withdraw** | Initiator withdraws | Discover error after submission |
| **Reject** | Reject (reject to where?) | Initiator / Previous Node / Specified Node |

**Approval Efficiency Design Principles:**

```
1. Approval nodes ≤ 5 (must justify if more)
2. Approvers per node ≤ 3
3. Must have timeout strategy (remind / escalate / auto-approve / auto-reject)
4. Mobile approval is mandatory (Slack / Teams / WeCom / DingTalk / Lark integration)
5. Approval detail page includes: full info + approval history + action buttons + attachments
6. Support batch approval (one-click for similar requests)
7. Approver view: Pending Approval list + Approved list
8. Initiator view: My Requests + Approval Progress + Withdraw / Remind
```

**Exception Flow Handling (The Most Overlooked B2B Area!):**

| Exception Scenario | Handling Strategy |
|-------------------|-------------------|
| Approver resigned / transferred | Auto-transfer to superior or delegate approver |
| Approval timeout | Remind (24h) → Escalate (48h) → Auto-approve/reject (72h) |
| Approver is the initiator | Auto-skip that node |
| Org structure change mid-process | Use org structure at time of initiation |
| Concurrent approval conflict | First-come-first-served, notify the latter |
| Approval system downtime | Auto-recover flow after state restoration |

**State Machine Diagram (Core Deliverable):**
Use draw.io to draw complete state machine, including entry/exit conditions and executable operations for all states.

**Output:** Approval Flow State Machine Diagram (draw.io) + Approval Rule Configuration Table (Excel) + Exception Scenario Handling Table

---

##### Pillar 3: Multi-Tenant Architecture Design

**Four Isolation Strategies & Decision Matrix:**

| Strategy | Isolation Strength | Cost | Implementation Complexity | Use Case |
|----------|-------------------|------|--------------------------|----------|
| **Database per Tenant** | ⭐⭐⭐⭐⭐ | Highest | Medium | Finance / Healthcare with strict compliance |
| **Schema per Tenant** | ⭐⭐⭐⭐ | High | Medium-High | Enterprise customers with customization needs |
| **Shared Table + tenant_id** | ⭐⭐ | Lowest | Low | Standardized SaaS, SMB customers |
| **Hybrid Model** | ⭐⭐⭐ | Medium-High | High | Enterprise separate + long-tail shared |

**Tenant Isolation Decision Tree:**
```
High compliance requirements? → Yes → Database per Tenant
                            → No → High customization needs? → Yes → Schema per Tenant
                                                           → No → Large customer volume? → Yes → Shared Table
                                                                                       → No → Hybrid
```

**Tenant-Level Configurable Items Checklist:**

| Config Category | Configurable Items | Implementation |
|----------------|-------------------|----------------|
| Branding | Logo / Theme Color / Name | Tenant config table |
| Organization | Department hierarchy / Positions / Roles | Tree configuration |
| Process | Approval rules / Process templates | Workflow engine config |
| Data | Custom fields / Numbering rules / Print templates | Extension fields + rule engine |
| Permissions | Custom roles / Data scopes | Permission engine |
| Reports | Custom reports / Dashboards | Report engine |
| Integration | SSO config / API Key / Webhook | Integration config |

**Output:** Multi-Tenant Architecture Design Document + Tenant Configuration Checklist

---

##### Pillar 4: Data Dictionary & Master Data Management (MDM)

**Data Dictionary Standard Template (One per Table):**

| Field Name | Field Code | Type | Length | Required | Default | Unique | Index | Enum Values | Validation Rules | Configurable | Description |
|------------|-----------|------|--------|----------|---------|--------|-------|-------------|-----------------|-------------|-------------|
| ID | id | bigint | - | Yes | auto | PK | - | - | - | No | Primary Key |
| Name | name | varchar | 100 | Yes | - | No | - | - | ≤100 chars | No | Name |
| Status | status | varchar | 20 | Yes | 'draft' | No | idx_status | See appendix | - | No | Status |
| Tenant ID | tenant_id | bigint | - | Yes | - | No | idx_tenant | - | - | No | Multi-tenant isolation |

**MDM Core Entities:**

B2B products must manage these master data:
- Organizational Structure (Company → Department → Position → Employee)
- Customer / Supplier Master Data
- Product / Material Master Data
- Account / Project / Cost Center
- Contract / License

**Database Naming Conventions:**
```
Table: t_{module_prefix}_{table_name}  →  e.g., t_pur_purchase_request
Column: snake_case                     →  e.g., created_at, creator_id
Index: idx_{column_name}               →  e.g., idx_tenant_id, idx_status
Unique Index: uk_{column_name}         →  e.g., uk_request_no
Foreign Key: fk_{table}_{column}       →  e.g., fk_user_creator_id
Boolean: is_xxx / has_xxx              →  e.g., is_deleted, has_attachment
Timestamp: xxx_at                      →  e.g., created_at, approved_at
Amount: xxx_amount (in cents)          →  e.g., total_amount → DECIMAL(18,0)
```

**Output:** Complete Data Dictionary (Excel) + ER Diagram (draw.io)

---

##### Pillar 5: Integration & Open API Design

**Enterprise Integration Patterns (EIP) Selection Guide:**

| Integration Pattern | Real-time | Coupling | Use Case |
|--------------------|-----------|----------|----------|
| File Transfer (SFTP) | Low | Low | Batch data sync, reconciliation |
| RESTful API | High | Medium | Standard integration, external exposure |
| Message Queue (MQ) | High | Low | Async decoupling, event-driven |
| Webhook | High | Medium-Low | Event push, notifications |
| gRPC | High | High | Internal microservices |
| Shared Database | Highest | Highest | Legacy system integration (not recommended) |

**Enterprise Integration Maturity Ladder:**

```
L1: File Import/Export (CSV/Excel)           ← MVP must reach at least this level
L2: Webhook + Message Notifications          ← GTG stage reaches this level
L3: RESTful API (with API documentation)     ← Required for scale
L4: SSO + Org Structure Sync                 ← Standard for enterprise customers
L5: Deep Integration (bidirectional sync + embedded components)  ← Industry-leading solution
```

**Must-Support Integration Checklist:**
- SSO / Identity: SAML 2.0, OAuth 2.0/OIDC, LDAP/Active Directory, CAS
- Messaging: Slack / Teams / WeCom / DingTalk / Lark, Email (SMTP), SMS
- E-Signature: DocuSign / HelloSign / Adobe Sign
- Enterprise Payment: ACH / Wire Transfer / Supply Chain Finance
- E-Invoicing: E-invoice platform integration
- Data Integration: ETL / Data Sync / Master Data Distribution

**OpenAPI Design Standards (if product offers an open platform):**

| Element | Standard |
|---------|----------|
| Versioning | URL path versioning: /api/v1/ |
| Authentication | Bearer Token + API Key + App Secret |
| Rate Limiting | Token bucket algorithm, per API Key |
| Documentation | OpenAPI 3.0 spec, Swagger auto-generated |
| Error Codes | Unified 4-digit error code + message + details |
| Pagination | pageNum + pageSize, return total |
| Format | JSON, UTF-8 encoding |

**Output:** Integration Architecture Diagram (draw.io) + API Design Document

---

##### Pillar 6: Compliance & Audit Design

**Compliance Frameworks B2B Products Must Consider:**

| Standard / Regulation | Applicable Domain | Core Requirements |
|----------------------|-------------------|-------------------|
| **SOC 2 Type II** | SaaS (Global) | Security / Availability / Processing Integrity / Confidentiality / Privacy — Five Trust Services |
| **GDPR** | EU user data | Data subject rights, DPO, cross-border data transfer restrictions |
| **ISO 27001** | General Information Security | ISMS framework, risk assessment, continuous improvement |
| **HIPAA** | Healthcare (US) | PHI protection, BA agreements |
| **PCI DSS** | Payment card industry | Cardholder data protection |
| **CCPA/CPRA** | California consumer privacy | Consumer data rights, opt-out mechanisms |
| **FedRAMP** | US Federal Government cloud | Standardized security assessment for cloud services |
| **China Cybersecurity Law / MLPS 2.0** | Systems in China | 5-level protection, generally Level 3 for enterprises |
| **China PIPL** | Personal information in China | Notice-consent, sensitive info separate consent, data localization |
| **Xinchuang (IT Innovation)** | Chinese government / SOEs | Domestic CPU/OS/DB/Middleware adaptation |

**Audit Log Design Specification:**

```
Each audit log entry must contain:
├── Who (operator_id + operator_name + operator_role)
├── When (timestamp, millisecond precision)
├── What (action: CREATE/READ/UPDATE/DELETE/EXPORT/APPROVE)
├── On What (resource_type + resource_id + resource_name)
├── Before (before_snapshot, JSON)
├── After (after_snapshot, JSON)
├── From Where (IP + User-Agent + Session ID)
├── Result (success/failure + error_detail)
└── Audit log itself: immutable, non-deletable, no manual insertion
```

**Data Security Baseline:**
- Transport: HTTPS everywhere, API signing
- Storage: AES-256 encryption for sensitive fields, KMS key management
- Access: RBAC least privilege, IP whitelisting, login time restrictions
- Masking: Auto-mask phone/ID card/bank card numbers in display
- Backup: Daily full + incremental, offsite backup
- DR: RPO < 1h, RTO < 4h

---

##### Pillar 7: B2B Product Architecture Design

**Evolution Path from Monolith to Platform (Yang Kun Framework):**

```
Stage 1: Excel → Single System → Multiple Independent Systems → System Integration → Platformization
  │          │              │                              │                    │
  Startup    Growth         Expansion                      Maturity             Platform Era

Platform Architecture (Ultimate Form of Enterprise Products):
├── Business Platform: Reusable business capabilities (User/Permission/Approval/Notification/Payment/Signature)
├── Data Platform: Unified data assets (Master Data/Metrics System/Data Services/Data Governance)
├── Technical Platform: Technical infrastructure (Microservices/Containers/CI-CD/Monitoring/Logging)
└── Organizational Platform: Organizational capability accumulation (Methodology/Toolchain/Training System)
```

---

"""

with open(DEST, 'a', encoding='utf-8') as f:
    f.write(chunk2)

print(f"Chunk 2 appended: {len(chunk2)} chars")