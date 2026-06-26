# Domain Adapters

## Table of Contents

1. [Overview](#overview)
2. [Scientific Domains](#scientific-domains)
3. [Business Domains](#business-domains)
4. [Technical Domains](#technical-domains)
5. [Personal Domains](#personal-domains)
6. [Social Domains](#social-domains)
7. [Cross-Domain Translation](#cross-domain-translation)

---

## Overview

Different domains have different epistemic standards, verification methods, and reconstruction challenges. This document provides domain-specific adaptations of the primal-foundation framework.

**Principle**: First principles are universal, but their application is context-dependent. Adapt the framework to domain characteristics while preserving core principles.

---

## Scientific Domains

### Characteristics

- **High epistemic standards**: Empirical evidence, falsifiability, peer review
- **Strong axioms**: Physical laws, mathematical theorems
- **Clear verification**: Experiments, predictions, reproducibility
- **Incremental progress**: Paradigm shifts are rare

### Domain-Specific Axioms

#### Physics
```
A1: Energy, momentum, and charge are conserved in closed systems
A2: No information or matter can exceed the speed of light
A3: Entropy increases in isolated systems (Second Law of Thermodynamics)
A4: Causality is preserved (cause precedes effect)
```

#### Biology
```
B1: Evolution acts on heritable variation
B2: Natural selection favors fitness-enhancing traits
B3: Organisms are complex adaptive systems
B4: Biological systems exhibit emergent properties
```

#### Chemistry
```
C1: Chemical reactions conserve mass and energy
C2: Reaction rates depend on concentration, temperature, and catalysts
C3: Molecular structure determines properties
C4: Chemical bonds have quantifiable energies
```

### Verification Emphasis

**Physics**: Experimental verification, mathematical consistency
**Biology**: Comparative studies, statistical validation, reproducibility
**Chemistry**: Reproducible synthesis, predictive models

### Reconstruction Challenges

- **Physics**: Quantum mechanics (measurement problem, indeterminacy)
- **Biology**: Complexity, emergence, nonlinear dynamics
- **Chemistry**: Scale bridging (quantum to macroscopic)

### Domain Adapter Protocol

```
1. Identify domain axioms (above)
2. Check assumptions against domain axioms
3. Use domain-specific verification methods
4. Incorporate uncertainty quantification (especially in biology)
5. Validate against experimental data
```

### Example: Drug Development

**Problem**: "Will this compound treat the disease?"

**Assumption extraction**:
- Axiological: "Safety and efficacy are the goals"
- Causal: "Compound interacts with target protein"
- Biological: "Target modulation treats disease"

**Verification**:
- Biological: In vitro assays, animal studies
- Statistical: Clinical trials, significance testing
- Reproducibility: Multi-site trials

**Axioms**:
- B1: Evolution (drug resistance may emerge)
- B3: Complex systems (side effects may emerge)
- New: Pharmacodynamics (dose-response relationship)

**Reconstruction**:
- Test mechanism (in vitro)
- Validate in model organisms (in vivo)
- Clinical trials (phase I, II, III)
- Monitor long-term effects (post-market surveillance)

---

## Business Domains

### Characteristics

- **Medium epistemic standards**: Empirical data, market research, A/B tests
- **Weak axioms**: Market dynamics are contingent, not universal
- **Probabilistic verification**: Market experiments, customer feedback
- **Rapid change**: Strategies must adapt quickly

### Domain-Specific Axioms

```
B1: Markets equilibrate supply and demand
B2: Competition erodes profits (commoditization)
B3: Customer value = perceived benefit - perceived cost
B4: Incentives drive behavior
B5: Network effects create winner-take-all dynamics
```

### Verification Emphasis

- **Market experiments**: A/B tests, pilot programs
- **Customer feedback**: Surveys, interviews, behavioral data
- **Financial analysis**: Unit economics, ROI, LTV/CAC
- **Competitive analysis**: Market share, pricing, positioning

### Reconstruction Challenges

- **Uncertainty**: Markets are noisy and unpredictable
- **Time lags**: Effects may take months/years to manifest
- **External shocks**: Economic cycles, regulatory changes, pandemics

### Domain Adapter Protocol

```
1. Use business axioms as foundation
2. Verify with market experiments (not just analysis)
3. Incorporate competitive dynamics
4. Model time lags and feedback loops
5. Prepare for contingency scenarios
```

### Example: Market Entry Strategy

**Problem**: "Should we enter this market?"

**Assumption extraction**:
- Causal: "Our product will outperform competitors"
- Temporal: "Market will continue growing"
- Systemic: "Network effects will not lock us out"

**Verification**:
- Market research: Customer interviews, competitor analysis
- Financial modeling: TAM, SAM, SOM, unit economics
- A/B testing: Landing page, pilot product

**Axioms**:
- B1: Supply-demand equilibrium (market saturation risk)
- B2: Competition (price pressure, commoditization)
- B4: Incentives (customer switching costs)
- B5: Network effects (winner-take-all risk)

**Reconstruction**:
- Calculate TAM/SAM/SOM
- Model unit economics (CAC, LTV, payback period)
- Assess competitive landscape
- Plan entry strategy (direct, partnership, acquisition)

---

## Technical Domains

### Characteristics

- **High epistemic standards**: Code correctness, performance, reliability
- **Strong axioms**: Physical constraints, algorithmic complexity
- **Clear verification**: Testing, profiling, code review
- **Rapid iteration**: Continuous deployment, feedback loops

### Domain-Specific Axioms

```
T1: Performance is constrained by physical limits (CPU, memory, I/O)
T2: Complexity grows with coupling and interface surface area
T3: Distributed systems have inherent failures (network partitions, latency)
T4: Security is a trade-off with usability and performance
T5: Maintenance cost scales with code size and complexity
```

### Verification Emphasis

- **Code correctness**: Unit tests, integration tests, property-based testing
- **Performance profiling**: Benchmarking, load testing
- **Reliability**: Chaos engineering, fault injection
- **Security**: Penetration testing, code review

### Reconstruction Challenges

- **Scalability**: Systems that work at scale differ from small systems
- **Complexity**: Distributed systems have emergent failures
- **Legacy constraints**: Existing systems constrain design space

### Domain Adapter Protocol

```
1. Use technical axioms as foundation
2. Verify with automated testing and profiling
3. Model distributed system properties (CAP theorem, eventual consistency)
4. Design for failure (fault tolerance, graceful degradation)
5. Plan for evolution (modularity, extensibility)
```

### Example: System Architecture

**Problem**: "How should we scale our application?"

**Assumption extraction**:
- Systemic: "Adding servers will linearly increase capacity"
- Causal: "Microservices improve scalability"
- Temporal: "Growth rate will continue"

**Verification**:
- Load testing: Stress test current architecture
- Profiling: Identify bottlenecks (CPU, memory, I/O, database)
- A/B testing: Compare monolith vs. microservices

**Axioms**:
- T1: Physical limits (CPU, memory, I/O)
- T2: Complexity (communication overhead, coordination cost)
- T3: Distributed failures (latency, partitions, partial failure)

**Reconstruction**:
- Profile current system (identify bottlenecks)
- Model scaling laws (linear vs. nonlinear)
- Choose architecture: monolith (simpler) vs. microservices (more scalable but more complex)
- Implement fault tolerance (circuit breakers, retries, timeouts)
- Plan for evolution (modular boundaries, API design)

---

## Personal Domains

### Characteristics

- **Low epistemic standards**: Intuition, experience, self-knowledge
- **Weak axioms**: Psychology is contingent, not universal
- **Self-verification**: Reflection, experimentation, feedback
- **Unique context**: Individual values, constraints, circumstances

### Domain-Specific Axioms

```
P1: Satisfaction = autonomy × competence × relatedness (Self-Determination Theory)
P2: Career value = skill scarcity × leverage
P3: Habits form through cue-routine-reward loops
P4: Decision quality improves with diversity of perspectives
P5: Resources are finite (time, energy, money, attention)
```

### Verification Emphasis

- **Self-reflection**: Journaling, meditation, therapy
- **Experiments**: Try new approaches, observe outcomes
- **Feedback**: Ask others, coach, mentor
- **Quantification**: Track metrics (time, habits, outcomes)

### Reconstruction Challenges

- **Cognitive biases**: Confirmation bias, sunk cost, overconfidence
- **Emotional factors**: Fear, desire, identity
- **Uncertainty**: Future is unpredictable, values change over time

### Domain Adapter Protocol

```
1. Use psychological axioms as foundation
2. Verify with self-experimentation and reflection
3. Account for cognitive biases
4. Incorporate emotional and identity factors
5. Plan for iteration (values change, circumstances change)
```

### Example: Career Decision

**Problem**: "Should I switch careers?"

**Assumption extraction**:
- Axiological: "New career will be more fulfilling"
- Causal: "Skills will transfer"
- Temporal: "Market demand will persist"

**Verification**:
- Self-assessment: Values, skills, interests
- Market research: Job postings, salary, growth
- Experiments: Internship, side project, informational interview

**Axioms**:
- P1: Autonomy, competence, relatedness
- P2: Skill scarcity × leverage
- P5: Resource constraints (time for learning, financial cushion)

**Reconstruction**:
- Assess current satisfaction (autonomy, competence, relatedness)
- Evaluate new career (skill scarcity, leverage)
- Calculate transition cost (time, money, risk)
- Plan transition path (part-time, education, networking)

---

## Social Domains

### Characteristics

- **Low epistemic standards**: Social phenomena are noisy, context-dependent
- **Contingent axioms**: Social norms, institutions are constructions, not laws
- **Empirical verification**: Sociology, anthropology, history
- **Complex emergence**: Social systems have emergent, unpredictable behaviors

### Domain-Specific Axioms

```
S1: Institutions are social constructs (can be changed)
S2: Social norms emerge from interaction, not design
S3: Power dynamics influence outcomes
S4: Information flows shape social behavior
S5: Social systems exhibit path dependence
```

### Verification Emphasis

- **Empirical research**: Surveys, ethnography, case studies
- **Historical analysis**: Precedents, patterns, cycles
- **Comparative analysis**: Cross-cultural, cross-temporal
- **Field experiments**: Policy pilots, social experiments

### Reconstruction Challenges

- **Complexity**: Social systems have many interacting factors
- **Path dependence**: History constrains possibilities
- **Power dynamics**: Interests influence what is possible

### Domain Adapter Protocol

```
1. Use social axioms as foundation
2. Verify with empirical and historical research
3. Account for power dynamics and interests
4. Consider path dependence and constraints
5. Plan for incremental change (radical change is rare)
```

### Example: Organizational Culture Change

**Problem**: "How should we improve our culture?"

**Assumption extraction**:
- Causal: "Changing values will change behavior"
- Systemic: "Leadership dictates culture"
- Temporal: "Culture change will be quick"

**Verification**:
- Employee surveys (current state, desired state)
- Behavioral data (turnover, engagement, collaboration)
- Historical analysis (past culture change efforts)

**Axioms**:
- S1: Institutions are constructs (culture can be changed)
- S2: Norms emerge from interaction (need to change practices, not just values)
- S4: Information flows (communication patterns matter)
- S5: Path dependence (existing culture resists change)

**Reconstruction**:
- Diagnose current culture (values, norms, behaviors)
- Identify leverage points (leadership, rituals, communication)
- Design interventions (change practices, reinforce with values)
- Monitor and iterate (culture change is slow)

---

## Cross-Domain Translation

### Analogy Mapping

Translate insights from one domain to another:

```
Physics → Business:
Conservation of energy → Conservation of resources (can't create from nothing)
Entropy → Organizational entropy (disorder increases without intervention)

Biology → Technical:
Evolution → Software evolution (survival of the fittest code)
Adaptation → System adaptation (load balancing, scaling)

Economics → Personal:
Supply-demand → Skill market (scarcity × leverage)
Marginal utility → Diminishing returns on effort
```

### Domain Bridging

Identify axioms that span domains:

```
Universal axioms:
- Scarcity (resources are finite)
- Incentives (agents respond to incentives)
- Complexity (complex systems have emergent properties)
- Time (effects have time lags, path dependence)
- Uncertainty (future is probabilistic, not deterministic)
```

### Anti-Pattern: False Analogy

Avoid inappropriate cross-domain analogies:

```
❌ Business → Physics:
"Companies should obey the second law of thermodynamics"
(Not applicable; organizations are not thermodynamic systems)

❌ Personal → Engineering:
"Optimize life like code"
(Not applicable; humans are not machines)

✅ Instead: Use domain-appropriate axioms
```

### Translation Framework

```
1. Identify source domain axiom
2. Test applicability to target domain
3. Map variables appropriately
4. Verify with target domain evidence
5. Refine or reject analogy
```

---

## When to Use This Reference

**Use during Phase 0 (Foundation) to select domain adapter.**

**Apply to**:
- Adapting the framework to specific domains
- Understanding domain-specific challenges
- Translating insights across domains
- Avoiding false analogies

**Domain Adapter Checklist**:
- [ ] Domain characteristics identified
- [ ] Domain-specific axioms selected
- [ ] Verification methods adapted to domain
- [ ] Reconstruction challenges anticipated
- [ ] Domain adapter protocol applied
- [ ] Cross-domain analogies validated
- [ ] False analogies avoided
