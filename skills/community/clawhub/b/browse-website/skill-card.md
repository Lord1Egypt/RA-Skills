## Description: <br>
Turn any website into a filesystem. Crawls sites automatically and mounts pages as markdown files you can grep, diff, cat, and explore with standard Unix commands — over SSH or HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigmindai](https://clawhub.ai/user/bigmindai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and support teams use this skill to crawl public websites, inspect pages as markdown, search site content, and compare changes across crawls with standard Unix commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenObj is a third-party service that can see requested sites, search terms, and commands. <br>
Mitigation: Use the skill for public, non-sensitive websites; avoid private URLs, confidential queries, authenticated pages, and regulated data unless the user explicitly trusts OpenObj for that processing. <br>
Risk: Fresh crawls and forced recrawls can consume OpenObj credits. <br>
Mitigation: Prefer cached reads, review commands before running recrawl operations, and stop retrying when a credit limit error appears. <br>
Risk: The skill depends on network access to openobj.com over SSH or HTTPS. <br>
Mitigation: Confirm network permission before use and fall back to the HTTP API when SSH is unavailable. <br>


## Reference(s): <br>
- [OpenObj HTTP API endpoint](https://openobj.com/exec) <br>
- [ClawHub skill page](https://clawhub.ai/bigmindai/browse-website) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with SSH and curl command examples; HTTP API calls return JSON with stdout, stderr, and exitCode fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to openobj.com. Cached reads are free, while new crawls and forced recrawls may consume OpenObj credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
