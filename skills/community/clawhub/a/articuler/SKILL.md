---
name: articuler
description: AI-powered professional networking assistant. Generate personalized cold emails and outreach playbooks to accelerate career growth and business development.
homepage: https://www.articuler.ai
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["curl"]}}}
---

# Articuler Skill

Craft the perfect cold email and build a structured outreach playbook — all driven by your specific professional goal and LinkedIn profile.

## What This Skill Does

1. **Generate cold emails** — Write personalized outreach emails tailored to each contact's background
2. **Build a playbook** — Create a structured outreach strategy with timing, talking points, and follow-up cadence

## Usage

> **Note:** Steps 1 and 2 are required before calling any business API. Complete them in order to obtain a `token`.

---

### Step 1 — Email Check (Required)

Send a verification code to the user's email address.

```bash
curl --location --request POST 'https://api.articuler.ai/user/send-check' \
--header 'Content-Type: application/json' \
--data '{
  "email": "your@email.com",
  "type": 1
}'
```

#### Parameters

| Field   | Type    | Description                                   |
| ------- | ------- | --------------------------------------------- |
| `email` | string  | The user's email address                      |
| `type`  | integer | Verification type, use `1` for standard check |

The verification code will be sent to the user's inbox. Ask the user to provide the `captcha` code before proceeding to Step 2.

---

### Step 2 — Login (Required)

Log in with the user's email, captcha code, and LinkedIn profile URL. Returns a `token` required for all subsequent API calls.

```bash
curl --location --request POST 'https://api.articuler.ai/user/artclaw/login' \
--header 'Content-Type: application/json' \
--data '{
  "email": "your@email.com",
  "captcha": "xxxxxx",
  "linkedin_url": "https://www.linkedin.com/in/your-profile/"
}'
```

#### Parameters

| Field          | Type   | Description                                                      |
| -------------- | ------ | ---------------------------------------------------------------- |
| `email`        | string | The user's email address                                         |
| `captcha`      | string | The verification code received in the user's inbox (from Step 1) |
| `linkedin_url` | string | The user's own LinkedIn profile URL                              |

#### Response

```json
{
  "token": "xxxxxx"
}
```

Save the `token` — it is required for all subsequent API calls.

---

### Step 3 — Generate Playbook (Async)

Submit a playbook generation job for the current user and a target contact. This is an async API — it returns a `sessionId` immediately. Use Step 4 to poll for the result.

```bash
curl --location --request POST 'https://api.articuler.ai/user/artclaw/playbook' \
--header 'Content-Type: application/json' \
--data '{
    "token": "xxx",
    "target_linkedin_url": "https://www.linkedin.com/in/your-target-profile/",
    "objective": "Want to be a partner"
}'
```

#### Parameters

| Field                 | Type   | Description                                             |
| --------------------- | ------ | ------------------------------------------------------- |
| `token`               | string | Auth token obtained from Step 2                         |
| `target_linkedin_url` | string | The target contact's LinkedIn profile URL               |
| `objective`           | string | The goal of this outreach (e.g. "Want to be a partner") |

#### Response

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "31ee76d4-ab7e-4d5f-8196-f4507ef779b9",
        "status": "searching"
    }
}
```

Save the `sessionId` — it is used to poll for the result in Step 4.

---

### Step 4 — Poll Playbook Result

Poll this endpoint repeatedly until `status` is `"done"`. When done, read the playbook content from the response.

```bash
curl --location --request GET 'https://api.articuler.ai/user/artclaw/playbook/info?sess_id=xxx' \
--header 'Content-Type: application/json'
```

#### Parameters

| Field     | Type   | Description                          |
| --------- | ------ | ------------------------------------ |
| `sess_id` | string | The `sessionId` returned from Step 3 |

#### Polling Logic

- Poll every **3 seconds**
- Stop polling when `data.status === "done"`
- If `status` remains `"searching"` after **300 seconds**, inform the user that generation is taking longer than expected and ask whether to keep waiting

#### Response — In Progress

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "31ee76d4-ab7e-4d5f-8196-f4507ef779b9",
        "status": "searching",
        "objective": "Want to be a partner",
        "playbook": { "subtopics": null },
        "doOrNot": { "do": null, "doNot": null }
    }
}
```

