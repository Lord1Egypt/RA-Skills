## Description: <br>
Query China domestic transport options through one skill for domestic flight or high-speed rail results, departure and arrival times, stations or airports, airline or train details, and public reference fares from open web sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baizhexue](https://clawhub.ai/user/baizhexue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to look up China domestic flight and high-speed rail options, including times, route details, filters, and public reference fares. It is intended for travel planning support, not ticket purchase or checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious because the skill has unsafe parsing and weakened HTTPS checks. <br>
Mitigation: Install only after reviewing these implementation risks; prefer a version that removes eval-based parsing and restores normal HTTPS certificate verification before routine travel searches. <br>
Risk: Queries send itinerary details to Tongcheng and 12306 public services. <br>
Mitigation: Use only when sharing departure, destination, date, and filter details with those public providers is acceptable. <br>
Risk: Public web pages, fares, availability, and endpoint structures can change or differ from checkout results. <br>
Mitigation: Treat returned prices and availability as planning references and verify final details with the provider before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baizhexue/fly-flight) <br>
- [Provider public web notes](references/provider-public-web.md) <br>
- [Tongcheng public flight pages](https://www.ly.com/flights/) <br>
- [12306 public train endpoints](https://kyfw.12306.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON transport-result payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include public reference prices, route timing, station or airport details, transport mode, provider, trip type, outbound options, and optional return options.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
