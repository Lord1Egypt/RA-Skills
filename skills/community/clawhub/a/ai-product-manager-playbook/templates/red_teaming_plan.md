# AI Red Teaming Plan Template

Use this template to structure your proactive, adversarial testing of AI systems for vulnerabilities and potential harms before release.

## 1. System Overview
*Describe the AI system being tested, its intended use cases, and the target audience.*
**System Name:** [Insert System Name]
**Intended Use Cases:** [List the primary use cases for the system]
**Target Audience:** [Describe the intended users of the system]

## 2. Threat Model & Risk Assessment
*Identify the potential threats and risks associated with the system.*
**Threat Actors:** [Who might try to exploit the system? e.g., malicious users, competitors, nation-states]
**Potential Harms:** [What are the potential negative consequences of the system? e.g., bias, misinformation, privacy violations]
**Risk Level:** [Assess the overall risk level of the system, e.g., Low, Medium, High, Critical]

## 3. Red Teaming Objectives
*Define the specific goals of the red teaming exercise.*
**Objective 1:** [e.g., Identify vulnerabilities to prompt injection attacks]
**Objective 2:** [e.g., Assess the system's propensity to generate biased or discriminatory content]
**Objective 3:** [e.g., Evaluate the effectiveness of the system's safety guardrails]

## 4. Testing Methodology
*Describe the approach and techniques that will be used for red teaming.*
**Manual Testing:** [Describe the manual testing techniques, e.g., adversarial prompting, role-playing]
**Automated Testing:** [Describe the automated testing tools and scripts, e.g., fuzzing, vulnerability scanners]
**Hybrid Approach:** [Explain how manual and automated testing will be combined]

## 5. Test Scenarios & Attack Vectors
*List the specific test scenarios and attack vectors that will be executed.*
- **Scenario 1:** [e.g., Attempt to bypass safety filters using jailbreak prompts]
- **Scenario 2:** [e.g., Input biased or discriminatory language to test the system's response]
- **Scenario 3:** [e.g., Attempt to extract sensitive information or PII from the system]

## 6. Execution & Reporting
*Outline the plan for executing the tests and reporting the findings.*
**Execution Timeline:** [Provide a schedule for the red teaming exercise]
**Reporting Format:** [Describe the format of the final report, e.g., executive summary, detailed findings, recommendations]
**Remediation Plan:** [Explain how the identified vulnerabilities will be addressed and mitigated]
