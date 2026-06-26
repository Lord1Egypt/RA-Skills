# CapSolver Skills

A collection of skills for the CapSolver, unleashing your RPA potential.

## Table of Contents

- [Supported captcha types](#supported-captcha-types)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Usage Examples](#usage-examples)
  - [Task(Recognition)](#taskrecognition)
    - [ImageToTextTask](#imagetotexttask)
    - [ReCaptchaV2Classification](#ReCaptchaV2Classification)
    - [AwsWafClassification](#AwsWafClassification)
    - [VisionEngine](#VisionEngine)
  - [Task(Token)](#tasktoken)
    - [GeeTest](#geetest)
    - [reCAPTCHA v2](#recaptcha-v2)
    - [reCAPTCHA v3](#recaptcha-v3)
    - [MTCaptcha](#mtcaptcha)
    - [DataDome](#datadome)
    - [AWS WAF](#aws-waf)
    - [Cloudflare Turnstile](#cloudflare-turnstile)
    - [Cloudflare Challenge](#cloudflare-challenge)
- [Resources](#resources)

## Supported captcha types

Task(Recognition)
1. ImageToText
2. reCAPTCHA v2
3. AWS WAF
4. VisionEngine

Task(Token)
1. Geetest V3
2. Geetest V4
3. reCAPTCHA v2
4. reCAPTCHA v3
5. Cloudflare Turnstile
6. Cloudflare Challenge
7. DataDome
8. AWS WAF
9. MTCaptcha

## Directory Structure

```
capsolver/
├── scripts/               # The capsolver script for this skill
├── SKILL.md               # Skill metadata
├── README.md              # README.md
├── requirements.txt       # Python dependencies
└── .env.example           # Example environment file
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/capsolver/capsolver-skills.git
cd capsolver-skills
```

2. Install python dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

1. Create a `.env` file in the root directory based on the `.env.example` file:

```bash
cp .env.example .env
```

2. Add your CapSolver API key to the `.env` file:

```
API_KEY=CAP-XXXXX-your-api-key-here
```

You can get an API key from the [CapSolver Dashboard](https://dashboard.capsolver.com/).

## Usage Examples

### Task(Recognition)

#### ImageToTextTask

Solve text-based captcha.

**Command:**

```bash
python3 solver.py ImageToTextTask --body "base64_image_data"
python3 solver.py ImageToTextTask --body "base64_image_data" --module "module_001"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--body`: Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--module`: Specify the module. All supported module references: https://docs.capsolver.com/en/guide/recognition/ImageToTextTask/#independent-module-support.
- `--images`: Only for `number` module, Support up to 9 base64 encoded images each time.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### ReCaptchaV2Classification

Classify reCAPTCHA v2 images.

**Command:**

```bash
python3 solver.py ReCaptchaV2Classification --question "question" --image "base64_image_data"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--websiteKey`: Website key to improve accuracy.
- `--question`: Please refer to: https://docs.capsolver.com/guide/recognition/ReCaptchaClassification/.
- `--image`: Base64 image string.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### AwsWafClassification

Classify AWS WAF images.

**Command:**

```bash
python3 solver.py AwsWafClassification --question "question" --images "base64_image_data1" "base64_image_data2" "base64_image_data3"
```

Too many images may exceed the command line length limit. You can try writing the base64 values of the images line by line to a file (such as aws_images.txt) and then using the xargs command to pass them to the --images parameter:

```bash
cat aws_images.txt | xargs python3 solver.py AwsWafClassification --question "question" --images
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--question`: Please refer to: https://docs.capsolver.com/guide/recognition/AwsWafClassification/.
- `--images`: Base64 image string, `aws:grid` supports 9 images each time, other types support 1 image each time.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### VisionEngine

Advanced AI vision-based captcha solving.

**Command:**
```bash
python3 solver.py VisionEngine --module "module" --image "base64_image_data" --imageBackground "base64_image_background_data"
```

Optional:
- `--websiteURL`: Page source url to improve accuracy.
- `--module`: Please refer to: https://docs.capsolver.com/guide/recognition/VisionEngine/.
- `--question`: Only the `shein` model requires, please refer to: https://docs.capsolver.com/en/guide/recognition/VisionEngine/.
- `--image`: Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--imageBackground`: Base64 encoded content of the background image (no newlines, no data:image/***;charset=utf-8;base64,).
- `--max-retries`: Maximum number of retries (default: 60).

---

### Task(Token)

#### GeeTest

Solve GeeTest captcha (v3/v4).

**Command:**
```bash
python3 solver.py GeeTestTaskProxyLess --websiteURL "https://example.com/" --captchaId "captcha_id"
```

Optional:
- `--websiteURL`: Web address of the website using geetest (Ex: https://geetest.com).
- `--gt`: Only Geetest V3 is required.
- `--challenge`: Only Geetest V3 is required.
- `--captchaId`: Only Geetest V4 is required.
- `--geetestApiServerSubdomain`: Special api subdomain, example: api.geetest.com.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### reCAPTCHA v2

Solve Google reCAPTCHA v2 (checkbox/invisible).

**Command:**

```bash
python3 solver.py ReCaptchaV2TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 solver.py ReCaptchaV2Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
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

#### reCAPTCHA v3

Solve Google reCAPTCHA v3.

**Command:**

```bash
python3 solver.py ReCaptchaV3TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 solver.py ReCaptchaV3Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
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

#### MTCaptcha

Solve MTCaptcha.

**Command:**

```bash
python3 solver.py MtCaptchaTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
python3 solver.py MtCaptchaTask --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
```

Optional:
- `--websiteURL`: Web address of the website using generally it’s fixed value. (Ex: https://google.com).
- `--websiteKey`: The domain public key, rarely updated. (Ex: sk=MTPublic-xxx public key).
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### DataDome

Solve DataDome.

**Command:**

```bash
python3 solver.py DatadomeSliderTask --captchaUrl "https://geo.captcha-delivery.com/xxxxxxxxx" --userAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" --proxy "host:port:username:password"
```

Optional:
- `--captchaUrl`: If the url contains t=bv that means that your ip must be banned, t should be t=fe.
- `--userAgent`: It needs to be the same as the userAgent you use to request the website. Currently we only support the following userAgent.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### AWS WAF

Solve AWS WAF.

**Command:**
```bash
python3 solver.py AntiAwsWafTask --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js" --proxy "host:port:username:password"
python3 solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js"
python3 solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com"
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

#### Cloudflare Turnstile

Solve Cloudflare Turnstile.

**Command:**
```bash
python3 solver.py AntiTurnstileTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
```

Optional:
- `--websiteURL`: The address of the target page.
- `--websiteKey`: Turnstile website key.
- `--action`: The value of the data-action attribute of the Turnstile element if it exists.
- `--cdata`: The value of the data-cdata attribute of the Turnstile element if it exists.
- `--max-retries`: Maximum number of retries (default: 60).

---

#### Cloudflare Challenge

Solve Cloudflare Challenge (5-second shield).

**Command:**
```bash
python3 solver.py AntiCloudflareTask --websiteURL "https://example.com" --proxy "host:port:username:password"
```

Optional:

- `--websiteURL`: The address of the target page.
- `--proxy`: Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/.
- `--userAgent`: The user-agent you used to request the target website. Only Chrome’s userAgent is supported.
- `--html`: The response of requesting the target website, it usually contains "Just a moment…" and status code is 403. we need this html for some websites, please be sure to use your sticky proxy to dynamically scrape the HTML every time.
- `--max-retries`: Maximum number of retries (default: 60).

## Resources

- [CapSolver Docs](https://docs.capsolver.com/) - The official capsolver documentation allows you to find answers to any questions you are unsure of here
