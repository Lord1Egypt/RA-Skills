"""
LanceDB index management for Ghostclaw vector store.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import pyarrow as pa
import lancedb

logger = logging.getLogger("ghostclaw.vector_store.index")


class VectorIndex:
    """Handles LanceDB table operations and similarity search with optional IVF-PQ index."""

    def __init__(self, db_path: Path, index_config: Optional[Dict] = None):
        """
        Initialize vector index.

        Args:
            db_path: Path to LanceDB database
            index_config: Configuration for vector index (type, partitions, sub_vectors, training_sample_size)
                          e.g., {"type": "ivf_pq", "partitions": 256, "sub_vectors": 64, "training_sample_size": 10000}
        """
        self.db_path = db_path
        self._conn = None
        self._table = None
        self.index_config = index_config or {}
        self._index_ready = False

    def connect(self) -> None:
        """Establish connection to LanceDB."""
        if self._conn is not None:
            return
        self.db_path.mkdir(parents=True, exist_ok=True)
        self._conn = lancedb.connect(str(self.db_path))
        if "embeddings" in self._conn.list_tables():
            self._table = self._conn.open_table("embeddings")

    def ensure_table(self) -> None:
        """Create the embeddings table if it doesn't exist."""
        self.connect()
        if self._table is None:
            schema = pa.schema([
                ("report_id", pa.int64()),
                ("chunk_id", pa.string()),
                ("text", pa.string()),
                ("vector", lancedb.vector(384)),
                ("repo_path", pa.string()),
                ("timestamp", pa.string()),
                ("vibe_score", pa.int32()),
                ("stack", pa.string()),
            ])
            self._table = self._conn.create_table("embeddings", schema=schema, mode="overwrite")
            logger.info("Created embeddings table")

    async def ensure_index(self) -> None:
        """Create IVF-PQ index if configured and not already present."""
        if not self._table:
            self.ensure_table()  # make sure table exists
        if not self._table or self._index_ready:
            return

        idx_cfg = self.index_config
        if not idx_cfg.get("enabled", True):
            logger.info("Vector index disabled by config; using brute-force search")
            return

        index_type = idx_cfg.get("type", "ivf_pq")
        if index_type != "ivf_pq":
            logger.warning("Unknown index type: %s; falling back to brute-force", index_type)
            return

        # Check if index already exists (optional; we'll just try to create)
        try:
            # Need to train on sample data
            training_sample_size = idx_cfg.get("training_sample_size", 10000)
            # Use LanceDB's dataset sampling
            total_rows = len(self._table)
            if total_rows < 1000:
                logger.warning("Insufficient training data for IVF-PQ (need >=1000 vectors, have %d); skipping index", total_rows)
                return

            # Sample up to training_sample_size rows
            sample_size = min(training_sample_size, total_rows)
            # Convert to pandas for sampling (LanceDB has to_pandas)
            df = self._table.to_pandas()
            training_data = df.sample(n=sample_size, random_state=42)
            if len(training_data) < 1000:
                logger.warning("Sampled data too small for training (%d rows)", len(training_data))
                return

            train_vectors = training_data['vector'].tolist()

            logger.info("Creating IVF-PQ index with %d partitions, %d sub_vectors, training on %d vectors",
                        idx_cfg.get("partitions", 256), idx_cfg.get("sub_vectors", 64), len(train_vectors))
            # LanceDB create_index
            self._table.create_index(
                column="vector",
                metric="cosine",
                index_type="IVF_PQ",
                num_partitions=idx_cfg.get("partitions", 256),
                num_sub_vectors=idx_cfg.get("sub_vectors", 64),
                replace=False
            )
            self._index_ready = True
            logger.info("IVF-PQ index created successfully")
        except Exception as e:
            logger.error("Failed to create IVF-PQ index: %s; falling back to brute-force", e)

    def add_records(self, records: List[Dict[str, Any]]) -> None:
        """Add records to the embeddings table."""
        self.ensure_table()
        table = pa.Table.from_pydict({
            "report_id": [r["report_id"] for r in records],
            "chunk_id": [r["chunk_id"] for r in records],
            "text": [r["text"] for r in records],
            "vector": [r["vector"] for r in records],
            "repo_path": [r["repo_path"] for r in records],
            "timestamp": [r["timestamp"] for r in records],
            "vibe_score": [r["vibe_score"] for r in records],
            "stack": [r["stack"] for r in records],
        })
        self._table.add(table)

    def search(self, query_vector: List[float], limit: int, where_clause: Optional[str] = None) -> List[Dict[str, Any]]:
        """Perform vector similarity search."""
        self.connect()
        if self._table is None:
            return []

        results = self._table.search(
            query=query_vector,
            vector_column_name="vector",
        ).metric("cosine").limit(limit * 3)

        if where_clause:
            results = results.where(where_clause, prefilter=True)

        arrow_table = results.to_arrow()
        return arrow_table.to_pylist()

    def clear(self) -> None:
        """Drop the embeddings table."""
        self.connect()
        if self._table:
            self._conn.drop_table("embeddings")
            self._table = None

    @property
    def table(self):
        return self._table
