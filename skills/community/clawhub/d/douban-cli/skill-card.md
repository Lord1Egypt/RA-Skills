## Description: <br>
Douban CLI helps agents query Douban movies, books, celebrities, user collections, reviews, and ratings, and run logged-in collection actions through the douban command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Marvae](https://clawhub.ai/user/Marvae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to choose and run Douban CLI commands for movie, book, celebrity, review, rating, and user collection lookup. With user login, it can help export viewing records and perform account actions such as marking, rating, commenting, reviewing, following, or unfollowing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login workflow reads local browser cookies to access Douban. <br>
Mitigation: Install only if the npm package is trusted, ask for explicit confirmation before login, and run logout or remove the auth cache when stored login state is no longer wanted. <br>
Risk: Authenticated commands can make visible changes to a user's Douban account. <br>
Mitigation: Require explicit confirmation before marking, rating, commenting, reviewing, following, unfollowing, exporting, or running batch operations. <br>
Risk: Batch operations can repeatedly call Douban and may trigger anti-abuse controls or unintended bulk changes. <br>
Mitigation: Review input files before execution and use conservative request delays for batch commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Marvae/douban-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Marvae) <br>
- [npm package @marvae24/douban-cli](https://www.npmjs.com/package/@marvae24/douban-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON or CSV command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the douban binary; authenticated workflows may read browser cookies and use local configuration and auth cache files.] <br>

## Skill Version(s): <br>
0.2.5 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
