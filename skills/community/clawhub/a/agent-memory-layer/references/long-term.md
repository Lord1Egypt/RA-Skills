# Long-Term Memory (Knowledge Store)

## Design
- Persistent facts, preferences, learned patterns
- Tag-based indexing for fast retrieval
- Vector similarity search for semantic retrieval (production)

## Vector Search Production Config

```python
import numpy as np

class VectorLongTerm:
    def __init__(self, embed_dim: int = 1536):
        self.embeddings = []  # np.ndarray (N, embed_dim)
        self.items = []       # MemoryItem[]
        self.tag_index = defaultdict(list)

    def store(self, content: str, embedding: np.ndarray, tags: list[str] = None):
        item = MemoryItem(content=content, tags=tags or [])
        self.items.append(item)
        self.embeddings.append(embedding)
        for tag in (tags or []):
            self.tag_index[tag].append(len(self.items) - 1)

    def search(self, query_embedding: np.ndarray, limit: int = 10, min_score: float = 0.7) -> list:
        if not self.embeddings:
            return []
        matrix = np.array(self.embeddings)
        scores = matrix @ query_embedding / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_embedding) + 1e-8)
        top_k = np.argsort(scores)[::-1][:limit]
        return [{"content": self.items[i].content, "score": float(scores[i]), "tags": self.items[i].tags}
                for i in top_k if scores[i] >= min_score]
```

## Qdrant Production Setup

```python
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
client.create_collection(collection_name="agent_memory", vectors_config={"size": 1536, "distance": "Cosine"})
```
