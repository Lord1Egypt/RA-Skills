## Description: <br>
Downloads Chinese-language ebooks from multiple sources with automatic fallback, file-host handling, archive extraction, and EPUB-to-PDF conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lb1121](https://clawhub.ai/user/lb1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for Chinese-language ebooks, download available formats, extract archives, and convert EPUB or MOBI files to PDF for downstream reading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates downloads from untrusted ebook and file-hosting sites and may extract remote archives. <br>
Mitigation: Run it in a sandbox or dedicated empty output folder, and scan downloaded files before opening or sharing them. <br>
Risk: Downloaded files may overwrite or collide with existing local files. <br>
Mitigation: Use a separate output directory for each run and review generated paths before running batch workflows. <br>
Risk: Book queries and download behavior are exposed to third-party sites. <br>
Mitigation: Avoid sensitive queries and assume external source and file-hosting services can observe searches and downloads. <br>
Risk: Downloaded content may have copyright or source-trust concerns. <br>
Mitigation: Use the skill only for content the user is authorized to access and verify the trustworthiness of each source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lb1121/chinese-ebook-downloader) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create downloaded ebook, archive, EPUB, MOBI, AZW3, TXT, or PDF files in a user-selected output directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
