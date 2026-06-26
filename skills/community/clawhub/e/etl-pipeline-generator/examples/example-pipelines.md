# ETL Pipeline Examples

Complete pipeline examples for different domains and use cases.

## Example 1: E-Commerce Customer Data Pipeline

### Scenario
Ingest customer order data from multiple sources (CSV, API, database) into a knowledge graph.

### Pipeline Configuration

```yaml
name: ecommerce_customer_graph
description: Ingest customer order data into knowledge graph

stages:
  extract:
    sources:
      - name: customer_csv
        type: csv
        location: data/customers.csv
      - name: orders_api
        type: api
        endpoint: https://api.ecommerce.com/orders
        auth: bearer_token
      - name: products_db
        type: database
        connection: postgresql://db.example.com:5432/products

  transform:
    operations:
      - normalize_customer_names
      - convert_dates_to_iso8601
      - infer_customer_location_from_address
      - deduplicate_customers
      - validate_email_format
      - enrich_with_customer_tier
    validation:
      - required_fields: [customer_id, name, email]
      - data_types: {age: integer, created_at: datetime}
      - value_ranges: {age: {min: 18, max: 150}}

  load:
    target: neo4j
    connection:
      uri: bolt://neo4j.example.com:7687
      database: ecommerce_kg
    method: bulk_import
    batch_size: 5000
    error_handling: skip_invalid_records

scheduling:
  trigger: daily
  time: "02:00 UTC"
  timeout: 3600
  retry:
    max_attempts: 3
    backoff: exponential

monitoring:
  alerts:
    - condition: execution_time > 1800
      action: notify_admin
    - condition: error_rate > 0.05
      action: pause_and_alert
```

### Generated DAG

```
Extract:
  ├─ Read CSV (customers.csv)
  ├─ Fetch API (orders endpoint)
  └─ Query Database (products)
         ↓
Transform:
  ├─ Normalize Names
  ├─ Convert Dates
  ├─ Infer Location
  ├─ Deduplicate
  └─ Validate Data
         ↓
Quality Check:
  ├─ Validate Schema
  ├─ Check Data Types
  └─ Verify Row Counts
         ↓
Load:
  ├─ Create Customer Nodes
  ├─ Create Product Nodes
  ├─ Create ORDER relationships
  └─ Create PURCHASED_FROM relationships
         ↓
Verify:
  ├─ Count Loaded Nodes
  ├─ Verify Relationships
  └─ Generate Report
```

### Generated Python Script

```python
import pandas as pd
from neo4j import GraphDatabase
from datetime import datetime

class ECommerceGraphPipeline:
    def __init__(self, neo4j_uri, neo4j_password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=("neo4j", neo4j_password))
        self.execution_log = []
    
    def extract(self):
        # Extract from CSV
        customers_df = pd.read_csv('data/customers.csv')
        
        # Extract from API
        import requests
        response = requests.get('https://api.ecommerce.com/orders')
        orders_df = pd.json_normalize(response.json()['orders'])
        
        # Extract from Database
        import sqlalchemy
        engine = sqlalchemy.create_engine('postgresql://...')
        products_df = pd.read_sql_table('products', engine)
        
        return customers_df, orders_df, products_df
    
    def transform(self, customers_df, orders_df, products_df):
        # Normalize customer names
        customers_df['name'] = customers_df['name'].str.strip().str.title()
        
        # Convert dates
        customers_df['created_at'] = pd.to_datetime(customers_df['created_at'])
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        
        # Deduplicate
        customers_df = customers_df.drop_duplicates(subset=['email'])
        
        # Validate
        assert customers_df['email'].str.contains(r'@').all(), "Invalid emails"
        
        return customers_df, orders_df, products_df
    
    def load(self, customers_df, orders_df, products_df):
        with self.driver.session() as session:
            # Load customers
            for _, row in customers_df.iterrows():
                session.run(
                    "MERGE (c:Customer {email: $email}) "
                    "SET c.name = $name, c.created_at = $created_at",
                    email=row['email'], name=row['name'], 
                    created_at=row['created_at'].isoformat()
                )
            
            # Load products
            for _, row in products_df.iterrows():
                session.run(
                    "MERGE (p:Product {sku: $sku}) "
                    "SET p.name = $name, p.price = $price",
                    sku=row['sku'], name=row['name'], price=row['price']
                )
            
            # Load orders and relationships
            for _, row in orders_df.iterrows():
                session.run(
                    "MATCH (c:Customer {email: $email}) "
                    "MATCH (p:Product {sku: $sku}) "
                    "MERGE (c)-[:PURCHASED]->(p) "
                    "SET r.quantity = $quantity, r.order_date = $order_date",
                    email=row['customer_email'], sku=row['product_sku'],
                    quantity=row['quantity'], order_date=row['order_date'].isoformat()
                )
    
    def execute(self):
        try:
            print("Starting ETL pipeline...")
            customers, orders, products = self.extract()
            print(f"Extracted {len(customers)} customers, {len(orders)} orders")
            
            customers, orders, products = self.transform(customers, orders, products)
            print(f"Transformed data, {len(customers)} valid customers")
            
            self.load(customers, orders, products)
            print("Successfully loaded data to Neo4j")
            
            return {"status": "SUCCESS", "timestamp": datetime.now().isoformat()}
        
        except Exception as e:
            print(f"Pipeline failed: {str(e)}")
            return {"status": "FAILED", "error": str(e), "timestamp": datetime.now().isoformat()}
        
        finally:
            self.driver.close()

if __name__ == "__main__":
    pipeline = ECommerceGraphPipeline("bolt://localhost:7687", "password")
    result = pipeline.execute()
    print(result)
```

