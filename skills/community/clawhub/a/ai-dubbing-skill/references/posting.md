# post.json: plan the posts

```json
{
  "manifest": "dubbed/manifest.json",
  "start": "2026-12-01",
  "order": ["names", "crew"],
  "accounts": [
    {"name": "TikTok ES", "platform": "TIKTOK", "socialAccountId": "<id>", "output": "vertical",
     "language": "es", "timezone": "America/Mexico_City", "days": ["mon", "wed", "fri"],
     "times": ["19:00"], "privacyLevel": "PUBLIC_TO_EVERYONE"},
    {"name": "Shorts ES", "platform": "YOUTUBE", "socialAccountId": "<id>", "output": "vertical",
     "language": "es", "privacy": "public", "category": "28", "madeForKids": false},
    {"name": "Reels BR", "platform": "INSTAGRAM", "socialAccountId": "<id>", "output": "vertical",
     "language": "pt-BR", "timezone": "America/Sao_Paulo"}
  ],
  "posts": {
    "crew": {
      "es": {"text": "La regla de oro de la nave Dragon: no hay que salvar la misión, hay que salvar a la tripulación. #astronauta #nasa #spacex", "title": "La regla de oro de la nave Dragon"},
      "pt-BR": {"text": "A regra de ouro da nave Dragon: não é salvar a missão, é salvar a tripulação. #astronauta #nasa #spacex"}
    }
  }
}
```

- `platform`: TIKTOK, INSTAGRAM, YOUTUBE, FACEBOOK, LINKEDIN (profile), LINKEDIN_PAGES, X,
  THREADS, BLUESKY. `name`: any label, unique.
- `output` and `language` pick which dubbed file the account gets. Each account gets every
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
`post_plan.py` warns. Give each account its own language, output or videos. That is also why a dub
usually goes to its own account per language (a Spanish TikTok next to the English one), not as a
second post on the original account.

Dubbed videos have an AI voice: `post_plan.py` sets `isAiGeneratedContent: true` for TikTok and
Instagram on every dubbed file, whatever the account says, and `plan.md` lists YouTube's "Altered or
synthetic content" answer as a step in YouTube Studio.
