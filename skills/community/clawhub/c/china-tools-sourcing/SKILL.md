---
name: china-tools-sourcing
version: 1.0.0
description: "Comprehensive tools industry sourcing guide for international buyers – provides detailed information about China's hand tools, power tools, garden tools, measuring tools, and industrial tool manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - tools
  - hand-tools
  - power-tools
  - garden-tools
  - measuring-tools
  - tool-storage
  - cutting-tools
  - sourcing
  - supply-chain
invocable: true
---

# China Tools Sourcing Skill

## Description
This skill helps international buyers navigate China's tools manufacturing landscape, which is projected to exceed **¥1.2 trillion in revenue by 2026**. China is the world's largest producer and exporter of tools, supplying both professional trades and DIY markets globally. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes hand tools, power tools, garden tools, measuring tools, tool storage, automotive tools, pneumatic tools, and cutting tools.

## Key Capabilities
- **Industry Overview**: Get a summary of China's tools industry scale, development targets, and key policy initiatives (smart manufacturing, battery technology).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials (steel, plastics, batteries) to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Yongkang for hand tools, Suzhou for power tools, Danyang for cutting tools, Shandong for automotive tools).
- **Subsector Insights**: Access detailed information on key subsectors (hand tools, power tools, garden tools, measuring tools, tool storage, automotive tools, pneumatic tools, cutting tools).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's tools industry in 2026?"
- "Show me the supply chain structure for power tools"
- "Which regions are best for sourcing hand tools?"
- "Tell me about cutting tool manufacturing clusters"
- "How do I evaluate suppliers of garden tools?"
- "What certifications should I look for in power tools?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Hardware Association
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's tools industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.