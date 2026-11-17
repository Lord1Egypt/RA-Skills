# Requirements Specification

## Metadata

- Document ID:
- Domain:
- Owner:
- Status:
- Version:
- Baseline:
- Date:

## Scope

Describe the scope covered by this specification.

## Requirement Template

Use the revision-aware V1.1 block below. Do not add a Markdown heading for an
individual requirement. Replace every angle-bracketed placeholder before
review or release.

```text
[<PROJECT>_<PROCESS>_REQ_<SEQ>@R<REV>]
Status: DRAFT
Upstream: ROOT
Allocated_To: <PROCESS_OR_NONE>
Verification_Method: <METHOD>
Verification_Scope: <SCOPE>
Verification_Activity: <ACTIVITY>
Verification_Process: <PROCESS>
Implementation_Milestone: <MILESTONE>
Verification_Milestone: <MILESTONE_OR_NONE>
Owner: <DOMAIN_OR_ROLE>
Priority: <PRIORITY>
Change_ID: <CR_ID_FOR_R2_AND_LATER>
Rationale: <WHY_THE_REQUIREMENT_EXISTS>
Acceptance_Criteria: <OBJECTIVE_PASS_OR_FAIL_CRITERION>
Text:
The system shall provide the required behavior under specified conditions.
[END_REQ]
```

`Text:` is the final attribute. Everything after it and before `[END_REQ]` is
normative requirement text. Use exact revision references in `Upstream`.
`ROOT` and `DERIVED` are exclusive special values; `DERIVED` requires a
rationale. Omit `Change_ID` for R1 and provide it for R2 and later.

## Requirements

Add controlled requirements below using the canonical block format.
