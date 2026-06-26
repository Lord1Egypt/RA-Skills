---
name: capsolver
description: Use capsolver to automatically resolve Geetest, reCAPTCHA v2, reCAPTCHA v3, MTCaptcha, DataDome, AWS WAF, Cloudflare Turnstile, and Cloudflare Challenge, etc.
homepage: https://capsolver.com/
credentials:
  - API_KEY
env:
  required:
    - API_KEY
---

# CapSolver Skill

Use this skill to automatically resolve various CAPTCHA challenges using the CapSolver API service. The skill supports Geetest, reCAPTCHA v2/v3, MTCaptcha, DataDome, AWS WAF, Cloudflare Turnstile, Cloudflare Challenge, and more.

**Authentication:** Set `API_KEY` in your environment or in a `.env` file in the repo root.

**Errors:** If it fails, the script will exit with code 1.

---

# Solver

## Task(Recognition)

### ImageToTextTask

Solve text-based captcha.

**Command:**

```bash
python3 ./scripts/solver.py ImageToTextTask --body "base64_image_data"
python3 ./scripts/solver.py ImageToTextTask --body "base64_image_data" --module "module_001"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--body`: Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--module`: Specify the module. All supported module references: https://docs.capsolver.com/en/guide/recognition/ImageToTextTask/#independent-module-support.
- `--images`: Only for `number` module, Support up to 9 base64 encoded images each time.
- `--max-retries`: Maximum number of retries (default: 60).

---

### ReCaptchaV2Classification

Classify reCAPTCHA v2 images.

**Command:**

```bash
python3 ./scripts/solver.py ReCaptchaV2Classification --question "question" --image "base64_image_data"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--websiteKey`: Website key to improve accuracy.
- `--question`: Please refer to: https://docs.capsolver.com/guide/recognition/ReCaptchaClassification/.
- `--image`: Base64 image string.
- `--max-retries`: Maximum number of retries (default: 60).

---

### AwsWafClassification

Classify AWS WAF images.

**Command:**

```bash
python3 ./scripts/solver.py AwsWafClassification --question "question" --images "base64_image_data1" "base64_image_data2" "base64_image_data3"
```

Too many images may exceed the command line length limit. You can try writing the base64 values of the images line by line to a file (such as aws_images.txt) and then using the xargs command to pass them to the --images parameter:

```bash
cat aws_images.txt | xargs python3 ./scripts/solver.py AwsWafClassification --question "question" --images
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--question`: Please refer to: https://docs.capsolver.com/guide/recognition/AwsWafClassification/.
- `--images`: Base64 image string, `aws:grid` supports 9 images each time, other types support 1 image each time.
- `--max-retries`: Maximum number of retries (default: 60).

---

### VisionEngine

Advanced AI vision-based captcha solving.

**Command:**
```bash
python3 ./scripts/solver.py VisionEngine --module "module" --image "base64_image_data" --imageBackground "base64_image_background_data"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--module`: Please refer to: https://docs.capsolver.com/guide/recognition/VisionEngine/.
- `--question`: Only the `shein` model requires, please refer to: https://docs.capsolver.com/en/guide/recognition/VisionEngine/.
- `--image`: Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--imageBackground`: Base64 encoded content of the background image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--max-retries`: Maximum number of retries (default: 60).

---

## Task(Token)

### GeeTest

Solve GeeTest captcha (v3/v4).

**Command:**
```bash
python3 ./scripts/solver.py GeeTestTaskProxyLess --websiteURL "https://example.com/" --captchaId "captcha_id"
```

Optional:
- `--websiteURL`: Web address of the website using geetest (Ex: https://geetest.com).
- `--gt`: Only Geetest V3 is required.
- `--challenge`: Only Geetest V3 is required.
- `--captchaId`: Only Geetest V4 is required.
- `--geetestApiServerSubdomain`: Special api subdomain, example: api.geetest.com.
- `--max-retries`: Maximum number of retries (default: 60).

---

### reCAPTCHA v2

Solve Google reCAPTCHA v2 (checkbox/invisible).

**Command:**

```bash
python3 ./scripts/solver.py ReCaptchaV2TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 ./scripts/solver.py ReCaptchaV2Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
```

Optional:
- `--websiteURL`: The URL of the target webpage that loads the captcha, It’s best to submit the full URL instead of just the host.
- `--websiteKey`: Recaptcha website key.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--pageAction`: For ReCaptcha v2, if there is an sa parameter in the payload of the /anchor endpoint, please submit its value.
- `--enterprisePayload`: For ReCaptchaV2 enterprise version, if there is an s parameter in the payload of the /anchor endpoint, please submit its value.
- `--isInvisible`: Pass true if there is no “I’m not a robot” checkbox but the challenge will still appear, usually required in v2 invisible mode.
- `--isSession`: Session mode, when enabled, will return a recaptcha-ca-t value, which is used as a cookie. It usually appears in v3. Note: Some websites require a recaptcha-ca-e value, which usually appears in v2. If this value is present, it will be automatically returned without any additional parameter settings.
- `--max-retries`: Maximum number of retries (default: 60).