### Execution Metrics

```json
{
  "pipeline_id": "ecommerce_customer_graph",
  "execution_date": "2024-04-09T02:00:00Z",
  "duration_seconds": 1245,
  "status": "SUCCESS",
  "stages": [
    {
      "name": "extract",
      "status": "SUCCESS",
      "duration_seconds": 180,
      "records_processed": 45000,
      "sources": {
        "customers_csv": 10000,
        "orders_api": 35000,
        "products_db": 5000
      }
    },
    {
      "name": "transform",
      "status": "SUCCESS",
      "duration_seconds": 320,
      "records_processed": 44950,
      "dropped_records": 50,
      "transformations": {
        "normalized_names": 10000,
        "converted_dates": 45000,
        "deduplicated": 50,
        "validated": 44950
      }
    },
    {
      "name": "load",
      "status": "SUCCESS",
      "duration_seconds": 745,
      "records_loaded": 44950,
      "nodes_created": 10050,
      "relationships_created": 35000
    }
  ]
}
```

---

## Example 2: Scientific Research Data Pipeline

### Scenario
Ingest research paper data from multiple databases and create knowledge graph of researchers, papers, and collaborations.

### Pipeline Configuration

```yaml
name: research_knowledge_graph
description: Build knowledge graph from research data

extract:
  sources:
    - name: arxiv_api
      type: api
      endpoint: https://export.arxiv.org/api/query
      query_params:
        search_query: "all"
        start: 0
        max_results: 10000
    
    - name: pubmed_database
      type: database
      connection: postgresql://pubmed.example.com/papers
      query: "SELECT * FROM papers WHERE published_year >= 2020"
    
    - name: dblp_xml
      type: text
      location: s3://research-data/dblp.xml
      format: xml

transform:
  operations:
    - parse_author_names
    - extract_affiliations
    - infer_collaborations
    - detect_research_areas
    - normalize_citations
    - validate_identifiers
  enrichment:
    - add_author_metadata_from_orcid
    - add_institution_data
    - add_citation_counts

load:
  target: rdf
  connection:
    sparql_endpoint: http://rdf.example.com:8080/sparql
    named_graph: http://research.example.org/kg
  format: turtle
  batch_size: 1000
```

### Generated RDF Output Sample

```turtle
@prefix ex: <http://research.example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:paper_2024_001 a ex:ResearchPaper ;
  dcterms:title "Deep Learning for Knowledge Graphs" ;
  dcterms:creator ex:author_alice, ex:author_bob ;
  dcterms:issued "2024-04-05"^^xsd:date ;
  ex:inResearchArea ex:area_machine_learning ;
  ex:citationCount 42 .

ex:author_alice a foaf:Person ;
  foaf:name "Dr. Alice Smith" ;
  foaf:mbox <mailto:alice@example.edu> ;
  foaf:workplaceHomepage <http://example.edu> ;
  ex:collaboratesWith ex:author_bob .

ex:author_bob a foaf:Person ;
  foaf:name "Dr. Bob Johnson" ;
  foaf:workplaceHomepage <http://stanford.edu> ;
  ex:collaboratesWith ex:author_alice .

ex:area_machine_learning a ex:ResearchArea ;
  dcterms:title "Machine Learning" ;
  ex:hasSubArea ex:area_deep_learning .
```

