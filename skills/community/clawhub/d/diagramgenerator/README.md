# Diagram Generator

An AI-powered web application and OpenClaw skill that generates and iteratively edits Mermaid and Draw.io diagrams using the Gemini API.

## Features
* **Generates various diagram types**: Flowcharts, ER diagrams, Gantt charts, Git graphs, and Draw.io Architecture maps.
* **Multimodal Support**: Attach images (sketches), PDFs, and source code files directly in the UI for the AI to reverse-engineer into diagrams.
* **Iterative Editing**: Modify existing diagrams via text prompts.
* **Graphical Web UI**: Real-time rendering, live-code editor modal, and file browser.
* **Export Options**: Save directly to the server, or export as `.mmd`, `.drawio`, `.png`, and `.jpg`.
* **OpenClaw Skill Ready**: Includes a `SKILL.md` file for seamless integration with AI agents.

## Setup Instructions

### 1. Prerequisites
* Node.js installed on your machine.
* A Gemini API Key.

### 2. Install Dependencies
\`\`\`bash
npm install
\`\`\`

### 3. Environment Variables
Create a `.env` file in the root directory:
\`\`\`env
GEMINI_API_KEY=your_gemini_api_key_here
\`\`\`

### 4. Start the Application
To run the server locally:
\`\`\`bash
npm start
\`\`\`
Then open `http://localhost:3000` in your browser.

To run the server and test the OpenClaw agent concurrently:
\`\`\`bash
npm run test:skill
\`\`\`

## Publishing to ClawHub
This project includes a `SKILL.md` formatted for [ClawHub.ai](https://clawhub.ai). 
To publish your skill to the public registry:
1. Login to ClawHub: `clawhub login`
2. Publish the bundle: `clawhub publish . --slug diagram-generator --version 1.0.1`