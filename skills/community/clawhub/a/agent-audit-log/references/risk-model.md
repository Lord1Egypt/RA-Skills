# risk-model

## Low risk
Use for:
- local documentation updates
- changelog or README edits
- low-impact local tooling changes
- identity cleanup that does not change external access

## Medium risk
Use for:
- repository creation and visibility changes
- external publication
- auth setup
- browser/manual login recovery attempts
- session maintenance
- non-sensitive local installs

## High risk
Use for:
- secret injection
- privileged/system-level updates
- changes that alter sensitive access paths
- operations with meaningful blast radius if wrong

## Rule
If an action changes access, secrets, publication surface, or system behavior, classify conservatively.
