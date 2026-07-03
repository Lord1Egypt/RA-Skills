# B2B Product Requirements Document (PRD) Standard Template

> Version: V1.0 | Applicable: SaaS / Enterprise Software / Middle Platform / Backend Systems

---

## Document Information

| Field | Content |
|------|------|
| Document Name | [Product/Feature Name] Product Requirements Document |
| Document Version | V[1.0] |
| Creation Date | [YYYY-MM-DD] |
| Author | [Name] |
| Status | ⬜ Draft / 📝 Under Review / ✅ Finalized |
| Related Documents | BRD-[xxx] / MRD-[xxx] |

### Version History

| Version | Date | Modified By | Changes |
|------|------|--------|---------|
| V1.0 | YYYY-MM-DD | [Name] | Initial version |

---

## 1. Requirement Background & Business Objectives

### 1.1 Requirement Background
- **Business Background**: [Why do this now? Industry trends? Customer demands? Competitive pressure?]
- **Problem Description**: [What is the current problem? Who is affected? How severe is the impact?]
- **Opportunity Description**: [What value will solving this problem bring?]

### 1.2 Business Objectives

| Objective Dimension | Metric | Current Value | Target Value | Timeframe |
|---------|------|--------|--------|---------|
| Revenue | ARR / Contract Value | - | - | QX |
| Customer | Active Customers / Adoption Rate | - | - | QX |
| Efficiency | User Operation Time Reduction | - | - | QX |
| Quality | Error Rate / Ticket Volume Decrease | - | - | QX |

### 1.3 Product One-Liner
> [Role] can achieve [Value] through [Feature], without needing [Current Pain Point / Alternative Solution]

---

## 2. User Roles & Permission Matrix

### 2.1 Involved Roles

| Role | Responsibility Description | Usage Frequency | Focus Areas |
|------|---------|---------|--------|
| [Super Admin] | System configuration, organization management | Low | Security / Compliance / Global Control |
| [Regular Admin] | Daily management operations | Medium | Efficiency / Batch Operations |
| [Business Operator] | Daily business operations | High | Operation Efficiency / Ease of Onboarding |
| [Approver] | Process approval | Low | Approval Efficiency / Risk Control |
| [Viewer] | Read-only access | Medium | Data Accuracy / Report Display |

### 2.2 Permission Matrix

| Feature Module | Super Admin | Regular Admin | Operator | Approver | Viewer |
|---------|-----------|-----------|--------|--------|--------|
| View List | ✅ | ✅ | ✅ (Own Dept) | ✅ | ✅ (Own Dept) |
| Create | ✅ | ✅ | ✅ | ❌ | ❌ |
| Edit | ✅ | ✅ | ✅ (Self-created) | ❌ | ❌ |
| Delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| Batch Import | ✅ | ✅ | ❌ | ❌ | ❌ |
| Data Export | ✅ | ✅ (Own Dept) | ❌ | ❌ | ❌ |
| Approve | - | - | - | ✅ | - |

### 2.3 Data Permission Policy

| Data Scope | Rule | Applicable Roles |
|---------|------|---------|
| All Data | View data across all organizations/departments | Super Admin |
| Own Dept & Subordinates | View data of own department and all sub-departments | Dept Admin |
| Own Only | View only data created/owned by self | Regular Operator |
| Specified Scope | Configured via data permission settings | Custom Roles |

---

## 3. Core Business Processes

### 3.1 Business Process Flow (Swimlane Diagram)

> Insert draw.io swimlane diagram here, showing the complete cross-role business process.
> Includes: Normal Flow + Exception Branches + Approval Nodes + Notification Triggers

```
Swimlane Roles:
├── Initiator: [Initiate] → [Fill In] → [Submit] → [Wait for Approval] → [View Result]
├── Approver: [Receive Notification] → [View Details] → [Approve / Reject] → [Fill in Comments]
├── System: [Validate] → [Generate Order No.] → [Route Node] → [Send Notification] → [Archive]
└── Admin: [Configure Rules] → [Monitor Routing] → [Exception Handling]
```

### 3.2 Key Business Rules

