# POC Evaluation and Decision Rules

## Four layers of indicators

| Hierarchy | Examples | What not to replace |
|---|---|---|
| Model/Component | Relevance, fidelity, recall, format, toxicity | End-to-end task completion |
| System | Success rate, latency, tool errors, cost, recoverability | User willingness to adopt |
| User tasks | Completion rate, time, human intervention, trust, rework | Business results |
| Business | Cost, quality, risk, revenue, turnaround time | Long-term causality and value at scale |

## Evaluation set design

- Extract and desensitize real work samples;
- Covers high-frequency, high-impact, boundary and failure scenarios;
- Save source, license, difficulty, user/scenario label and gold-labeled owner for each case;
- After the model or agent fails to be repaired, add the case to the regression set;
- Prevent assessment examples from leaking completely to prompt words, skill examples, or retrieval libraries.

## Scoring method

Priority use can determine whether the task is completed, whether the fields are correct, and whether the tool status changes. Open output uses clear scales and expert examples; model scoring needs to be calibrated with human samples and the scorer version recorded.

When the score difference exceeds the agreed threshold, it will be reviewed by experts in the field and no arbitrary average will be taken.

## Decision matrix

| Results | Suggestions |
|---|---|
| Business, User, Technology and Risk gated | Access to Adoption & Value or Pre-Production Assessment |
| The core value has a signal, and the technology/experience can be repaired | Open a new version round after adjustment |
| The technology is passed but the user/business is not established | Enter adoption analysis or stop and do not continue to stack functions |
| Value may hold but data/evaluation is invalid | Redo run design without declaring success |
| Security/Compliance Hard Access Failure | Stop and Upgrade |
| Unacceptable cost, latency or reliability | Adjust architecture/model or stop |

Conclusions also report sample number, coverage, confidence limits, and unvalidated scenarios.
