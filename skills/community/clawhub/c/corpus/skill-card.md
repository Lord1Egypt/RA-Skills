## Description:

Access a user's Corpus library from OpenClaw to search saved content, fetch item details, save links, and create reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doninocode](https://clawhub.ai/user/doninocode)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent read and update a user's Corpus library through the Corpus API. It supports profile lookup, content listing, search, content detail retrieval, URL saving, and reminder creation when a valid Corpus API token is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Corpus API token can be sent to any configured API URL.

Mitigation: Keep CORPUS_API_BASE_URL pinned to the legitimate HTTPS Corpus API before running the skill.

Risk: Passing the Corpus API token on the command line can expose it through shell history or process inspection.

Mitigation: Set CORPUS_API_TOKEN through the OpenClaw environment and avoid printing or logging the token.

Risk: Write commands can save URLs or create reminders in the user's Corpus account.

Mitigation: Review each save-url or create-reminder action before allowing it to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doninocode/skills/corpus)
- [Corpus AI app](https://apps.apple.com/us/app/corpus-ai/id6748364607)
- [Corpus API default service](https://corpusai.app)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CORPUS_API_TOKEN. Write actions can save URLs or create reminders in the user's Corpus account.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
