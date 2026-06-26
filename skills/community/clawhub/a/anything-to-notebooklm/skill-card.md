## Description: <br>
Turns content from WeChat articles, webpages, YouTube videos, documents, images, audio, archives, and search queries into NotebookLM sources and generated outputs such as podcasts, slide decks, mind maps, reports, quizzes, and flashcards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SonicBotMan](https://clawhub.ai/user/SonicBotMan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect public web content and local files, upload selected material to NotebookLM, and request generated learning or presentation assets. Typical outputs include summaries, reports, quizzes, flashcards, slide decks, mind maps, podcasts, and other NotebookLM-generated artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, URLs, OCR output, transcribed audio, and search-derived material may be uploaded to NotebookLM. <br>
Mitigation: Use a preflight review of exactly which sources will be processed and avoid sensitive, regulated, confidential, or oversized inputs unless the user explicitly approves the upload. <br>
Risk: The installer adds a third-party WeChat MCP server dependency and asks the user to configure it in the global Claude configuration. <br>
Mitigation: Review the MCP server source and configuration before enabling it, keep dependencies pinned or reviewed, and remove or disable the MCP entry when it is not needed. <br>
Risk: Archive, OCR, and transcription workflows can process more content than the user initially expects. <br>
Mitigation: List files and extracted content before upload, limit processing to user-selected paths, and avoid bulk archives unless the contents have been inspected. <br>
Risk: Generated materials can reflect copyrighted or third-party source content. <br>
Mitigation: Confirm rights to the source material and review generated outputs before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SonicBotMan/anything-to-notebooklm) <br>
- [Project homepage](https://github.com/joeseesun/anything-to-notebooklm) <br>
- [Google NotebookLM](https://notebooklm.google.com/) <br>
- [Microsoft markitdown](https://github.com/microsoft/markitdown) <br>
- [wexin-read-mcp](https://github.com/Bwkyd/wexin-read-mcp) <br>
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown-style agent responses with command snippets, status messages, local file paths, and generated artifacts such as MP3, PDF, JSON, Markdown, PNG, or MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected source content to NotebookLM and may create intermediate converted text files and downloaded artifacts under /tmp unless the user specifies another path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
