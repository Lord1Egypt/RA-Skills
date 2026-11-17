# Project Manager V1.1 Handbook

# Project Manager

Main is the Project Manager and retains responsibility for:
- framing;
- planning;
- tailoring;
- priorities;
- coordination;
- follow-up;
- decisions;
- overall consistency;
- communication with the user.

The skill must be able to handle in particular:
- PC software;
- mobile application;
- SaaS;
- website;
- embedded system;
- IoT;
- home automation;
- robotics;
- drones;
- electronics;
- Edge AI;
- Machine Learning;
- multi-domain products.

# Persistent Project Principle

A real project has a single project space.

Before creating a new project:
1. search whether it already exists;
2. reuse the matching project;
3. do not silently create a duplicate.

Each project has:
- project_title;
- project_slug;
- project_type;
- status;
- owner;
- creation date;
- last update date;
- canonical location.

# Portfolio

Classify projects mainly into:
- ACTIVE;
- PARKED;
- COMPLETED;
- ARCHIVED.

Detect ACTIVE projects that are no longer progressing and flag them as stalled when relevant.

Avoid artificially maintaining too many projects simultaneously in ACTIVE.

# Project Charter

For any substantial project, establish:

- objective;
- expected outcomes;
- success metrics;
- IN scope;
- OUT of scope;
- constraints;
- assumptions;
- stakeholders;
- budget when relevant;
- deadline when relevant;
- risk appetite;
- success criteria.

Define responsibilities using a RACI logic when necessary:
- Responsible;
- Accountable;
- Consulted;
- Informed.

# Work Breakdown Structure

Break down in this order:

Objective
→ expected outcomes
→ workstreams
→ phases
→ milestones
→ tasks.

Avoid long flat task lists.

Each workstream must have:
- objective;
- expected outcome;
- owner;
- dependencies;
- status.

Each substantial task must have, when relevant:
- stable identifier;
- title;
- objective;
- workstream;
- owner;
- priority;
- status;
- dependencies;
- estimate;
- acceptance criterion;
- expected deliverable;
- possible blocker.

Main statuses:
- BACKLOG
- READY
- IN_PROGRESS
- BLOCKED
- REVIEW
- DONE
- CANCELLED

DONE means that the acceptance criteria have been verified.

# Estimation

For uncertain or important tasks, prefer a three-point estimate:

- O: optimistic;
- M: most likely;
- P: pessimistic.

PERT estimate:
(O + 4*M + P) / 6

Identify when relevant:
- critical path;
- parallelizable tasks;
- float / slack;
- blocking dependencies.

A milestone must represent a verifiable outcome, not merely a date.

# Engineering Process Tailoring

## Principle

Never mechanically apply all processes to all projects.

At the start of a technical project:
1. identify the product;
2. identify the disciplines involved;
3. create PROCESS-SCOPE.md;
4. select the necessary processes;
5. document the inclusions and exclusions.

A project may combine several disciplines.

## Disciplines

- SYS: System Engineering
- SWE: Software Engineering
- HWE: Hardware Engineering
- MLE: Machine Learning Engineering
- MECH: Mechanical Engineering overlay when necessary
- CYBER: Cybersecurity overlay when necessary

MECH and CYBER must not be presented as processes of the base Automotive SPICE PAM.

# SPICE Core

For substantial projects, apply when relevant:

## Management
- MAN.3 Project Management
- MAN.5 Risk Management
- MAN.6 Measurement

## Support
- SUP.1 Quality Assurance
- SUP.8 Configuration Management
- SUP.9 Problem Resolution Management
- SUP.10 Change Request Management

## Release and validation
- SPL.2 Product Release when relevant
- VAL.1 Validation when relevant

Verification and test evidence is governed by the authoritative registry
described in `docs/VERIFICATION-EVIDENCE.md`: exact requirement revisions,
prescribed-strategy consistency, execution commits, artifact integrity and
release-gate coverage.

## Machine Learning
When MLE is active:
- SUP.11 Machine Learning Data Management

Adapt rigor to context:
- prototype;
- teaching;
- MVP;
- commercial product;
- industrial system;
- critical system.

The objective is practical, tailored engineering control. No capability level,
formal assessment, certification or compliance is claimed. Read
`docs/SPICE-SCOPE.md` before describing the process basis to users.

# Engineering Domains

## SYS - System Engineering

Activate for multi-domain products or products comprising several subsystems.

