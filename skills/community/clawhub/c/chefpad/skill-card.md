## Description: <br>
Chefpad manages local recipes and grocery lists with ingredient tracking, meal planning, search, ratings, and shopping-list workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use Chefpad to maintain a local recipe collection from the command line, add ingredients and steps, search by keyword or ingredient, rate recipes, and choose meal suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted recipe text, ingredients, or search terms could execute local code because the script interpolates user input into embedded Python. <br>
Mitigation: Review this version before installing and only pass trusted local recipe data until input handling uses argv, environment variables, or JSON-safe serialization. <br>
Risk: Recipe data is stored locally under ~/.chefpad and may include personal ingredients, meal preferences, or recipe notes. <br>
Mitigation: Treat ~/.chefpad/recipes.json as local user data and avoid sharing it unless intentionally exported. <br>


## Reference(s): <br>
- [Chefpad on ClawHub](https://clawhub.ai/bytesagain-lab/chefpad) <br>
- [bytesagain-lab Publisher Profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with command examples and local JSON recipe data managed by the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.chefpad and does not require external APIs or API keys.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
