## Description: <br>
Skill Box guides agents through five digital-life self-reflection workflows that analyze user-provided digital traces and produce structured profiles and readable reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wildbyteai](https://clawhub.ai/user/wildbyteai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users install this skill to ask an agent for guided self-reflection over their own social posts, chats, screenshots, public pages, or digital-history exports. The skill helps the agent collect scoped inputs, summarize behavioral patterns, and write local JSON and Markdown profiles that can be corrected, appended, or rolled back. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to inspect logged-in social accounts, chats, screenshots, and digital-history exports. <br>
Mitigation: Use pasted excerpts or narrow exports where possible, explicitly approve each platform and timeframe, and avoid full-account scans. <br>
Risk: Generated profile files may preserve sensitive personal inferences even when raw data is not retained. <br>
Mitigation: Review files under profiles after each run and delete or redact outputs that should not remain on disk. <br>
Risk: Browser-assisted collection may expose more personal context than the user intended. <br>
Mitigation: Prefer read-only browsing, confirm the account belongs to the user, and stop collection once the agreed scope has enough evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wildbyteai/digital-life) <br>
- [AI Clone methodology](artifact/references/ai-clone.md) <br>
- [Cringe Archaeology methodology](artifact/references/cringe-archaeology.md) <br>
- [Epitaph methodology](artifact/references/epitaph.md) <br>
- [Legacy Audit methodology](artifact/references/legacy-audit.md) <br>
- [Past Life methodology](artifact/references/past-life.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown summaries plus local JSON and Markdown profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profiles are intended to contain behavioral-pattern analysis rather than raw source content.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
