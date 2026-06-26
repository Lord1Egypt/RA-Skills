---
name: china-furniture-sourcing
version: 1.0.0
description: "Comprehensive furniture industry sourcing guide for international buyers – provides detailed information about China's residential, office, hotel, outdoor, and custom furniture manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - furniture
  - home-furniture
  - office-furniture
  - outdoor-furniture
  - custom-furniture
  - mattresses
  - wood-furniture
  - sourcing
  - supply-chain
invocable: true
---

# China Furniture Sourcing Skill

## Description
This skill helps international buyers navigate China's furniture manufacturing landscape, which is projected to exceed **¥1.8 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes residential furniture (sofas, beds, wardrobes), office furniture (desks, chairs), hotel furniture, outdoor furniture, custom furniture, children's furniture, and mattresses.

## Key Capabilities
- **Industry Overview**: Get a summary of China's furniture industry scale, development targets, and key policy initiatives (green manufacturing, smart furniture).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials (wood, panels, hardware, upholstery) to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs for different furniture types (Pearl River Delta for sofas and residential, Zhejiang for office chairs and outdoor, Sichuan for panel furniture, Jiangxi for solid wood).
- **Subsector Insights**: Access detailed information on key subsectors (residential, office, hotel, outdoor, custom, children, mattresses).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's furniture industry in 2026?"
- "Show me the supply chain structure for wooden furniture"
- "Which regions are best for sourcing office chairs?"
- "Tell me about outdoor furniture manufacturing clusters"
- "How do I evaluate suppliers of custom furniture?"
- "What certifications should I look for in mattresses?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China National Furniture Association (CNFA)
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's furniture industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.