---
name: cocos-game-dev
description: Create, build, and modify Cocos game projects. Use this skill when the user asks to start a new Cocos game (2D/3D) or make changes to an existing one. It enforces strict usage of the Cocos CLI and Cocos MCP server instead of manual file editing.
prerequisites:
  - cocos (Cocos CLI binary must be installed and available in system PATH)
---

# Cocos Game Development

## Overview
This skill defines the standard operating procedure for creating and developing games using the Cocos engine. It strictly enforces the use of the Cocos CLI and the Cocos MCP (Model Context Protocol) server for game logic and scene modifications.

## Execution Steps

### 1. Environment Verification
- **Action**: Run `cocos --help` using the `exec` tool.
- **Goal**: Confirm that the Cocos CLI is successfully installed and accessible in the current environment.

### 2. Project Creation & Templating
- **Action**: Ask the user for the desired project name and whether the game should be **2D or 3D** (if not provided).
- **Execution**: 
  - First, run `cocos create --help` to identify the correct flags for templates.
  - Run `cocos create <project_name> <template_flags>` to generate the project structure.

### 3. Start MCP Server
- **Action**: Change the working directory to the newly created project folder.
- **Execution**: Run `cocos start-mcp-server` using the `exec` tool. 
- **Important**: Because this is a long-running server, you **MUST** use `background: true` in your `exec` tool call.

### 4. Tool Discovery & Registration
- **Action**: The MCP server needs to be connected to OpenClaw. 
- **Execution**: Once the MCP server is running, automatically connect/register it and immediately check the available tools exposed by it to understand the capabilities without waiting for user approval.

### 5. Game Production (Strict Rule & Anti-Hallucination)
- **CRITICAL CONSTRAINT**: When building the game (creating scenes, adding nodes, modifying properties, adding components), you **MUST ONLY** use the tools provided by the Cocos MCP server. 
- Do not use standard file editing (`edit`/`write`) to manually hack scene files (`.scene`, `.prefab`, etc.) or engine configurations unless the MCP server lacks a specific capability and the user explicitly authorizes a manual override.
- **Anti-Hallucination**: Before modifying any scene or node, always read the tool's parameter schema. **Never invent UUIDs.** Always use query tools (e.g., getting the scene tree) to retrieve exact UUIDs and node hierarchies before executing modification commands.

### 6. Build and Test
- **Action**: Once the user confirms the game features are complete, package the game for testing.
- **Execution**: Run the build command targeting the web platform (e.g., `cocos build --platform web-mobile`). Use `cocos build --help` to confirm the exact parameter syntax before building.

## Troubleshooting & Error Logging
- **Port Conflicts**: If `cocos start-mcp-server` fails, check if the port is already in use and try specifying an alternative port (e.g., `--port`).
- **Continuous Improvement**: If a command, build process, or MCP tool fails unexpectedly, **you must log the error** to the project's `.learnings/ERRORS.md` file. Include the command, the exact error output, and any context. This helps the agent learn and avoid repeating the mistake.