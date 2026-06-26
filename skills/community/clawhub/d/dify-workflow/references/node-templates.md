# Dify Node Templates Reference

Complete YAML templates for all Dify workflow node types.

---

## Start Node

The entry point of every workflow. Defines input parameters.

```yaml
- data:
    type: start
    title: Start
    desc: "Input parameters description"
    variables:
      # Text Input
      - variable: text_input
        label: "Text Input"
        type: text-input
        required: true
        max_length: 1000
        options: []

      # Paragraph (Multi-line text)
      - variable: long_text
        label: "Long Text"
        type: paragraph
        required: true
        max_length: 50000
        options: []

      # Number
      - variable: count
        label: "Count"
        type: number
        required: false
        options: []

      # Select (Dropdown)
      - variable: language
        label: "Language"
        type: select
        required: true
        options:
          - Chinese
          - English
          - Japanese

  id: '1700000000001'
  type: custom
  position:
    x: 30
    y: 275
  width: 244
  height: 150
```

### Variable Types

| Type | Description | Options |
|------|-------------|---------|
| `text-input` | Single line text | `max_length` |
| `paragraph` | Multi-line text | `max_length` |
| `number` | Numeric input | - |
| `select` | Dropdown menu | `options: []` |

---

## End Node

Terminates workflow and defines outputs.

```yaml
- data:
    type: end
    title: End
    desc: "Output results"
    outputs:
      # Single output
      - variable: result
        value_selector:
          - '1700000000002'  # Source node ID
          - text              # Source variable name

      # Multiple outputs
      - variable: summary
        value_selector:
          - '1700000000002'
          - text
      - variable: score
        value_selector:
          - '1700000000003'
          - score

  id: '1700000000099'
  type: custom
  position:
    x: 1550
    y: 275
  width: 244
  height: 118
```

---

## LLM Node

Invokes large language model for text generation.

```yaml
- data:
    type: llm
    title: "LLM Process"
    desc: "Process with language model"

    # Model Configuration
    model:
      provider: langgenius/openai/openai     # Provider path
      name: gpt-4o                           # Model name
      mode: chat                             # chat | completion
      completion_params:
        temperature: 0.7
        max_tokens: 4096
        top_p: 1

    # Prompt Template
    prompt_template:
      - id: system-prompt-uuid
        role: system
        text: |
          You are a helpful assistant.
          Follow these guidelines:
          1. Be concise
          2. Be accurate

      - id: user-prompt-uuid
        role: user
        text: |
          User request: {{#1700000000001.user_input#}}

          Please process this request.

    # Context (for RAG)
    context:
      enabled: false
      variable_selector: []

    # Vision (for image input)
    vision:
      enabled: false
      configs:
        detail: high
        variable_selector: []

  id: '1700000000002'
  type: custom
  position:
    x: 334
    y: 275
  width: 244
  height: 118
```

### Common Model Providers

| Provider | Path | Models |
|----------|------|--------|
| OpenAI | `langgenius/openai/openai` | gpt-4o, gpt-4o-mini, gpt-4-turbo |
| Anthropic | `langgenius/anthropic/anthropic` | claude-3-5-sonnet, claude-3-opus |
| Google | `langgenius/gemini/google` | gemini-2.0-flash, gemini-1.5-pro |

---

## Code Node

Executes Python or JavaScript code.

### Python Code Node

```yaml
- data:
    type: code
    title: "Process Data"
    desc: "Custom data processing"
    code_language: python3
    code: |
      import json

      def main(input_text, options):
          """
          Process input and return structured output.

          Args:
              input_text: String input from previous node
              options: Additional options dict

          Returns:
              dict with defined output keys
          """
          result = {
              "success": True,
              "processed_text": input_text.upper(),
              "word_count": len(input_text.split()),
              "error_message": ""  # Note: Don't use 'error' as key name
          }

          try:
              # Processing logic
              if not input_text:
                  result["success"] = False
                  result["error_message"] = "Empty input"
          except Exception as e:
              result["success"] = False
              result["error_message"] = str(e)

          return result

    # Input Variables Binding
    variables:
      - variable: input_text         # Parameter name in main()
        value_selector:
          - '1700000000001'          # Source node ID
          - user_input               # Source variable
      - variable: options
        value_selector:
          - '1700000000001'
          - config

    # Output Schema (REQUIRED!)
    outputs:
      success:
        type: boolean
        children: null
      processed_text:
        type: string
        children: null
      word_count:
        type: number
        children: null
      error_message:
        type: string
        children: null

  id: '1700000000003'
  type: custom
  position:
    x: 638
    y: 275
  width: 244
  height: 82
```

