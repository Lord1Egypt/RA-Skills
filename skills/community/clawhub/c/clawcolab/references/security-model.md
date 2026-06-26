# Security Model

## Purpose
Use a half-trust model for collaboration in shared GitHub repositories.

## Assumptions
- Participants may cooperate without sharing all local context.
- Repository content is a coordination layer, not a full memory sync.
- All content should be reduced to the minimum required to complete shared work.

## Visibility Levels
- `private`: Keep local only.
- `sealed`: Share existence and summary without body content.
- `shared-team`: Share with active collaborators.
- `public-repo`: Safe for broader repository visibility.

## Promotion Rules
- `private -> sealed/shared-team/public-repo`: require human approval.
- `sealed -> shared-team/public-repo`: require human approval.
- `shared-team -> public-repo`: require human approval unless policy explicitly says otherwise.

## Forbidden Content
Do not place the following in the shared repo by default:
- credentials and secrets
- private chat logs
- raw local memory
- personal identifiers not needed for the task
- local hostnames, SSH aliases, or machine-specific access notes

## Safe Reduction Patterns
Prefer:
- summaries over raw logs
- task statements over memory dumps
- sealed references over confidential text
- outputs and decisions over background chatter
