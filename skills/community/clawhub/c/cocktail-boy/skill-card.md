## Description: <br>
Your private bartender for cocktail recommendations, recipe lookup, and mixing guidance, with search by drink name, ingredients, random recommendations, and scenario-based suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flarecentury](https://clawhub.ai/user/flarecentury) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up cocktail recipes, search drinks by ingredient, and receive random or scenario-based cocktail suggestions from a bundled CSV recipe database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary notes a packaging mismatch: the manifest points to a missing script name, so configured commands may not run as published. <br>
Mitigation: Confirm the entrypoint before relying on the skill, and update the manifest to point to an existing script such as scripts/query.sh or scripts/main.sh if needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flarecentury/cocktail-boy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with CLI command patterns and recipe details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bundled CSV database of 1635+ cocktail recipes; no API key or network access is identified in the server security summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
