# 团队与客户数据库 Schema

Use these schemas for memory, CRM records, Hermes/OpenClaw knowledge stores, or structured notes.

## Team Member Profile

```json
{
  "type": "team_member_profile",
  "name": "",
  "role": "",
  "department": "",
  "leader": "",
  "join_date": "",
  "compensation_structure": "",
  "responsibilities": [],
  "key_results": [],
  "daily_actions": [],
  "scores": {
    "professional": 0,
    "sales": 0,
    "communication": 0,
    "execution": 0,
    "learning": 0,
    "review": 0,
    "collaboration": 0,
    "management_potential": 0,
    "customer_service": 0,
    "stress_resistance": 0,
    "values_fit": 0
  },
  "status": "",
  "recent_performance": "",
  "strengths": [],
  "risks": [],
  "recommended_action": "",
  "training_tasks": [],
  "next_1on1_date": "",
  "boss_notes": "",
  "last_updated": ""
}
```

## Team Training Record

```json
{
  "type": "team_training_record",
  "member_name": "",
  "training_topic": "",
  "start_date": "",
  "end_date": "",
  "tasks": [],
  "score_before": null,
  "score_after": null,
  "manager_feedback": "",
  "next_action": ""
}
```

## Customer Relationship Profile

```json
{
  "type": "customer_relationship_profile",
  "basic": {
    "name": "",
    "gender": "",
    "age_range": "",
    "city": "",
    "occupation": "",
    "industry": "",
    "company": "",
    "role": ""
  },
  "contact": {
    "phone": "",
    "wechat": "",
    "social_accounts": [],
    "source_channel": "",
    "referrer": "",
    "first_touch_date": "",
    "first_touch_context": ""
  },
  "purchase": {
    "products": [],
    "total_spend": 0,
    "purchase_motives": [],
    "decision_maker": "",
    "payer": "",
    "user": "",
    "budget_range": "",
    "price_sensitivity": "",
    "deal_reasons": [],
    "loss_reasons": []
  },
  "needs": {
    "pain_points": [],
    "short_term_goals": [],
    "long_term_goals": [],
    "past_attempts": [],
    "concerns": []
  },
  "preferences": {
    "interests": [],
    "favorite_topics": [],
    "favorite_brands": [],
    "favorite_foods_or_drinks": [],
    "favorite_platforms": [],
    "communication_style": "",
    "best_contact_time": "",
    "preferred_contact_method": "",
    "disliked_contact_method": "",
    "preferred_name": "",
    "accepts_humor": null
  },
  "relationships": {
    "family": [],
    "children": [],
    "partner_or_colleagues": [],
    "influencers": []
  },
  "important_dates": [
    {
      "type": "birthday/anniversary/event/follow_up",
      "date": "",
      "note": ""
    }
  ],
  "service": {
    "service_preferences": [],
    "satisfied_points": [],
    "unsatisfied_points": [],
    "needs_reminder": false,
    "likes_ritual": false,
    "gift_suitable": ""
  },
  "risks": {
    "taboo_topics": [],
    "sensitive_points": [],
    "complaints": [],
    "privacy_sensitivity": "",
    "churn_risks": []
  },
  "relationship_ops": {
    "last_greeting": "",
    "last_gift_or_care": "",
    "important_quotes": [],
    "emotion_status": "",
    "relationship_temperature": "cold/normal/warm/trusted",
    "referral_potential": "",
    "next_service_action": "",
    "owner": ""
  },
  "last_updated": ""
}
```

## Memory Rules

- Store only user-provided facts, accepted conclusions, or completed training results.
- Keep team and customer records separate.
- For customer sensitive data, ask permission when needed.
- Update records after user corrections.
- Before advice, retrieve relevant team/customer profile if available.
