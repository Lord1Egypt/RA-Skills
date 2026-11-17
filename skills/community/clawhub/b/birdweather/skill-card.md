## Description:

Query BirdWeather station data for species detections, trends, and comparisons from BirdNET-Pi and PUC bird song detection stations without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxdraki](https://clawhub.ai/user/maxdraki)

### License/Terms of Use:


## Use Case:

Developers, birders, and wildlife monitoring users use this skill to retrieve station information, species detections, recent detections, top species, and period comparisons from public BirdWeather stations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Station IDs, date ranges, limits, and species filters are sent to BirdWeather's public API.

Mitigation: Review command inputs before running the skill and avoid submitting information that should not be disclosed to the public API.

Risk: BirdNET AI classification can misidentify species, especially unusual detections.

Mitigation: Treat detection results and trends as advisory and verify unusual species with supporting observations or source data.

Risk: Empty results can reflect offline stations rather than absence of birds.

Mitigation: Check station status and latest detection metadata before drawing conclusions from empty results.

## Reference(s):

- [BirdWeather station directory](https://app.birdweather.com/)
- [BirdWeather API endpoint](https://app.birdweather.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text summaries with optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses station IDs, date ranges, period selections, limits, and optional species filters; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
