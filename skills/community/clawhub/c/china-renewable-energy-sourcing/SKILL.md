---
name: china-renewable-energy-sourcing
version: 1.0.0
description: "Comprehensive renewable energy industry sourcing guide for international buyers – provides detailed information about China's solar PV, wind power, energy storage, and hydrogen manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - renewable-energy
  - solar-pv
  - wind-power
  - energy-storage
  - hydrogen
  - batteries
  - inverters
  - clean-energy
  - sourcing
  - supply-chain
invocable: true
---

# China Renewable Energy Sourcing Skill

## Description
This skill helps international buyers navigate China's renewable energy manufacturing landscape, which is projected to exceed **¥1.8 trillion in revenue by 2026**. China is the world's largest producer of solar modules, wind turbines, lithium batteries, and electrolyzers, supplying global markets. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes solar PV, wind power, energy storage, hydrogen, and smart grid integration.

## Key Capabilities
- **Industry Overview**: Get a summary of China's renewable energy industry scale, installed capacity, and key policy initiatives (14th Five-Year Plan, carbon neutrality goals).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials (polysilicon, lithium, rare earths) to equipment manufacturing and project development.
- **Regional Clusters**: Identify specialized manufacturing hubs (Yangtze River Delta for solar and offshore wind, Pearl River Delta for batteries, Southwest for polysilicon).
- **Subsector Insights**: Access detailed information on key subsectors (solar PV, wind power, energy storage, hydrogen, smart grid).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's renewable energy industry in 2026?"
- "Show me the supply chain structure for solar PV"
- "Which regions are best for sourcing lithium batteries?"
- "Tell me about wind turbine manufacturing clusters"
- "How do I evaluate suppliers of hydrogen electrolyzers?"
- "What certifications should I look for in energy storage systems?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- National Energy Administration (NEA)
- China Renewable Energy Engineering Institute
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's renewable energy industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, installed capacity, key drivers, etc.