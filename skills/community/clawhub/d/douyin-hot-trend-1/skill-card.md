## Description: <br>
Fetches Douyin hot list and trending-search data, including titles, heat values, rankings, and links for popular videos, challenges, music, and related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, analysts, marketers, and social media operators use this skill to fetch public Douyin trend data for hot-topic tracking, content trend analysis, and planning reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the fetch scripts sends network requests to Douyin. <br>
Mitigation: Run the skill only in environments where Douyin access is expected and permitted. <br>
Risk: Local trend history may be retained in data/douyin.db or regenerated data/index.html. <br>
Mitigation: Delete those local files when trend history should not be kept. <br>
Risk: Generated HTML reports render fetched titles and links. <br>
Mitigation: Open generated reports cautiously and review fetched content before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-1106/douyin-hot-trend-1) <br>
- [Douyin web interface](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, shell commands] <br>
**Output Format:** [Console text output, JSON arrays, and locally generated HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trend items include rank, title, heat value, label when present, and a detail link; scripts can limit the number of returned items.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
