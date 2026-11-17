# Deployment architecture input guide

## Enter inventory

| Domain | Required Information | Owner | Risk of Missing |
|---|---|---|---|
| Users and entrances | Who triggers, where to enter, whether login/approval is required | Business/product | Unable to design identity and experience |
| Customer system | System name, environment,API/UI, rate, maintenance window | Customer technology | Integration is not feasible or unstable |
| Data | Source, sample, format, quality, freshness, sensitivity level | Data owner | Result distortion or violation |
| Identity permissions | Users, service accounts, authorization scope, key management | Security/Platform | Override of authority and credential leakage |
| Model/Agent | Model, context, tool, memory, output usage |AI/FDE| Unable to assess costs and risks |
| Non-functional requirements | Latency, concurrency, availability, geography, cost ceiling | Business/architecture | POC conclusions cannot be extrapolated |
| Observation | Logs, indicators, tracking, feedback and audit requirements | Operations/security | Failure cannot be located and reproduced |
| Operational governance | Release, rollback, support, incident escalation and data deletion | Operation and maintenance/business | Unable to safely test run |

## System Boundary Interview Questions

1. Which step must use a real system to prove value?
2. Which data cannot leave the customer environment, and which can be de-identified or synthesized?
3. What can the agent read, suggest, and execute? Which actions must be manually confirmed?
4. Is it possible that external documents, web pages, emails, or tool output contain malicious instructions?
5. Should it stop, retry, downgrade, switch to manual or rollback when it fails?
6. What logs, indicators, and evidence should be used to reproduce the POC results?

## Information credibility

Mark "the interface should have" and "the permission should be able to be opened" as assumptions. Only interface documentation/sample calls, customer lead confirmation, environment verification, or real testing count as available evidence.
