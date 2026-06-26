---
name: china-beauty-factory
version: 1.0.0
description: "Comprehensive beauty industry factory guide for international buyers – provides detailed information about China's skincare, color cosmetics, hair care, and personal care manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "factory-china"
tags:
  - beauty
  - cosmetics
  - skincare
  - makeup
  - haircare
  - personal-care
  - ODM
  - factory
  - supply-chain
invocable: true
---

# China Beauty Factory Skill

## Description
This skill helps international buyers navigate China's beauty manufacturing landscape, which is projected to exceed **¥1.5 trillion in revenue by 2026**. China is the world's second-largest beauty market and largest producer of cosmetics. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes skincare, color cosmetics, hair care, body care, fragrances, and men's grooming.

## Key Capabilities
- **Industry Overview**: Get a summary of China's beauty industry scale, development targets, and key policy initiatives (efficacy claims, clean beauty, domestic brand growth).
- **Supply Chain Structure**: Understand the complete industry chain from raw materials (hyaluronic acid, peptides), packaging, formulation R&D to manufacturing and global sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs (Pearl River Delta for mass production, Yangtze River Delta for premium, Shandong for ingredients).
- **Subsector Insights**: Access detailed information on key subsectors (skincare, color cosmetics, hair care, body care, fragrances).
- **Factory Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's beauty industry in 2026?"
- "Show me the supply chain structure for skincare products"
- "Which regions are best for factory color cosmetics?"
- "Tell me about hyaluronic acid manufacturing clusters"
- "How do I evaluate ODM suppliers for private label?"
- "What certifications should I look for in clean beauty products?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT)
- China Association of Fragrance Flavor and Cosmetic Industries (CAFFCI)
- National Medical Products Administration (NMPA)
- National Bureau of Statistics of China
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `run.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `run.py` for programmatic access:

### `get_industry_overview() -&gt; Dict`
Returns overview of China's beauty industry scale, targets, and key policy initiatives.

**Example:**
```python
from run import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, key drivers, domestic brand share, etc.