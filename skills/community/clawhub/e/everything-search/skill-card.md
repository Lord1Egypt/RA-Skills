## Description: <br>
Everything Windows file search skill for fast HTTP API searches, Chinese and English fuzzy matching, and file type filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steve-shi-web](https://clawhub.ai/user/steve-shi-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows power users use this skill to let an agent query a local Everything HTTP Server, search indexed files and folders, filter by type, size, path, or date, and return matching file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local filenames and full paths from the user's Everything index. <br>
Mitigation: Use it only on machines where the agent is allowed to inspect local file metadata, and avoid sharing raw search or diagnostic output publicly. <br>
Risk: Enabling Everything HTTP Server beyond localhost can expose local file index data over the network. <br>
Mitigation: Keep the server bound to 127.0.0.1 by default, enable remote access only on trusted networks, and use authentication where appropriate. <br>
Risk: The local HTTP server may remain available after the agent task is complete. <br>
Mitigation: Disable the Everything HTTP Server when it is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steve-shi-web/everything-search) <br>
- [Everything official documentation](https://www.voidtools.com/support/everything/) <br>
- [Everything HTTP Server documentation](https://www.voidtools.com/support/everything/http_server/) <br>
- [Everything search commands](https://www.voidtools.com/support/everything/search_commands/) <br>
- [Everything Search API reference](docs/api-reference.md) <br>
- [Everything Search configuration guide](docs/configuration.md) <br>
- [Everything Search troubleshooting guide](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and search result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include local filenames and full paths returned by the user's Everything HTTP Server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
