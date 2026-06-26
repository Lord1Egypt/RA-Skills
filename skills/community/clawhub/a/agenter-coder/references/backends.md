# Agenter Backend Comparison

Use this reference when the user asks which backend to use or wants to understand
the differences.

## Quick summary

| Backend | Provider | Best for | Requirements |
|---------|----------|----------|-------------|
| `anthropic-sdk` | Anthropic | General coding, custom tools | `ANTHROPIC_API_KEY` or AWS Bedrock |
| `claude-code` | Anthropic | Battle-tested file ops, native sandbox | Claude Code CLI installed |
| `codex` | OpenAI | OpenAI models (gpt-5.4, gpt-5.4-mini) | `OPENAI_API_KEY` + Codex CLI |
| `openhands` | Any (litellm) | Any model, full filesystem | OpenHands runtime, `--no-sandbox` |

## Detailed comparison

### anthropic-sdk (default)

- **How it works**: Pure Python using the Anthropic SDK. Runs a custom tool loop
  with file read/write/edit tools, bash execution, and path security.
- **Models**: Claude Sonnet 4, Claude Opus 4, Claude Haiku. Also supports AWS Bedrock.
- **Sandbox**: Enforces `allowed_write_paths` within `cwd` via PathResolver.
- **Custom tools**: Full support — pass tools to the agent and they're available
  to the model.
- **Best for**: Most coding tasks. Good balance of control and capability.

### claude-code

- **How it works**: Wraps the Claude Code SDK (`claude-agent-sdk`). Uses Claude
  Code's own battle-tested tools: Read, Edit, Write, Bash, Glob, Grep.
- **Models**: Whatever Claude Code uses (typically Claude Sonnet 4).
- **Sandbox**: Native OS-level sandbox via Claude Code's built-in sandboxing.
- **Custom tools**: Supported — tools are passed through to Claude Code.
- **Best for**: Users who already use Claude Code and want its familiar tool set.
  Strongest sandboxing.

### codex

- **How it works**: Wraps OpenAI's Codex CLI via MCP (Model Context Protocol).
  Tools are serialized and sent to Codex as MCP servers.
- **Models**: gpt-5.4 (default, best for complex tasks), gpt-5.4-mini (fast mode).
- **Sandbox**: Uses Codex's "workspace-write" mode (writes restricted to workspace).
- **Custom tools**: Supported via MCP server serialization (uses cloudpickle).
- **Best for**: Tasks where OpenAI models excel, or when user prefers OpenAI.

### openhands

- **How it works**: Wraps the OpenHands SDK. Any model supported via litellm.
  Full code execution in an OpenHands runtime environment.
- **Models**: Anything litellm supports — OpenAI, Anthropic, local models, etc.
- **Sandbox**: No sandbox support — must use `--no-sandbox`. OpenHands manages its
  own runtime isolation.
- **Custom tools**: Not supported.
- **Best for**: Users who need a specific model not available in other backends,
  or who want OpenHands' runtime capabilities.
