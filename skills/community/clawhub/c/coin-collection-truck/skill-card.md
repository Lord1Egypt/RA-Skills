## Description: <br>
Agent skill to search for the Hong Kong Coin Cart (收銀車) locations and schedules when a user asks about coin collection truck location, schedule, or availability by date or district. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sodiasm](https://clawhub.ai/user/sodiasm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer natural language questions about Hong Kong coin collection truck locations, schedules, service suspensions, and district availability. <br>

### Deployment Geography for Use: <br>
Global; the schedule content is specific to Hong Kong. <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script to query bundled schedule data. <br>
Mitigation: Review the script before installation and run it only in an agent environment where local tool execution is expected. <br>
Risk: Answers may become outdated if the bundled Hong Kong coin collection truck schedule data is not refreshed. <br>
Mitigation: Check the data version or refresh the schedule data before relying on answers for current truck availability. <br>


## Reference(s): <br>
- [Coin collection truck schedule data](references/coin_collection_truck_hk.json) <br>
- [Query script](scripts/query_coin_truck.py) <br>
- [ClawHub skill page](https://clawhub.ai/sodiasm/coin-collection-truck) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with schedule details, suspension notes, and Google Maps links; supporting local lookup output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled schedule data and a local Python lookup script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
