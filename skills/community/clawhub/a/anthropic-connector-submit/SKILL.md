---
name: anthropic-connector-submit
description: "Prepare and submit an MCP server to Anthropic's Connectors Directory. Use this skill whenever the user wants to list their MCP server on Claude's connector marketplace, submit to Anthropic's directory, get their MCP server featured in Claude Desktop or claude.ai, or prepare a connector submission. Also triggers on: 'submit to Anthropic', 'Claude connector directory', 'list on Claude marketplace', 'Anthropic MCP submission', 'get listed in Claude connectors', 'MCP directory submission form'. Even if the user just says 'how do I get my MCP server in the Claude directory' or 'I want Claude users to find my server', use this skill."
license: MIT
metadata:
  author: lucaperret
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F4CB"
    homepage: https://github.com/lucaperret/agent-skills
---

# Submit to Anthropic Connectors Directory

Get your MCP server listed alongside Gmail, Notion, and Slack in Claude's official connector marketplace. This covers the complete submission process — from technical requirements to filling out the 6-page form.

## Prerequisites checklist

Before submitting, your server must meet ALL of these. Missing any one will delay or reject your submission.

- [ ] MCP server is live, deployed, and accessible via HTTPS
- [ ] OAuth 2.0 implemented (if auth required)
- [ ] All tools have safety annotations (`readOnlyHint`, `destructiveHint`)
- [ ] All tools have human-readable titles
- [ ] Privacy policy published at a public URL
- [ ] Terms of service published at a public URL
- [ ] Support channel (GitHub issues or email)
- [ ] At least 3 example prompts prepared
- [ ] Test account with sample data ready
- [ ] Server tested end-to-end on Claude Desktop or claude.ai

## The submission form

Submit at: https://docs.google.com/forms/d/e/1FAIpQLSeafJF2NDI7oYx1r8o0ycivCSVLNq92Mpc1FPxMKSw1CzDkqA/viewform

The form has 6 pages. Here's what to put in each field.

### Page 1: Submission Details

**Company Information:**
- **Company/Organization Name** — Your name or company
- **Company/Organization URL** — Your website
- **Primary Contact Name** — Your full name
- **Primary Contact Email** — Your email (reviewers will contact you here)
- **Primary Contact Role** — e.g., "Creator & Maintainer"
- **Anthropic Point of Contact** — Leave blank unless you know someone

**Server Details:**
- **MCP Server Name** — Short name, no "MCP" or "Server" in it (e.g., "Tidal", not "Tidal MCP Server")
- **MCP Server URL** — Select "Universal URL", then enter your endpoint (e.g., `https://example.com/api/mcp`)
- **Tagline** — Max 55 characters. Format: "Verb your thing with Claude" (e.g., "Search, play, and manage your Tidal music library")

**MCP Server Description** (50-100 words, shown in-app):
Template: "[Action] your [service] directly from Claude. [Key capabilities in 2-3 sentences]. [Number] tools covering [categories]. OAuth authentication with your own [service] account."

**Use Cases + Examples** (minimum 3):
Each example should show a realistic user prompt and explain what tools fire. Template:

```
**[Use Case Category]**
"[Realistic user prompt]"
[Which tools are called and what happens, in 1-2 sentences]
```

Good examples show multi-step orchestration — not just single tool calls.

**Connection requirements:**
State what users need (e.g., "Requires a [Service] subscription. Available worldwide.")

**Read/Write Capabilities:** Select "Read + Write" if you have any write tools.

**Is this an MCP App:** Select "No" unless you have interactive UI elements.

**Third-party Connections:** Check what applies:
- "Third-party data retrieval" — if you fetch from an external API
- "Third-party data modification" — if you write to an external API

**Data Handling:** Check all that apply (typically all 4):
- Server only accesses data explicitly requested by user
- No data is stored beyond session requirements
- Data transmission is encrypted (HTTPS/TLS)
- GDPR compliant

**Personal health data:** "No" (unless your service handles health data)

**Categories:** Pick the closest (e.g., "Media & Entertainment", "Business & Productivity")

**Sponsored content:** "No, there is no sponsored content or advertisements"

**Authentication:**
- **Authentication Type:** "OAuth 2.0"
- **Auth Client:** "Dynamic OAuth Client (e.g., DCR, CIMD)"
- **Static Client ID/Secret:** Leave blank for dynamic registration
- **Transport Support:** Check "Streamable HTTP"

