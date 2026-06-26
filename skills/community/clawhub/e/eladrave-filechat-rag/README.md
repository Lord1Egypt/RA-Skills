# FileChat RAG

A powerful Retrieval-Augmented Generation (RAG) AgentSkill for OpenClaw. 

This skill connects to a Google Drive folder, recursively downloads all files (resolving shortcuts), extracts text (including text from images via OCR), chunks it, embeds it with Gemini, and saves it to a persistent local vector database.

## Features
- Deep sync with Google Drive folders and sub-folders
- Resolves Google Drive Shortcuts automatically
- OCRs image text automatically using Gemini Flash
- Reads PDFs natively
- Local Cosine-Similarity Vector Search (No external vector DB required)

## Usage
Once installed, the agent will ask for:
1. Your Google Gemini API Key
2. The Google Drive Folder ID you want to index

Then, just tell your agent to `sync`, and you can start chatting with your entire document library immediately!
