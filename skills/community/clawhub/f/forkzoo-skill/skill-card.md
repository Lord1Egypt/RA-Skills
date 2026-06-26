## Description: <br>
Adopt and manage GitHub-native digital pets that evolve daily with AI, including adoption, status checks, interactions, and community gallery browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levi-law](https://clawhub.ai/user/levi-law) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use ForkZoo to create and manage GitHub-hosted digital pets, trigger or inspect pet evolution, and browse related community pet activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adoption requires GitHub repository and workflow authority that can fork repositories, enable Actions, run workflows, and publish Pages. <br>
Mitigation: Use the narrowest practical GitHub token, review requested scopes before use, and revoke or rotate the token after adoption if ongoing access is unnecessary. <br>
Risk: Forked pet repositories may run upstream workflows through GitHub Actions. <br>
Mitigation: Review the upstream ForkZoo repositories and workflow files before enabling Actions or triggering evolution workflows. <br>


## Reference(s): <br>
- [ForkZoo Skill on ClawHub](https://clawhub.ai/levi-law/forkzoo-skill) <br>
- [ForkZoo Main Site](https://forkzoo.com) <br>
- [ForkZoo Gallery](https://forkzoo.com/gallery) <br>
- [ForkZoo GitHub Organization](https://github.com/forkZoo) <br>
- [Original forkMonkey Project](https://github.com/roeiba/forkMonkey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call GitHub APIs and requires a GitHub token for adoption, status, and interaction workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
