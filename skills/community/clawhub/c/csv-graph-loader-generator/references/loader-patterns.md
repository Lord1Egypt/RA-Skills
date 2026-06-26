# CSV Loader Design Patterns

This guide provides patterns for converting CSV data into graph structures.

## Entity Detection Patterns

### ID-Based Entity Pattern

```
Pattern: Column names indicate entity identifiers

Identifies: person_id, user_id, company_id, product_id, etc.

Detection:
  - Column names ending with "_id" or "_identifier"
  - Often integer or string values that uniquely identify entities

Example CSV:
  person_id,name,company_id,salary
  1,Alice,C001,100000

Generated Nodes:
  (:Person {id: 1})
  (:Company {id: "C001"})
```

**When to use:**
✓ Data with explicit ID columns
✓ Pre-existing unique identifiers
✓ Reference-based relationships

---

### Name-Based Entity Pattern

```
Pattern: Column contains entity names or labels

Identifies: person_name, company_name, product_title, etc.

Detection:
  - Column names containing "name", "title", "label", "description"
  - String values that represent entity names

Example CSV:
  person_name,company_name
  Alice Johnson,Acme Corp

Generated Nodes:
  (:Person {name: "Alice Johnson"})
  (:Company {name: "Acme Corp"})
```

**When to use:**
✓ Data with descriptive names
✓ No explicit IDs available
✓ Natural language entities

---

### Category-Based Entity Pattern

```
Pattern: Column values categorize entities

Identifies: entity_type, category, classification, genre, etc.

Detection:
  - Repeated categorical values across rows
  - Limited unique values in a column

Example CSV:
  person_name,person_type,company_name
  Alice,Employee,Acme
  Bob,Contractor,Acme

Generated Nodes:
  (:Employee {name: "Alice"})
  (:Contractor {name: "Bob"})
  (:Company {name: "Acme"})
```

**When to use:**
✓ Implicit entity types in data
✓ Classification columns
✓ Type-driven entity creation

---

### Implicit Entity Pattern

```
Pattern: Values in a column represent entities

Identifies: department, location, status, etc.

Detection:
  - Repeated non-ID values
  - Values that reference other entities
  - Department names, location names, etc.

Example CSV:
  person_name,department,location
  Alice,Engineering,New York
  Bob,Engineering,San Francisco

Generated Nodes:
  (:Person {name: "Alice"})
  (:Department {name: "Engineering"})
  (:Location {name: "New York"})
```

**When to use:**
✓ Implicit hierarchical data
✓ Shared entity references
✓ Dimension tables

---

## Relationship Pattern Detection

### Direct Column Association

```
Pattern: Two columns in same row represent related entities

Example:
  person_id, company_id
  1, C001

Maps to:
  (:Person {id: 1})-[:WORKS_AT]->(:Company {id: "C001"})

Detection:
  - Column pairs with complementary entity references
  - Pattern: source_id and target_id columns
```

**When to use:**
✓ Explicit foreign key relationships
✓ Two distinct entity types
✓ One-to-one or many-to-one

---

### Implicit Relationship Pattern

```
Pattern: Column indicates relationship through association

Example:
  person_name, department
  Alice, Engineering

Maps to:
  (:Person {name: "Alice"})-[:WORKS_IN]->(:Department {name: "Engineering"})

Detection:
  - Categories or implicit entities in columns
  - Shared values across rows (normalization)
```

**When to use:**
✓ Implicit relationships
✓ Dimension tables
✓ Categorical associations

---

### Hierarchical Relationship Pattern

```
Pattern: Multiple levels of entity hierarchy

Example CSV:
  person_name, department, company, industry
  Alice, Engineering, Acme, Technology

Hierarchy:
  Person
    └─ Department
       └─ Company
          └─ Industry

Generated Relationships:
  (:Person)-[:IN_DEPARTMENT]->(:Department)
  (:Department)-[:IN_COMPANY]->(:Company)
  (:Company)-[:IN_INDUSTRY]->(:Industry)
```

**When to use:**
✓ Multi-level hierarchies
✓ Dimension hierarchies
✓ Organizational structures

---

### Self-Referencing Relationship Pattern