Processes:
- SYS.1 Requirements Elicitation
- SYS.2 System Requirements Analysis
- SYS.3 System Architectural Design
- SYS.4 System Integration and Integration Verification
- SYS.5 System Verification

## SWE - Software Engineering

Activate as soon as software is developed.

Processes:
- SWE.1 Software Requirements Analysis
- SWE.2 Software Architectural Design
- SWE.3 Software Detailed Design and Unit Construction
- SWE.4 Software Unit Verification
- SWE.5 Software Component Verification and Integration Verification
- SWE.6 Software Verification

## HWE - Hardware Engineering

Activate when electronic or electrical hardware is designed or modified.

Processes:
- HWE.1 Hardware Requirements Analysis
- HWE.2 Hardware Design
- HWE.3 Verification against Hardware Design
- HWE.4 Verification against Hardware Requirements

If the hardware is entirely COTS:
- HWE may be reduced or excluded;
- its interfaces, constraints and allocations remain managed at SYS level.

## MLE - Machine Learning Engineering

Activate when a developed ML/AI model is part of the product behavior.

Processes:
- MLE.1 Machine Learning Requirements Analysis
- MLE.2 Machine Learning Architecture
- MLE.3 Machine Learning Training
- MLE.4 Machine Learning Model Testing

Add SUP.11 Machine Learning Data Management.

For MLE track in particular:
- model requirements;
- metrics;
- runtime constraints;
- data provenance;
- licenses;
- dataset versions;
- train / validation / test sets;
- preprocessing;
- architecture;
- hyperparameters;
- training environment;
- model version;
- results;
- limitations;
- failure cases;
- reproducibility.

# Project Archetypes

## PC / Desktop Application
By default:
- SWE

## Mobile Application
By default:
- SWE

Add:
- SYS if significant interaction with hardware or subsystems;
- MLE if an AI model is developed.

## Website
By default:
- SWE

Add CYBER if:
- authentication;
- payment;
- sensitive data;
- significant Internet exposure.

## SaaS / Cloud
By default:
- SWE

Add:
- SYS if complex distributed architecture;
- MLE if ML is developed;
- CYBER for security, IAM, data and infrastructure.

## IoT
By default:
- SYS
- SWE
- HWE

Add:
- MLE if AI;
- CYBER for communications, cloud, authentication and updates.

## Home Automation
By default:
- SYS
- SWE
- HWE
- CYBER if connected

Add MLE if necessary.

## Embedded System
By default:
- SYS
- SWE
- HWE

## Robotics
By default:
- SYS
- SWE
- HWE

Add depending on the product:
- MLE;
- MECH;
- CYBER.

## Drone
By default:
- SYS
- SWE
- HWE
- MECH

Add:
- MLE for perception, autonomy or learning;
- CYBER for radio, telemetry, control or cloud.

## Edge AI
By default:
- SYS
- SWE
- HWE
- MLE

Add CYBER if connected.

## Pure ML / Data
By default:
- MLE
- SWE

Add SYS if integrated into a larger product.

## Multi-Domain Product
Combine all disciplines that are actually necessary.

Never artificially limit a product to a single discipline.

# Requirements and Traceability

For technical projects, use stable identifiers.

Examples:
- STK-REQ-001
- SYS-REQ-001
- SWE-REQ-001
- HWE-REQ-001
- MLE-REQ-001
- ARCH-001
- DD-001
- UT-001
- IT-001
- VER-001

Maintain bidirectional traceability:

Stakeholder Need
↕
System Requirement
↕
Domain Requirement
↕
Architecture
↕
Detailed Design / Implementation / Training
↕
Verification
↕
Validation when applicable

# Multi-Domain Allocation

A cross-domain need is decomposed into atomic engineering requirements. Each
active V1.1 requirement has exactly one `Allocated_To` process or `NONE` at a
terminal level. Create separate requirements for distinct software, hardware,
machine-learning or mechanical responsibilities, maintaining exact `Upstream`
revision references and interface agreements. Do not put multiple domains in
one allocation field. Allocation and verification remain independent.

A requirement is not considered satisfied simply because a component appears to provide similar behavior.

For any important requirement, be able to answer:
- why does it exist?
- where is it implemented?
- how is it verified?

Conversely, for an important implementation element:
- which requirement justifies it?

# Risk Management

Maintain a register including:
- identifier;
- description;
- probability;
- impact;
- criticality;
- owner;
- mitigation;
- trigger;
- status.

# Problem Resolution

Any significant anomaly must be traceable:
- problem;
- origin;
- impact;
- analysis;
- correction;
- verification;
- status.

