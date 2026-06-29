## Description: <br>
Queries, filters, installs, and updates ClawHub/CMS skills from the aishuo.co skill service into the current agent workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spzwin](https://clawhub.ai/user/spzwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to discover available ClawHub/CMS skills, inspect skill details, and request installation or update of selected skills by skill code. It is intended for registry search and workspace-local skill management, not for publishing or administering skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry calls may transmit AppKey, userId, skill searches, and install or update requests to the aishuo.co/CMS service. <br>
Mitigation: Use only in environments where the publisher and service are trusted to handle those identifiers and requests. <br>
Risk: Security evidence states that TLS verification is disabled for registry calls. <br>
Mitigation: Avoid restricted or sensitive environments until TLS verification is enabled and certificate warnings are no longer suppressed. <br>
Risk: The skill can request installation or overwrite updates for workspace skills. <br>
Mitigation: Require explicit user confirmation before install, update, or force-overwrite actions and review the installed skill before loading it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spzwin/skills/cms-find-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/spzwin) <br>
- [aishuo.co Skill Service](https://aishuo.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text tables, JSON responses, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill lists, skill details, download URLs, install/update results, and follow-up reload guidance.] <br>

## Skill Version(s): <br>
1.7.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
