## Description:

Read EPUB, PDF, or TXT books from Project Gutenberg, direct URLs, or local files with progress tracking and chunked reading for agent learning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josharsh](https://clawhub.ai/user/josharsh)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to search, download, and read long-form books in manageable chunks while preserving reading progress. It is suited for learning, research, summarization, and knowledge extraction from public-domain, owned, or otherwise permitted reading material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe page-count input can turn the --pages argument into local command execution.

Mitigation: Review before installing and do not allow untrusted users or content to choose --pages until numeric argument validation is fixed.

Risk: Untrusted download URLs or unauthorized book sources can expose agents to unsafe or impermissible content.

Mitigation: Use public-domain or owned books, avoid untrusted download URLs, and check local law before using copyrighted sources.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Install dependencies in a pinned virtual environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josharsh/skills/book-reader)
- [Publisher profile](https://clawhub.ai/user/josharsh)
- [Gutendex Project Gutenberg API](https://gutendex.com)
- [Anna's Archive](https://annas-archive.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with JSON progress state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads selected chunks of books, reports progress, lists downloaded files, and stores reading state under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
