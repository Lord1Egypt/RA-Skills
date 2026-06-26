## Description: <br>
Measures page performance, cumulative layout shift, theme flicker, and visual stability with Playwright scripts that agents can run before and after changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local browser diagnostics against pages or endpoints they control, compare before and after changes, and identify performance waterfalls, layout shift, and theme flicker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser diagnostics load user-supplied URLs and page content during testing. <br>
Mitigation: Run the scripts only against pages and endpoints you control or are authorized to test, and avoid untrusted URLs or sensitive internal/admin endpoints. <br>
Risk: Theme flicker detection writes screenshots that may capture page content under /tmp. <br>
Mitigation: Avoid running screenshot diagnostics on sensitive pages, and remove temporary screenshot files after review when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/fix-visual-stability-browser-testing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON diagnostic output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled Playwright scripts print measurement JSON to stdout and write flicker screenshots under /tmp.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
