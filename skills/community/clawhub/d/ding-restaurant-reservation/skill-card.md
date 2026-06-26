## Description: <br>
DINGs is a managed AI phone assistant that searches restaurants in China and Japan, places automated reservation calls through TripNow/DINGs, and retrieves reservation status, call records, and vouchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallgeding](https://clawhub.ai/user/smallgeding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search supported China and Japan restaurants, collect reservation details, create TripNow/DINGs AI phone booking tasks, and check booking results. It is suited for restaurant reservation workflows that need phone outreach, callbacks, call-record links, and dining voucher URLs. <br>

### Deployment Geography for Use: <br>
China and Japan <br>

## Known Risks and Mitigations: <br>
Risk: Personal booking details and phone numbers are sent to TripNow/DINGs. <br>
Mitigation: Install only when the user trusts the TripNow/DINGs service, collect only booking details needed for the reservation, and avoid retaining those details after the task is complete. <br>
Risk: The skill can initiate automated phone calls for restaurant reservations without a clearly required final consent step. <br>
Mitigation: Before creating a booking call, require explicit user confirmation of the restaurant, date and time, party size, contact phone, preferred language, callback destination, and permission to place the call. <br>
Risk: API keys and callback endpoints can expose sensitive reservation data if shared in URLs or logs. <br>
Mitigation: Store the API key in private configuration, avoid putting credentials in URLs or shared logs, and use a private HTTPS callback endpoint. <br>


## Reference(s): <br>
- [TripNow AI Open Platform](https://tripnowengine.133.cn/tripnow-ai-open-platform/) <br>
- [ClawHub release page](https://clawhub.ai/smallgeding/ding-restaurant-reservation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Text] <br>
**Output Format:** [Markdown guidance with JSON request and response examples, curl commands, and reservation status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIPNOW_API_KEY; supports optional TRIPNOW_BASE_URL and HTTPS CALLBACK_URL; reservation tasks are asynchronous and may return status messages, call-record links, and voucher URLs.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