| Rule No. | Rule Description | Trigger Condition | Execution Action |
|---------|---------|---------|---------|
| BR-001 | [Rule Name] | [Condition] | [Action] |
| BR-002 | [Rule Name] | [Condition] | [Action] |

---

## 4. Detailed Feature Description

### 4.1 Feature Architecture Diagram

> Insert feature architecture diagram (draw.io), showing all feature modules involved in this requirement and their relationships

### 4.2 Feature Module 1: [Module Name]

#### 4.2.1 Feature Overview
[One-liner describing what this module does]

#### 4.2.2 Prototype / Wireframe
> Insert prototype screenshot or wireframe here

#### 4.2.3 Page Element Description

**List Page:**

| Element | Type | Description |
|------|------|------|
| Search Box | Input | Supports fuzzy search by [Field1/Field2], real-time search |
| Status Filter | Multi-select Dropdown | Enum values: Pending Submission / Under Approval / Approved / Rejected |
| Date Range | Date Picker | Default: last 30 days |
| Create Button | Primary Button | Permission-controlled: visible only to [Role] |
| Batch Operations | Dropdown Menu | Batch Delete / Batch Export, activated after selection |
| Data Table | Table | Columns: [Field1 / Field2 / ... / Actions] |
| Paginator | Pagination | Default 20/page, options: 10/20/50/100 |

**Form Page (Create / Edit):**

| Field Name | Type | Required | Validation Rule | Default Value | Description |
|--------|------|------|---------|--------|------|
| [Field1] | Text Input | Yes | Max 50 characters | - | Name |
| [Field2] | Dropdown Select | Yes | Enum values | First | Type |
| [Field3] | Date Picker | No | Not earlier than today | Today | Date |
| [Field4] | Number Input | No | 0-99999999 | 0 | Amount |
| [Field5] | File Upload | No | PDF/Word ≤10MB | - | Attachment |

**Detail Page:**

| Section | Content | Description |
|------|------|------|
| Basic Info | [Field List / Values] | Read-only display |
| Related Info | [Related Orders / Related Customers] | Clickable links |
| Operation History | [Timeline] | Who + When + What |
| Attachments | [File List] | Preview / Download |

#### 4.2.4 Interaction Description

| Operation | Precondition | Interaction Flow | Exception Handling |
|------|---------|---------|---------|
| Create | Has create permission | Click Create → Form pops up → Fill in → Submit | Validation fails → Red highlight hint |
| Edit | Has edit permission + Status allows | Click Edit → Form pre-filled → Modify → Submit | Modified by others → Prompt to refresh |
| Delete | Has delete permission + Status allows | Click Delete → Confirm dialog → Execute | Has related data → Show deletion prohibited message |
| Batch Operation | At least 1 item selected | Select → Choose operation → Confirm → Execute | Partial failure → List failure details |

#### 4.2.5 Status Description

| Status | Display Style | Trigger Condition | Available Actions |
|------|---------|---------|-----------|
| Pending Submission | Gray tag | New / Draft | Edit / Submit / Delete |
| Under Approval | Blue tag + Progress | After submission | Withdraw / Remind / View |
| Approved | Green tag | Last node approved | View / Related Operations |
| Rejected | Red tag + Rejection reason | Any node rejected | Edit / Resubmit / Delete |

---

## 5. Approval Flow & Workflow Design

### 5.1 Approval Process

```
[Submit Application] → [Dept Head Approval] → [Finance Approval (Amount > 5000)] → [GM Approval (Amount > 50000)] → [Complete]
                                     ↓ (Reject)                  ↓ (Reject)
                                  [Return to Initiator]          [Return to Initiator]
```

### 5.2 Approval Node Configuration

| Node | Approver Determination | Approval Rule | Timeout Handling |
|------|--------------|---------|---------|
| Dept Head | Applicant's direct manager | Default approve | Auto-remind after 48h timeout |
| Finance Approval | Designated role: Finance Approver | Auto-skip if amount ≤5000 | Escalate to Finance Director after 24h timeout |
| GM Approval | Designated position: General Manager | Auto-skip if amount ≤50000 | Auto-remind after 72h timeout |

