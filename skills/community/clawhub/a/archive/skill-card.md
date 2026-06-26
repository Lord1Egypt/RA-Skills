## Description: <br>
Capture and preserve content as intelligent snapshots with semantic search, automatic extraction, and proactive resurfacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use Archive to preserve user-supplied articles, webpages, videos, PDFs, images, and notes as local Markdown snapshots, then retrieve them by topic, project, time, author, or type. It also supports limited contextual resurfacing of relevant archived items when the user is working on related topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archived items can include full extracted text, metadata, user preferences, search history, and resurfacing history in a persistent local copy. <br>
Mitigation: Avoid archiving secrets or sensitive private material unless the user is comfortable storing that content under ~/archive/. <br>
Risk: Contextual resurfacing can interrupt the user or reveal previously saved material at an unwanted time. <br>
Mitigation: Respect opt-out language such as 'don't resurface' or 'just search when I ask' and switch to search-only mode. <br>
Risk: Fetching or extracting user-supplied URLs and documents may capture more content than a bookmark would. <br>
Mitigation: Use the skill only for material the user explicitly asks to archive and preserve the saved context for why it was stored. <br>


## Reference(s): <br>
- [ClawHub release: Archive](https://clawhub.ai/ivangdavila/archive) <br>
- [Capture Patterns](artifact/capture.md) <br>
- [Search Patterns](artifact/search.md) <br>
- [Resurfacing Rules](artifact/resurface.md) <br>
- [Archive Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with local Markdown files and occasional shell commands for archive setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local archive state under ~/archive/ when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