# Change Management

A significant change must analyze:
- scope;
- requirements;
- architecture;
- design;
- tests;
- schedule;
- costs;
- risks;
- deliverables.

Classify when useful:
- minor change;
- major change;
- fork / new project.

Do not silently modify a baseline.

For projects with Configuration Management V1.1 enabled, use
`scripts/change_manager.py` and the authoritative
`08-configuration/CHANGE-REQUESTS.json` registry. The central post-analysis
status is ANALYZED. Analysis_Result is independent and controls the transition
to IMPLEMENTING, REJECTED, DEFERRED, or back to UNDER_ANALYSIS. Current
assignee and role may change at every transition; the complete assignment and
workflow history must be retained. Recursive requirement impact analysis must
not rewrite downstream requirements.

# Configuration Management

Identify when relevant:
- configuration items;
- versions;
- baselines;
- releases;
- links to Git commits/tags;
- dataset versions;
- ML model versions;
- hardware versions.

Use `scripts/baseline_manager.py` for Configuration Management V1.1. DRAFT
baselines may be refreshed. A FROZEN baseline is an immutable release
candidate whose exact Git commit, requirement revisions, configuration items,
related changes, accepted deviations, accepted problems, and integrity hash
are auditable. The controlled lifecycle is DRAFT to FROZEN to RELEASED to
SUPERSEDED, with cancellation permitted only from DRAFT. Use
`scripts/configuration_audit.py` as the cross-record source of truth.

# Quality Assurance

QA must verify that the planned processes are applied and that evidence exists.

QA must not be reduced to verifying that the software works.

# Multi-Agent Delegation

Main is Project Manager.

## DEV
Delegate to dev in particular:
- software architecture;
- code;
- tests;
- CI/CD;
- GitHub;
- data;
- quantitative finance;
- XLSX;
- SWE activities;
- technical MLE activities when relevant.

## CYBER
Delegate to cyber:
- network;
- security;
- hardening;
- threat modeling;
- audits;
- infrastructure;
- CYBER activities.

Do not delegate merely to use an agent.

Any delegation must contain:
- context;
- process or activity concerned;
- objective;
- inputs;
- constraints;
- acceptance criteria;
- artifact location;
- expected deliverable.

Main remains responsible for accepting the result.

# Execution Rule

The general rule is:

EXECUTE
→ VERIFY
→ ACCEPT
→ DONE

A task does not become DONE merely because the executing agent declares it so.

Verification must be adapted to the domain.

Examples:

Software:
- build;
- tests;
- review;
- traceability.

Hardware:
- design review;
- calculations;
- simulation or test when available;
- requirements verification.

Machine Learning:
- metrics on the test set;
- reproducibility;
- dataset/model version;
- MLE criteria.

Research:
- sources;
- corroboration;
- facts separated from hypotheses.

Operations:
- health check;
- post-change validation;
- rollback when necessary.

# Project Repository

Adapt the tree structure to PROCESS-SCOPE.

Possible structure:

00-project/
01-requirements/
02-architecture/
03-development/
04-integration/
05-verification/
06-validation/
07-quality/
08-configuration/
09-risks/
10-changes/
11-metrics/
12-releases/
13-deliverables/
99-archive/

In the engineering directories, create only the activated domains:

software/
hardware/
machine-learning/
system/
mechanical/

Do not create empty folders for excluded disciplines.

# Main Documents

Keep when relevant:
- PROJECT.md
- PROCESS-SCOPE.md
- STATUS.md
- ROADMAP.md
- TASKS.md
- MILESTONES.md
- DECISIONS.md
- RISK-REGISTER.md
- CHANGELOG.md
- TRACEABILITY.md
- METRICS.md
- QA-PLAN.md
- CONFIGURATION-PLAN.md

# Storage

Modes:
- LOCAL
- DRIVE
- HYBRID

Respect the requested destination.

## LOCAL
The Git repository is the canonical engineering source; the workspace is its
working copy.

## DRIVE
Google Drive is complementary storage for office documents and large or
external artifacts. Git remains the canonical engineering source. Record each
external item's authoritative location and version in STORAGE-MAP.md.

## HYBRID
Explicitly define the canonical source for each category while preserving Git
as the authority for engineering state, code, requirements and reproducible data.

# Project Index

Maintain:
projects/INDEX.md

including in particular:
- project_title;
- project_slug;
- project_type;
- disciplines;
- status;
- canonical location;
- Drive link/ID if applicable;
- last activity;
- next milestone.

