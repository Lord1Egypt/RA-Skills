# currency-convert

An OpenClaw skill that converts amounts between any two currencies
using live exchange rates from the Open Exchange Rates API.

## What it does

- Converts any amount between 170+ world currencies
- Fetches live rates via a local Python script
- Shows the exact exchange rate and timestamp
- Works with currency codes (USD, PKR, EUR) and country names

## Setup

### 1. Get a free API key
Sign up at https://openexchangerates.org — free tier gives
1000 requests/month, no credit card needed.

### 2. Store your API key
Add this to your ~/.bashrc or systemd service override:
export OXR_APP_ID="your_app_id_here"

### 3. Install the skill
openclaw skills install currency-convert

## Usage

Just ask naturally in OpenClaw chat:

- "convert 100 USD to PKR"
- "what is 500 euros in Japanese yen"
- "exchange rate USD to AED"

## Example output

💱 Currency Conversion

100 USD → 27,835.00 PKR

📈 Exchange Rate: 1 USD = 278.35 PKR
🕐 Rates updated: 2026-06-18

_Powered by Open Exchange Rates_

## Requirements

- python3 in PATH
- OXR_APP_ID environment variable set
- exec tool enabled in OpenClaw tools profile

## Currency codes

Uses standard ISO 4217 three-letter codes.
Full list: https://openexchangerates.org/currencies