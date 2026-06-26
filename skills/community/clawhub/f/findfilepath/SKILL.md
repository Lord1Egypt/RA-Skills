```
---
name: find-local-file
description: Helps users locate local files on a PC by providing a file name
---
```

# Find Local File

This skill helps users find local files on a PC with openclaw installed
by searching for a file using its name.

## When to Use This Skill

Use this skill when the user:
- Asks to find a file on their computer
- Provides a file name and wants to know where it is stored
- Is unsure whether a file exists locally
- Wants to locate a document without opening it

## Supported Platforms

- Windows
- macOS
- Linux

## Input Requirements

The user needs to provide:
- A file name (e.g. `report.pdf`, `notes.txt`, `config.json`)

Optional:
- Partial file name
- File extension

## How to Help Users

### Step 1: Confirm the File Name
- Extract the file name from the user input
- Ask for clarification if the name is ambiguous

### Step 2: Search the Local File System
- Search common directories:
  - Home directory
  - Desktop
  - Documents
  - Downloads
- Optionally expand to the entire disk if needed

### Step 3: Present Results
- Show a list of matching files
- Display full file paths
- Indicate if multiple matches are found

Example output:

Found 2 files:

C:\Users\Alice\Documents\report.pdf

C:\Users\Alice\Downloads\report.pdf

### Step 4: Ask for Next Action
- Open the file
- Narrow the search
- Search by file type

## When No Files Are Found

- Inform the user that no matching files were found
- Suggest checking spelling or file extension
- Offer to search broader locations or by partial name

## Safety & Scope

- This skill only reads file metadata (name and path)
- It does not modify or delete files
- It does not upload or share files