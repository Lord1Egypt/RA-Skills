## Description: <br>
Fetches Douyin hot-list data and keyword search results, including natural-language requests that map to scraper commands. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Douyin trending topics or keyword-based video search results and save them as structured data for analysis or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers can initiate Douyin network searches and send search terms to Douyin sooner than some users expect. <br>
Mitigation: Use explicit Douyin-related requests, avoid sensitive keywords, and run the skill only when sharing those search terms with Douyin is acceptable. <br>
Risk: Saved result files may be written to paths chosen during use. <br>
Mitigation: Choose output file paths deliberately and review saved JSON or CSV results before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-hot-scraper) <br>
- [Douyin](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON or CSV data with terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save results to a selected output path; keyword search defaults to 10 results and hot-list retrieval defaults to 20 results.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
