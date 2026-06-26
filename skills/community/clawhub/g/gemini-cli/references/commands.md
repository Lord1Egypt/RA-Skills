# Gemini CLI Command Reference

## Prerequisites

Before running any commands:
1. **Install Gemini CLI:** Usually pre-installed, or `npm install -g @google/gemini-cli`
2. **Get API Key:** Visit https://aistudio.google.com/app/apikey
3. **Set environment variable:** `export GEMINI_API_KEY="your-key"`

API key is NOT stored in the tool — it's passed via environment variable.

---

## Core Commands

### Chat (Interactive)

```bash
gemini chat                              # Start interactive chat
gemini chat --context ./src              # Chat with codebase context
gemini chat --context ./src --prompt "explain the architecture"  # Direct prompt
```

**Flags:**
- `--context <path>` — Include files/directories for context
- `--prompt <text>` — Ask a question directly (non-interactive)
- `--model <model>` — Use specific model (default: gemini-2.5-pro)
- `--temperature <0-1>` — Creativity level (0=precise, 1=creative)

### Code Analysis

```bash
gemini code --explain ./file.js          # Explain code
gemini code --review ./changes.patch     # Review changes
gemini code --fix ./file.js              # Suggest fixes
gemini code --test ./function.ts         # Suggest tests
```

**Flags:**
- `--explain` — Explain what code does
- `--review` — Review code quality
- `--fix` — Suggest improvements
- `--test` — Generate test suggestions
- `--format <format>` — Output format (json, markdown, text)

### Code Generation

```bash
gemini create --from-image ./design.png  # Code from image
gemini create --from-pdf ./spec.pdf      # Code from PDF
gemini create --template react           # Generate boilerplate
gemini create --lang javascript --prompt "todo app"  # Language-specific
```

**Flags:**
- `--from-image <path>` — Generate from image file
- `--from-pdf <path>` — Generate from PDF document
- `--template <type>` — Use template (react, vue, express, etc.)
- `--lang <language>` — Programming language
- `--prompt <text>` — Describe what you want
- `--output <path>` — Save to file

### Batch Operations

```bash
gemini batch --input tasks.json --output results.json
gemini batch --input ./files/*.js --operation "explain" --output ./docs
```

**Flags:**
- `--input <path>` — Input file(s) or directory
- `--operation <op>` — Operation (explain, review, fix, test)
- `--output <path>` — Output location
- `--parallel <n>` — Run N operations in parallel

### Debug Mode

```bash
gemini debug ./file.js --prompt "why does this crash?"
gemini debug --error "TypeError: undefined is not a function" --context ./src
```

**Flags:**
- `--error <message>` — Error message to debug
- `--context <path>` — Code context for debugging
- `--stack-trace <file>` — Include stack trace

### Workflow Automation

```bash
gemini workflow --steps "analyze, report, suggest-fixes"
gemini workflow --input ./project --output ./report.md
```

---

## Global Options

```bash
--version                    # Show version
--help                      # Show help
--api-key <key>             # Override GEMINI_API_KEY env var
--model <model>             # Specify model (default: gemini-2.5-pro)
--verbose                   # Verbose logging
--quiet                     # Suppress output
--json                      # Output as JSON
--format <format>           # Output format (text, json, markdown)
--save <file>               # Save output to file
```

---

## Common Workflows

### Analyze Your Codebase

```bash
# Get architecture overview
gemini chat --context ./src --prompt "What's the overall architecture?"

# Find potential issues
gemini code --review ./src

# Generate documentation
gemini code --explain ./src --format markdown > architecture.md
```

### Code Review

```bash
# Review specific file
gemini code --review ./src/components/App.tsx

# Review pull request
gemini code --review ./pr.patch

# Suggest tests
gemini code --test ./src/utils/helpers.ts
```

### Generate from Design

```bash
# Screenshot to React component
gemini create --from-image ./design.png --template react

# Multiple designs
for img in designs/*.png; do
  gemini create --from-image "$img" --template react --output "components/$(basename $img).tsx"
done
```

### Document from PDF Spec

```bash
# Create API from spec document
gemini create --from-pdf ./api-spec.pdf --lang typescript --output ./api.ts

# Generate schema from requirements
gemini create --from-pdf ./requirements.pdf --template schema --output ./schema.json
```

### Batch Fix Issues

```bash
# Create list of files to fix
ls src/**/*.js > files.txt

# Process all
gemini batch --input files.txt --operation "fix" --output ./fixed
```

---

## Output Formats

### Text (Default)

```bash
gemini code --explain ./file.js
```

Output: Plain text explanation

### JSON

```bash
gemini code --explain ./file.js --json
```

Output: Structured JSON with explanation, suggestions, etc.

### Markdown

```bash
gemini code --explain ./src --format markdown > docs.md
```

Output: Markdown documentation

### Save to File

```bash
gemini code --review ./src --save review.txt
gemini code --explain ./file.js --save explanation.md
```

---

## Models Available

```bash
--model gemini-2.5-pro          # Latest (default, recommended)
--model gemini-2.0-flash        # Faster, less capable
--model gemini-1.5-pro          # Previous stable
```

---

## API Key Management

### Set for Current Session

```bash
export GEMINI_API_KEY="your-key-here"
gemini chat
```

### Use Inline

```bash
GEMINI_API_KEY="your-key-here" gemini chat
```

### Use from File

```bash
export GEMINI_API_KEY=$(cat ~/.gemini-key)
gemini chat
```

### Override Env Var

```bash
gemini chat --api-key "different-key-here"
```

---

## Troubleshooting

**"API key not found"**
```bash
# Set it
export GEMINI_API_KEY="your-key"
```

**"Quota exceeded"**
- Check https://aistudio.google.com/app/apikey (usage stats)
- Wait for quota reset (usually daily)
- Consider upgrading plan

**"Invalid context path"**
```bash
# Make sure path exists
ls -la ./src
gemini chat --context ./src
```

**"Command not found: gemini"**
```bash
# Reinstall
npm install -g @google/gemini-cli

# Or use npx
npx @google/gemini-cli --help
```

---

## Help

```bash
gemini --help                  # Global help
gemini <command> --help        # Command-specific help
gemini chat --help
gemini code --help
gemini create --help
gemini batch --help
```

**Official Documentation:** https://geminicli.com/docs
