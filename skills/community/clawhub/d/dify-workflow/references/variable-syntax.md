# Dify Variable Syntax Complete Guide

## Core Syntax

### Standard Variable Reference

```
{{#NODE_ID.VARIABLE_NAME#}}
```

- **Double curly braces** `{{ }}` - Marks dynamic content
- **Hash symbols** `#` - Required delimiters around the reference
- **NODE_ID** - Timestamp-based node identifier (e.g., `1718352852007`)
- **VARIABLE_NAME** - Output variable from that node

### Examples

```yaml
# Reference start node input
{{#1718352852007.input_text#}}

# Reference LLM output
{{#1718355814693.text#}}

# Reference Code node output
{{#1719357159255.success#}}

# Reference HTTP response body
{{#1719356422842.body#}}
```

---

## Common Mistakes

### Mistake 1: Missing Hash Symbols

```yaml
# ❌ WRONG - No hash symbols
prompt: "Analyze: {{1718352852007.input_text}}"

# ❌ WRONG - Only opening hash
prompt: "Analyze: {{#1718352852007.input_text}}"

# ✅ CORRECT
prompt: "Analyze: {{#1718352852007.input_text#}}"
```

### Mistake 2: Triple Braces

```yaml
# ❌ WRONG - Triple braces
prompt: "{{{#1718352852007.text#}}}"

# ✅ CORRECT - Double braces only
prompt: "{{#1718352852007.text#}}"
```

### Mistake 3: Node ID as String Name

```yaml
# ❌ WRONG - Using descriptive names
{{#start_node.input#}}
{{#llm_analyzer.text#}}

# ✅ CORRECT - Using actual node IDs
{{#1718352852007.input_text#}}
{{#1718355814693.text#}}
```

### Mistake 4: Wrong Variable Name

```yaml
# ❌ WRONG - Variable doesn't exist on LLM node
{{#1718355814693.result#}}

# ✅ CORRECT - LLM nodes output 'text'
{{#1718355814693.text#}}
```

---

## Node Output Variables

### Start Node

| Variable | Type | Description |
|----------|------|-------------|
| `{variable_name}` | Defined in config | User-defined input variables |

```yaml
# If start node has: variable: input_article_id
{{#1718352852007.input_article_id#}}
```

### LLM Node

| Variable | Type | Description |
|----------|------|-------------|
| `text` | string | Generated text output |

```yaml
{{#1718355814693.text#}}
```

### Code Node

| Variable | Type | Description |
|----------|------|-------------|
| `{output_name}` | Defined in outputs | Variables defined in outputs schema |

```yaml
# If code node outputs: success, content, title
{{#1719357159255.success#}}
{{#1719357159255.content#}}
{{#1719357159255.title#}}
```

### HTTP Request Node

| Variable | Type | Description |
|----------|------|-------------|
| `body` | string | Response body content |
| `status_code` | number | HTTP status code |
| `headers` | object | Response headers |
| `files` | array | Downloaded files (if any) |

```yaml
{{#1719356422842.body#}}
{{#1719356422842.status_code#}}
```

### IF/ELSE Node

The IF/ELSE node doesn't produce output variables. It routes flow based on conditions.

### Knowledge Retrieval Node

| Variable | Type | Description |
|----------|------|-------------|
| `result` | array[object] | Retrieved document chunks |

```yaml
{{#1720000000000.result#}}
```

### Iteration Node

| Variable | Type | Description |
|----------|------|-------------|
| `output` | array | Collected results from all iterations |

Built-in iteration variables (inside iteration only):
- `items` - Current item being processed
- `index` - Current iteration index (0-based)

---

## System Variables

System variables use the `sys.` prefix:

```yaml
# User ID
{{#sys.user_id#}}

# Conversation ID (Chatflow only)
{{#sys.conversation_id#}}

# Dialogue count (Chatflow only)
{{#sys.dialogue_count#}}

# Current files
{{#sys.files#}}

# Current query (Chatflow only)
{{#sys.query#}}
```

---

## Environment Variables

Reference environment variables configured in Dify:

```yaml
# Access environment variable
{{#env.API_KEY#}}
{{#env.BASE_URL#}}
```

**Security Note**: Use environment variables for sensitive data like API keys.

---

## Variable in Different Contexts

### In Prompt Templates

```yaml
prompt_template:
  - role: user
    text: |
      Title: {{#1719357159255.title#}}
      Content: {{#1719357159255.content#}}

      Please analyze this article.
```

### In HTTP Request Params

```yaml
params: "id:{{#1718352852007.input_article_id#}}&format:json"
```

### In HTTP Request Headers

```yaml
headers: "Authorization:Bearer {{#env.API_KEY#}}"
```

### In HTTP Request Body (JSON)

```yaml
body:
  type: json
  data:
    - key: content
      type: text
      value: "{{#1719357159255.content#}}"
```

### In Code Node Variables Binding

```yaml
variables:
  - variable: json_body          # Parameter name in main()
    value_selector:
      - '1719356422842'          # Source node ID
      - body                     # Source variable name
```

---

## Jinja2 Template Syntax

LLM nodes support Jinja2 for advanced templating:

### Loops

```jinja2
{% for item in items %}
- {{ item.title }}: {{ item.content }}
{% endfor %}
```

### Conditionals

```jinja2
{% if score > 80 %}
High quality content
{% else %}
Needs improvement
{% endif %}
```

### Filters

```jinja2
{{ content | truncate(100) }}
{{ text | replace('\n', ' ') }}
{{ data | default('N/A') }}
```

---

## Value Selector Format

In DSL YAML, variables are referenced using `value_selector` arrays:

```yaml
value_selector:
  - '1719357159255'    # Node ID (as string)
  - content            # Variable name

# This is equivalent to: {{#1719357159255.content#}}
```

### In End Node Outputs

```yaml
outputs:
  - variable: result
    value_selector:
      - '1719444170368'
      - text
```

### In Code Node Variables

```yaml
variables:
  - variable: input_data
    value_selector:
      - '1718352852007'
      - input_text
```

---

## Quick Reference Table

| Context | Syntax | Example |
|---------|--------|---------|
| Prompt text | `{{#ID.var#}}` | `{{#1718352852007.input#}}` |
| HTTP params | `{{#ID.var#}}` | `id:{{#1718352852007.id#}}` |
| HTTP headers | `{{#ID.var#}}` | `Bearer {{#env.API_KEY#}}` |
| System var | `{{#sys.name#}}` | `{{#sys.user_id#}}` |
| Env var | `{{#env.name#}}` | `{{#env.BASE_URL#}}` |
| DSL value_selector | Array format | `['1718352852007', 'input']` |

---

## Debugging Tips

1. **Check node IDs** - Use Dify UI to find correct node IDs
2. **Verify variable names** - Each node type has specific outputs
3. **Test incrementally** - Add one variable reference at a time
4. **Use Dify 1.5.0+** - "Last Run" feature shows actual values
