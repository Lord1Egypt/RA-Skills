## Description: <br>
Queries 1688 product ranking lists and category-level hot search keywords using the official 1688 Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve 1688 category rankings, hot-selling or value rankings, hot keywords, and top-level category data for sourcing and marketplace research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable 1688 access and refresh tokens may be stored in a shared local cache without explicit permission hardening. <br>
Mitigation: Use a least-privileged 1688 app or token, avoid shared or untrusted machines, protect or periodically delete ~/.openclaw/workspace/skills/.1688_token_cache.json, and avoid running scripts/auth.py directly unless token output is removed or masked. <br>


## Reference(s): <br>
- [1688 API Reference](references/api.md) <br>
- [1688 Open Platform API Invocation Guide](https://open.1688.com/doc/apiInvoke.htm) <br>
- [1688 Open Platform Signature Rules](https://open.1688.com/doc/signature.htm) <br>
- [1688 Open Platform Authorization Guide](https://open.1688.com/doc/apiAuth.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and command-line error JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 1688 app credentials and either a refresh token or access token; product ranking commands clamp requested result count to 1-20.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