### JavaScript Code Node

```yaml
- data:
    type: code
    title: "JS Process"
    code_language: javascript
    code: |
      function main(inputText) {
        return {
          result: inputText.toUpperCase(),
          length: inputText.length
        };
      }
    variables:
      - variable: inputText
        value_selector:
          - '1700000000001'
          - text
    outputs:
      result:
        type: string
        children: null
      length:
        type: number
        children: null
  id: '1700000000003'
  type: custom
```

### Output Types

| Type | Python Type | JavaScript Type |
|------|-------------|-----------------|
| `string` | `str` | `string` |
| `number` | `int`, `float` | `number` |
| `boolean` | `bool` | `boolean` |
| `object` | `dict` | `object` |
| `array[string]` | `list[str]` | `string[]` |
| `array[number]` | `list[int]` | `number[]` |
| `array[object]` | `list[dict]` | `object[]` |

---

## HTTP Request Node

Makes HTTP requests to external APIs.

```yaml
- data:
    type: http-request
    title: "API Call"
    desc: "Call external API"

    # Request Configuration
    method: post                             # get | post | put | delete | patch
    url: https://api.example.com/endpoint

    # Query Parameters (key:value format)
    params: "id:{{#1700000000001.resource_id#}}&format:json"

    # Headers
    headers: |
      Content-Type:application/json
      Authorization:Bearer {{#env.API_KEY#}}
      X-Custom-Header:value

    # Request Body
    body:
      type: json                             # none | json | form-data | raw
      data:
        - key: content
          type: text
          value: "{{#1700000000002.text#}}"
        - key: metadata
          type: text
          value: '{"source": "dify"}'

    # Or form-data
    # body:
    #   type: form-data
    #   data:
    #     - key: file
    #       type: file
    #       value: "{{#1700000000001.uploaded_file#}}"

    # Authentication
    authorization:
      type: no-auth                          # no-auth | api-key | bearer
      config: null

    # Timeouts (milliseconds)
    timeout:
      max_connect_timeout: 30000
      max_read_timeout: 60000
      max_write_timeout: 30000

    # Retry Configuration
    retry_config:
      retry_enabled: true
      max_retries: 3
      retry_interval: 1000

    # SSL Verification
    ssl_verify: true

  id: '1700000000004'
  type: custom
  position:
    x: 334
    y: 275
  width: 244
  height: 139
```

### HTTP Node Outputs

| Variable | Type | Description |
|----------|------|-------------|
| `body` | string | Response body |
| `status_code` | number | HTTP status code |
| `headers` | object | Response headers |
| `files` | array | Downloaded files |

---

## IF/ELSE Node

Conditional branching based on variable values.

```yaml
- data:
    type: if-else
    title: "Check Condition"
    desc: "Branch based on condition"

    # Condition Cases
    cases:
      # IF branch
      - id: 'true'
        case_id: 'true'
        logical_operator: and              # and | or
        conditions:
          # Condition 1
          - id: condition-1
            variable_selector:
              - '1700000000003'
              - success
            comparison_operator: is        # See operators below
            value: 'true'
            varType: boolean

          # Condition 2 (AND with above)
          - id: condition-2
            variable_selector:
              - '1700000000003'
              - score
            comparison_operator: gte
            value: '80'
            varType: number

  id: '1700000000005'
  type: custom
  position:
    x: 942
    y: 275
  width: 244
  height: 126
```

### Comparison Operators

| Operator | Description | Types |
|----------|-------------|-------|
| `is` | Equals | string, number, boolean |
| `is-not` | Not equals | string, number, boolean |
| `contains` | Contains substring | string |
| `not-contains` | Doesn't contain | string |
| `starts-with` | Starts with | string |
| `ends-with` | Ends with | string |
| `is-empty` | Is empty/null | string |
| `is-not-empty` | Is not empty | string |
| `gt` | Greater than | number |
| `gte` | Greater or equal | number |
| `lt` | Less than | number |
| `lte` | Less or equal | number |

### Edge Connections for IF/ELSE

```yaml
# TRUE branch
- source: '1700000000005'
  sourceHandle: 'true'        # Important!
  target: '1700000000006'

# FALSE branch
- source: '1700000000005'
  sourceHandle: 'false'       # Important!
  target: '1700000000007'
```

