## Description:

Michelin-grade AI culinary intelligence for Greek recipe consulting, culinary analysis, molecular gastronomy, food cost, HACCP, allergen review, wine pairing, plating, and related kitchen guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send food and recipe questions to an external culinary API and receive structured Greek culinary guidance, including restaurant-style recipe sections, molecular gastronomy analysis, nutrition, allergens, and pairing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User recipe or food-related questions are sent to the external api.neurodoc.app service.

Mitigation: Inform users before the first API call and send only the explicit food or recipe query needed for processing.

Risk: Sensitive personal, credential, medical, private file, or business information could be included in prompts by mistake.

Mitigation: Strip sensitive data before sending requests and avoid submitting credentials, private files, medical information, or sensitive dietary and business data.

Risk: Responses are primarily in Greek, which may limit reviewability for non-Greek readers.

Mitigation: Tell users to expect Greek output and translate or review the response before using it in contexts requiring another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contrario/skills/aetherlang-chef)
- [Publisher profile](https://clawhub.ai/user/contrario)
- [Publisher homepage](https://omnimusmind.com)
- [External API endpoint](https://api.neurodoc.app/aetherlang/execute)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Greek Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typical responses are described as 4000-8000 characters with markdown section headers.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
