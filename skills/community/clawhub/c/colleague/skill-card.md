## Description: <br>
Distill colleagues' work styles, thinking patterns, and institutional knowledge into local profiles that support collaboration and continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to structure their own observations about colleagues into work-style profiles, meeting preparation guidance, team-dynamics analysis, and institutional memory for knowledge transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create long-lived coworker behavior profiles that may include sensitive or reputation-harming information. <br>
Mitigation: Keep entries limited to necessary work facts, avoid health, family, protected-class, speculative, or reputation-harming notes, and regularly review or delete stale profiles. <br>
Risk: Colleague documentation may require consent, organizational authorization, or policy review in some workplaces. <br>
Mitigation: Install and use only where workplace policy permits this kind of documentation, and get consent or organizational authorization where required. <br>
Risk: Local profile files may expose sensitive workplace observations if the user's machine or home directory is accessible to others. <br>
Mitigation: Treat ~/.colleague-skill as sensitive local data, restrict access to the directory, and avoid syncing it to external services. <br>


## Reference(s): <br>
- [Work Style Dimensions](references/work-style-dimensions.md) <br>
- [Colleague Profile Template](templates/COLLEAGUE-PROFILE.md) <br>
- [Interaction Log Template](templates/INTERACTION-LOG.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/colleague) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown profiles, JSONL interaction logs, and plain-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-supplied observations locally under ~/.colleague-skill/ as plain text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
