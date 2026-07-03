# B2B Product Functional Requirements Document (FRD) Template

> The "technical translation" of PRD — development team can code directly from this

## Document Info

| Field | Content |
|------|------|
| Document Name | [Feature Module Name] FRD |
| Related PRD | PRD-[xxx] V[X.X] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |

---

## 1. Feature Overview

[Describe what this feature does, what it takes as input, and what it outputs — in one paragraph]

### Pre-requisites
- What data needs to be ready?
- Which system integrations must be completed?
- What infrastructure dependencies must be in place?

---

## 2. Data Structure Definition

### 2.1 Table Inventory

| Table Name | Description | New/Existing | Estimated Data Volume |
|------|------|---------|-----------|
| `t_xxx` | [Description] | New/Existing | Avg X records/day |

### 2.2 Table Structure Definition

**Table: [Table Name]**

| Field Name | Type | Length/Precision | Required | Default | Unique | Index | Description |
|--------|------|----------|------|--------|------|------|------|
| id | bigint | - | Yes | auto | PK | - | Primary Key |
| ... | | | | | | | |

### 2.3 Index Design

| Index Name | Fields | Type | Description |
|--------|------|------|------|
| idx_xxx | (col1, col2) | BTREE/UNIQUE | [Query Scenario] |

---

## 3. API Interface Definition

### 3.1 API Inventory

| # | API Name | Method | Path | Description |
|------|--------|--------|------|------|
| API-01 | Query List | POST | /api/v1/xxx/list | Pagination + Search + Filter + Sort |
| API-02 | Query Detail | GET | /api/v1/xxx/{id} | Includes related info |
| API-03 | Create | POST | /api/v1/xxx | |
| API-04 | Update | PUT | /api/v1/xxx/{id} | |
| API-05 | Delete | DELETE | /api/v1/xxx/{id} | Logical delete |

### 3.2 Detailed API Definitions

#### API-01: Query List

```
POST /api/v1/xxx/list
Content-Type: application/json
Authorization: Bearer {token}

Request Body:
{
  "pageNum": 1,           // Page number, starting from 1
  "pageSize": 20,         // Items per page, max 100
  "keyword": "search keyword",  // Fuzzy search (optional)
  "filters": {            // Exact filter (optional)
    "status": "approved",
    "type": "contract"
  },
  "dateRange": {          // Date range (optional)
    "start": "2026-01-01",
    "end": "2026-06-07"
  },
  "sortField": "created_at",  // Sort field (optional)
  "sortOrder": "desc"         // asc/desc
}

Response 200:
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 150,
    "pageNum": 1,
    "pageSize": 20,
    "list": [
      {
        "id": 1,
        "name": "xxx",
        "status": "approved",
        "creatorName": "John Doe",
        "createdAt": "2026-06-07 10:00:00"
      }
    ]
  }
}

Data Permission Notes:
- Super Admin: Returns all data
- Department Admin: Returns data for own department and sub-departments (filtered by tenant_id + dept_id)
- Regular User: Returns data created by self (filtered by creator_id)
```

#### API-03: Create

```
POST /api/v1/xxx
Content-Type: application/json

Request Body:
{
  "name": "xxx",          // [Required] Name, 1-100 characters
  "type": "contract",     // [Required] Type, see data dictionary for enum values
  "amount": 50000.00,     // [Optional] Amount, 0-99999999.99
  "date": "2026-06-07",   // [Optional] Date, format yyyy-MM-dd
  "description": "xxx",   // [Optional] Description, ≤500 characters
  "attachmentIds": [1,2]  // [Optional] Attachment ID list
}

Validation Rules:
- name: Required, 1-100 characters, trim leading/trailing spaces, cannot be all spaces
- type: Required, must be one of the enum values
- amount: Optional, ≥0, 2 decimal places
- date: Optional, cannot be earlier than 1900-01-01

Response 200 (Success):
{
  "code": 0,
  "message": "success",
  "data": { "id": 123 }
}

Response 400 (Validation Failed):
{
  "code": 40001,
  "message": "Parameter validation failed",
  "errors": [
    { "field": "name", "message": "Name cannot be empty" }
  ]
}
```

### 3.3 Common Response Codes

| Error Code | HTTP | Description | Frontend Handling |
|--------|------|------|---------|
| 0 | 200 | Success | - |
| 40001 | 400 | Parameter validation failed | Highlight form fields |
| 40100 | 401 | Not logged in | Redirect to login |
| 40300 | 403 | No permission | Show permission denied |
| 40400 | 404 | Resource not found | Return to list |
| 40900 | 409 | Data conflict (concurrency) | Prompt to refresh and retry |
| 50000 | 500 | Server error | Prompt to retry later |

---

## 4. Business Logic

### 4.1 Core Business Flow

```
[Pseudo-code level flow description — dev team can code from this]

1. Receive request → Parameter validation
2. Permission check: Does current user have [operation] permission?
3. Data scope check: Can current user operate on this data?
4. Business rule validation:
   a. Status check: Does current status allow this operation?
   b. Rule check: Are business rules satisfied (e.g., amount threshold)?
5. Execute operation:
   a. Open transaction
   b. Update main table
   c. Record operation log (audit)
   d. Trigger approval flow (if needed)
   e. Send notification (if needed)
   f. Commit transaction
6. Return result
```

### 4.2 Business Rules Detail

