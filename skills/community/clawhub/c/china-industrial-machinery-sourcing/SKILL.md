---
name: china-industrial-machinery-sourcing
version: 1.0.0
description: "Comprehensive industrial machinery industry sourcing guide for international buyers – provides detailed information about China's machine tools, construction machinery, agricultural equipment, packaging lines, robotics, and other industrial machinery manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - industrial-machinery
  - machine-tools
  - construction-equipment
  - agricultural-machinery
  - packaging-machinery
  - robotics
  - sourcing
  - supply-chain
invocable: true
---

# China Industrial Machinery Sourcing Skill

## Description
This skill helps international buyers navigate China's industrial machinery manufacturing landscape, which is projected to exceed **¥11.8 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports.

## Key Capabilities
- **Industry Overview**: Get a summary of China's industrial machinery industry scale, development targets, and key policy initiatives.
- **Supply Chain Structure**: Understand the complete industry chain from raw materials and core components to downstream applications.
- **Regional Clusters**: Identify specialized manufacturing hubs for different machinery types (CNC machine tools, construction machinery, agricultural equipment, packaging lines, robotics, etc.).
- **Subsector Insights**: Access detailed information on key subsectors (metal cutting machine tools, construction machinery, agricultural machinery, packaging machinery, industrial robots, etc.).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, and typical lead times.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's industrial machinery industry in 2026?"
- "Show me the supply chain structure for industrial machinery"
- "Which regions are best for sourcing CNC machine tools?"
- "Tell me about construction machinery manufacturing clusters in China"
- "How do I evaluate suppliers of packaging lines?"
- "What certifications should I look for in industrial robot suppliers?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT) official policies
- China Machinery Industry Federation (CMIF) annual reports
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's industrial machinery industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, automation rates, key drivers, etc.