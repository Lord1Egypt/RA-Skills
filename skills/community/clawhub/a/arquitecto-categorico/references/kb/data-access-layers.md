# Data Access Layers via Category Theory

Categorical patterns for DAL: storage, APIs, repositories, ORMs, data lakes.

## Storage and API

Storage: SQL-heavy designs often exploit limit-like constructions (product, pullback, equalizer) for integrity, joins, and normalized structure. NoSQL/document-oriented designs often exhibit colimit-like assembly patterns (coproduct, pushout, schema accretion) for flexible schema and polyglot aggregation. Mixed read/write architectures can be modeled with asymmetric lenses or schema mappings.

APIs as functors — Domain→ResourceCat (REST), Domain→TypeCat (GraphQL, dynamic pullback), Domain→ProtoCat (gRPC, streaming). Streams: coalgebra, action = primary key. Functor check: F(id)=id; F(g∘f)=F(g)∘F(f).

## Repository, ORM, Data Lake

**Repository** = coalgebraic interface model c: X → F(X) when the repository is treated observationally through operations and responses. Bisimulation then expresses observational equivalence between repository implementations under the shared interface.

**ORM** = adjunction-shaped discipline, not automatically a literal theorem. A good ORM aspires to approximate a pair of translations between DomainCat and SchemaCat with controlled unit/counit drift. ORM drift = semantic mismatch introduced by the round-trip.

**Data Lake** = indexed family of schemas/data products organized by zones or tenants, often integrated through Grothendieck construction ∫F and, when a synthesis artifact is needed, suitable colimits of local diagrams. Audit: declared pipelines/mappings should compose coherently and preserve stated invariants.

## Synthesis

2-categorical model: objects = DAL components, 1-morphisms = transformations, 2-morphisms = migrations.

Audit dimensions: STORAGE-MODEL-ALIGN (chosen storage patterns fit the intended categorical structure), API-FUNCTOR-PRESERVE (functoriality where explicitly claimed), REPO-BISIM (observational equivalence under shared interface), ORM-ROUNDTRIP-DRIFT (semantic loss across domain/schema translations), PIPELINE-COMMUTE (declared pipeline diagram commutes).