```
Pattern: Rows reference other rows in same table

Example CSV:
  employee_id, name, manager_id
  1, Alice, NULL
  2, Bob, 1
  3, Carol, 1

Maps to:
  (:Person {id: 2, name: "Bob"})-[:REPORTS_TO]->(:Person {id: 1, name: "Alice"})
  (:Person {id: 3, name: "Carol"})-[:REPORTS_TO]->(:Person {id: 1, name: "Alice"})

Detection:
  - Foreign key references to same entity type
  - NULL values for root nodes (no manager)
```

**When to use:**
✓ Organizational hierarchies
✓ Manager-employee relationships
✓ Parent-child structures

---

## Output Format Patterns

### Neo4j Cypher Pattern

```cypher
Pattern: Generate LOAD CSV script for Neo4j import

Basic structure:
  LOAD CSV WITH HEADERS FROM 'file:///<filename>' AS row
  MERGE (n:<NodeType> {id: row.<id_column>})
  SET n.<property> = row.<column>
  MERGE (m:<OtherType> {id: row.<other_id>})
  MERGE (n)-[:<RELATIONSHIP>]->(m)
```

Example:
```cypher
LOAD CSV WITH HEADERS FROM 'file:///employees.csv' AS row
MERGE (e:Employee {id: row.employee_id})
SET e.name = row.name, e.salary = toInteger(row.salary)
MERGE (d:Department {name: row.department})
MERGE (e)-[:WORKS_IN]->(d)
```

**When to use:**
✓ Neo4j database import
✓ Direct LOAD CSV usage
✓ Production deployments

---

### RDF Triple Pattern

```turtle
Pattern: Generate RDF/OWL triples

Basic structure:
  @prefix ex: <http://example.org/> .
  ex:<entity1> a ex:<EntityType> ;
    ex:<property> "<value>" ;
    ex:<relationship> ex:<entity2> .
```

Example:
```turtle
@prefix ex: <http://example.org/company#> .

ex:employee_1 a ex:Employee ;
  ex:name "Alice" ;
  ex:salary "100000"^^xsd:integer ;
  ex:worksIn ex:engineering_dept .

ex:engineering_dept a ex:Department ;
  ex:name "Engineering" .
```

**When to use:**
✓ RDF/OWL knowledge graphs
✓ Semantic web integration
✓ SPARQL querying

---

### Property Graph JSON Pattern

```json
Pattern: Generate node/edge JSON structure

Structure:
  {
    "nodes": [
      {"id": "...", "type": "...", "properties": {...}}
    ],
    "edges": [
      {"source": "...", "target": "...", "type": "...", "properties": {...}}
    ]
  }
```

Example:
```json
{
  "nodes": [
    {"id": "e1", "type": "Employee", "properties": {"name": "Alice", "salary": 100000}},
    {"id": "d1", "type": "Department", "properties": {"name": "Engineering"}}
  ],
  "edges": [
    {"source": "e1", "target": "d1", "type": "WORKS_IN"}
  ]
}
```

**When to use:**
✓ API responses
✓ Graph visualization
✓ Tool interoperability

---

### Separated CSV Pattern

```
Pattern: Generate separate nodes.csv and edges.csv files

Structure:
  nodes.csv: id, type, property1, property2, ...
  edges.csv: source, target, type, property1, ...
```

Example nodes.csv:
```csv
id,type,name,salary
e1,Employee,Alice,100000
d1,Department,Engineering,
```

Example edges.csv:
```csv
source,target,type
e1,d1,WORKS_IN
```

**When to use:**
✓ Bulk import tools
✓ Data interchange
✓ Intermediate format

---

## Data Type Inference Patterns

### String Type Pattern

```
Detection:
  - Text columns (names, descriptions)
  - Non-numeric values
  - Contains spaces or special characters

Example:
  person_name → String
  description → String
  email → String
```

---

### Integer Type Pattern

```
Detection:
  - Numeric whole numbers
  - No decimal points
  - Often used for IDs, counts

Example:
  employee_id → Integer
  age → Integer
  count → Integer
```

---

### Float Type Pattern

```
Detection:
  - Decimal numbers
  - Scientific notation
  - Price/salary data

Example:
  salary → Float
  price → Float
  rating → Float
```

---

### DateTime Type Pattern

