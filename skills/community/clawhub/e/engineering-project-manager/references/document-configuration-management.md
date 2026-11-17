# Document and Configuration Management

## Principle: a single canonical source

Each Configuration Item must have a single, clearly identified source of truth.

Maintain in each project:

00-project/STORAGE-MAP.md
08-configuration/CONFIGURATION-ITEMS.md
08-configuration/BASELINES.md

STORAGE-MAP.md indicates for each category:
- canonical location;
- working location;
- backup;
- access;
- versioning tool.

Never silently keep two competing versions of the same Configuration Item.

# Storage types

## Git

Git is mandatory as the engineering source of truth for:
- source code;
- scripts;
- configuration files;
- tests;
- Markdown documentation;
- requirements stored as text;
- textual architecture;
- CI/CD;
- reproducible files;
- small data needed for the build.

Git is the version reference for these elements in all storage modes.

## Google Drive

Preferably use Drive for:
- DOCX;
- PDF;
- PPTX;
- user-facing XLSX;
- contracts;
- office documents;
- signed or approved reports;
- large reference documents;
- external deliverables;
- assets not suited to Git.

For a complementary document whose authoritative copy is in Drive, record its
ID, version and purpose in STORAGE-MAP.md. Drive never replaces engineering Git.

## Local disk

The local disk may be:
- working copy of the canonical Git repository in LOCAL mode;
- working space;
- generation cache.

A temporary local copy does not automatically become an official Configuration Item.

## Large files

Do not automatically store in Git:
- large datasets;
- large ML models;
- videos;
- large binaries;
- build outputs;
- large archives.

Use Drive, dedicated storage, or Git LFS only if it is explicitly configured.

# Configuration Item Register

CONFIGURATION-ITEMS.md must be able to contain:

- CI ID;
- name;
- type;
- domain;
- owner;
- status;
- version/revision;
- canonical location;
- repository/Drive ID;
- baseline;
- classification;
- access rights when relevant;
- last modification;
- associated change request;
- applicable backup.

# Document statuses

Mainly use:

- DRAFT
- REVIEW
- APPROVED
- BASELINED
- RELEASED
- OBSOLETE
- ARCHIVED

Do not directly modify a BASELINED or RELEASED item without going through the applicable change process.

# Document metadata

Every substantial engineering document must identify at minimum:

- Document ID
- Title
- Project
- Process / Domain
- Owner
- Status
- Version
- Date
- Approver when necessary
- Configuration Item ID
- Classification when necessary

# Naming rules

## Files versioned by Git

Use a stable name.

Examples:

PROJECT.md
PROCESS-SCOPE.md
STANDARDS.md
SWE-REQUIREMENTS.md
SOFTWARE-ARCHITECTURE.md
TRACEABILITY.md

Do not write:

SOFTWARE-ARCHITECTURE-v7-final-final2.md

Git already carries the history.

## Office deliverables / Drive

Use:

<project-slug>_<document-id>_<short-title>_v<major>.<minor>_<status>.<ext>

Examples:

tajer-ai_BP_business-plan_v1.0_RELEASED.pdf
tuneaccess_SWE-SRS_software-requirements_v1.2_APPROVED.docx
robot-ai_SAD_software-architecture_v0.4_REVIEW.pdf

Names must:
- be understandable;
- stay reasonably short;
- avoid ambiguous characters;
- avoid "final", "new", "latest", "final2".

# Versioning

Default convention:

v0.x: non-baselined document
v1.0: first major baseline/release
v1.x: approved compatible changes
v2.0: major baseline or structure change

For hardware, separately use a Hardware Revision:
HW-REV-A
HW-REV-B

For delivered software:
use Semantic Versioning when relevant.

# Git conventions

Default branches:

feat/<task-id>-short-description
fix/<problem-id>-short-description
docs/<task-id>-short-description
refactor/<task-id>-short-description
test/<task-id>-short-description

Every substantial Pull Request must reference when relevant:
- Task ID;
- Requirement IDs;
- Change Request;
- Problem Report;
- tests executed;
- results;
- documentation impacts.

Commits must be understandable and atomic.

An important baseline must be linkable to:
- commit;
- tag;
- release;
- dependency configuration.

# Baselines

A baseline must specify:
- scope;
- included Configuration Items;
- versions;
- date;
- reason;
- approval;
- Git commit/tag when applicable;
- Drive documents when applicable.

# Backup and Recovery

For each critical category, define:
- where the canonical copy resides;
- how it is backed up;
- how it can be restored.

Do not consider GitHub or Drive as a complete backup strategy without explicitly defining the recovery mechanism.

# Requirements Engineering Rules

# Requirement IDs

IDs are unique, stable, and must not be reused after deletion.

Default prefixes:

STK-REQ-### : stakeholder
SYS-REQ-### : system
SWE-REQ-### : software
HWE-REQ-### : hardware
MLE-REQ-### : machine learning
MEC-REQ-### : mechanical
CYB-REQ-### : cybersecurity