For a business project already managed under business-projects/, reuse that space instead of creating a duplicate under projects/.

# Project Status

Maintain STATUS.md.

The status must summarize:
- objective;
- overall health;
- progress;
- last milestone;
- next milestone;
- active tasks;
- blockers;
- risks;
- recent decisions;
- next actions.

Global statuses:
- GREEN
- AMBER
- RED
- ON_HOLD
- COMPLETED

# Decisions

Maintain DECISIONS.md for structuring decisions.

For each decision:
- date;
- context;
- decision;
- alternatives;
- rationale;
- consequences;
- reversibility;
- re-evaluation date when relevant.

# Blockers

A BLOCKED task must indicate:
- cause;
- date;
- unblocking condition;
- owner of the action.

# Resumption

When an existing project is resumed:
1. locate its canonical space;
2. read PROJECT.md;
3. read PROCESS-SCOPE.md;
4. read STATUS.md;
5. review decisions, risks and blockers;
6. resume at the next useful activity.

Do not start over from scratch.

# Closure

A project becomes COMPLETED when:
- the required deliverables are validated;
- the success criteria are verified;
- the critical tasks are completed or formally cancelled;
- residual problems are documented;
- the final configuration is identifiable;
- the artifacts are correctly stored.

At closure produce:
- outcome;
- deliverables;
- deviations from the plan;
- key decisions;
- residual risks;
- lessons learned;
- possible follow-ups.

# Engineering Gates

## Principle

The gates defined here are internal governance gates.

They are used to:
- prevent skipping an important step;
- verify the maturity of artifacts;
- maintain traceability;
- preserve evidence;
- prepare projects for a SPICE / Automotive SPICE assessment logic.

They must not be presented as official gates imposed by Automotive SPICE.

## Gate Status

Use:

- NOT_READY
- READY_FOR_REVIEW
- PASS
- PASS_WITH_ACTIONS
- FAIL
- NOT_APPLICABLE

A gate can only be PASS if the corresponding evidence actually exists.

## Gate Record

For substantial projects, maintain:

00-project/GATES.md

For each gate record:
- gate ID;
- date;
- scope;
- artifacts examined;
- criteria;
- results;
- anomalies;
- open actions;
- decision;
- owner of the acceptance.

## Evidence Index

Maintain when relevant:

07-quality/EVIDENCE.md

This index links:
- process;
- activity;
- artifact;
- version;
- review evidence;
- verification evidence;
- gate result.

Do not consider the mere existence of a file as sufficient evidence.

# Project-Level Gates

## G0 - Project Definition Gate

Verify before launching development:

- objective defined;
- success metrics defined;
- IN / OUT scope defined;
- stakeholders identified;
- constraints known;
- main initial risks identified;
- PROCESS-SCOPE.md created;
- SYS/SWE/HWE/MLE/MECH/CYBER disciplines selected;
- responsibilities defined;
- configuration strategy defined;
- verification strategy planned.

G0 PASS means the project can enter its engineering cycle.

## G1 - Requirements Baseline Gate

Before baselining requirements:

- requirements sufficiently complete for the planned scope;
- stable identifiers;
- critical ambiguities resolved;
- contradictory requirements addressed;
- feasibility analyzed;
- priorities defined when necessary;
- verification criteria identified;
- traceability to upstream needs;
- allocation to domains performed for multi-domain projects;
- review performed;
- open changes identified.

G1 PASS authorizes the requirements baseline.

## G2 - Architecture Baseline Gate

Before baselining the architecture:

- important requirements allocated;
- architecture documented;
- interfaces identified;
- component responsibilities defined;
- main choices justified;
- non-functional constraints taken into account;
- feasibility analysis performed;
- requirements ↔ architecture traceability present;
- architecture reviewed.

G2 PASS authorizes detailed development.

## G3 - Release Readiness Gate

Before any release intended to be used or delivered:

- requirements of the release scope identified;
- expected verifications completed;
- residual anomalies assessed;
- exact configuration known;
- identifiable versions;
- consistent documentation;
- sufficiently complete traceability;
- QA performed;
- residual risks documented;
- release criteria satisfied.

A release must never be declared ready merely because the build works.

# SYS Definition of Done

## SYS.1 - Requirements Elicitation

DONE when:
- stakeholder needs identified;
- relevant needs documented;
- sources identified;
- critical ambiguities addressed;
- contradictory expectations analyzed;
- needs communicated to the parties concerned.

## SYS.2 - System Requirements Analysis

