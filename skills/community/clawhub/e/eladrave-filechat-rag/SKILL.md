---
name: filechat-rag
description: >
  Search, retrieve, and chat with documents securely stored in ANY Google Drive folder using semantic vector search (RAG). Use when: (1) a user asks to save a file for later, (2) a user asks a question about their saved files/documents, (3) a user asks you to retrieve or send them a previously stored file, (4) a user asks to sync or flush their document library. This skill automatically chunks, embeds, and indexes Google Drive documents into isolated persistent vector databases per folder.
metadata:
  openclaw:
    category: "knowledge"
    requires:
      bins: ["node", "npm", "gws"]
    install:
      - id: gws
        kind: node
        package: "@googleworkspace/cli"
        bins: ["gws"]
        label: "Install Google Workspace CLI"
      - id: filechat-deps
        kind: script
        script: "cd ./skills/filechat && npm install"
        label: "Install FileChat Dependencies"
---

# FileChat RAG Skill

Your personal RAG (Retrieval-Augmented Generation) document library backed by Google Drive.
Supports multiple Google Drive folders dynamically and allows choosing between Gemini or OpenAI for embeddings.

## Setup & Bootstrap

If the user asks to use FileChat or asks a question about their files, FIRST verify that the required environment variables are set in `/workspace/skills/filechat/.env`:
1. `EMBEDDING_PROVIDER` (either `gemini` or `openai`)
2. `GEMINI_API_KEY` or `OPENAI_API_KEY` (Depending on the provider)

If they are missing, STOP and ask the user to provide them. 
Create the `.env` file like this:
```bash
echo "EMBEDDING_PROVIDER=gemini" > ./skills/filechat/.env
echo "GEMINI_API_KEY=your_key_here" >> ./skills/filechat/.env
```

## How to Sync the Library

When the user asks to "sync", "flush", or "update" a specific FileChat folder, you must run the ingestion script. This connects to Google Drive, downloads all new/changed files (including PDFs, resolving shortcuts, and traversing sub-folders), chunks the text, gets embeddings, and saves them to a local JSON vector database keyed by the Folder ID.

You must supply the `FOLDER_ID` to the script. If you don't know the folder ID the user wants, ask them.

```bash
cd ./skills/filechat && node sync.js <FOLDER_ID>
```

## How to Answer User Questions (RAG)

When a user asks a question about the contents of their documents, you MUST query the local vector store to fetch the relevant text chunks. You need the Folder ID.

```bash
cd ./skills/filechat && node query.js <FOLDER_ID> "What does my medical discharge say?"
```
The output will give you the most relevant text snippets, the original file names, and the Google Drive File IDs. Use the text snippets to formulate a comprehensive answer for the user. Always cite the file name you are referencing.

## How to Retrieve and Send a Physical File

If the user asks for the actual file (e.g., "Send me the discharge PDF"), first find the `File ID` using the query script.

Then, use the `gws` CLI to download the file into your workspace:
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "alt": "media"}' --output /workspace/discharge.pdf
```
Then, reply to the user using the OpenClaw media attachment syntax: `MEDIA:/workspace/discharge.pdf` to send the physical file directly to their chat window.

## How to Store a New File for the User

If the user uploads a file and asks you to "store" or "save" it:
1. Upload it to their specific FileChat Google Drive folder using `gws`:
   ```bash
   gws drive files create \
     --json '{"name": "filename.pdf", "parents": ["<FOLDER_ID>"]}' \
     --upload /path/to/uploaded/file.pdf
   ```
2. Trigger the sync process so the new file is immediately readable by the vector database:
   ```bash
   cd ./skills/filechat && node sync.js <FOLDER_ID>
   ```

