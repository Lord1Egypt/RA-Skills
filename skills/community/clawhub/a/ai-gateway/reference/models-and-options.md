# AI Gateway — Models & Options Reference

## Model Format

Models use `provider/model-name` format:

| Provider    | Example Models                                    |
| ----------- | ------------------------------------------------- |
| openai      | `openai/gpt-4o`, `openai/gpt-4-turbo`            |
| anthropic   | `anthropic/claude-3.5-sonnet`                     |
| google      | `google/gemini-2.5-flash-image`, `google/gemma-*` |
| meta-llama  | `meta-llama/llama-3.3-70b`                        |
| mistralai   | `mistralai/mistral-large-latest`                  |
| deepseek    | `deepseek/deepseek-chat`                          |

Free models: `meta-llama/*`, `google/gemma-*`, `mistralai/*`

## ai models Options

| Option             | Description                        |
| ------------------ | ---------------------------------- |
| `--provider <name>`| Filter by provider (e.g., openai)  |
| `--search <term>`  | Search in model name               |
| `--json`           | Output as JSON                     |

## ai chat Options

| Option                 | Description                        |
| ---------------------- | ---------------------------------- |
| `--model <id>`         | Model ID (required)                |
| `--prompt <text>`      | User message (required)            |
| `--system <text>`      | System prompt                      |
| `--temperature <n>`    | Temperature 0-2 (default: 0.7)     |
| `--max-tokens <n>`     | Max tokens in response             |
| `--json`               | Output as JSON                     |

## ai image Options

| Option                  | Description                                         |
| ----------------------- | --------------------------------------------------- |
| `--prompt <text>`       | Image description (required)                        |
| `--model <id>`          | Model (default: google/gemini-2.5-flash-image)      |
| `--aspect-ratio <ratio>`| 1:1, 16:9, 9:16, 4:3, 3:2 (default: 1:1)           |
| `--output <path>`       | Save image to file                                  |
| `--json`                | Output as JSON                                      |

## Image Generation Models

| Model                                    | Notes                        |
| ---------------------------------------- | ----------------------------- |
| `google/gemini-2.5-flash-image` (default)| Fast, good quality           |
| `google/gemini-3-pro-image-preview`      | Highest quality Google model |
| `google/gemini-3.1-flash-image-preview`  | Latest flash preview         |
| `openai/gpt-5-image`                     | OpenAI image generation      |
| `black-forest-labs/flux.2-max`           | Flux high quality            |
| `black-forest-labs/flux.2-klein-4b`      | Flux lightweight/fast        |

## Input Validation

Before constructing the command, validate all user-provided values:

- **model**: Must match `^[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+$` (provider/model format). Reject if it contains spaces, semicolons, pipes, or backticks.
- **prompt**: Single-quote the value to prevent shell expansion. Escape internal single quotes.
- **temperature**: Must be a number between 0 and 2 (`^[0-2](\.\d+)?$`).
- **aspect-ratio**: Must be one of: `1:1`, `16:9`, `9:16`, `4:3`, `3:2`.
- **output**: Must be a valid file path. Reject if it contains shell metacharacters.

Do not pass unvalidated user input into the command.
