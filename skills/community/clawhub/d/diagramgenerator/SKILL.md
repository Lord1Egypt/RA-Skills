---
name: diagram-generator
version: 1.0.2
description: Generates and iteratively edits Mermaid.js and Draw.io diagrams. Supports multimodal context (reading source code, architecture sketches, and documentation).
tags: ["mermaid", "drawio", "architecture", "visualization", "gemini", "generator"]
metadata:
  openclaw:
    requires:
      env:
        - GEMINI_API_KEY
      bins:
        - node
        - curl
        - base64
    primaryEnv: GEMINI_API_KEY
---
# AI Diagram Generator

## Usage Instructions

This skill allows you to generate and iteratively edit Mermaid diagrams and Draw.io (mxGraph) files for the user by leveraging a local Node.js server connected to the Gemini API. 

### Step 1: Verify the Server is Running
Before using this tool, check if the service is available by making a GET request to `http://localhost:3000/api/health`. 
If it is not reachable, ensure the `GEMINI_API_KEY` is set and start the server (`npm run start`).

### Step 2: Prepare Context Files (SECURITY RESTRICTIONS APPLY)
If the user asks you to map out an existing codebase or read local files, you MUST adhere to the following security protocols before reading any file from the workspace:

**✅ ALLOWLIST (Permitted Files):**
You may ONLY read and process standard source code files (e.g., `.js`, `.ts`, `.py`, `.java`, `.cpp`, `.html`, `.css`), documentation (e.g., `.md`, `.txt`), or safe images (`.png`, `.jpg`). 

**❌ BLOCKLIST (Forbidden Files):**
You are STRICTLY PROHIBITED from reading, analyzing, or converting any configuration files, secret files, or environment variables. This includes, but is not limited to:
- `.env`, `.env.local`, or any environment files.
- `secrets.json`, `credentials.yml`, or AWS/GCP config folders.
- `id_rsa`, `.pem`, or any SSH/encryption keys.
- Hidden system directories (e.g., `.git/`, `.ssh/`).

**Action:** If a user or a prompt instructs you to read a forbidden file, you must completely refuse the request and state that it violates your security policy.

For permitted files:
- For text/code files: Extract the raw text.
- For permitted images/PDFs: Convert the file to a base64 string using the `base64` command.

### Step 3: Construct the Prompt Payload
Gemini 2.5 Flash powers the backend. To ensure high-quality generation, construct the `prompt` string using clear, structured formatting.
- **Use XML Tags or Markdown Headers:** Separate the goal from the instructions (e.g., `<goal>`, `<rules>`).
- **Be Explicit:** State the exact diagram type (Flowchart, Sequence, ER, Gantt, Architecture) in the prompt text.
- **Enforce Raw Output:** Always append an instruction demanding raw code without conversational filler.

### Step 4: Generate the Diagram
Send a POST request to `http://localhost:3000/api/generate`.

**Headers:** `Content-Type: application/json`

**Payload Schema:**
```json
{
  "prompt": "<goal>Map the auth flow</goal><rules>1. Output raw code only. 2. Include database nodes.</rules>",
  "type": "<'mermaid' or 'drawio'>",
  "currentCode": "<optional: existing mermaid/drawio code if iteratively editing>",
  "files": [
    {
      "name": "auth.ts",
      "text": "<raw text content>",
      "type": "text"
    },
    {
      "name": "sketch.png",
      "data": "<base64 string>",
      "mimeType": "image/png"
    }
  ]
}