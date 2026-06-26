## Description: <br>
Gaokao Essay helps agents generate Gaokao essay drafts, openings, endings, writing materials, structure suggestions, and scoring-style feedback from local templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, educators, and agents use this skill to draft Gaokao essay responses and retrieve Chinese writing templates, openings, endings, and topic-material suggestions for exam preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an undocumented generic helper that can persist user-supplied text and command history locally. <br>
Mitigation: Use the documented scripts/essay.sh workflow for essay generation, avoid passing sensitive text to scripts/script.sh, and review or clear the local Gaokao Essay data directory when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/gaokao-essay) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain terminal text from local shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated locally from built-in templates; auxiliary utility behavior may write local files under the configured Gaokao Essay data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
