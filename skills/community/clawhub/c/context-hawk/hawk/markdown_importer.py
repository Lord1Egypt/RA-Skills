"""
markdown_importer.py — 用户 markdown 记忆文件导入器

功能：
- 扫描 ~/.openclaw/memory/ 下的所有 .md 文件
- 按 ## / ### 分块，保留结构
- 转 embeddings → 存入 LanceDB
- 增量导入（用 hawk:imported 标签去重）
- 与 hawk 记忆系统无缝融合
"""

import os
import glob
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Chunk:
    source_file: str
    chunk_id: str
    title: str
    heading: str
    content: str
    file_mtime: float


def _get_table(table_name="memory_chunks", db_path="~/.hawk/lancedb"):
    try:
        import lancedb
        db_path = os.path.expanduser(db_path)
        os.makedirs(db_path, exist_ok=True)
        db = lancedb.connect(db_path)
        if table_name not in db.table_names():
            return None
        return db.open_table(table_name)
    except Exception:
        return None


class MarkdownImporter:
    """把用户的 .md 记忆文件导入到 LanceDB"""

    def __init__(self, memory_dir="~/.openclaw/memory", table_name="memory_chunks"):
        self.memory_dir = os.path.expanduser(memory_dir)
        self.table_name = table_name

    def scan(self):
        """扫描所有 .md 文件，按 ## 分块"""
        chunks = []
        for filepath in glob.glob(os.path.join(self.memory_dir, "*.md")):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if '<!-- hawk:imported -->' in content:
                continue  # 增量跳过
            chunks.extend(self._parse_file_content(filepath, content))
        return chunks

    def _parse_file_content(self, filepath, content):
        """Parse file from already-read content (avoids double-read)"""
        mtime = os.path.getmtime(filepath)
        filename = os.path.basename(filepath)

    def _parse_file(self, filepath):
        """Legacy method — kept for backward compat. Use _parse_file_content for efficiency."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._parse_file_content(filepath, content)

        title = ""
        m = re.search(r'^# (.+)$', content, re.MULTILINE)
        if m:
            title = m.group(1)

        chunks = []
        idx = 0
        lines = content.split('\n')
        current_h2 = ""
        current_h3 = ""

        for i, line in enumerate(lines):
            if re.match(r'^## (.+)$', line):
                current_h2 = re.match(r'^## (.+)$', line).group(1).strip()
                current_h3 = ""
            elif re.match(r'^### (.+)$', line):
                current_h3 = re.match(r'^### (.+)$', line).group(1).strip()
            elif line.strip() and not line.startswith('#'):
                chunk_id = hashlib.sha256(
                    f"{filename}:{idx}:{line[:50]}".encode()
                ).hexdigest()[:16]
                heading = f"{current_h2} / {current_h3}" if current_h3 else current_h2
                chunks.append(Chunk(
                    source_file=filename,
                    chunk_id=chunk_id,
                    title=title,
                    heading=heading,
                    content=line.strip(),
                    file_mtime=mtime,
                ))
                idx += 1

        return chunks

    def embed_and_store(self, chunks, batch=20):
        """转 embeddings → LanceDB"""
        if not chunks:
            return 0
        try:
            import lancedb
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(f"缺少依赖: {e}\n请运行: python3.12 -m pip install lancedb openai")

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("请设置 OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        db_path = os.path.expanduser("~/.hawk/lancedb")
        os.makedirs(db_path, exist_ok=True)
        db = lancedb.connect(db_path)

        if self.table_name in db.table_names():
            db.drop_table(self.table_name)

        table = db.create_table(self.table_name, schema=lancedb.schema([
            ("chunk_id", "string"),
            ("source_file", "string"),
            ("title", "string"),
            ("heading", "string"),
            ("content", "string"),
            ("file_mtime", "float64"),
            ("imported_at", "float64"),
            ("vector", "vector(1536)"),
        ]))

        for i in range(0, len(chunks), batch):
            batch_chunks = chunks[i:i + batch]
            texts = [c.content for c in batch_chunks]
            resp = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
            )
            rows = [{
                "chunk_id": c.chunk_id,
                "source_file": c.source_file,
                "title": c.title,
                "heading": c.heading,
                "content": c.content,
                "file_mtime": c.file_mtime,
                "imported_at": datetime.now().timestamp(),
                "vector": vec,
            } for c, vec in zip(batch_chunks, [d.embedding for d in resp.data])]
            table.add(rows)

        # 打标签
        for c in chunks:
            fp = os.path.join(self.memory_dir, c.source_file)
            if os.path.exists(fp):
                with open(fp, 'r', encoding='utf-8') as f:
                    existing = f.read()
                if '<!-- hawk:imported -->' not in existing:
                    with open(fp, 'a', encoding='utf-8') as f:
                        f.write(f"\n<!-- hawk:imported {datetime.now().date()} -->\n")

        return len(chunks)

    def import_all(self):
        """一键增量导入"""
        chunks = self.scan()
        if not chunks:
            return {"files": 0, "chunks": 0, "skipped": 0}
        count = self.embed_and_store(chunks)
        return {"files": len(set(c.source_file for c in chunks)), "chunks": count, "skipped": 0}
