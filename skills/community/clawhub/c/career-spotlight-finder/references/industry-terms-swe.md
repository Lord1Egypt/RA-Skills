# Industry Terms: Software Engineering

> **Usage note:** This file is for software engineering in the product/backend/frontend/full-stack sense. Use this file to catch colloquial or informal descriptions and map them to the recognized industry terms that belong on a resume or portfolio. If the user's work is more about distributed systems, storage systems, runtimes, or computer systems as a field, use the systems file instead.

---

## Architecture & Design

| User's description | Industry term |
|---|---|
| "split app into services" | Microservices Architecture |
| "used message queues" | Event-driven Architecture / Message Broker |
| "made code pluggable" | Plugin Architecture / Extension Points |
| "separated UI from logic" | MVC / MVVM / Presentation Layer Separation |
| "designed API contracts" | API-first Design / Contract-first Development |
| "cached frequently used data" | Caching Strategy (Redis, CDN, Memoization) |
| "handled requests without storing state" | Stateless Service Design |
| "set up a shared data format across teams" | Schema Registry / Canonical Data Model |
| "made system work even when parts fail" | Fault-tolerant / Resilient Architecture |
| "let features toggle on and off" | Feature Flags / Feature Toggle System |

## DevOps & Infrastructure

| User's description | Industry term |
|---|---|
| "set up auto-deploy" | CI/CD Pipeline |
| "used containers" | Containerization (Docker, OCI) |
| "managed cloud resources" | Infrastructure as Code (IaC) (Terraform, Pulumi) |
| "set up monitoring/alerts" | Observability Stack (Logging, Metrics, Tracing) |
| "handled traffic spikes" | Auto-scaling / Horizontal Scaling |
| "managed secrets" | Secrets Management (Vault, AWS Secrets Manager) |
| "made deploys easy to undo" | Rollback Strategy / Blue-Green Deployment |
| "set up dev environments automatically" | Dev Environment Provisioning / Devcontainers |
| "managed DNS and routing" | Service Mesh / Ingress Configuration |
| "wrote scripts to automate repetitive ops tasks" | Operational Automation / Runbook Automation |

## Quality & Testing

| User's description | Industry term |
|---|---|
| "wrote tests first" | Test-driven Development (TDD) |
| "tested components together" | Integration Testing |
| "load tested the system" | Performance / Load Testing (k6, Locust, JMeter) |
| "caught bugs before merge" | Pre-commit Hooks / Static Analysis / Linting |
| "tested edge cases" | Boundary / Edge Case Testing |
| "tracked test coverage" | Code Coverage Analysis |
| "tested the whole user flow" | End-to-End (E2E) Testing |
| "faked external services in tests" | Mocking / Service Virtualization |
| "tested what happens when things break" | Chaos Engineering / Fault Injection |
| "made sure old features still work" | Regression Testing |

## Collaboration & Process

| User's description | Industry term |
|---|---|
| "reviewed others' code" | Code Review / Engineering Mentorship |
| "wrote docs for the team" | Technical Documentation / Internal Knowledge Base |
| "onboarded new engineers" | Developer Onboarding / Ramp-up Program |
| "estimated work" | Story Point Estimation / Sprint Planning |
| "led standups" | Agile Facilitation / Scrum Ceremonies |
| "defined coding standards" | Engineering Standards / Style Guides |
| "helped debug others' issues" | Technical Troubleshooting / Cross-team Support |
| "broke down big projects into tasks" | Technical Decomposition / Work Breakdown Structure |
| "wrote RFCs or design docs" | Technical Design Document / RFC Process |
| "led a post-mortem after an outage" | Incident Post-mortem / Blameless Retrospective |

## Reliability & Platform Engineering

| User's description | Industry term |
|---|---|
| "defined uptime or latency goals" | SLI / SLO / SLA Management |
| "balanced shipping speed with stability" | Error Budget Policy / Reliability Engineering |
| "built an internal paved road for teams" | Internal Developer Platform (IDP) / Golden Path |
| "tracked delivery speed and deploy stability" | DORA Metrics |
| "kept one noisy service from hurting everyone else" | Multi-tenant Isolation / Resource Quotas |
| "moved logic closer to users" | Edge Computing / Edge Runtime |
| "changed database schema without downtime" | Zero-downtime Migration / Online Schema Change |
| "moved slow work off the request path" | Asynchronous Processing / Queue Offloading |
| "limited failures to a smaller blast radius" | Bulkhead Pattern / Blast-radius Reduction |
| "planned recovery before incidents happened" | Disaster Recovery / Resilience Planning |
