---
name: china-vehicle-sourcing
version: 1.0.0
description: "Comprehensive vehicle sourcing guide for international buyers – provides detailed information about China's passenger car, commercial vehicle, motorcycle, and new energy vehicle manufacturing industry, including regional clusters, production bases, key players, and sourcing best practices (2026 updated)."
author: "sourcing-china"
tags:
  - vehicle-sourcing
  - automotive
  - passenger-cars
  - commercial-vehicles
  - motorcycles
  - NEV
  - electric-vehicles
  - manufacturing
  - sourcing
  - supply-chain
invocable: true
---

# China Vehicle Sourcing Skill

## Description
This skill helps international buyers navigate China's vehicle manufacturing landscape, which produces over 30 million vehicles annually and is projected to exceed **¥12.5 trillion in revenue by 2026**. It provides data-backed intelligence on regional production clusters, vehicle types (passenger cars, commercial vehicles, motorcycles, NEVs), key manufacturers, and industry trends based on the latest government policies and industry reports.

## Key Capabilities
- **Industry Overview**: Get a summary of China's vehicle industry scale, production targets, and key policy initiatives.
- **Supply Chain Structure**: Understand the complete vehicle supply chain from raw materials to manufacturing and sales channels.
- **Regional Clusters**: Identify specialized production hubs for different vehicle types (passenger cars, commercial vehicles, motorcycles, NEVs) across China.
- **Vehicle Type Insights**: Access detailed information on key vehicle segments (passenger cars, commercial vehicles, motorcycles, new energy vehicles).
- **Sourcing Recommendations**: Get practical guidance on evaluating vehicle manufacturers, including verification methods, communication best practices, typical lead times, and payment terms.

## How to Use
You can interact with this skill using natural language. For example:
- "What's the overall status of China's vehicle industry in 2026?"
- "Show me the supply chain structure for vehicle manufacturing"
- "Which regions are best for sourcing NEVs?"
- "Tell me about motorcycle manufacturing clusters"
- "How do I evaluate commercial vehicle suppliers?"
- "What are the requirements for importing vehicles from China?"

## Data Sources
This skill aggregates data from:
- Ministry of Industry and Information Technology (MIIT) official policies
- China Association of Automobile Manufacturers (CAAM)
- China Motorcycle Association
- National Bureau of Statistics of China
- China Customs export data
- Industry research publications (updated Q1 2026)

## Implementation
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's vehicle industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: production volume, revenue, NEV share, export volume, etc.