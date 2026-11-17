## Description:

获取百度首页热搜、小说、电影、电视剧等榜单。当用户说：百度今天热搜榜？热播剧榜单，或类似百度榜单问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and summarize Baidu homepage ranking lists for hot searches, novels, movies, and TV series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Baidu to retrieve public ranking pages.

Mitigation: Review network access expectations before installation and run it only in environments where outbound requests to the source page are acceptable.

Risk: The skill asks users to install Python packages from pip.

Mitigation: Install dependencies in a virtual environment and consider pinning package versions for stricter environments.

Risk: The ranking parser depends on Baidu page structure and may fail if the page changes or rate limits requests.

Mitigation: Review results before relying on them and adjust parsing rules or request frequency if the source page changes or returns errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/baidu-top)
- [Baidu Top ranking source](https://top.baidu.com/board?platform=pc&tab=homepage&sa=pc_index_homepage_all)
- [JisuAPI publisher site](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing ranked Baidu board entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports result limits up to 50 items per board, request timeout configuration, and optional custom User-Agent.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
