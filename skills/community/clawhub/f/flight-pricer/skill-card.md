## Description: <br>
Flight Pricer is a command-line tool that searches flight prices through the Duffel API with options for dates, passengers, stops, and cabin class. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrojas537](https://clawhub.ai/user/jrojas537) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to configure a Duffel API key and query flight offers from the command line for specified routes, dates, passenger counts, stop limits, and cabin classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Duffel API key is stored on disk in the user's configuration directory. <br>
Mitigation: Install in a virtual environment, use a least-privilege Duffel key where possible, and check permissions on ~/.config/flight-pricer/config.yaml. <br>
Risk: Unpinned dependencies can reduce supply-chain reproducibility. <br>
Mitigation: Use pinned dependencies or install from a controlled lockfile for environments that require stronger reproducibility. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jrojas537/flight-pricer) <br>
- [Duffel](https://duffel.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Terminal text with human-readable tables and status or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores the Duffel API key in ~/.config/flight-pricer/config.yaml and calls the Duffel flight offer API during searches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
