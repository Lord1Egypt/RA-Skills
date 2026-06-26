# Memory Fields API

Memory Fields implement **Holographic Quantum Encoding (HQE)** from the Sentient Observer formalism. They provide hierarchical holographic memory with global, user, and conversation scopes.

## Features

- **Holographic Memory Fields** with global, user, and conversation scopes
- **Prime-indexed storage** with holographic interference patterns
- **Similarity-based retrieval** via resonance correlation
- **Consensus verification** for shared knowledge
- **Checkpoint/rollback** with SHA-256 integrity verification
- **Cross-scope synchronization** and knowledge synthesis

## Endpoints

### Create Memory Field

```
POST /api/memory
```

Request body:
```json
{
  "name": "Research Notes",
  "scope": "user",
  "description": "AI research findings",
  "consensusThreshold": 0.85,
  "visibility": "private"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "field_abc123",
    "primeSignature": "...",
    "entropy": 0.1
  }
}
```

### List Memory Fields

```
GET /api/memory
```

Query parameters:
- `scope`: global, user, conversation, organization
- `includePublic`: true/false

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "field_abc123",
      "name": "Research Notes",
      "scope": "user",
      "consensusScore": 0.9,
      "locked": false
    }
  ]
}
```

### Get Field Details

```
GET /api/memory/:fieldId
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "field_abc123",
    "metadata": { ... },
    "entropy": 0.5,
    "consensusScore": 0.9,
    "contributionCount": 42
  }
}
```

### Store to Memory Field

```
POST /api/memory/:fieldId/store
```

Request body:
```json
{
  "content": "The speed of light is constant",
  "significance": 0.9,
  "metadata": { "source": "physics_book" }
}
```

Response:
```json
{
  "success": true,
  "data": {
    "fragmentId": "frag_xyz789",
    "primeSignature": "...",
    "checksum": "sha256:..."
  }
}
```

### Query Memory Field

```
POST /api/memory/:fieldId/query
```

Request body:
```json
{
  "query": "speed of electromagnetic radiation",
  "threshold": 0.5,
  "limit": 10
}
```

Response:
```json
{
  "success": true,
  "data": {
    "fragments": [
      {
        "content": "The speed of light is constant",
        "similarity": 0.85,
        "confidence": 0.9,
        "sourceNode": "node_123"
      }
    ]
  }
}
```

### Query Global Field

```
POST /api/memory/global/query
```

Request body:
```json
{
  "query": "quantum entanglement",
  "minConsensus": 0.7
}
```

### Sync Conversation Memory

```
POST /api/memory/sync
```

Request body:
```json
{
  "conversationId": "conv_xyz",
  "targetFieldId": "field_abc123",
  "verifiedOnly": true
}
```

Response:
```json
{
  "success": true,
  "data": {
    "syncedFragmentCount": 5,
    "entropyDelta": -0.05
  }
}
```

### Field Entropy

```
GET /api/memory/:fieldId/entropy
```

Response:
```json
{
  "success": true,
  "data": {
    "shannon": 0.45,
    "trend": "stable",
    "coherence": 0.8
  }
}
```

### Create Checkpoint

```
POST /api/memory/:fieldId/checkpoint
```

Response:
```json
{
  "success": true,
  "data": {
    "path": "/path/to/checkpoint",
    "checksum": "sha256:...",
    "timestamp": 1705320000000
  }
}
```

### Rollback to Checkpoint

```
POST /api/memory/:fieldId/rollback
```

Request body:
```json
{
  "checkpointId": "cp_123"
}
```
