# Dify Workflow Common Gotchas

A comprehensive troubleshooting guide for Dify workflow DSL issues.

---

## Variable Reference Issues

### Gotcha 1: Missing Hash Symbols

**Symptom**: Variable not replaced, shows literal text

```yaml
# ❌ WRONG
text: "Input: {{1718352852007.input_text}}"
# Result: "Input: {{1718352852007.input_text}}"

# ✅ CORRECT
text: "Input: {{#1718352852007.input_text#}}"
# Result: "Input: Hello World"
```

**Solution**: Always use `{{#NODE_ID.VARIABLE#}}` with both `#` symbols.

---

### Gotcha 2: Wrong Node ID

**Symptom**: Variable is empty or workflow fails

```yaml
# ❌ WRONG - Using made-up ID
{{#start.input#}}
{{#llm_node.text#}}

# ✅ CORRECT - Using actual timestamp ID
{{#1718352852007.input_text#}}
{{#1718355814693.text#}}
```

**Solution**: Copy exact node ID from Dify UI or existing DSL.

---

### Gotcha 3: Non-existent Variable Name

**Symptom**: Empty value returned

```yaml
# ❌ WRONG - LLM nodes don't have 'result' output
{{#1718355814693.result#}}

# ✅ CORRECT - LLM nodes output 'text'
{{#1718355814693.text#}}
```

**Solution**: Check node type's available outputs:
- LLM: `text`
- HTTP: `body`, `status_code`, `headers`, `files`
- Code: Custom defined in `outputs`

---

## Code Node Issues

### Gotcha 4: Missing Outputs Schema

**Symptom**: "Failed to parse result" error

```yaml
# ❌ WRONG - No outputs defined
- data:
    type: code
    code: |
      def main(x):
        return {"result": x * 2}

# ✅ CORRECT - Outputs schema defined
- data:
    type: code
    code: |
      def main(x):
        return {"result": x * 2}
    outputs:
      result:
        type: number
        children: null
```

**Solution**: Define every returned key in `outputs` with correct type.

---

### Gotcha 5: Reserved Variable Name "error"

**Symptom**: JavaScript execution error

```python
# ❌ WRONG - "error" is reserved
def main(data):
    if not data:
        return {"error": "No data provided"}
    return {"error": None, "result": data}

# ✅ CORRECT - Use different name
def main(data):
    if not data:
        return {"error_message": "No data provided", "success": False}
    return {"error_message": None, "success": True, "result": data}
```

**Solution**: Never use `error` as output variable name. Use `error_message`, `error_text`, or `has_error` instead.

