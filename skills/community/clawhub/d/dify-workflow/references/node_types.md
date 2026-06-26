# Dify Workflow Node Types Reference

This document describes all available node types in Dify workflow DSL based on the actual Dify codebase implementation.

## Node Type Classification

Nodes are classified by execution type:
- **EXECUTABLE**: Standard logic nodes (llm, code, http-request, etc.)
- **BRANCH**: Conditional routing nodes (if-else, question-classifier)
- **CONTAINER**: Sub-graph management (iteration, loop)
- **RESPONSE**: Output streaming (answer, end)
- **ROOT**: Entry points (start, datasource, trigger-webhook, trigger-schedule, trigger-plugin)

## Current Docs-Backed Node Highlights

Diese Punkte sind zusaetzlich durch aktuelle offizielle Dify-Doku abgedeckt und deshalb fuer neue self-hosted Aussagen besonders wertvoll.

### Answer

- nur fuer **Chatflow**
- liefert Antworten an den Nutzer
- kann Text, Bilder und Dateien streamen
- mehrere Answer-Nodes sind in einem Chatflow moeglich
- die Reihenfolge der Variablen im Answer beeinflusst das Streaming-Verhalten

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/answer`

### HTTP Request

- verbindet den Workflow mit externen APIs und Webservices
- deckt GET, HEAD, POST, PUT, PATCH und DELETE ab
- ist relevant fuer Datenabfrage, Webhooks, Uploads und Resource-Management

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/http-request`

### List Operator

- filtert, sortiert und selektiert Elemente aus Arrays
- besonders stark fuer gemischte Datei-Uploads
- kann Dateien nach Typ, MIME, Extension, Name, Groesse oder Transfer-Methode trennen
- typische Outputs sind `result`, `first_record`, `last_record`

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/list-operator`

### Parameter Extractor

- wandelt unstrukturierten Text in strukturierte Parameter um
- kann Parameter fuer nachgelagerte Tools und APIs vorbereiten
- unterstuetzt Function-/Tool-Call oder Prompt-basierten Modus
- liefert eingebaute Statusvariablen wie `__is_success` und `__reason`

Quelle:

- `https://docs.dify.ai/en/use-dify/nodes/parameter-extractor`

## Core Node Types

### 1. start
**Purpose**: Entry point of the workflow, defines input variables

**Required fields**:
- `type`: "start"
- `title`: Display name
- `variables`: Array of input variable definitions

**Variable fields**:
- `variable`: Variable name
- `label`: Display label
- `type`: Variable type (text, paragraph, number, select, etc.)
- `required`: Boolean
- `max_length`: Maximum length (for text types)
- `options`: Array of options (for select type)

**Example**:
```yaml
type: start
title: Start
variables:
  - label: User Input
    max_length: 10000
    required: true
    type: paragraph
    variable: user_input
```

### 2. end
**Purpose**: Terminal node that defines workflow outputs

**Required fields**:
- `type`: "end"
- `title`: Display name
- `outputs`: Array of output variable selectors

**Output fields**:
- `variable`: Output variable name
- `value_selector`: Array path to source value (e.g., ['node_id', 'field_name'])

**Example**:
```yaml
type: end
title: End
outputs:
  - variable: result
    value_selector:
      - '1733478262179'
      - text
  - variable: error_message
    value_selector:
      - '1733478343153'
      - error_message
```

### 3. llm
**Purpose**: Large Language Model inference node

**Required fields**:
- `type`: "llm"
- `title`: Display name
- `model`: Model configuration
- `prompt_template`: Array of message templates

**Model fields**:
- `provider`: Model provider (anthropic, openai, etc.)
- `name`: Model name (claude-3-5-sonnet-20241022, gpt-4, etc.)
- `mode`: chat or completion
- `completion_params`: Parameters like temperature

