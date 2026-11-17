# UAT and production transition verification

## Distinguish between three types of verification

| Type | Question answered | Key performer | What cannot be proven |
|---|---|---|---|
| Offline evaluation | Does the model, rule, or workflow meet standards on frozen samples | Evaluation leader | Real user adoption, real integration, and production runs |
| POC on-site operation | Ability to complete core tasks in controlled customer scenarios | FDE, user representatives, technical on duty | Full production, long-term value and organizational promotion |
| UAT | Whether authorized users accept the behavior of a specified version in a specified business process | Business acceptors and real users | Security approval, production SLO or final ROI |

The three types of results are recorded separately; offline scores may not be used to replace UAT, and user reviews may not be used to offset hard failures.

## UAT entry conditions

- POC deeds, PRDs and acceptance criteria have been frozen;
- Versions, environments, datasets, models, knowledge bases and configurations are identifiable;
- CoreS0/S1defect has been closed or accepted by the rightful owner;
- Users, tasks, samples and abnormal paths are representative;
- Role permissions, data boundaries, manual upgrade and stop methods have been explained;
- Each scenario has expectations, evidence collection and business acceptance persons;
- Users know this is acceptance, not a training demonstration or satisfaction interview.

## UAT scenario table

```markdown
| UAT | User/role | Real task | Pre-data | Operation | Expected results | Prohibited results | Evidence | Acceptor |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
```

At least normal, missing, conflict, override, system failure and manual takeover are covered. High-risk tasks should also cover repeated execution, timeouts, partial failures, undo, and recovery.

## Shadow mode

When the risk of directly changing business results is too high, first let the system generate recommendations on real traffic but not execute them:

- The user continues to complete the task according to the original process;
- System output and real results are saved in parallel;
- Evaluate latency, quality, failures, coverage and labor variances;
- Do not secretly display shadow results as adopted;
- Reconfirm risks and success criteria before entering a controlled pilot.

## Acceptance conclusion

Each UAT scenario can only be marked as: passed, passed with conditions, failed, blocked, or not executed. Summary conclusions must state:

- Which users and tasks are covered;
- Whether failure and non-execution change the decision to continue;
- Which issues report back to PRD, Architecture, Skill Design or Operational Design;
- Which gaps are left for production transition and who has the right to accept them;
- Next round of releases and return scope.

## Evidence given to Stage 7

- Target users, participating users, task completion and rejection/bypass;
- First time success, repeated use and actual manual modification;
- Level of training, on-site support and FDE involvement;
- Added or deleted steps in the workflow;
- Technology limitations, production gaps, support needs and complete costs;
- Scenarios for user acceptance versus explicit rejection.

UAT approval does not mean production approval, nor does it mean full user adoption. Stage 7 must continue to observe long-term behaviors and business results.
