## Description: <br>
Use when users need Pengleni beauty assistant capabilities via SMS login/session APIs, including AI virtual try-on, makeup analysis, style transfer, product recommendation, and beauty knowledge Q&A with HTML message exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayleethu](https://clawhub.ai/user/rayleethu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to authenticate with Pengleni by phone/SMS, create or resume a session, and ask beauty-assistant questions for virtual try-on, makeup analysis, style transfer, product recommendations, and beauty knowledge Q&A. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a service token, SMS verification code, and local session file. <br>
Mitigation: Keep credentials and .session.json private, delete the session file when no longer needed, and prompt re-login on authorization failures. <br>
Risk: Misconfigured service URLs could send authentication or session traffic to the wrong endpoint. <br>
Mitigation: Verify SITE_BASE_URL and API_BASE_URL before use and keep them aligned with the intended Pengleni service. <br>
Risk: User-provided HTML or rich text can carry unsafe content if passed through without filtering. <br>
Mitigation: Apply the documented HTML allow-list, block script-like and form-related tags, and prefer escaped text payloads when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rayleethu/cosmetics-advisor-pengleni) <br>
- [Publisher Profile](https://clawhub.ai/user/rayleethu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python client usage, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return answer_text for plain responses or answer_html when rich text is requested.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
