# AlphaPortal endpoint reference (curl)

Base: `https://api.alpharoute.app`. Auth: `Authorization: Bearer $ALPHAPORTAL_TOKEN`
(see `SKILL.md` for minting). Envelope: `{success, data, message}`.
`{sid}` = a numeric `studentId`; `{shift}` = `0` (AM, to school) / `1` (PM, home).

All reads below are **live-verified** (2026-08-25). Define the helper once:

```sh
alpha() { curl -s "https://api.alpharoute.app/$1" -H "Authorization: Bearer $ALPHAPORTAL_TOKEN"; }
apost() { curl -s -X POST "https://api.alpharoute.app/$1" -H "Authorization: Bearer $ALPHAPORTAL_TOKEN" -H 'Content-Type: application/json' -d "$2"; }
```

## Students & transportation

```sh
# full student records
alpha AlphaPortal/v1/user-students/list | jq '.data.students'

# slim list (id + name only)
alpha AlphaPortal/v1/user-students/lightlist | jq '.data.students'

# one student: school + morning/afternoon stops
alpha AlphaPortal/v1/user-students/retrieve/218652901 | jq '.data'

# a student's assigned stops (name, time, lat/lng, days)
alpha AlphaPortal/v1/user-students/stops/218652901 \
  | jq '.data.stops[] | {stopName, time, afternoonFlag, saLat, saLng, vehicleName}'

# LIVE bus GPS for a run (shift 0=AM, 1=PM); empty location = not running
alpha AlphaPortal/v1/user-students/vehicle-location/218652901/1 | jq '.data.location'

# a one-time PDF report link
alpha "AlphaPortal/v1/user-students/reports-bulk?studentId=218652901" | jq '.data'

# the account groups (districts) you belong to
alpha AlphaPortal/v1/user-students/account-groups | jq '.data.accountGroups'
```

## Notifications & requests

```sh
# arrival/departure notification feed (the real one)
alpha AlphaPortal/v1/notifications/list \
  | jq '.data.notifications[] | {title, personName, body, creationDate}'

# your submitted transportation requests (tracking numbers, status)
alpha AlphaPortal/v1/requests/list | jq '.data.requestTransportations'
```

## Account & district reference

```sh
apost AlphaCore/v1/user/profile '{}' | jq '.data.Profile'
alpha AlphaCore/v1/user/accountdate | jq '.data'          # server date + timezone
alpha AlphaCore/v1/account/inforetrieve | jq '.data.Account'
alpha AlphaPortal/v1/applicationsetting/retrieve | jq '.data.settings'   # feature flags
alpha AlphaPlan/v1/school/lightlist | jq '.data.School[] | {SchoolName, Lat, Lng}'
alpha AlphaPlan/v1/student/gradelist | jq '.data.Grades'
alpha AlphaPlan/v1/distanceunit/list | jq '.data.Units'
```

## Writes (real & permanent here — no dry-run)

Both require a `studentId`. Bodies are transcribed from the AlphaPortal web
client. Values for notification toggles are `0`/`1`.

```sh
# set walk-zone radius (meters) — affects eligibility
apost AlphaPortal/v1/user-students/radius-edit '{"studentId":218652901,"radius":800}' | jq

# set notification preferences (per category, push/email, AM/PM).
# Categories the district enables: stopRadiusEntry, studentScan, backupBus,
# schoolArrival, stopServiced. Fields: <category>NotifyAm/Pm (push),
# <category>EmailAm/Pm (email). The web client sends the whole set at once.
apost AlphaPortal/v1/user-students/setnotification \
  '{"studentId":218652901,"schoolArrivalNotifyAm":1,"schoolArrivalNotifyPm":1,"schoolArrivalEmailAm":0,"schoolArrivalEmailPm":0}' | jq
```

## Refresh (mint a new access token, rotating the refresh token)

```sh
# returns {token, refreshToken, lang}; the refresh token is reusable, but each
# call also issues a fresh 8-day one you can save to roll the window forward.
curl -s -X POST https://api.alpharoute.app/AlphaCore/v1/public/refresh-token \
  -H 'Content-Type: application/json' \
  -d "{\"refreshToken\":\"$ALPHAPORTAL_RT\"}" | jq '.data | {token, refreshToken}'
```
