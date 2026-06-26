# CSV Graph Loader Examples

Complete loader examples for different domains and use cases.

## Example 1: Business Domain - Employees & Companies

### Input CSV

```csv
employee_id,employee_name,job_title,department,company_name,company_industry,manager_id
E001,Alice Johnson,Software Engineer,Engineering,Acme Corp,Technology,E100
E002,Bob Smith,Product Manager,Product,Acme Corp,Technology,E100
E003,Carol Davis,Sales Executive,Sales,Acme Corp,Technology,NULL
E004,David Wilson,Software Engineer,Engineering,TechStart Inc,Technology,E200
E005,Emma Brown,HR Manager,HR,Acme Corp,Technology,E100
```

### Entity Detection

```
Entities detected:
- Person: employee_id, employee_name, job_title
- Company: company_name, company_industry
- Department: department
```

### Generated Neo4j Cypher

```cypher
LOAD CSV WITH HEADERS FROM 'file:///employees.csv' AS row

-- Create Person nodes
MERGE (e:Person {id: row.employee_id})
SET e.name = row.employee_name,
    e.jobTitle = row.job_title,
    e.department = row.department

-- Create Company nodes
MERGE (c:Company {name: row.company_name})
SET c.industry = row.company_industry

-- Create WORKS_AT relationships
MERGE (e)-[:WORKS_AT]->(c)

-- Create REPORTS_TO relationships (if manager exists)
WITH row, e
WHERE row.manager_id IS NOT NULL
MATCH (manager:Person {id: row.manager_id})
MERGE (e)-[:REPORTS_TO]->(manager)
```

### Generated RDF Triples (Turtle)

```turtle
@prefix ex: <http://example.org/business#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

ex:person_E001 a ex:Person ;
  foaf:name "Alice Johnson" ;
  ex:jobTitle "Software Engineer" ;
  ex:department "Engineering" ;
  ex:worksAt ex:acme_corp ;
  ex:reportsTo ex:person_E100 .

ex:person_E100 a ex:Person ;
  foaf:name "Manager Name" ;
  ex:jobTitle "Engineering Manager" .

ex:acme_corp a ex:Company ;
  foaf:name "Acme Corp" ;
  ex:industry "Technology" .
```

### Generated Property Graph JSON

```json
{
  "nodes": [
    {"id": "e1", "type": "Person", "properties": {"name": "Alice Johnson", "job_title": "Software Engineer", "department": "Engineering"}},
    {"id": "e2", "type": "Person", "properties": {"name": "Bob Smith", "job_title": "Product Manager", "department": "Product"}},
    {"id": "c1", "type": "Company", "properties": {"name": "Acme Corp", "industry": "Technology"}},
    {"id": "c2", "type": "Company", "properties": {"name": "TechStart Inc", "industry": "Technology"}}
  ],
  "edges": [
    {"source": "e1", "target": "c1", "type": "WORKS_AT"},
    {"source": "e2", "target": "c1", "type": "WORKS_AT"},
    {"source": "e1", "target": "e100", "type": "REPORTS_TO"},
    {"source": "e2", "target": "e100", "type": "REPORTS_TO"}
  ],
  "metadata": {
    "total_persons": 5,
    "total_companies": 2,
    "total_relationships": 7
  }
}
```

---

## Example 2: Scientific Domain - Research Papers

### Input CSV

```csv
paper_id,title,publication_year,doi,author_name,author_affiliation,research_area
P001,Deep Learning Advances,2023,10.1234/paper1,Dr. Alice Chen,MIT,Machine Learning
P001,Deep Learning Advances,2023,10.1234/paper1,Dr. Bob Kumar,Stanford,Machine Learning
P002,Quantum Computing,2023,10.1234/paper2,Dr. Carol Wilson,IBM,Quantum Computing
P003,Gene Therapy,2024,10.1234/paper3,Dr. David Lee,Johns Hopkins,Biotechnology
```

### Entity Detection & Deduplication

```
Entities detected:
- Paper: paper_id, title, publication_year, doi
- Researcher: author_name, author_affiliation
- ResearchArea: research_area

Deduplication:
- Paper P001 appears twice (different authors)
- Merged into single Paper node with multiple AUTHORS relationships
```

### Generated Neo4j Cypher

