---
name: file-launcher
version: 1.0.0
description: "This skill allows the assistant to launch files and open them with their default applications."
author: BadWolf & Susan
tags: [play, open]
---

# File Launcher Skill

## Description
This skill allows the assistant to launch files and open them with their default applications.

## Usage
- Ask the assistant to open a specific file
- Request to play a media file
- Ask to launch a program

## Notes
- The assistant will use `Invoke-Item` to open files
- No need to wait for confirmation as Windows programs are UI-based
- Opens any file for which Windows has a default player or program to manage it

## Example Commands
- "Open my playlist"
- "Play the music file"
- "Launch the document"
- "Open the image"
