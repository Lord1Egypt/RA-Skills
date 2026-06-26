# Seed Ontologies: Guide Wiki Structure with Standard Vocabularies

> Seeds are optional cold-start references, not mandatory dependencies.
> Domains without seeds, wikis grow freely—seeds just make starting more standardized.

## Mechanism

### What is a Seed

A seed is a domain vocabulary configuration containing:

| Content | Purpose |
|---------|---------|
| **Standard terms** | Provide naming reference for wiki page slugs and titles |
| **Classification system** | Hint to Agent what dimensions this domain typically needs to cover |
| **Relationship templates** | Standard inter-entity relationship types (manages, regulates, invests_in, etc.) |
| **Non-mixing rules** | Label common concept confusions, prevent Agent from mixing them up |

Seed files are stored in `seeds/` directory, one file per domain.

### How to Reference

When creating new wiki, declare which seed to use in `meta.yaml`:

```yaml
name: my-research-topic
ontology_type: domain
seed: fibo-pensions          # References seeds/fibo-pensions.md
```

Agent reads corresponding seed file before first ingest. If `seed` field is empty or not set, skip seed, wiki grows freely.

### What It Doesn't Do

- No OWL/RDF import—wiki is markdown, not semantic web
- No forced standard terms—if domain actual usage differs, use actual, but label mapping relationship
- No override of user customization—seed is just starting reference, wiki evolves beyond seed scope

---

## Available Seeds

| Seed File | Coverage Domain | Based On |
|-----------|-----------------|----------|
| `seeds/fibo-pensions.md` | Enterprise annuity, pension management | FIBO (EDM Council) |
| *(to be extended)* | | |

### Referenceable Industry Standard Ontologies

When writing new seeds, can reference these standards:

| Standard | Coverage Domain | Applicable Scenario | Reference Link |
|----------|-----------------|---------------------|----------------|
| **FIBO** | Full financial industry | Banking, insurance, funds, pensions | spec.edmcouncil.org/fibo |
| **XBRL Taxonomy** | Financial reporting | Listed company financial data analysis | xbrl.org |
| **Schema.org** | General entities | People, organizations, events, places | schema.org |
| **SKOS** | Knowledge organization | Classification systems, concept hierarchies | w3.org/2004/02/skos |
| **Dublin Core** | Document metadata | Source page frontmatter | dublincore.org |
| **FOAF** | People & social | Person research (cognitive type) | xmlns.com/foaf |

| Research Type | Recommended Seed/Standard |
|---------------|---------------------------|
| Enterprise annuity / pensions | `fibo-pensions` |
| Public funds | FIBO-SEC (Fund), can write new seed based on this |
| Listed company analysis | FIBO-BP + XBRL |
| Macro economy | No standard seed (free growth) |
| Person cognition | FOAF + custom mental model types |
| General topics | Schema.org |

---

## How Agent Uses Seeds

### During Ingest

```
1. Read source file, extract key entities
2. If meta.yaml declared seed → Read seed file, reference vocabulary:
   - Does this entity have a standard name? → Use standard name as page slug
   - What standard category does this entity belong to? → Place in corresponding entities/ or concepts/
   - Does it touch non-mixing rules? → Clearly distinguish in page
3. Execute normal ingest subsequent steps
```

**Example** (using financial domain):
```
Source file mentions a bank's pension business
→ Reference seed vocabulary: This is an Organization, serving as Trustee role
→ Create entities/bank-x.md (institution page)
→ Label in relationships that bank-x serves as trustee role
→ Don't create entities/bank-x-trustee.md (organization ≠ role, obey non-mixing rules)
```

### During Lint

```
1. If meta.yaml declared seed → Read seed file
2. Check if page naming aligns with seed vocabulary
3. Check if non-mixing rules are violated
4. Check if key dimensions from seed are uncovered
5. Output alignment score in health report
```

### During Query

```
User asks about a domain term
→ Agent knows the term's standard position and related concepts from seed vocabulary
→ Search expands to related concepts
→ More comprehensive answer
```

---

## External Validators

Seed files can declare associated external validators (frontmatter `validator` field).
Validators provide runtime logic validation, beyond seed's static vocabulary—validating domain/range legality of relations, whether entities have required relations, etc.

Validator configurations are stored in `validators/` directory. See specific validator documentation for details.

Current available validators:

| Validator | Description | Corresponding Seed |
|-----------|-------------|-------------------|
| `validators/fibo-mcp.md` | FIBO SPARQL logic validation (627K inferred triples) | `fibo-pensions` |

**Validators are optional enhancements**. When unreachable, lint falls back to schema.py format validation + seed static rules, not affecting core flow.

---

## Limitations

1. **Seeds are starting points, not endpoints**. Wiki accumulation produces concepts not in seeds
2. **Standard terms may differ from industry actual usage**. Use industry terminology, but label standard term mapping in pages
3. **Not all domains have mature standard ontologies**. Domains without suitable seeds, wikis grow freely
4. **Seeds themselves evolve**. When standards update, wikis don't need to sync—seeds only referenced once at cold start
