## Description: <br>
ForkZoo lets agents adopt and manage GitHub-native digital pets that evolve daily with AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levi-law](https://clawhub.ai/user/levi-law) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use ForkZoo to adopt digital pets into their GitHub accounts, check pet status and evolution, trigger interactions, and browse community gallery or lineage information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires GitHub access that can create repositories, enable workflows, and change publishing settings. <br>
Mitigation: Use a dedicated fine-grained or temporary GitHub token limited to the intended pet repository where possible, and revoke it after use. <br>
Risk: The adopted repositories can run GitHub Actions and publish GitHub Pages under the user's account. <br>
Mitigation: Inspect the forkZoo repositories and workflows before adoption, and disable Actions, disable Pages, or delete the fork when the automation is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/levi-law/forkzoo) <br>
- [ForkZoo Main Site](https://forkzoo.com) <br>
- [ForkZoo GitHub Organization](https://github.com/forkZoo) <br>
- [Original forkMonkey Project](https://github.com/roeiba/forkMonkey) <br>
- [ForkZoo Community Gallery](https://forkzoo.com/gallery) <br>
- [ForkZoo Leaderboard](https://forkzoo.com/leaderboard) <br>
- [ForkZoo Family Trees](https://forkzoo.com/trees) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub credentials for repository operations; scripts may create forks, enable Actions, enable Pages, and trigger workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