```
Detection:
  - ISO 8601 format: YYYY-MM-DD
  - Timestamps: YYYY-MM-DD HH:MM:SS
  - Common date patterns

Example:
  birth_date → Date (YYYY-MM-DD)
  created_at → DateTime (YYYY-MM-DD HH:MM:SS)
  updated_at → DateTime
```

---

### Boolean Type Pattern

```
Detection:
  - True/False values
  - Yes/No values
  - 1/0 values (sometimes ambiguous)

Example:
  is_active → Boolean
  is_verified → Boolean
  active → Boolean
```

---

### Reference Type Pattern

```
Detection:
  - Foreign key columns (ends with _id)
  - Values that match IDs in other columns
  - Used for relationship detection

Example:
  manager_id → Reference (to Person.id)
  company_id → Reference (to Company.id)
  department_id → Reference (to Department.id)
```

---

## Deduplication Patterns

### Entity Merge Pattern

```
Pattern: Multiple rows with same entity merge into single node

Input CSV:
  paper_id, title, author
  P001, Deep Learning, Alice
  P001, Deep Learning, Bob

Processing:
  1. Detect duplicate paper_id
  2. Create single Paper node for P001
  3. Create multiple AUTHORED edges (one per author)

Output Nodes:
  (:Paper {id: "P001", title: "Deep Learning"})
  (:Researcher {name: "Alice"})
  (:Researcher {name: "Bob"})

Output Edges:
  (:Researcher {name: "Alice"})-[:AUTHORED]->(:Paper)
  (:Researcher {name: "Bob"})-[:AUTHORED]->(:Paper)
```

**When to use:**
✓ Many-to-many relationships
✓ Normalized data (repeating headers)
✓ Authors/contributors lists

---

### Edge Deduplication Pattern

```
Pattern: Duplicate relationships are merged

Input CSV:
  person_id, person_name, company_id
  1, Alice, C001
  1, Alice, C001

Detection:
  - Same source, same target, same type
  - Can be merged or kept as single edge

Strategy:
  Keep single edge: (Person 1)-[:WORKS_AT]->(Company C001)
```

**When to use:**
✓ Removing redundant edges
✓ Ensuring unique relationships
✓ Data quality

---

### Identity Merge Pattern

```
Pattern: Use explicit ID field for merging

Configuration:
  - Define ID column per entity type
  - Use ID for MERGE operations
  - Prevent duplicate nodes

Example:
  Person uses: employee_id
  Company uses: company_name
  Department uses: department_id

Ensures:
  - One Person node per unique employee_id
  - One Company node per unique name
  - One Department node per unique id
```

**When to use:**
✓ Guaranteed unique identifiers
✓ Production data
✓ Reference integrity

---

## Error Handling Patterns

### Missing Value Pattern

```
Pattern: Handle NULL or empty values

Strategies:
  1. Ignore: Skip row or column
  2. Default: Use default value
  3. Skip relationship: Don't create edge

Example:
  manager_id = NULL → Don't create REPORTS_TO relationship
  department = "" → Set to "Unknown"
```

---

### Data Validation Pattern

```
Pattern: Validate data before loading

Checks:
  - Required fields not empty
  - Data types match schema
  - References exist in source
  - No circular dependencies (for hierarchies)

Example:
  If manager_id = 999 doesn't exist
  - Log warning
  - Skip relationship
  - Continue processing
```

---

### Type Conversion Pattern

```
Pattern: Convert data to expected types

Examples:
  "100000" (String) → 100000 (Integer)
  "2024-01-15" (String) → DateTime
  "true" (String) → Boolean
  "3.14" (String) → Float
```

---

## Best Practices

✓ **Use stable identifiers** – Choose consistent ID columns
✓ **Handle duplicates explicitly** – Define merge strategy
✓ **Validate data quality** – Check before loading
✓ **Document assumptions** – Record entity detection rules
✓ **Test with samples** – Validate before full import
✓ **Normalize entity names** – Prevent duplicate entities
✓ **Handle missing values** – Define NULL handling strategy
✓ **Version configurations** – Track mapping changes
✓ **Monitor relationships** – Validate relationship direction
✓ **Keep audit trail** – Log transformation decisions

---

See [example-loaders.md](../examples/example-loaders.md) for complete CSV loader implementation examples.


