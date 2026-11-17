## Description: <br>
archive-free helps agents capture external articles, videos, tweets, and PDFs as local Markdown snapshots with summaries, tags, metadata, and keyword search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to archive external URLs or text into local Markdown files for personal knowledge management and research collection. It is intended for basic content extraction, metadata capture, tag management, and keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks for broad command execution permissions. <br>
Mitigation: Install only when local archive setup commands are needed, review proposed commands before execution, and prefer a later version that narrows command execution. <br>
Risk: The skill advertises unrelated activation claims outside basic archiving. <br>
Mitigation: Treat the supported behavior as local content archiving and verify any media processing, SEO, or unrelated workflow claims before relying on them. <br>
Risk: Archived content may include sensitive local research notes or third-party material. <br>
Mitigation: Restrict access to the archive directory, avoid storing secrets, and review copyright or site terms before archiving protected content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and structured JSON-style status output with occasional shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archived items are described as local files under ~/archive/items/{date}_{slug}.md; media binaries are not saved.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
