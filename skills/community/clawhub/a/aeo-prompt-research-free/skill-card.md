## Description: <br>
Discovers AI prompts and topics that matter for a brand's Answer Engine Optimization using free web crawling, search, and model reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, SEO, and content teams use this skill to research conversational AI prompts for a brand, prioritize AEO opportunities, audit existing content coverage, and identify content gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make outbound requests to user-provided domains while researching a brand website. <br>
Mitigation: Use it on public sites, avoid internal or private network hosts, and review target domains before crawling. <br>
Risk: Generated prompt priorities and content recommendations are model-derived and may be incomplete or inaccurate. <br>
Mitigation: Review the report before using it for strategy decisions and validate high-priority recommendations against current business and market context. <br>


## Reference(s): <br>
- [AEO Prompt Research Methodology](references/aeo-methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with prompt tiers, scores, coverage status, content gap analysis, and recommended next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include website crawl text when the optional crawl script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
