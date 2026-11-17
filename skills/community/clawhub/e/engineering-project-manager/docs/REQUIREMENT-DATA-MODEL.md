# Requirement Data Model

Version: 1.1

## Identifier

Stable identity:

`<PROJECT>_<PROCESS>_REQ_<SEQ>`

Revision-specific identity:

`<PROJECT>_<PROCESS>_REQ_<SEQ>@R<REV>`

Examples:

`M5_SYS2_REQ_001@R1`
`M5_SWE1_REQ_014@R3`
`DRONE_HWE1_REQ_027@R2`

Process codes contain no dots: SYS1, SYS2, SWE1, HWE1, etc.

Sequence numbers are never reused.
A semantic change creates a new revision.

For revision R2 and later, `Change_ID` is mandatory. When Configuration
Management V1.1 is enabled, it must reference an existing controlled Change
Request whose Changed Items identify the previous or new exact requirement
revision. Use `change_manager.py revise-requirement`; never edit a RELEASED
historical revision in place.

## Canonical Requirement Block

A requirement starts directly with its revisioned identifier
between square brackets and ends with `[END_REQ]`.

Example:

[M5_SYS2_REQ_001@R3]
Status: RELEASED
Upstream: M5_SYS1_REQ_003@R2, M5_SYS1_REQ_007@R1
Allocated_To: SWE1
Verification_Method: TEST
Verification_Scope: SYSTEM
Verification_Activity: VERIFICATION
Verification_Process: SYS5
Implementation_Milestone: M2
Verification_Milestone: M3
Owner: SYS
Priority: MUST
Change_ID: CR-023
Rationale: Required to guarantee the system reaction time.
Acceptance_Criteria: Communication loss shall be detected within 100 ms.
Text:
The system shall detect loss of communication within 100 ms.
[END_REQ]

`Text:` is always the final attribute.

Everything after `Text:` and before `[END_REQ]`
is the normative requirement body.

The body may contain multiple lines.

## Upstream Traceability

`Upstream` contains exact revision-specific requirement references.

Multiple references are comma-separated.

The parser shall ignore optional spaces after or before commas.

Examples:

Upstream: M5_SYS1_REQ_003@R2,M5_SYS1_REQ_007@R1

Upstream: M5_SYS1_REQ_003@R2, M5_SYS1_REQ_007@R1

Both forms are equivalent.

Special exclusive values:

- `ROOT`: requirement imported or created as a root project requirement.
- `DERIVED`: engineering-derived requirement without a formal upstream requirement.

ROOT and DERIVED cannot be combined with requirement IDs.

When Upstream is DERIVED, Rationale is mandatory.

All active upstream references must include an exact revision.

## Allocation

`Allocated_To` identifies the single downstream engineering process
expected to cover the requirement.

Example:

Allocated_To: SWE1

A downstream requirement from another process does not satisfy
the allocation.

Example:

M5_SYS2_REQ_021@R1
Allocated_To: SWE1

may be covered by:

M5_SWE1_REQ_034@R1

but not by:

M5_HWE1_REQ_012@R1

`Allocated_To: NONE` is permitted for a terminal requirement
that is not expected to generate another requirement layer.

Allocation and verification responsibility are independent.

## Verification

Each requirement has exactly one verification strategy.

Mandatory attributes:

- Verification_Method
- Verification_Scope
- Verification_Activity
- Verification_Process

Methods:

- TEST
- ANALYSIS
- INSPECTION
- SIMULATION
- CODE_REVIEW
- REVIEW
- DEMONSTRATION

Scopes:

- UNIT
- COMPONENT
- SOFTWARE
- HARDWARE
- MODEL
- SUBSYSTEM
- SYSTEM
- PRODUCT

Activities:

- UNIT_VERIFICATION
- INTEGRATION
- VERIFICATION
- VALIDATION
- ACCEPTANCE

Example:

Verification_Method: TEST
Verification_Scope: SYSTEM
Verification_Activity: INTEGRATION
Verification_Process: SYS4

## Status and Revision Rules

Allowed statuses:

- DRAFT
- REVIEWED
- RELEASED
- CANCELLED

Normal lifecycle:

DRAFT -> REVIEWED -> RELEASED

A semantic modification creates a new revision.

A new revision always returns to DRAFT.

Evidence against an older revision does not automatically
verify a newer revision.

CANCELLED requirements remain in the specification and history
but are excluded from active coverage, implementation,
verification and release-readiness calculations.

Historical traceability is retained.

## Milestones

Every active requirement has:

Implementation_Milestone

Verification_Milestone is optional.

Implementation and verification may therefore occur
in different project milestones.

## External Specifications

Source document metadata is not repeated on each requirement.

External customer or stakeholder specifications are first
normalized into a compliance matrix.

The compliance matrix extracts, orders and assigns project
requirement identifiers to incoming requirements.

Those tagged root requirements then use:

Upstream: ROOT

All downstream provenance is represented by revision-aware
Upstream links.
