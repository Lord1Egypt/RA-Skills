# Agent skill design package template

```markdown
## 1. Skill positioning
- Skill name and target platform:
- Service objects and usage scenarios:
- Tasks to be completed:
- What not to do:

## 1.1 Platform Adaptation Statement
| Project | Description |
|---|---|
| Target platform and version | |
| Installation/Release Method | |
| Available Tools and Permissions Model | |
| Platform-specific restrictions | |
| Delivery boundaries when the platform is unknown | Only design packages are output, and installable files are not promised |

## 2. Task closed loop
| Link | Definition |
|---|---|
| Trigger conditions | |
| Required input | |
| Work steps | |
| Callable tools/data | |
| expected output | |
| Exceptions and rollbacks | |

## 3. Guardrail and manual collaboration
- Permissions and data boundaries:
- Actions that must be manually confirmed:
- Handling of uncertainty or failure:
- Disable output/disable execution:

## 4. Evaluation case
| Case | Input | Expected behavior/output | Unacceptable results | Corresponding POC standards |
|---|---|---|---|---|
| normal scenarios | | | | |
| boundary scenario | | | | |
| Failure Scenario | | | | |

### Evaluation indicators and versions
| Metrics | Scoring Methodology | Pass Thresholds | Hard Failure Conditions | Owner |
|---|---|---|---|---|
| | | | | |

- Skill version:
- Model/config version:
- Tool/interface version:
- Evaluation set version:

## 5. Deliverables and pending items
- Skill files and dependencies:
- Installation/calling method:
- Contents that require customer confirmation:
- Evidence submitted to the POC for operational verification:

## 6. Runnable POC (on demand)
- Build modes: Design package / Minimal skeleton / Controlled integration
- POC directory with `poc-manifest.json`:
- Mock, real data and external action boundaries:
- Startup and smoke test commands:
- Normal, blocking and failed scenario results:
- Unrealized capability and production gaps:
- Key verification questions for Stage 6:
```