### 5.3 Approval Operations

| Operation | Description | Permission |
|------|------|------|
| Approve | Route to next node | Current node approver |
| Reject | Return to initiator; can specify which node to reject back to | Current node approver |
| Transfer | Transfer to another person for approval | Current node approver |
| Countersign | Add additional approver (before / after) | Current node approver |
| Withdraw | Initiator withdraws application | Initiator (only during approval) |
| Remind | Send reminder notification | Initiator |

### 5.4 State Machine Diagram

> Insert approval flow state machine diagram (draw.io) here

```
Draft → Under Approval ⇄ Rejected
Under Approval → Approved
Under Approval → Withdrawn
Approved → Voided (Admin)
```

---

## 6. Data Model Design

### 6.1 ER Diagram

> Insert Entity-Relationship diagram (draw.io), marking core entities, fields, and relationship types

### 6.2 Data Dictionary

**Table 1: [Table Name]**

| Field Name | Field Code | Type | Length | Required | Default Value | Description |
|--------|---------|------|------|------|--------|------|
| ID | id | bigint | - | Yes | Auto-increment | Primary Key |
| Name | name | varchar | 100 | Yes | - | - |
| Type | type | varchar | 20 | Yes | 'default' | See enum appendix |
| Amount | amount | decimal | 18,2 | No | 0.00 | Unit: Yuan |
| Status | status | varchar | 20 | Yes | 'draft' | See status enum |
| Creator | creator_id | bigint | - | Yes | - | FK → user.id |
| Created At | created_at | datetime | - | Yes | now() | - |
| Updated At | updated_at | datetime | - | Yes | now() | - |
| Tenant ID | tenant_id | bigint | - | Yes | - | Multi-tenant isolation |

### 6.3 Enum Value Definitions

| Enum Field | Enum Value | Description |
|---------|--------|------|
| status | draft | Draft |
| status | pending_approval | Pending Approval |
| status | approved | Approved |
| status | rejected | Rejected |
| status | cancelled | Voided |

---

## 7. Integration & API Requirements

### 7.1 Internal System Integration

| Integration System | Integration Method | Integration Content | Priority |
|---------|---------|---------|--------|
| User Center | API / SSO | User info / Org structure / Permissions | P0 |
| Notification Center | MQ / API | Approval notifications / System notifications | P0 |
| File Storage | SDK / API | Attachment upload / Preview / Download | P0 |
| Data Platform | ETL | Event tracking data / Business data sync | P2 |

### 7.2 External System Integration

| Integration System | Integration Method | Integration Content | Priority |
|---------|---------|---------|--------|
| WeCom / DingTalk / Feishu / Lark | API | Message notifications / Approval integration / Org sync | P0 |
| SSO (LDAP / OAuth / SAML) | Standard Protocol | Identity authentication | P1 |
| E-Signature | API | Contract / Document signing | P1 |
| Enterprise Payment | API | Corporate payment / Reimbursement | P2 |
| E-Invoice | API | Invoice issuance / Verification | P2 |

### 7.3 OpenAPI Definition (if applicable)

| API Name | Method | Path | Description | Auth Method |
|---------|--------|------|------|---------|
| Query List | GET | /api/v1/[resources] | Paginated query | Bearer Token |
| Query Detail | GET | /api/v1/[resources]/{id} | Single record query | Bearer Token |
| Create | POST | /api/v1/[resources] | Create new | Bearer Token |
| Update | PUT | /api/v1/[resources]/{id} | Full update | Bearer Token |
| Delete | DELETE | /api/v1/[resources]/{id} | Logical delete | Bearer Token |

---

## 8. Non-Functional Requirements

### 8.1 Performance Requirements

| Metric | Requirement | Description |
|------|------|------|
| Page Load | P95 < 2s | First screen load with data |
| List Query | P95 < 500ms | Within 1000 records |
| Form Submit | P95 < 1s | Including validation |
| Export | Support 100K records/time | Async export + progress indicator |
| Concurrency | Support 500 concurrent users | Estimated from operational data |

### 8.2 Security Requirements

