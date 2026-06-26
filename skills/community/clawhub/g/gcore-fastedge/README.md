# FastEdge Skill

FastEdge skill for building and deploying WebAssembly apps to Gcore FastEdge.

## Installation

```bash
openclaw skill install fastedge
```

## Usage

After installation, Codex will automatically use this skill when you ask about FastEdge, edge computing, or Wasm deployment.

Example prompts:
- "Deploy this to FastEdge"
- "Create a new FastEdge app"
- "Build a Wasm app for edge computing"

## Structure

```
fastedge-skill/
├── SKILL.md                 # Main skill documentation
├── assets/
│   └── rust-template/       # Starter Rust project template
├── scripts/
│   └── build_rust.py        # Build helper script
```

## License

MIT
