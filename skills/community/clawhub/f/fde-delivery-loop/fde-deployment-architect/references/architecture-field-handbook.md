# POC Architecture Field Manual

## Architecture review order

Business risks first, then data and identity, then tools and models, and finally infrastructure. Don’t start with a cloud product checklist.

## Component review

Ask each component: what is its responsibility, which standard it supports, input and output, failure mode, version, owner, and whether it can be replaced.

## Data life cycle

Covers collection, transmission, storage, processing, logging, sharing, archiving and deletion. Verify territory, encryption, permissions, sensitive fields and auditing at every step.

## Identity model

- Separation of user identity and service identity;
- Customer tenant isolation;
- The identity of the manual confirmer can be traced;
- No personal long-term keys are used;
- Credential expiration and revocation are operational;
- Permissions are not reused between environments.

## Tool classification

- Read-only queries: still require tenant, fields and rate limits;
- Draft writing: marked as inactive;
- External actions: manual confirmation and idempotent keys;
- Irreversible actions: POC is disabled by default;
- Management tools: isolated from business agents.

## Model and context

Document model version, region, data retention, context length, cost, and rate. Sensitive content is minimized before entering the model; external content is not trusted.

## RAG check

- Document authorization and source;
- Chunking and metadata;
- Validity/invalidation and freshness;
- Tenant and permission filtering;
- Recalls are consistent with citations;
- No result, conflict and expiration processing;
- Index versions and rollbacks.

## Write operation check

Display objects, fields, before and after values, external effects and revocability; require confirmation of the corresponding role; verify the final state after execution; retries must be idempotent.

## Failure Mode

- Model timeout: retry limit, downgrade or transfer to manual;
- Tools are partially successful: don’t pretend the whole is successful;
- Missing data: stops key conclusions;
- Retrieve conflicts: display conflicts and escalate;
- Configuration drift: Verify version before deployment;
- Cost anomalies: limits and circuit breakers;
- Security Incident: Stop immediately and preserve evidence.

## Environment

Development, POC, pre-production, production isolation. Clarify data, accounts, configuration and release paths. POC close to production does not equal production approval.

## Observe the third floor

- Systems: delays, errors, resources and costs;
- Agents: trajectories, tools, retrieval, models and human intervention;
- Business: mission completion, quality, adoption and risk outcomes.

## Cost model

Includes model, retrieval, storage, network, tools, logs, human review, support and error costs. Record unit task costs rather than just looking at monthly totals.

## Architecture diagram requirements

At least one system boundary diagram and one data/trust flow diagram. Only add timing or state diagrams for complex states to avoid drawing cloud icons for display.

## Production issues

- Who is on duty and who is supporting;
- What isSLA/SLO;
- How to release, rollback and audit;
- How to evaluate model/cue word changes;
- How to handle data drift and policy updates;
- How to do capacity, disaster recovery and incident response;
- Who accepts residual risk and long-term costs.

## Architecture handover

Design for skills: tools, permissions, data, artificial nodes and error semantics.

Run the POC: environment, versions, logs, datasets, costs, and stopping mechanisms.
