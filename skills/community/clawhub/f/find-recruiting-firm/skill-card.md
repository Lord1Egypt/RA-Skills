## Description: <br>
Find, shortlist, vet, and enrich US recruiting and staffing firms through the ServiceGraph pro_services dataset, including executive search, RPO, contingent staffing, temp staffing, and vertical specializations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nostrband](https://clawhub.ai/user/nostrband) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting, talent, procurement, and operations teams use this skill to find external US recruiting or staffing firms and decide which firms to shortlist or enrich. It is for procuring agencies and firms, not for hiring in-house recruiters, posting jobs, candidate career help, or non-US firm searches. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: ServiceGraph API credentials could be exposed if users paste tokens into chat or load environment files into the model context. <br>
Mitigation: Keep SERVICEGRAPH_API_KEY in the shell or harness environment and prompt users to add the key locally instead of sharing it in conversation. <br>
Risk: Unlocking detailed firm records can spend ServiceGraph credits. <br>
Mitigation: Show the selected firm list and expected credit cost before approving unlock requests. <br>
Risk: Searches can drift outside the intended recruiting-firm procurement scope. <br>
Mitigation: Pin industry:hr_recruiting_staffing and decline candidate-side, in-house hiring, job-posting, and non-US firm requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nostrband/find-recruiting-firm) <br>
- [ServiceGraph API](https://api.servicegraph.co) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and concise shortlist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the pro_services dataset and requires a SERVICEGRAPH_API_KEY for authenticated ServiceGraph calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata; artifact frontmatter says 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
