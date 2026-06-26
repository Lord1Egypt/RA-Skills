---
name: china-shoes-sourcing
version: 1.0.0
description: "Comprehensive footwear industry sourcing guide for international buyers – provides detailed information about China's athletic, leather, women's, children's, and casual shoe manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - footwear
  - shoes
  - athletic-shoes
  - sneakers
  - leather-shoes
  - women-shoes
  - children-shoes
  - sourcing
  - supply-chain
invocable: true
---

# China Footwear Sourcing Skill

## Description
This skill helps international buyers navigate China's footwear manufacturing landscape, which accounts for approximately 60% of global shoe production and is projected to exceed **¥820 billion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes athletic shoes, leather shoes, women's shoes, children's shoes, casual shoes, sandals/slippers, and safety footwear.

## Key Capabilities
- **Industry Overview**: Get a summary of China's footwear industry scale, development targets, and key policy initiatives (sustainability, automation, brand building).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials (leather, textiles, soles) and components to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Fujian for athletic shoes, Guangdong for women's shoes, Zhejiang for leather shoes, etc.).
- **Subsector Insights**: Access detailed information on key subsectors (athletic, leather, women's, children's, casual, sandals/slippers, safety).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's footwear industry in 2026?"
- "Show me the supply chain structure for athletic shoes"
- "Which regions are best for sourcing women's fashion shoes?"
- "Tell me about leather shoe manufacturing clusters"
- "How do I evaluate suppliers of children's shoes?"
- "What certifications should I look for in safety footwear?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Leather Industry Association
- China Footwear Industry Association
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's footwear industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.