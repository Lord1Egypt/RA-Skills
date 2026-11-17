## Description:

An OpenClaw skill to manage a user's vinyl record collection on Discogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrojas537](https://clawhub.ai/user/jrojas537)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to query and manage a Discogs vinyl collection, search the Discogs catalog, fetch release details and album art, manage a wantlist, and calculate collection value from a local cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable Discogs account token in local configuration.

Mitigation: Use a narrowly scoped token, avoid entering it in commands that may be logged, and check permissions on ~/.config/discogs-cli/config.yaml.

Risk: Wantlist commands can modify the user's Discogs account.

Mitigation: Confirm the target release ID and intended add or remove action before running wantlist mutation commands.

Risk: Sync and album-art commands create local cache files.

Mitigation: Review where cache files are written and periodically remove stale local data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jrojas537/skills/discogs-cli)
- [Go installation documentation](https://go.dev/doc/install)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Files]

**Output Format:** [Markdown with bash command examples, CLI text tables, and local media/cache file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Go, a Discogs username, and a Discogs personal access token for authenticated collection and wantlist commands.]

## Skill Version(s):

1.3.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