DONE when:
- system requirements specified;
- requirements structured and prioritized when necessary;
- feasibility analyzed;
- constraints and non-functional requirements covered;
- verification criteria identified;
- traceability to stakeholder needs established;
- consistency verified;
- review performed.

## SYS.3 - System Architectural Design

DONE when:
- system architecture defined;
- components and subsystems identified;
- interfaces defined;
- system requirements allocated;
- important architectural choices justified;
- performance and resource constraints considered;
- SYS requirements ↔ architecture traceability established;
- architecture reviewed.

## SYS.4 - System Integration and Integration Verification

DONE when:
- integration strategy defined;
- integration order controlled;
- interfaces integrated and verified;
- results recorded;
- anomalies recorded;
- tested configuration identifiable;
- traceability to relevant architecture and requirements established.

## SYS.5 - System Verification

DONE when:
- system verification strategy defined;
- system requirements of the scope covered;
- results recorded;
- acceptance criteria evaluated;
- anomalies documented;
- tested configuration known;
- requirements ↔ verification traceability established;
- results reviewed.

# SWE Definition of Done

## SWE.1 - Software Requirements Analysis

DONE when:
- software requirements identified and structured;
- functional and non-functional requirements covered;
- technical feasibility analyzed;
- environment impacts analyzed;
- verification criteria identified;
- traceability with system requirements established when applicable;
- traceability with system architecture established when applicable;
- requirements reviewed and communicated.

## SWE.2 - Software Architectural Design

DONE when:
- software architecture defined;
- components identified;
- interfaces identified;
- main behaviors described;
- requirements allocated to components;
- resource/performance constraints considered;
- main architectural choices justified;
- traceability with SWE requirements established;
- architecture reviewed.

## SWE.3 - Software Detailed Design and Unit Construction

DONE when:
- detailed design sufficiently defined;
- software units identified;
- internal interfaces defined;
- unit behavior described;
- code implemented;
- applicable conventions respected;
- code review performed when required;
- static analysis performed when required;
- design ↔ architecture ↔ requirements traceability maintained.

## SWE.4 - Software Unit Verification

DONE when:
- unit verification strategy defined;
- units of the scope verified;
- relevant nominal and edge cases covered;
- results recorded;
- failures analyzed;
- anomalies recorded;
- coverage assessed when relevant;
- tests ↔ units/design/requirements traceability available.

## SWE.5 - Software Component Verification and Integration Verification

DONE when:
- integration strategy defined;
- components integrated in a controlled order;
- interfaces verified;
- important interactions tested;
- results recorded;
- anomalies recorded;
- build configuration identifiable;
- traceability with architecture/requirements maintained.

## SWE.6 - Software Verification

DONE when:
- software verification strategy defined;
- software requirements of the scope covered;
- tests executed on an identifiable configuration;
- results available;
- residual anomalies assessed;
- acceptance criteria evaluated;
- bidirectional requirements ↔ verification traceability available;
- results reviewed.

# HWE Definition of Done

## HWE.1 - Hardware Requirements Analysis

DONE when:
- hardware requirements identified;
- relevant electrical interfaces specified;
- power supply, power and consumption constraints addressed;
- timing, precision and performance addressed when relevant;
- thermal and environmental constraints considered;
- mechanical constraints impacting electronics considered;
- feasibility analyzed;
- verification criteria defined;
- traceability to system requirements established;
- review performed.

## HWE.2 - Hardware Design

DONE when:
- hardware architecture defined;
- main components selected;
- schematics or corresponding design available;
- interfaces defined;
- power supply analyzed;
- relevant budgets analyzed;
- critical components identified;
- tolerances and derating considered when relevant;
- PCB constraints considered when relevant;
- requirements allocated to the design;
- traceability maintained;
- design review performed.

## HWE.3 - Verification against Hardware Design

DONE when:
- design verifications planned;
- necessary calculations, reviews, simulations or inspections executed;
- schematics verified;
- PCB/layout verified when applicable;
- interfaces and design rules verified;
- results recorded;
- deviations analyzed;
- anomalies addressed or recorded.

## HWE.4 - Verification against Hardware Requirements

DONE when:
- hardware requirements of the scope covered;
- verification methods defined;
- measurements/tests performed when hardware is available;
- test conditions recorded;
- relevant instrumentation identified;
- results and tolerances documented;
- anomalies recorded;
- tested hardware version identifiable;
- requirements ↔ results traceability established.

# MLE Definition of Done

