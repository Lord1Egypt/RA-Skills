# post.json: plan the posts

```json
{
  "manifest": "captioned/manifest.json",
  "start": "2026-11-23",
  "order": ["speed", "intro"],
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "socialAccountId": "<id>", "output": "vertical",
     "language": "en", "timezone": "America/New_York", "days": ["mon", "wed", "fri"],
     "times": ["18:00"], "privacyLevel": "PUBLIC_TO_EVERYONE"},
    {"name": "Shorts", "platform": "YOUTUBE", "socialAccountId": "<id>", "output": "vertical",
     "language": "en", "privacy": "public", "category": "28", "madeForKids": false},
    {"name": "TikTok ES", "platform": "TIKTOK", "socialAccountId": "<id>", "output": "vertical",
     "language": "es", "timezone": "America/Mexico_City", "privacyLevel": "PUBLIC_TO_EVERYONE"}
  ],
  "posts": {
    "speed": {
      "en": {"text": "Why does a radio call with the ISS last only 10 minutes? ...", "title": "Why a radio call with the ISS lasts 10 minutes"},
      "es": {"text": "¿Por qué una llamada de radio con la Estación Espacial dura solo 10 minutos? ..."}
    }
  }
}
```

- `platform`: TIKTOK, INSTAGRAM, YOUTUBE, FACEBOOK, LINKEDIN (profile), LINKEDIN_PAGES, X,
  THREADS, BLUESKY. `name`: any label, unique.
- `output` and `language` pick which captioned file the account gets. Each account gets every
  video once, at most one a day, in `order`.
- `timezone` (IANA name), `days`, `times` (24-hour, the account's local time).
- TikTok: `privacyLevel` is required and is the user's choice (`PUBLIC_TO_EVERYONE`,
  `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`). Optional `allowComment`,
  `allowDuet`, `allowStitch`, `isBrandedContent`, `isYourBrand`, `isAiGeneratedContent`. Check the
  account's allowed values with `social_accounts_get_platform_inputs`.
- YouTube: `title` in `posts` (100 characters), `privacy` (public, unlisted, private),
  `category` (a number as text, 28 = Science & Technology), and `madeForKids` (true or false):
  the user's answer, never yours. Before an account is connected, a missing answer is a reminder
  in `plan.md`; once it's connected, it's an error.
- Instagram: posting needs a Business or Creator account (free to switch in the Instagram app).
  `isAiGeneratedContent` when it applies.
- Facebook: posts go to a Page.

Post text: say what the video is about in plain words (that's what search reads), one question or
line that makes people watch, 3 to 5 specific hashtags. Write each language natively; don't
machine-translate the text you write for a market.

Two accounts on the same platform with the same video in the same language looks like reposting;
`post_plan.py` warns. Give each account its own language, output or videos.
