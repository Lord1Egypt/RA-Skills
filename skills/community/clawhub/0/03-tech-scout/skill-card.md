## Description: <br>
Daily multi-source intelligence digest that proactively scans X, YouTube, Reddit, and GitHub for tools, techniques, and updates relevant to active projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pingukim225](https://clawhub.ai/user/pingukim225) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent produce a daily shortlist of high-signal technical updates for active AI, crypto, content creation, or technical projects. It supports morning briefings by ranking relevant items, explaining why they matter, and suggesting concrete next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs recurring web and API research that may use external services and credentials. <br>
Mitigation: Confirm whether automatic daily runs are enabled and use restricted API keys or tokens with the minimum permissions needed. <br>
Risk: Project keywords may reveal sensitive client names, strategy terms, or internal priorities to external search and API providers. <br>
Mitigation: Use sanitized keyword sets and avoid confidential terms when configuring monitored project domains. <br>
Risk: Local digest and seen-URL state files may retain research history over time. <br>
Mitigation: Periodically review, archive, or clean state files according to the user's data-retention needs. <br>


## Reference(s): <br>
- [03 Tech Scout ClawHub Listing](https://clawhub.ai/pingukim225/03-tech-scout) <br>
- [pingukim225 ClawHub Profile](https://clawhub.ai/user/pingukim225) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown digest files with ranked items, source notes, links, and suggested actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a daily digest, maintains seen-URL state for deduplication, and may produce partial results when individual sources fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
