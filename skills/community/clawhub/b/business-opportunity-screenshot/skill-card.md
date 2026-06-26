## Description: <br>
Generates a business opportunity Skills report from ClawHub data, opens it in Chromium, and saves a full-page screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JakLiao](https://clawhub.ai/user/JakLiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business analysts can use this skill to create a shareable visual report of business opportunity-related ClawHub skills. It is useful when a lightweight HTML report and screenshot are needed for review or presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell execution can be affected by arbitrary query or output-name text. <br>
Mitigation: Run only in a controlled workspace and avoid passing untrusted or arbitrary input values. <br>
Risk: The script may kill existing Chromium remote-debugging sessions and opens a browser on a debuggable local port. <br>
Mitigation: Close unrelated browser debugging sessions first and run the skill in an isolated browser/workspace environment. <br>
Risk: The skill writes HTML reports and screenshot files locally. <br>
Mitigation: Review the output path and generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JakLiao/business-opportunity-screenshot) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Screenshot Script](artifact/scripts/screenshot.js) <br>


## Skill Output: <br>
**Output Type(s):** [HTML, Files, Screenshots, Shell commands] <br>
**Output Format:** [HTML report file and JPG screenshot, with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an optional search query and output name; saves files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
