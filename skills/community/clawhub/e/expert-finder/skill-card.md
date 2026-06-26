## Description: <br>
Find domain experts, thought leaders, and subject-matter authorities on any topic by searching Twitter and Reddit for people who demonstrate deep knowledge, frequent discussion, and above-average expertise in a specific field. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, recruiters, and analysts use this skill to identify subject-matter experts, thought leaders, practitioners, educators, and key opinion leaders from public social-media activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the Xpoz service and the mcporter npm package to search and export social-media data. <br>
Mitigation: Install it only after trusting Xpoz and the mcporter package, and review the OAuth setup before use. <br>
Risk: Search topics, exported CSVs, rankings, and profile analysis can be personal-data-adjacent. <br>
Mitigation: Avoid confidential or sensitive search topics, collect only necessary data, store exports carefully, delete them when finished, and follow platform terms and applicable privacy rules. <br>


## Reference(s): <br>
- [Expert Finder on ClawHub](https://clawhub.ai/atyachin/expert-finder) <br>
- [Xpoz](https://xpoz.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked expert profiles, scores, rationale, social-media metrics, quotes, and CSV-derived analysis.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
