## Description: <br>
Use when analyzing a TikTok video or breaking down its script and structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newt0n](https://clawhub.ai/user/newt0n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, sellers, and content teams use this skill to analyze TikTok URLs, recover transcripts and visual notes, and produce a reusable breakdown of script, storyboard, metrics, hooks, and conversion logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok URLs are sent to CreatOK for remote analysis. <br>
Mitigation: Use a dedicated CreatOK API key and avoid submitting URLs whose analysis would expose sensitive or restricted information. <br>
Risk: Returned transcripts, visual analysis, metadata, and results are written to local .artifacts folders. <br>
Mitigation: Review and delete local artifacts after sensitive analyses. <br>
Risk: The package includes broader remote task APIs in addition to the analyze workflow. <br>
Mitigation: Review follow-up generation workflows before use and avoid invoking broader task APIs unless they are needed. <br>


## Reference(s): <br>
- [CreatOK Analyze Video Skill Page](https://clawhub.ai/newt0n/creatok-analyze-video) <br>
- [Common Rules](references/common-rules.md) <br>
- [Agent Skills Contracts](references/contracts.md) <br>
- [CreatOK API Keys](https://www.creatok.ai/app/workspace/api-keys) <br>
- [CreatOK](https://www.creatok.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown analysis in the conversation plus local JSON artifacts under analyze-video/.artifacts/<run_id>.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TikTok URL and CREATOK_API_KEY; stores transcript, visual analysis, metadata, and result artifacts locally.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
