# Domain Ontology Bootstrap and Download Workflow

The user requested either bundled ontology content or at least code and technique for downloading and building one. This file defines a lightweight workflow that can be executed manually or with `scripts/ontology_bootstrap.py`.

## 1. Goal

Construct a small domain ontology before drafting the abstract so that terminology, relations, and verb selection are typed instead of guessed.

## 2. Minimum ontology payload

For an abstract-writing task, the local ontology only needs five blocks:

1. `entities`: domain nouns and noun phrases
2. `types`: upper-ontology assignments such as `artifact`, `process`, or `constraint`
3. `relations`: `enables`, `constrains`, `depends_on`, `measured_by`, `implemented_by`
4. `metrics`: evaluation quantities and qualities
5. `aliases`: abbreviations and surface variants

## 3. Bootstrap algorithm

### Step 1. Harvest terms

Extract terms from:

- title
- problem statement
- method name
- environment
- constraints
- metrics
- claimed results

### Step 2. Type each term

Map each term to the upper ontology in `references/lexeme-typing.md`.

Examples:

- `service continuity -> quality`
- `mission semantics -> relation`
- `task-centric orchestration framework -> artifact`
- `resource contention -> constraint`
- `planning latency -> metric`

### Step 3. Add computable relations

Use only relations that can support abstract writing and checking:

- `artifact enables task`
- `constraint limits task`
- `process implements artifact`
- `metric evaluates artifact`
- `relation links artifact and constraint`

### Step 4. Emit a seed ontology

Use the script to emit both JSON and Turtle:

```bash
python scripts/ontology_bootstrap.py \
  --domain "low-altitude autonomous systems" \
  --terms "airspace rule,uav mission,trajectory,legal constraint,information quality" \
  --outdir ./aero_seed
```

This creates:

- `ontology_seed.json`
- `ontology_seed.ttl`

### Step 5. Optional public ontology download

If a public ontology already exists, fetch it and keep it next to the local seed:

```bash
python scripts/ontology_bootstrap.py \
  --download-url "https://example.org/ontology.owl" \
  --outdir ./downloaded_ontology
```

Preferred sources are official project repositories, institutional artifact pages, or the paper's released code/data repository.

## 4. Merge policy

When a downloaded ontology and a local seed disagree:

1. preserve the downloaded class names,
2. keep the local upper-ontology typing as an alignment layer,
3. attach aliases instead of renaming public classes,
4. store abstract-writing relations separately if the public ontology lacks them.

## 5. Abstract-facing use of the ontology

The ontology is not the final product. It is a control layer for better abstracts.

Use it to:

- reject type-mismatched phrasing,
- preserve stable terminology across sentences,
- ensure each proposed artifact is linked to a challenge and an evaluation target,
- support relation choices such as `for`, `to`, `enables`, and `measured_by`.