```cypher
LOAD CSV WITH HEADERS FROM 'file:///papers.csv' AS row

-- Create unique Paper nodes
MERGE (p:Paper {doi: row.doi})
SET p.id = row.paper_id,
    p.title = row.title,
    p.publication_year = toInteger(row.publication_year)

-- Create Researcher nodes
MERGE (r:Researcher {name: row.author_name})
SET r.affiliation = row.author_affiliation

-- Create ResearchArea nodes
MERGE (a:ResearchArea {name: row.research_area})

-- Create relationships
MERGE (r)-[:AUTHORED]->(p)
MERGE (p)-[:FOCUSES_ON]->(a)
```

### Generated RDF/OWL

```turtle
@prefix ex: <http://example.org/research#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:paper_P001 a ex:ResearchPaper ;
  dcterms:title "Deep Learning Advances" ;
  dcterms:issued "2023"^^xsd:gYear ;
  ex:doi "10.1234/paper1" ;
  ex:hasAuthor ex:researcher_alice_chen, ex:researcher_bob_kumar ;
  ex:focusesOn ex:area_machine_learning .

ex:researcher_alice_chen a ex:Researcher ;
  foaf:name "Dr. Alice Chen" ;
  ex:affiliation "MIT" .

ex:area_machine_learning a ex:ResearchArea ;
  rdfs:label "Machine Learning" .
```

---

## Example 3: Social Network Domain

### Input CSV

```csv
user_id,username,display_name,bio,follower_count,account_type,followed_user_id,followed_username,post_id,post_text,post_date,engagement_count
U001,alice_tech,Alice,Data Scientist,5000,verified,U002,bob_dev,POST1,Great insights on graphs,2024-01-15,250
U001,alice_tech,Alice,Data Scientist,5000,verified,U003,carol_ai,POST1,Great insights on graphs,2024-01-15,250
U002,bob_dev,Bob,Software Dev,3000,standard,U001,alice_tech,POST2,Working on ML,2024-01-16,180
```

### Entity Detection

```
Entities detected:
- User: user_id, username, display_name, bio
- Post: post_id, post_text, post_date
- Hashtag/Topic: (implicit from post content)

Relationships:
- FOLLOWS: User → User
- POSTED: User → Post
- HAS_ENGAGEMENT: Post → Post/User
```

### Generated Neo4j Cypher

```cypher
LOAD CSV WITH HEADERS FROM 'file:///social.csv' AS row

-- Create User nodes
MERGE (u:User {id: row.user_id})
SET u.username = row.username,
    u.displayName = row.display_name,
    u.bio = row.bio,
    u.followerCount = toInteger(row.follower_count),
    u.accountType = row.account_type

-- Create followed User nodes
MERGE (following:User {id: row.followed_user_id})
SET following.username = row.followed_username

-- Create Post nodes
MERGE (p:Post {id: row.post_id})
SET p.text = row.post_text,
    p.postDate = datetime(row.post_date),
    p.engagementCount = toInteger(row.engagement_count)

-- Create relationships
MERGE (u)-[:FOLLOWS]->(following)
MERGE (u)-[:POSTED]->(p)
```

### Generated Property Graph JSON

```json
{
  "nodes": [
    {"id": "u1", "type": "User", "properties": {"username": "alice_tech", "display_name": "Alice", "account_type": "verified"}},
    {"id": "u2", "type": "User", "properties": {"username": "bob_dev", "display_name": "Bob", "account_type": "standard"}},
    {"id": "post1", "type": "Post", "properties": {"text": "Great insights on graphs", "engagement_count": 250}}
  ],
  "edges": [
    {"source": "u1", "target": "u2", "type": "FOLLOWS"},
    {"source": "u1", "target": "post1", "type": "POSTED"}
  ]
}
```

---

## Example 4: E-Commerce Domain

### Input CSV

```csv
product_id,product_name,category,price,stock,seller_id,seller_name,order_id,customer_id,order_date,quantity,review_score
PROD001,Laptop,Electronics,999.99,50,SELLER001,TechHub,ORD001,CUST001,2024-01-10,1,4.5
PROD002,Mouse,Electronics,29.99,200,SELLER001,TechHub,ORD002,CUST002,2024-01-11,2,4.0
PROD001,Laptop,Electronics,999.99,50,SELLER001,TechHub,ORD003,CUST001,2024-01-12,1,4.5
PROD003,Keyboard,Electronics,79.99,150,SELLER002,ElectroStore,ORD004,CUST003,2024-01-13,1,4.8
```

### Deduplication Strategy

