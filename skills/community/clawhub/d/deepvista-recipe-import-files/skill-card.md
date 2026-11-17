## Description:

Imports selected local files recursively as DeepVista context cards so they can be searched as project knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other DeepVista users use this skill to bulk-import scoped project files into DeepVista as searchable file cards. It is intended for cases such as indexing a folder, adding codebase context, or uploading local files as knowledge cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive imports can upload exact local file contents, including secrets, tokens, keys, databases, or private configuration, to DeepVista.

Mitigation: Use a narrow directory or extension allow-list, exclude hidden credential paths and secret-bearing files, and review the matched file list before upload.

Risk: Running the recipe on a large directory can create many cards, and re-running it can create duplicates.

Mitigation: Confirm scope with the user, warn before processing more than 50 matched files, skip common generated directories, and use project-specific tags to make imports easier to review.

Risk: Binary, very large, or unreadable files may fail to import or create unsuitable cards.

Mitigation: Skip non-UTF-8 binary files, continue past individual file errors, and report skipped files and failures in the final summary.

## Reference(s):

- [DeepVista CLI](https://cli.deepvista.ai)
- [ClawHub Skill Page](https://clawhub.ai/jingconan/skills/deepvista-recipe-import-files)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through scoped file discovery, DeepVista card creation, progress reporting, and import summary output.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
