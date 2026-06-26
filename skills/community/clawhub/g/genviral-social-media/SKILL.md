---
name: genviral-social-media
description: Generate viral social media posts using AI with trend analysis and hashtag optimization for X, Instagram, and Telegram
version: 1.0.0
---

# GenViral Social Media Skill

A skill for generating viral social media posts using AI. Analyzes current trends and creates engaging content optimized for maximum reach on X (Twitter) and other platforms.

## Features

- AI-powered viral post generation
- Automatic hashtag suggestions
- Trend-aware content creation
- Multi-platform support (X, Instagram, Telegram)

## Usage

Call `generateViralPost(topic)` with your desired topic to generate an optimized viral post.

## Example
```js
const skill = require('./index.js');
const post = await skill.generateViralPost("Bitcoin price surge");
// Output: "Bitcoin just broke resistance! Are you holding or folding? #BTC #Crypto"
```

## Requirements

- Node.js 18+
- OpenClaw agent runtime
