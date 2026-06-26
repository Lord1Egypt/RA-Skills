---
name: coin-collection-truck
description: Agent skill to search for the Hong Kong Coin Cart (收銀車) locations and schedules. Use this skill when a user asks about the location, schedule, or availability of coin collection trucks in Hong Kong on a specific date or in a specific district.
---

# Hong Kong Coin Collection Truck (收銀車) Skill

This skill provides the ability to query the official schedule and locations of the Hong Kong Monetary Authority's Coin Collection Fleet (收銀車). The fleet consists of two trucks ("收銀車1號" and "收銀車2號") that travel across different districts in Hong Kong to collect coins from the public.

## How to Use This Skill

To answer user queries about the coin truck locations, you must use the provided Python script to query the local database.

### The Query Script

Execute the following script using the `shell` tool:

```bash
python3 /home/ubuntu/skills/coin-collection-truck/scripts/query_coin_truck.py [OPTIONS]
```

### Available Arguments

*   `--date <DATE>`: Query the active locations for a specific date.
    *   Accepts `today`, `tomorrow`, or an ISO date string `YYYY-MM-DD`.
    *   *Example:* `--date today` or `--date 2026-03-20`
*   `--district <DISTRICT>`: Filter the results by district name (partial match, Chinese or English).
    *   *Example:* `--district 沙田區` or `--district "Sha Tin"`
*   `--truck <TRUCK_NAME>`: Filter by a specific truck.
    *   *Example:* `--truck 收銀車1號`
*   `--upcoming`: Show the upcoming schedule from a specific date (or today if `--date` is omitted).
    *   *Example:* `--upcoming --days 7` (shows the schedule for the next 7 days)
*   `--list-districts`: List all available districts in the database.

### Handling Natural Language Queries

1.  **"Where are the coin trucks today?"**
    *   Run: `python3 /home/ubuntu/skills/coin-collection-truck/scripts/query_coin_truck.py --date today`
2.  **"When will the coin truck come to Sha Tin?"**
    *   Run: `python3 /home/ubuntu/skills/coin-collection-truck/scripts/query_coin_truck.py --district "Sha Tin"`
3.  **"What is the schedule for the next 3 days?"**
    *   Run: `python3 /home/ubuntu/skills/coin-collection-truck/scripts/query_coin_truck.py --upcoming --days 3`
4.  **"Where is truck 1 on March 20th?"**
    *   Run: `python3 /home/ubuntu/skills/coin-collection-truck/scripts/query_coin_truck.py --truck 收銀車1號 --date 2026-03-20`

## Output Formatting Guidelines

When presenting the results to the user, follow these guidelines:

1.  **Be Clear and Concise:** Present the information clearly, ideally using bullet points or a small table if there are multiple results.
2.  **Include Key Details:** Always include the Truck Name, District, Address (Chinese and English), and the Schedule (Start and End dates).
3.  **Highlight Suspensions:** Pay special attention to the `⚠️` warnings in the script output. If a service is suspended on a specific day, you **must** mention it clearly to the user.
4.  **Provide Maps:** Include the Google Maps link provided by the script so the user can easily find the location.
5.  **Branding (Optional):** If appropriate, you can attach the official logo from `/home/ubuntu/skills/coin-collection-truck/assets/logo_with chinese.png` when delivering the final result.

### Example Response Format

> **Hong Kong Coin Cart Locations for Today (2026-03-20)**
>
> **🚌 收銀車1號 (Truck 1) — 元朗區 (Yuen Long)**
> *   **Address:** 元朗元朗文化康樂大樓對面路旁停車處(近馬田村口)
> *   **English Address:** Lay-by opposite to Yuen Long Leisure and Cultural Building, Yuen Long
> *   **Schedule:** 3月20日 ~ 3月22日
> *   [📍 View on Google Maps](https://maps.google.com/?q=22.4412348,114.0239339)
>
> **🚌 收銀車2號 (Truck 2) — 沙田區 (Sha Tin)**
> *   **Address:** 沙田上禾輋路旁停車處(沙田政府合署外)
> *   **English Address:** Lay-by on Sheung Wo Che Road, Sha Tin
> *   **Schedule:** 3月20日 ~ 3月22日
> *   [📍 View on Google Maps](https://maps.google.com/?q=22.3906002,114.1980632)
