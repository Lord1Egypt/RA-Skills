# Minimum runnable POC build mode

## When to enter

Only enter when the user explicitly asks to "generate a demo, build a runnable POC, create a skills file or quickly verify the interaction" and the PRD, architecture and permission boundaries are clear enough. Only continue to output skill design packages when design requests are made, and do not create codes without authorization.

POC construction belongs to Stage 5 because it packages an approved scenario into an executable skill and demo shell. Stage 6 runs and evaluates it against frozen evidence; “it starts” is not POC success.

## Three delivery depths

| Mode | Applicability | Delivery | No Commitment |
|---|---|---|---|
| Design Packages | Unknown platform, directory, or permissions | Roles, Workflows, Guardrails, Assessment Designs | Can install or run |
| Minimum runnable skeleton | Need to quickly display interaction and failure status | Static interface, Mock, logic, evaluation, checklist | Real integration, production performance |
| Controlled integration POC | Interfaces, credentials, environment and approvals in place | Limited tools, read-only/controlled actions, audits and rollbacks | Production rollout and value at scale |

The lowest depth that answers the project's key uncertainties is selected by default. When it is only used to demonstrate visual effects, it will not be connected to the real customer system.

## Skeleton generation

```text
node scripts/scaffold-poc.js --output <target-directory> --name <POC-name> --scenario <scenario-description> --project-id <ID>
```The script copies the reference skeleton without third-party dependencies from`assets/minimal-poc/`without overwriting the existing directory. After building run:```text
node <target directory>/evals/run-evals.js
node <target directory>/server.js
```

The default skeleton only demonstrates the following contracts:

- Block when input is missing;
- Untrusted text cannot modify system boundaries;
- The output clearly requires manual review;
- Does not have the ability to write to external systems;
- The page displays Mock, version and non-production statement;
- The evaluation can be run repeatedly without models and networks.

## Adapt to real scenes

After generating the skeleton, replace it in the following order, do not start by modifying the interface copy:

1. Write the user story, acceptance criteria and hard failure of PRD into `poc-manifest.json`;
2. Change the Mock sample to test data with source, license, representativeness and version;
3. Implement deterministic access control in `logic.js` or skill core, and then add generative capabilities;
4. Expand `evals/cases.json` for normal, boundary, failure, safety and unauthorized scenarios;
5. Differentiate between facts, inferences, gaps, suggestions, and human decisions in the interface;
6. Real tools define purpose, minimum permissions, failure, idempotence, auditing and manual confirmation one by one;
7. Before access, the deployment architecture will review data, identity, network, logs, rollback and operational responsibilities;
8. Give the full version to Stage 6 to freeze and run.

## `poc-manifest.json` Minimum field

- POC ID, name, scenario, version and status;
- Input, output and presentation paths;
- Mock/real data boundaries;
- External actions and permissions;
- Acceptance criteria, hard failures, evaluation commands;
- Known limitations, production gaps and next owners.

Listings describe current construction facts, not future visions. When there is no real interface, write `mock_only` and cannot write "Integrated"; when there is no security approval, write "To be reviewed" and cannot write "Safe and Available".

## Build completion definition

- You can start it by pressing the list command in a clean environment;
- At least one normal scenarios and one blocking scenarios are operable;
- Pass the smoke test and retain the original results;
- Version, mock, permission and non-production boundaries are visible in pages and manifests;
- No undeclared network, write, key or third-party dependencies;
- PRD acceptance, implementation location and evaluation cases are traceable;
- Known limitations and validation issues handed over to Stage 6 are clarified.

## Situations that must stop

- User requests access to production without clear authorization, environment or rollback;
- The true data source, permission or de-identification status is unknown;
- High-risk actions are blocked only by prompt words;
- Demo needs to fake online capabilities, real effects or customer indicators;
- Skeleton conflicts with PRD/architecture boundaries;
- Unable to log running versions, inputs, outputs and failures.
