## Description:

Use DeepEvidence for evidence-based clinical questions, including guideline interpretation, drug safety and interactions, dose adjustment, clinical-trial evidence, medical literature, and supported medical-image analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindy8753](https://clawhub.ai/user/cindy8753)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, clinical informatics teams, and developers use this skill to query DeepEvidence for literature-backed clinical reference on guidelines, medication safety, dose adjustment, clinical studies, and authorized medical-image analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical questions and image URLs are sent to an external DeepEvidence service and may contain sensitive patient information.

Mitigation: Use only authorized clinical content, avoid PHI/PII unless consent, contracts, and compliance controls are in place, and keep DEEPEVIDENCE_API_KEY in the environment.

Risk: Users may treat DeepEvidence output as diagnosis, treatment instruction, or emergency triage.

Mitigation: Present results as clinical reference only, advise immediate local emergency care for urgent symptoms, and require clinician verification against original literature and current guidelines.

Risk: Failed, empty, or timed-out retrieval can be mistaken for absence of medical risk or evidence.

Mitigation: Use the documented failure message and do not interpret retrieval failures as no risk or no evidence.

Risk: Authenticated requests may be exposed through cross-origin redirects in the helper's HTTP path.

Mitigation: Harden or wrap the helper to reject cross-origin redirects for authenticated requests.

## Reference(s):

- [DeepEvidence ClawHub Skill Page](https://clawhub.ai/cindy8753/skills/deepevidence)
- [DeepEvidence Public API Documentation](https://deepevid.medsci.cn/platform/docs)
- [DeepEvidence API Keys](https://deepevid.medsci.cn/platform/api-keys)
- [DeepEvidence Public API Reference](references/api.md)
- [DeepEvidence Safety Reference](references/safety.md)
- [DeepEvidence Error Handling](references/errors.md)
- [DeepEvidence Integration Examples](references/integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell examples; successful API helper calls return clinical answer text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve DeepEvidence citation markers and present responses as clinical reference, not diagnosis or treatment instruction.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