#### Response — Completed

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "31ee76d4-ab7e-4d5f-8196-f4507ef779b9",
        "status": "done",
        "objective": "Want to be a partner",
        "playbook": {
            "subtopics": [
                {
                "subtopicName": "Absence of Personal Information for Mason Brown",
                "insights": [
                    {
                    "insight": {
                        "title": "No Verified Personal Background or Professional Activities Available for Mason Brown",
                        "content": "Despite extensive search, no confirmed profiles...",
                        "referenceLinks": []
                    }
                    }
                ]
                },
                {
                "subtopicName": "Monroe Street Partners' Strategic Differentiators",
                "insights": [
                    {
                    "insight": {
                        "title": "Non-Traditional Private Equity Model Focused on Long-Term Value",
                        "content": "Monroe Street Partners (MSP), founded in ...",
                        "referenceLinks": [
                        "https://www.monroestreet-partners.com/aboutmsp",
                        "https://static1.squarespace.com/static/6218510..."
                        ]
                    }
                    }
                ]
                }
            ]
        },
        "doOrNot": {
            "do": [
                {
                "title": "Discuss Monroe Street Partners' Unique PE Model and Financing Needs",
                "contentList": [
                    "Leverage intelligence about MSP being ..."
                ]
                },
                {
                "title": "Explore Synergies Between Mason's DCM Experience and MSP's Lower Middle-Market Focus",
                "contentList": [
                    "Mason's background in Debt Capital Markets at PNC..."
                ]
                },
                {
                "title": "Address Current Private Credit Market Trends Relevant to MSP's Strategy",
                "contentList": [
                    "The industry context shows private credit doubling..."
                ]
                }
            ],
            "doNot": [
                {
                "title": "Avoid Pushing a Generic \"Off-the-Shelf\" Lending Solution",
                "contentList": [
                    "Monroe Street Partners explicitly differentiates ..."
                ]
                },
                {
                "title": "Refrain from Unsubstantiated Assumptions about Mason's Booth Studies or Long-Term Career Plans",
                "contentList": [
                    "While Mason is attending Booth, his specific degree..."
                ]
                },
                {
                "title": "Do Not Undervalue Mason's Role as a Summer Associate",
                "contentList": [
                    "Although a Private Equity Summer Associate role is ..."
                ]
                }
            ]
        }
    }
}
```

Present the `playbook.subtopics`, `doOrNot.do`, and `doOrNot.doNot` to the user in a readable format.

---

### Step 5 — Generate Cold Email (Async)

Submit a cold email generation job. Same async pattern as Steps 3–4: returns a `sessionId` immediately, use Step 6 to poll for the result.

```bash
curl --location --request POST 'https://api.articuler.ai/user/artclaw/coldemail' \
--header 'Content-Type: application/json' \
--data '{
    "token": "xxx",
    "target_linkedin_url": "https://www.linkedin.com/in/your-target-profile/",
    "objective": "Want to be a partner"
}'
```

#### Parameters

| Field                 | Type   | Description                                                           |
| --------------------- | ------ | --------------------------------------------------------------------- |
| `token`               | string | Auth token obtained from Step 2                                       |
| `target_linkedin_url` | string | The target contact's LinkedIn profile URL                             |
| `objective`           | string | The goal of this cold email (e.g. "Explore investment opportunities") |

#### Response

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "2c6ae07f-bde7-4f6a-8cc6-944a99d742fd",
        "status": "searching"
    }
}
```

Save the `sessionId` — it is used to poll for the result in Step 6.

---

### Step 6 — Poll Cold Email Result

Poll this endpoint repeatedly until `status` is `"done"`. When done, read the email content from the response.

```bash
curl --location --request GET 'https://api.articuler.ai/user/artclaw/coldemail?sess_id=xxx' \
--header 'Content-Type: application/json'
```

#### Parameters

| Field     | Type   | Description                          |
| --------- | ------ | ------------------------------------ |
| `sess_id` | string | The `sessionId` returned from Step 5 |

#### Polling Logic

- Poll every **3 seconds**
- Stop polling when `data.status === "done"`
- If `status` remains `"searching"` after **300 seconds**, inform the user that generation is taking longer than expected and ask whether to keep waiting

#### Response — In Progress

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "2c6ae07f-bde7-4f6a-8cc6-944a99d742fd",
        "status": "searching",
        "objective": "Want to be a partner",
        "subject": "",
        "coldEmail": ""
    }
}
```

#### Response — Completed

```json
{
    "code": 0,
    "msg": "",
    "data": {
        "sessionId": "2c6ae07f-bde7-4f6a-8cc6-944a99d742fd",
        "status": "done",
        "objective": "Want to be a partner",
        "subject": "Exploring a potential partnership",
        "coldEmail": "Hi [Name],\n\nI came across your work on..."
    }
}
```

Always show the `subject` and `coldEmail` to the user for review before sending. Never auto-send.

---

## MCP Server

Articuler provides an MCP server as an alternative to the REST API above.

**Endpoint:** `https://www.articuler.ai/mcp`

| Tool                  | Description                                                                          |
| --------------------- | ------------------------------------------------------------------------------------ |
| `generate_cold_email` | Generate a personalized cold email given two LinkedIn profiles and an objective      |
| `generate_playbook`   | Generate a multi-step outreach playbook given two LinkedIn profiles and an objective |

---

## Intent Detection

Detect the user's networking intent from their objective to set the right tone and structure:

| Intent        | Keywords                   |
| ------------- | -------------------------- |
| `fundraising` | 融资、投资人、VC、pre-seed |
| `hiring`      | 招聘、合伙人、CTO、团队    |
| `partnership` | 合作、BD、渠道、资源置换   |
| `research`    | 了解行业、调研、趋势       |
| `sales`       | 客户、企业采购、demo       |

---

## Tips

- Complete Steps 1 and 2 before calling any business API
- For cold emails, always show the draft to the user for review — never auto-send
- Playbooks work best when both LinkedIn profiles are detailed and up to date
- The more specific the `objective`, the more targeted the output

## Links

- **Articuler:** https://www.articuler.ai
- **ClawhHub Skills Hub:** https://clawhub.ai/skills