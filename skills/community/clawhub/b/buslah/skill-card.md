## Description:

Get Singapore bus arrivals from a source location to a destination using the trigger "bus from <source> to <destination>".

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhayjb](https://clawhub.ai/user/abhayjb)

### License/Terms of Use:


## Use Case:

External users use this skill to ask for Singapore bus options and live arrival times between a source and destination in natural language.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: Source and destination locations are sent to third-party Singapore transit and geocoding APIs.

Mitigation: Avoid entering sensitive personal locations unless that sharing is acceptable.

Risk: Live bus arrivals depend on external transit APIs and may be unavailable or stale.

Mitigation: Check returned timings against current conditions before relying on them for time-critical travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhayjb/skills/buslah)
- [Project homepage](https://github.com/abhay/arrivelah)
- [OneMap geocode API](https://www.onemap.gov.sg/api/common/elastic/search)
- [BusRouter bus stops data](https://busrouter.sg/data/2/bus-stops.json)
- [BusRouter routes data](https://busrouter.sg/data/2/routes.json)
- [ArriveLah live arrivals API](https://arrivelah2.busrouter.sg)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown with bus arrival details and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bus service numbers, arrival minutes, load indicators, bus type, wheelchair accessibility, stop names, roads, and stop codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
