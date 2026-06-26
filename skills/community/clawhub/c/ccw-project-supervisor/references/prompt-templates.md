# Prompt Templates

## workflow-plan template

Use this when turning a PRD or backlog into a plan.

```text
workflow-plan "
This is a [greenfield/existing] software project.

Project goal:
[goal]

Current status:
[current status]

Requirements:
1. Group by milestones and epics
2. Make dependencies explicit
3. Identify the shortest runnable path
4. Identify parallelizable work
5. Attach acceptance criteria and test points to each issue
6. Output issue drafts ready for /issue/plan

Constraints:
- [constraint 1]
- [constraint 2]
- [constraint 3]

Backlog:
[paste backlog]
"
```

## /issue/plan template

```text
/issue/plan "
Based on the approved project plan, generate execution-ready issues.

Requirements:
- keep epic grouping
- preserve dependencies
- include acceptance criteria
- include test points
- keep scope inside p0 unless otherwise stated
"
```

## /issue/queue template

```text
/issue/queue "
Based on the approved issues, generate the shortest runnable path and identify parallel work.

Requirements:
- do not start with premature optimization
- do not pull complex layout before the base editing loop
- keep the first issue low ambiguity and easy to verify
"
```
