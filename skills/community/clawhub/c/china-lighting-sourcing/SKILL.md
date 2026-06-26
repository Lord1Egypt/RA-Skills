---
name: china-lighting-sourcing
version: 1.0.0
description: "Comprehensive lighting industry sourcing guide for international buyers – provides detailed information about China's LED, smart, outdoor, automotive, and specialty lighting manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - lighting
  - led-lighting
  - smart-lighting
  - outdoor-lighting
  - automotive-lighting
  - lamps
  - luminaires
  - sourcing
  - supply-chain
invocable: true
---

# China Lighting Sourcing Skill

## Description
This skill helps international buyers navigate China's lighting manufacturing landscape, which is projected to exceed **¥980 billion in revenue by 2026**. China accounts for over 60% of global lighting output. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes LED lamps and luminaires, outdoor lighting, smart lighting, automotive lighting, and specialty lighting (grow lights, UV-C).

## Key Capabilities
- **Industry Overview**: Get a summary of China's lighting industry scale, development targets, and key policy initiatives (energy efficiency, smart lighting).
- **Supply Chain Structure**: Understand the complete industry chain from LED chips, drivers, optics to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Zhongshan Guzhen as Lighting Capital, Shenzhen for LEDs, Changzhou for automotive, etc.).
- **Subsector Insights**: Access detailed information on key subsectors (LED lamps, outdoor, smart, automotive, specialty).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's lighting industry in 2026?"
- "Show me the supply chain structure for LED lighting"
- "Which regions are best for sourcing smart lighting?"
- "Tell me about automotive lighting manufacturing clusters"
- "How do I evaluate suppliers of LED street lights?"
- "What certifications should I look for in lighting products?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Lighting Industry Association (CALI)
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's lighting industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.