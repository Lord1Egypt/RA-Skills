## Description:

Provides open source intelligence techniques for CTF challenges. Use when gathering information from public sources, social media, geolocation, DNS records, username enumeration, reverse image search, Google dorking, Wayback Machine, Tor relays, FEC filings, or identifying unknown data like hashes and coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

CTF participants, security learners, and challenge-solving agents use this skill to choose OSINT techniques and commands for authorized CTF or sandbox investigations involving public web, social media, geolocation, media metadata, DNS, archives, and username research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes real-world profiling and geolocation workflows that can expose sensitive information about people or locations.

Mitigation: Use it only for authorized CTF or sandbox targets and avoid targeting real people or their home or work locations.

Risk: Third-party OSINT lookup services may receive target identifiers submitted during research.

Mitigation: Treat each lookup as a disclosure and avoid submitting sensitive identifiers unless the CTF rules and target authorization permit it.

Risk: The security evidence warns against a Discord user-token workflow and pasting personal tokens into shell commands.

Mitigation: Do not use personal Discord tokens or paste credentials into shell commands when following the skill.

Risk: The setup guidance installs Python packages without pinned versions.

Mitigation: Use a virtual environment and pin dependencies before installing packages such as Shodan and Pillow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gandli/skills/ctf-osint)
- [Social Media OSINT](social-media.md)
- [Geolocation and Media Analysis](geolocation-and-media.md)
- [Web and DNS OSINT](web-and-dns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized CTF or sandbox targets, internet access for lookups, and local tools such as bash, Python 3, whois, dig, nmap, exiftool, ImageMagick, curl, Shodan, and Pillow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
