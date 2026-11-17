## Description: <br>
Converts RSS or Atom feed content into structured Markdown by fetching a feed, extracting titles, links, descriptions, publication dates, and authors, and saving the result locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive RSS or Atom feeds, back up blog posts, or collect reading material as Markdown files. It is intended for explicit feed-conversion tasks rather than unrelated document generation or search work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The activation wording is broader than RSS-to-Markdown conversion and could be invoked for unrelated document or search tasks. <br>
Mitigation: Use the skill only for explicit RSS or Atom feed conversion requests and avoid activating it for unrelated document-processing work. <br>
Risk: The skill can fetch URLs and save files locally. <br>
Mitigation: Review feed URLs, generated commands, and output paths before execution, and write only to intended local directories. <br>


## Reference(s): <br>
- [Detailed reference](references/detail.md) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feed-to-md-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch user-provided feed URLs and write Markdown files plus feed metadata to a local output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
