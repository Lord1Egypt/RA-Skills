## Description: <br>
Builds a blog editorial backlog from verifiable user-demand signals by mining sources such as Google Suggest, People Also Ask, Reddit, Stack Overflow, GitHub issues, vendor forums, and changelogs, then returning writer-ready topic scaffolds with cited evidence, post formats, primary sources, problem summaries, fixes, version context, and FAQ variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, founders, indie hackers, and developer-tool teams use this skill to research long-tail blog topics grounded in citable user demand. It helps build an editorial backlog with demand signals, source URLs, topic formats, keyword variants, problem summaries, fixes, and version context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rely on sensitive credentials for optional keyword-data enrichment or authenticated workflows. <br>
Mitigation: Configure only the credentials needed for the intended workflow and review generated commands or append operations before execution. <br>
Risk: Research output may become stale because search results, issue threads, forums, and keyword metrics change over time. <br>
Mitigation: Re-fetch primary sources before publication and preserve cited URLs and verbatim evidence with each accepted topic. <br>
Risk: Backlog append behavior could add unwanted or duplicate topics if accepted without review. <br>
Mitigation: Use the skill's confirmation step and cannibalization checks before writing accepted topics to a backlog file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/automatelab/blog-topic-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured topic records with citable source URLs and optional JSON append guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backlog append instructions after user confirmation; can optionally use DataForSEO keyword data when credentials are configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
