---
name: auto-watchdog
description: A continuous monitoring skill for crypto, stock markets, and general news. It gathers information from various sources (X, blogs, Forbes, etc.) and provides regular updates. The monitoring duration is configurable by the user, including an option for indefinite surveillance until explicitly stopped.
license: Complete terms in LICENSE.txt
---

# Auto-Watchdog Skill

This skill enables continuous, automated surveillance of financial markets (crypto, stocks) and general news from a wide array of online sources. It is designed to keep you informed with timely and relevant updates, adapting to your specified monitoring duration.

## Usage

To activate the Auto-Watchdog, simply invoke the skill. It will then prompt you to specify the desired monitoring duration. You can choose a specific time frame (e.g., "1 hour", "3 days") or opt for continuous monitoring by stating "forever".

### Parameters

- **Duration**: The period for which the monitoring should run. Examples include "1 hour", "24 hours", "3 days", "1 week", or "forever". If "forever" is selected, the monitoring will continue until explicitly stopped by the user.

## Workflow

1. **Initialization**: Upon invocation, the skill will ask the user for the monitoring duration.
2. **Monitoring Loop**: Based on the specified duration, the skill will initiate a continuous loop of information gathering.
3. **Information Gathering**: The skill will query various online sources, including social media platforms (e.g., X), financial news outlets (e.g., Forbes), and specialized blogs, to collect relevant data on crypto, stock markets, and general news.
4. **Analysis and Summarization**: Collected information will be processed, analyzed for key trends and developments, and then summarized into concise updates.
5. **Reporting**: Regular updates will be provided to the user at predefined intervals (e.g., every hour for short durations, daily for longer durations).
6. **Termination**: The monitoring will cease automatically after the specified duration or immediately if the user explicitly requests to stop the skill.

## Compatibility

This skill is designed to be compatible with OpenClaw environments, ensuring seamless integration and execution within such systems.

## Bundled Resources

- `scripts/monitor.py`: The core Python script responsible for executing the monitoring loop, gathering data, and generating reports.
- `references/sources.md`: A list of predefined and configurable sources for information gathering.

