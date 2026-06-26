---
name: csv_graph_loader_generator
title: CSV Graph Loader Generator
description: Generate graph database loaders and triple mappings from CSV datasets. Converts tabular CSV data into graph-ready nodes, edges, and triples for graph databases or knowledge graphs.
category: data-ingestion
tags:
  - csv-loading
  - graph-database
  - neo4j
  - rdf
  - data-transformation
  - etl
  - knowledge-graph
  - schema-generation
  - property-graph
  - developer-tools
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"📥","homepage":"https://clawhub.com"}}
---

# CSV Graph Loader Generator

**Convert CSV datasets into graph-ready structures for knowledge graph construction.**

This skill transforms **tabular CSV data** into **graph database ingestion formats** such as nodes, edges, or triples. It generates mappings and loader scripts for graph systems like **Neo4j, RDF triple stores, property graphs, and knowledge graphs**.

## Quick Start

### Use When
- Converting CSV datasets to graph structures
- Preparing data for graph database import
- Generating Neo4j LOAD CSV scripts
- Creating RDF triple mappings
- Building property graphs from tables
- Constructing knowledge graphs from structured data
- Automating CSV → graph ETL workflows

### Inputs
- CSV file or data
- Column definitions and data types
- Entity type specifications
- Relationship definitions
- Target graph format
- Custom mapping rules

### Outputs
- Node definitions (labels, properties)
- Relationship mappings (types, directions)
- Neo4j Cypher import scripts
- RDF triple definitions
- Property graph JSON
- Graph schema definitions
- Mapping configuration files

## Example

**Input CSV:**
```csv
person_id,name,company_name,company_industry,job_title
1,Alice Johnson,Acme Corp,Technology,Software Engineer
2,Bob Smith,Acme Corp,Technology,Product Manager
3,Carol Davis,TechStart Inc,Technology,CTO
```

**Generated Output (Nodes & Edges):**
```json
{
  "nodes": [
    {"id": "p1", "type": "Person", "properties": {"name": "Alice Johnson", "job": "Software Engineer"}},
    {"id": "p2", "type": "Person", "properties": {"name": "Bob Smith", "job": "Product Manager"}},
    {"id": "c1", "type": "Company", "properties": {"name": "Acme Corp", "industry": "Technology"}},
    {"id": "c2", "type": "Company", "properties": {"name": "TechStart Inc", "industry": "Technology"}}
  ],
  "edges": [
    {"source": "p1", "target": "c1", "type": "WORKS_AT"},
    {"source": "p2", "target": "c1", "type": "WORKS_AT"},
    {"source": "p3", "target": "c2", "type": "WORKS_AT"}
  ]
}
```

## CSV-to-Graph Transformation Strategy

### 1. Entity Detection
Automatically identify entity columns:
- **ID columns** - Unique identifiers (person_id, company_id)
- **Name columns** - Entity names (name, title, company_name)
- **Category columns** - Entity types (type, category, industry)

### 2. Entity Classification
Create node types from detected entities:
```
person_id → Person node
company_name → Company node
department → Department node
```

### 3. Relationship Inference
Map column associations to relationships:
```
person_id + company_name → WORKS_AT
employee_id + manager_id → REPORTS_TO
product_id + category_id → BELONGS_TO
```

### 4. Property Assignment
Remaining columns become node properties:
```
name → Person.name
salary → Person.salary
industry → Company.industry
```

### 5. Output Generation
Create loader scripts for target system:
```cypher
Neo4j: LOAD CSV WITH HEADERS...
RDF: :Alice rdf:type :Person
JSON: {"nodes": [...], "edges": [...]}
```

## Supported Entity Patterns

### ID-Based Entities
```
pattern: column_name contains "id" or "identifier"
example: person_id, user_id, company_id
```

### Name-Based Entities
```
pattern: column_name contains "name" or "title"
example: person_name, company_name, job_title
```

### Category-Based Entities
```
pattern: column_name contains "type" or "category"
example: person_type, company_category, product_category
```

### Implicit Entities
```
pattern: column values represent entities
example: department column with values like "Sales", "Engineering"
```

## Output Formats

