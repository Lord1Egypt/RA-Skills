---
name: consulting
description: Consulting practice management with engagement scoping, proposal writing, pricing strategy, and client relationship management. Use when user mentions consulting engagements, proposals, pricing, client relationships, or deliverables. Helps scope real problems, write winning proposals, set value-based prices, structure findings for impact, and navigate difficult client situations. NEVER replaces consultant judgment or independence.
---

# Consulting

Consulting practice system. Deliver work that changes things.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All client data stored locally only**: `memory/consulting/`
- **Strict client confidentiality** - no data sharing between engagements
- **No external CRM** connections
- **No cloud storage** of client information
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Help scope engagements and identify real problems
- ✅ Write proposals and structure deliverables
- ✅ Guide pricing and value conversations
- ✅ Navigate difficult client situations
- ❌ **NEVER replace** consultant judgment or independence
- ❌ **NEVER make** client decisions
- ❌ **NEVER share** client information across engagements

### Professional Note
Consulting value depends on independence and judgment. This skill supports your practice but the expertise, decisions, and client relationships remain entirely yours.

### Data Structure
Consulting data stored locally:
- `memory/consulting/engagements.json` - Active and past engagements
- `memory/consulting/proposals.json` - Proposal templates and history
- `memory/consulting/deliverables.json` - Deliverable structures
- `memory/consulting/pricing.json` - Pricing strategies and benchmarks
- `memory/consulting/relationships.json` - Client relationship notes

## Core Workflows

### Scope Engagement
```
User: "Help me scope this new client engagement"
→ Use scripts/scope_engagement.py --client "Acme Corp" --presenting "marketing strategy"
→ Distinguish presenting problem from real problem, define success metrics
```

### Write Proposal
```
User: "Write a proposal for the operations project"
→ Use scripts/write_proposal.py --engagement "ENG-123" --pricing "value-based"
→ Generate proposal with executive summary, approach, investment, terms
```

### Structure Pricing
```
User: "How should I price this engagement?"
→ Use scripts/structure_pricing.py --type "project" --value "$500K savings"
→ Recommend pricing model and anchor points
```

### Structure Deliverable
```
User: "Structure my findings for maximum impact"
→ Use scripts/structure_findings.py --audience "C-suite" --type "recommendation"
→ Build deliverable: recommendation first, supporting evidence, implementation
```

### Navigate Difficult Situation
```
User: "Client is not implementing what we agreed"
→ Use scripts/navigate_situation.py --type "implementation-gap" --engagement "ENG-123"
→ Prepare conversation that holds client accountable without damaging relationship
```

## Module Reference
- **Scoping Engagements**: See [references/scoping.md](references/scoping.md)
- **Proposal Writing**: See [references/proposals.md](references/proposals.md)
- **Pricing Strategy**: See [references/pricing.md](references/pricing.md)
- **Deliverable Structure**: See [references/deliverables.md](references/deliverables.md)
- **Client Relationships**: See [references/relationships.md](references/relationships.md)
- **Difficult Conversations**: See [references/difficult-conversations.md](references/difficult-conversations.md)
- **Referral Generation**: See [references/referrals.md](references/referrals.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `scope_engagement.py` | Scope new engagement |
| `write_proposal.py` | Write client proposal |
| `structure_pricing.py` | Design pricing strategy |
| `structure_findings.py` | Structure deliverable |
| `navigate_situation.py` | Navigate client challenge |
| `log_engagement.py` | Log engagement details |
| `track_deliverable.py` | Track deliverable progress |
| `generate_questions.py` | Generate discovery questions |
