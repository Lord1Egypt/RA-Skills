# Delivery Use-Case Decision Table

| Situation | Template | Why |
|---|---|---|
| First meeting after approval | `kickoff-agenda` | Aligns owners, scope, cadence, and next steps. |
| Need systems/docs/API access | `client-access-checklist` | Captures access needs and owners. |
| Need execution plan | `project-plan` | Structures work into phases and milestones. |
| Track milestone progress | `milestone-tracker` | Shows status, dates, and blockers. |
| Regular client update | `weekly-status-update` | Communicates progress and decisions needed. |
| Decision made | `decision-log` | Records decision, owner, date, and rationale. |
| Risk or issue arises | `risk-and-issue-log` | Tracks impact, owner, mitigation, and status. |
| New scope request | `change-request-intake` | Keeps scope changes controlled. |
| Blocker or prerequisite | `dependency-tracker` | Tracks dependencies and owners. |
| Communication cadence unclear | `stakeholder-communication-plan` | Defines who gets what updates. |
| Prototype ready | `prototype-review-checklist` | Guides structured prototype feedback. |
| Evaluation run complete | `evaluation-run-report` | Captures examples, results, and failures. |
| Test summary needed | `test-results-summary` | Summarizes test status for stakeholders. |
| Formal acceptance | `acceptance-review-packet` | Packages acceptance evidence. |
| Launch planning | `launch-readiness-checklist` | Checks readiness before launch. |
| Monitoring needed | `monitoring-plan` | Defines logs, metrics, owners, and review rhythm. |
| Support terms needed | `support-plan` | Defines support window and scope. |
| Handoff preparation | `handoff-checklist` | Ensures docs, owners, and training are complete. |
| Admin/operator docs | `administrator-runbook` | Gives operating instructions. |
| User/reviewer enablement | `user-reviewer-quickstart` | Gives concise reviewer guidance. |
| After launch | `post-launch-review` | Reviews outcomes, issues, and next steps. |
| Retrospective | `lessons-learned` | Captures what to repeat or change. |
| Project close | `closeout-summary` | Summarizes final status and artifacts. |
| Support request | `support-ticket-intake` | Captures issue details for triage. |
| Escalation path | `escalation-procedure` | Defines severity, contacts, and response path. |
| Deployment execution | `deployment-runbook` | Lists rollout steps and rollback notes. |
| Acceptance defects | `defect-remediation-plan` | Tracks fixes before acceptance. |
| Training session | `training-session-plan` | Plans reviewer/admin enablement. |

Selection rule: choose the artifact matching the current operational event. If the event changes scope, use change request intake before changing project plans or invoices. If acceptance, launch, or closeout is requested, require evidence first.
