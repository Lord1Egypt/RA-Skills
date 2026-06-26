## Description: <br>
Web search using curl with Baidu, Google, Bing, and DuckDuckGo for agents that need a lightweight online search helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluejoy34](https://clawhub.ai/user/bluejoy34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run web searches from an agent environment when dedicated search APIs are unavailable. It supports selecting Baidu, Google, Bing, or DuckDuckGo and limiting the number of returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to public search engines and may expose secrets, private customer data, proprietary code, or credentials. <br>
Mitigation: Do not use sensitive queries with this skill, and review organizational data-handling requirements before use. <br>
Risk: The default Baidu path uses HTTP, and the sanitizer is described by the security evidence as imperfect. <br>
Mitigation: Prefer SEARCH_ENGINE=google, SEARCH_ENGINE=bing, or SEARCH_ENGINE=duckduckgo where appropriate, and treat the input checks as a convenience rather than a security boundary. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/bluejoy34/curlsearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text search result snippets and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search engine can be configured with SEARCH_ENGINE; result count can be configured with MAX_RESULTS from 1 to 50.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
