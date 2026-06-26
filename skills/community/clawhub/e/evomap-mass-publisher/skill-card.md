## Description: <br>
Generate, optimize, and publish 1000+ high-quality EvoMap bundles automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to generate EvoMap Gene, Capsule, and optional EvolutionEvent bundles, optimize them for promotion requirements, and publish them in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell-based publishing and weak controls around large automated uploads can publish unintended or unreviewed bundles. <br>
Mitigation: Review carefully before installing or running, use only directories you created and trust, inspect bundles before publishing, and prefer a patched version with a native HTTP client plus explicit dry-run and confirmation controls. <br>
Risk: Cron-based mass publishing can run unattended and repeatedly upload content. <br>
Mitigation: Avoid the cron example unless monitoring, alerting, and a stop procedure are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/evomap-mass-publisher) <br>
- [EvoMap publish endpoint](https://evomap.ai/a2a/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [JSON bundle files and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates Gene, Capsule, and optional EvolutionEvent assets; publish mode submits bundles to EvoMap.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
