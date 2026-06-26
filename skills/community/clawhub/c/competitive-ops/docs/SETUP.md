# Setup Guide

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and configured
- Node.js 18+ (for utility scripts)

## Quick Start (5 steps)

### 1. Clone and install

```bash
git clone <repository-url>
cd competitive-ops-v2
npm install
```

### 2. Configure your profile

Edit `config/profile.yml` with your company details:
- Company name and website
- Product name
- Target market

### 3. Add your CV/Product Definition

Edit `cv.md` with your product/company information using the template provided.

### 4. Add Competitors

Edit `data/competitors.md` to add your known competitors:
- Company name
- Tier (Direct/Indirect)
- Website

### 5. Start using

Open Claude Code in this directory:

```bash
claude
```

Then ask to analyze a competitor or generate a report.

## Available Commands

| Action | How |
|--------|-----|
| Add a competitor | "Add competitor [name]" |
| Run analysis | "Analyze [competitor]" |
| Generate report | "Generate report for [competitor]" |
| Check for changes | "Check for changes" |
| Monitor pricing | "Monitor pricing" |

## Verify Setup

```bash
node scripts/verify-setup.mjs
```