**Reference**: [GitHub Issue #22389](https://github.com/langgenius/dify/issues/22389)

---

### Gotcha 6: Function Signature Mismatch

**Symptom**: Code node fails with parameter errors

```yaml
# ❌ WRONG - Parameter name doesn't match
variables:
  - variable: input_data
    value_selector: ['1718352852007', 'input']
code: |
  def main(data):  # Expected 'input_data', got 'data'
    return {"result": data}

# ✅ CORRECT - Names match
variables:
  - variable: input_data
    value_selector: ['1718352852007', 'input']
code: |
  def main(input_data):  # Matches variable name
    return {"result": input_data}
```

**Solution**: Ensure `main()` parameter names match `variables[].variable` names.

---

### Gotcha 7: Wrong Output Type

**Symptom**: Type mismatch errors

```yaml
# ❌ WRONG - Returning string, declared as number
outputs:
  count:
    type: number
code: |
  def main(items):
    return {"count": str(len(items))}  # Returns "5" not 5

# ✅ CORRECT - Return matching type
outputs:
  count:
    type: number
code: |
  def main(items):
    return {"count": len(items)}  # Returns 5
```

**Solution**: Match return types to declared output types:
- `string` → `str`
- `number` → `int` or `float`
- `boolean` → `bool` (lowercase in Python: `True`/`False`)

---

## DSL Import/Export Issues

### Gotcha 8: Version Incompatibility

**Symptom**: Import fails or workflow shows loading indefinitely

```yaml
# Check DSL version
version: 0.6.0  # Replace with exported version from your instance

# Minimum versions for features:
# 0.10.0+ - Basic DSL import
# 0.13.0+ - Parallel tasks, session variables
# 1.5.0+  - Real-time debugging
```

**Solution**: Upgrade Dify to match DSL version or re-export from matching version.

**Reference**: [GitHub Issue #3643](https://github.com/langgenius/dify/issues/3643)

---

### Gotcha 9: Missing Plugin Dependencies

**Symptom**: Import succeeds but nodes show errors

```yaml
# ❌ WRONG - Missing dependency declaration
app:
  name: My Workflow

# ✅ CORRECT - Dependencies declared
dependencies:
  - current_identifier: null
    type: marketplace
    value:
      marketplace_plugin_unique_identifier: langgenius/gemini:0.1.5@012c9e0...
```

**Solution**: Ensure all model providers are listed in `dependencies`.

---

### Gotcha 10: Secrets Lost on Export

**Symptom**: API keys and credentials missing after import

```yaml
# HTTP node with API key - NOT exported by default
authorization:
  type: api-key
  config:
    api_key: "sk-xxx..."  # Will be empty after import
```

**Solution**:
1. Use environment variables instead: `{{#env.API_KEY#}}`
2. Or manually re-enter credentials after import
3. Or choose to include secrets during export (security risk)

**Reference**: [GitHub Issue #7598](https://github.com/langgenius/dify/issues/7598)

---

### Gotcha 11: Export Not Matching Draft

**Symptom**: Exported DSL differs from what you see in editor

**Solution**: Always save workflow before exporting. Export uses last auto-saved version.

**Reference**: [GitHub Issue #24884](https://github.com/langgenius/dify/issues/24884)

---

## LLM Node Issues

### Gotcha 12: Invalid Context Structure

**Symptom**: "Invalid Context Structure Error"

```yaml
# ❌ WRONG - Context can't be array[object]
context:
  enabled: true
  variable_selector:
    - '1720000000000'
    - result  # If this is array[object], it fails

---

## Current Node Pattern Gotchas

### Gotcha 13: Answer ist kein Workflow-Ende

**Symptom**: Nutzer will in einem Single-run Workflow Zwischenantworten ueber `Answer` liefern

**Reality**:

- `Answer` ist laut aktueller Doku nur fuer Chatflow verfuegbar.
- Workflow benutzt stattdessen `End`.

**Praktische Folge**: Wenn das Ziel mehrfaches Antworten waehrend einer Konversation ist, zuerst Chatflow statt Workflow pruefen.

**Reference**: `https://docs.dify.ai/en/use-dify/nodes/answer`

### Gotcha 14: Trigger nicht fuer Chatflow zusagen

**Symptom**: User will Trigger in einem Chatflow

**Reality**:

- Trigger sind fuer Workflow verfuegbar.
- Chatflow kann laut aktueller Doku nicht per Trigger starten.

**Praktische Folge**: Bei Trigger-Anforderungen zuerst Workflow-Denke aktivieren und self-hosted Trigger-/OAuth-Kontext prüfen.

**Reference**:

- `https://docs.dify.ai/en/use-dify/getting-started/key-concepts#workflow`
- `https://docs.dify.ai/en/use-dify/nodes/trigger/plugin-trigger`

### Gotcha 15: Gemischte Datei-Arrays nicht blind in einen Node kippen

**Symptom**: Images, PDFs und andere Dateien laufen in denselben Folge-Node und machen den Flow unklar oder fehleranfällig

**Reality**:

- Der `List Operator` ist fuer genau diese Trennung dokumentiert.
- Bilder und Dokumente sollten oft in getrennte Pfade.

**Praktische Folge**: Vor Vision-LLM oder Document-Extractor lieber zuerst nach Dateityp splitten.

**Reference**: `https://docs.dify.ai/en/use-dify/nodes/list-operator`

### Gotcha 16: Parameter Extractor ohne Statuspfad

**Symptom**: Extraktion liefert unvollstaendige Daten, aber der Flow faehrt blind weiter

**Reality**:

- `Parameter Extractor` liefert eingebaute Statusvariablen `__is_success` und `__reason`.

**Praktische Folge**: Bei produktionsnahen Flows einen Fehler- oder Retry-Pfad mit diesen Statusvariablen mitdenken.

**Reference**: `https://docs.dify.ai/en/use-dify/nodes/parameter-extractor`

# ✅ CORRECT - Convert to string first
# Use a Template node to convert array to string before LLM
```

**Solution**: Context only accepts `String` type. Use Template node to convert arrays.

---

### Gotcha 13: Knowledge Retrieval Output Format

**Symptom**: LLM receives malformed context from knowledge base

```yaml
# Knowledge retrieval outputs array of objects
# Must convert before using in LLM context

# Use Template node with Jinja2:
template: |
  {% for item in result %}
  Document {{ loop.index }}:
  {{ item.content }}
  ---
  {% endfor %}
```

**Solution**: Add Template node between Knowledge Retrieval and LLM nodes.

---

## Iteration Node Issues

### Gotcha 14: Input Not Array

**Symptom**: Iteration node fails to start

```yaml
# ❌ WRONG - String input
input_variable_selector:
  - '1718355814693'
  - text  # This is a string

# ✅ CORRECT - Array input
# Use Code node to convert string to array first:
code: |
  def main(text):
    return {"items": text.split('\n')}
```

**Solution**: Ensure input is `Array` type. Use Code node to convert if needed.

---

### Gotcha 15: Direct Answer Inside Iteration

**Symptom**: Workflow crashes or behaves unexpectedly

```yaml
# ❌ WRONG - These nodes can't be inside iteration
iteration:
  nodes:
    - type: answer        # Not allowed
    - type: variable-assigner  # Not allowed
    - type: tool          # Not allowed
```

**Solution**: Keep Answer, Variable Assigner, and Tool nodes outside iteration.

---

### Gotcha 16: Iteration Output Format

**Symptom**: Cannot use iteration output directly

```yaml
# Iteration outputs array, not string
# Must convert for most downstream uses

# Use Template node after iteration:
template: |
  {% for item in output %}
  {{ item.text }}
  {% endfor %}
```

**Solution**: Use Template node to convert array output to string.

---

## HTTP Request Issues

### Gotcha 17: Request Method Reset

**Symptom**: POST becomes GET after saving

**Workaround**: This is a known bug. Try:
1. Re-save the workflow
2. Check if body and auth are preserved
3. Report if persists

**Reference**: [GitHub Issue #4168](https://github.com/langgenius/dify/issues/4168)

---

### Gotcha 18: Params Format

**Symptom**: Parameters not sent correctly

```yaml
# ❌ WRONG - JSON format
params: {"id": "{{#1718352852007.id#}}"}

# ✅ CORRECT - Key:value format
params: "id:{{#1718352852007.id#}}"

# Multiple params
params: "id:{{#1718352852007.id#}}&format:json"
```

**Solution**: Use `key:value` format separated by `&`, not JSON.

---

## Edge Connection Issues

### Gotcha 19: Missing Edges

**Symptom**: Nodes not executing in sequence

```yaml
# Every connection needs an edge
edges:
  - source: '1718352852007'      # Start
    target: '1719356422842'      # HTTP Request
  - source: '1719356422842'      # HTTP Request
    target: '1719357159255'      # Code (MUST HAVE THIS)
```

**Solution**: Verify every node-to-node connection has corresponding edge.

---

### Gotcha 20: IF/ELSE Branch Handles

**Symptom**: Wrong branch executes

```yaml
# IF/ELSE uses special sourceHandle values
edges:
  - source: '1720855943817'
    sourceHandle: 'true'         # IF condition met
    target: '1718355814693'      # → LLM node

  - source: '1720855943817'
    sourceHandle: 'false'        # ELSE branch
    target: '1747277797191'      # → End node
```

**Solution**: Use `sourceHandle: 'true'` or `sourceHandle: 'false'` for IF/ELSE.

---

## Quick Diagnostic Checklist

When workflow fails, check in order:

1. [ ] Variable syntax: All `{{#NODE_ID.VAR#}}` have both `#`
2. [ ] Node IDs exist: Referenced IDs match actual nodes
3. [ ] Variable names: Using correct output names for node type
4. [ ] Code outputs: All returned keys defined in schema
5. [ ] No `error` variable: Using alternative names
6. [ ] Edges complete: All connections have edges
7. [ ] Type compatibility: Input types match expected types
8. [ ] Version compatible: Dify version supports DSL features
9. [ ] Dependencies: All plugins listed in dependencies
