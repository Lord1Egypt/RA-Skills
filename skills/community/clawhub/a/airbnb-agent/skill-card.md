## Description:

Search Airbnb listings, filter short-term rentals, and analyze detail pages for parking, basement, and renovation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Airbnb rentals by dates, guests, coordinate radius, price, rating, and bedroom count, then compare shortlisted listings. It can also inspect listing detail pages for parking, basement, and renovation signals that should be verified before booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup creates a local Python virtual environment and installs current pip versions of pyairbnb and curl-cffi.

Mitigation: Review the setup script and dependency policy before running setup in a production or managed environment.

Risk: Search and detail commands send dates, guest count, location bounds, currency, language, and listing requests to Airbnb.

Mitigation: Use only search parameters appropriate to share with Airbnb and avoid including unnecessary sensitive information.

Risk: Detail keyword matches for parking, basement, and renovation can be false positives or stale signals.

Mitigation: Verify important amenities and property attributes on the listing page or with the host before booking.

Risk: Default result files are written under /tmp and may be overwritten by later runs.

Mitigation: Use explicit output paths when preserving results or controlling storage location matters.

## Reference(s):

- [Airbnb API Fields Reference](references/api-fields.md)
- [Schema.org](https://schema.org)
- [ClawHub Skill Page](https://clawhub.ai/suidge/skills/airbnb-agent)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search writes /tmp/airbnb_candidates.json and detail analysis writes /tmp/airbnb_results.json by default unless an output path is provided.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
