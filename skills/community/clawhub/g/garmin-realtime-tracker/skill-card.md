## Description: <br>
Facilitates real-time tracking and automated data delivery from Garmin devices for live location, activity data, and sensor streams from Garmin wearables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kritsanan1](https://clawhub.ai/user/kritsanan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integrators use this skill to compare Garmin real-time and near-real-time data access approaches and choose an integration path for location, activity, or sensor-data delivery. It is most useful when planning official Garmin Connect IQ, Garmin Health SDK, or Garmin Connect API workflows and understanding the risks of unofficial LiveTrack approaches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live location, activity, and health data can reveal sensitive personal information if collected or shared without proper controls. <br>
Mitigation: Use the skill only with informed consent, collect only necessary data, send it only to trusted destinations over secure transport, and define retention and sharing rules before deployment. <br>
Risk: Unofficial LiveTrack approaches may be unstable, unsupported, or dependent on session tokens and reverse-engineered behavior. <br>
Mitigation: Prefer official Garmin Connect IQ, Garmin Health SDK, or Garmin Connect API options for operational systems, and reserve unofficial LiveTrack methods for non-critical personal or experimental use. <br>


## Reference(s): <br>
- [Garmin Connect IQ Positioning](https://developer.garmin.com/connect-iq/core-topics/positioning) <br>
- [Garmin Connect IQ ActivityMonitor.Info](https://developer.garmin.com/connect-iq/api-docs/Toybox/ActivityMonitor/Info.html) <br>
- [Garmin Connect Developer Program Overview](https://developer.garmin.com/gc-developer-program/overview/) <br>
- [Garmin Connect Activity API](https://developer.garmin.com/gc-developer-program/activity-api/) <br>
- [Garmin Connect Health API](https://developer.garmin.com/gc-developer-program/health-api/) <br>
- [Garmin Health SDK Overview](https://developer.garmin.com/health-sdk/overview/) <br>
- [renarsvilnis/garmin-livetrack](https://github.com/renarsvilnis/garmin-livetrack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with technical recommendations and example code or configuration when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May discuss sensitive live location or health-data sharing; outputs should be reviewed before operational use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
