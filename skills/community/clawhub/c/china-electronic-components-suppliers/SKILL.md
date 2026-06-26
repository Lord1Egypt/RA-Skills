---
name: china-electronic-components-suppliers
version: 1.0.0
description: "Comprehensive electronic components industry suppliers guide for international buyers – provides detailed information about China's semiconductor, passive component, PCB, connector, and sensor manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "suppliers-china"
tags:
  - electronic-components
  - semiconductors
  - passives
  - PCBs
  - connectors
  - suppliers
  - supply-chain
invocable: true
---

# China Electronic Components Factory Skill

## Description
This skill helps international electronics buyers navigate China's electronic components manufacturing landscape, which is projected to exceed **¥5.2 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports.

## Key Capabilities
- **Industry Overview**: Get a summary of China's electronic components industry scale and development targets.
- **Supply Chain Structure**: Understand the complete industry chain from raw materials to downstream applications.
- **Regional Clusters**: Identify specialized manufacturing hubs for different component types (semiconductors, passives, PCBs, connectors, sensors).
- **Subsector Insights**: Access detailed information on key subsectors (semiconductors, passive components, PCBs, connectors, sensors, etc.).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods and communication best practices.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's electronic components industry in 2026?"
- "Show me the supply chain structure for electronic components"
- "Which regions are best for suppliers automotive-grade semiconductors?"
- "Tell me about MLCC manufacturing clusters"
- "How do I evaluate PCB suppliers in China?"
- "What certifications should I look for in sensor suppliers?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT) official policies
- National Bureau of Statistics of China
- China Electronic Components Association (CECA) annual reports
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `run.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual suppliers contacts.

## API Reference

The following Python functions are available in `run.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's electronic components industry scale, targets, and key policy initiatives.

**Example:**
```python
from run import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, automation rates, key drivers, etc.