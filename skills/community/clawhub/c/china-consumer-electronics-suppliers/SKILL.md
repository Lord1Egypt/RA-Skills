---
name: china-consumer-electronics-suppliers
version: 1.0.0
description: "Comprehensive consumer electronics industry suppliers guide for international buyers – provides detailed information about China's smartphone, wearable, audio, smart home, and AR/VR manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "suppliers-china"
tags:
  - consumer-electronics
  - smartphones
  - wearables
  - audio-devices
  - smart-home
  - AR-VR
  - TWS
  - electronics-manufacturing
  - suppliers
  - supply-chain
invocable: true
---

# China Consumer Electronics Factory Skill

## Description
This skill helps international buyers navigate China's consumer electronics manufacturing landscape, which is projected to exceed **¥15.2 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes smartphones, wearables, audio devices, smart home products, AR/VR headsets, and accessories.

## Key Capabilities
- **Industry Overview**: Get a summary of China's consumer electronics industry scale, development targets, and key policy initiatives (Digital China, 5G, AI).
- **Supply Chain Structure**: Understand the complete industry chain from core components (chips, displays, batteries) to assembly and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs for different product categories (smartphones in Pearl River Delta, laptops in Yangtze River Delta, AR/VR in Beijing).
- **Subsector Insights**: Access detailed information on key subsectors (smartphones, wearables, audio devices, smart home, AR/VR).
- **Factory Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's consumer electronics industry in 2026?"
- "Show me the supply chain structure for smartphones"
- "Which regions are best for suppliers TWS earbuds?"
- "Tell me about smart watch manufacturing clusters"
- "How do I evaluate suppliers of smart home devices?"
- "What certifications should I look for in consumer electronics?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Electronic Information Industry Development Institute
- National Bureau of Statistics of China
- China Audio Industry Association
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `run.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual suppliers contacts.

## API Reference

The following Python functions are available in `run.py` for programmatic access:

### `get_industry_overview() -&gt; Dict`
Returns overview of China's consumer electronics industry scale, targets, and key policy initiatives.

**Example:**
```python
from run import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, export value, etc.