| Rule ID | Description | Trigger Condition | Validation Logic | Failure Message |
|--------|------|---------|---------|---------|
| BR-001 | Only draft status allows editing | Edit operation | status == 'draft' | "Editing not allowed in current status" |
| BR-002 | Cannot delete while pending approval | Delete operation | status != 'pending_approval' | "Cannot delete record while pending approval" |
| BR-003 | Amount > 50000 requires GM approval | Submit for approval | amount <= 50000 skip node | - |

### 4.3 Exception Handling

| Exception | Trigger Condition | Handling |
|------|---------|---------|
| Concurrent edit | Two users editing same record simultaneously | Optimistic lock (version field), prompt latter user to refresh |
| Duplicate submission | Network timeout retry | Anti-duplicate token, frontend button loading + disabled |
| Related data deletion | Deleting referenced data | Check foreign key, prohibit deletion if related data exists |
| Attachment upload failure | Network / size / format | Retry mechanism, single file ≤10MB, total ≤50MB |
| Batch operation partial failure | Mix of valid/invalid data | Transaction rollback or return failure details |

---

## 5. Approval Flow Definition

### 5.1 Flow Definition

```json
{
  "processKey": "contract_approval",
  "processName": "Contract Approval Process",
  "nodes": [
    {
      "nodeId": "node_start",
      "nodeName": "Submit Request",
      "type": "start",
      "assignee": "${initiator}"
    },
    {
      "nodeId": "node_manager",
      "nodeName": "Department Manager Approval",
      "type": "approval",
      "assignee": "${departmentManager}",
      "timeout": { "duration": 48, "unit": "hours", "action": "remind" }
    },
    {
      "nodeId": "node_finance",
      "nodeName": "Finance Approval",
      "type": "approval",
      "assignee": "role:finance_approver",
      "condition": "${amount > 5000}",
      "timeout": { "duration": 24, "unit": "hours", "action": "escalate" }
    },
    {
      "nodeId": "node_gm",
      "nodeName": "General Manager Approval",
      "type": "approval",
      "assignee": "role:general_manager",
      "condition": "${amount > 50000}",
      "timeout": { "duration": 72, "unit": "hours", "action": "remind" }
    },
    {
      "nodeId": "node_end",
      "nodeName": "Complete",
      "type": "end"
    }
  ],
  "edges": [
    { "from": "node_start", "to": "node_manager" },
    { "from": "node_manager", "to": "node_finance" },
    { "from": "node_finance", "to": "node_gm" },
    { "from": "node_gm", "to": "node_end" }
  ]
}
```

### 5.2 Approval Actions & Status Transitions

| Action | Previous Status | Next Status | Description |
|------|---------|---------|------|
| Submit | draft | pending_approval | Enter approval flow |
| Approve | pending_approval | pending_approval / approved | Last node approve → approved |
| Reject | pending_approval | rejected | Return to initiator |
| Withdraw | pending_approval | draft | Initiator only |
| Remind | pending_approval | pending_approval | No change, send notification |

---

## 6. Notifications

| Trigger Event | Recipient | Channel | Notification Template |
|---------|---------|---------|------------|
| Submit for approval | Next node approver | WeCom/DingTalk/Email/In-app | "You have a new approval pending: [Title]" |
| Approved | Initiator | In-app + WeCom | "Your [Title] has been approved" |
| Rejected | Initiator | In-app + WeCom + Email | "Your [Title] has been rejected. Reason: [Rejection Note]" |
| Timeout reminder | Current approver | In-app + WeCom | "You have [Title] pending approval, exceeded [X] hours" |
| Reminder (nudge) | Current approver | In-app + WeCom | "[Initiator] has nudged [Title], please process ASAP" |

---

## 7. Frontend Interaction Spec

### 7.1 Page States

| Page State | Trigger Condition | Display |
|---------|---------|---------|
| Loading | Data request in progress | Skeleton screen / loading spinner |
| Empty | No data | Empty state illustration + "No data yet" + [Create] button |
| With Data | Data returned | Normal list / detail |
| Network Error | Request failed | Error message + "Tap to retry" button |
| No Permission | 403 | "You don't have permission to access this page" + [Back] button |

### 7.2 Operation Feedback

| Operation | Feedback Method | Duration |
|------|---------|---------|
| Regular operation (create/edit) | Toast "Operation successful" | 3 seconds |
| Long-running operation (batch/import) | Progress bar + Toast on completion | Until complete |
| Dangerous operation (delete) | Modal confirmation dialog | Execute after user confirms |
| Failed operation | Toast with specific reason | 5 seconds |


---

## v1.1.0 New: Pricing Model Feature Spec

### Pricing Engine Feature Requirements
| Feature | Description | Priority |
|------|------|--------|
| Multi-dimensional billing | Support usage-based / per-user / per-feature / per-storage billing | P0 |
| Plan management | Free/Starter/Pro/Enterprise plan configuration | P0 |
| Usage metering | Real-time usage stats + threshold alerts | P0 |
| Auto upgrade/downgrade | Usage-triggered auto upgrade/downgrade | P1 |
| Trial management | Free trial period management + expiration reminders | P1 |
| Invoice management | Auto invoicing + multi-currency + multi-tax-rate | P1 |
| Coupons/discounts | Promo codes + tiered discounts + volume discounts | P2 |
| Price experimentation | A/B test different pricing plans | P2 |

### Pricing Data Model
| Entity | Key Fields | Description |
|------|---------|------|
| Plan | name, price, features, limits | Plan definition |
| Subscription | user_id, plan_id, start_date, end_date | User subscription |
| Usage | user_id, metric, value, timestamp | Usage record |
| Invoice | user_id, amount, period, status | Bill |