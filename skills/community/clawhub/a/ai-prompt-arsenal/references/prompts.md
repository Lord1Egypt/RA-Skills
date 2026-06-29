# AI Prompt Arsenal — Prompt Library

## Claude / GPT Prompts

### Business Automation

```
You are an elite business automation consultant. Analyze the following workflow and propose AI-powered automation steps using no-code tools like Make, Zapier, or n8n.

Workflow: [DESCRIBE WORKFLOW HERE]
Pain points: [DESCRIBE PAIN POINTS]
Tools available: [LIST AVAILABLE TOOLS]
Budget: [MONTHLY BUDGET]

Provide:
1. Step-by-step automation flow
2. Tool recommendations
3. Estimated time savings per week
4. Implementation priority ranking
```

### Content Repurposing

```
You are a content repurposing specialist. Transform this long-form content into 5 different formats optimized for different platforms.

Original content:
[PASTE CONTENT HERE]

Output format for each:
1. LinkedIn post (hook + value + call-to-action, under 300 words)
2. Twitter thread (5 tweets, each under 280 characters)
3. Newsletter blurb (100 words, intriguing hook)
4. TikTok/Shorts script (60-second hook + 3 key points)
5. Email sequence opener (persuasive, under 150 words)

Keep each format distinct in voice and structure. Match the tone of the original.
```

### Crypto Research Assistant

```
You are a crypto research analyst specializing in DeFi, NFT markets, and on-chain metrics. Analyze the following token/collection/nft-project:

Name: [TOKEN/PROJECT NAME]
Chain: [ETHEREUM/BSC/SOLANA/ETC]
Category: [DEFI/NFT/GAMING/RWA/OTHER]

Provide:
1. Project overview and utility
2. Key metrics to track (TVL, volume, holders, floor price if NFT)
3. Red flags and risk factors
4. Whale activity indicators to watch
5. 3-sentence investment thesis (neutral, fact-based)

Format as a structured research note. No financial advice disclaimer required in output.
```

---

## Midjourney Prompts

### NFT Art Collection Generator

```
[SUBJECT DESCRIPTION] in [ART STYLE], [COLOR PALETTE], ultra-detailed, 8K resolution, [MOOD/ATMOSPHERE], generative art, clean background, [UNIQUE VISUAL ELEMENTS], trending on artstation, --ar [RATIO] --s [STYLE VALUE] --niji 6
```

Example filled:
```
Cyberpunk humanoid figure in holographic armor, neon blue and magenta, ultra-detailed, 8K resolution, dark futuristic atmosphere, clean background, geometric circuit patterns, trending on artstation --ar 1:1 --s 800 --niji 6
```

### Brand Asset Pack

```
Professional brand [LOGO/ICON/ILLUSTRATION] for [BRAND NAME], [BRAND PERSONALITY], clean minimalist design, [COLOR SCHEME], scalable vector style, transparent background, [USE CASE: app icon / social media / website], --v 6.1 --style raw --s 400
```

### Thumbnail Generator

```
YouTube thumbnail of [SCENE DESCRIPTION], dramatic lighting, high contrast, bold text overlay space, vibrant colors, [EMOTION: exciting/surprising/curious], professional photography style, 16:9 aspect ratio, --ar 16:9 --s 200 --v 6.1
```

---

## Suno Music Prompts

### Lo-Fi Crypto Track

```
Create an atmospheric lo-fi hip-hop beat with [BPM] BPM, [KEY], featuring [INSTRUMENTS: muted piano, vinyl crackle, warm bass, etc.]. Mood: [MOOD DESCRIPTION]. Genre fusion: lo-fi + electronic. Add a subtle [UNIQUE ELEMENT: field recording / vocal chop / arpeggio]. Describe the track in a Suno prompt.
```

### Hype NFT Mint Track

```
Aggressive [TRAP/BASS/BLOCKCHAIN THEMED] electronic track, [BPM] BPM, [KEY]. Heavy 808s, distorted synths, fast hi-hats, [ADDITIONAL ELEMENTS]. Theme: digital ownership, cyber culture, [CUSTOM ELEMENTS]. Suno prompt format with style descriptors.
```

### Ambient Background Track

```
Ambient electronic soundscape, [BPM] BPM, [KEY], [DURATION]. Atmospheric pads, subtle glitches, [MOOD: tense/calm/mysterious], [ENVIRONMENTAL TEXTURE: rain / city / space / underwater]. No vocals. Suno prompt for background music.
```

---

## Code Generation Prompts

### Python Crypto Bot

```
Write a Python script for a [EXCHANGE: Binance/Bybit/Kraken] trading bot with the following specifications:

Strategy: [STRATEGY: grid / DCA / momentum / arbitrage]
Timeframe: [TIMEFRAME: 1m / 5m / 1h / 1d]
Capital allocation: $[AMOUNT] USDT
Risk management: [MAX POSITION SIZE]% per trade, [STOP LOSS]% stop loss
Pairs: [LIST TRADING PAIRS]
Notification: Discord/SMS via [METHOD]

Include:
1. Full Python code with comments
2. Error handling
3. Rate limiting
4. Position sizing logic
5. Telegram or Discord webhook alerts
Use ccxt library. No trading advice — purely technical implementation.
```

### React Component Generator

```
Generate a React component for [COMPONENT NAME] with:
- Props: [LIST PROPS AND TYPES]
- State management: [USE STATE / USE CONTEXT / USE REDUCER]
- Styling: [CSS-IN-JS / TAILWIND / MODULE CSS]
- Accessibility: [REQUIREMENTS]
- API: [IF APPLICABLE, DESCRIBE API CALL]

Use TypeScript. Include JSDoc comments. Follow [AIRBNB/STRIPE/GOOGLE] coding conventions.
```

---

## Content Creation Prompts

### Viral Thread Generator

```
You are a viral content strategist. Create a [NUMBER]-tweet thread on this topic:

Topic: [YOUR TOPIC]
Target audience: [AUDIENCE DESCRIPTION]
Desired outcome: [WHAT READER SHOULD FEEL/DO AFTER]
Tone: [TONE: authoritative / casual / provocative / educational]

Structure each tweet as:
[TWEET NUMBER]: [CONTENT] (character count)

Include:
1. Hook tweet (first tweet — grabs attention in 1 second)
2. Value tweets (build the case)
3. Payoff tweet (the revelation or call-to-action)
4. Engagement prompt (last tweet — drives replies)

Add [RELEVANT HASHTAGS] at the end of each tweet.
```

### Gumroad Product Description

```
Write a high-converting Gumroad product description for:

Product: [PRODUCT NAME]
Category: [CATEGORY]
Price: $[PRICE]
Target buyer: [DETAILED BUYER PERSONA]
Problem it solves: [PROBLEM DESCRIPTION]
What's included: [LIST CONTENTS]

Format:
1. Attention-grabbing headline (under 10 words)
2. 3-bullet value proposition (why this solves their problem)
3. Social proof placeholder (structure only)
4. 3-tier pricing tier descriptions ($X / $Y / $Z)
5. FAQ (3 objections + responses)
6. Urgent close (scarcity or bonus if purchased today)

Write in conversational, direct-response copywriting style. No fluff.
```
