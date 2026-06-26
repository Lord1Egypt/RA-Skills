## Description: <br>
Downloads Chinese ebooks to the user's computer by searching third-party ebook sources, resolving cloud-storage download links, downloading archives, and extracting supported ebook formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoyishuai](https://clawhub.ai/user/caoyishuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for Chinese ebook files, obtain download links from third-party sources, and extract EPUB, AZW3, MOBI, PDF, or TXT files on their computer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads book files from third-party sources, which may raise source legitimacy or rights concerns. <br>
Mitigation: Confirm that each source is legitimate and that the user has rights to download the material before running the workflow. <br>
Risk: Downloaded archives from third-party sources may contain unsafe or unexpected files. <br>
Mitigation: Download into a quarantined folder, inspect the archive, and review extracted files before opening them or moving them to sensitive locations. <br>
Risk: The workflow writes and removes local files during download, extraction, and cleanup. <br>
Mitigation: Run only in a user-approved download directory and verify file paths before deleting temporary archives. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caoyishuai/ebook-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded archive files and extracted ebook files when executed by an agent with browsing and local file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