| Requirement | Description |
|------|------|
| Authentication | Support SSO + Username/Password + SMS Verification Code |
| Authorization | RBAC, Principle of Least Privilege |
| Transport Encryption | HTTPS site-wide |
| Storage Encryption | AES-256 encryption for sensitive fields (phone / ID card / bank card) |
| Audit Log | Record all CUD operations, non-deletable |
| Data Masking | Mask phone / ID card / bank card numbers on display |
| Anti-Replay | Verification token required for critical operations (approval / payment / delete) |

### 8.3 Availability Requirements

| Metric | Target |
|------|------|
| Service Availability | 99.9% (monthly) |
| Data Backup | Daily full + Every 6 hours incremental |
| Disaster Recovery | RPO < 1h, RTO < 4h |

### 8.4 Scalability Requirements

| Dimension | Requirement |
|------|------|
| Tenant Count | Initially support 100 tenants, scalable to 10,000+ |
| Data Volume | Single table support 100M+ records, reserve sharding strategy |
| Configurability | Tenant-level: Logo / Theme / Custom Fields / Workflow / Reports |

---

## 9. Acceptance Criteria

### 9.1 Functional Acceptance

| No. | Acceptance Item | Acceptance Criteria | Test Role |
|------|--------|---------|---------|
| AC-001 | List Query | Each role views per data permissions; pagination/search/filter work correctly | All |
| AC-002 | Create Data | Required field validation & format validation correct; status correct after submission | Operator |
| AC-003 | Approval Flow | Each node routes correctly; initiator can modify and resubmit after rejection | Approver |
| ... | ... | ... | ... |

### 9.2 Non-Functional Acceptance

| No. | Acceptance Item | Acceptance Criteria |
|------|--------|---------|
| NAC-001 | Performance | Meet performance metrics in section 8.1 |
| NAC-002 | Security | Pass security scan, no high-risk vulnerabilities |
| NAC-003 | Compatibility | Chrome / Firefox / Edge / Safari mainstream versions |
| NAC-004 | Mobile | Approval operations adapted for mobile H5 |

---

## 10. Appendix

### 10.1 Glossary

| Term | Description |
|------|------|
| [Term1] | [Definition] |

### 10.2 Reference Documents

| Document | Link |
|------|------|
| BRD | [Link] |
| Technical Proposal | [Link] |
| Design Mockups | [Link] |

### 10.3 Pending Confirmation Items

| No. | Question | Owner | Deadline | Status |
|------|------|--------|---------|------|
| Q-001 | [Question to confirm] | [Name] | YYYY-MM-DD | Pending |

---

## v1.1.0 New: SaaS Pricing Model & PLG Elements

### Pricing Model Design (Seven-Step Pricing Process)
| Step | Content | Output |
|------|------|------|
| 1. Value Quantification | How much money can customers save/earn using the product? | Value Quantification Table |
| 2. Pricing Dimensions | By usage (API calls / Storage / Users) or by feature complexity? | Pricing Dimension Matrix |
| 3. Competitive Benchmarking | How do competitors price? Where is the price anchor? | Competitive Price Comparison |
| 4. Plan Design | What does Free / Starter / Pro / Enterprise each include? | Plan Comparison Table |
| 5. Price Anchoring | Which plan is the "anchor"? Which is the "profit center"? | Price Psychology Strategy |
| 6. Trial Conversion | Free trial → Paid conversion path design | Conversion Funnel Design |
| 7. Pricing Test | A/B test conversion rates at different price points | Pricing Experiment Plan |

### PLG (Product-Led Growth) Elements
| Element | Design Key Points | Metric |
|------|---------|------|
| Free Experience | Experience core value within 5 minutes of signup | Time-to-Value < 5min |
| Viral Spread | Collaboration / Sharing features naturally bring new users | Viral Coefficient > 1.0 |
| Self-Service Upgrade | Auto-prompt upgrade when usage hits threshold | Upgrade Conversion Rate > 5% |
| In-Product Education | Guided onboarding replaces training videos | Activation Rate > 60% |
| Data-Driven | Optimize product based on usage behavior data | Retention Rate > 40% (M1) |