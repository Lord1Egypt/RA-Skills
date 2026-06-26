---
name: china-toys-sourcing
version: 1.0.0
description: "Comprehensive toys industry sourcing guide for international buyers – provides detailed information about China's plastic, electronic, wooden, plush, model, and educational toy manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - toys
  - plastic-toys
  - electronic-toys
  - wooden-toys
  - plush-toys
  - educational-toys
  - model-kits
  - sourcing
  - supply-chain
invocable: true
---

# China Toys Sourcing Skill

## Description
This skill helps international buyers navigate China's toy manufacturing landscape, which accounts for over 70% of global toy production and is projected to exceed **¥1.1 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes plastic toys, electronic toys, wooden toys, plush toys, model kits, and educational toys.

## Key Capabilities
- **Industry Overview**: Get a summary of China's toy industry scale, development targets, and key policy initiatives (safety standards, innovation).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials and components to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Chenghai for plastic/electronic toys, Ningbo for wooden toys, Yangzhou for plush).
- **Subsector Insights**: Access detailed information on key subsectors (plastic, electronic, wooden, plush, model, educational).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's toy industry in 2026?"
- "Show me the supply chain structure for electronic toys"
- "Which regions are best for sourcing wooden educational toys?"
- "Tell me about plush toy manufacturing clusters"
- "How do I evaluate suppliers of plastic action figures?"
- "What safety certifications should I look for?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Toy & Juvenile Products Association
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's toy industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.