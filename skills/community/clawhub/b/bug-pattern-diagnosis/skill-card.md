## Description: <br>
Matches reported bug symptoms against a bundled case library to suggest likely debugging directions, verification checks, and follow-up diagnostics without treating prior cases as automatic answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to structure reports of intermittent, environment-specific, or confusing bugs, compare symptoms with prior case notes, and choose concrete checks before changing code or infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest kubectl, curl, tcpdump, EMQX, or cluster repair commands during debugging. <br>
Mitigation: Run operational commands only with proper authorization, scoped environments, and change-control awareness. <br>
Risk: New BUGxx.md case notes may capture sensitive logs, infrastructure details, or customer-specific incident information. <br>
Mitigation: Review and sanitize new case notes before sharing, publishing, or committing them. <br>
Risk: Prior bug cases can resemble a new issue without sharing the same root cause. <br>
Mitigation: Use the case library as hypothesis support and require independent verification before applying code or infrastructure changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/bug-pattern-diagnosis) <br>
- [SKILL.md](SKILL.md) <br>
- [BUG01: multi-replica intermittent NPE](experience/BUG01.md) <br>
- [BUG02: intermittent Netty eventLoop termination](experience/BUG02.md) <br>
- [BUG03: EMQX cluster route-table desynchronization](experience/BUG03.md) <br>
- [BUG04: MQTT ClientID takeover disconnects](experience/BUG04.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured diagnostic notes, checklists, and inline code or shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose creating or updating BUGxx.md case notes after user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
