# Artsonia endpoints — curl + parser recipes

All paths are relative to `https://www.artsonia.com`. `$JAR` is the cookie
jar from `SKILL.md`'s login step. All parsing functions below are the
MCP's own live-verified `src/parse.ts` (built to `dist/parse.js`) — build
once with `npm install && npm run build` in the repo, then reuse the
`node --input-type=module` one-liner shown per endpoint. Swap in
`grep -oP '(?<=KEY=)\d+'` on the raw HTML instead if you only need an id and
don't want to build the repo.

Shorthand used below: `$REPO` = the absolute path to this clone of
`artsonia-mcp` (e.g. `~/git/artsonia-mcp`); `$ID` = a resolved `artist_id`;
`$ART` = a resolved `artwork_id`.

```sh
# generic shape of every parse call — swap the function name + input path
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseStudents as fn } from '$REPO/dist/parse.js';
console.log(JSON.stringify(fn(readFileSync('/tmp/page.html', 'utf8'))));
" | jq '.'
```

## Reads

### list_students — GET `/members/`

```sh
curl -s -b "$JAR" -c "$JAR" 'https://www.artsonia.com/members/' -o /tmp/dash.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseStudents } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseStudents(readFileSync('/tmp/dash.html','utf8'))));
" | jq -r '.[] | "\(.artist_id)\t\(.name)\t\(.school)\tgrade \(.grade)\t\(.artwork_count) artworks"'
```
Fields: `artist_id`, `name`, `school`, `grade`, `artwork_count`,
`fan_count`, `comment_count`, `feedback_count`, `award_count`,
`portfolio_path`. Selector: `.artist-card`.

### get_activity — GET `/members/` (notifications)

Same fetch as above, different parser:

```sh
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseNotifications } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseNotifications(readFileSync('/tmp/dash.html','utf8'))));
" | jq '.'
```
Shape: `{ count, items: [{ title, body, href }] }`. Selectors:
`.textSubhead` (text `Notifications (N)`) + `div.notice`.

### get_portfolio — GET `/artists/portfolio.asp?id=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" "https://www.artsonia.com/artists/portfolio.asp?id=$ID" -o /tmp/portfolio.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parsePortfolio } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parsePortfolio(readFileSync('/tmp/portfolio.html','utf8'))));
" | jq -r '.[] | "\(.artwork_id)\t\(.is_private)\t\(.thumbnail)"'
```
Fields: `artwork_id`, `is_private`, `thumbnail` (derived
`images.artsonia.com/art/small/<id>.jpg`). Selector: `.grid-item` that
contains an `a[href*="art.asp"]` (the first `.grid-item` is a non-artwork
section header — no art link — and is dropped by that filter).

### get_artwork / list_comments — GET `/museum/art.asp?id=$ART`

```sh
curl -s -b "$JAR" -c "$JAR" "https://www.artsonia.com/museum/art.asp?id=$ART" -o /tmp/artwork.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseArtwork } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseArtwork(readFileSync('/tmp/artwork.html','utf8'))));
" | jq '{title, artist_screen_name, views, grade, project, comments}'
```
Fields: `title`, `artist_screen_name`, `views`, `grade`, `project`,
`comment_entry: {artist_id, artwork_id}|null`, `comments: [{author, text}]`.
`list_comments` is just the `.comments` array from the same fetch.
**Comment-item markup (`.comment`/`.comment-author`/`.comment-text`) is
UNVERIFIED upstream** — both captured accounts had 0 comments, so it
degrades to `[]` without throwing but hasn't been confirmed against a real
comment. Verify against a live artwork with comments before trusting it.

### get_fans — GET `/members/fanclub/?artist=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" "https://www.artsonia.com/members/fanclub/?artist=$ID" -o /tmp/fans.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseFans } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseFans(readFileSync('/tmp/fans.html','utf8'))));
" | jq '.'
```
Fields: `name`, `relationship`. Selector: `.fan-card` (name from the first
`a.hiddenlink`; relationship from the card's own-text div, e.g. "Father" —
the card also carries the fan's email, which the MCP deliberately doesn't
surface).

### get_feedback — GET `/members/feedback/?artist=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" "https://www.artsonia.com/members/feedback/?artist=$ID" -o /tmp/feedback.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseFeedback } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseFeedback(readFileSync('/tmp/feedback.html','utf8'))));
" | jq '[.[] | select(.is_read==false)]'   # unread only
```
Fields: `artwork_id`, `message`, `posted_by`, `is_read` (false while the row
says "has not been marked as read"), `thumbnail`. Selector: `.comment-row`
(message `.comment`, attribution `.commenter`, read state
`.comment-options`).

### get_awards — GET `/artists/awards.asp?id=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" "https://www.artsonia.com/artists/awards.asp?id=$ID" -o /tmp/awards.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseAwards } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseAwards(readFileSync('/tmp/awards.html','utf8'))));
" | jq '[.[] | select(.earned)]'   # earned only
```
Fields: `name`, `earned`, `description`, `progress`,
`period: "current"|"past"`. Selectors: `.award-card` (current year —
name/"Earned"|"Not earned"/criteria/progress) + `.award-card-past`
(prior-year badge icons, name derived from `artist_<name>[_ghosted].gif`).

### get_profile — GET `/members/profile/`

```sh
curl -s -b "$JAR" -c "$JAR" 'https://www.artsonia.com/members/profile/' -o /tmp/profile.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseProfile } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseProfile(readFileSync('/tmp/profile.html','utf8'))));
" | jq '.'
```
Fields: `first_name`, `last_name`, `email`, `mobile`,
`opt_ins: {news, artist_activity, promos}`. Selector: `#TheForm`
(`input[name=...]`/`select[name=...]`).

