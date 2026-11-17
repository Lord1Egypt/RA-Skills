## Description:

Analyze brands to generate comprehensive brand identity profiles (JSON). Use when the user wants to analyze a brand, create a brand profile, or needs brand data for ad generation. Stores profiles for reuse across Ad-Ready, Morpheus, and other creative workflows. Can list existing profiles and update them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers and creative workflow operators use this skill to research a brand with Gemini Flash and Google Search grounding, then generate a structured JSON brand identity profile for ad generation and related creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names and prompts are sent to Gemini and Google Search.

Mitigation: Avoid confidential unreleased brands and install only when this data sharing is acceptable.

Risk: AI-generated web research may be reused in downstream creative workflows without enough validation.

Mitigation: Review generated brand profiles before using them in ad generation or other AI workflows.

Risk: Auto-save can write generated profiles into the Ad-Ready brand catalog.

Mitigation: Back up or review catalog files before using --auto-save.

Risk: The script declares a broad google-genai dependency range.

Mitigation: Pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/ai-brand-analyzer)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON brand identity profile, optionally saved as a file or printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GEMINI_API_KEY or --api-key and can auto-save profiles to an Ad-Ready brand catalog.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
