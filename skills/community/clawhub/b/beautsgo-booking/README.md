# BeautsGO — Korean Beauty & Medical Aesthetic Booking Skill

[![clawhub](https://img.shields.io/badge/clawhub-beautsgo--booking-blue)](https://clawhub.ai/BeautsGO/beautsgo-booking)
[![version](https://img.shields.io/badge/version-1.0.8-green)](https://clawhub.ai/BeautsGO/beautsgo-booking)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-1300%2B%20Clinics-brightgreen)](https://beautsgo.github.io/beautsgo-booking/)

> **One sentence, one appointment.** Tell your AI assistant which Seoul clinic you want or what procedure you need — BeautsGO handles the rest: clinic matching, booking submission, price lookup, and live customer service. Built on a curated database of **1300+ dermatology clinics, plastic surgery hospitals, and aesthetic centers** in Seoul, supporting **Chinese, English, Japanese, and Thai**.

---

## Install

### Claude Code / OpenClaw (CLI)

```bash
npx clawhub install beautsgo-booking
```

Compatible with Claude Code, WorkBuddy, and any [OpenClaw](https://clawhub.ai)-compatible AI client.

### ModelScope (魔搭社区)

```bash
npx skills add https://www.modelscope.cn/skills/spidericer/beautsgo-booking
```

Or via ModelScope SDK: `pip install --upgrade modelscope && modelscope skills add spidericer/beautsgo-booking`

### Smithery

```bash
npx -y smithery skill add beautsgo7/beautsgo-booking
```

### 国内 AI 助手（粘 GitHub URL 一键装）

#### 月之暗面 Kimi

打开 Kimi 网页版 → **Agent 集群** → 点 **「+ 添加 Claw」** → 粘贴：

```
https://github.com/BeautsGO/beautsgo-booking
```

#### 网易有道 LobsterAI

打开 LobsterAI 客户端 → **设置** → **Skills** → **远程导入** → 粘贴上面同一个 URL。

---

## What It Does

BeautsGO Booking is a conversational skill that turns natural language into real appointments at Seoul's top aesthetic clinics. No app download. No form filling. No language barrier.

### Quick Examples

| You Say | Skill Does |
|---------|-----------|
| `"Book JD Skin Clinic"` | Returns the full booking guide with 5 appointment channels |
| `"I want Botox in Seoul"` | Matches clinics offering Botox, lists top results |
| `"Recommend a dermatology clinic"` | Returns curated popular clinic recommendations |
| `"How much is laser at Wonjin?"` | Opens the clinic's price page |
| `"Chat with customer service"` | Opens the clinic's live consultation page |
| `"Download the app"` | Returns iOS / Android / APK download links |

### Multi-Turn Conversation Flow

The skill maintains context across turns, so you can complete an entire booking in a natural conversation:

```
Round 1 — Search
  You:     "How to book JD Skin Clinic?"
  Skill:   Returns 5 booking channels + suggests next steps

Round 2 — Browse
  You:     "Open the link"
  Skill:   Opens the BeautsGO clinic detail page in your browser

Round 3 — Book
  You:     "Book it for me"
  Skill:   Collects party size and preferred date

Round 4 — Submit
  You:     "2 people, April 10th"
  Skill:   Submits the appointment via API, returns confirmation

Round 5 — Consult
  You:     "Talk to customer service"
  Skill:   Opens the clinic's live chat page
```

### Supported Input Styles

The resolver uses a **4-tier matching strategy** to understand what you mean:

- **Exact match**: `"JD皮肤科"` → JD Skin Clinic
- **Pinyin match**: `"jd pifu"` or `"jdpfk"` → JD Skin Clinic
- **Fuzzy match**: `"韩国jd"` → JD Skin Clinic
- **Intent match**: `"I want double eyelid surgery"` → Lists relevant clinics

Minimum query length is 2 characters to prevent false positives.

---

## Core Capabilities

| Feature | Description |
|---------|-------------|
| 🏥 **1300+ Clinics** | Curated database of Seoul dermatology, plastic surgery, and aesthetic centers |
| 🧠 **4-Tier Matching** | Exact → Pinyin → Fuzzy → Alias — handles Chinese, English, abbreviations, and nicknames |
| 🎯 **Intent Recognition** | No clinic name needed — just say what procedure you want |
| 📅 **Direct API Booking** | Submits appointments via `POST /api/Appointment/saveFromSkill` — no browser required |
| 💰 **Price Lookup** | Opens up-to-date price lists for any listed clinic |
| 💬 **Live Consultation** | Instant connection to clinic customer service |
| 📱 **App Download** | iOS, Android, Google Play, WeChat Mini Program, and APK links |
| 🌐 **Multi-Language** | Chinese, English, Japanese, Thai — auto-detected from user input |
| 📄 **Static Clinic Pages** | SEO-optimized pages for 1300+ clinics in 4 languages on [GitHub Pages](https://beautsgo.github.io/beautsgo-booking/) |

---

## Booking Channels

Every clinic returns all 5 available appointment channels:

| Channel | Platform |
|---------|----------|
| 🍎 App Store | iOS |
| 🤖 Google Play | Android |
| 💬 WeChat Mini Program | 微信小程序 |
| 🟢 WeChat Official Account | 微信公众号 |
| 🌐 Web | Browser |

---

## Quick Start

### As a Skill (Recommended)

```bash
npx clawhub install beautsgo-booking
```

### As a Node.js Module

```bash
npm install
```

```js
const skill = require('./api/skill')

// Search & get booking info
const result = await skill({
  query: 'Book JD Skin Clinic',
  lang: 'en'   // en / zh / ja / th
})

// Multi-turn: submit an appointment
const result2 = await skill({
  query: 'Book it for 2 people on April 10th',
  lang: 'en',
  context: { hospitalName: 'JD Skin Clinic' }
})

console.log(result2)
```

---

## Project Structure

```
├── api/
│   ├── skill.js              # Skill entry point
│   └── browser/
│       └── open-url.js       # Open URLs in system browser
├── core/
│   ├── preprocessor.js       # NLP preprocessing
│   ├── resolver.js           # 4-tier clinic matching
│   ├── service.js            # Business orchestration
│   └── renderer.js           # Template rendering
├── data/
│   └── hospitals.json        # Clinic database (1300+)
├── i18n/
│   ├── en.json               # English
│   ├── zh.json               # Chinese
│   ├── ja.json               # Japanese
│   └── th.json               # Thai
├── templates/
│   └── booking.tpl           # Booking response template
├── docs/
│   ├── index.html            # Landing page (GitHub Pages)
│   └── clinics/              # Static clinic pages (zh/en/ja/th)
├── scripts/
│   └── generate-md.js        # Clinic page generator
├── SKILL.md                  # Skill metadata (clawhub)
└── skill.json                # Skill configuration
```

---

## Clinic Data

Clinic records are stored in `data/hospitals.json`:

```json
{
  "id": 1,
  "name": "韩国JD皮肤科",
  "en_name": "JD Skin Clinic",
  "alias": "JD皮肤科",
  "aliases": ["jd皮肤科", "韩国jd", "jd"],
  "url": "https://i.beautsgo.com/cn/hospital/jd-skin-clinic",
  "category": "皮肤科"
}
```

To add a new clinic, simply append a record to `hospitals.json` and push — the static pages regenerate automatically.

---

## Matching Strategy

The resolver runs queries through 4 tiers in order, returning on the first match:

1. **Exact** — Full match against `name`, `en_name`, or `alias`
2. **Pinyin Exact** — Full pinyin or initials match (Chinese characters only)
3. **Chinese Fuzzy** — Query is a substring of the Chinese name
4. **General Fuzzy** — Query appears in English name, aliases, or pinyin

---

## Generate Static Pages

```bash
npm run generate        # Chinese only
npm run generate:all    # All languages (zh/en/ja/th)
```

Output goes to `docs/clinics/`, served via GitHub Pages at [beautsgo.github.io/beautsgo-booking](https://beautsgo.github.io/beautsgo-booking/).

---

## Links

- 🔗 [Skill on ClawHub](https://clawhub.ai/BeautsGO/beautsgo-booking)
- 🌐 [BeautsGO Official](https://beautsgo.com)
- 📱 [Clinic Pages](https://beautsgo.github.io/beautsgo-booking/)
- 🍎 [iOS App Store](https://apps.apple.com/cn/app/beautsgo%E5%BD%BC%E6%AD%A4%E7%BE%8E-%E9%9F%A9%E5%9B%BD%E7%9A%AE%E8%82%A4%E7%A7%91%E9%A2%84%E7%BA%A6/id6741841509)
- 🤖 [Google Play](https://play.google.com/store/apps/details?id=uni.UNIEF980DB)
