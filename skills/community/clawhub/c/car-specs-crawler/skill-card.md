## Description: <br>
Fetch car specifications from Chinese automotive websites (懂车帝 dongchedi.com and 汽车之家 autohome.com.cn). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect vehicle configuration data from dongchedi.com and autohome.com.cn for comparison reports, presentations, or spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler makes web requests to dongchedi.com and autohome.com.cn. <br>
Mitigation: Install and run it only when those outbound requests are acceptable for the user's environment. <br>
Risk: The optional --output path can write a local JSON file. <br>
Mitigation: Choose the output path deliberately to avoid overwriting an unintended file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/car-specs-crawler) <br>
- [Dongchedi](https://www.dongchedi.com) <br>
- [Autohome](https://car.autohome.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files] <br>
**Output Format:** [Markdown tables or JSON written to stdout, with optional JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires requests and lxml; makes web requests to the selected automotive sites and can save JSON when --output is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
