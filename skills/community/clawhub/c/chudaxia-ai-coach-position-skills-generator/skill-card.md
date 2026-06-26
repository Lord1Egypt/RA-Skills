## Description: <br>
Generates Agent Skill packages from position-agent prompts by extracting role capabilities, internalizing user-provided knowledge, creating skill directories, and syncing the prompt skill list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charleschor](https://clawhub.ai/user/charleschor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt engineers use this skill after generating a position-agent prompt to turn each role capability into a separate, mountable Agent Skill package with internalized knowledge, source mapping, and prompt updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills can contain incomplete or unverified role knowledge when the provided IMA or local source material is narrow or missing. <br>
Mitigation: Review the generated knowledge documents, source maps, and knowledge-gaps files before mounting or relying on the generated skills. <br>
Risk: The skill may create or update multiple files while generating skill packages and syncing the original position-agent prompt. <br>
Mitigation: Use a narrow output directory and inspect generated file changes before deploying the resulting skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charleschor/chudaxia-ai-coach-position-skills-generator) <br>
- [Skill extraction framework](artifact/references/skill-extraction-framework.md) <br>
- [Skill package checklist](artifact/references/skill-package-checklist.md) <br>
- [Position skill template](artifact/assets/templates/position-skill-template.md) <br>
- [Agent Skills specification](artifact/assets/specs/agents-skills-specification.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown files and directory structures for generated Agent Skill packages, plus mapping tables and updated prompt content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill-package files under a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