---

## Example 3: Healthcare Data Pipeline

### Scenario
Integrate patient, provider, and treatment data from EHR systems into healthcare knowledge graph.

### Pipeline Definition

```yaml
name: healthcare_kg_pipeline
description: Integrate healthcare data into knowledge graph

extract:
  sources:
    - name: ehr_system
      type: database
      connection: oracle://ehr.hospital.local:1521/EHR
      tables: [patients, providers, treatments, diagnoses]
      privacy:
        - anonymize_patient_id
        - mask_pii
    
    - name: claims_database
      type: database
      connection: postgresql://claims.insurance.local/claims
      query: SELECT * FROM claims WHERE service_date >= CURRENT_DATE - INTERVAL '1 year'

transform:
  operations:
    - standardize_diagnosis_codes_to_icd10
    - normalize_medication_names_to_rxnorm
    - infer_treatment_relationships
    - calculate_patient_risk_scores
    - detect_adverse_events
    - validate_clinical_data
  privacy:
    - apply_hipaa_compliance
    - anonymize_identifiers
    - redact_sensitive_information

load:
  target: neo4j
  connection:
    uri: bolt://neo4j.hospital.local:7687
  method: streaming
  batch_size: 100
  error_handling:
    strategy: fail_safe
    log_location: /var/log/etl/healthcare_errors.log

quality_gates:
  - name: completeness_check
    rule: records_with_null_required_fields < 0.01
  - name: consistency_check
    rule: icd10_codes_valid >= 0.99
  - name: timeliness_check
    rule: data_freshness <= 24_hours
```

---

## Example 4: IoT Sensor Data Pipeline

### Scenario
Real-time ingestion of IoT sensor data into time-series graph database.

### Pipeline Configuration

```yaml
name: iot_sensor_graph
description: Real-time sensor data ingestion

extract:
  source:
    type: stream
    protocol: mqtt
    broker: mqtt.iot.example.com
    topics:
      - sensors/temperature/*
      - sensors/humidity/*
      - sensors/pressure/*
    batch_timeout: 5_seconds

transform:
  operations:
    - parse_sensor_messages
    - aggregate_by_location
    - detect_anomalies
    - calculate_moving_averages
    - infer_equipment_health
  real_time_rules:
    - condition: temperature > 80
      action: create_alert_node
    - condition: humidity < 30
      action: flag_dry_condition

load:
  target: arangodb
  connection:
    url: http://arangodb.example.com:8529
    database: iot_kg
  method: streaming
  time_series_retention: 30_days

execution_mode: continuous
error_recovery: checkpoint_resume
```

---

## Example 5: Text Processing Pipeline

### Scenario
Extract named entities from documents and build knowledge graph from document relationships.

### Pipeline Definition

```yaml
name: document_knowledge_extraction
description: Extract knowledge from documents

extract:
  source:
    type: text
    location: s3://documents/corpus/
    filter: "*.pdf"
    formats: [pdf, txt, docx]

transform:
  stages:
    - parse_documents
    - extract_named_entities:
        entity_types: [PERSON, ORGANIZATION, LOCATION, CONCEPT]
    - extract_relationships:
        patterns: [WORKS_AT, LOCATED_IN, FOUNDED_BY]
    - summarize_documents
    - extract_keywords
    - build_concept_hierarchy
    
  nlp_pipeline:
    tokenizer: spacy
    ner_model: en_core_web_lg
    dependency_parser: spacy
    relation_extractor: custom_model

load:
  target: neo4j
  method: batch
  batch_size: 500

metrics:
  - entities_extracted
  - relationships_discovered
  - confidence_scores
  - document_coverage
```

---

## Pipeline Patterns Comparison

| Pattern | Data Source | Volume | Latency | Complexity | Example |
|---------|-------------|--------|---------|-----------|---------|
| Batch | File/DB | Large | Hours | Medium | E-Commerce |
| Streaming | Message Queue | Continuous | Seconds | High | IoT Sensors |
| API Poll | REST/GraphQL | Medium | Minutes | Low | Data Feeds |
| Database Sync | Database | Large | Hourly | Medium | Healthcare |
| Document Process | Files/Text | Large | Hours | High | Text Mining |

---

See [pipeline-patterns.md](../references/pipeline-patterns.md) for detailed ETL pipeline design patterns.


