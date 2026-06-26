## Description: <br>
Guide travelers through international airport transit connections step-by-step with Chinese-language instructions, terminal maps/photos, live queue or crowd signals when available, and baggage re-check confirmation using baggage tags/receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to generate Simplified Chinese airport transfer action cards for international connections, including immigration, terminal changes, baggage re-check decisions, queue signals, maps, and delay response steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Visa, immigration, baggage-through, and missed-connection decisions can materially affect a traveler if public data is incomplete or stale. <br>
Mitigation: Verify critical decisions with the airline, airport, border authority, or official counter before relying on the action card. <br>
Risk: The data-fetching script contacts public airport and travel websites, saves local JSON output, and may create screenshots when Chrome is available. <br>
Mitigation: Review generated sources and timestamps, and run the script only when outbound HTTPS access and local file output are acceptable. <br>


## Reference(s): <br>
- [Airport Transfer Guide on ClawHub](https://clawhub.ai/tinayunyunyun/airport-transfer-guide) <br>
- [Transit Context Guide](references/transit_context_guide.md) <br>
- [Airport Registry](references/airport_registry.json) <br>
- [iFly terminal maps](https://www.ifly.com/airports/{slug}-airport/terminal-map) <br>
- [FlightQueue airport wait times](https://flightqueue.com/airport/{code}) <br>
- [Flightradar24 airport boards](https://www.flightradar24.com/data/airports/{code_lower}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Simplified Chinese Markdown action cards with tables, ordered steps, image links, source timestamps, and optional JSON data-fetching output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run a local Python script that contacts public airport and travel websites and saves a local transit_context.json file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
