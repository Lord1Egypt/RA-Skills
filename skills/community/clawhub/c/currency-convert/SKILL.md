---
name: currency-convert
version: 1.0.0
description: Converts an amount from one currency to another using live exchange rates from Open Exchange Rates API. Runs a local Python script via exec for accurate, real-time results.
homepage: https://github.com/SHA-data/currency-convert
metadata:
        openclaw:
                requires:
                        bins:
                                - python3
                        env:
                                - OXR_APP_ID
                        triggers:
                                - convert currency
                                - exchange rate
                                - how much is
                                - currency conversion
                                - convert dollars
                                - convert rupees
                                - what is the rate
---
# Currency Converter

You are in currency conversion mode. Use the Python script at
`{baseDir}/scripts/convert.py` to fetch live exchange rates and
convert amounts between currencies.

## Steps to follow

1. Read the user's message and extract three things:
   - The source currency (what they have)
   - The target currency (what they want)
   - The amount to convert
2. If the user didn't specify an amount, assume 1.
3. If the user gave a country name instead of a currency code,
   convert it yourself. Examples:
   - Pakistan → PKR
   - USA / dollars → USD
   - Europe / euros → EUR
   - UK / pounds → GBP
   - India → INR
   - UAE / dirhams → AED
4. Run the script using the exec tool:
   python3 {baseDir}/scripts/convert.py FROM TO AMOUNT
   Example: python3 {baseDir}/scripts/convert.py USD PKR 100
5. Read the script output line by line and present it using
   the output format below.
6. If the script prints a line starting with ERROR:, show the
   error clearly and suggest a fix to the user.

## Rules

- Always use the script. Never calculate exchange rates from
  memory — they change daily.
- Currency codes must be exactly 3 uppercase letters.
- If the user asks for multiple conversions in one message,
  run the script once per conversion.
- Never expose the OXR_APP_ID value in your response.
- If exec is not available, tell the user clearly:
  "exec tool is required for this skill."

## Output format

💱 **Currency Conversion**

**{AMOUNT} {FROM}** → **{RESULT} {TO}**

📈 Exchange Rate: 1 {FROM} = {RATE} {TO}
🕐 Rates updated: {TIMESTAMP converted to readable time}

_Powered by Open Exchange Rates_