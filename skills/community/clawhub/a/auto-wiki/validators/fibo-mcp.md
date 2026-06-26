# FIBO MCP: Runtime Logic Validator

> External validator, validates wiki knowledge logic structure via SPARQL queries to FIBO ontology (627K inferred triples).
> Optional enhancement—falls back to schema.py format validation + seed static rules when unreachable.
>
> Based on [NeuroFusionAI/fibo-mcp](https://github.com/NeuroFusionAI/fibo-mcp) (MIT), which materializes the FIBO ontology into a queryable MCP SPARQL endpoint.

## Service Information

| Item | Value |
|------|-------|
| Endpoint | `https://mcp.ablemind.cc/fibomcp/mcp` |
| Protocol | MCP Streamable HTTP (requires `Mcp-Session-Id`), HTTPS via Cloudflare |
| Tools | Only `sparql` (no search) |
| Data Scale | 627,712 triples (includes OWL-RL inference materialization) |

## Calling Method

Send `tools/call` request via MCP protocol, tool name = `sparql`, parameter is SPARQL query string.
Need to `initialize` first to get `Mcp-Session-Id`, subsequent requests include that header.

> **No user credentials needed**: `Mcp-Session-Id` is a standard session identifier for MCP Streamable HTTP transport (similar to HTTP Session), automatically obtained by the agent during `initialize`. No API key or secrets required from the user. The endpoint is a public read-only SPARQL query service.

## Three Validation Levels

schema.py validates page format (frontmatter field presence, type correctness).
FIBO SPARQL validates knowledge logic—three levels:

### 1. Logic Pathway: Domain/Range of Relations

Agent wrote a relation, is this relation valid in standard ontology?

**Query template**: Given a property name, query its domain and range.

```sparql
SELECT DISTINCT ?domainLabel ?rangeLabel WHERE {
  ?prop rdfs:label ?propLabel .
  FILTER(CONTAINS(LCASE(STR(?propLabel)), "{property_name}"))
  ?prop rdfs:domain ?domain . ?domain rdfs:label ?domainLabel .
  ?prop rdfs:range ?range . ?range rdfs:label ?rangeLabel .
}
```

**Example** (using `has trustee` as example, verified 2026-04-07):

| domain | range |
|--------|-------|
| business entity | trustee |
| trust | trustee |
| trust | controlling party |

-> If Agent writes `PensionProduct --hasTrustee--> X`, logic pathway invalid: PensionProduct not in domain.

### 2. Conditional Edges: Required Relations for Entities

Agent created an entity page, what required relations are needed?

**Query template**: Given a class URI, query its OWL constraints.

```sparql
SELECT DISTINCT ?onPropLabel ?restrictType ?valueLabel WHERE {
  <{class_uri}> rdfs:subClassOf ?r .
  { ?r owl:onProperty ?p . ?p rdfs:label ?onPropLabel .
    ?r owl:someValuesFrom ?v . ?v rdfs:label ?valueLabel .
    BIND("someValuesFrom" AS ?restrictType) }
  UNION
  { ?r owl:onProperty ?p . ?p rdfs:label ?onPropLabel .
    ?r owl:allValuesFrom ?v . ?v rdfs:label ?valueLabel .
    BIND("allValuesFrom" AS ?restrictType) }
}
```

`someValuesFrom` = entities of this class **must** have this relation (at least one).
`allValuesFrom` = values of this relation **can only** be specified type.

### 3. Type Hierarchy: Entity Classification Correctness

Agent marked entity as a type, does standard ontology have it?

**Query template**: Fuzzy search class name.

```sparql
SELECT DISTINCT ?label ?def WHERE {
  ?class rdfs:label ?label .
  FILTER(CONTAINS(LCASE(STR(?label)), "{keyword}"))
  OPTIONAL { ?class <http://www.w3.org/2004/02/skos/core#definition> ?def }
}
```

If not found, validator should prompt: "This type not in standard ontology, please confirm naming".

## Integration Method

Doesn't change Skill core flow, as optional enhancement layer for lint:

```
lint → schema.py format validation
     → External validator (if meta.yaml declared validator and reachable)
       ├─ Logic pathway: relation type domain/range match
       ├─ Conditional edges: required relations (someValuesFrom) missing
       └─ Type hierarchy: entity type in standard ontology
     → Health report
```

## Principles

- Don't hardcode FIBO constraints into schema.py—external reference, not internal rule
- Don't require wiki pages satisfy all OWL constraints—report missing, Agent judges whether to supplement
- Don't block ingest—logic validation only runs during lint, ingest prioritizes speed
- Skip silently when service unreachable—note "external validator unreachable, skipped" in health report
