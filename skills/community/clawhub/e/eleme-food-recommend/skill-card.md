## Description: <br>
Recommends nearby Ele.me food delivery items based on meal times, flavor preferences, and location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Du425](https://clawhub.ai/user/Du425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal automation agents use this skill to configure Ele.me account, meal-time, taste, and location settings, then request nearby food delivery recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live Ele.me cookie may grant account access if exposed. <br>
Mitigation: Use only when comfortable sharing that cookie with the skill, avoid passing secrets where they may be logged or saved in shell history, and rotate or remove the cookie after use. <br>
Risk: The skill stores the Ele.me cookie and precise location in plaintext local configuration. <br>
Mitigation: Run only on trusted machines, restrict access to the configuration directory, avoid shared accounts or shared hosts, and delete the stored configuration when no longer needed. <br>
Risk: TLS certificate verification is disabled in the Ele.me API helper. <br>
Mitigation: Prefer a version that keeps default TLS verification enabled; until then, avoid using the skill on untrusted networks. <br>
Risk: Recommendation quality and availability depend on Ele.me endpoints and account state. <br>
Mitigation: Treat recommendations as convenience output, review results before acting, and expect failures when the cookie, location, or service response changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Du425/eleme-food-recommend) <br>
- [Declared project homepage](https://github.com/your-name/eleme-food-recommend) <br>
- [Ele.me](https://www.ele.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON responses printed to stdout with CLI command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendation responses can include meal type, flavor, restaurant count, and food item metadata; configuration commands handle cookie, meal times, flavor, count, and location.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
