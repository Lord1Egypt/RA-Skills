## Description:

Helps agents find in-network doctors through Zocdoc.com using specialty, condition, insurance, location, visit type, reviews, and real-time appointment availability, then directs users to Zocdoc.com to complete booking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylemorgan-commits](https://clawhub.ai/user/kylemorgan-commits)

### License/Terms of Use:


## Use Case:

External users and care-navigation agents use this skill to search for doctors who accept a user's insurance, compare reviews and appointment availability, and route booking completion through Zocdoc.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches may involve sensitive health, insurance, location, and scheduling preferences.

Mitigation: Share only the minimum information needed for provider search and avoid adding unnecessary personal health details.

Risk: Booking and account steps may require trusted handling of personal information.

Mitigation: Complete booking, authentication, and account actions directly through Zocdoc's trusted site or app.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylemorgan-commits/skills/find-and-book-in-network-doctors)
- [Zocdoc.com](https://www.zocdoc.com/)

## Skill Output:

**Output Type(s):** [text, guidance, links]

**Output Format:** [Structured provider list with booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider name, specialty, accepted insurance confirmation, location, review summary, available appointment slots, visit type, and a Zocdoc.com booking link.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
