## Description: <br>
Control local Chrome browser via Chrome DevTools Protocol (CDP) using Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiaolin](https://clawhub.ai/user/hanxiaolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to drive a local Chrome session for browser navigation, form interaction, screenshots, JavaScript evaluation, web scraping, testing, and network-response inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live Chrome session, including authenticated pages in the connected browser. <br>
Mitigation: Use a dedicated temporary Chrome profile with no important logins, and keep the remote debugging endpoint local and short-lived. <br>
Risk: Network interception and JavaScript evaluation can expose sensitive page data or produce misleading automation results. <br>
Mitigation: Limit interception to intended sites and patterns, review captured output before use, and avoid running untrusted scripts against sensitive pages. <br>
Risk: File upload support can pass local files into web pages when command JSON includes file paths. <br>
Mitigation: Provide only paths that are intentionally meant for upload, and review command files before execution. <br>


## Reference(s): <br>
- [Chrome remote debugging setup](references/chrome-setup.md) <br>
- [CDP controller usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON command sequences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute browser actions through Puppeteer and return structured JSON results from command runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
