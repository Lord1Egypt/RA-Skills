# Phase 3: Emit Repository YAML

Use this target only when explicitly requested. Shared field semantics also govern OKF output.

One `semantic_catalog` per bundle contains name, purpose, evidence boundary, required context, and
entry points mapping triggers to ontology entities and source operations.

An optional shared-dimension `semantic_ontology` defines conformed dimensions reused across facts.
Every dimension declares `kind`, business key, source operations, attributes, and evidence.
Snowflake dimensions also declare their parent. Degenerate dimensions remain keys on a fact rather
than separate objects.

One model ontology per business process or billing mode defines facts with grain, source operations,
time, dimensions, degenerate keys, measures, additivity, units/basis, selection rules, and evidence.
Values typed into commands or read from responses stay in the contract layer; semantic YAML links to
that contract instead of copying enums or command examples.

Allowed dimension kinds are `conformed_dimension` for cross-fact reuse and `snowflake_dimension` for
a normalized child. Use `degenerate` only as a fact annotation. Keep confirmed names stable and all
references resolvable.
