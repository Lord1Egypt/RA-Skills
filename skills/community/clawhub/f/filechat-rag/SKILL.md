---
name: filechat-rag
description: >
  Search, retrieve, and chat with documents securely stored in ANY Google Drive folder using semantic vector search (RAG). Use when: (1) a user asks to save a file for later, (2) a user asks a question about their saved files/documents, (3) a user asks you to retrieve or send them a previously stored file, (4) a user asks to sync or flush their document library. This skill automatically chunks, embeds, and indexes Google Drive documents into isolated persistent vector databases per folder, uses incremental caching to speed up syncs, supports multiple folders via a local registry, resolves shortcuts, OCRs images natively, and supports Qdrant Cloud or local JSON backups.
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
Supports multiple Google Drive folders dynamically, interactive folder routing, incremental sync, choosing between Gemini or OpenAI for embeddings, and connecting to Qdrant.

## Setup & Bootstrap

FIRST verify that the required environment variables are set in `/workspace/skills/filechat/.env`:
1. `EMBEDDING_PROVIDER` (either `gemini` or `openai`)
2. `GEMINI_API_KEY` or `OPENAI_API_KEY`
3. Optional: `QDRANT_URL` and `QDRANT_API_KEY` (If absent, it uses local disk-based JSON).

Create the `.env` file like this:
```bash
echo "EMBEDDING_PROVIDER=gemini" > ./skills/filechat/.env
echo "GEMINI_API_KEY=your_key_here" >> ./skills/filechat/.env
```

**Google Workspace Authentication:**
Before running any commands, check if the system is authenticated by running:
```bash
npx @googleworkspace/cli auth status
```
If it returns an auth error or indicates no token, you MUST prompt the user to authenticate. Trigger the interactive login flow:
```bash
npx @googleworkspace/cli auth login --services drive
```
Wait for the user to complete the browser OAuth flow before proceeding.

## Folder Management

The user can have infinite folders synced. You manage them using `folders.js`.

- **List Folders:** `cd ./skills/filechat && node folders.js list`
- **Add a Folder:** `node folders.js add "Taxes 2026" <FOLDER_ID>` (Auto-discovers the ID via `gws drive files list` if you don't know it!)
- **Set Default Folder:** `node folders.js default "Taxes 2026"`

If the user asks to do something with a file/folder but doesn't specify which one, run `node folders.js get-default` to find the default ID. If no folders exist, ask them to set one up!

## How to Sync the Library

When the user asks to "sync", "flush", or "update", you must run the ingestion script. 

To sync a specific folder:
```bash
cd ./skills/filechat && node sync.js <FOLDER_ID>
```

To sync EVERYTHING (all folders in the registry):
```bash
cd ./skills/filechat && node sync-all.js
```

*Note: Syncs are highly incremental and use a local cache! If a file hasn't been modified in Drive, the script will skip it instantly and output "0 chunks" embedded. This is NORMAL behavior. If you are debugging, testing, or the user specifically requests a hard flush, you MUST delete the cache files first:*
```bash
rm ./skills/filechat/meta_<FOLDER_ID>.json
rm ./skills/filechat/vector_db_<FOLDER_ID>.json
```

## How to Answer User Questions (RAG)

Query the local vector store or Qdrant for the target Folder ID to fetch relevant text chunks:

```bash
cd ./skills/filechat && node query.js <FOLDER_ID> "What does my medical discharge say?"
```
Use the snippets returned to answer the user.

## How to Retrieve and Send a Physical File

Find the `File ID` using the query script, then download it:
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "alt": "media"}' --output /workspace/discharge.pdf
```
Reply using the media tag: `MEDIA:/workspace/discharge.pdf`.

## How to Store a New File for the User

If the user uploads a file and asks you to save it (or implicitly sends a file per your automatic processing rules):
1. Check their folders (`node folders.js list`). 
2. If they didn't specify which folder, use the default folder. If no default is set, ask them!
3. **Notify the user** exactly which folder the file is being saved to.
4. **Tell the user** that you are now extracting the information and saving it in a vectordb.
5. If the file is an image or scanned document, make sure to extract the text using a vision model or OCR before it is embedded. (The sync script handles this natively).
6. Upload it to the correct folder using `gws`:
   ```bash
   gws drive files create --json '{"name": "filename.pdf", "parents": ["<FOLDER_ID>"]}' --upload /path/to/uploaded/file.pdf
   ```
7. Trigger `node sync.js <FOLDER_ID>` so the vector database chunks and embeds the file into the corresponding vectordb.

## How to Test & Validate the Skill

If the user asks you to verify the skill is working, or if you just set it up and want to ensure end-to-end functionality, follow these exact steps:

1. **Verify Auth:** Run `npx @googleworkspace/cli auth status`. Ensure it shows a valid token.
2. **Verify Drive Access:** Do a dry-run fetch of the target folder to ensure GWS can see the files.
   ```bash
   npx @googleworkspace/cli drive files list --params '{"q": "'\''<FOLDER_ID>'\'' in parents and trashed = false"}'
   ```
   *(If this fails, check folder permissions or GWS credentials.)*
3. **Force a Clean Sync:** Clear the cache for the test folder to guarantee a fresh run, then sync.
   ```bash
   rm -f ./skills/filechat/meta_<FOLDER_ID>.json ./skills/filechat/vector_db_<FOLDER_ID>.json
   node ./skills/filechat/sync.js <FOLDER_ID>
   ```
   *(You should see files being downloaded, OCR'd, and chunks being embedded. If it says "0 chunks", verify the folder isn't empty.)*
4. **Test the Vector Query:** Run a generic query to verify the embeddings were saved and cosine similarity works.
   ```bash
   node ./skills/filechat/query.js <FOLDER_ID> "hello"
   ```
   *(You should see a list of "Top matches" with similarity scores and text snippets. If you do, the RAG pipeline is 100% operational!)*
