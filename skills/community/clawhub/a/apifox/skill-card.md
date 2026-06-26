## Description: <br>
Summarizes and organizes public YApi product and open-source documentation, including feature notes, documentation links, and repository examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and documentation maintainers use this skill to collect concise summaries and link sets from public YApi product, deployment, and open-source pages without account or project changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry display name is Apifox, while the artifact content describes a YApi documentation helper. <br>
Mitigation: Confirm the release label before publishing or make the YApi scope explicit in downstream review materials. <br>
Risk: Users may provide private project URLs, credentials, or sensitive internal API details to a skill intended for public documentation. <br>
Mitigation: Use only public product, documentation, or open-source URLs and redact secrets or internal endpoint details before prompting the agent. <br>
Risk: Summaries of dynamically loaded pages may omit or misread content if the page is not fully loaded. <br>
Mitigation: Wait for page load completion and verify generated summaries against the source page before using them. <br>


## Reference(s): <br>
- [ClawHub Apifox Skill Page](https://clawhub.ai/CodeKungfu/apifox) <br>
- [YApi Homepage](https://yapi.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and link lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials, private URLs, or sensitive internal API details should be included.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
