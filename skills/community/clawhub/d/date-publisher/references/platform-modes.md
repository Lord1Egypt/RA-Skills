# Platform Modes

Classify a target before taking any action. Do not claim a platform supports automated publishing until an official integration is configured and the user has authorized it.

| Mode | Examples | Agent action |
| --- | --- | --- |
| Registry | showme-registry | Prepare JSON and an owner-approved GitHub PR. |
| Static page | GitHub Pages, owner-controlled site | Build/deploy only after the owner authorizes that site and deployment account. |
| Community post | GitHub Discussions, social/community account | Draft text and links; the owner confirms each post. |
| Official API | A platform with a documented write API and owner OAuth | Explain the scope, receive explicit confirmation, then call the official API. |
| Manual-only dating app | Any app without an approved API or with anti-bot controls | Provide a copy-ready draft and setup checklist. Do not create accounts, automate UI, swipe, or message. |

## Distribution Log Fields

Keep the log local or in the user's chosen private workspace:

```json
{
  "target": "github-registry",
  "public_url": "https://github.com/example/repo/pull/123",
  "published_at": "2026-09-16T00:00:00.000Z",
  "approved_fields": ["name", "city", "bio", "tags", "contact.email"],
  "status": "published"
}
```

Never put an access token, password, recovery code, or private message in this log.
