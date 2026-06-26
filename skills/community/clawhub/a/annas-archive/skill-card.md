## Description: <br>
Find and download ebooks or papers from Anna's Archive with EPUB-first selection and /tmp storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ricardodpalmeida](https://clawhub.ai/user/Ricardodpalmeida) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Anna's Archive for books or papers, rank candidates with an EPUB preference, and optionally download a selected match to /tmp when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Externally configured downloader code can be executed through the Anna MCP command or source directory settings. <br>
Mitigation: Install only trusted annas-mcp binaries or source trees and avoid environment overrides unless the paths are controlled. <br>
Risk: The skill can download potentially copyrighted or unauthorized materials to the local machine. <br>
Mitigation: Use it only for material the user is authorized to access, keep downloads confined to /tmp/annas-archive-downloads, and purge old files with the cleanup script. <br>
Risk: Download URLs could point outside the intended Anna's Archive hosts if runtime safeguards are changed. <br>
Mitigation: Keep HTTPS-only access and the configured allowed-host list in place before downloading. <br>


## Reference(s): <br>
- [Security and Storage Rules](artifact/references/security-and-storage-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Ricardodpalmeida/annas-archive) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, files, guidance] <br>
**Output Format:** [JSON status objects and chat-facing text, with optional downloaded ebook or paper files under /tmp/annas-archive-downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers EPUB when available, keeps downloads under /tmp, and includes a cleanup script for aged temporary downloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
