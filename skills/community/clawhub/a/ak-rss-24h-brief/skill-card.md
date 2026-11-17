## Description:

Read RSS/Atom feeds from an OPML list, fetch articles from the last N hours, and generate a Chinese categorized brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seandong](https://clawhub.ai/user/seandong)

### License/Terms of Use:


## Use Case:

Developers and knowledge workers use this skill to generate recent Chinese RSS briefings from an OPML feed bundle while preserving source titles and article links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The feed fetcher can make outbound requests to arbitrary or internal URLs supplied by an OPML file.

Mitigation: Use trusted OPML files and run the skill in a sandboxed environment without access to internal networks or sensitive local files.

Risk: Large feed lists or responses can increase network and processing load.

Mitigation: Keep worker and feed counts conservative until URL and response-size validation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seandong/skills/ak-rss-24h-brief)
- [RSS source OPML list](https://gist.githubusercontent.com/emschwartz/e6d2bf860ccc367fe37ff953ba6de66b/raw/426957f043dc0054f95aae6c19de1d0b4ecc2bb2/hn-popular-blogs-2025.opml)
- [Andrej Karpathy source post](https://x.com/karpathy/status/2018043254986703167)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Chinese categorized summaries and original article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write the generated brief to a Markdown file when an output path is supplied.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
