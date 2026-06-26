## Description: <br>
Commit Helper helps agents generate, validate, lint, and summarize Conventional Commit-style messages through bundled shell utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to draft Conventional Commit messages, list commit types, generate changelog text, and check recent commit messages before committing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unrelated local data-storage script that is not disclosed in the main instructions. <br>
Mitigation: Review the bundled scripts before installing and prefer the documented scripts/cz_cli.sh path for commit-helper workflows. <br>
Risk: Generated git commit commands may be copied into a repository without review. <br>
Mitigation: Review generated commit messages and commands before running them. <br>
Risk: The local data utility can store user-provided text on disk. <br>
Mitigation: Avoid entering sensitive text into scripts/script.sh unless local storage is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/commit-helper) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Commitizen cz-cli reference](https://github.com/commitizen/cz-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown, including suggested git commit commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read git history for changelog, lint, and breaking-change summaries; includes a separate local data utility in the artifact.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
