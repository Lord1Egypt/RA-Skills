## Description: <br>
Provides web, news, and image search through 360 Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiyang2007](https://clawhub.ai/user/feiyang2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve web, news, and image search results from 360 Search for query-driven research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to an external search provider. <br>
Mitigation: Do not submit secrets, credentials, private customer data, or sensitive internal terms through this skill. <br>
Risk: The skill relies on Playwright and browser dependencies while its package documentation is incomplete. <br>
Mitigation: Install and run it only in an environment where those dependencies can be reviewed, pinned, and isolated before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feiyang2007/360-search) <br>
- [360 Search](https://www.so.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search result arrays and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, links, snippets, source labels, timestamps, and image URLs depending on the search mode.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
