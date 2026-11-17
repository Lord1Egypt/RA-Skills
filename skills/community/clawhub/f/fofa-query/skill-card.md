## Description:

Queries FOFA for internet-exposed assets across IPs, domains, ports, protocols, certificates, geography, and time ranges for authorized asset discovery and security research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, asset owners, and authorized researchers use this skill to construct FOFA queries, run the bundled Python helper, and interpret returned asset data. It supports asset discovery, exposure review, certificate analysis, and vulnerability-oriented asset location when the user is authorized to assess the targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad FOFA queries can enable internet reconnaissance outside an authorized scope.

Mitigation: Use narrowly scoped queries tied to assets you own or are explicitly allowed to assess, and avoid generic high-volume searches.

Risk: FOFA credentials may be exposed if passed directly on the command line or stored insecurely.

Mitigation: Provide FOFA_API_KEY from a protected environment or secret manager and avoid the --api-key option for shared terminals, scripts, and logs.

Risk: Returned asset data can be misused or overinterpreted without validation.

Mitigation: Review results against the authorized assessment scope and validate findings before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moxin1044/skills/fofa-query)
- [Publisher profile](https://clawhub.ai/user/moxin1044)
- [FOFA query syntax reference](references/query_syntax.md)
- [FOFA](https://fofa.info)
- [FOFA API endpoint](https://fofa.info/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and FOFA query strings; the helper can return text, JSON, or table output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, requests==2.31.0, network access to FOFA, and FOFA_API_KEY credentials.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
