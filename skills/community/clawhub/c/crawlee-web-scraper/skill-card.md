## Description: <br>
Crawlee Web Scraper helps agents scrape single URLs or bulk URL lists with Crawlee-based fallback behavior when standard requests are blocked by rate limits or bot detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BryanTegomoh](https://clawhub.ai/user/BryanTegomoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for authorized scraping of public web pages when standard fetching is blocked or when many URLs need to be processed into structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for web scraping with bot-detection evasion and can be misused against sites that do not permit automated access. <br>
Mitigation: Use only for legitimate, authorized scraping targets, restrict runs to approved domains, and do not use it to bypass sites that prohibit automation. <br>
Risk: The artifact does not define explicit authorization checks or target limits for bulk scraping. <br>
Mitigation: Run it in an isolated environment with reviewed URL lists, enforce local rate and volume limits, and stop jobs that trigger blocking or abuse signals. <br>
Risk: Fetching arbitrary URLs or passing sensitive request context can expose internal locations or confidential data. <br>
Mitigation: Avoid internal URLs and sensitive headers, pin dependencies, and review outputs before sharing or storing scraped content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BryanTegomoh/crawlee-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; scraper scripts return JSON arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Per-URL JSON includes URL, status, fetch timestamp, content length, and either extracted text or an HTML preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
