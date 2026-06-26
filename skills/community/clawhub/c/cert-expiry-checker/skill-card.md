## Description: <br>
SSL/TLS certificate expiry checker and domain health monitor for certificate expiration, issuer details, SAN entries, and chain validity across one or more domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security teams use this skill to check SSL/TLS certificate health for domains, monitor renewals, validate non-standard ports, and generate reports for operational review or CI gating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network lookups against user-provided domains and may inspect security-relevant certificate details. <br>
Mitigation: Run it only against domains you are authorized to assess and review results before using them for operational decisions. <br>
Risk: The skill can write JSON or HTML reports that may contain domain, certificate, issuer, and SAN details. <br>
Mitigation: Use explicit output paths in a dedicated reports directory and review generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/cert-expiry-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, HTML files, shell commands] <br>
**Output Format:** [Terminal status tables, JSON arrays, and optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read domain lists from files, connect to target domains over the network, and write JSON or HTML reports when an output path is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
