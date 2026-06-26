## Description: <br>
Avengers-themed multi-agent coordination system where Nick Fury orchestrates six specialized hero agents through sessions_spawn delegation, round-robin dispatch, reply-first protocol, and sessionKey reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenXinBest](https://clawhub.ai/user/ChenXinBest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate complex or multi-part work by delegating missions across specialized spawned agent sessions and synthesizing their reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated spawned-agent sessions may retain prior mission context through reused session keys. <br>
Mitigation: For sensitive work, request fresh sessions or single-session handling and avoid including secrets in delegated tasks. <br>
Risk: Multi-agent delegation can spread user-provided context across several spawned sessions. <br>
Mitigation: Limit mission briefings to the minimum necessary context and review synthesized reports before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChenXinBest/avengers-assemble) <br>
- [Marvel Avengers homepage](https://marvel.com/avengers) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Markdown text with sessions_spawn call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fixed hero session keys and a 300 second spawned-session timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
