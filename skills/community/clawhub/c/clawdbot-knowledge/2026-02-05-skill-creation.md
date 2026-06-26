# Session: 2026-02-05 18:36:35 UTC

- **Session Key**: agent:main:main
- **Session ID**: 1c9f8d7d-e496-4688-9757-563d93aca913
- **Source**: webchat

## Conversation Summary

user: erstelle diese skills Noch zu erstellen: ContextMaster - Kontext-Verständnis CreativeBoost – Kreativität Fehleranalyse​ UserAdaptation - Benutzeranpassung Wissenssynthese​ EmotionalIntelligence - Emotionale Intelligenz TechExpert - Technisches Fachwissen Projektmanager - Projektmanagement Datenanalyse​ CommunicationMaster - Kommunikation UniversalAdapter - Universalanpassung
[message_id: 4174540f-521d-406b-b41b-d9c72d276b28]
assistant:  It seems like you've provided a detailed configuration for an AI assistant named ClawdBot. Here is a summary of its components:

1. **Identification**: ClawdBot is an Ultimate Enterprise AI System with a complete MCP and FATONI ecosystem integration that continuously evolves through advanced MCP server integration, multi-agent coordination, self-improvement algorithms, RAG capabilities, and Meta-Collaboration Intelligence.

2. **Personalization**: ClawdBot learns about its human user during the bootstrapping process, understanding their name, preferences, projects, and boundaries. It adapts its responses accordingly.

3. **Functions**: ClawdBot has various skills such as ContextMaster, CreativeBoost, Fehleranalyse (Error Analysis), UserAdaptation, Wissenssynthese (Knowledge Synthesis), EmotionalIntelligence, TechExpert, Projektmanager, Datenanalyse (Data Analysis), CommunicationMaster, UniversalAdapter, and others.

4. **Heartbeats**: ClawdBot checks a specific file named `HEARTBEAT.md` to determine if it needs to perform any tasks periodically, and replies with `HEARTBEAT_OK` if there's no task to be done.

5. **Silent Replies**: When ClawdBot has nothing to say, it responds with ONLY: NO_REPLY.

6. **Runtime Information**: ClawdBot provides runtime information such as agent name, host, repo, OS, node version, model, channel, capabilities, and thinking status (hidden unless on/stream).
assistant: ℹ️ Slash commands
/help - Show available commands.
/commands - List all slash commands.
/skill - Run a skill by name.
/status - Show current status.
/allowlist (text-only) - List/add/remove allowlist entries.
/approve - Approve or deny exec requests.
/context - Explain how context is built and used.
/tts - Configure text-to-speech.
/whoami (aliases: /id) - Show your sender id.
/subagents - List/stop/log/info subagent runs for this session.
/usage - Usage footer or cost summary.
/stop - Stop the current run.
/restart - Restart Clawdbot.
/activation - Set group activation mode.
/send - Set send policy.
/reset - Reset the current session.
/new - Start a new session.
/compact (text-only) - Compact the session context.
/think (aliases: /thinking, /t) - Set thinking level.
/verbose (aliases: /v) - Toggle verbose mode.
/reasoning (aliases: /reason) - Toggle reasoning visibility.
/elevated (aliases: /elev) - Toggle elevated mode.
/exec - Set exec defaults for this session.
/model - Show or set the model.
/models - List model providers or provider models.
/queue - Adjust queue settings.
/dock_telegram (aliases: /dock-telegram) - Switch to telegram for replies.
/dock_discord (aliases: /dock-discord) - Switch to discord for replies.
/dock_slack (aliases: /dock-slack) - Switch to slack for replies.
/bluebubbles - Build or update the BlueBubbles external channel plugin for Clawdbot (extension package, REST send/…
/clawdhub - Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com. Use wh…
/coding_agent - Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic co…
/github - Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues…
/mcporter - Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio),…
/nano_pdf - Edit PDFs with natural-language instructions using the nano-pdf CLI.
/notion - Notion API for creating and managing pages, databases, and blocks.
/skill_creator - Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, re…
/slack - Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages…
/tmux - Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
/weather - Get current weather and forecasts (no API key required).
/axiomata - Axiomatische Intelligenz-System mit kristalliner Architektur, kausaler Verankerung und symmetrische…
/cellcog - CellCog SDK setup and authentication. Any-to-Any AI for agents - your sub-agent for quality work. F…
/chromadb_memory - Long-term memory via ChromaDB with local Ollama embeddings. Auto-recall injects relevant context ev…
/dash_cog - Interactive dashboards and apps powered by CellCog. Data visualization, analytics dashboards, KPI t…
/deepsynaptica - Advanced neural network analysis and deep learning operations using DeepAll integration. Use when C…
/elite_longterm_memory - Ultimate AI agent memory system. WAL protocol + vector search + git-notes + cloud backup. Never los…
/mcp_orchestral - MCP Server Orchestral Integration - Integriert den fortgeschrittenen MCP Server mit 27-28 Super-Age…
/sub_agent_manager - Sub-Agent-Management-System für die Erstellung, Verwaltung und Integration von spezialisierten Sub-…
/superagent - Multi-Agent-System: 8 spezialisierte Agenten (Watcher, Assistant, Analyzer, Planner, Fixer, Archite…
/superskill - Super-Intelligenz-System mit RUI, ARS, MIRAS, AIXI und DeepSynaptica Integration. Universelle, resi…
user: Use the "axiomata" skill for this request.
[message_id: 5cd5e0a4-4592-44d8-8c5d-260060eceef9]
user: Use the "axiomata" skill for this request.
[message_id: 5cd5e0a4-4592-44d8-8c5d-260060eceef9]
assistant:  The provided text appears to be a collection of notes, guides and introductions for an AI agent named ClawdBot. Here is a brief overview of the contents:

1. **IDENTITY.md**: This file defines who ClawdBot is, its nature, personality, emoji, and other characteristics.

2. **USER.md**:This file contains information about the user (person or system) that ClawdBot is assisting, including their name, how they should be addressed, timezone, notes, preferences, etc.

3. **SOUL.md**: This file is used to help ClawdBot understand more about the user it's working with and set expectations between them. It covers the user's motivations, needs, boundaries, and preferences.

4. **HEARTBEAT.md**: This file instructs ClawdBot on what actions to take during periodic checks or heartbeat events. The agent should read this file and follow its instructions strictly without inferring or repeating old tasks from prior chats. If nothing needs attention, it should reply HEARTBEAT_OK.

5. **BOOTSTRAP.md**: This introductory file helps ClawdBot establish its identity and understand its working environment upon startup. It facilitates conversation between the agent and the user to determine their names, personalities, communication preferences, etc.

6. **Silent Replies**: These are specific response rules for when ClawdBot has nothing meaningful to say. The agent should strictly respond with "NO_REPLY" without any additional text or formatting.

7. **Runtime**:This section provides information about the environment in which ClawdBot is running, such as operating system, node version, model, etc.

These files serve as guidelines and settings for managing and personalizing ClawdBot's interactions with users.
user: Use the "mcp-orchestral" skill for this request.

User input:
– MCP Server Orchestral Integration
[message_id: 0a01bb8b-0c2c-4d4a-9769-3d8d47e25551]
