## Description: <br>
Provides open source intelligence techniques for CTF challenges, including public-source research across social media, geolocation, DNS records, username enumeration, reverse image search, Google dorking, web archives, Tor relays, FEC filings, hashes, and coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, CTF players, and security learners use this skill for authorized OSINT challenge workflows, including social media analysis, geolocation, web and DNS research, archive lookups, metadata extraction, and technical artifact identification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live reconnaissance or de-anonymization beyond an authorized CTF or lab scope. <br>
Mitigation: Use it only for authorized CTF/lab targets and do not probe, identify, or de-anonymize real systems or people without permission. <br>
Risk: Some workflows reference sensitive personal-location signals such as routes, EXIF metadata, IPs, usernames, browser history, and platform profiles. <br>
Mitigation: Treat discovered personal data as sensitive, minimize collection, and avoid retaining or sharing it outside the authorized challenge context. <br>
Risk: Discord/API examples may encourage pasting personal tokens or discovered credentials into commands. <br>
Mitigation: Do not use personal Discord tokens or real credentials; use scoped lab credentials only and redact secrets from notes and outputs. <br>
Risk: Scanner evidence classifies the release as suspicious due to under-scoped guidance around tokens, live reconnaissance, and personal-location research. <br>
Mitigation: Review the guidance before deployment and add local policy constraints for authorization, privacy, and credential handling. <br>


## Reference(s): <br>
- [Ctf Osint on ClawHub](https://clawhub.ai/gandli/ctf-osint) <br>
- [Social Media OSINT](social-media.md) <br>
- [Geolocation and Media Analysis](geolocation-and-media.md) <br>
- [Web and DNS OSINT](web-and-dns.md) <br>
- [WhatIsMyName Username Enumeration](https://whatsmyname.app) <br>
- [Tor Relay Search](https://metrics.torproject.org/rs.html) <br>
- [OpenRailwayMap](https://www.openrailwaymap.org/) <br>
- [Google Plus Codes](https://maps.google.com/pluscodes/) <br>
- [Bluesky Search Documentation](https://bsky.social/about/blog/05-31-2024-search) <br>
- [FEC Campaign Finance Data](https://www.fec.gov/data/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code snippets, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, URLs, API examples, and short code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; internet access and third-party tools may be needed for OSINT lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
