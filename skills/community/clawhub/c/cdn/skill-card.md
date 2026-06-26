## Description: <br>
Configure, optimize, and troubleshoot CDN deployments with caching strategies, security hardening, and multi-provider management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to select CDN providers, configure caching, harden CDN security, plan invalidation, monitor performance, and troubleshoot CDN behavior across common production web delivery scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CDN command examples and configuration guidance can affect live services if applied to the wrong zone, distribution, pull zone, path, or environment. <br>
Mitigation: Confirm the exact target resource and environment before running commands, prefer targeted purges over full cache purges, and test changes in a non-production environment when feasible. <br>
Risk: API tokens used for CDN automation can grant broad control over production delivery settings. <br>
Mitigation: Use least-privilege provider tokens, keep credentials out of shared prompts and logs, and rotate tokens according to the provider's operational policy. <br>
Risk: Firewall, WAF, and rate-limit guidance can block legitimate traffic if thresholds or allowlists are misconfigured. <br>
Mitigation: Roll out security rules in log or challenge mode where supported, validate expected user and bot traffic, and monitor edge and origin errors after enforcement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/cdn) <br>
- [CDN provider comparison and CLI examples](artifact/providers.md) <br>
- [CDN caching strategies](artifact/caching.md) <br>
- [CDN security hardening](artifact/security.md) <br>
- [CDN troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
