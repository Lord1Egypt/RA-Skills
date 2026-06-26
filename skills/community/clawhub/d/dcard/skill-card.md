## Description: <br>
Fetches full Dcard article content and forum post listings using Camoufox browser automation, returning titles, body text, image links, and post metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public Dcard posts or forum listings for summarization, analysis, or content review workflows. It is best suited for low-volume access to public content where the operator accepts Dcard and Cloudflare policy considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stealth browser automation that contacts Dcard and may conflict with Dcard or Cloudflare policies. <br>
Mitigation: Use it only for public content, keep usage low-volume, and confirm the intended workflow is acceptable before running it. <br>
Risk: The skill depends on Camoufox, patchright, and lxml at runtime. <br>
Mitigation: Review and install dependencies from trusted sources in an isolated environment before use. <br>
Risk: Short bursts of requests may trigger rate limits or access challenges. <br>
Mitigation: Limit repeated fetches and add delays or manual review for any automated workflow. <br>


## Reference(s): <br>
- [ClawHub Dcard skill page](https://clawhub.ai/ichendong/dcard) <br>
- [Publisher profile: ichendong](https://clawhub.ai/user/ichendong) <br>
- [Dcard public forum](https://www.dcard.tw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands; Markdown guidance with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact Dcard through Camoufox and patchright browser automation and can include public post URLs and image links.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
