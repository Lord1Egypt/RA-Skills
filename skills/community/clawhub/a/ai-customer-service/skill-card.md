## Description: <br>
Builds AI-powered customer service knowledge bases by extracting FAQs from local documents or website URLs, testing answer matching, and exporting results in common formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and small-business support teams use this skill to turn FAQ documents or help pages into a local customer-service knowledge base and test automated replies before use with customers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI can read user-selected files and write to user-selected output paths. <br>
Mitigation: Run it only on intended FAQ sources, avoid sensitive files, and choose output paths that will not overwrite important data. <br>
Risk: Generated or matched answers may be incomplete or misleading for customer support use. <br>
Mitigation: Review the generated knowledge base and test replies before publishing or connecting them to customer-facing workflows. <br>
Risk: Website scraping depends on the URL provided by the user and the code does not enforce site permissions. <br>
Mitigation: Confirm site permissions and robots.txt expectations before scraping external help pages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dagangtj/ai-customer-service) <br>
- [Publisher Profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, CSV, or Markdown knowledge-base files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js CLI that reads user-selected files or URLs and writes user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