## Downloads (public CDN, no auth)

```sh
curl -s -o "$ART.jpg" "https://images.artsonia.com/art/full/$ART.jpg"
curl -sI "https://images.artsonia.com/art/full/$ART.jpg" | grep -i last-modified
```
No teacher-entered "created" date exists anywhere in the HTML; the CDN
image's `Last-Modified` header is the real per-artwork date (verified
spanning 2022→2026 on one portfolio). Resolutions: `small` (~11 KB)
`medium` (~34 KB) `large` (~58 KB) `xlarge` (~102 KB) `full`/`original`
(~665 KB). To bulk-download a portfolio: loop `get_portfolio`'s
`artwork_id`s through the CDN curl above. There's no starred/favorited
control on the artwork page for the parent role — don't look for one.

## Writes (POST, form-urlencoded, session-cookie auth, no CSRF)

Every write below: **a 3xx from curl is not proof it persisted** — Artsonia
302s even on a silently-dropped payload. Re-GET the affected page (recipes
above) and diff before trusting it.

### post_comment — POST `/museum/enter.asp?artist=$ID&art=$ART`

```sh
curl -s -b "$JAR" -c "$JAR" -o /tmp/comment-result.html -w '%{http_code}\n' \
  --data-urlencode "Comment=Nice work!" \
  "https://www.artsonia.com/museum/enter.asp?artist=$ID&art=$ART"
```
Body: `Comment=<text>` only. **Not verifiable from the parent side** — the
MCP's live test got a 302 to a content page (not a form bounce) but the
comment never appeared on the public artwork page or the parent comments
view; most likely held for teacher moderation. Treat a 302 here as
"submitted/pending," never "posted."

### invite_fan — POST `/members/fanclub/add.asp?artist=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" -o /tmp/invite-result.html -w '%{http_code}\n' \
  --data-urlencode "MemberType=fan" \
  --data-urlencode "RelationshipID=<relationship-id-from-the-live-Add-Fans-form>" \
  --data-urlencode "FirstName=Test" \
  --data-urlencode "LastName=Fan" \
  --data-urlencode "EmailAddress=test@example.com" \
  --data-urlencode "ArtistID=$ID" \
  "https://www.artsonia.com/members/fanclub/add.asp?artist=$ID"
