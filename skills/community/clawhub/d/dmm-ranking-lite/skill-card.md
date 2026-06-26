## Description: <br>
Fetch DMM/FANZA public rankings (daily/weekly/monthly) without API keys and output top 10 in numbered text format with Japanese title, Chinese translation, and cover image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeeroyjoy-pixel](https://clawhub.ai/user/leeeroyjoy-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to collect DMM/FANZA daily, weekly, or monthly ranking entries from public pages and present a compact Top N result with original Japanese titles, Chinese translations, and cover image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public page structure changes or age confirmation failures can cause incomplete or missing ranking data. <br>
Mitigation: Check the page snapshot, adjust selectors, and report the actual number of entries retrieved when fewer than requested are available. <br>
Risk: The release security guidance recommends use only in trusted ClawHub development or maintainer environments. <br>
Mitigation: Review any proposed browser actions or commands before allowing workflows that publish, deploy, moderate, or use local credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leeeroyjoy-pixel/dmm-ranking-lite) <br>
- [DMM/FANZA ranking page](https://video.dmm.co.jp/av/ranking/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Numbered Markdown text with Japanese title, Chinese translation, and cover URL fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default Top10 output; may return fewer entries when the public page yields fewer results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
