## Description:

Stash and recall short text snippets in a local file-backed clipboard for later use in the same workspace without a database or external service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and workspace users use this skill to save, list, recall, and clear short one-line or escaped multi-line snippets during a session-spanning workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snippet contents are stored unencrypted in a plaintext local cache file.

Mitigation: Do not use the skill for secrets or sensitive personal data, and inspect or remove the cache file according to local data handling requirements.

Risk: The clear-all command truncates the stash file and can permanently remove saved snippets.

Mitigation: Back up needed snippets before clearing the stash, or confirm that the saved content is disposable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/clipboard-stash-demo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and plain-text snippet content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists snippets as plaintext TSV under ~/.cache/clipboard-stash/stash.tsv; no external service or database is used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
