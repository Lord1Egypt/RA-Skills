# Autonomous Execution Engine

## Authority

Main is the sole authority for managing project state.

Dev, Cyber, or any subagent:
- execute a task;
- produce artifacts;
- provide evidence;
- report problems and limitations.

They do not declare a task DONE themselves.

## Task lifecycle

BACKLOG
→ READY
→ IN_PROGRESS
→ REVIEW
→ DONE

Alternative transitions:

IN_PROGRESS → BLOCKED
REVIEW → REWORK
REWORK → READY
BLOCKED → READY
BACKLOG/READY → CANCELLED

## Dependency Gate

A task can only become READY if all of its mandatory dependencies are DONE.

Never bypass a dependency without a documented decision. The task engine
validates identifiers, dependency references, cycles, priorities, statuses and
canonical list fields before every write. Mutating commands use an exclusive
lock and atomic JSON/Markdown replacement so concurrent agents cannot silently
lose task updates.

## Execution Gate

Before IN_PROGRESS verify:
- inputs available;
- requirements identified when applicable;
- relevant baseline known;
- competent agent selected;
- acceptance criteria defined;
- applicable Definition of Done known;
- canonical location of results known.

## Review Gate

Before DONE verify:
- artifact actually created;
- acceptance criteria satisfied;
- necessary tests/reviews performed;
- evidence available;
- traceability updated;
- configuration identifiable;
- impacted documentation updated;
- critical anomalies resolved or formally accepted.

## Rework

If a mandatory criterion fails:
- status = REWORK;
- document the cause;
- specify what must be corrected;
- keep the previous evidence;
- do not erase history.

## WIP

By default:
- maximum 3 tasks IN_PROGRESS simultaneously (enforced by the task engine);
- avoid several concurrent tasks modifying the same artifacts;
- favor parallelism only for independent tasks.

Main may reduce WIP for critical tasks.

## Agent routing

MAIN:
- PM;
- business;
- requirements;
- synthesis;
- documents;
- arbitration.

DEV:
- SWE;
- technical MLE;
- code;
- tests;
- CI;
- data/finance.

CYBER:
- cybersecurity;
- network;
- infrastructure;
- hardening;
- audits.

For HWE, SYS or MECH:
main coordinates and uses the appropriate available tools/agents.

## Evidence

Every substantial task must accumulate appropriate evidence:

SWE:
- commit/PR;
- build;
- tests;
- lint/static analysis;
- review;
- traceability.

HWE:
- schematic/design;
- ERC/DRC;
- calculations;
- review;
- measurements/tests.

MLE:
- code commit;
- dataset/model versions;
- experiment ID;
- metrics;
- model test.

SYS:
- requirements/architecture;
- interface review;
- integration/verification evidence.

Documentation:
- document;
- version;
- review;
- approval when necessary.

## Drive

Git is the canonical source of engineering state, requirements, code and
reproducible artifacts in every storage mode. Drive is optional complementary
storage for office documents and external or large files, as recorded in
STORAGE-MAP.md. It does not replace the engineering repository.

Any task producing a Drive deliverable must record:
- Drive folder;
- file ID or link;
- version;
- status.

## Git

For a substantial SWE task:
- create/use the planned branch;
- link Task ID and Requirement IDs;
- record commit/PR as evidence;
- do not consider the merge alone as proof of compliance.
