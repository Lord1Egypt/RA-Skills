## Description: <br>
Reviews daily AI advancements and banking fintech progress from curated sources with full text inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lube845](https://clawhub.ai/user/lube845) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and fintech teams use this skill to fetch curated AI, banking, and financial technology sources, summarize substantive technical developments, and save a daily Markdown brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses listed public news and fintech sites over the network. <br>
Mitigation: Install it only if that network access is acceptable for the target environment and review the disclosed source list before use. <br>
Risk: The skill stores raw cached data and permanent Markdown report history in the local OpenClaw workspace. <br>
Mitigation: Delete or manage the workspace output directory when report history should not be retained, and treat cached-data reports as potentially one day stale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lube845/daily-fintech-brief) <br>
- [The Batch RSS](https://www.deeplearning.ai/the-batch/rss/) <br>
- [Ben's Bites RSS](https://www.bensbites.co/rss) <br>
- [Banking Dive RSS](https://www.bankingdive.com/feeds/news/) <br>
- [China Financial Computer technology news](https://www.fcc.com.cn/art/kjzx/) <br>
- [China Electronic Banking digital banking](https://www.cebnet.com.cn/szyh/) <br>
- [China Electronic Banking financial AI](https://www.cebnet.com.cn/financialai/) <br>
- [MPayPass](https://www.mpaypass.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown daily brief, with JSON returned from data-fetching helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw source data is cached locally for seven days; generated report Markdown files are retained in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
