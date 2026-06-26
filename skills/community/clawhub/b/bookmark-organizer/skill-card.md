## Description: <br>
Imports browser bookmark HTML exports and turns them into a deduplicated, categorized, time-sorted Markdown knowledge base with optional dead-link checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[farhigh233](https://clawhub.ai/user/farhigh233) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to convert browser bookmark exports into organized Markdown files for review, search, cleanup, and personal knowledge-base workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bookmark exports can contain private, intranet, account-specific, or token-bearing URLs. <br>
Mitigation: Process exports locally, review generated Markdown before sharing, and avoid publishing output that contains sensitive links. <br>
Risk: The optional link-checking mode contacts every bookmarked URL and may reveal private browsing or internal-resource information to remote servers. <br>
Mitigation: Use link checking only for exports that are safe to probe externally, and avoid it for intranet, confidential, or tokenized URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/farhigh233/bookmark-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates categorized Markdown files, summary files, duplicate/link reports, and optional dead-link results based on local bookmark input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
