# Seed Configuration

Seed files provide cold-start vocabularies for specific domain wikis. Stored in this directory, one file per domain.

## File Format

```markdown
---
name: my-seed-name              # Unique identifier, referenced in meta.yaml
display_name: Display Name
source: Based on standard ontology name
url: Reference link to standard ontology
applies_to: Description of applicable research domains
validator: validators/xxx.md    # Optional, associated external validator
---

# Seed Title

## Vocabulary Category 1

| Standard Concept | Description | Wiki Mapping |
|-----------------|-------------|--------------|
| ConceptA | ... | entities/ |
| ConceptB | ... | concepts/ |

## Relationship Templates

```
EntityA --relation_type--> EntityB
```

## Non-mixing Rules

| Easily Confused Concept Pair | Difference |
|------------------------------|------------|
| A ≠ B | Explanation |
```

## How to Reference

Set `seed` field in wiki's `meta.yaml`:

```yaml
name: my-research-topic
ontology_type: domain
seed: my-seed-name        # Corresponds to name in seed file frontmatter
```

Agent reads corresponding seed file before first ingest.

## Writing Principles

1. **Vocabulary should be concise**. Only list 20-50 core concepts for the domain, don't try to cover entire standard
2. **Non-mixing rules are core value**. Concepts Agent most easily confuses, write clear distinctions
3. **Relationship templates should be concrete**. Don't just list relationship type names, give complete `A --type--> B` examples
4. **Allow Chinese**. Concept names use standard English, but explanations and non-mixing rules use Chinese (or target language)
5. **Declaring validator is optional**. If domain has available external validator (e.g., FIBO MCP), point to it in frontmatter `validator` field

## Currently Available Seeds

| File | Domain | Concept Count |
|------|--------|---------------|
| `fibo-pensions.md` | Enterprise annuity/Pensions | ~30 |
