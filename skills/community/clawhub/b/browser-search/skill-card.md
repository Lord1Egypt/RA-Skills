## Description: <br>
Browser Search lets an agent use a local Chromium browser to search public search engines and extract search result titles and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshuikeji](https://clawhub.ai/user/linshuikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search public web results, gather current information, find technical documentation, and perform public market research without configuring a search API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to public search engines and may reveal confidential or sensitive intent. <br>
Mitigation: Do not use the skill for confidential searches; review queries before execution. <br>
Risk: The skill depends on Playwright and a local Chromium installation. <br>
Mitigation: Install only in environments where adding Playwright and Chromium is acceptable and maintain those dependencies with normal patching. <br>
Risk: The skill can save search results to a user-specified output path. <br>
Mitigation: Review requested output paths before saving; the artifact limits output paths to the user's home directory. <br>


## Reference(s): <br>
- [Browser Search on ClawHub](https://clawhub.ai/linshuikeji/browser-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [JSON search results with optional saved result files and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include the normalized query, selected search engine, result count, and title and URL pairs.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
