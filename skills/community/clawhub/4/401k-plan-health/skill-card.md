## Description: <br>
Retrieves and assesses a company's retirement plan details from planprovider.pro, including providers, participation, assets, and compliance signals for benchmarking and meeting preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oil-can-man](https://clawhub.ai/user/oil-can-man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advisors, consultants, and sales teams use this skill to research a company's retirement plan from public Form 5500-derived data, evaluate plan health signals, benchmark against peers, and prepare for plan sponsor conversations. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The source data may lag current plan status because Form 5500-derived reporting can be delayed. <br>
Mitigation: Verify the source URL and filing year, and present the filing year as the as-of date. <br>
Risk: Plan details or provider relationships could be misstated if the agent extrapolates beyond the source page. <br>
Mitigation: Report only data that appears in the planprovider.pro markdown response and state when a company is not found. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oil-can-man/401k-plan-health) <br>
- [PlanProvider company directory](https://planprovider.pro/companies) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes company, plan name, EIN if shown, participants, assets, plan type, linked providers, notable health signals, filing year, and source URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
