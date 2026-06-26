# Unified Representation and Transformation of Multi-Model Data

## Abstract

Ctx: Unified category-theoretic representation for multi-model data with high-level transformation algorithms.
Src: `sources/cat/A unified representation and transform.md`

Multi-model data = combination of relational, document, graph, wide-column, key/value models. Proposes category-theory-based unifying model for representing and transforming multi-model schemas and instances. Enables querying, evolution, and migration across models via common categorical intermediary.

Example query (Ex 1.1): "For each customer in Prague, find a friend who ordered the most expensive product among all that customer's friends." — combines relational customer data, graph friendships, document orders, wide-column references, key/value shopping carts.

## Category Theory Prerequisites

**Category** (C = (O, M, ∘)): objects O = Obj(C); morphisms M = Hom(C); f: A → B with domain A and codomain B; associative composition (h ∘ g) ∘ f = h ∘ (g ∘ f); identity 1_A for each A.

**Functor** F: C1 → C2: maps objects and morphisms preserving identities and composition.

Example: **Set** = category (objects = sets, morphisms = functions); **Rel** = category (objects = sets, morphisms = binary relations).

## Schema Category

**S = (O_S, M_S, ∘_S)** — models structure of data (analogous to conceptual schema).

**Objects**: each o ∈ O_S = tuple (key, label, superid, ids). superid = set of attributes for o; ids = collection of identifiers (subsets of superid).

**Morphisms**: each m ∈ M_S = (signature, dom, cod, min, max). signature ∈ M* for composing base morphisms; dom and cod = domain and codomain objects; min, max ∈ {0, 1, *} = cardinalities.

**Composition**: m₂ ∘_S m₁ = (signature₂ · signature₁, dom₁, cod₂, min, max) with cardinality rules applied to min and max.

**Dual morphisms**: for each m: X → Y, dual m⁻¹: Y → X required — bidirectional relationship capture.

Example (Ex 2.4): ER schema → schema category with objects {Customer, Order, Address, Product, ...}; superid and ids per object from ER identifiers.

## Instance Category

**I = (O_I, M_I, ∘_I)** — models actual data.

**Objects**: O_I corresponds to O_S. Each o_I = set of tuples (active domain) conforming to attributes in superid.

**Morphisms**: M_I = relations between tuples, reflecting cardinalities (min, max). Identities = reflexive relations on object sets. Composition ∘_I = standard relational composition.

Example (Ex 2.5): Customer in O_S with attributes {id, name, surname} → Customer in O_I = {(id,1),(name,Mary),(surname,Smith)}, {(id,2),(name,Anne),(surname,Maxwell)}, ...

Example (Ex 2.6): Morphism Customer → Surname = subset of Customer × Surname matching each tuple to its surname.

## Categorical Representation of Multi-Model Data

The schema category S and the instance category I together form the categorical intermediary that makes cross-model transformation possible. This representation is the canonical bridge between concrete DBMS kinds and high-level transformation algorithms.

### Categorical_Representation_of_Multi_Model_Data

Alias fragment preserved for legacy XRef compatibility.

## Category-to-Data Mapping (Kinds)

**Kind κ** = (D, name_κ, root_κ, morph_κ, pkey_κ, ref_κ, P_κ):
- D = DBMS
- root_κ ∈ O_S or M_S = main object/morphism
- pkey_κ = collection of signatures forming identifier
- ref_κ = set of references to other kinds
- P_κ = access path (tree/JSON-like structure describing nested properties)

Access paths describe nesting, arrays, maps. JSON-like grammar accommodates document and column models, dynamic property names.

## Transformation Algorithms

**Algorithm 1 (Model to Category — M2C)**:
1. Extract records from DBMS kind κ.
2. Represent as forests of records (trees).
3. Traverse forest; fill instance category I with objects and morphisms respecting cardinalities and compositions.
- Properties/arrays → objects or morphisms based on access path.
- Missing values → empty sets of superidentifiers.

**Algorithm 2 (DDL — Category to Model schema)**: creates or alters target DBMS schema based on category structure via wrapper for each system.

**Algorithm 3 (DML — Category to Model data)**: inserts data from instance category into new schema.

**Algorithm 4 (IC — integrity constraints)**: finalizes references and constraints (primary keys, foreign keys).

**Multi-model to multi-model migration** — categorical representation as intermediary avoids O(n²) pairwise mappings:
1. Transform source model(s) → instance category.
2. Transform instance category → target model(s).
Inter-model references and schema strategies captured in category.

## MM-cat Framework

MM-cat = tool implementing schema/instance categories and unified transformations.

Architecture:
- Schema category + instance category as core data structures.
- Wrappers per DBMS implementing interface for schema creation, references, data push/pull.
- Transformation modules: model-to-category and category-to-model.

Wrapper types: AbstractPathWrapper (object/morphism → DBMS property mapping); AbstractDDLWrapper (schema creation/alteration); AbstractPushWrapper, AbstractPullWrapper, AbstractICWrapper (insertion, retrieval, integrity constraints).

Performance: transformation algorithms linear in record count; logarithmic overhead if indexing required; parallelizable by data splitting or distributed composition tasks.

## Benefits and Future Work

Benefits of categorical approach:
- Cross-model representation without forcing constructs across models.
- Proper handling of relationships (composite morphisms) for joins and transformations.
- Generic expansions to conceptual querying, evolution management, partial schema usage in schema-less contexts.

Application: conceptual query language derivable; cross-model joins and navigations use morphism compositions; partial results combined via pullbacks in category.

Future work: comprehensive query language; advanced evolution management based on categorical foundations.
