## Description:

Downloads product images from Taobao and 1688 by using product URLs or product-name search to collect main and detail images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gufusheng1994-dev](https://clawhub.ai/user/gufusheng1994-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather e-commerce product imagery from Taobao or 1688 listings, save the images locally, and report download results. It is most useful when a user provides a product URL, product name, or curated image URL list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can fetch and save arbitrary URL contents without strong validation or scope controls.

Mitigation: Use only trusted image URL lists or product pages, avoid internal or private network URLs, and review the destination directory before running downloads.

Risk: The advertised product URL and search workflow depends on separate browser extraction and may be incomplete when the script runs by itself.

Mitigation: Confirm browser extraction has produced the intended image URLs before invoking the download helper, and review failed or missing downloads in the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gufusheng1994-dev/skills/1688)
- [Publisher profile](https://clawhub.ai/user/gufusheng1994-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, browser-operation steps, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded image files and report counts, file sizes, save paths, and failures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
