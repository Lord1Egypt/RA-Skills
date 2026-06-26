# Category-Theoretic Database Approaches

## Functorial Data Model (FDM)

Ctx: Analysis (Walter) on FDM and DIK hierarchy applied to databases and migrations.
Src: `sources/cat/Exploring Category-Theoretic Approaches to Databases.md`
XRef: `urn:fxsl:kb:seven-sketches`

Database = functor I: S → **Set**, where S = schema category (finitely presented). Allows migration and schema integration as functorial operations (pullbacks, pushforwards), guaranteeing mathematical integrity.

## Core Definitions

**FDM** — data as functor from schema category to Set.

**Schema category S** — finitely presented category: objects = tables/entities; morphisms = columns/relations/foreign keys; equations = path integrity constraints.

**Instance** — functor I: S → **Set**. For each object A in S, I(A) = set of records. For each morphism f: A → B, I(f) = function between sets.

**Schema translation** — functor F: S → T inducing migration operations.

## Migration Operators

**Δ_F (Pullback)** — brings data from T to S; simple reindexation. No information loss.

**Σ_F (Left Pushforward)** — migrates data from S to T using colimits (unions/sums). May lose information via co-identifications.

**Π_F (Right Pushforward)** — migrates data from S to T using limits (products/joins). May discard records not satisfying conditions.

**Adjunction chain**: Σ_F ⊣ Δ_F ⊣ Π_F.

**Grothendieck construction** — tool for integrating heterogeneous data; basis for integrating multiple databases via colimits in Cat.

## DIK Layer Mapping

| Layer | Categorical Object | Formal Def |
|---|---|---|
| Data | Functor I: S → **Set** | I(A) = records; I(f) = FK function |
| Information | Schema category S | Objects, morphisms, equations |
| Knowledge | Migration functors Δ_F, Σ_F, Π_F | F: S → T induces operations |
| Modeling | Design of schema categories + natural transformations | Colimits in Cat for multi-DB integration |

XRef (Modeling): `urn:fxsl:kb:formal-framework-data-lakes-ct`, `urn:fxsl:kb:unified-multimodel`

## Conclusion Summary

- Data: Functor I: S → **Set**
- Information: Schema category S
- Knowledge: Migration functors (Δ_F, Σ_F, Π_F)
- Modeling: Design of categories and natural transformations
