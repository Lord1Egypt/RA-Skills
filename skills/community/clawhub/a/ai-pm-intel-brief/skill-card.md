## Description: <br>
Creates concise AI product-management intelligence briefs from recent Twitter/X or similar high-signal sources, emphasizing key signals, product insights, excerpts, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QRG-cloud](https://clawhub.ai/user/QRG-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI product managers and product strategy teams use this skill to turn recent social posts or curated account watchlists into a selective daily brief with judgments, high-signal items, product implications, excerpts, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may route broad news or trend-summary requests into an AI product-management brief workflow and may default to a Chinese brief template. <br>
Mitigation: Use it when an AI product-management intelligence brief is intended, and specify language or scope when the default template is not appropriate. <br>
Risk: Collecting recent social signals can expand beyond intended public sources or involve unnecessary account/session access. <br>
Mitigation: Limit collection to intended public sources and avoid granting unnecessary account or session access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QRG-cloud/ai-pm-intel-brief) <br>
- [Output template](references/output-template.md) <br>
- [Default watchlist](references/watchlist.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown brief with judgments, ranked signals, summaries, product insights, optional excerpts, and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include partial-coverage notes when rate limits or unavailable accounts limit collection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