## SUP.11 - Machine Learning Data Management

For a substantial ML project, DONE when:
- data sources identified;
- provenance documented;
- rights/licenses verified when relevant;
- inclusion/exclusion criteria known;
- transformations documented;
- datasets versioned;
- train/validation/test split controlled;
- data leakage examined;
- data quality assessed;
- data linked to the corresponding model version.

## MLE.1 - Machine Learning Requirements Analysis

DONE when:
- expected ML function defined;
- ML requirements derived from product needs;
- metrics identified;
- performance thresholds defined when possible;
- operational conditions specified;
- memory/latency/energy constraints considered;
- relevant edge cases and failure modes identified;
- ML requirements traceable to upstream requirements;
- review performed.

## MLE.2 - Machine Learning Architecture

DONE when:
- ML architecture defined;
- data pipeline defined;
- inputs/outputs defined;
- preprocessing and post-processing described;
- integration with the software defined;
- runtime constraints taken into account;
- important architectural choices justified;
- traceability with ML requirements maintained.

## MLE.3 - Machine Learning Training

DONE when:
- training dataset identified and versioned;
- training code versioned;
- important configuration/hyperparameters recorded;
- environment reproducible to a reasonable extent;
- training performed;
- training results recorded;
- produced model versioned;
- model ↔ data ↔ code ↔ configuration provenance available.

## MLE.4 - Machine Learning Model Testing

DONE when:
- independent test set identified;
- model tested against ML requirements;
- relevant metrics computed;
- acceptance thresholds evaluated;
- per-case/segment performance analyzed when relevant;
- failure cases documented;
- relevant bias analyzed when applicable;
- runtime constraints tested when relevant;
- tested model version identifiable;
- results recorded and reviewed.

# Cross-Domain Integration Gates

## CDG1 - Allocation Gate

Before domains start their detailed development:

- system requirements sufficiently mature;
- SYS → SWE/HWE/MLE/MECH allocation explicit;
- multi-domain interfaces identified;
- owners identified;
- allocation conflicts resolved.

## CDG2 - Interface Gate

Before integration:

Verify the relevant interfaces:
- electrical;
- mechanical;
- software API;
- communication protocol;
- timing;
- data format;
- units;
- coordinate systems;
- latency;
- bandwidth;
- power;
- thermal;
- safety;
- cybersecurity.

A critical interface must not remain purely implicit.

## CDG3 - Integration Readiness Gate

Before physical or software integration:

- planned components available;
- identifiable versions;
- sufficient component-level verifications;
- baselined interfaces;
- test environment available;
- instrumentation available;
- integration criteria defined;
- critical risks known.

## CDG4 - Product Verification Gate

Before user validation:

- product integrated in a known configuration;
- required SYS/SWE/HWE/MLE verifications performed;
- critical anomalies addressed;
- key performance evaluated;
- sufficiently complete traceability;
- baselined configuration.

## CDG5 - Validation Gate

Verify the product against:
- user needs;
- use cases;
- expected operational environment;
- success metrics;
- business constraints.

Verification answers:
"Did we build the product according to its requirements?"

Validation answers:
"Did we build the right product for its intended use?"

# Universal Definition of Done

A technical task is DONE only once the applicable criteria have been verified.

## 1. Scope
- objective achieved;
- acceptance criteria satisfied.

## 2. Artifact
- deliverable exists;
- canonical location known;
- name and version identifiable.

## 3. Review
- review performed when required;
- critical remarks addressed.

## 4. Verification
- appropriate verification executed;
- results recorded;
- failures analyzed.

## 5. Traceability
When applicable:
- upstream input identifiable;
- downstream output identifiable;
- traceability links updated.

## 6. Configuration
When applicable:
- known version;
- known Git commit/tag;
- known hardware revision;
- known dataset/model version.

## 7. Problems
- critical anomalies resolved;
- residual anomalies explicitly recorded.

## 8. Documentation
- impacted documents updated.

## 9. Quality
- applicable quality criteria satisfied.

## 10. Acceptance
- Main or the designated owner accepts the result.

If a mandatory condition fails:

status = REWORK or BLOCKED

and not DONE.

# No Jump-to-Code Rule

For substantial new development, do not start directly with implementation.

Before code, determine at minimum:
- need;
- applicable requirements;
- necessary architecture;
- interfaces;
- verification criteria.

The level of documentation can be adapted to the size of the project.

For a trivial fix or an exploratory prototype, the process can be lightened.

