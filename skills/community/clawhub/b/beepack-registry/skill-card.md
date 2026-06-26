## Description: <br>
Search Beepack for reusable API packages before coding. Saves tokens and time by reusing production-tested code instead of writing from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[actabi](https://clawhub.ai/user/actabi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search Beepack for reusable JavaScript API packages, inspect package READMEs and feedback, and decide whether to reuse, improve, or publish reusable integration code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feedback or suggestion submissions can send project details to Beepack. <br>
Mitigation: Remove secrets, API keys, internal URLs, proprietary code, customer data, and sensitive business context before submitting feedback or suggestions. <br>
Risk: Third-party package instructions or code returned by Beepack may not match the user's security, licensing, or reliability requirements. <br>
Mitigation: Review package READMEs, feedback, ratings, and code before using a package in a project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/actabi/beepack-registry) <br>
- [Beepack homepage](https://beepack.ai) <br>
- [Beepack search API](https://beepack.ai/api/v1/search?q=what+you+need) <br>
- [Beepack package detail API](https://beepack.ai/api/v1/packages/{slug}) <br>
- [Beepack package feedback API](https://beepack.ai/api/v1/packages/{slug}/feedback) <br>
- [Beepack package suggestions API](https://beepack.ai/api/v1/packages/{slug}/suggestions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Code] <br>
**Output Format:** [Markdown guidance with HTTP request examples and package README content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party Beepack package instructions, package feedback, and reusable JavaScript module code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
