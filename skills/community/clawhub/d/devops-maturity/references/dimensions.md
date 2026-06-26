# Assessment Dimensions — Questions & Scoring

## 1. CI/CD & Deployment

**Questions:**
- How often do you deploy to production? (on-demand / daily / weekly / monthly / quarterly+)
- What is your lead time from commit to production? (<1h / <1 day / <1 week / <1 month / >1 month)
- What percentage of your build/test/deploy pipeline is automated? (0-100%)
- Do you practice trunk-based development or long-lived branches?

**Scoring:**
- 0: No pipeline, manual deployments
- 1: Some CI exists but deployments are manual
- 2: CI/CD for some projects, inconsistent
- 3: Standard CI/CD pipeline across teams, automated testing
- 4: Deploy multiple times/week, measured lead times, feature flags
- 5: Deploy on-demand, lead time <1 day, canary/blue-green deployments
- 6: Deploy continuously, lead time <1 hour, progressive delivery, auto-rollback

## 2. Infrastructure as Code (IaC)

**Questions:**
- What percentage of infrastructure is defined as code? (0-100%)
- Do you version-control your IaC? Do you do code review for infra changes?
- Do you test IaC before applying? (linting, plan/preview, integration tests)
- Do you detect and remediate configuration drift?

**Scoring:**
- 0: All infrastructure managed manually (clickops)
- 1: Some scripts exist but not systematic
- 2: Key resources in IaC, but many exceptions
- 3: Most infra in IaC, version-controlled, reviewed
- 4: IaC tested (lint + plan), drift detection in place
- 5: Full IaC coverage, automated testing pipeline, self-service modules
- 6: Policy-as-code, auto-remediation of drift, immutable infrastructure

## 3. Observability

**Questions:**
- Do you collect metrics, logs, and traces? Which of the three pillars?
- Do you have defined SLOs/SLIs for your services?
- How quickly can you diagnose root cause of an incident? (<1h / hours / days)
- Do you use alerting? Is it actionable or noisy?

**Scoring:**
- 0: No monitoring
- 1: Basic server metrics (CPU/RAM), no centralized logging
- 2: Centralized logs + basic metrics, reactive alerting
- 3: Metrics + logs + some tracing, defined dashboards
- 4: All 3 pillars, SLOs defined, actionable alerts, error budgets
- 5: Distributed tracing across services, anomaly detection, AIOps elements
- 6: Full observability platform, predictive alerting, automated correlation

## 4. Security (DevSecOps)

**Questions:**
- At what stage do you perform security checks? (production only / pre-deploy / during CI / during development)
- Do you scan dependencies for vulnerabilities automatically?
- How do you manage secrets? (env vars / vault / hardcoded / ?)
- Do you have automated compliance checks?

**Scoring:**
- 0: Security is an afterthought, no scanning
- 1: Periodic manual security reviews
- 2: Some automated scanning, secrets in env vars
- 3: SAST/DAST in CI pipeline, secrets in vault, security training
- 4: Shift-left security, dependency scanning, compliance-as-code
- 5: Security gates in every pipeline, threat modeling, bug bounty
- 6: Zero-trust architecture, automated remediation, continuous compliance

## 5. Culture & Organization

**Questions:**
- How do Dev and Ops teams collaborate? (separate silos / some collaboration / integrated)
- Do you conduct blameless postmortems after incidents?
- How is knowledge shared? (tribal / wiki / structured documentation / automated)
- Can developers self-service infrastructure and deployments?

**Scoring:**
- 0: Complete silos, blame culture
- 1: Occasional joint meetings, finger-pointing after incidents
- 2: Shared tools but separate responsibilities
- 3: Cross-functional teams, blameless postmortems, documented runbooks
- 4: Platform teams serving dev teams, self-service portals, learning culture
- 5: Full ownership (you build it, you run it), communities of practice
- 6: Continuous learning embedded, experimentation encouraged, innovation time

## 6. FinOps

**Questions:**
- Do you have visibility into cloud costs per team/service/environment?
- Do you actively optimize cloud spend? (reserved instances, rightsizing, spot)
- Who is responsible for cloud costs? (finance only / engineering+finance / everyone)
- Do you forecast and budget cloud costs?

**Scoring:**
- 0: No cost visibility, surprise bills
- 1: Monthly total cost reviewed, no breakdown
- 2: Cost allocation by team/project exists but not acted upon
- 3: Regular cost reviews, tagging standards, basic optimization
- 4: FinOps practice in place, cost in CI/CD, anomaly alerts
- 5: Real-time cost dashboards, automated rightsizing, committed use discounts
- 6: Cost-per-transaction metrics, engineering KPIs include cost, predictive modeling

## 7. Reliability (SRE)

**Questions:**
- What is your mean time to recovery (MTTR) after an incident? (<1h / hours / days)
- What is your change failure rate? (% of deployments causing incidents)
- Do you have automated rollback or auto-remediation?
- Do you practice chaos engineering or resilience testing?

**Scoring:**
- 0: No incident process, days to recover
- 1: Ad-hoc incident response, MTTR in days
- 2: Incident process exists, MTTR in hours, manual rollback
- 3: Defined runbooks, MTTR <4h, automated rollback capability
- 4: SRE practices, MTTR <1h, error budgets, on-call rotation
- 5: Auto-remediation for common issues, chaos engineering, <5% failure rate
- 6: Self-healing systems, proactive resilience, near-zero unplanned downtime

## DORA Benchmarks (for context)

Source: DORA State of DevOps reports

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deploy frequency | On-demand (multiple/day) | Weekly-monthly | Monthly-6 months | <6 months |
| Lead time | <1 hour | 1 day-1 week | 1-6 months | >6 months |
| MTTR | <1 hour | <1 day | 1 day-1 week | >6 months |
| Change failure rate | 0-15% | 16-30% | 16-30% | >30% |
