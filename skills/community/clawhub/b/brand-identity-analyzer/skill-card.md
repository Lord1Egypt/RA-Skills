## Description: <br>
Analyzes brands with Gemini and Google Search grounding to generate structured brand identity JSON profiles for ad generation and creative workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative workflow operators use this skill to research a brand and produce reusable JSON profiles capturing official identity, visual style, tone, campaign guidance, and compliance constraints for downstream ad and design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated brand profiles may be saved into another project and pushed to GitHub without an explicit review gate. <br>
Mitigation: Review the generated JSON, confirm the destination repository and branch, and require manual approval before any commit or push. <br>
Risk: Brand names and prompts are sent to Gemini with Google Search grounding. <br>
Mitigation: Use only when sharing the requested brand research with Gemini and Google Search is acceptable for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/brand-identity-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON brand profile, with optional saved files and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key; can print JSON to stdout or save profiles to a specified path or Ad-Ready catalog.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
