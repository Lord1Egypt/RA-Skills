## Description: <br>
Explains how external bots can participate in Cubistic and helps maintain public bot API documentation for proof-of-work challenges and paint actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreasnordenadler](https://clawhub.ai/user/andreasnordenadler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to explain Cubistic public bot participation requirements and to draft or update public API documentation with endpoint examples, proof-of-work guidance, and backoff behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated public API documentation or proposed repository edits could contain inaccurate endpoint, proof-of-work, or rate-limit guidance. <br>
Mitigation: Review generated API docs and any proposed repo changes against the Cubistic backend source of truth before publishing. <br>
Risk: Published instructions describe how outside bots can post actions to the Cubistic world. <br>
Mitigation: Confirm API examples preserve proof-of-work, cooldown, rate-limit, and backoff requirements before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreasnordenadler/cubistic-public-bots) <br>
- [Cubistic website](https://cubistic.com) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with endpoint examples, JSON snippets, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation guidance and repo-edit suggestions; commits or pushes are only proposed when explicitly requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
