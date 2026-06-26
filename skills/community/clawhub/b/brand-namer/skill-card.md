## Description: <br>
Generate brand names with domain checks and analysis. Use when naming a startup, checking domain availability, or brainstorming product names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to brainstorm product or startup names, check likely domain availability, analyze name readability, and manage a local shortlist of candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain checks may disclose unreleased name ideas through DNS lookups. <br>
Mitigation: Avoid checking highly confidential names unless DNS lookup exposure is acceptable; use a separate manual review process for sensitive naming work. <br>
Risk: Saved shortlists and command history remain on the local machine under the configured Brand Namer data directory. <br>
Mitigation: Set BRAND_NAMER_DIR to an appropriate private location and remove saved shortlist or history files when they are no longer needed. <br>
Risk: A missing DNS A record is only a weak signal and does not prove that a domain, trademark, or social handle is available. <br>
Mitigation: Confirm availability with a registrar, trademark search, and social account checks before relying on a generated name. <br>


## Reference(s): <br>
- [Brand Namer on ClawHub](https://clawhub.ai/ckchzh/brand-namer) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with optional txt, csv, or json shortlist exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform DNS lookups for domain checks and may write shortlist and history files under the configured local data directory.] <br>

## Skill Version(s): <br>
3.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
