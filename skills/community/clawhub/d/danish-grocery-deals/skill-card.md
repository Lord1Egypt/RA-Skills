## Description:

Scrape Danish supermarket weekly tilbudsaviser (Lidl, Rema 1000, Netto, Meny, 365 discount) from the Tjek API and push filtered wow deals to ntfy.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rune-philip](https://clawhub.ai/user/rune-philip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a weekly Danish grocery deal scraper that filters supermarket offers by unit price, discount, and interests, then sends concise ntfy.sh notifications and writes full local deal lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An easy-to-guess public ntfy.sh topic could expose grocery deal notifications to anyone who knows or guesses the topic.

Mitigation: Use a random topic suffix or configure an authenticated ntfy.sh topic before enabling notifications.

Risk: The configuration file can become sensitive if an ntfy.sh token is added.

Mitigation: Treat the runtime config file as sensitive and avoid sharing it after credentials are configured.

Risk: Generated local deal files may retain shopping-interest history in the data directory.

Mitigation: Review or clean the generated data directory if retaining deal history is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rune-philip/skills/danish-grocery-deals)
- [Tjek API base](https://squid-api.tjek.com)
- [ntfy.sh](https://ntfy.sh)
- [Lidl weekly offers](https://etilbudsavis.dk/Lidl)
- [REMA 1000 weekly offers](https://etilbudsavis.dk/REMA-1000)
- [Netto weekly offers](https://etilbudsavis.dk/Netto)
- [Meny weekly offers](https://etilbudsavis.dk/MENY)
- [365 discount weekly offers](https://etilbudsavis.dk/365discount)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and generated plain-text deal summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated local JSON and text deal files, prints a bounded weekly summary, and can send chunked ntfy.sh notifications with an attached full deal list.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
