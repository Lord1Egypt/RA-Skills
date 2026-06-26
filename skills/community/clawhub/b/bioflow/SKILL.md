---
name: bioflow-api-quickstart
description: Quick guide for BioFlow backend API usage and integration. Use when an agent needs concise project intro plus end-to-end API flow: signup/login, file upload/download, token balance query, task submission, and result retrieval.
---

# BioFlow API Quickstart

Provide a concise implementation/use checklist for BioFlow APIs with minimal context loading.

## Workflow
1. Read [references/current-auth-map.md](references/current-auth-map.md) for project scope and auth/token model.
2. Read [references/api-call-flow.md](references/api-call-flow.md) for concise API call sequence (signup/login -> upload -> balance -> create task -> poll -> results -> download).
3. Use one algorithm path for demo execution (default PTMPred) instead of mixing multiple algorithms in one run.
4. Keep responses concise: show endpoint, required params, minimal request example, and key response fields only.

## Output Structure
1. Project intro: base URL, auth mode, major API groups.
2. Registration/login: send SMS verification code, signup (telephone + verification_code), login, refresh, me.
3. File workflow: upload dataset and get dataset download URL.
4. Balance query: `GET /api/v1/token/balance`.
5. Task submission: one concrete algorithm endpoint and required parameters.
6. Result query: job detail, results list, and result download endpoint.

## Done Criteria
1. Agent can explain complete API path from account creation to result retrieval in one compact response.
2. Endpoint examples are executable with current Bearer token flow.
3. File upload/download and task/result endpoints are both covered.

## References
1. [references/current-auth-map.md](references/current-auth-map.md)
2. [references/api-call-flow.md](references/api-call-flow.md)
