# genealogy-agent

A powerful agent skill for extracting, structuring, researching, and visualizing family history from raw text (memoirs, archives, chat logs).

## Features
- **LLM Extraction**: Parses unstructured text to find people, dates, locations, and relationships.
- **Knowledge Graph**: Stores family data in a local JSONL ontology graph.
- **Obsidian Vault Generation**: Automatically generates an Obsidian-compatible vault (Markdown files with YAML frontmatter) for your family tree.
- **Auto-Research**: Autonomously searches global and regional databases (FamilySearch, Ancestry, OBD Memorial, Geneteka, etc.) to find new facts about ancestors.
- **GEDCOM Export**: Exports your family tree to the standard `.ged` format for use in MyHeritage, FamilySearch, or any desktop genealogy software.
- **Mermaid Visualization**: Automatically generates beautiful family tree diagrams.

## Setup
1. Install dependencies: `uv pip install pydantic litellm duckduckgo-search`
2. Set your preferred LLM provider (e.g., `OPENAI_API_KEY` or `GEMINI_API_KEY`).

## Usage
You can ask the agent to:
- "Extract family members from this text: [text]"
- "Generate an Obsidian vault from my family data"
- "Research my great-grandfather Ivan Ivanov born in 1910"
- "Export my family tree to GEDCOM"

## Tools
- `extract_family_data`: Extracts structured family data from raw text.
- `build_family_graph`: Saves extracted data into the local ontology graph.
- `generate_obsidian_vault`: Generates an Obsidian-formatted vault from extracted family data.
- `research_ancestor`: Autonomously researches an ancestor using web search and LLM extraction.
- `export_gedcom`: Exports extracted family data to a standard GEDCOM (.ged) file.
- `generate_mermaid_tree`: Generates a Mermaid diagram from the graph.