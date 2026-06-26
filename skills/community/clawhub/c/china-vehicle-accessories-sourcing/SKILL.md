---
name: china-vehicle-accessories-sourcing
version: 1.0.0
description: "Comprehensive vehicle accessories industry sourcing guide for international buyers – provides detailed information about China's aftermarket products for all vehicle types (passenger cars, commercial vehicles, motorcycles, etc.) including interior/exterior trim, electronics, lighting, vehicle care, functional accessories, and safety equipment manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - vehicle-accessories
  - automotive-aftermarket
  - car-accessories
  - truck-accessories
  - motorcycle-accessories
  - dash-cams
  - floor-mats
  - seat-covers
  - roof-racks
  - vehicle-care
  - led-lighting
  - sourcing
  - supply-chain
invocable: true
---

# China Vehicle Accessories Sourcing Skill

## Description
This skill helps international buyers navigate China's vehicle accessories manufacturing landscape, which is projected to exceed **¥1.2 trillion in revenue by 2026**. It provides data-backed intelligence on regional clusters, supply chain structure, and industry trends based on the latest government policies and industry reports. Coverage includes a wide range of aftermarket products for all vehicle types: interior accessories (seat covers, floor mats), exterior accessories (roof racks, window visors), electronic gadgets (dash cams, GPS), lighting upgrades, vehicle care chemicals, functional accessories (roof boxes, tow bars, truck bed accessories), and safety equipment.

## Key Capabilities
- **Industry Overview**: Get a summary of China's vehicle accessories industry scale, development targets, and key policy initiatives.
- **Supply Chain Structure**: Understand the complete industry chain from raw materials and semi-finished goods to manufacturing and sales channels.
- **Regional Clusters**: Identify specialized manufacturing hubs for different accessory types (electronics, interior, exterior, vehicle care, etc.), including those serving commercial vehicle and motorcycle segments.
- **Subsector Insights**: Access detailed information on key subsectors (electronic accessories, interior accessories, exterior accessories, lighting, vehicle care products, functional accessories, safety accessories).
- **Sourcing Recommendations**: Get practical guidance on evaluating and selecting suppliers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's vehicle accessories industry in 2026?"
- "Show me the supply chain structure for vehicle accessories"
- "Which regions are best for sourcing dash cams and vehicle electronics?"
- "Tell me about floor mat manufacturing clusters for trucks and cars"
- "How do I evaluate suppliers of vehicle care products?"
- "What certifications should I look for in child safety seats?"
- "Do you have information on motorcycle accessories suppliers?"

## Data Sources
This skill aggregates data from:
- China Vehicle Accessories Industry Association (formerly Auto Accessories)
- Ministry of Commerce of the People's Republic of China
- National Bureau of Statistics of China
- China Council for the Promotion of International Trade (CCPIT)
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's vehicle accessories industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, automation rates, key drivers, etc.