**Documentation & Support:**
- **Documentation Link** — Your GitHub repo or docs site
- **Privacy Policy** — URL to your privacy policy page
- **Data Processing Agreement URL** — Leave blank unless you have one
- **Support Channel** — GitHub issues URL or support email

### Page 2: Testing

**Testing Account Credentials:**
If your server requires auth, provide credentials. Recommended: "Test account credentials will be shared via 1Password secure link. Contact [email] to receive the link."

**Test Account Setup Instructions:**
Write clear steps:
```
1. Click "Connect" on the [Name] connector in Claude
2. Log in with the test credentials provided
3. Try: "[example prompt]" to verify
The test account has [what data is pre-loaded]
```

**Test Data Availability:** Check both:
- Test account includes sample data
- All tools can be tested with provided data

**List of tools:**
Comma-separated, format: `tool_name (Human-Readable Name)`

**Tool Titles & Annotations:** Check both:
- I've specified user-friendly titles for all tools
- I've specified accurate tool annotations for all tools

**List of resources:** Leave blank (unless you expose MCP resources)

**List of prompts:** Leave blank (unless you expose MCP prompts, which are optional)

### Page 3: Launch Readiness & Media

**Timeline - Server GA Date:** Today's date (your server should already be live)

**Testing complete:** Check where you've tested:
- Claude.ai (web)
- Claude Desktop

**Server Logo:** Provide your SVG logo URL or upload it. Square, 1:1 aspect ratio.

**Server Logo URL:** Verify that `https://www.google.com/s2/favicons?domain=YOUR_DOMAIN&sz=64` returns your icon. Check the box to confirm.

**Promotional Images:** Upload 3-5 screenshots of your MCP server in use on Claude. Show:
1. A search/discovery interaction
2. A create/write operation
3. A multi-step orchestration

Tips for screenshots:
- Use wide window (1000px+)
- Start conversation with "Respond in English. Format with clear headings and tables."
- Show the tool calls and results clearly

**Link to Promotional Materials:** Optional. Your website URL.

### Page 4: Skills & Plugins (Optional)

If you have a SKILL.md file for Claude Code:
- **Skill Name** — Your skill name
- **Skill Description** — Short description
- **GitHub URL of Skill** — Public repo URL
- **Extra Information** — Mention other marketplaces (ClawHub, skills.sh)

### Page 5: Submission Requirements Checklist

**Policy Compliance** — Check all 5 (all are required):
- I have reviewed and agree to the Software Directory Policy
- My server does NOT enable cross-service automation
- My server does NOT transfer money
- My MCP server is live and ready for production traffic
- I work for the company that owns/controls the API endpoints

Note: The last checkbox is about YOUR MCP server endpoint, not the upstream API.

**Technical Requirements** — Check all 6:
- OAuth 2.0 fully implemented
- All tools include safety annotations
- Server accessible via HTTPS
- CORS configured
- Claude IPs allowlisted (check if behind firewall)
- Tested on latest Claude build

**Documentation Requirements** — Check all 4:
- Documentation published and accessible
- Includes setup instructions and tool descriptions
- Privacy policy published
- Terms of service published

**Testing Requirements** — Check all 3:
- Test account with sample data ready
- Test credentials valid for 30+ days
- All tools functional and tested

**Additional Information:** Optional. Good place to mention:
- Open source status and license
- Where else the server is available (Smithery, ClawHub)
- Any unique value proposition

## After submission

- Anthropic reviews submissions but cannot guarantee inclusion or timeline
- For updates to an existing listing, email mcp-review@anthropic.com
- Check back in 2-3 weeks if no response

## Privacy policy template

Your privacy policy should cover:
- What data is collected (OAuth tokens, user queries)
- Where data is stored (Redis/database, TTL/retention)
- What third-party services are used (upstream API, hosting)
- How to delete data (revoke access, delete session files)
- Contact information

## Terms of service template

Your ToS should cover:
- Service description
- Requirements (subscription needed, acceptable use)
- Disclaimer of warranties ("as is")
- Limitation of liability
- Third-party services and their terms
- Open source license

## Also publish on Smithery

After submitting to Anthropic, also publish on Smithery for immediate distribution:

1. Go to https://smithery.ai/new
2. Enter your MCP server URL
3. Smithery scans tools automatically
4. Configure display name, description, homepage, icon
5. Uncheck "Unlisted" to appear in search

Smithery gives you instant visibility while waiting for Anthropic's review.
