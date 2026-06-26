# Gemini CLI Usage Examples

Make sure to set your API key first:
```bash
export GEMINI_API_KEY="your-api-key"
```

---

## Interactive Conversations

### Chat About Your Project

```bash
cd /path/to/your/project
gemini chat --context ./src

# Then ask questions like:
# "What's the overall architecture?"
# "Where are the performance bottlenecks?"
# "How do I add a new feature?"
```

### Quick Code Question

```bash
gemini chat --context ./src/utils.ts --prompt "Is this function efficient?"
```

---

## Code Analysis

### Explain a Function

```bash
gemini code --explain ./src/algorithms/sort.ts
```

**Output:** Detailed explanation of what the code does

### Review Code Quality

```bash
gemini code --review ./src/components/Button.tsx
```

**Output:** Suggestions for improvements, best practices, etc.

### Find Bugs

```bash
gemini code --fix ./src/handlers/payment.js
```

**Output:** Potential bugs and fixes

### Generate Tests

```bash
gemini code --test ./src/utils/validators.ts
```

**Output:** Suggested test cases and test code

---

## Code Generation

### React Component from Design Image

```bash
# Take a screenshot of your Figma design
gemini create --from-image ./design.png --template react
```

**Output:** React component matching the design

### Multiple Components from Designs

```bash
for img in designs/*.png; do
  NAME=$(basename "$img" .png)
  gemini create --from-image "$img" \
    --template react \
    --output "src/components/${NAME}.tsx"
done
```

### TypeScript from API Spec PDF

```bash
gemini create --from-pdf ./api-spec.pdf \
  --template typescript \
  --output ./api/client.ts
```

**Output:** TypeScript client code matching the spec

### Database Schema from Requirements

```bash
gemini create --from-pdf ./requirements.pdf \
  --template schema \
  --lang sql \
  --output ./schema.sql
```

---

## Batch Operations

### Analyze Entire Codebase

```bash
# Using helper script
~/.openclaw/workspace/skills/gemini-cli/scripts/batch-analyze.sh explain ./src ./analysis

# Manual batch
gemini batch --input ./src --operation "explain" --output ./docs
```

**Output:** Analysis of all files in `./docs` directory

### Review All Component Files

```bash
gemini batch --input ./src/components \
  --operation "review" \
  --output ./component-reviews \
  --parallel 4  # Run 4 at a time
```

### Document Your Project

```bash
gemini code --explain ./src --format markdown > project-docs.md
```

---

## Debugging

### Debug Error Message

```bash
gemini debug --error "TypeError: Cannot read property 'map' of undefined" \
  --context ./src
```

**Output:** Analysis of the error and potential fixes

### Analyze Stack Trace

```bash
gemini debug ./error-stack.txt --context ./src
```

---

## Real-World Workflows

### Code Review Workflow

```bash
#!/bin/bash
# review-pr.sh - Review all changes in a PR

PR_FILE="$1"

echo "📋 Reviewing pull request..."

# Get changed files
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD)

for file in $CHANGED_FILES; do
  echo "Reviewing: $file"
  gemini code --review "$file" --format markdown >> pr-review.md
done

echo "✅ Review complete: pr-review.md"
```

Usage:
```bash
./review-pr.sh
cat pr-review.md
```

### Migrate Codebase to New Framework

```bash
#!/bin/bash
# migrate-to-react.sh - Convert vanilla JS to React

OLD_DIR="./src/old-vanilla"
NEW_DIR="./src/react-version"

mkdir -p "$NEW_DIR"

for file in "$OLD_DIR"/*.js; do
  NAME=$(basename "$file")
  echo "Converting: $NAME"
  
  gemini code --explain "$file" \
    --prompt "Convert this to React component" \
    --save "$NEW_DIR/${NAME%.js}.tsx"
done
```

### Generate API Documentation

