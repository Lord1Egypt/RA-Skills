"""
原子化RAG知识库构建器

提供从PDF到原子化知识库的完整流程。
"""

import os
import json
import uuid
from typing import List, Dict, Optional
from dataclasses import dataclass
import re

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Milvus, Chroma


@dataclass
class KnowledgeAtom:
    """知识原子数据结构"""
    atom_id: str
    atom_type: str
    title: str
    content: str
    metadata: Dict
    methodology: Dict
    embedding: Optional[List[float]] = None


class AtomicRAGBuilder:
    """
    原子化RAG知识库构建器
    
    核心功能：
    1. 格式转化：消除PDF视觉盲区
    2. 语义分段：按知识完整性拆分
    3. 方法论提炼：去故事留方法
    4. 元数据提取：多维度标签
    5. 向量化存储：准备检索
    """
    
    def __init__(self, domain: str = "general", embedding_model: str = "text-embedding-ada-002"):
        """
        初始化构建器
        
        Args:
            domain: 领域 (math/physics/chemistry/medicine/general)
            embedding_model: 嵌入模型名称
        """
        self.domain = domain
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        
        # 根据领域选择处理器
        self.processor = self._get_processor(domain)
    
    def _get_processor(self, domain: str):
        """获取领域专用处理器"""
        from .processors import (
            MathProcessor,
            PhysicsProcessor,
            ChemistryProcessor,
            MedicineProcessor,
            GeneralProcessor
        )
        
        processors = {
            "math": MathProcessor(),
            "physics": PhysicsProcessor(),
            "chemistry": ChemistryProcessor(),
            "medicine": MedicineProcessor(),
            "general": GeneralProcessor()
        }
        
        return processors.get(domain, GeneralProcessor())
    
    def process_pdf(self, file_path: str, metadata: Dict = None) -> List[KnowledgeAtom]:
        """
        处理PDF文件，生成原子化知识库
        
        Args:
            file_path: PDF文件路径
            metadata: 书籍元信息
            
        Returns:
            List[KnowledgeAtom]: 知识原子列表
        """
        print(f"🔄 开始处理: {file_path}")
        
        # Step 1: 格式转化
        raw_text = self._extract_text(file_path)
        
        # Step 2: 语义分段
        chunks = self._semantic_chunk(raw_text)
        
        # Step 3: 方法论提炼 + Step 4: 元数据提取
        atoms = []
        for i, chunk in enumerate(chunks):
            print(f"  处理第 {i+1}/{len(chunks)} 个知识块...")
            
            atom = self._create_atom(chunk, metadata, i)
            atoms.append(atom)
        
        # Step 5: 向量化存储
        atoms = self._vectorize_atoms(atoms)
        
        print(f"✅ 完成！共生成 {len(atoms)} 个知识原子")
        return atoms
    
    def _extract_text(self, file_path: str) -> str:
        """
        Step 1: 格式转化 - 提取PDF文本
        检测PDF类型（扫描件/文本），进行OCR处理
        """
        import pdfplumber
        
        text_parts = []
        
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # 提取文本
                text = page.extract_text()
                
                # 如果文本太少，可能是扫描件，需要OCR
                if not text or len(text) < 100:
                    text = self._ocr_page(page)
                
                # 提取表格
                tables = page.extract_tables()
                if tables:
                    table_text = self._process_tables(tables)
                    text += "\n" + table_text
                
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _ocr_page(self, page) -> str:
        """对扫描件页面进行OCR"""
        try:
            import pytesseract
            from PIL import Image
            
            img = page.to_image(resolution=300)
            pil_img = Image.open(img.original)
            text = pytesseract.image_to_string(pil_img, lang='chi_sim+eng')
            return text
        except Exception as e:
            print(f"  ⚠️ OCR失败: {e}")
            return ""
    
    def _process_tables(self, tables: List) -> str:
        """处理表格数据"""
        table_texts = []
        for table in tables:
            rows = []
            for row in table:
                row_text = " | ".join(str(cell) for cell in row if cell)
                rows.append(row_text)
            table_texts.append("\n".join(rows))
        return "\n\n".join(table_texts)
    
    def _semantic_chunk(self, text: str, max_chunk_size: int = 2000) -> List[str]:
        """
        Step 2: 语义分段
        按知识完整性分段，不是按字数硬切
        """
        # 识别章节标题
        chapter_pattern = r'(第[一二三四五六七八九十]+[章节]|[0-9]+\.[0-9]+|[一二三四五六七八九十]、|\([0-9]+\))'
        
        # 先按章节分割
        parts = re.split(f'({chapter_pattern})', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for part in parts:
            part_size = len(part)
            
            # 如果当前块加上这部分超过限制，先保存当前块
            if current_size + part_size > max_chunk_size and current_chunk:
                chunks.append("".join(current_chunk))
                current_chunk = [part]
                current_size = part_size
            else:
                current_chunk.append(part)
                current_size += part_size
        
        # 添加最后一块
        if current_chunk:
            chunks.append("".join(current_chunk))
        
        return chunks
    
    def _create_atom(self, chunk: str, metadata: Dict, index: int) -> KnowledgeAtom:
        """
        Step 3: 方法论提炼 + Step 4: 元数据提取
        """
        # 生成唯一ID
        atom_id = f"atom_{metadata.get('subject', 'general')}_{index:04d}"
        
        # 提取标题（第一行或前50字）
        title = self._extract_title(chunk)
        
        # 领域处理器提取专业内容
        processed = self.processor.process(chunk)
        
        # 构建元数据
        atom_metadata = {
            "source_title": metadata.get("title", ""),
            "source_author": metadata.get("author", ""),
            "atom_index": index,
            "char_count": len(chunk),
            **processed.get("metadata", {})
        }
        
        # 构建方法论
        methodology = {
            "steps": processed.get("steps", []),
            "key_points": processed.get("key_points", []),
            "common_mistakes": processed.get("common_mistakes", []),
            "verification": processed.get("verification", "")
        }
        
        return KnowledgeAtom(
            atom_id=atom_id,
            atom_type=self.domain,
            title=title,
            content=chunk,
            metadata=atom_metadata,
            methodology=methodology
        )
    
    def _extract_title(self, text: str) -> str:
        """从文本中提取标题"""
        lines = text.strip().split('\n')
        
        # 尝试第一行作为标题
        if lines:
            first_line = lines[0].strip()
            # 如果第一行很短（<50字），可能是标题
            if len(first_line) < 50 and len(first_line) > 5:
                return first_line
        
        # 否则取前30字
        return text[:30].replace('\n', ' ') + "..."
    
    def _vectorize_atoms(self, atoms: List[KnowledgeAtom]) -> List[KnowledgeAtom]:
        """
        Step 5: 向量化存储
        """
        print("🔄 正在生成向量嵌入...")
        
        texts = [atom.content for atom in atoms]
        embeddings = self.embeddings.embed_documents(texts)
        
        for atom, embedding in zip(atoms, embeddings):
            atom.embedding = embedding
        
        print(f"✅ 已生成 {len(atoms)} 个向量嵌入")
        return atoms
    
    def store_to_vector_db(self, atoms: List[KnowledgeAtom], 
                          collection_name: str = "knowledge_base",
                          db_type: str = "chroma"):
        """
        存储到向量数据库
        
        Args:
            atoms: 知识原子列表
            collection_name: 集合名称
            db_type: 数据库类型 (chroma/milvus)
        """
        print(f"🔄 正在存储到 {db_type} 数据库...")
        
        texts = [atom.content for atom in atoms]
        metadatas = [
            {
                "atom_id": atom.atom_id,
                "title": atom.title,
                **atom.metadata
            }
            for atom in atoms
        ]
        ids = [atom.atom_id for atom in atoms]
        
        if db_type == "chroma":
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
                ids=ids,
                collection_name=collection_name
            )
        elif db_type == "milvus":
            vectorstore = Milvus.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
                ids=ids,
                collection_name=collection_name
            )
        
        print(f"✅ 已存储到向量数据库: {collection_name}")
        return vectorstore
    
    def save_atoms_to_json(self, atoms: List[KnowledgeAtom], output_path: str):
        """保存原子到JSON文件"""
        data = []
        for atom in atoms:
            data.append({
                "atom_id": atom.atom_id,
                "atom_type": atom.atom_type,
                "title": atom.title,
                "content": atom.content,
                "metadata": atom.metadata,
                "methodology": atom.methodology,
                "embedding": atom.embedding[:10] if atom.embedding else None  # 只保存前10个用于检查
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保存到: {output_path}")
