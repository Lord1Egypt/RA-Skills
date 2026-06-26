## Description: <br>
Use when integrating with the energy-app-middle BFF service, including REST API endpoints, gRPC client setup, authentication headers, multi-tenancy, and downstream service dependencies for the changyuanfeilun energy platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effort02](https://clawhub.ai/user/effort02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate agents and services with the energy-app-middle BFF service across Owner, Provider, Platform, and internal gRPC interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may use incorrect tenant or user headers, causing authorization failures or cross-tenant data access mistakes. <br>
Mitigation: Verify X-ACCESS-TOKEN, X-App, X-Tenant, X-UID, and X-PUID for each request and use least-privilege tokens. <br>
Risk: POST or configuration-changing API calls may alter automation, pricing, market, or device settings. <br>
Mitigation: Require explicit confirmation before POST requests or configuration changes and validate the target resource, tenant, and time range. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/effort02/energy-app-middle-integration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown guidance with API endpoint tables and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only integration guidance; no executable installer or hidden behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