### Neo4j Cypher Script
```cypher
LOAD CSV WITH HEADERS FROM 'file:///employees.csv' AS row
MERGE (p:Person {id: row.person_id})
SET p.name = row.name, p.job_title = row.job_title
MERGE (c:Company {name: row.company_name})
SET c.industry = row.company_industry
MERGE (p)-[:WORKS_AT]->(c)
```

### RDF Triples (Turtle)
```turtle
@prefix ex: <http://example.org/> .

ex:person1 a ex:Person ;
  ex:name "Alice Johnson" ;
  ex:jobTitle "Software Engineer" ;
  ex:worksAt ex:acme_corp .

ex:acme_corp a ex:Company ;
  ex:name "Acme Corp" ;
  ex:industry "Technology" .
```

### Property Graph JSON
```json
{
  "nodes": [
    {"id": "p1", "type": "Person", "properties": {"name": "Alice", "job": "Engineer"}},
    {"id": "c1", "type": "Company", "properties": {"name": "Acme", "industry": "Tech"}}
  ],
  "edges": [
    {"source": "p1", "target": "c1", "type": "WORKS_AT"}
  ]
}
```

### CSV to Node/Edge Tables
```csv
# nodes.csv
id,type,name,job_title
p1,Person,Alice,Software Engineer
p2,Person,Bob,Product Manager
c1,Company,Acme Corp,

# edges.csv
source,target,type
p1,c1,WORKS_AT
p2,c1,WORKS_AT
```

## Mapping Strategies

### Automatic Detection
```
pros: No manual configuration needed
cons: May infer wrong relationships
use: Quick prototyping, simple datasets
```

### Semi-Automated with Hints
```
pros: Balance between automation and control
cons: Requires some input
use: Most common production use case
```

### Explicit Mapping
```
pros: Full control, exact desired output
cons: Requires complete configuration
use: Complex schemas, strict requirements
```

## Data Type Inference

The loader automatically infers:
- **String** - Text columns
- **Integer** - Numeric whole numbers
- **Float** - Decimal numbers
- **Boolean** - True/false values
- **DateTime** - Date and time formats
- **Reference** - Columns pointing to other entities

## Duplicate Handling

### Merge Strategy
```
Identical entities across rows are merged
example: Two rows with "Acme Corp" → one Company node
```

### Deduplication
```
Removes duplicate edges from same source/target
example: Multiple WORKS_AT edges → single edge
```

### ID-Based Deduplication
```
Uses unique identifiers to prevent duplicates
example: person_id as stable key for Person nodes
```

## Execution Steps

1. **Parse CSV** – Read file and validate structure
2. **Analyze Schema** – Detect data types and patterns
3. **Detect Entities** – Identify entity columns
4. **Infer Relationships** – Map column associations
5. **Create Schema** – Define node types and relationship types
6. **Generate Mappings** – Create column-to-property mappings
7. **Validate Data** – Check for data quality issues
8. **Generate Loaders** – Output scripts for target system

## Recommended Libraries

- **CSV Processing:** pandas, csv, polars
- **Graph Generation:** neo4j, rdflib, networkx
- **Data Validation:** pydantic, jsonschema
- **RDF/OWL:** rdflib, owlready2, sparql-client
- **JSON Transformation:** jsonschema, jinja2

## Best Practices

✓ Use stable, meaningful identifiers  
✓ Normalize entity names to prevent duplicates  
✓ Define explicit entity types rather than guessing  
✓ Validate data before loading to graph database  
✓ Document custom mapping rules  
✓ Test with sample data first  
✓ Monitor for duplicate nodes or relationships  
✓ Keep mapping configurations version-controlled  
✓ Handle missing values explicitly  
✓ Implement referential integrity checks  

## Integration with Downstream Skills

The generated graph data feeds into:

- **Graph Query Optimization** – Optimize generated Cypher queries
- **Schema Validation** – Validate against graph schema
- **Graph Constraint Generator** – Define constraints for loaded data
- **Knowledge Graph Construction** – Build KGs from CSV sources
- **ETL Pipeline Generator** – Orchestrate full CSV → Graph workflows

## References

See [loader-patterns.md](references/loader-patterns.md) for detailed CSV loader patterns and [example-loaders.md](examples/example-loaders.md) for complete domain-specific examples.

---

**Version:** 1.0.0
