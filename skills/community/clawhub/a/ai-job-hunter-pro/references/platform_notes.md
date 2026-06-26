# Platform Integration Notes

## LinkedIn

- **Easy Apply**: Can be automated via browser control. Requires login session.
- **Rate Limits**: LinkedIn actively detects automation. Recommend max 10 applications/day.
- **Best Practice**: Use `require_confirmation: true` for LinkedIn. Review each application.
- **API**: No public apply API. Use browser automation (Playwright/Puppeteer) through OpenClaw's browser skill.

## Boss直聘 (Boss Zhipin)

- **Approach**: Primary Chinese job platform. Requires mobile verification.
- **Auto-Greet**: Boss supports automated greeting messages. Use sparingly.
- **Rate Limits**: Aggressive anti-bot. Max 5-8 applications/day recommended.
- **Integration**: Web scraping via browser automation. No public API.

## Indeed

- **Easy Apply**: Similar to LinkedIn Easy Apply. More automation-friendly.
- **Rate Limits**: Moderate. 15-20 applications/day is safe.
- **API**: Indeed has a job search API (requires registration). Application submission is browser-based.

## Glassdoor

- **Approach**: Good for salary research and company reviews. Application redirects to company sites.
- **Integration**: Primarily used for job discovery + company research, not direct application.
- **Rate Limits**: Liberal for browsing, standard for applications.

## General Safety Rules

1. **Never exceed 20 total applications/day** across all platforms.
2. **Always start in dry-run mode** to verify behavior.
3. **Rotate timing**: Don't apply to all jobs at once. Spread across the day.
4. **Monitor for blocks**: If a platform returns errors, pause for 24 hours.
5. **Keep sessions fresh**: Rotate cookies/sessions periodically.
6. **Be honest**: Never misrepresent qualifications in any generated content.