**Prompt template fields**:
- `id`: Unique identifier
- `role`: system, user, or assistant
- `text`: Template text with variable references {{#node_id.field#}}

**Context fields** (optional):
- `enabled`: Boolean
- `variable_selector`: Array of context variable paths

**Vision fields** (optional):
- `enabled`: Boolean

**Example**:
```yaml
type: llm
title: Generate Response
model:
  provider: anthropic
  name: claude-3-5-sonnet-20241022
  mode: chat
  completion_params:
    temperature: 0.7
prompt_template:
  - id: unique-id-1
    role: system
    text: You are a helpful assistant.
  - id: unique-id-2
    role: user
    text: "{{#1732007415808.user_input#}}"
context:
  enabled: false
  variable_selector: []
vision:
  enabled: false
```

### 4. code
**Purpose**: Execute Python or JavaScript code

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "code"
- `title`: Display name
- `code`: Code string
- `code_language`: "python3" or "javascript" (CodeLanguage enum)
- `variables`: Input variables array
- `outputs`: Output type definitions

**Variable fields**:
- Array of variable selectors: `[node_id, field_name]`

**Output fields**:
- `[output_name]`: Output variable name
  - `type`: Data type from SegmentType (string, number, object, boolean, array_string, array_number, array_object, array_boolean)
  - `children`: Nested structure for object types (recursive)

**Error handling fields** (optional):
- `error_strategy`: "fail-branch" or "default-value" (ErrorStrategy enum)
- `dependencies`: Optional array of package dependencies
  - `name`: Package name
  - `version`: Package version

**Source Handles**:
- Default: `"source"` (success path)
- With fail-branch: `"success-branch"` (success), `"fail-branch"` (error)

**Outputs**:
- Named outputs as defined in `outputs` config
- On fail-branch: `error_message`, `error_type`

**Example**:
```yaml
type: code
title: Process Data
code: |
  def main(input_text: str) -> dict:
      result = input_text.upper()
      return {'output': result}
code_language: python3
variables:
  - - '1733478262179'
    - text
outputs:
  output:
    type: string
    children: null
error_strategy: fail-branch
dependencies:
  - name: requests
    version: "2.31.0"
```

### 5. variable-aggregator
**Purpose**: Merge multiple conditional branch outputs into a single variable

**Required fields**:
- `type`: "variable-aggregator"
- `title`: Display name
- `variables`: Array of variable selector paths to aggregate
- `output_type`: Data type (string, number, object, array)

**Usage**: Required when downstream nodes need to reference values from multiple possible upstream branches (e.g., success/fail branches)

**Example**:
```yaml
type: variable-aggregator
title: Merge Results
output_type: object
variables:
  - - '1733478343153'
    - result
  - - '17334785192390'
    - result
```

### 6. if-else
**Purpose**: Conditional branching based on conditions

**Execution Type**: BRANCH

**Required fields**:
- `type`: "if-else"
- `title`: Display name
- `cases`: Array of Case objects (new format) OR `conditions` + `logical_operator` (legacy)

**Case structure** (recommended):
- `case_id`: Unique case identifier
- `logical_operator`: "and" or "or"
- `conditions`: Array of Condition objects

**Condition fields**:
- `variable_selector`: Array path to value `[node_id, field_name]`
- `comparison_operator`: SupportedComparisonOperator
  - String/Array: "contains", "not contains", "start with", "end with", "is", "is not", "empty", "not empty", "in", "not in", "all of"
  - Number: "=", "≠", ">", "<", "≥", "≤", "null", "not null"
  - File: "exists", "not exists"
- `value`: Comparison value (string, array of strings, or boolean)
- `sub_variable_condition`: Optional nested conditions for objects
  - `logical_operator`: "and" or "or"
  - `conditions`: Array of SubCondition objects

**Source Handles**:
- `"true"`: Condition(s) met
- `"false"`: Condition(s) not met

**Outputs**:
- `condition_result`: Boolean result

**Example**:
```yaml
type: if-else
title: Check Condition
cases:
  - case_id: case_1
    logical_operator: and
    conditions:
      - variable_selector:
          - '1733478262179'
          - text
        comparison_operator: contains
        value: "error"
      - variable_selector:
          - '1733478262179'
          - status
        comparison_operator: "="
        value: "failed"
```

### 7. iteration
**Purpose**: Loop over an array/list

**Required fields**:
- `type`: "iteration"
- `title`: Display name
- `input_selector`: Array path to iterable
- `output_selector`: Array path to aggregated output

**Example**:
```yaml
type: iteration
title: Process Items
input_selector:
  - '1733478262179'
  - items
```

### 8. knowledge-retrieval
**Purpose**: Retrieve information from knowledge base

**Required fields**:
- `type`: "knowledge-retrieval"
- `title`: Display name
- `dataset_ids`: Array of dataset IDs
- `query_variable_selector`: Array path to query text

**Example**:
```yaml
type: knowledge-retrieval
title: Search Knowledge
dataset_ids:
  - dataset-id-1
query_variable_selector:
  - '1732007415808'
  - user_query
```

### 9. http-request
**Purpose**: Make HTTP API calls

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "http-request"
- `title`: Display name
- `method`: "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS" (case insensitive)
- `url`: Request URL (supports variable substitution)
- `authorization`: Authorization configuration
- `headers`: Request headers string
- `params`: Query parameters string

**Authorization structure**:
- `type`: "no-auth" or "api-key"
- `config`: HttpRequestNodeAuthorizationConfig (when type is "api-key")
  - `type`: "basic", "bearer", or "custom"
  - `api_key`: API key value
  - `header`: Custom header name (for custom type)

**Body structure** (for POST/PUT/PATCH):
- `type`: "none", "form-data", "x-www-form-urlencoded", "raw-text", "json", or "binary"
- `data`: Array of BodyData objects
  - `key`: Field key
  - `type`: "file" or "text"
  - `value`: Field value (text type)
  - `file`: File variable selector (file type)

**Timeout structure** (optional):
- `connect`: Connect timeout in seconds (default from config)
- `read`: Read timeout in seconds (default from config)
- `write`: Write timeout in seconds (default from config)

**Other fields**:
- `ssl_verify`: Boolean, verify SSL certificates (default from config)
- `error_strategy`: "fail-branch" or "default-value" (optional)

**Source Handles**:
- Default: `"source"`
- With fail-branch: `"success-branch"`, `"fail-branch"`

**Outputs**:
- `body`: Response body (text or file)
- `status_code`: HTTP status code (integer)
- `headers`: Response headers (object)
- `files`: Downloaded file(s) if response is file type
- On fail-branch: `error_message`, `error_type`

**Example**:
```yaml
type: http-request
title: API Call
method: POST
url: "https://api.example.com/endpoint"
authorization:
  type: api-key
  config:
    type: bearer
    api_key: "{{#env.API_KEY#}}"
headers: |
  Content-Type: application/json
  Accept: application/json
params: ""
body:
  type: json
  data:
    - key: "input"
      type: text
      value: "{{#1732007415808.user_input#}}"
timeout:
  connect: 10
  read: 30
  write: 30
ssl_verify: true
error_strategy: fail-branch
```

### 10. template-transform
**Purpose**: Transform variables using Jinja2 templates

**Required fields**:
- `type`: "template-transform"
- `title`: Display name
- `template`: Jinja2 template string
- `variables`: Input variables

**Example**:
```yaml
type: template-transform
title: Format Output
template: "Hello {{name}}, your score is {{score}}"
variables:
  - variable: name
    value_selector:
      - '1732007415808'
      - user_name
  - variable: score
    value_selector:
      - '1733478343153'
      - result
```

## Additional Node Types

### 11. answer
**Purpose**: Output answer to user in chatflow/workflow

**Required fields**:
- `type`: "answer"
- `title`: Display name
- `answer`: Answer template string with variable references

**Example**:
```yaml
type: answer
title: Answer
answer: "The result is: {{#1733478262179.text#}}"
```

### 12. loop
**Purpose**: Execute a set of nodes multiple times with break conditions

**Execution Type**: CONTAINER

**Required fields**:
- `type`: "loop"
- `title`: Display name
- `loop_count`: Maximum number of iterations (integer)
- `break_conditions`: Array of Condition objects to break the loop
- `logical_operator`: "and" or "or" for combining break conditions
- `loop_variables`: Optional array of LoopVariableData for loop state
- `outputs`: Output configuration (dictionary)

**Loop Variable structure**:
- `label`: Variable label/name
- `var_type`: SegmentType (string, number, object, boolean, array types)
- `value_type`: "variable" or "constant"
- `value`: Initial value (variable selector or constant value)

**Break condition fields**: (same as if-else conditions)
- `variable_selector`: Array path to value
- `comparison_operator`: SupportedComparisonOperator
- `value`: Comparison value

**Source Handles**:
- `"loop"`: Continue loop iteration
- `"source"`: Exit loop (after completion or break)

**Outputs**:
- `output`: Array of outputs from each iteration
- `iteration`: Current iteration number
- On completion: metadata includes `completed_reason` ("loop_break" or "loop_completed")

**Internal nodes**:
- Loop creates internal sub-graph with loop-start and loop-end nodes
- Nodes between loop-start and loop-end execute on each iteration

**Example**:
```yaml
type: loop
title: Loop Processing
loop_count: 10
logical_operator: or
break_conditions:
  - variable_selector:
      - '1733478262179'
      - is_complete
    comparison_operator: is
    value: "true"
  - variable_selector:
      - '1733478262179'
      - error_count
    comparison_operator: ≥
    value: "3"
loop_variables:
  - label: counter
    var_type: number
    value_type: constant
    value: 0
  - label: accumulated_result
    var_type: array_object
    value_type: constant
    value: []
outputs:
  result:
    type: array_object
```

### 13. tool
**Purpose**: Call external tools or plugins

**Required fields**:
- `type`: "tool"
- `title`: Display name
- `provider_id`: Tool provider identifier
- `provider_type`: Tool provider type
- `tool_name`: Name of the tool
- `tool_parameters`: Tool-specific parameters

**Example**:
```yaml
type: tool
title: Call API Tool
provider_id: provider-123
provider_type: api
tool_name: fetch_data
tool_parameters:
  endpoint: "{{#1732007415808.api_endpoint#}}"
```

### 14. parameter-extractor
**Purpose**: Extract structured parameters from LLM output

**Required fields**:
- `type`: "parameter-extractor"
- `title`: Display name
- `model`: Model configuration
- `query`: Input text to extract from
- `parameters`: Parameter schema definitions

**Example**:
```yaml
type: parameter-extractor
title: Extract Parameters
model:
  provider: anthropic
  name: claude-3-5-sonnet-20241022
query:
  variable_selector:
    - '1732007415808'
    - user_input
parameters:
  - name: date
    type: string
    description: Extract the date mentioned
    required: true
```

### 15. variable-assigner
**Purpose**: Assign or transform variables

**Required fields**:
- `type`: "variable-assigner"
- `title`: Display name
- `variables`: Variable assignments

**Example**:
```yaml
type: variable-assigner
title: Assign Variables
variables:
  - variable: output_var
    value_selector:
      - '1733478262179'
      - text
```

### 16. question-classifier
**Purpose**: Classify user questions into categories

**Required fields**:
- `type`: "question-classifier"
- `title`: Display name
- `model`: Model configuration
- `query_variable_selector`: Input query
- `classes`: Classification categories

**Example**:
```yaml
type: question-classifier
title: Classify Question
model:
  provider: anthropic
  name: claude-3-5-sonnet-20241022
query_variable_selector:
  - '1732007415808'
  - user_query
classes:
  - name: technical
    description: Technical questions
  - name: general
    description: General questions
```

### 17. document-extractor
**Purpose**: Extract content from documents

**Required fields**:
- `type`: "document-extractor"
- `title`: Display name
- `variable_selector`: Document input

**Example**:
```yaml
type: document-extractor
title: Extract Document
variable_selector:
  - '1732007415808'
  - document_file
```

### 18. list-operator
**Purpose**: Perform operations on lists (filter, map, reduce)

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "list-operator"
- `title`: Display name
- `operation`: Operation type
- `variable_selector`: Input list selector

**Outputs**:
- Depends on operation type

**Example**:
```yaml
type: list-operator
title: Filter List
operation: filter
variable_selector:
  - '1733478262179'
  - items
```

## Advanced Node Types

### 19. agent
**Purpose**: Agent-based autonomous task execution

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "agent"
- `title`: Display name
- `model`: Model configuration
- `tools`: Available tools for agent
- `prompt`: Agent instructions

**Example**:
```yaml
type: agent
title: Research Agent
model:
  provider: anthropic
  name: claude-3-5-sonnet-20241022
tools:
  - web_search
  - calculator
prompt: "Research and provide information about {{#1732007415808.topic#}}"
```

### 20. trigger-webhook
**Purpose**: Webhook trigger for workflow execution

**Execution Type**: ROOT

**Required fields**:
- `type`: "trigger-webhook"
- `title`: Display name
- `variables`: Input variable definitions

**Important**: Cannot coexist with standard start nodes

**Example**:
```yaml
type: trigger-webhook
title: Webhook Trigger
variables:
  - variable: payload
    type: object
    required: true
```

### 21. trigger-schedule
**Purpose**: Scheduled/cron-based workflow execution

**Execution Type**: ROOT

**Required fields**:
- `type`: "trigger-schedule"
- `title`: Display name
- `schedule`: Cron expression or schedule config

**Important**: Cannot coexist with standard start nodes

**Example**:
```yaml
type: trigger-schedule
title: Daily Schedule
schedule:
  cron: "0 9 * * *"
  timezone: "UTC"
```

### 22. trigger-plugin
**Purpose**: Plugin-based workflow trigger

**Execution Type**: ROOT

**Required fields**:
- `type`: "trigger-plugin"
- `title`: Display name
- `plugin_id`: Plugin identifier

**Important**: Cannot coexist with standard start nodes

### 23. human-input
**Purpose**: Pause workflow for human input

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "human-input"
- `title`: Display name
- `variables`: Input variable definitions

**Behavior**:
- Workflow status changes to PAUSED
- Execution resumes when human provides input

**Example**:
```yaml
type: human-input
title: Request Approval
variables:
  - variable: approval_decision
    type: select
    options:
      - approve
      - reject
    required: true
```

### 24. datasource
**Purpose**: Data source integration as workflow entry point

**Execution Type**: ROOT

**Required fields**:
- `type`: "datasource"
- `title`: Display name
- `datasource_config`: Data source configuration

**Important**: Can serve as root node (alternative to start node)

### 25. knowledge-index
**Purpose**: Index content into knowledge base

**Execution Type**: EXECUTABLE

**Required fields**:
- `type`: "knowledge-index"
- `title`: Display name
- `dataset_id`: Target dataset identifier
- `content_selector`: Content to index

**Example**:
```yaml
type: knowledge-index
title: Index Content
dataset_id: "dataset-123"
content_selector:
  - '1732007415808'
  - processed_text
```

### 26. assigner (variable-assigner)
**Purpose**: Assign or transform variables with expressions

**Execution Type**: EXECUTABLE

**Note**: Different from variable-aggregator (which merges branches)

**Required fields**:
- `type`: "assigner"
- `title`: Display name
- `variables`: Variable assignment configurations

**Example**:
```yaml
type: assigner
title: Transform Variables
variables:
  - output_var: transformed_text
    expression: "upper(input_text)"
```

## Variable References

Variables are referenced using the syntax: `{{#node_id.field_name#}}`

**Examples**:
- `{{#1732007415808.user_input#}}` - Reference user_input from start node
- `{{#1733478262179.text#}}` - Reference text output from LLM node
- `{{#1733478343153.result#}}` - Reference result from code node
- `{{#1733478343153.error_message#}}` - Reference error_message from failed code node
- `{{#1733478343153.error_type#}}` - Reference error_type from failed code node

## Error Handling

### Fail Branch Strategy

Code and HTTP request nodes support `error_strategy: "fail-branch"` which creates an alternative execution path when the node fails.

**Source Handles**:
- `"success-branch"`: Normal execution path (success)
- `"fail-branch"`: Alternative error path (failure)

**Available error variables** (in fail-branch path):
- `error_message`: Human-readable error description (string)
- `error_type`: Error type/classification (string)

**Edge Configuration**:

Success edge:
```yaml
- id: code_node-success-branch-next_node-target
  source: code_node_id
  target: next_node_id
  sourceHandle: success-branch
  targetHandle: target
  data:
    sourceType: code
    targetType: llm  # or other target node type
```

Fail edge:
```yaml
- id: code_node-fail-branch-error_handler-target
  source: code_node_id
  target: error_handler_id
  sourceHandle: fail-branch
  targetHandle: target
  data:
    sourceType: code
    targetType: llm  # error handler node type
```

**Required convergence**: Both branches typically merge into a variable-aggregator before reaching the end node.

**Example workflow with error handling**:
```
Start → Code (fail-branch) → [Success → Aggregator] / [Fail → LLM Recovery → Aggregator] → End
```

### Default Value Strategy

Alternative simpler error handling:
```yaml
error_strategy: default-value
default_value:
  output: "default_text"
```

- Returns predefined default value on error
- Continues on main execution path (no branching)
- Less robust than fail-branch

### Retry Strategy

Configure automatic retries for transient failures:
```yaml
retry_config:
  max_retries: 3
  retry_interval: 1000  # milliseconds
```

### Abort Strategy (Default)

No configuration needed. Workflow stops on error:
```yaml
# No error_strategy field = abort on error (default)
```

## Node Type Summary

All 26+ available node types:

**ROOT** (Entry Points):
1. start - Standard workflow entry
2. datasource - Data source entry
3. trigger-webhook - Webhook trigger
4. trigger-schedule - Scheduled trigger
5. trigger-plugin - Plugin trigger

**EXECUTABLE** (Logic Nodes):
6. llm - Language model inference
7. code - Python/JavaScript execution
8. http-request - HTTP API calls
9. knowledge-retrieval - Query knowledge base
10. knowledge-index - Index to knowledge base
11. template-transform - Jinja2 templating
12. tool - External tool integration
13. parameter-extractor - LLM-based extraction
14. document-extractor - Document parsing
15. list-operator - List operations
16. agent - Autonomous agent
17. human-input - Pause for human input
18. assigner - Variable transformation

**BRANCH** (Conditional):
19. if-else - Conditional routing
20. question-classifier - Question classification

**CONTAINER** (Loops):
21. iteration - Array iteration
22. loop - Conditional looping

**RESPONSE** (Output):
23. answer - Mid-workflow output
24. end - Workflow termination

**UTILITY**:
25. variable-aggregator - Branch merging
26. variable-assigner - Legacy variable assignment (use assigner instead)
