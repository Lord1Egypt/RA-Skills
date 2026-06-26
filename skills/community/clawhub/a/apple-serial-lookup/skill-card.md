## Description: <br>
Look up Apple device information from a serial number. Supports iPhones, iPads, Macs (MacBook, iMac, Mac mini, Mac Pro, Mac Studio), Apple Watch, Apple TV, and iPods. Use when a user provides an Apple serial number and wants to identify the device, check specs, manufacturing date/location, warranty status, or get detailed model information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siatrial](https://clawhub.ai/user/siatrial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, support staff, and device technicians use this skill to identify Apple hardware from a serial number, decode older serial formats, and find model, manufacturing, specification, or warranty lookup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple serial numbers can be sensitive device identifiers and may be shared with external lookup sources during web-based enrichment. <br>
Mitigation: Only perform web lookups when the user is comfortable sharing the serial number with the selected source, and prefer official Apple Check Coverage for warranty checks. <br>
Risk: Older model-code mappings and third-party specification databases may be incomplete or inaccurate for some regional variants or undocumented codes. <br>
Mitigation: Present uncertain matches as approximate and cross-check important model or warranty conclusions against Apple Check Coverage or another authoritative source. <br>


## Reference(s): <br>
- [Apple Serial Number Formats](references/serial-format.md) <br>
- [Apple Model Code Mappings](references/model-codes.md) <br>
- [EveryMac Ultimate Mac Lookup](https://everymac.com/ultimate-mac-lookup/?search_keywords=SERIAL) <br>
- [Apple Check Coverage](https://checkcoverage.apple.com/) <br>
- [Beetstech Apple Device Lookup](https://beetstech.com/apple-device-lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional JSON output from the bundled decoder script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local serial decode results, model/specification notes, and links or instructions for external warranty and specification lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