---

## Iteration Node

Loops over array elements.

```yaml
- data:
    type: iteration
    title: "Process Items"
    desc: "Iterate over array"

    # Input array
    input_variable_selector:
      - '1700000000002'
      - items                   # Must be array type

    # Output variable name
    output_variable: processed_items

    # Parallel processing
    is_parallel: true
    parallel_nums: 5            # Max concurrent (1-10)

    # Error handling
    error_handle_mode: terminated  # terminated | remove_abnormal

  id: '1700000000006'
  type: custom
  position:
    x: 942
    y: 275
  width: 500
  height: 300
```

### Built-in Iteration Variables

Inside iteration, access:
- `items` - Current item being processed
- `index` - Current index (0-based)

```yaml
# Inside iteration LLM node
text: |
  Processing item {{#iteration.index#}}:
  {{#iteration.items#}}
```

---

## Template Node (Jinja2)

Transform data using Jinja2 templates.

```yaml
- data:
    type: template
    title: "Format Output"
    desc: "Transform data with Jinja2"

    template: |
      # Analysis Report

      ## Summary
      {{ summary }}

      ## Key Points
      {% for point in points %}
      - {{ point.title }}: {{ point.description }}
      {% endfor %}

      ## Score
      {{ score | default('N/A') }}

    # Input Variables
    variables:
      - variable: summary
        value_selector:
          - '1700000000002'
          - summary
      - variable: points
        value_selector:
          - '1700000000002'
          - key_points
      - variable: score
        value_selector:
          - '1700000000002'
          - score

  id: '1700000000007'
  type: custom
  position:
    x: 1246
    y: 275
  width: 244
  height: 82
```

---

## Knowledge Retrieval Node

Query knowledge base for RAG.

```yaml
- data:
    type: knowledge-retrieval
    title: "Search Knowledge"
    desc: "Retrieve from knowledge base"

    # Query
    query_variable_selector:
      - '1700000000001'
      - user_query

    # Knowledge Base IDs
    dataset_ids:
      - dataset-uuid-1
      - dataset-uuid-2

    # Retrieval Settings
    retrieval_mode: multiple         # single | multiple
    top_k: 5
    score_threshold: 0.5
    reranking_enable: true

  id: '1700000000008'
  type: custom
  position:
    x: 334
    y: 275
  width: 244
  height: 118
```

### Knowledge Retrieval Output

Output is `result` containing array of retrieved chunks:
```json
[
  {
    "content": "Retrieved text content...",
    "metadata": {
      "score": 0.85,
      "source": "document.pdf"
    }
  }
]
```

---

## Variable Assigner Node

Assign values to workflow variables.

```yaml
- data:
    type: variable-assigner
    title: "Set Variable"
    desc: "Assign value to variable"

    # Target variable
    output_type: string
    write_to_variable_selector:
      - conversation_variables
      - accumulated_text

    # Value to assign
    input_variable_selector:
      - '1700000000002'
      - text

  id: '1700000000009'
  type: custom
  position:
    x: 638
    y: 275
  width: 244
  height: 82
```

---

## Answer Node (Chatflow Only)

Outputs response in chatflow applications.

```yaml
- data:
    type: answer
    title: "Response"
    desc: "Output to user"

    answer: |
      {{#1700000000002.text#}}

  id: '1700000000010'
  type: custom
  position:
    x: 942
    y: 275
  width: 244
  height: 82
```

---

## Edge Template

Connect nodes together.

```yaml
edges:
  # Standard connection
  - data:
      sourceType: start
      targetType: llm
      isInIteration: false
    id: unique-edge-id
    source: '1700000000001'
    sourceHandle: source
    target: '1700000000002'
    targetHandle: target
    type: custom
    zIndex: 0

  # IF/ELSE true branch
  - data:
      sourceType: if-else
      targetType: llm
    id: ifelse-true-edge
    source: '1700000000005'
    sourceHandle: 'true'          # 'true' for IF branch
    target: '1700000000006'
    targetHandle: target
    type: custom
    zIndex: 0

  # IF/ELSE false branch
  - data:
      sourceType: if-else
      targetType: end
    id: ifelse-false-edge
    source: '1700000000005'
    sourceHandle: 'false'         # 'false' for ELSE branch
    target: '1700000000007'
    targetHandle: target
    type: custom
    zIndex: 0
```