```bash
#!/bin/bash
# generate-api-docs.sh

SRC_DIR="./src/api"
DOC_DIR="./docs/api"

mkdir -p "$DOC_DIR"

for file in "$SRC_DIR"/*.ts; do
  NAME=$(basename "$file" .ts)
  echo "Documenting: $NAME"
  
  gemini code --explain "$file" \
    --format markdown \
    --prompt "Generate API documentation for this endpoint" \
    --save "$DOC_DIR/${NAME}.md"
done
```

---

## Tips & Tricks

### Pipe Between Commands

```bash
# Get explanation and save
gemini code --explain ./complex-file.ts | tee explanation.txt

# Review and count issues
gemini code --review ./src | grep -i "issue\|warning" | wc -l
```

### Use Gemini as Git Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Auto-review before commit
CHANGED=$(git diff --cached --name-only --diff-filter=ACM)

for file in $CHANGED; do
  gemini code --review "$file" > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "⚠️  Review failed for $file"
    # Optionally fail commit
    # exit 1
  fi
done
```

### Create Reusable Prompts

```bash
# Create ./prompts/api-review.txt
cat << 'EOF' > prompts/api-review.txt
Review this API implementation for:
1. Security (authorization, input validation)
2. Performance (N+1 queries, unnecessary calculations)
3. Error handling (proper status codes, error messages)
4. Documentation (clear endpoint descriptions)
EOF

# Use it
gemini code --review ./src/api/users.ts < prompts/api-review.txt
```

### Batch Process with Progress

```bash
FILES=$(find ./src -name "*.ts" | head -20)
TOTAL=$(echo "$FILES" | wc -l)
COUNT=0

for file in $FILES; do
  COUNT=$((COUNT+1))
  echo "[$COUNT/$TOTAL] Analyzing $file..."
  gemini code --explain "$file" --save "./docs/${file}.md"
done
```

---

## Common Patterns

### Explain → Review → Fix Flow

```bash
FILE="./src/utils.ts"

echo "1️⃣  Explaining..."
gemini code --explain "$FILE"

echo "2️⃣  Reviewing..."
gemini code --review "$FILE"

echo "3️⃣  Getting fixes..."
gemini code --fix "$FILE"
```

### Design → Code → Tests → Docs

```bash
DESIGN="./design.png"
OUTPUT="./src/components/NewComponent"

echo "1️⃣  Generating from design..."
gemini create --from-image "$DESIGN" --template react --save "${OUTPUT}.tsx"

echo "2️⃣  Generating tests..."
gemini code --test "${OUTPUT}.tsx" --save "${OUTPUT}.test.tsx"

echo "3️⃣  Generating docs..."
gemini code --explain "${OUTPUT}.tsx" --format markdown --save "${OUTPUT}.md"
```

### Full Project Analysis

```bash
PROJECT="./my-app"

echo "📊 Full project analysis..."

mkdir -p project-analysis

# Architecture
gemini chat --context "$PROJECT" --prompt "Describe the architecture" > project-analysis/architecture.md

# Security review
gemini code --review "$PROJECT" --format markdown > project-analysis/security.md

# Documentation
find "$PROJECT" -name "*.ts" -type f | head -10 | while read file; do
  gemini code --explain "$file" --format markdown >> project-analysis/code-docs.md
done

echo "✅ Analysis saved to project-analysis/"
```

---

## Troubleshooting Examples

### "API key not found"

```bash
# Fix:
export GEMINI_API_KEY="your-key-from-aistudio-google-com"

# Verify:
gemini chat --prompt "Hello"
```

### "Context path invalid"

```bash
# Wrong:
gemini chat --context ./nonexistent

# Right:
gemini chat --context ./src/  # Must exist
```

### "File too large"

```bash
# Instead of whole directory:
gemini code --explain ./src/large-file.ts

# Or break it up:
split -l 100 large-file.ts part_
for part in part_*; do
  gemini code --explain "$part"
done
```

---

**More examples:** Check out https://geminicli.com/docs/examples
