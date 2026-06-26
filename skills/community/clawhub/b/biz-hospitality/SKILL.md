---
name: biz-hospitality
version: 1.0.0
description: "Professional business hospitality including reception plans, seating arrangements, dining coordination, and etiquette guidance. Covers VIP visits, business dinners, corporate events, and relationship-building occasions with cultural sensitivity and protocol compliance."
author: "openclaw"
tags:
 - biz-hospitality
 - hospitality
 - reception
 - vip

invocable: true
---

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| guest_profile | text | Yes | Guest information and importance |
| visit_purpose | text | Yes | Purpose of visit |
| visit_duration | text | Yes | Length of visit |
| host_representatives | text | Yes | Company representatives |
| cultural_considerations | text | Yes | Cultural or dietary requirements |
| budget_range | text | Yes | Hospitality budget |
| previous_visits | text | No | History with this guest |

## Output

| Name | Type | Description |
|------|------|-------------|
| reception_plan | text | Complete visit itinerary |
| seating_arrangement | text | Meeting and dining seating plan |
| dining_arrangements | text | Restaurant selection and menu |
| etiquette_guide | text | Protocol and etiquette reminders |
| gift_suggestions | text | Appropriate gift options |
| talking_points | text | Suggested conversation topics |
| follow_up_plan | text | Post-visit follow-up actions |

## Example

### Input
```json
{
  "guest_profile": "CEO of major client company, strategic partner",
  "visit_purpose": "Partnership renewal discussion",
  "visit_duration": "Full day",
  "host_representatives": "Our CEO, VP Sales, Technical Director",
  "cultural_considerations": "Guest is Japanese, prefers formal settings",
  "budget_range": "$2,000 for day"
}
```

### Output
```json
{
  "reception_plan": "9AM: Office arrival, tour | 10AM: Executive meeting | 12PM: Business lunch | 2PM: Technical demo | 4PM: Partnership discussion | 6PM: Dinner",
  "seating_arrangement": "Meeting: Host CEO center, guest CEO right, others by seniority | Dinner: Alternating host/guest",
  "dining_arrangements": "Lunch: Private room at business club | Dinner: High-end Japanese restaurant",
  "etiquette_guide": "Business card exchange with both hands, bow slightly, formal address, punctuality critical",
  "gift_suggestions": "Company-branded premium item, local specialty, quality pen set",
  "talking_points": "Partnership achievements, future opportunities, industry trends, personal interests",
  "follow_up_plan": "Thank you email within 24hrs, meeting summary, partnership proposal within week"
}
```