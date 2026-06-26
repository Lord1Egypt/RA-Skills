## Description: <br>
Performs a three-part customer compliance background check covering OFAC sanctions name and address searches, BIS/eCFR restricted-address keyword checks, and a drafted internal export-data follow-up message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittymi](https://clawhub.ai/user/kittymi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees use this skill to run an initial customer compliance screen, document OFAC and eCFR lookup results, flag possible matches for manual review, and draft a Dora or Shellen follow-up request for export-data checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer names and address keywords are entered into public government lookup pages. <br>
Mitigation: Use only customer information the user is comfortable querying publicly, and make clear which keywords were searched. <br>
Risk: No-result lookup pages can be mistaken for a final compliance clearance. <br>
Mitigation: Treat results as an initial screen only, report the exact lookup terms used, and avoid absolute compliance conclusions. <br>
Risk: Possible OFAC or eCFR matches may be false positives or require context outside the page result. <br>
Mitigation: Record candidate names, addresses, scores, and nearby context, then require manual review for any possible match. <br>
Risk: A drafted follow-up message could be sent before the user has checked it. <br>
Mitigation: Confirm explicitly before sending any message to Dora, Shellen, or another recipient, and do not invent export-data conclusions. <br>


## Reference(s): <br>
- [OFAC Sanctions List Search](https://sanctionssearch.ofac.treas.gov/) <br>
- [eCFR Supplement No. 4 to Part 744](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-744/appendix-Supplement%20No.%204%20to%20Part%20744) <br>
- [Customer Background Check Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with lookup findings, review notes, and drafted follow-up message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes actual search keywords, whether follow-up retries were attempted, and manual-review status for possible matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
