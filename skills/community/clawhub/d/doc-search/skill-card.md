## Description:

Searches a local document library such as an Obsidian vault, wiki, or notes folder using a BM25 inverted index, LLM query expansion, and grep for line-level matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantasyrl](https://clawhub.ai/user/fantasyrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and knowledge workers use this skill to find relevant files and line-level matches in local Markdown, text, reStructuredText, and Org document collections without external search infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recursively scans a user-selected local document directory and can index sensitive local content.

Mitigation: Use it only on trusted, intentional document directories and avoid folders containing secrets, private keys, or unrelated personal data.

Risk: The skill writes a persistent local index that may reveal document paths, titles, summaries, and terms.

Mitigation: Keep the index in a private location, avoid shared or attacker-writable directories, and delete or rebuild the index when the document set changes sensitivity.

Risk: Unsafe command and path handling can make grep or script execution risky when paths, keywords, or index contents are untrusted.

Mitigation: Quote shell arguments, validate returned paths stay under the selected docs directory, and review commands before execution.

Risk: The artifact describes more than one default index location, which can confuse review and cleanup.

Mitigation: Confirm the actual index path before use and document a single expected location in deployment guidance.

## Reference(s):

- [doc-search README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/fantasyrl/skills/doc-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown response with inline shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top-K defaults to 5; default indexed extensions are md, txt, rst, and org.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
