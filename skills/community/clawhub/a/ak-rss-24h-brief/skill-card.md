## Description: <br>
Read RSS/Atom feeds from an OPML list, fetch articles from the last N hours, and generate a Chinese categorized brief that keeps original titles and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seandong](https://clawhub.ai/user/seandong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and information workers use this skill to turn an OPML RSS subscription list into a concise Chinese Markdown brief for a recent time window. It is suited for requests such as generating a 24-hour categorized summary while preserving source article titles and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to the OPML URL and to feed URLs listed inside that OPML source. <br>
Mitigation: Use trusted OPML sources and lower --max-feeds for unfamiliar lists. <br>
Risk: The optional --output parameter writes the generated brief to a file path. <br>
Mitigation: Provide --output only for a file path where the brief is intended to be written. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seandong/ak-rss-24h-brief) <br>
- [Andrej Karpathy RSS list source post](https://x.com/karpathy/status/2018043254986703167) <br>
- [Default OPML RSS list](https://gist.githubusercontent.com/emschwartz/e6d2bf860ccc367fe37ff953ba6de66b/raw/426957f043dc0054f95aae6c19de1d0b4ecc2bb2/hn-popular-blogs-2025.opml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with categorized article links and Chinese summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated Markdown brief to a requested output file.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
