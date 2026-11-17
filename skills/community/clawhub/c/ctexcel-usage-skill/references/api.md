# CTExcel web API notes

These are the endpoints used by the CTExcel UK personal-home page and by
`ctexcel-usage`. They are unofficial and can change without notice. The CLI
isolates them in `internal/ctexcel-usage/client.go`.

## Base URL

```
https://www.ctexcel.com/newcteuk
```

All requests are `POST` with `Content-Type: application/json` and `lang: zh`.
Authentication is a server-side `SESSION` cookie.

## Login

### 1. Bootstrap an anonymous session

```
POST /logged/getMycteUserInfo
```

An anonymous call returns `{"code":1001,"message":"登录信息失效"}` and sets a
`SESSION` cookie. That cookie is the anchor for the SMS flow.

### 2. Request the SMS code

```
POST /verify/sendMessage
{"userName":"07XXXXXXXX","type":0,"modularId":1}
```

The service rate-limits re-sends for about 180 seconds.

### 3. Exchange the code for a session

```
POST /login/doLogin
{"mobile":"07XXXXXXXX","verifyCode":"123456","type":2}
```

`type: 2` is SMS-only login. Success returns `code: 0` and sets an
authenticated `SESSION` cookie. `type: 1` is the password-plus-code variant;
this CLI does not use it.

## Request encryption

The profile and bundle endpoints accept plain JSON, but two login endpoints
require the frontend's hybrid envelope:

```
POST /verify/sendMessage
POST /login/doLogin
```

Body shape:

```json
{"requestData": "<base64>", "encrypted": "<base64>"}
```

- `requestData`: the real JSON payload encrypted with **AES-128-ECB +
  PKCS#7**, keyed by a random 16-character base-22 string.
- `encrypted`: that 16-character key encrypted with **RSA PKCS#1 v1.5** using
  the public key embedded in the CTExcel JavaScript bundle.

The CLI implements this in `internal/ctexcel-usage/crypto.go`. If the carrier
changes the login flow, re-capture a browser request before editing the
implementation.

## Account profile

```
POST /logged/getMycteUserInfo
```

Returns `data.userInfo` with `msisdn`, `realMsisdn`, `simCardType`, `balance`,
`userState`, and `lastloginTime`. The CLI only uses the masked account,
`simCardType`, `balance`, and login time.

## Bundle allowances

```
POST /logged/getMyBundleInfo/0   # eSIM
POST /logged/getMyBundleInfo/1   # physical SIM
```

Returns `data.bundleUsageList`, one entry per active bundle. Every allowance is
a **quoted string in megabytes**, for example `"14849.31"`. The CLI converts
them to GB by dividing by 1024.

Field mapping used by the CLI:

| API field | Resource key | Meaning |
| --- | --- | --- |
| `zhData` / `zhDataTotal` | `china_data` | China data |
| `eurData` / `eurDataTotal` | `europe_data` | Europe data |
| `data` / `dataTotal` | `local_data` | Local (UK) data |
| `globalData` / `globalDataTotal` | `global_data` | Global data |
| `ukCNData` / `ukCNDataTotal` | `uk_cn_data` | UK/China shared data |
| `bonusData` / `bonusDataTotal` | `bonus_data` | Bonus data |

`bonusData` sometimes mirrors `zhData`; the CLI suppresses the duplicate.
A zero or missing total means the plan does not include that allowance.

Other fields present in the response but not reported: `sms`, `intSms`,
`cnVoice`, `ukVoice`, `intVoice`, `dataPercent`, `bonusDataPercent`. The
percentage fields are the carrier's own rounding; the CLI recomputes
`remaining / total` for consistency.

## Response envelope

```json
{"code":0,"message":null,"data":{...}}
```

- `code: 0` — success.
- `code: 1001` — session expired; log in again.
- Any other non-zero code — surface the message and stop.

Non-2xx HTTP responses are reported as API errors with the status code and body.