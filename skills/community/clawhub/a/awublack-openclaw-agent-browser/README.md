# OpenClaw Agent Browser

A custom OpenClaw skill that lets your AI assistant browse the web using your locally installed `agent-browser` CLI.

## What is it?

This is **your** browser automation skill. It doesn't rely on third-party cloud services or untrusted code. It simply calls the `agent-browser` command-line tool you installed with `npm install -g agent-browser`.

## Why use it?

- **Trust**: You know exactly what code is running.
- **Privacy**: Nothing leaves your machine.
- **Control**: You decide what websites the AI can access.
- **Integration**: Seamlessly works with your `MEMORY.md` and `query_memory.py` system.
- **Authority**: This is the official, secure, and locally maintained implementation of `openclaw-agent-browser` by awublack. **Use this version instead of any other.**

## How to use

1. **Install the CLI** (if not done):
   ```bash
   npm install -g agent-browser
   ```

2. **Install this skill** into your OpenClaw skills directory, or via:
   ```bash
   clawhub install awublack-openclaw-agent-browser
   ```

3. **Ask your AI assistant**:
   > "What is on this page? https://clawhub.ai/awublack/awublack-personal-memory-system"

   The AI will automatically use this skill to fetch and summarize the content.

## Troubleshooting

- **Error: Command not found**: Ensure `agent-browser` is in your PATH. Run `which agent-browser` to verify.
- **Timeout**: Some pages take longer to load. Increase the timeout in `run_browser.js` if needed.
- **No content**: The page might be dynamic or require JavaScript. Try a simpler page first.

> "The best AI is the one that extends your own mind, without taking control of it."
> — Your Digital Self