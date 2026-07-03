# PRD Example: Enterprise Procurement Management Module

> This is a complete B2B PRD example demonstrating documentation in a real-world context

## Document Information

| Field | Content |
|------|------|
| Document Name | Enterprise Procurement Management Module PRD |
| Version | V1.0 |
| Date | 2026-06-07 |
| Author | Product Manager - Zhang Ming |
| Status | 📝 Under Review |
| Related Documents | BRD - Enterprise Procurement Platform V2.0 |

---

## 1. Background & Goals

### 1.1 Requirement Background

During the on-premise deployment for XX Group, the client explicitly pointed out the lack of procurement management functionality. Upon investigation, among the existing 30+ paying customers, 12 have directly mentioned procurement management needs, and 8 were lost to competitors due to the absence of a procurement module.

Internal product committee decision: Launch procurement management as the key Q3 module.

### 1.2 Business Goals

| Goal Dimension | Metric | Current Value | Target Value (Q4) |
|---------|------|--------|----------|
| Customers | Paying customers using procurement module | 0 | 15 |
| Revenue | Procurement module incremental revenue | ¥0 | ¥1.2M/year |
| Retention | Existing customer upsell rate | 0% | 30% |

### 1.3 Product in One Sentence

> Enterprise procurement staff can manage the full process — from purchase requisition → RFQ comparison → purchase order → receiving & warehousing → reconciliation & settlement — on a single platform, reducing the procurement cycle from an average of 15 days to 3 days, while ensuring every purchase is compliant and controllable.

---

## 2. User Roles & Permissions

### 2.1 Involved Roles

| Role | Description | Typical Position |
|------|------|---------|
| Purchase Requisitioner | Initiates procurement requests | Employees across departments |
| Procurement Officer | Executes procurement tasks | Procurement Department |
| Procurement Manager | Manages procurement team, approvals | Procurement Manager |
| Warehouse Administrator | Receiving & warehousing | Warehouse Keeper |
| Finance | Reconciliation & settlement | Finance/Accounting |
| Administrator | System configuration | IT/System Administrator |

### 2.2 Permission Matrix (Simplified; full version in Excel)

| Action | Requisitioner | Procurement Officer | Procurement Manager | Warehouse | Finance | Admin |
|------|----------|--------|---------|------|------|--------|
| My Requests | ✅CRUD | ✅R | ✅R | ❌ | ❌ | ✅ALL |
| Purchase Order Management | ❌ | ✅CRUD (own) | ✅CRUD (dept) | ✅R | ✅R | ✅ALL |
| RFQ Comparison | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Receiving & Warehousing | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Reconciliation & Settlement | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Supplier Management | ❌ | ✅R | ✅CRUD | ❌ | ✅R | ✅ALL |
| Approval | - | - | ✅ | - | - | Config |

---

## 3. Core Business Process

### 3.1 Procurement Full Process (Swimlane Diagram)

```
Requisitioner → Procurement Officer → Procurement Manager → Supplier → Warehouse → Finance
    │          │         │         │       │      │
    ├─Create Request─┤         │         │       │      │
    │          ├─Approve──→         │       │      │
    │          │   ←──Approve/Reject──        │       │      │
    │          ├─RFQ Comparison──→       │       │      │
    │          │   ←──Quotation──          │       │      │
    │          ├─Generate PO──→             │       │      │
    │          │   ←──Confirm Order──────────→│       │      │
    │          │         │         ├─Ship──→       │      │
    │          │         │         │       ├─Receive & Warehouse─┤
    │          │         │         │       │   QC  │
    │          ├─Reconciliation─────────────────────────────→│
    │          │         │         │       │   ├─Settle─┤
    │          │         │         │       │   │ Payment │
```

### 3.2 Key Business Rules

| Rule ID | Description |
|--------|------|
| BR-001 | Purchase amount > ¥5,000 requires at least 3 supplier quotations |
| BR-002 | Single transaction > ¥50,000 requires GM countersignature |
| BR-003 | Quantity deviation > 5% at receiving triggers system alert and blocks warehousing |
| BR-004 | Suppliers on the supplier blacklist cannot participate in RFQ |
| BR-005 | Contract payment ratio and amount must not exceed the total contract value |

---

## 4. Detailed Feature Description

### 4.1 Feature Architecture

