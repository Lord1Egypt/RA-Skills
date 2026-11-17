## Description:

bt-search searches adog.uk for BT magnet-link torrents by keyword and returns torrent names, sizes, seed and leech counts, matched files, creation dates, and magnet links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[men459](https://clawhub.ai/user/men459)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search BT magnet-link resources by keyword, inspect torrent metadata, and present results as readable search listings. It does not download files or stream media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the search script silently contacts an unrelated advertising domain on every search.

Mitigation: Review before installing and prefer a version with the advertising request removed.

Risk: Torrent search results and magnet links may be untrusted, unsafe, or unlawful to download.

Mitigation: Treat results as untrusted metadata and verify legality, safety, and source trust before using any magnet link.

## Reference(s):

- [bt-search ClawHub skill page](https://clawhub.ai/men459/skills/bt-search)
- [adog.uk BT magnet-link search homepage](https://www.adog.uk/)
- [adog.uk torrent detail API](https://www.adog.uk/api/skill/torrent/{info_hash})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with JSON search-result fields and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include magnet links and torrent file metadata; search terms are sent to adog.uk.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
