---
name: china-electronic-components-sourcing
version: 1.0.0
description: "Comprehensive electronic components industry sourcing guide for international buyers – provides detailed information about China's semiconductor, passive component, PCB, connector, and sensor manufacturing clusters, supply chain structure, regional specializations, and industry trends (2026 updated)."
author: "sourcing-china"
tags:
  - electronic-components
  - semiconductors
  - passives
  - PCBs
  - connectors
  - sourcing
  - supply-chain
invocable: true
---

# China Electronic Components Sourcing Skill

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
- "Which regions are best for sourcing automotive-grade semiconductors?"
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
The skill logic is implemented in `do.py`, which reads structured data from `data.json`. All data is cluster-level intelligence without individual factory contacts.

## API Reference

The following Python functions are available in `do.py` for programmatic access:

### `get_industry_overview() -> Dict`
Returns overview of China's electronic components industry scale, targets, and key policy initiatives.

**Example:**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, automation rates, key drivers, etc.
```

### `get_supply_chain_structure() -> Dict`
Returns the complete electronic components supply chain structure (upstream, midstream, downstream).

**Example:**
```python
from do import get_supply_chain_structure
result = get_supply_chain_structure()
# Returns: raw materials, manufacturing, application industries
```

### `get_regional_clusters(region: Optional[str] = None) -> Union[List[Dict], Dict]`
Returns all regional clusters or a specific cluster by name.
- If `region` is None: returns list of all clusters
- If `region` is specified: returns that cluster's details

**Example:**
```python
from do import get_regional_clusters
all_clusters = get_regional_clusters()
yangtze = get_regional_clusters("Yangtze River Delta")
```

### `find_clusters_by_specialization(specialization: str) -> List[Dict]`
Find clusters that specialize in a given component type.

**Example:**
```python
from do import find_clusters_by_specialization
results = find_clusters_by_specialization("automotive semiconductors")
```

### `get_subsector_info(subsector: str) -> Dict`
Return detailed information about a specific electronic components subsector.

**Example:**
```python
from do import get_subsector_info
mlcc_info = get_subsector_info("MLCC")
semiconductor_info = get_subsector_info("semiconductors")
```

### `get_sourcing_guide() -> Dict`
Return supplier evaluation and sourcing best practices.

**Example:**
```python
from do import get_sourcing_guide
guide = get_sourcing_guide()
# Returns: evaluation criteria, verification methods, communication tips
```

### `get_faq(question: Optional[str] = None) -> Union[List[Dict], Dict]`
Return FAQ list or answer to a specific question.

**Example:**
```python
from do import get_faq
all_faqs = get_faq()
moq_faq = get_faq("MOQ")
```

### `get_glossary(term: Optional[str] = None) -> Union[Dict, str]`
Return glossary of terms or definition of a specific term.

**Example:**
```python
from do import get_glossary
all_terms = get_glossary()
mlcc_def = get_glossary("MLCC")
```

### `search_data(query: str) -> List[Dict]`
Simple search across all data for a query string.

**Example:**
```python
from do import search_data
results = search_data("automotive")
```

### `get_metadata() -> Dict`
Return metadata about the data source and last update.

**Example:**
```python
from do import get_metadata
meta = get_metadata()
```
