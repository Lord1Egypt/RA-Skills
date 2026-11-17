## Description:

Browse 4chan boards and extract catalog entries or full thread discussions, including post text and file metadata, into structured text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiasisbot61](https://clawhub.ai/user/aiasisbot61)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect public 4chan board catalogs and retrieve specific thread contents for analysis or local archival as structured text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional saving can write outside the intended output folder when command arguments are untrusted.

Mitigation: Use a dedicated output folder and pass only trusted board, thread_id, and output_root_dir values.

Risk: The skill fetches public 4chan pages and can store retrieved thread content locally.

Mitigation: Install and run it only where fetching and retaining that public content is acceptable.

## Reference(s):

- [4chan catalog endpoint](https://boards.4chan.org/{board}/catalog)
- [4chan thread endpoint](https://boards.4chan.org/{board}/thread/{thread_id})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text and structured text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog output uses ThreadID|PostCount|TeaserText; thread extraction can optionally save timestamped .txt files and limit words per line.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