Example:
SYS-REQ-0042

Do not renumber all requirements simply to fill a gap.

# Mandatory attributes

Every substantial requirement must contain when applicable:

- ID
- Title
- Requirement Text
- Rationale
- Source
- Domain
- Type
- Priority
- Status
- Owner
- Verification Method
- Acceptance Criteria
- Parent Requirement
- Allocated Element
- Downstream Requirements
- Verification IDs
- Change Request
- Criticality
- Safety Classification if applicable
- Cybersecurity Classification if applicable
- Version / Baseline
- Tags when useful

# Requirement types

Possible types:

- FUNCTIONAL
- PERFORMANCE
- INTERFACE
- CONSTRAINT
- SAFETY
- SECURITY
- USABILITY
- DIAGNOSTIC
- DATA
- ENVIRONMENTAL
- OPERATIONAL
- REGULATORY

# Status

Mainly use:

- DRAFT
- REVIEWED
- APPROVED
- BASELINED
- IMPLEMENTED
- VERIFIED
- REJECTED
- OBSOLETE

# Requirement wording

A requirement must be:

- necessary;
- clear;
- unambiguous;
- atomic;
- consistent;
- feasible;
- verifiable;
- traceable.

A normative requirement uses explicit wording.

In English:
"The system shall ..."

Avoid vague terms such as:
- fast;
- easy;
- appropriate;
- sufficient;
- optimal;
- user-friendly;
- as soon as possible;

unless accompanied by a measurable criterion.

# Atomicity

A requirement should ideally cover a single verifiable obligation.

Avoid:

"The controller shall acquire the current and filter it and transmit it over CAN."

Prefer several requirements when the obligations can be verified independently.

# Quantification

Specify when relevant:
- min;
- max;
- nominal;
- tolerance;
- unit;
- conditions;
- timing;
- environment.

Example:

SWE-REQ-0123
The control task shall execute every 1 ms with a maximum release jitter of 50 us under nominal operating conditions.

# Implementation independence

Requirements must express WHAT before HOW.

Do not impose a technical solution in a requirement unless it is genuinely an imposed constraint or decision.

# Verification Method

Mainly use:

- TEST
- ANALYSIS
- INSPECTION
- REVIEW
- DEMONSTRATION

A requirement may need several methods.

# Acceptance Criteria

A requirement is not verifiable merely because "TEST" is indicated.

Define the result that allows a PASS or FAIL conclusion.

# Traceability

Maintain:

Stakeholder
↕
System
↕
Domain
↕
Architecture
↕
Design / Implementation
↕
Verification

Links must be bidirectional when the process requires it.

# Baseline changes

After baselining:
- do not silently modify the text;
- use a Change Request when the change is significant;
- analyze the impact on architecture, code, hardware, model, tests and documentation.

# Reviews

A requirements review checks in particular:
- clarity;
- testability;
- consistency;
- uniqueness;
- feasibility;
- interfaces;
- units;
- traceability;
- absence of a prematurely imposed solution;
- acceptance criteria.

# Mandatory Git Repository Policy

## Mandatory Git remote

Every project managed by Project Manager must have at least one remote Git repository.

Allowed backends:
- GitHub;
- GitLab.

At project bootstrap, explicitly choose:

GIT_BACKEND = GITHUB
or
GIT_BACKEND = GITLAB

A project must not enter normal execution until a canonical remote Git repository has been defined.

## Source of truth

The canonical Git repository is the source of truth for in particular:

- source code;
- scripts;
- configuration;
- CI/CD;
- tests;
- Markdown documentation;
- textual requirements;
- textual architecture;
- traceability;
- Project Manager state when appropriate;
- standards;
- instantiated templates;
- reproducible manifests.

## Simultaneous GitHub + GitLab

Both may be used, but only one must be declared:

PRIMARY_GIT_REMOTE

The other may be:
- mirror;
- backup;
- secondary destination.

Never maintain two diverging primary repositories.

## Google Drive

Google Drive is optional.

It may be used in particular for:
- DOCX;
- XLSX;
- PPTX;
- PDF;
- signed documents;
- client documents;
- large files;
- assets;
- binary files poorly suited to Git;
- external deliverables.

Drive does not replace GitHub or GitLab for:
- development versioning;
- configuration management;
- branches;
- Pull/Merge Requests;
- code review;
- tags;
- releases;
- CI/CD.

## CI/CD

The canonical Git backend must carry the project's CI/CD pipeline when CI/CD is applicable.

Depending on the backend:

GitHub:
- GitHub Actions by default when appropriate.

GitLab:
- GitLab CI/CD by default when appropriate.

The pipeline must be versioned in the repository.

Every technical release must be linkable to:
- repository;
- commit;
- tag;
- pipeline;
- verification results;
- baseline.
