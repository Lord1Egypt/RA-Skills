# aftersale-sop

## Name
After-Sales Service SOP

## Description
Comprehensive after-sales service standard operating procedures including退换货流程 (return/exchange processes), complaint escalation, service recovery, and compensation frameworks. Covers policy documentation, workflow design, quality standards, response timeframes, and customer satisfaction measurement for consistent, efficient post-purchase support operations.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| business_type | text | Yes | Type of products/services sold |
| return_policy | text | Yes | Current return and exchange policy |
| team_structure | text | Yes | Customer service team organization |
| common_issues | text | Yes | Frequent after-sales scenarios |
| service_standards | text | Yes | Target response and resolution times |
| escalation_matrix | text | No | Current escalation procedures |

## Output

| Name | Type | Description |
|------|------|-------------|
| return_process | text | Step-by-step return/exchange workflow |
| complaint_sop | text | Complaint handling procedures |
| escalation_procedures | text | Clear escalation paths and criteria |
| service_recovery | text | Service failure recovery protocols |
| compensation_matrix | text | Compensation guidelines by scenario |
| quality_standards | text | Service quality metrics and monitoring |
| training_materials | text | CS team training content |

## Example

### Input
```json
{
  "business_type": "Consumer electronics, 30-day return policy",
  "return_policy": "30 days unused, 14 days defective exchange",
  "team_structure": "Tier 1: 10 agents, Tier 2: 3 specialists, Manager",
  "common_issues": "Defective products, wrong items, buyer's remorse",
  "service_standards": "First response 2 hours, resolution 24 hours"
}
```

### Output
```json
{
  "return_process": "1. Verify eligibility, 2. Issue RMA, 3. Receive item, 4. Process refund",
  "complaint_sop": "Acknowledge in 1hr, investigate in 4hrs, resolve in 24hrs",
  "escalation_procedures": "Tier 2: >$500 value, Manager: legal threat, repeat complaint",
  "service_recovery": "Empower agents to offer up to $50 credit without approval",
  "compensation_matrix": "Shipping error: $10 credit, Defective: Full refund + $20 credit",
  "quality_standards": "CSAT >85%, First contact resolution >70%, Response time <2hrs",
  "training_materials": "Product knowledge, empathy scripts, de-escalation techniques"
}
```
