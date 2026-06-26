## Description: <br>
ClawFlight searches flight offers, filters for Starlink-equipped airlines, ranks results by WiFi quality, price, duration, or jet-lag friendliness, and returns booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assistant-design](https://clawhub.ai/user/assistant-design) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-focused agents use ClawFlight to search routes where in-flight internet matters, compare Starlink-equipped flight options, and save or rate flights after travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight searches are sent to Amadeus and booking-provider links may disclose route, date, and passenger-search intent. <br>
Mitigation: Use a dedicated Amadeus API key, avoid sensitive searches on untrusted systems, and review booking links before opening or sharing them. <br>
Risk: The skill can save trip-related data, user ratings, and an Amadeus token cache in local JSON files. <br>
Mitigation: Keep the data directory private, restrict filesystem permissions, and delete saved-flight, ratings, or token-cache files when they are no longer needed. <br>
Risk: Starlink fleet coverage and community WiFi ratings are approximate and may not match the aircraft assigned to a specific flight. <br>
Mitigation: Treat rankings as decision support, verify aircraft and connectivity details with the airline before booking, and avoid relying on the WiFi score as a guarantee. <br>
Risk: The skill text includes a Kiwi API key setup instruction that the security guidance says appears unnecessary for this version. <br>
Mitigation: Configure only the Amadeus credentials required by this implementation unless a future version explicitly uses a Kiwi API integration. <br>


## Reference(s): <br>
- [ClawFlight ClawHub release page](https://clawhub.ai/assistant-design/clawflight) <br>
- [Amadeus Self-Service API portal](https://developers.amadeus.com/self-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output or pretty-printed JSON; setup and usage guidance in Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include ranked flight options and booking links; save and rate commands may write local JSON data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
