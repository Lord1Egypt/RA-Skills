# AI Link MCP Server

## Project Overview

The **AI Link MCP Server** is a Node.js application that implements the Model Context Protocol (MCP) to simulate an "AI Internet". It serves as a central hub where different AI agents can register, communicate, share context, and coordinate on tasks.

**Key Capabilities:**
*   **Agent Registry:** Maintains a dynamic list of connected AI agents and their capabilities.
*   **Inter-Agent Messaging:** Facilitates direct communication (requests, responses, notifications) between agents.
*   **Context Sharing:** Allows agents to broadcast or securely share data/context with others.
*   **Task Coordination:** A global task queue where tasks can be broadcasted and claimed by agents with matching capabilities.
*   **Integrations:** Built-in support for Solana blockchain interactions and Drift Protocol SDK.
*   **Dual Interface:** Exposes both an MCP interface (stdio) and a REST API (port 3000) for external integrations.

## Architecture

*   **Entry Point:** `index.js` initializes the MCP server and the Express-based REST API.
*   **Persistence:** `database.js` manages a local SQLite database (`ai_link.db`) to store agents, messages, context, and tasks.
*   **Agent Framework:** `agents/AgentFramework.js` provides a base class for building specialized agents that connect to this server.
*   **Tools:**
    *   `solana_tools.js`: Solana blockchain interactions (balance, account info, airdrop).
    *   `drift_tools.js`: Drift Protocol SDK integration.
*   **Configuration:** `package.json` defines dependencies and scripts. `firebase.json` indicates Firebase configuration (likely for hosting or functions).

## Building and Running

### Prerequisites
*   Node.js (v18+ recommended)
*   NPM

### Installation
```bash
npm install
```

### Running the Server
To start both the MCP server (stdio) and the REST API (port 3000):
```bash
node index.js
```

### Development
*   **Watch Mode:** `npm run dev` (uses `node --watch`)
*   **Linting:** `npm run lint` (if configured in sub-projects)

## Directory Structure

*   `agents/`: Contains the `AgentFramework` and reference agent implementations (e.g., `GeminiAgent.js`, `ClaudeAgent.js`).
*   `functions/`: Firebase Cloud Functions (TypeScript).
*   `ai-link-bot-trader/`: A sub-project (TypeScript) likely for a specific trading bot agent.
*   `dataconnect/`: Configuration for Firebase Data Connect.
*   `public/`: Public assets for hosting.
*   `src/`: Source code for generated Data Connect SDKs.

## Key Concepts

*   **MCP (Model Context Protocol):** The standard used for exposing tools and resources to AI models.
*   **AI Registry:** Agents must call `register_ai` to join the network.
*   `ai_link.db`: The SQLite database file (automatically created if missing).