```
Only test with a real address you're authorized to invite (`@example.com`
for dry testing — it sends a real invite email). `MemberType=fan` is
assumed correct (live-verified by the MCP build); `RelationshipID` is the
`<select>` value from `/members/fanclub/add.asp?artist=$ID`'s live form —
read that page first if you don't already know the code. Add
`--data-urlencode "IsParent=on"` if the fan is also a parent/guardian.
Verify by re-`GET`ting the fan club (`get_fans` above) — a successful
invite shows up as a pending fan.

### mark_feedback_read — POST `/members/feedback/default.asp?artist=$ID`

```sh
curl -s -b "$JAR" -c "$JAR" -o /tmp/mark-read-result.html -w '%{http_code}\n' \
  --data-urlencode "ConfirmAsRead=Mark as Read" \
  "https://www.artsonia.com/members/feedback/default.asp?artist=$ID"
```
Body: `ConfirmAsRead=Mark as Read` only. Marks **all** of the student's
feedback (no per-item control). Verify by re-running `get_feedback` above
and confirming no row has `is_read: false`.

### set_notifications — read `/members/profile/`, POST `/members/profile/default.asp`

This is a read-modify-write of the whole profile form — re-send every
current field, flip only the opt-in(s), never send a password:

```sh
# 1. Read current form values (also needed for every other field below)
curl -s -b "$JAR" -c "$JAR" 'https://www.artsonia.com/members/profile/' -o /tmp/profile.html

# 2. Inspect it to see the *current* value of every input/select in #TheForm
#    (FirstName, LastName, EmailAddress, MobileNumber, MobileCountryCode,
#    Action, EmailAddressPrev, DidChangePassword, OptInNews,
#    OptInArtistActivity, OptInPromos, ...). Checkboxes submit their real
#    `value` attribute (Artsonia uses "Y", never "on") when checked, and are
#    OMITTED entirely when unchecked — exactly like a browser form.
grep -oP '<input[^>]*name="[^"]+"[^>]*>' /tmp/profile.html

# 3. Re-POST every field verbatim EXCEPT: blank OldPassword/NewPassword/
#    NewPassword2, keep DidChangePassword=N, and flip only the opt-in(s)
#    you're changing (include `Field=Y` to turn ON, omit `Field` entirely
#    to turn OFF).
curl -s -b "$JAR" -c "$JAR" -o /tmp/notif-result.html -w '%{http_code}\n' \
  --data-urlencode "FirstName=<current>" \
  --data-urlencode "LastName=<current>" \
  --data-urlencode "EmailAddress=<current>" \
  --data-urlencode "EmailAddressPrev=<current>" \
  --data-urlencode "MobileCountryCode=<current>" \
  --data-urlencode "MobileNumber=<current>" \
  --data-urlencode "Action=<current>" \
  --data-urlencode "DidChangePassword=N" \
  --data-urlencode "OldPassword=" \
  --data-urlencode "NewPassword=" \
  --data-urlencode "NewPassword2=" \
  --data-urlencode "OptInArtistActivity=Y" \
  "https://www.artsonia.com/members/profile/default.asp"
  # (omit OptInNews / OptInPromos entirely here to turn them off)

# 4. Verify: re-fetch the profile and confirm the checkbox state changed
curl -s -b "$JAR" -c "$JAR" 'https://www.artsonia.com/members/profile/' -o /tmp/profile-after.html
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseProfile } from '$REPO/dist/parse.js';
console.log(JSON.stringify(parseProfile(readFileSync('/tmp/profile-after.html','utf8')).opt_ins));
"
```
Field names: `OptInNews`, `OptInArtistActivity` (default checked),
`OptInPromos`. This form also carries password-change fields
(`OldPassword`/`NewPassword`/`NewPassword2`) — always send them blank.
