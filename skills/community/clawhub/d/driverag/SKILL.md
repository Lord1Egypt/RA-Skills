---
name: driverag
description: Use the Google Drive RAG CLI to search your synced personal documents, add tracking folders, or check the service account status.
---

# Google Drive RAG CLI Skill

## When to use
Use this skill when the user asks you to search their personal documents via the Google Drive RAG API. This includes questions like "What is my Aetna ID?", "Search my drive for...", "Sync my drive", "What is the status of my sync?", "What is the service account email?", or "Renew my token".

## Setup and Initialization
This skill includes a self-contained Python CLI tool in its directory.

Before running any commands, you MUST verify the environment is set up:
1. Check if `~/.agents/skills/driverag/.env` exists. 
   - If it DOES NOT exist, you MUST ask the user to provide their `API_URL` and `JWT_TOKEN`.
   - Once they provide them, create the `.env` file in the skill directory (`~/.agents/skills/driverag/.env`) with those values.
2. Check if the virtual environment exists (`~/.agents/skills/driverag/venv`). 
   - If it DOES NOT exist, create it: `cd ~/.agents/skills/driverag && python3 -m venv venv`
   - Then install the requirements: `source venv/bin/activate && pip install -r requirements.txt`

## Instructions
Once the environment is validated and the `.env` file is created, you can interact with the RAG system using the CLI tool. 

ALWAYS run the CLI from the skill directory (`~/.agents/skills/driverag/`) and ALWAYS activate its virtual environment first.

Here are the commands you can run:

1. **Search documents**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py search "$ARGUMENTS"
   ```
   *If the user passes specific folders, append them:* `python3 cli.py search "$ARGUMENTS" -f "Folder Name"`

2. **List all Indexed Files in the RAG Database**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py list-files
   ```

3. **Check Sync Status**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py status
   ```

4. **Sync documents**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py sync
   ```
   *To force a complete re-download and re-indexing of all files:* `python3 cli.py sync --force`

5. **Get Service Account Email**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py service-account
   ```

6. **Renew Token**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py renew-token
   ```

7. **Add a folder manually**:
   ```bash
   cd ~/.agents/skills/driverag && source venv/bin/activate && python3 cli.py add-folder "$ARGUMENTS"
   ```

## Important notes
- Do NOT hallucinate answers. ALWAYS run the `cli.py search` command to get the exact answer from the RAG system and output the exact response it gives you.
- CRITICAL: If the user asks "What files do you have", "List my files", or "What documents are in the database", DO NOT use the search command! You MUST use the `list-files` command instead, because RAG semantic search cannot generate file lists.
- If the CLI returns a 401 Unauthorized or warns that the token is about to expire, inform the user and automatically run the `renew-token` command to update their `.env` file.
- When outputting the RAG search results to the user, ensure you include the citations/source documents exactly as the CLI returns them so the user knows where the information came from.

## Examples
- "Search my drive for my Aetna ID" -> Run the search command with "What is my Aetna ID?"
- "What files do you have in the database?" -> Run the list-files command.
- "What is the status of my sync?" -> Run the status command.
- "What email should I share my folders with?" -> Run the service-account command.
- "Renew my token" -> Run the renew-token command.
