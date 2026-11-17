# Deployment architecture quality score

| Dimensions | 0 points | 1 point | 2 points |
|---|---|---|---|
| Business tracking | Not related to POC | Partially related | proof criterions for each component/risk mapping |
| System boundary | Only component name | Connection relationship | Complete user, system, manual, and external boundaries |
| Data flow | Not described | Source and destination | Classification, retention, deletion, region and permission integrity |
| Identity Permissions | Use a Universal Account | Have Roles | Least Privileges, Credentials, Tenant Isolation and Auditing |
| Tool security | Fully enabled by default | With manual confirmation | Minimum functions, quotas, verification, and rollback complete |
| Plan selection | Single conclusion | Candidates | Record of time, cost, risk, extrapolation reasons |
| Observability | Error logs only | Metrics available | Versions, trajectories, costs, feedback and alerts reproducible |
| Reliability | Failures not considered | Retries available | Idempotent, downgrade, manual, rollback and stop |
| Version management | "Current version" | Record section | Full stack version and configuration drift traceable |
| POC/Production Boundaries | Blurred | General Description | Technical Debt, Rewrites, and Production Gates Clear |

Only when you have a score of 16 or above and the identity permissions, data flow, and tool security are not 0 can you enter skill implementation or POC operation.

## Architecture review questioning

- If an external document contains malicious instructions, what tools can be triggered?
- If the same request is retried twice, will the data be sent or modified repeatedly?
- How to prove which version of prompt words, skills, models and data are currently running?
- After the success of Mock, what are the unknowns about real integration?
- Are the logs sufficient for reproducibility, and do they record sensitive data that should not be retained?
- Who accepts the residual risk and who is responsible for incident response?
