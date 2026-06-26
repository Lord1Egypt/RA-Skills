# ClawHub Blueair Skill (CLI Edition)

This is an OpenClaw CLI skill that extends your AI agent with the ability to manage Blueair air purifiers natively, turning it into an **Indoor Air Quality Specialist**. It communicates directly with the Blueair Rest APIs using local Node.js scripts.

## 🚀 Features

This skill provides two primary capabilities via standalone CLI scripts:

### 1. Device Status & Sensor Data

- Fetches real-time status for all connected Blueair devices in the household using `node dist/get_status.js`.
- Reads PM1, PM2.5, PM10, tVOC, HCHO, CO2, NO2, O3, Temperature, and Humidity.
- The AI acts as an expert, summarizing the data into health indicators (e.g., Excellent, Good, Moderate, Unhealthy).

### 2. Purifier Control

- Control your purifiers using natural language. The AI will invoke `node dist/set_state.js`.
- Supported commands:
  - Fan Speed adjustment
  - Power Toggle (Standby)
  - Auto Mode Toggle
  - Night Mode / Child Lock Toggles

## ⚙️ Configuration & Installation

Because this is a CLI skill, it requires you to install its Node dependencies before using it.

### 1. Install Dependencies

Navigate to this folder and run:

```bash
npm install
```

### 2. Configure Credentials

Create a `~/.blueair/config.json` file on your system with your Blueair account details:

```json
{
  "username": "your-email@example.com",
  "password": "your-password",
  "region": "CN"
}
```

*(Valid regions: `US`, `EU`, `AU`, `CN`, `RU`. The system will auto-detect if omitted, but setting it is recommended for speed).*

## 📖 Usage Examples

Once installed into your OpenClaw agent, you can simply talk to it about your air:

- **Check Status:** "How is the air quality in the bedroom?"
- **Contextual Action:** "It feels a bit stuffy in here." (The agent will check VOCs/CO2 and suggest boosting the fan).
- **Control:** "Turn the living room purifier to max speed," or "Put all purifiers in auto mode."

## 🏗️ Repository Structure & Architecture

Because this is a **standalone OpenClaw CLI skill**, it doesn't require a persistent MCP server. The agent executes Node.js scripts just like a human developer running commands in a terminal.

Here is how the repository is structured:

- **`SKILL.md` (The AI's Brain)**: Configures the OpenClaw agent's persona ("Indoor Air Quality Specialist") and instructs it on exactly which CLI commands it can use to check and change your purifiers.
- **`README.md` (The Human's Guide)**: The instructions you are reading right now!
- **`package.json`**: Manages the local dependencies (`node-fetch` and `async-mutex`) required to safely communicate with Blueair's cloud APIs.
- **`scripts/`**: Contains the core logic and scripts that the AI executes:
  - `scripts/api/`: Reusable classes handling Blueair REST API authentication, tokens, and regional routing.
  - `scripts/get_status.ts` & `scripts/set_state.ts`: The entry points written in TypeScript.
- **`dist/`**: Contains the compiled JavaScript versions (`get_status.js` and `set_state.js`) that are actually executed by the skill instructions.
- **`examples/`**: Contains `basic-usage.md` with example conversational transcripts showing how to talk to your agent. This is documentation for users viewing this project on ClawHub.

## 📦 Distributing via ClawHub

This repository is a fully compliant standard OpenClaw AgentSkill. To share it with others:

1. Push this folder to GitHub.
2. Ensure you have tested that it loads perfectly into your own local `.claude/skills` directory via symlink.
3. Submit it to the ClawHub marketplace. Other users will simply download this folder, run `npm install`, and their OpenClaw agents will instantly learn how to manage Blueair devices!

## 🔐 Security & Privacy Notice

This skill interacts with Blueair's cloud infrastructure (Gigya/AWS). Please note:

- **Credential Storage**: Your Blueair email and password are never hardcoded. They are loaded from `~/.blueair/config.json` or your environment variables at runtime.
- **Data Transmission**: To fetch status or change settings, your credentials are sent to Blueair's official authentication endpoints (Gigya) and API Gateway.
- **API Keys**: The repository contains public API keys for Gigya and AWS. These are standard identifiers used by Blueair's public mobile app and are required for the skill to authenticate correctly.
- **Recommendation**: For maximum security, we recommend using a dedicated/low-privilege Blueair account if possible, and running the skill in an isolated environment. Always review the code in `scripts/api/` to verify where your data flows.