```
Procurement Management Module
├── Purchase Requisition
│   ├── My Requests (List/New/View/Withdraw)
│   ├── Request Approval (Pending/Reviewed)
│   └── Request Templates (Common procurement item templates)
├── Procurement Execution
│   ├── Purchase Order Management (Pending/In Progress/Completed)
│   ├── RFQ Comparison (Initiate RFQ/Quotation Comparison/Comparison Report)
│   └── Order Tracking (Shipping/Logistics/ETA)
├── Supplier Management
│   ├── Supplier Database (List/Details/Evaluation/Blacklist)
│   ├── Supplier Onboarding (Registration/Audit/Qualification Management)
│   └── Supplier Performance (Rating/Transaction Records/Adverse Records)
├── Receiving & Warehousing
│   ├── Receiving Note (Pending/Received)
│   ├── Quality Inspection (Pass/Fail/Concession Acceptance)
│   └── Warehouse Confirmation (Auto-generate inventory records)
└── Reconciliation & Settlement
    ├── Reconciliation Statement (Generate/Confirm/Discrepancy Handling)
    ├── Payment Plan (By Contract/By Milestone)
    └── Invoice Management (Registration/Verification/Deduction)
```

### 4.2 Core Page: Purchase Requisition List

**Page Layout:**
```
┌──────────────────────────────────────────────────────┐
│ Purchase Requisitions                                     │
│                                                        │
│ [Search Request No./Name...]  [Status▼] [Date Range▼]  [Search]  │
│                                                        │
│ [New Request] [Batch Submit]                            │
│                                                        │
│ ☐ | Request No.       | Title            | Amount  | Status   | Requester | Date  │
│ ☐ | PR20260607001     | Office Computers | ¥50,000 | Pending  | Li Si     | 06-07 │
│ ☐ | PR20260607002     | Printer Paper    | ¥500    | Approved | Wang Wu   | 06-07 │
│ ☐ | PR20260606001     | Server Expansion | ¥80,000 | Rejected | Zhao Liu  | 06-06 │
│                                                        │
│ 2 selected [Batch Submit]       128 total  < 1 2 3 ... 7 >  │
└──────────────────────────────────────────────────────┘
```

**Field Descriptions:**

| Field | Type | Required | Validation | Notes |
|------|------|------|------|------|
| Request Title | Text | Yes | 2-100 chars | Brief description of procurement item |
| Procurement Type | Dropdown | Yes | Enumerated values | Office Supplies/IT Equipment/Services/Raw Materials/Other |
| Purchase Amount | Number | Yes | 0.01-99999999.99 | Estimated amount for approval submission |
| Requesting Department | Dropdown | Yes | Linked to org structure | Default: current user's department |
| Expected Delivery Date | Date | No | ≥ Today | |
| Purchase Details | Table | Yes | At least 1 row | Name/Spec/Qty/Unit Price/Total |
| Request Reason | Textarea | Yes | 10-500 chars | Explain procurement necessity |
| Attachments | File | No | ≤10MB×3 | Quotations/Contracts/Approval documents |

**Interaction Rules:**
- New Form: Opens full-screen/side panel form, with "Basic Info" and "Purchase Details" as two steps
- Save Draft: All fields can be empty, skip validation
- Submit: Execute full validation; upon passing, generate request number and enter approval workflow
- Withdraw: Only "Pending Approval" status can be withdrawn; returns to "Draft" after withdrawal

### 4.3 Core Page: RFQ Comparison

**Feature Description:**
The procurement officer initiates RFQs to multiple suppliers, collects quotations, performs comparison analysis, and selects the optimal supplier.

**RFQ Form Fields:**

| Field | Description |
|------|------|
| RFQ Items | Auto-populated from purchase requisition, can be added/removed |
| RFQ Suppliers | Selected from supplier database, minimum 2, must be non-blacklisted |
| RFQ Deadline | Suppliers must submit quotations before this time |
| Quotation Notes | Supplementary requirements for suppliers |

**Comparison Report:**

| Dimension | Supplier A | Supplier B | Supplier C |
|------|--------|--------|--------|
| Total Quotation | ¥48,500 | ¥51,000 | ¥47,200 |
| Delivery Cycle | 7 days | 5 days | 10 days |
| Payment Method | Payment on delivery | 30% advance | Monthly settlement |
| Historical Rating | 4.5/5 | 4.2/5 | 4.8/5 |
| Overall Recommendation | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

**Post-Selection Flow:** Select supplier → System auto-generates purchase order → Procurement manager approval → Send to supplier for confirmation

---

## 5. Approval Workflow Design

### Purchase Requisition Approval Flow

```
[Submit Request] 
    → [Department Head Approval] (Mandatory)
        → [Procurement Manager Approval] (Mandatory)  
            → [Finance Approval] (Triggered when amount > ¥5,000)
                → [GM Approval] (Triggered when amount > ¥50,000)
                    → [Complete, generate purchase order]
```

### Approval Rules

