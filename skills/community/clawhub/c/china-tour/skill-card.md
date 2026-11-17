## Description:

AI-powered tour guide with backend API and offline fallback for personalized routes, photo spots, cultural narration for China's scenic spots, and bilingual support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitzhuyong](https://clawhub.ai/user/bitzhuyong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-assistant agents use this skill for single-attraction China tours with personalized routes, photo spot recommendations, cultural narration, and English/Chinese interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-backed answers may send user questions and optional conversation history to an undisclosed unencrypted remote server by default.

Mitigation: Review before installing, use the offline/local fallback or configure CHINATOUR_API_URL to a trusted HTTPS endpoint, and avoid sending sensitive travel plans, family details, or unrelated conversation history.

Risk: Travel details such as opening hours, tickets, and no-photo rules may be outdated or site-specific.

Mitigation: Verify time-sensitive travel information and cultural-heritage restrictions with official sources before travel.

## Reference(s):

- [China Tour ClawHub Skill Page](https://clawhub.ai/bitzhuyong/skills/china-tour)
- [bitzhuyong Publisher Profile](https://clawhub.ai/user/bitzhuyong)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Development Guide](artifact/DEVELOPMENT.md)
- [Forbidden City Attraction Reference](artifact/references/attractions/beijing/forbidden-city.md)
- [Forbidden City Photo Spots](artifact/references/photo-spots/beijing/forbidden-city-spots.md)
- [Forbidden City English Cultural Stories](artifact/references/culture-stories/beijing/forbidden-city-stories-en.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Bilingual Markdown-style conversational guidance with numbered options and occasional helper-script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local fallback data when API access is unavailable; API-backed answers depend on configured endpoint availability.]

## Skill Version(s):

1.1.3 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
