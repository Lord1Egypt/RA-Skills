## Description: <br>
Search Amazon product listings for a keyword and return structured JSON results, with ASIN/UUID caching and automatic result file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikehankk](https://clawhub.ai/user/mikehankk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run keyword-based Amazon product searches with price and page limits, optional proxying, incremental deduplication, and optional image downloads for product research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser stealth settings, cookie/session handling, debug captures, and automatic persistence can expose browsing or session data. <br>
Mitigation: Run the skill only in a disposable sandbox, avoid authenticated Amazon sessions, and treat generated cache files, debug files, and terminal logs as sensitive. <br>
Risk: The scanner identified an unsafe shell execution path and raw cookie output behavior. <br>
Mitigation: Prefer a later version that removes shell interpolation and raw cookie output; if this version is used, only pass trusted inputs and review execution in an isolated environment. <br>
Risk: Proxy support can route requests and image downloads through infrastructure controlled by the proxy operator. <br>
Mitigation: Use only trusted proxies or leave proxy configuration disabled. <br>


## Reference(s): <br>
- [ClawHub Amazon Search release](https://clawhub.ai/mikehankk/amazon-search) <br>
- [Bun runtime](https://bun.sh) <br>
- [Amazon](https://www.amazon.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Structured JSON search results, saved JSON files, and plain-text configuration commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include search metadata and product item fields; incremental mode caches ASIN/UUID identifiers for deduplication, and optional image downloads write to a local image cache.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
