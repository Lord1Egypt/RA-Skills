# Dify Workflow DSL Structure

This document describes the overall structure of a Dify workflow DSL file.

## Top-Level Structure

A complete Dify workflow DSL file has the following top-level structure:

```yaml
kind: app
version: 0.1.4
app:
  # App metadata
workflow:
  # Workflow definition
```

## App Section

Defines application-level metadata.

```yaml
app:
  name: Workflow Name
  description: Detailed description of the workflow
  mode: workflow  # Always "workflow" for workflow apps
  icon: 🔨  # Emoji icon
  icon_background: '#FFEAD5'  # Hex color
  use_icon_as_answer_icon: false
```

## Workflow Section

Contains the complete workflow definition with features, graph, and configuration.

### Structure

```yaml
workflow:
  features:
    # UI and interaction features
  environment_variables: []
  conversation_variables: []
  graph:
    nodes: []
    edges: []
  viewport:
    # Canvas view settings
```

## Features Configuration

### File Upload

```yaml
features:
  file_upload:
    enabled: true/false
    allowed_file_types:
      - image
      - document
    allowed_file_extensions:
      - .JPG
      - .PNG
      - .PDF
    allowed_file_upload_methods:
      - local_file
      - remote_url
    number_limits: 3
    fileUploadConfig:
      file_size_limit: 15
      image_file_size_limit: 5
      audio_file_size_limit: 50
      video_file_size_limit: 100
      batch_count_limit: 5
      workflow_file_upload_limit: 10
```

### Other Features

```yaml
features:
  opening_statement: 'Welcome message'
  suggested_questions: []
  suggested_questions_after_answer:
    enabled: false
  speech_to_text:
    enabled: false
  text_to_speech:
    enabled: false
    language: ''
    voice: ''
  retriever_resource:
    enabled: true
  sensitive_word_avoidance:
    enabled: false
```

## Graph Structure

The graph contains the visual workflow representation.

### Nodes Array

Each node has:

```yaml
nodes:
  - id: '1732007415808'  # Unique numeric string ID
    type: custom  # Always "custom"
    data:
      type: start  # Actual node type (start, end, llm, code, etc.)
      title: Node Title
      desc: Optional description
      selected: false
      # Type-specific configuration
    position:
      x: 100.5
      y: 200.0
    positionAbsolute:
      x: 100.5
      y: 200.0
    width: 244
    height: 90
    selected: false
    sourcePosition: right
    targetPosition: left
```

### Edges Array

Edges define connections between nodes.

```yaml
edges:
  - id: 1732007415808-source-1733478262179-target
    source: '1732007415808'  # Source node ID
    target: '1733478262179'  # Target node ID
    sourceHandle: source  # Or "fail-branch" for error paths
    targetHandle: target
    type: custom
    data:
      sourceType: start  # Source node type
      targetType: llm    # Target node type
      isInIteration: false
    zIndex: 0
    selected: false
```

**Edge naming convention**: `{source_id}-{handle}-{target_id}-target`

**Common handles**:
- `source`: Normal output flow
- `fail-branch`: Error handling flow (for code nodes)
- `true`: True branch (for if-else nodes)
- `false`: False branch (for if-else nodes)

## Viewport

Canvas view settings for the visual editor.

```yaml
viewport:
  x: 190.28
  y: 286.09
  zoom: 0.33
```

## ID Generation

Node IDs are typically Unix timestamps in milliseconds as strings:
- Example: `'1732007415808'`
- Generate in Python: `str(int(time.time() * 1000))`
- Must be unique within the workflow

## Complete Minimal Example

```yaml
kind: app
version: 0.1.4
app:
  name: Simple Workflow
  description: A basic workflow
  mode: workflow
  icon: 🚀
  icon_background: '#FFEAD5'
  use_icon_as_answer_icon: false
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    file_upload:
      enabled: false
    opening_statement: ''
    retriever_resource:
      enabled: false
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions: []
    suggested_questions_after_answer:
      enabled: false
    text_to_speech:
      enabled: false
  graph:
    nodes:
      - id: '1732007415808'
        type: custom
        data:
          type: start
          title: Start
          variables:
            - variable: user_input
              label: User Input
              type: paragraph
              required: true
              max_length: 1000
        position:
          x: 100
          y: 100
        positionAbsolute:
          x: 100
          y: 100
        width: 244
        height: 90
        selected: false
        sourcePosition: right
        targetPosition: left
      - id: '1732007415809'
        type: custom
        data:
          type: end
          title: End
          outputs:
            - variable: result
              value_selector:
                - '1732007415808'
                - user_input
        position:
          x: 400
          y: 100
        positionAbsolute:
          x: 400
          y: 100
        width: 244
        height: 90
        selected: false
        sourcePosition: right
        targetPosition: left
    edges:
      - id: 1732007415808-source-1732007415809-target
        source: '1732007415808'
        sourceHandle: source
        target: '1732007415809'
        targetHandle: target
        type: custom
        data:
          sourceType: start
          targetType: end
          isInIteration: false
        zIndex: 0
  viewport:
    x: 0
    y: 0
    zoom: 1
```

## Best Practices

1. **Unique IDs**: Always generate unique IDs for nodes and ensure edge IDs reference valid node IDs
2. **Consistent Positioning**: Space nodes adequately (300-400 pixels apart horizontally)
3. **Edge Validation**: Ensure source and target nodes exist before creating edges
4. **Type Matching**: Ensure edge data.sourceType and data.targetType match actual node types
5. **Variable References**: Always use the format `{{#node_id.field_name#}}` for variable references
6. **Error Handling**: Use variable-aggregator to merge success/fail branches before end node
