## Description: <br>
Identify coins from photos using evidence-based visual checks, ranked candidates, mint-mark reasoning, and a reusable local catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and collecting-focused agents use this skill to identify coins from user-supplied photos, return ranked candidates, and separate likely identification from grading, pricing, authenticity, or metal-purity claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save coin identification notes and preferences locally if the user enables memory. <br>
Mitigation: Ask for user approval before writing files and keep saved data under ~/coin-identifier/. <br>
Risk: Photo-based coin identification can be mistaken for grading, authentication, metal-purity, or market-value advice. <br>
Mitigation: State confidence and missing evidence, and keep grading, authenticity, composition, and value claims provisional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/coin-identifier) <br>
- [Skill homepage](https://clawic.com/skills/coin-identifier) <br>
- [Coin Evidence Guide](artifact/evidence-guide.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown with ranked candidates, confidence bands, missing evidence, and optional local note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local identification notes under ~/coin-identifier/ only after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
