# Evite endpoint reference (curl)

Base host: `https://www.evite.com`. All paths below assume `$JAR` already
holds an authenticated session (see `SKILL.md`'s one-time login) and that
every call passes `-b "$JAR" -c "$JAR"` so a rotated `csrftoken` lands
back in the jar. Reads add `-H 'Accept: application/json'`; writes add
`-H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF"` with `CSRF`
re-read from the jar immediately before the call:

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
```

Transcribed from `evite-mcp`'s `src/client.ts` + `docs/EVITE-API.md`
(live-verified 2026-06-01/02). Every shape below is a REAL captured
request/response unless marked "assumed" (URL captured, body not).

---

## Reads

### 1. List events — `GET /services/events/v1/`

Query: `filterBy` (`all|host|others`, others = you're a guest), `status`
(repeatable — `upcoming|draft|archived|past|canceled`), `type=invitation`,
`offset`, `numResults`, `filter` (free text).

```sh
curl -sS -b "$JAR" -c "$JAR" -H 'Accept: application/json' \
  'https://www.evite.com/services/events/v1/?filterBy=all&type=invitation&status=upcoming&status=draft&numResults=25' \
  | jq '.totals, (.events[] | {id: .event_id, title, start, status, is_host, rsvp})'
```

→ `{ events: Event[], totals }`. `totals` = `{all, sending, draft,
received, canceled, past, upcoming, archived}` (sending = hosting,
received = invited). `Event` fields: `event_id, title, start, end,
status, past, is_host, rsvp(yes|no|maybe), guest_status(0|1|2),
guest_id, host_id, host_name, location{location_name, street_address,
unit_num, city, state, zip_code, place_id}, timezone,
known_timezone_name, template_name, event_category, rsvp_off, is_invite,
is_pending_cohost, rendered_image_url, updated`.

### 2. Get event detail — `GET /services/event/v1/{id}`

```sh
curl -sS -b "$JAR" -c "$JAR" -H 'Accept: application/json' \
  "https://www.evite.com/services/event/v1/$EVENT_ID" \
  | jq '{title: .event.title, start: .event.startDatetime, status: .event.status, settings}'
```

→ top keys: `event, calculatedFields, design, location,
userEventContext, attributes, registries, settings, charity, gifting,
rendered, calendar, features`. `event`: `id, title, message,
startDatetime, endDatetime, knownTimezoneName,
knownTimezoneAbbreviation, eventHostName, eventPhoneNumber, hostId,
hostIds, status, isPast, eventType, category, superCategory,
templateName, origin, isFabricPremium, shareableLink, sendOn`.
`settings`: `enableMaybe, privateGuestList, headCountByFamily, plusOne,
maxEventCapacity, allowViewMap, showGifting, rsvpBy, strictRsvpBy,
enableHostPhotoGallery, enablePhotoSharing, allowGuestNumber, rsvpOff`.

### 3. Guest list + RSVP summary — `GET /services/event/v1/{id}/guests/`

One endpoint powers both `evite_list_guests` and `evite_rsvp_summary`.

```sh
curl -sS -b "$JAR" -c "$JAR" -H 'Accept: application/json' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/guests/" \
  | jq '.summary, (.guests[] | {guestId, name, rsvpResponse, numberOfAdults, numberOfKids})'
```

→ `{ guests: Guest[], summary }`. `Guest`: `guestId, userId, name,
email, phone, guestType(host|cohost|guest),
rsvpResponse(yes|no|maybe|noreply), numberOfAdults, numberOfKids,
checkedIn, comments, deliveryStatus, inviteMethod(email|null),
invitedBy, sentOn, timesViewed, avatarUrl, shortLink, longLink,
created, updated`. `summary`: `{yes, no, maybe, noReply, adultsYes,
kidsYes, adultsMaybe, kidsMaybe, inviteesYes, inviteesMaybe,
lockedStatus}`.

### 4. Messages — `GET /services/event/v1/{id}/posts/`

```sh
curl -sS -b "$JAR" -c "$JAR" -H 'Accept: application/json' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/posts/" | jq '.posts'
```

→ `{ posts: Post[] }` — the event's "Messages" tab thread.

### 5. List templates (HTML scrape, not JSON) — `GET /invites/{category}/`

The gallery is server-rendered — no JSON API. Grep the SSR HTML for
`/invitation/{slug}/(create|preview|details)` links (mirrors
`EviteClient.listTemplates`'s regex). Add `?active_filter=free_premium%2Cfree`
for free-only.

```sh
curl -sS -b "$JAR" -c "$JAR" \
  'https://www.evite.com/invites/kids-birthday/?active_filter=free_premium%2Cfree' \
  | grep -oE '/invitation/[a-z0-9][a-z0-9_-]+/(create|preview|details)' \
  | sed -E 's#/invitation/([a-z0-9_-]+)/.*#\1#' | sort -u
```

Each slug is a `templateName` — pass it to `create_event` below.

---

## Writes

Every write really mutates Evite. `-d` bodies below are exact JSON
unless marked "assumed" (endpoint captured live; the exact body field
wasn't).

### 6. RSVP — `PUT /services/event/v1/{id}/guests/{guestId}`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X PUT \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"rsvpResponse":"yes","numberOfAdults":2,"numberOfKids":0,"comments":"can'\''t wait!"}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/guests/$GUEST_ID"
```

Body: `rsvpResponse` (`yes|no|maybe`), `numberOfAdults`,
`numberOfKids`, optional `comments` — field names match the read
`Guest` shape. `comments` is optional (omit the key entirely to leave
it unchanged).

### 7. Send a private guest message (assumed body) — `POST /tsunami/v1/services/event/{id}/guest/{gid}/messages`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"message":"See you Saturday!"}' \
  "https://www.evite.com/tsunami/v1/services/event/$EVENT_ID/guest/$GUEST_ID/messages"
```

A **third API base** (`/tsunami/`, not `/services/…/posts/`, which is
GET-only). Body assumed `{message}`.

### 8. Broadcast to RSVP segments — `POST /tsunami/v1/services/event/{id}/broadcast/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"message":"Reminder: parking is on the north side!","captcha":null,"virtual_groups":["yes","maybe"],"participantCount":12}' \
  "https://www.evite.com/tsunami/v1/services/event/$EVENT_ID/broadcast/"
