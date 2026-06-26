## Description: <br>
Formats commit messages using the Conventional Commits specification for automated tooling, changelog generation, and semantic versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bastos](https://clawhub.ai/user/bastos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to draft, edit, and validate git commit messages in the Conventional Commits format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during broad discussions about commits, even when the user did not explicitly ask to draft or format a commit message. <br>
Mitigation: Use it for explicit requests to draft, edit, validate, or format commit messages, and review generated messages before committing. <br>
Risk: A generated commit type, scope, or breaking-change marker can affect changelog and semantic-versioning automation if it does not match the actual change. <br>
Mitigation: Check the final message against the diff and release policy before using it in a repository. <br>


## Reference(s): <br>
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) <br>
- [ClawHub skill page](https://clawhub.ai/bastos/conventional-commits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown commit-message guidance and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commit types, optional scopes, body and footer guidance, breaking-change notation, and example commit messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
