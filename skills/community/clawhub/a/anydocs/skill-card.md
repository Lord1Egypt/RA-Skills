## Description:

Generic Documentation Indexing and Search indexes documentation sites, including SPAs and static docs, and lets agents search them from CLI or Python workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pektech](https://clawhub.ai/user/pektech)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use anydocs to configure documentation profiles, index pages from sitemaps or crawls, and search cached documentation from terminal or Python workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network behavior can retrieve and index untrusted or sensitive documentation URLs.

Mitigation: Use only trusted documentation URLs, and avoid indexing sensitive internal docs unless local cache retention is acceptable.

Risk: Optional browser rendering and gateway-token behavior need review before installation.

Mitigation: Use a trusted local gateway only, avoid non-loopback gateways, and do not pass tokens inline on shared systems.

Risk: Cached pages and indexes may retain copied documentation content locally.

Mitigation: Use the cache controls to clear retained content and review cache location and TTL before indexing private documentation.

Risk: Pinned dependencies may age after release.

Mitigation: Install in a virtual environment and update dependencies before use.

## Reference(s):

- [ClawHub anydocs release page](https://clawhub.ai/pektech/skills/anydocs)
- [anydocs README](artifact/README.md)
- [anydocs Quick Start Examples](artifact/examples/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with URLs, snippets, JSON configuration, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include rank, title, URL, relevance score, tags, and snippet when available.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
