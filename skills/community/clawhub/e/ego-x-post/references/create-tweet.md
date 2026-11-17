# CreateTweet (verified 2026-11-04)

Source: Ego Lite `page.fetch` against a logged-in x.com session, after a UI Network capture of the same call. Client bundle at capture time: `https://abs.twimg.com/responsive-web/client-web/main.0a76dc3677efe2b2a.js`.

This file is the API contract for `x-post`. Do not invent a different mutation, query id, or body.

## Create text post — verified

`POST https://x.com/i/api/graphql/l4hk8uVGvR-a8kzQ4nOhPA/CreateTweet`

| Piece | Value |
|-------|--------|
| Method | `POST` |
| Path | `/i/api/graphql/{queryId}/CreateTweet` |
| Captured `queryId` | `l4hk8uVGvR-a8kzQ4nOhPA` |
| Bundle marker | `operationName:"CreateTweet"` |

`queryId` rotates when X ships a new `main.*.js`. The script reads the loaded client bundle first and uses this captured id only when that read finds nothing. `--query-id` is for a human to pass a newly captured id. No other query id is shipped.

### Body

Top-level JSON: `variables`, `features`, `queryId` (same id as the path).

`variables` for a text-only post:

| Field | Captured value |
|-------|----------------|
| `tweet_text` | the post text |
| `media` | `{ "media_entities": [], "possibly_sensitive": false }` for text-only. With `--image`, `media_entities` is the list in `references/media-upload.md`. |
| `semantic_annotation_ids` | `[]` |
| `disallowed_reply_options` | `null` (kept; do not drop the key) |
| `semantic_annotation_options` | `{ "source": "UniversalLink" }` |

`features` is the object in `CAPTURED_FEATURES` inside `scripts/lib/pure.mjs`, copied from the UI request. Do not add or remove keys.

The exact text used in the capture was `ego-x-post-capture-ping`. That post was deleted after capture. It is not the smoke text.

### Headers

Sent by `page.fetch` with `credentials: "include"` so the browser attaches `auth_token` (HttpOnly) and `ct0`.

| Header | Notes |
|--------|--------|
| `authorization` | Public web-client bearer (`Bearer AAAA…ANRILg…`). Read it from the loaded bundle when present. Not a user secret. Do not print it next to `ct0`. |
| `x-csrf-token` | Must equal cookie `ct0`. Session secret. Never log it. |
| `x-twitter-auth-type` | `OAuth2Session` |
| `x-twitter-active-user` | `yes` |
| `x-twitter-client-language` | Page language when it looks like `zh-cn` / `en`. Omitted when unknown. |
| `content-type` | `application/json` |
| `referer` | `https://x.com/compose/post` |

Both CreateTweet and CreateNoteTweet now send `x-client-transaction-id`. The skill reads the verification key, `ondemand.s` URL, and `loading-x-anim` from the x.com shell document (`https://x.com/i/jf/`, then home). Script bytes come from the page cache or, in parallel, from Node HTTPS and from the Ego browser (`Network.loadNetworkResource`, then a script tag on the current x.com page). It does not post when any of those materials are missing. `--transaction-id` supplies a value copied from a real UI request. Do not invent one.

Do not set a `Cookie` header. The jar rides along with `credentials: "include"`.

### Success

Envelope: `data.create_tweet.tweet_results.result`.

| Field | Use |
|-------|-----|
| `rest_id` | status id |
| `legacy.id_str` | same id |
| `core.user_results.result.core.screen_name` | screen name |

Public URL: `https://x.com/{screen_name}/status/{rest_id}`.

Captured example (deleted throwaway): `https://x.com/Suchuanyi/status/2117826677376160218`.

If the response has no screen name, the script reads the profile link (`a[data-testid="AppTabBar_Profile_Link"]`, or the anchor labeled 个人资料 / Profile). It does not scrape a random author link out of the timeline.

## Reply — best-effort, not verified

Same CreateTweet URL and body, plus:

```json
"reply": {
  "in_reply_to_tweet_id": "<parent rest_id>",
  "exclude_reply_user_ids": []
}
```

The shape is from the client bundle. A live `page.fetch` reply on 2026-11-04 returned HTTP 200 with GraphQL **226** (`AuthorizationError`, request looked automated). No UI reply was driven. Treat `--reply-to` as best-effort. On 226, stop. Do not click the reply composer and do not retry.

## DeleteTweet — verified, not called

Captured and verified the same day, then left unwired. `cleanup` only closes the local Ego task space. It does not delete a post. Do not call this from `post.mjs`.

`POST https://x.com/i/api/graphql/nxpZCY2K-I6QoFHAHeojFQ/DeleteTweet`

```json
{ "variables": { "tweet_id": "<rest_id>", "dark_request": false }, "queryId": "nxpZCY2K-I6QoFHAHeojFQ" }
```

Success: HTTP 200 `{"data":{"delete_tweet":{"tweet_results":{}}}}`.

## CreateNoteTweet — verified 2026-11-04

Long plain text in `https://x.com/compose/post` uses a different mutation. Articles composer is not required. The client chooses it when the weighted length of `tweet_text` is greater than `maxWeightedTweetLength` (280 in twitter-text v3). Sending that text to CreateTweet returns GraphQL **186**.

`POST https://x.com/i/api/graphql/seOZkIS8AysCGfPo6yYPVA/CreateNoteTweet`

| Piece | Value |
|-------|--------|
| Captured `queryId` | `seOZkIS8AysCGfPo6yYPVA` |
| Bundle marker | `operationName:"CreateNoteTweet"` |
| features | the same 39 keys as CreateTweet in this capture |
| Success envelope | `data.notetweet_create.tweet_results.result` |

`variables` match CreateTweet except the annotation object below. The 2026-11-04 note capture was text-only, so `media` was an empty `media_entities` array. `--image` on a note sends that same `media` object with one entity per image. A note that actually carried an image was not on the wire in that capture. See `references/media-upload.md`.

`variables` match CreateTweet except:

```json
"semantic_annotation_options": { "composition_signal_1": true, "source": "UniversalLink" }
```

`legacy.full_text` is a short preview (capture: 279). The full body is `note_tweet.note_tweet_results.result.text`.

`page.fetch` without `x-client-transaction-id` returned GraphQL **226**. The same body with a transaction id the web client had just produced returned 200. This skill builds that header for the CreateNoteTweet POST. `twitter-site-verification` and `loading-x-anim` come from the Ego document. `ondemand.s` and `main.*.js` URLs are discovered from that document. Bytes already in the page are used first. Otherwise Node HTTPS (up to 4 attempts, backing off after `ECONNRESET` and other transient failures) races the Ego browser: `Network.loadNetworkResource`, then a `<script src>` inserted into the current x.com page whose body is read back from script text, the performance resource list, `Page.getResourceContent`, and `Network.getResponseBody`. A home page right after check-login often has not cached `ondemand.s`; the browser race loads it without opening the composer. `page.fetch` from x.com is CORS-blocked on `abs.twimg.com`. The first source to return bytes wins and the other attempt is aborted. `--transaction-id` passes a value copied from a real UI request. A missing page does not get a made-up id. Do not reuse a header from a different GraphQL call.

Re-read the query id from the loaded `main.*.js`. The captured id is only the fallback.

DeleteTweet (not called by this skill) also deletes notes. There is no separate DeleteNoteTweet in that bundle.

## Smoke

Pro posts the exact string in `SKILL.md` / `SMOKE_TEXT` after the user confirms, with `--yes`. Success is the status URL. Leave that announcement up.
