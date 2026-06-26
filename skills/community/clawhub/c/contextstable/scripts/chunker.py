from .config import config


class TextChunker:
    def __init__(self):
        self.chunk_size = config.chunker.chunk_size
        self.chunk_overlap = config.chunker.chunk_overlap
        self.separators = config.chunker.separators

    def split_text(self, long_text: str) -> list:
        if len(long_text) <= self.chunk_size:
            return [(0, long_text)]

        chunks = []
        start = 0
        chunk_id = 0

        while start < len(long_text):
            end = start + self.chunk_size

            if end >= len(long_text):
                chunk = long_text[start:]
                chunks.append((chunk_id, chunk.strip()))
                break

            best_split = end
            for sep in self.separators:
                pos = long_text.rfind(sep, start, end)
                if pos > start + self.chunk_size // 2:
                    best_split = pos + len(sep)
                    break

            chunk = long_text[start:best_split]
            chunks.append((chunk_id, chunk.strip()))

            start = best_split - self.chunk_overlap
            if start <= 0:
                start = best_split
            chunk_id += 1

        return chunks
