# MultiCategory: Multi-Model Query Processing

## Abstract

Ctx: Multi-model query processing based on category theory and functional programming (Haskell).
Src: `sources/cat/MultiCategory Multi-model Query Proce.md`

MultiCategory processes multi-model queries based on category theory and functional programming. Four main scenarios: building schema and instance categories from various data models; query processing using Haskell; flexible output models; visualizing queries as graphs in relation to the schema category.

## Category Definition

**Def 2.1 (Category)** — C: collection of objects Obj(C), collection of morphisms Hom(C). For each f ∈ Hom(C): ∃ A,B ∈ Obj(C) with f: A → B. Axioms: composition g ∘ f: A → C for f: A → B, g: B → C; associativity; identity id_A: A → A with f ∘ id_A = f and id_A ∘ f = f whenever defined. Informally: category = graph with composition rule.

## Schema and Instance Categories

**Schema Category** — Represents schema information of a multi-model environment.
- Objects: predefined data types (string, integer) and entities (customers, products).
- Morphisms: typed functions between data types (e.g., customer located in location).
- Provides unified view for different data models, enabling seamless multi-model query processing.

**Instance Category** — Models how concrete data instances are stored. Each object in schema category mapped to typed Haskell data structure; morphisms mapped to concrete Haskell functions.

**Instance Functor** — Mapping from schema to instance categories via collection constructor functors: Instance_Functor: Schema_Category → Instance_Category.

Example schema objects: {Location, Order, Customer, Product}. Morphisms: orderedBy: Order → Customer; contains: Order → Product; located: Customer → Location.

## Multi-Model Query Language

Queries use QUERY/FROM/TO keywords with Haskell functions and expressions.

**Example 3.1** — Select customers with credit limit > 3000:

```haskell
QUERY (\x -> if creditLimit x > 3000
             then cons x else nil)
FROM customers
TO graph/xml/relational
```

**Example 3.2** — Nested query: find customers who ordered books, return name and country:

```haskell
LET t BE
QUERY (\x xs -> if elem "Book" (map productName (orderProducts x))
               then cons x xs else xs)
FROM orders TO relational IN
QUERY (\x -> if any (\y -> orderedBy y customers == x)
             then cons (customerName x, countryName (located x locations)) else nil)
FROM customers TO algebraic graph/relational/xml
```

t = orders containing a Book; outer query = names and locations of customers who placed such orders. Results available in algebraic graph, relational, or XML models.

## Query Processing Mechanism

1. Parsing: user queries parsed into sequence of fold-functions based on schema information.
2. Execution: Haskell backend executes fold-functions against instance category.
3. Visualization: results returned to frontend, visualized per specified data model.

**Catamorphism** — Generalization of fold functions used to process data structures.

**Foldable data structures** — Data structures foldable to summary values; essential for query processing.

**Haskell properties** — Pure Haskell: referential transparency, lazy evaluation.

## Conclusion and Future Work

MultiCategory applies category theory to model and query multi-model data via functional programming.

Future work:
- Automating generation of schema and instance categories from input datasets
- Expanding theoretical framework to support multi-model joins and data transformations
