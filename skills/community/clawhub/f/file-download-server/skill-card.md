## Description: <br>
快速搭建临时 HTTP 文件下载服务器，支持生成下载页面、启动下载服务和开放指定防火墙端口。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtafersit1-png](https://clawhub.ai/user/mtafersit1-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create short-lived HTTP download links for files or folders when a chat or workflow cannot transfer the files directly. It is intended for deliberate temporary sharing of selected files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a local folder over unauthenticated HTTP. <br>
Mitigation: Use a dedicated folder that contains only files intended for sharing, prefer localhost unless external access is required, and stop the server after the transfer. <br>
Risk: The skill can automatically open firewall ports. <br>
Mitigation: Run the port-opening behavior only when network exposure is intended, track the opened port, and manually remove the firewall rule after use. <br>
Risk: Generated download pages can include filenames, titles, or descriptions supplied by the operator. <br>
Mitigation: Avoid untrusted filenames and descriptions, and review the generated page before sharing the link externally. <br>


## Reference(s): <br>
- [Quickstart](references/QUICKSTART.md) <br>
- [Python http.server documentation](https://docs.python.org/3/library/http.server.html) <br>
- [iptables project](https://netfilter.org/projects/iptables/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and code snippets; generated HTML download pages when the bundled scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a background HTTP server and change local firewall rules when the operator runs the relevant scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