| Node | Approver | Timeout | Available Actions |
|------|--------|------|-----------|
| Department Head | Requester's direct manager | 48h reminder | Approve/Reject/Forward |
| Procurement Manager | Procurement manager role | 24h reminder | Approve/Reject/Forward/Countersign |
| Finance Approval | Finance approval role | 24h escalation | Approve/Reject |
| GM | GM role | 72h reminder | Approve/Reject |

---

## 6. Data Model (Core Tables)

### Purchase Requisition Table (t_purchase_request)

| Field | Type | Required | Description |
|------|------|------|------|
| id | bigint | Yes | Primary key |
| request_no | varchar(32) | Yes | Request number, PR+date+sequence |
| title | varchar(100) | Yes | Request title |
| type | varchar(20) | Yes | Procurement type |
| total_amount | decimal(18,2) | Yes | Estimated total amount |
| dept_id | bigint | Yes | Requesting department ID |
| expected_date | date | No | Expected delivery date |
| reason | varchar(500) | Yes | Request reason |
| status | varchar(20) | Yes | draft/pending/approved/rejected/cancelled |
| process_instance_id | varchar(64) | No | Approval workflow instance ID |
| creator_id | bigint | Yes | Creator |
| tenant_id | bigint | Yes | Tenant ID |
| created_at | datetime | Yes | Creation time |
| updated_at | datetime | Yes | Update time |
| deleted_at | datetime | No | Soft delete time |

### Purchase Requisition Items Table (t_purchase_request_item)

| Field | Type | Description |
|------|------|------|
| id | bigint | Primary key |
| request_id | bigint | FK to purchase requisition |
| item_name | varchar(200) | Item name |
| spec | varchar(200) | Specification/Model |
| quantity | int | Quantity |
| unit | varchar(20) | Unit |
| unit_price | decimal(18,2) | Estimated unit price |

---

## 7. Non-Functional Requirements

| Category | Metric | Target |
|------|------|------|
| Performance | Purchase list loading | P95 < 1s (within 1000 records) |
| Performance | Comparison report generation | P95 < 3s |
| Security | Amount fields | Encrypted in transit, not encrypted at rest (audit requirement) |
| Audit | Key operations | CUD operations recorded in audit log, immutable |
| Notifications | Approval node changes | In-app + WeCom/DingTalk notification, delivered within 5 minutes |

---

## 8. Acceptance Criteria (Excerpt)

| No. | Acceptance Item | Acceptance Criteria |
|------|--------|---------|
| AC-001 | Purchase requisition submission | All required fields filled, submission succeeds, approval workflow starts |
| AC-002 | Comparison report | At least 2 suppliers selected, comparison table auto-generated |
| AC-003 | Amount > ¥5,000 triggers finance approval | Finance receives approval notification, can approve |
| AC-004 | Amount ≤ ¥5,000 skips finance approval | Completes directly after procurement manager approval, no finance node |
| AC-005 | Supplier blacklist | Blacklisted suppliers not selectable in RFQ list |
| AC-006 | Receiving quantity deviation | Deviation > 5% triggers system alert, blocks warehouse confirmation |
| AC-007 | Audit log | All CUD operations queryable in audit log, cannot be deleted |

---

## 9. Version Plan

| Version | Scope | Goal |
|------|------|------|
| V1.0 (MVP) | Purchase requisition + Approval workflow + Purchase orders + Basic supplier database | 3 beta customers go-live |
| V1.1 | RFQ comparison + Comparison report | Quantifiable procurement efficiency improvement |
| V1.2 | Receiving & warehousing + Quality inspection | Full process closed loop |
| V2.0 | Reconciliation & settlement + Invoice management | Business-finance integration |

---

> **Example Note**: This is a simplified PRD example. In practice, supplement with more detail based on product complexity.
> A complete PRD would also include: interaction design mockups, frontend state machines, detailed API definitions, test cases, etc.


---

## v1.1.0 Added: Pricing Considerations

### ERP Procurement System Pricing Model
| Pricing Dimension | Plan | Description |
|---------|------|------|
| Base Pricing | Per user | Procurement officers + Approvers + Administrators |
| Usage Pricing | Per purchase order | Monthly orders < 1000 / 1000-5000 / > 5000 |
| Feature Pricing | Basic/Professional/Enterprise | Approval workflow / Supplier management / Data analytics |
| Plan Design | Starter (¥99/mo) / Pro (¥299/mo) / Enterprise (Custom) | By team size + feature tier |

### PLG Growth Strategy (ERP Procurement System)
| Strategy | Plan | Expected Effect |
|------|------|---------|
| Free Trial | 14-day full-feature trial | Conversion rate > 5% |
| Viral Growth | Supplier collaboration invites | Each invited supplier = 1 new lead |
| Self-Service Onboarding | 5-minute import template | Activation rate > 50% |
| Content Marketing | Procurement best practices blog | SEO traffic growth |