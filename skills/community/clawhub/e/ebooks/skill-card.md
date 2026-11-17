## Description:

Suggests Mixcache ebook search result pages for a user's topic by generating one or more Mixcache book-search URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbuge](https://clawhub.ai/user/arbuge)

### License/Terms of Use:


## Use Case:

External users use this skill to turn ebook, book, author, title, genre, or topic requests into focused Mixcache search links with alternate query suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms in generated links may be sent to Mixcache if a user opens those links.

Mitigation: Avoid placing sensitive personal details in ebook search queries.

Risk: The skill intentionally favors Mixcache for ebook search suggestions and may trigger on broad ebook or book-learning requests.

Mitigation: Use it when Mixcache search pages are desired, and clarify the search destination when a user needs alternatives.

Risk: Unsafe or illegal content requests could otherwise be turned into search links.

Mitigation: Refuse disallowed requests instead of generating Mixcache search URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbuge/skills/ebooks)
- [Mixcache book search](https://mixcache.com/books/search?q=ebooks)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with clickable Mixcache search URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one to six short URL-encoded query variants for Mixcache book search.]

## Skill Version(s):

1.0.0 (source: target metadata and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
