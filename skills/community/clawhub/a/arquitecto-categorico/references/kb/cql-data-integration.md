# CQL Data Integration for Computational Science

Brown, K., Spivak, D.I., Wisnesky, R. (2019). Categorical Data Integration for Computational Science. CQL (Categorical Query Language) applied to computational science data sharing. Demonstrates functorial data migration for integrating quantum materials databases (OQMD, Catalysis).

Keywords: data integration, data migration, heterogeneous data, category theory, machine learning, density functional theory.

## CQL Overview

**CQL (Categorical Query Language).** Open-source query and data integration scripting language based on algebraic database formalism motivated by category theory. Distinct from relational, RDF, graph, and LINQ models.

Properties:
- Static guarantees of data integrity enforcement via rich constraint language.
- Complete provenance for all transformations.
- Seamless integration of programming languages into schema.

**CQL schema = Olog (ontology log).** Captures conceptual knowledge explicitly. Boxes = database tables or sets; arrows = foreign keys or functions; path equations = higher-level semantic meaning + data integrity constraints. A CQL schema is not merely a container for information but itself conveys important conceptual knowledge and distinguishes sensible from nonsensical instance data.

Use cases: financial data, health records, manufacturing service databases (Wisnesky et al.), materials science knowledge (Schultz, Ghani, Wisnesky, Breiner).

## Functorial Migration

**Functorial data migration.** CQL transformations are structure-preserving in both source and target schemas. Migration = application of Δ/Σ/Π induced by schema functor F: S_source → S_target.

Guarantee: correctness by construction — if the functor exists, migration respects integrity and constraints. Two forms of protection:
1. Static guarantee: data in algebraic database cannot violate constraints. Researcher can safely draw from external sources without worrying about constraint violation.
2. Structure preservation: data can only be migrated in a way that respects rules accompanying source schema.

Without these abstractions, users must write raw SQL scripts — error-prone and fragile to schema changes. General problem of checking if arbitrary schema mapping preserves constraints is undecidable; CQL automates this.

**Migration procedure:**
1. Define source schema S_source as category (CQL ologs).
2. Define target schema S_target.
3. Construct functor F: S_source → S_target capturing the translation.
4. CQL automatically generates Δ_F, Σ_F, Π_F.
5. Apply appropriate operator by migration type.
6. CQL guarantees correctness + automatic provenance.

### CQL-PROVENANCE

**Provenance.** Complete traceability of the origin of each migrated datum. Mechanism: functoriality preserves origin information through every transformation.

## Data Sharing Problem in Computational Science

**DFT (Density Functional Theory).** Popular tool in materials science; efficient prediction of electronic properties (stability) from chemical structure. Databases benefit the public: aid further computational studies, establish reference for comparison, facilitate property screening.

**Key challenges (Kitchin 2015, JPC 2016):**
- Tables and figures = current standard; machine readability sacrificed for flexibility.
- Heterogeneous formats: no standards for complex entities (symmetry analysis, pseudopotentials, density of states, DFT calculations).
- DFT calculation = no a priori restrictions on inputs or outputs.
- Formation energies depend on ensembles of calculations, not single calculations.
- Scientists can only share tiny fragments of structured raw data.

**OQMD (Open Quantum Materials Database).** Only major materials database that is relational (vs Materials Project, ICSD, NOMAD which use document models). Used as primary case study.

## Heterogeneity Factors

| Factor | Mitigation in CQL |
|--------|-----------------|
| Differing names for same concepts | Direct name mapping specification (overlap.py §1.2) |
| Implicit constants (undocumented) | Declare database-wide constants during migration (e.g., every OQMD calculation uses VASP) |
| Degree of denormalization | Map attributes to paths (Structures.x0 → Structure.cell_id.x0); unpack JSON fields via functions |
| Hidden structure (JSON attributes) | Functions to access specific parameters from JSON (params) |
| Different granularity levels | Low→high: leave attributes as NULLs; high→low: ignore excess attributes/FKs |
| Labelled nulls | CQL uses labelled nulls (distinct but unknown values behaving like variables) vs SQL NULLs |

## Case Studies — OQMD + Catalysis

**Two problems addressed:**
1. Data migration: OQMD → Catalysis (resulting instance has Catalysis schema and data from both databases).
2. Data integration: merge OQMD and Catalysis into new schema with overlapping and non-overlapping content.

**Key questions for each migration:**
- What tables/paths correspond to the same meaning? (overlap.py §1.1)
- What functions are required to translate between representations (unit conversion, formatting)? (javafuncs.py)
- Are there attributes not explicitly represented (constant or function of other attributes)? Compute in SQL while landing data or within CQL. (overlap.py §3)
- What filters apply if only a subset of records is needed?
- What is sufficient for two records to be considered the same despite different representation?

## Future Outlook

Surface DFT models (more complex than bulk materials): multiple structures per calculation, more complicated relations. Plan: demonstrate algebraic data integration utility in surface science. Broader: life sciences lack widespread data standardization; urgent need for "user-friendly tools targeting integration of heterogeneous datasets" (Gonçalves et al., 2014).

## Conclusion

Key open problems in data sharing: (1) lack of structured data, (2) tools to combine information from disparate datasets, (3) communication of data set nuances. CQL addresses all three via precise schema specification, functorial migration, and path equation constraints.

Code: https://github.com/kris-brown/cql_data_integration

Funding: KB supported by DoD/NDSEG Fellowship. Spivak and Wisnesky are consulting members of Categorical Informatics.
