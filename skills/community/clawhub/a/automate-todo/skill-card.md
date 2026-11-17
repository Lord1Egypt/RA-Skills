## Description:

Automate TODO helps an agent complete items under the Current header in TODO.md, apply related documentation, changelog, manifest, and roadmap updates, and archive completed items with a bundled TODO maintenance script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to work through repository TODO.md Current items, apply associated version and documentation updates, maintain a current roadmap, and archive completed TODOs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback guidance can discard unrelated tracked local changes across the repository.

Mitigation: Use the skill only in a clean branch or disposable worktree, or after committing or stashing unrelated work; review any rollback step before allowing it.

Risk: The skill can update TODO.md, documentation, CHANGELOG.md, manifest files, and the current roadmap.

Mitigation: Review proposed file changes and test results before accepting the completed TODO automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhauga/skills/automate-todo)
- [Publisher profile](https://clawhub.ai/user/jhauga)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code edits and shell commands; bundled script output is terminal text and TODO.md file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify repository files including TODO.md, documentation, CHANGELOG.md, manifests, and .github/current.roadmap.md.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
