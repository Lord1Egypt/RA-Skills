## Description: <br>
Searches Eastmoney financial data for timely news, reports, announcements, and policy analysis based on user queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunduanmanbu](https://clawhub.ai/user/yunduanmanbu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis agents use this skill to search Eastmoney for current market news, research reports, announcements, policy analysis, and related securities for a natural-language query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial-search queries are sent to Eastmoney's API. <br>
Mitigation: Avoid confidential, regulated, or proprietary details in queries. <br>
Risk: The artifact includes a default Eastmoney API key path and has credential-management caveats. <br>
Mitigation: Set a user-controlled EASTMONEY_APIKEY where possible instead of relying on the provided default. <br>
Risk: Search results can be saved as eastmoney_news_*.txt files in the working directory. <br>
Mitigation: Run the script from a directory where creating and retaining those result files is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunduanmanbu/eastmoney-finance-news) <br>
- [Eastmoney news-search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Plain text financial-news results with titles, related securities, and core content; optionally saved as local .txt files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to Eastmoney's API and saved files use eastmoney_news_*.txt naming.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
