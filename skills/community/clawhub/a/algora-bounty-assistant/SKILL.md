---
name: github-bounty-hunter
version: 1.0.0
description: Automatically search for low-competition GitHub bounty tasks (comments < 5) and generate a clean report with details and estimated difficulty.
author: Your Name
price: 299
category: Bounty Hunting
tags:
  - github
  - bounty
  - automation
  - search
---

# GitHub Bounty Hunter 🎯💰

Automatically find low-competition bounty tasks on GitHub. Filter by number of comments to avoid crowded bounties and maximize your chance of getting accepted.

## Features

- 🔍 **Search open bounties** with label:bounty and state:open
- 🎯 **Low-competition filter** - only shows bounties with `< N` comments (default 5)
- 📊 **Generate clean report** with title, URL, comment count, difficulty estimation
- ⚡ **Fast search** via GitHub API
- 🎨 **Sorted by competition level** - least competition first

## Installation

```bash
npx clawhub install github-bounty-hunter
```

## Usage

Search for low-competition bounties:

```bash
npx github-bounty-hunter
```

Customize maximum comment count:

```bash
npx github-bounty-hunter 3
```

## Output example:

```text
=========================================
  GitHub Bounty Hunter - Search Results
=========================================

Found 5 low-competition bounties:

👉 Add transaction history page
   URL: `https://github.com/example/project/issues/6` 
   💬 Comments: 2 | 💪 Difficulty: Beginner

👉 FAQ & How It Works Page
   URL: `https://github.com/example/project/issues/264` 
   💬 Comments: 1 | 💪 Difficulty: Beginner

...
```

## Requirements

- Node.js 16+
- GitHub API access (authenticated for higher rate limits)

## How it works

This skill uses the GitHub Search API to find open issues with the bounty label, filters by comment count, sorts by least comments first, and outputs a clean report ready for you to pick your next bounty.

## Perfect for:

- Beginners looking for easy bounties
- Bounty hunters who want less competition
- Daily quick scans for new opportunities

## Changelog

### 1.0.0
- Initial release
- Basic search and filtering
- Report generation