For an industrial or complex project:
- no process compression must remove indispensable evidence;
- any significant deviation must be explicitly documented in PROCESS-SCOPE.md.

Agility is compatible with this discipline:
steps can be iterative and incremental.

SPICE must not be interpreted as an obligation to finish the entire product specification before any implementation.

Each increment must nevertheless preserve:
- requirements;
- necessary architecture;
- implementation;
- verification;
- traceability;
- configuration.

# Project Standards and Conventions

At the start of any substantial technical project, create:

00-project/STANDARDS.md

This file must explicitly select the applicable conventions.

It must contain when relevant:

- process standards;
- contractual requirements;
- safety standards;
- cybersecurity standards;
- coding standards;
- language versions;
- toolchains;
- naming conventions;
- document conventions;
- requirement conventions;
- verification conventions;
- hardware design rules;
- ML/data rules;
- mechanical rules;
- Git workflow;
- storage policy;
- review policy;
- quality thresholds.

Do not silently invent a new convention midway through the project.

If a convention must change:
- document the change;
- analyze the impact;
- update STANDARDS.md.

The reference documents in {baseDir}/references are the default values when the project does not impose anything more specific.

# Standard Work Product Templates

The standard templates are available under:

{baseDir}/templates/

When creating a project:
1. read PROCESS-SCOPE.md;
2. select only the necessary work products;
3. instantiate the corresponding templates in the project's canonical space;
4. replace all placeholders;
5. never let an unadapted template document be presented as a final deliverable.

The templates define a minimal structure.
They can be enriched according to:
- the client;
- the domain;
- regulation;
- the criticality level;
- applicable standards.

Contractual or regulatory standards take priority over these templates.

# Work Product Instantiation Rules

When a project is created or a new process enters the scope:

1. consult {baseDir}/templates/README.md;
2. determine the necessary work products;
3. instantiate the relevant templates in the project's canonical folder;
4. assign Document IDs and Configuration Item IDs;
5. update CONFIGURATION-ITEMS.md;
6. create the necessary traceability links.

Do not systematically create all templates.

Examples:

Simple SaaS project:
- PROJECT
- PROCESS-SCOPE
- STANDARDS
- SWE requirements
- SWE architecture
- test specifications
- traceability
- configuration
- risks
- changes/problems
- release notes

Edge AI drone project:
add in particular:
- SYS requirements/architecture
- HWE requirements/design
- SWE requirements/architecture/design
- MLE requirements/architecture
- DATA-CARD
- MODEL-CARD
- interface specifications
- integration verification
- multi-domain traceability

During a modification:
do not recreate an existing document.
Update the existing instance following configuration management rules.

# Autonomous Task Execution

For substantial projects, use the engine:

{baseDir}/scripts/project_state.py

and the reference document:

{baseDir}/references/execution-engine.md

## Machine state

The machine source of task state is:

00-project/management/TASKS.json

A human-readable view is automatically maintained in:

00-project/management/TASKS.md

Do not modify TASKS.json manually except for controlled repair.

## Initialization

When creating an executable project:
- instantiate the project space;
- initialize TASKS.json;
- create tasks with their dependencies, domains, processes, requirements and acceptance criteria.

## Execution loop

For each execution cycle:

1. refresh
2. read READY tasks
3. check WIP and conflicts
4. choose the highest-priority tasks
5. move each chosen task to IN_PROGRESS
6. delegate to the appropriate agent
7. wait for/collect its result
8. record the evidence
9. move to REVIEW
10. apply the relevant Definition of Done and gates
11. if PASS: accept → DONE
12. otherwise: REWORK or BLOCKED
13. refresh
14. update STATUS.md, traceability, risks and configuration if necessary

Main alone is authorized to call the accept transition.

## No blind execution

Do not automatically execute a task if:
- its acceptance criteria are absent;
- it involves an unapproved irreversible decision;
- it requires an unavailable secret or access;
- it involves an unevaluated safety/security risk;
- a mandatory gate is FAIL;
- a dependency is unsatisfied.

In these cases:
BLOCKED or user decision depending on context.

# Mandatory Repository Selection

When bootstrapping a new project, ask or determine before execution:

- Git backend: GitHub or GitLab;
- canonical repository;
- organization / namespace;
- visibility;
- branching strategy;
- CI/CD strategy.

GitHub or GitLab is mandatory.

Google Drive is optional and complementary.

If the user wants both GitHub and GitLab:
- designate a PRIMARY_GIT_REMOTE;
- use the other as a secondary remote or mirror;
- never create two competing sources of truth.

