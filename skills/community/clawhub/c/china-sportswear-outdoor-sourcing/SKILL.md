---
name: china-sportswear-outdoor-sourcing
version: 1.0.0
description: "Comprehensive sportswear and outdoor equipment sourcing guide for international buyers – provides detailed information about China's athletic apparel, footwear, outdoor gear, and accessories manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - sportswear
  - outdoor-gear
  - athletic-apparel
  - footwear
  - tents
  - backpacks
  - functional-fabrics
  - sourcing
  - supply-chain
invocable: true
---

# China Sportswear & Outdoor Sourcing Skill

## Description
This skill helps international buyers navigate China's sportswear and outdoor equipment manufacturing landscape, which is projected to exceed **¥1.2 trillion in revenue by 2026**. China is the world's largest producer, supplying global brands and fast-growing domestic players. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes athletic apparel (leggings, jerseys, sports bras), outerwear (jackets, down coats), footwear (running shoes, hiking boots), outdoor gear (tents, backpacks, sleeping bags), and accessories.

## Key Capabilities
- **Industry Overview**: Get a summary of China's sportswear and outdoor industry scale, development targets, and key policy initiatives (National Fitness Program, winter sports legacy).
- **Supply Chain Structure**: Understand the complete industry chain from functional fabrics, insulation, components to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Fujian for footwear, Yangtze River Delta for outerwear and down, Pearl River Delta for sportswear).
- **Subsector Insights**: Access detailed information on key subsectors (athletic apparel, outerwear, footwear, outdoor gear, accessories).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's sportswear industry in 2026?"
- "Show me the supply chain structure for running shoes"
- "Which regions are best for sourcing down jackets?"
- "Tell me about tent manufacturing clusters"
- "How do I evaluate suppliers of waterproof jackets?"
- "What certifications should I look for in outdoor gear?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Sporting Goods Federation
- China Textile Industry Federation
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's sportswear and outdoor industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.