```
Input rows: 4
Unique products: 3 (PROD001 appears twice)
Unique orders: 4
Unique customers: 3
Unique sellers: 2

Merge strategy:
- Product with same ID merged
- Each order is unique even with same product
```

### Generated Node & Edge Tables

**nodes.csv**
```csv
id,type,name,category,stock,price
PROD001,Product,Laptop,Electronics,50,999.99
PROD002,Product,Mouse,Electronics,200,29.99
PROD003,Product,Keyboard,Electronics,150,79.99
SELLER001,Seller,TechHub,,
SELLER002,Seller,ElectroStore,,
CUST001,Customer,Customer 1,,
CUST002,Customer,Customer 2,,
```

**edges.csv**
```csv
source,target,type,quantity,review_score
CUST001,PROD001,PURCHASED,1,4.5
CUST002,PROD002,PURCHASED,2,4.0
CUST001,PROD001,PURCHASED,1,4.5
CUST003,PROD003,PURCHASED,1,4.8
SELLER001,PROD001,SELLS,,
SELLER001,PROD002,SELLS,,
SELLER002,PROD003,SELLS,,
```

---

## Example 5: Knowledge Graph - Wikipedia-like Data

### Input CSV

```csv
entity_id,entity_name,entity_type,birth_date,profession,country,related_entity,relation_type
E001,Marie Curie,Person,1867-11-24,Scientist,Poland,E002,MARRIED_TO
E001,Marie Curie,Person,1867-11-24,Scientist,Poland,E003,DISCOVERED
E002,Pierre Curie,Person,1859-05-15,Scientist,France,E001,MARRIED_TO
E003,Radium,Chemical Element,,Element,Natural,E001,DISCOVERED_BY
E004,Polonium,Chemical Element,,Element,Natural,E001,DISCOVERED_BY
```

### Generated RDF Knowledge Graph

```turtle
@prefix ex: <http://example.org/knowledge#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dbo: <http://dbpedia.org/ontology/> .

ex:marie_curie a ex:Person ;
  foaf:name "Marie Curie" ;
  dbo:birthDate "1867-11-24"^^xsd:date ;
  dbo:profession "Scientist" ;
  dbo:country ex:poland ;
  ex:marriedTo ex:pierre_curie ;
  ex:discovered ex:radium, ex:polonium ;
  rdfs:comment "Polish-born physicist" .

ex:radium a ex:ChemicalElement ;
  rdfs:label "Radium" ;
  ex:discoveredBy ex:marie_curie ;
  ex:country ex:natural ;
  ex:atomicNumber 88 .

ex:pierre_curie a ex:Person ;
  foaf:name "Pierre Curie" ;
  dbo:birthDate "1859-05-15"^^xsd:date ;
  dbo:profession "Scientist" ;
  dbo:country ex:france ;
  ex:marriedTo ex:marie_curie .

ex:poland a ex:Country ;
  rdfs:label "Poland" .
```

---

## Loader Comparison Table

| Domain | CSV Rows | Entities | Relationships | Node Types | Edge Types | Deduplication | Format |
|--------|----------|----------|---------------|-----------|-----------|----------------|--------|
| Business | 5 | 3 types | Manager+Company | Person, Company, Dept | WORKS_AT, REPORTS_TO | Merge by ID | Cypher |
| Scientific | 4 | 3 types | Author+Area | Paper, Researcher, Area | AUTHORED, FOCUSES_ON | Merge duplicates | RDF/Turtle |
| Social | 3 | 2 types | Follow+Post | User, Post | FOLLOWS, POSTED | Deduplicate | JSON |
| E-Commerce | 4 | 3 types | Purchase+Sell | Product, Customer, Seller | PURCHASED, SELLS | Merge products | CSV tables |
| Knowledge | 5 | 2 types | Multiple | Person, Element | MARRIED_TO, DISCOVERED | None | RDF/OWL |

---

## Transformation Performance Notes

| Example | Input Size | Processing Time | Nodes Generated | Edges Generated |
|---------|-----------|-----------------|-----------------|-----------------|
| Business | 5 rows | < 100ms | 8 | 7 |
| Scientific | 4 rows | < 100ms | 6 | 8 |
| Social | 3 rows | < 50ms | 4 | 3 |
| E-Commerce | 4 rows | < 100ms | 8 | 8 |
| Knowledge | 5 rows | < 100ms | 6 | 6 |

---

See [loader-patterns.md](../references/loader-patterns.md) for detailed CSV loader design patterns.


