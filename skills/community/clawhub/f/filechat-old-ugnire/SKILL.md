---
name: filechat
description: >
  Search, retrieve, and chat with documents securely stored in a designated Google Drive folder using semantic vector search (RAG RAG). Use when: (1) a user asks to save a file for later, (2) a user asks a question about their saved files/documents, (3) a user asks you to retrieve or send them a previously stored file, (4) a user asks to sync or flush their document library. This skill automatically chunks, embeds, and indexes Google Drive documents into a local persistent ChromaDB instance.
metadata:
  openclaw:
    category: "knowledge"
    requires:
      bins: ["node", "npm", "gws"]
      env: ["GEMINI_API_KEY", "FILECHAT_DRIVE_FOLDER_ID"]
    install:
      - id: gws
        kind: node
        package: "@googleworkspace/cli"
        bins: ["gws"]
        label: "Install Google Workspace CLI"
      - id: filechat-deps
        kind: script
        script: "cd ./skills/filechat && npm install"
        label: "Install FileChat Dependencies (ChromaDB, Gemini API, PDF-Parse)"
---

# FileChat Skill

Your personal RAG (Retrieval-Augmented Generation) document library backed by Google Drive.

## Setup & Bootstrap

If the user asks to use FileChat or asks a question about their files, FIRST verify that the required environment variables are set in `/workspace/skills/filechat/.env`:
1. `GEMINI_API_KEY` (For the embedding model `text-embedding-004`)
2. `FILECHAT_DRIVE_FOLDER_ID` (The root Google Drive folder ID to index)

If they are missing, STOP and ask the user to provide them. 
(To find the folder ID, they can look at the URL of the folder in Google Drive: `https://drive.google.com/drive/folders/<FOLDER_ID>`)

Create the `.env` file like this:
```bash
echo "GEMINI_API_KEY=your_key_here" > ./skills/filechat/.env
echo "FILECHAT_DRIVE_FOLDER_ID=your_folder_id_here" >> ./skills/filechat/.env
```

## How to Sync the Library

When the user asks to "sync", "flush", or "update" their FileChat library, you must run the ingestion script. This connects to Google Drive, downloads all new/changed files (including PDFs, resolving shortcuts, and traversing sub-folders), chunks the text, gets embeddings, and saves them to a local ChromaDB.

```bash
cd ./skills/filechat && node sync.js
```
*(Warning: The first sync may take a few minutes depending on the folder size.)*

## How to Answer User Questions (RAG)

When a user asks a question about the contents of their documents (e.g., "What does my medical discharge say?"), you MUST query the local ChromaDB vector store to fetch the relevant text chunks.

```bash
cd ./skills/filechat && node query.js "What does my medical discharge say?"
```
The output will give you the most relevant text snippets, the original file names, and the Google Drive File IDs. 
Use the text snippets to formulate a comprehensive answer for the user. Always cite the file name you are referencing.

## How to Retrieve and Send a Physical File

If the user asks for the actual file (e.g., "Send me the discharge PDF"), first find the `File ID` using the query script (if you don't already know it).

Then, use the `gws` CLI to download the file into your workspace:
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "alt": "media"}' > /workspace/discharge.pdf
```
Then, reply to the user using the OpenClaw media attachment syntax: `MEDIA:/workspace/discharge.pdf` to send the physical file directly to their chat window.

## How to Store a New File for the User

If the user uploads a file and asks you to "store" or "save" it:
1. Upload it to their FileChat Google Drive folder using `gws`:
   ```bash
   gws drive files create \
     --json '{"name": "filename.pdf", "parents": ["<FILECHAT_DRIVE_FOLDER_ID>"]}' \
     --upload /path/to/uploaded/file.pdf
   ```
2. Trigger the sync process so the new file is immediately readable by the vector database:
   ```bash
   cd ./skills/filechat && node sync.js
   ```