---

### reCAPTCHA v3

Solve Google reCAPTCHA v3.

**Command:**

```bash
python3 ./scripts/solver.py ReCaptchaV3TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 ./scripts/solver.py ReCaptchaV3Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
```

Optional:
- `--websiteURL`: The URL of the target webpage that loads the captcha, It’s best to submit the full URL instead of just the host.
- `--websiteKey`: Recaptcha website key.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--pageAction`: For ReCaptcha v3, You can find the value of the action parameter by searching for grecaptcha.execute.
- `--enterprisePayload`: For the enterprise version, search for grecaptcha.enterprise.render and pass the s parameter.
- `--isSession`: Session mode, when enabled, will return a `recaptcha-ca-t` value, which is used as a cookie. It usually appears in v3. Note: Some websites require a `recaptcha-ca-e` value, which usually appears in v2. If this value is present, it will be automatically returned without any additional parameter settings.
- `--max-retries`: Maximum number of retries (default: 60).

---

### MTCaptcha

Solve MTCaptcha.

**Command:**

```bash
python3 ./scripts/solver.py MtCaptchaTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 ./scripts/solver.py MtCaptchaTask --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
```

Optional:
- `--websiteURL`: Web address of the website using generally it’s fixed value. (Ex: https://google.com).
- `--websiteKey`: The domain public key, rarely updated. (Ex: sk=MTPublic-xxx public key).
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--max-retries`: Maximum number of retries (default: 60).

---

### DataDome

Solve DataDome.

**Command:**

```bash
python3 ./scripts/solver.py DatadomeSliderTask --captchaUrl "https://geo.captcha-delivery.com/xxxxxxxxx" --userAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" --proxy "host:port:username:password"
```

Optional:
- `--captchaUrl`: If the url contains t=bv that means that your ip must be banned, t should be t=fe.
- `--userAgent`: It needs to be the same as the userAgent you use to request the website. Currently we only support the following userAgent.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--max-retries`: Maximum number of retries (default: 60).

---

### AWS WAF

Solve AWS WAF.

**Command:**
```bash
python3 ./scripts/solver.py AntiAwsWafTask --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js" --proxy "host:port:username:password"
python3 ./scripts/solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js"
python3 ./scripts/solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com"
```

Optional:
- `--websiteURL`: If the url contains t=bv that means that your ip must be banned, t should be t=fe.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--awsKey`: The key value returned by the captcha page.
- `--awsIv`: The iv value returned by the captcha page.
- `--awsContext`: The context value returned by the captcha page.
- `--awsChallengeJS`: The challenge.js link returned by the captcha page.
- `--awsApiJs`: The jsapi.js link returned by the captcha page.
- `--awsProblemUrl`: The problem endpoint url containing keywords like problem, num_solutions_required, etc..
- `--awsApiKey`: The api_key value of the problem endpoint.
- `--awsExistingToken`: The aws-waf-token used for the last verification.
- `--max-retries`: Maximum number of retries (default: 60).