```

Body **fully captured** (not assumed): `message`, `captcha` (always
`null`), `virtual_groups` (array of RSVP segments to reach — the
values the dashboard uses are `yes`/`no`/`maybe`), optional
`participantCount` (informational — the count the web UI sends along).
This emails every guest in the named segments.

### 9. Upload a photo to the shared gallery — 4-step Google Cloud Storage flow

The file goes to GCS, not Evite. All 4 steps, in order:

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")

# Step 1 — get a signed-upload ticket from Evite.
TICKET=$(curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d "$(jq -n --arg eid "$EVENT_ID" --arg gid "$GUEST_ID" --arg mt "image/jpeg" \
        '{upload_path:"feed_photos",event_id:$eid,photo_id:"",guest_id:$gid,redirect:true,mimetype:$mt,width:1200,height:900}')" \
  "https://www.evite.com/services/photos/v1/$EVENT_ID/upload/request/")
UPLOAD_URL=$(jq -r '.upload_url' <<<"$TICKET")
PHOTO_ID=$(jq -r '.upload_form.key' <<<"$TICKET" | awk -F/ '{print $NF}')

# Step 2 — multipart POST straight to GCS: signed fields first, `file` LAST,
# no Evite cookies (the policy/signature ARE the auth). Capture the redirect.
FORM_ARGS=()
for k in $(jq -r '.upload_form | keys[]' <<<"$TICKET"); do
  v=$(jq -r --arg k "$k" '.upload_form[$k]' <<<"$TICKET")
  FORM_ARGS+=(-F "$k=$v")
done
FINISH_URL=$(curl -sS -D - -o /dev/null "${FORM_ARGS[@]}" -F "file=@/path/to/photo.jpg" "$UPLOAD_URL" \
  | grep -i '^location:' | tr -d '\r' | awk '{print $2}')

# Step 3 — finalize the object into the album (best-effort; ignore failures).
curl -sS -b "$JAR" -c "$JAR" "$FINISH_URL" -o /dev/null

# Step 4 — register the photo in the event's shared gallery.
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d "$(jq -n --arg pid "$PHOTO_ID" '{photo_ids:[$pid]}')" \
  "https://www.evite.com/services/photos/v1/$EVENT_ID/shared-gallery/?gid=$GUEST_ID"
```

Step 1's mimetype must match the file's real content type; the GCS
policy enforces `Content-Type == mimetype` and a 20 MB cap.