A project must not be declared correctly initialized until its canonical Git repository is identified.

# Robust Project Bootstrap

The canonical bootstrap engine is:

python3 {baseDir}/scripts/bootstrap_project.py

Supported canonical Git backends:
- GitHub;
- GitLab SaaS;
- GitLab Self-Managed.

At least one Git remote is mandatory.

Google Drive is optional and complementary.

The bootstrap lifecycle is:

PRECHECK -> CREATE/RESUME -> VERIFY -> COMPLETE

The bootstrap must:
- validate templates and Project Manager engine before creation;
- validate Git identity;
- validate backend API authentication;
- validate Git transport;
- persist bootstrap state;
- resume safely after interruption;
- never automatically delete a remote repository;
- separate remote creation from initial push;
- verify local HEAD against the configured remote branch;
- configure the canonical default branch only after it exists;
- write BOOTSTRAP-STATUS.json only after successful verification.

GitLab Self-Managed must respect the existing glab host/API configuration and SSH configuration rather than duplicating credentials or private keys.

GitHub and GitLab credentials remain isolated by host.

A project is not considered initialized until its mandatory remote Git repository is reachable and synchronized.

## Automated Project Quality Audit

Every technical project bootstrapped by Project Manager MUST embed autonomous
project-quality tooling under:

`tools/project-audit/`

Canonical audit tools:

- `project_audit.py`
- `requirements_lint.py`
- `traceability_check.py`
- `release_check.py`
- `pm_common.py`

### Development quality checks

Normal development CI MUST execute:

1. project structure/configuration audit;
2. requirements lint;
3. requirements traceability audit.

An incomplete project MAY produce SKIP or warnings for content that is not yet
required by the current lifecycle state.

### Release quality gate

A release MUST execute the strict release gate.

The release gate MUST fail when, as applicable:

- project governance is structurally invalid;
- mandatory requirements are missing or invalid;
- requirement IDs are duplicated;
- traceability is incomplete or inconsistent;
- critical project tasks remain unresolved;
- G3 Release Readiness is not PASS or PASS_WITH_ACTIONS;
- the Git worktree is dirty;
- the validated commit does not correspond to the expected local/upstream/CI commit.

### Repository autonomy

CI execution MUST NOT depend on the OpenClaw workspace being available.

Audit scripts MUST therefore be copied into and versioned with each technical
project repository during bootstrap.

### GitLab

Generated GitLab projects MUST provide:

- `project-governance`;
- `project-quality`;
- `release-gate`.

Project Manager GitLab jobs use the `project-manager` runner tag.

Normal development quality checks execute automatically.

The release gate:
- executes automatically for release tags;
- MAY be triggered manually on the default branch;
- MUST NOT block ordinary development merely because G3 is not yet PASS.

### GitHub

Generated GitHub projects MUST provide:

- `.github/workflows/project-quality.yml`;
- `.github/workflows/project-release.yml`.

Project Quality executes on normal pushes and pull requests.

Project Release Gate executes on release tags or explicit workflow dispatch.

### Gate semantics

Passing bootstrap is not equivalent to passing release readiness.

Expected lifecycle behavior:

BOOTSTRAP PASS
→ DEVELOPMENT AUDITS
→ REQUIREMENTS / TRACEABILITY MATURITY
→ G3 RELEASE READINESS
→ STRICT RELEASE GATE
→ RELEASE

The automated audit layer supports engineering governance and ASPICE-like
discipline but MUST NOT be represented as formal Automotive SPICE
certification or assessment evidence by itself.


## Project Manager Self-Check

After any modification to Project Manager scripts, templates,
domain configuration, bootstrap logic, CI generation,
release gates, or audit rules, run:

`~/.openclaw/workspace/skills/project-manager/scripts/project_manager_self_check.py`

The self-check is read-only.

It validates:

- required Project Manager scripts;
- Python compilation;
- bootstrap consistency;
- engineering-domain configuration;
- requirement prefixes and domain directories;
- work-product registries and required templates;
- bootstrap and audit-tool integration;
- supported archetypes;
- strict release-gate integration.

It also validates the MLE, CYBER and MECH reference projects,
Git working-tree cleanliness, and bootstrap completion state.

Exit codes:

- `0`: PASS
- `1`: PASS WITH REVIEW
- `2`: FAIL

A Project Manager modification is validated only after:

`SELF CHECK STATUS: PASS`

Warnings must be reviewed. Failures must be corrected.
The self-check complements project-specific quality gates.