---

### Cloudflare Turnstile

Solve Cloudflare Turnstile.

**Command:**
```bash
python3 ./scripts/solver.py AntiTurnstileTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
```

Optional:
- `--websiteURL`: The address of the target page.
- `--websiteKey`: Turnstile website key.
- `--action`: The value of the data-action attribute of the Turnstile element if it exists.
- `--cdata`: The value of the data-cdata attribute of the Turnstile element if it exists.
- `--max-retries`: Maximum number of retries (default: 60).

---

### Cloudflare Challenge

Solve Cloudflare Challenge (5-second shield).

**Command:**
```bash
python3 ./scripts/solver.py AntiCloudflareTask --websiteURL "https://example.com" --proxy "host:port:username:password"
```

Optional:

- `--websiteURL`: The address of the target page.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--userAgent`: The user-agent you used to request the target website. Only Chrome’s userAgent is supported.
- `--html`: The response of requesting the target website, it usually contains "Just a moment…" and status code is 403. we need this html for some websites, please be sure to use your sticky proxy to dynamically scrape the HTML every time.
- `--max-retries`: Maximum number of retries (default: 60).

---

## Response example

**Output:** All commands return JSON objects with task-specific solution fields.

### ImageToTextTask

```json
{
  "errorId": 0,
  "errorCode": "",
  "errorDescription": "",
  "status": "ready",
  "solution": {
    "text": "44795sds",
    // number module:
	"answers": ["100", "1330", "147", "248", "303", "439", "752", "752", "752"],
  },
  "taskId": "..."
}
```

### ReCaptchaV2Classification

multi objects:

```json
{
 "errorId": 0,
 "status": "ready",
 "solution": {
   "type": "multi",
   "objects": [
     0,
     1,
     2,
     3
   ],
   "size": 4,
   // 3 or 4
 },
 "taskId": "cbb1c730-e569-4ba6-b5fc-e06377694aa7"
}
```

single object:

```json
{
 "errorId": 0,
 "status": "ready",
 "solution": {
   "type": "single",
   "hasObject": true,
   "size": 1,
 },
 "taskId": "cbb1c730-e569-4ba6-b5fc-e06377694aa7"
}
```

### AwsWafClassification

```json
{
 "errorId": 0,
 "status": "ready",
 "solution": {
   //carcity point
   "box": [
     116.7,
     164.1
   ],
   // grid type, objects means the image index that matches the question
   "objects": [0, 1, 3, 4, 6],
   //if question include `bifurcatedzoo`
   "distance": 500
 },
 "taskId": "cbb1c730-e569-4ba6-b5fc-e06377694aa7"
}
```

### VisionEngine

```json
{
  "errorId": 0,
  "errorCode": "",
  "errorDescription": "",
  "status": "ready",
  "solution": {
     "distance": 213,
  },
  "taskId": "cbb1c730-e569-4ba6-b5fc-e06377694aa7"
}
```

### GeeTest

Geetest v3:

```json
{
  "errorId": 0,
  "taskId": "e0ecaaa8-06f6-41fd-a02e-a0c79b957b15",
  "status": "ready",
  "solution": {
    "challenge": "...",
    "validate": "...",
    "seccode": "...",
    "userAgent": "..."
  },
}
```

Geetest v4:

```json
{
  "errorId": 0,
  "taskId": "e0ecaaa8-06f6-41fd-a02e-a0c79b957b15",
  "status": "ready",
  "solution": {
    "captcha_id": "",
    "captcha_output": "",
    "gen_time": "",
    "lot_number": "",
    "pass_token": "",
    "risk_type": "slide"
  }
}
```

### reCAPTCHA

reCAPTCHA v2/v3:

```json
{
    "errorId": 0,
    "errorCode": null,
    "errorDescription": null,
    "solution": {
        "userAgent": "xxx", // User-Agent
        "secChUa": "xxx", // Sec-Ch-Ua
        "createTime": 1671615324290, // The creation time of the token
        "gRecaptchaResponse": "3AHJ......", // token
        "recaptcha-ca-t": "AbEM......", // Some v3 websites have session mode. After enabling isSession, this parameter will be returned and used as a cookie.
        "recaptcha-ca-e": "Abp_......" // Some v2 websites have this parameter, which is used as a cookie. If there is such a value, it will be automatically returned.
    },
    "status": "ready"
}
```

### MTCaptcha

```json
{
  "errorId": 0,
  "taskId": "646825ef-9547-4a29-9a05-50a6265f9d8a",
  "status": "ready",
  "solution": {
    "token": ""
  }
}
```

### DataDome

```json
{
  "errorId": 0,
  "errorCode": null,
  "errorDescription": null,
  "solution": {
    "cookie": "datadome=yzj_BK...S0; Max-Age=31536000; Domain=; Path=/; Secure; SameSite=Lax"
  },
  "status": "ready"
}
```

### AWS WAF

```json
{
  "errorId": 0,
  "taskId": "646825ef-9547-4a29-9a05-50a6265f9d8a",
  "status": "ready",
  "solution": {
    "cookie": "223d1f60-0e9f-4238-ac0a-e766b15a778e:EQoAf0APpGIKAAAA:AJam3OWpff1VgKIJxH4lGMMHxPVQ0q0R3CNtgcMbR4VvnIBSpgt1Otbax4kuqrgkEp0nFKanO5oPtwt9+Butf7lt0JNe4rZQwZ5IrEnkXvyeZQPaCFshHOISAFLTX7AWHldEXFlZEg7DjIc="
  }
}
```

### Cloudflare Turnstile

```json
{
  "errorId": 0,
  "taskId": "61138bb6-19fb-11ec-a9c8-0242ac110006",
  "status": "ready",
  "errorCode": null,
  "errorDescription": null,
  "solution": {
    "token": "0.mF74FV8wEufAWOdvOak_xFaVy3lqIDel7SwNhw3GgpICSWwTjYfrQB8mRT1dAJJBEoP7N1sESdp6WH9cTS1T0catWLecG3ayNcjwxVtr3hWfS-dmcBGRTx4xYwI64sAVboYGpIyuDBeMIRC3W8dK35v1nDism9xa595Da5VlXKM7hk7pIXg69lodfiftasIkyD_KUGkxBwxvrmz7dBo10-Y5zvro9hD4QKRjOx7DYj9sumnkyYCDx0m4ImDIIkNswfVTWI2V22wlnpHdvMgdtKYgOIIAU28y9gtdrdDkpkH0GHcDyd15sxQGd9VjwhGZA_mpusUKMsEoGgst2rJ3zA.UWfZupqLlGvlATkPo3wdaw.38d55cd0163610d8ce8c42fcff7b62d8981495cc1afacbb2f14e5a23682a4e13",
    "type": "turnstile",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
  }
}
```

### Cloudflare Challenge

```json
{
  "errorId": 0,
  "taskId": "df944101-64ac-468d-bc9f-41baecc3b8ca",
  "status": "ready",
  "errorCode": "",
  "errorDescription": "",
  "solution": {
    "cookies": {
        "cf_clearance": "Bcg6jNLzTVaa3IsFhtDI.e4_LX8p7q7zFYHF7wiHPo...uya1bbdfwBEi3tNNQpc"
    },
    "token": "Bcg6jNLzTVaa3IsFhtDI.e4_LX8p7q7zFYHF7wiHPo...uya1bbdfwBEi3tNNQpc",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
  }
}
```
