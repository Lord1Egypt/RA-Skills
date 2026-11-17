## Description:

Turn any website into a filesystem. Crawls sites automatically and mounts pages as markdown files you can grep, diff, cat, and explore with standard Unix commands — over SSH or HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigmindai](https://clawhub.ai/user/bigmindai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research public websites, inspect documentation, search crawled pages, and compare crawl changes using familiar Unix commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target website domains, search terms, and remote commands may be sent to OpenObj.

Mitigation: Use the skill only when sharing those inputs with OpenObj is acceptable.

Risk: Commands may be built from unvalidated user-controlled domains, paths, or search terms.

Mitigation: Validate and quote user-provided values before execution, and avoid attacker-supplied domains or terms.

Risk: The skill requests broad network access for SSH or HTTPS calls.

Mitigation: Prefer destination-scoped access to openobj.com where the agent runtime supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigmindai/skills/browse-website)
- [OpenObj HTTP execution endpoint](https://openobj.com/exec)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return crawled website content, search results, file listings, diffs, command output, stderr, and exit codes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
