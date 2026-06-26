# Lexeme Typing and Selection Rules

Use this file when word choice depends on upper-ontology fit rather than surface familiarity.

## 1. Upper ontology used for lexical checking

Map content nouns to one or more coarse types:

- `quantity`: number, scale, traffic, demand, volume, coverage extent
- `quality`: robustness, continuity, reliability, safety, adaptability
- `process`: orchestration, planning, deployment, training, evolution, parsing
- `artifact`: application, system, framework, architecture, model, ontology, service chain
- `capability`: generalization, autonomy, coordination, interpretability
- `relation`: dependency, conflict, alignment, coupling
- `task`: mission, workflow, objective, scheduling target
- `constraint`: regulation, rule, budget, resource limit, airspace restriction
- `metric`: latency, accuracy, node expansions, success rate

## 2. Core selection rules

### 2.1 `grow`

`Sel(grow) = {quantity}`

Good:

- traffic grows
- demand grows
- the number of users grows
- constellation scale grows

Bad:

- applications grow
- the framework grows
- the ontology grows

Reason: these nouns denote artifacts or designed systems, not quantity-bearing scales.

### 2.2 `develop`

`Sel(develop) = {artifact, capability, process}`

Good:

- applications develop
- the system develops new coordination behavior
- the field develops rapidly
- the workflow develops from manual to autonomous execution

This is the preferred repair for `growth of applications` when the intended meaning is maturation, diversification, or functional evolution.

### 2.3 `increase`

`Sel(increase) = {quantity, metric}`

Good:

- latency increases
- throughput increases
- the number of tasks increases

### 2.4 `improve`

`Sel(improve) = {quality, capability, metric}`

Good:

- improve robustness
- improve planning latency
- improve generalization

### 2.5 `maintain`

`Sel(maintain) = {quality, metric}`

Good:

- maintain service continuity
- maintain safety margins
- maintain low latency

### 2.6 `enable`

Use `enable(x, y)` when the subject is a method, system, or mechanism and the object is a task, capability, or operational gain.

Good:

- the parser enables logical constraint extraction
- the scheduler enables resilient service chaining
- the ontology enables consistent retrieval

### 2.7 `translate`

Use `translate(x, y)` when the source is an intent, goal, or abstract specification and the target is a representation or executable structure.

Good:

- translate mission goals into logical service chains
- translate regulations into machine-checkable constraints

### 2.8 `decouple`

Use `decouple(x, y)` for relation repair when the method severs an undesirable dependence.

Good:

- decouple logical service continuity from physical resource fluctuations
- decouple planning quality from topology volatility

## 3. Subject-verb-object patterns

Use typed relation triples rather than loose phrasing.

- `method -> improves -> quality`
- `mechanism -> enables -> task`
- `constraint -> limits -> capability`
- `ontology -> organizes -> concept set`
- `planner -> minimizes -> metric`
- `architecture -> maintains -> quality`

Reject triples with type mismatch. Example:

- `growth -> of -> applications` is rejected because `growth` encodes quantity change while `applications` is typed primarily as `artifact`.
- `development -> of -> applications` is accepted because `development` licenses artifact and capability evolution.

## 4. Repair table

| bad form | type error | preferred repair |
| --- | --- | --- |
| growth of applications | quantity applied to artifact | development of applications |
| framework improves tasks | object should be quality or capability | framework improves task success rates |
| ontology grows retrieval | subject and object mismatch | ontology enables structured retrieval |
| challenge is important | summary-only and weak predicate | challenge intensifies due to ... |
| method is useful | summary-only | method reduces ... or enables ... |

## 5. Using the machine-readable lexicon

Load `assets/lexeme_types.json` when a reusable rule or script needs explicit type assignments. The file contains:

- noun-to-type mappings,
- verb selection sets,
- forbidden or suspicious surface patterns,
- suggested repairs for common mismatches.
