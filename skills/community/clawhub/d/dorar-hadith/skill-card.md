## Description:

Searches Dorar Hadith for Arabic hadith text or hadith numbers and returns authenticity details such as narrator, source, page number, and grading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m7madash](https://clawhub.ai/user/m7madash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Dorar Hadith from an agent workflow and review hadith text, narrator, source, and authenticity grading before reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted search query could be interpreted as executable Python source by the shell script's current query encoding path.

Mitigation: Review before installing or running, avoid untrusted or automatically generated search strings, and update the script to pass the query to Python as data before production use.

## Reference(s):

- [Dorar Hadith API endpoint](https://dorar.net/dorar_api.json?skey=QUERY&callback=?)
- [Dorar Hadith search](https://dorar.net/hadith/search?q=)
- [ClawHub skill page](https://clawhub.ai/m7madash/skills/dorar-hadith)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text formatted search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include hadith text, narrator, scholar, source, page or number, grading summary, and a Dorar search URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
