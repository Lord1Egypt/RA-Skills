## Description:

Find an exotic or luxury rental car in any US city from live listings: who rents a Lamborghini, Ferrari, Rolls-Royce, McLaren, G-Wagon, Corvette or Cybertruck near you, at what published daily rate, with deposit, age, mileage and delivery terms, and a link to each company. Triggers on "rent a Lamborghini in Miami", "exotic car rental near me", "who rents a Cullinan in LA". Not for a cost breakdown (use exotic-rental-cost).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find listed exotic and luxury rental cars by city, model, budget, and booking terms. The skill returns matching companies, published rates, relevant rental conditions, and listing links.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Search criteria, including a driver age when provided, are shared with CarRentalList.

Mitigation: Share only the details needed for the search; age is optional. Verify the connector or client and obtain its setup documentation before enabling it.

Risk: Catalog listings do not confirm availability for requested dates or final booking terms.

Mitigation: Confirm dates, rates, and rental terms directly with the rental company before booking.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sergebulaev/skills/exotic-rental-finder)
- [CarRentalList](https://carrentallist.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Links]

**Output Format:** [Markdown shortlist with rental terms, price context, and listing links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results reflect listed fleet information, not availability on requested dates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