### 10. Create an event — `POST /services/event/v1/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"event":{"title":"Backyard BBQ","startDatetime":"2026-08-15T18:00:00Z","templateName":"camp-confetti_vanilla_kids"}}' \
  'https://www.evite.com/services/event/v1/'
```

Required (Pydantic-enforced): `title`, `startDatetime`, `templateName`
(get a valid slug from endpoint 5). **Quirk**: a successful create
still returns `500 "Unknown error"` (a secondary post-create step
fails) — the draft is created anyway. Treat a 500 here as "possibly
created" and re-list drafts (endpoint 1, `status=draft`) rather than
retrying blindly.

### 11. Update an event — `PATCH /services/event/v1/{id}`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X PATCH \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"event":{"title":"Backyard BBQ — Rain Date"}}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID"
```

Fields MUST be nested under `event` (a bare `{"title":...}` 200s as a
no-op). `PUT` 500s — only `PATCH` works.

### 12. Add draft guests — `POST /ajax/event/{id}/guestlist/draft/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '[{"name":"Ada Lovelace","email":"ada@example.com"}]' \
  "https://www.evite.com/ajax/event/$EVENT_ID/guestlist/draft/"
```

**Legacy `/ajax/` base**, and the body is a **top-level JSON array**
(NOT wrapped in an object) — the server does `for g in payload:
DraftGuest(**g)`. Only persists once the event is finalized (status
`sending`); on a bare `draft` the POST 200s but silently drops the
guest.

### 13. Edit a draft guest — `PATCH /ajax/event/{id}/guestlist/draft/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X PATCH \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"guest_id":"'"$GUEST_ID"'","event_id":"'"$EVENT_ID"'","invite_method":"email","name":"Ada Lovelace","email":"ada@example.com","phone":""}' \
  "https://www.evite.com/ajax/event/$EVENT_ID/guestlist/draft/"
```

Full object every time (`guest_id` selects, the rest are the new
values) — this is a set, not a merge.

### 14. Remove a draft guest — `DELETE /ajax/event/{id}/guestlist/draft/{guestId}`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X DELETE \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  "https://www.evite.com/ajax/event/$EVENT_ID/guestlist/draft/$GUEST_ID"
```

No body, but `src/client.ts`'s `write()` always sends `Content-Type:
application/json` on every write regardless of body presence — include it
here too.

### 15. Send the invitation ("Send now", assumed body) — `POST /services/event/v1/{id}/send/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" -d '{}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/send/"
```

Sends the draft guest list. Body assumed empty — this really emails
every draft guest; test on a throwaway event first.

### 16. Cancel an event (also "delete draft") — `POST /services/event/v1/{id}/actions/cancel/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" -d '{}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/actions/cancel/" \
  -w '\n%{http_code}\n'
```

→ `202 Accepted`. The `/actions/{verb}/` convention for host lifecycle
actions.

### 17. Reinstate a canceled event — `POST /services/event/v1/{id}/actions/reinstate/`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X POST \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" -d '{}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/actions/reinstate/" \
  -w '\n%{http_code}\n'
```

→ `202 Accepted`. Restores a `cancelled` event to `sending`.

### 18. Duplicate an event — `GET /plus/create/{id}/copy/?previous=my_events`

```sh
curl -sS -b "$JAR" -c "$JAR" -D - -o /dev/null \
  "https://www.evite.com/plus/create/$EVENT_ID/copy/?previous=my_events" \
  | grep -i '^location:'
# Location: /invitation/{newId}/customize?...&source_event={id}
```

A plain `GET` that `302`s; the new draft's id is the `/invitation/{newId}/`
path segment of the `Location` header (no request body).

---

## Endpoint count

19 distinct HTTP calls across 3 bases (`/services/`, `/ajax/`,
`/tsunami/`) + 1 external GCS call — mirrors all 6 read tools and 13
write tools evite-mcp exposes (`evite_list_events`, `evite_get_event`,
`evite_list_guests`, `evite_rsvp_summary`, `evite_list_messages`,
`evite_list_templates`, `evite_rsvp`, `evite_send_message`,
`evite_broadcast`, `evite_upload_photo`, `evite_create_event`,
`evite_update_event`, `evite_add_guest`, `evite_update_guest`,
`evite_remove_guest`, `evite_send`, `evite_cancel_event`,
`evite_reinstate_event`, `evite_duplicate_event`).
