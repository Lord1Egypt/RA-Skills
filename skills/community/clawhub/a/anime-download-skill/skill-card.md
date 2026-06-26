## Description: <br>
Use when the user asks to search anime torrents, download anime episodes, find anime resources, or browse miobt.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isongxw](https://clawhub.ai/user/isongxw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search anime torrent listings, browse seasonal anime, and prepare download commands through the anicatch CLI. Users should confirm that any requested download is lawful and safe for their environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BitTorrent downloads can create legal, privacy, and untrusted-file exposure. <br>
Mitigation: Confirm each download explicitly, verify that the content is lawful to download, use a safe output folder, and scan or validate downloaded files before opening them. <br>
Risk: The skill runs the external anicatch CLI through uvx or pipx. <br>
Mitigation: Install only if the user accepts that dependency path and review the generated command before execution. <br>


## Reference(s): <br>
- [Anime Download Skill on ClawHub](https://clawhub.ai/isongxw/anime-download-skill) <br>
- [anicatch GitHub Repository](https://github.com/isongxw/anicatch) <br>
- [anicatch on PyPI](https://pypi.org/project/anicatch/) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may invoke uvx or pipx to run the external anicatch CLI.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
