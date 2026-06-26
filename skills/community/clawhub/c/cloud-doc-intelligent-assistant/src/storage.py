"""数据存储模块"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    create_engine, Index, inspect
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from .models import Document as DocModel


Base = declarative_base()


class DocumentDB(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content_hash = Column(String(64), nullable=False)
    last_modified = Column(DateTime, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    versions = relationship("DocumentVersionDB", back_populates="document", cascade="all, delete-orphan")
    changes = relationship("ChangeDB", back_populates="document", cascade="all, delete-orphan")


class DocumentVersionDB(Base):
    __tablename__ = 'document_versions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False, index=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)
    metadata_json = Column(Text, nullable=True)
    version = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    document = relationship("DocumentDB", back_populates="versions")
    __table_args__ = (Index('idx_doc_version', 'document_id', 'version'),)


class ScanRecordDB(Base):
    __tablename__ = 'scan_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False)
    documents_scanned = Column(Integer, nullable=True)
    changes_detected = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    changes = relationship("ChangeDB", back_populates="scan", cascade="all, delete-orphan")


class ChangeDB(Base):
    __tablename__ = 'changes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(Integer, ForeignKey('scan_records.id'), nullable=False, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False, index=True)
    change_type = Column(String(50), nullable=False)
    diff = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    scan = relationship("ScanRecordDB", back_populates="changes")
    document = relationship("DocumentDB", back_populates="changes")


class DocumentStorage:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)
        self._ensure_optional_columns()

    def _ensure_optional_columns(self) -> None:
        inspector = inspect(self.engine)
        existing_tables = set(inspector.get_table_names())
        required_columns = {
            "documents": {"metadata_json": "TEXT"},
            "document_versions": {"metadata_json": "TEXT"},
        }
        with self.engine.begin() as conn:
            for table_name, columns in required_columns.items():
                if table_name not in existing_tables:
                    continue
                existing_columns = {col["name"] for col in inspector.get_columns(table_name)}
                for col_name, col_type in columns.items():
                    if col_name not in existing_columns:
                        conn.exec_driver_sql(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}")

    def get_session(self) -> Session:
        return self.SessionLocal()

    @staticmethod
    def _serialize_metadata(metadata: Optional[Dict[str, Any]]) -> Optional[str]:
        if metadata is None:
            return None
        return json.dumps(metadata or {}, ensure_ascii=False)

    @staticmethod
    def _deserialize_metadata(metadata_json: Optional[str]) -> Dict[str, Any]:
        if not metadata_json:
            return {}
        try:
            value = json.loads(metadata_json)
            return value if isinstance(value, dict) else {}
        except Exception:
            return {}

    def save_document(self, doc: DocModel) -> int:
        session = self.get_session()
        try:
            existing = session.query(DocumentDB).filter_by(url=doc.url).first()
            if existing:
                existing.title = doc.title
                existing.content_hash = doc.content_hash
                existing.last_modified = doc.last_modified
                existing.metadata_json = self._serialize_metadata(doc.metadata)
                existing.updated_at = datetime.now()
                session.commit()
                return existing.id
            else:
                db_doc = DocumentDB(
                    url=doc.url, title=doc.title, content_hash=doc.content_hash,
                    last_modified=doc.last_modified,
                    metadata_json=self._serialize_metadata(doc.metadata),
                )
                session.add(db_doc)
                session.commit()
                return db_doc.id
        finally:
            session.close()

    def get_document(self, url: str) -> Optional[DocModel]:
        session = self.get_session()
        try:
            db_doc = session.query(DocumentDB).filter_by(url=url).first()
            if not db_doc:
                return None
            latest_version = (
                session.query(DocumentVersionDB)
                .filter_by(document_id=db_doc.id)
                .order_by(DocumentVersionDB.version.desc())
                .first()
            )
            content = latest_version.content if latest_version else ""
            metadata = self._deserialize_metadata(
                latest_version.metadata_json if latest_version else db_doc.metadata_json
            )
            return DocModel(
                url=db_doc.url, title=db_doc.title, content=content,
                content_hash=db_doc.content_hash, last_modified=db_doc.last_modified,
                crawled_at=db_doc.updated_at, metadata=metadata,
            )
        finally:
            session.close()

    def get_all_documents(self) -> List[DocModel]:
        session = self.get_session()
        try:
            db_docs = session.query(DocumentDB).all()
            documents = []
            for db_doc in db_docs:
                latest_version = (
                    session.query(DocumentVersionDB)
                    .filter_by(document_id=db_doc.id)
                    .order_by(DocumentVersionDB.version.desc())
                    .first()
                )
                content = latest_version.content if latest_version else ""
                metadata = self._deserialize_metadata(
                    latest_version.metadata_json if latest_version else db_doc.metadata_json
                )
                documents.append(DocModel(
                    url=db_doc.url, title=db_doc.title, content=content,
                    content_hash=db_doc.content_hash, last_modified=db_doc.last_modified,
                    crawled_at=db_doc.updated_at, metadata=metadata,
                ))
            return documents
        finally:
            session.close()

    def save_version(self, doc_id: int, content: str, content_hash: str,
                     metadata: Optional[Dict[str, Any]] = None) -> int:
        session = self.get_session()
        try:
            latest_version = (
                session.query(DocumentVersionDB)
                .filter_by(document_id=doc_id)
                .order_by(DocumentVersionDB.version.desc())
                .first()
            )
            if latest_version and latest_version.content_hash == content_hash:
                if metadata is not None:
                    latest_version.metadata_json = self._serialize_metadata(metadata)
                    session.commit()
                return latest_version.id
            next_version = (latest_version.version + 1) if latest_version else 1
            version = DocumentVersionDB(
                document_id=doc_id, content=content, content_hash=content_hash,
                metadata_json=self._serialize_metadata(metadata), version=next_version,
            )
            session.add(version)
            session.commit()
            return version.id
        finally:
            session.close()

    def save_scan_record(self, started_at: datetime, status: str = "running") -> int:
        session = self.get_session()
        try:
            scan = ScanRecordDB(started_at=started_at, status=status)
            session.add(scan)
            session.commit()
            return scan.id
        finally:
            session.close()

    def update_scan_record(self, scan_id: int, completed_at: Optional[datetime] = None,
                           status: Optional[str] = None, documents_scanned: Optional[int] = None,
                           changes_detected: Optional[int] = None,
                           error_message: Optional[str] = None) -> None:
        session = self.get_session()
        try:
            scan = session.query(ScanRecordDB).filter_by(id=scan_id).first()
            if scan:
                if completed_at:
                    scan.completed_at = completed_at
                if status:
                    scan.status = status
                if documents_scanned is not None:
                    scan.documents_scanned = documents_scanned
                if changes_detected is not None:
                    scan.changes_detected = changes_detected
                if error_message:
                    scan.error_message = error_message
                session.commit()
        finally:
            session.close()

    # ---- 便捷方法（供 skills 调用）----

    def get_latest(self, url: str) -> Optional[DocModel]:
        """获取最新版本文档，等同于 get_document"""
        return self.get_document(url)

    def save(self, doc: DocModel) -> None:
        """保存文档及其版本（便捷方法）"""
        doc_id = self.save_document(doc)
        self.save_version(doc_id, doc.content, doc.content_hash, doc.metadata)

    def search_local(self, keyword: str, cloud: Optional[str] = None, limit: int = 50) -> List[DocModel]:
        """从本地数据库按关键词搜索已存储的文档
        
        Args:
            keyword: 搜索关键词，匹配 title 或 url
            cloud: 云厂商过滤（通过 url 域名判断）
            limit: 最大返回数量
            
        Returns:
            匹配的文档列表（含最新版本内容）
        """
        cloud_domain_map = {
            "aliyun": "help.aliyun.com",
            "tencent": "cloud.tencent.com",
            "baidu": "cloud.baidu.com",
            "volcano": "volcengine.com",
        }
        session = self.get_session()
        try:
            query = session.query(DocumentDB)
            # 按关键词模糊匹配 title 或 url
            if keyword:
                kw = f"%{keyword}%"
                query = query.filter(
                    (DocumentDB.title.ilike(kw)) | (DocumentDB.url.ilike(kw))
                )
            # 按云厂商过滤
            if cloud and cloud in cloud_domain_map:
                domain = cloud_domain_map[cloud]
                query = query.filter(DocumentDB.url.ilike(f"%{domain}%"))
            db_docs = query.order_by(DocumentDB.updated_at.desc()).limit(limit).all()
            documents = []
            for db_doc in db_docs:
                latest_version = (
                    session.query(DocumentVersionDB)
                    .filter_by(document_id=db_doc.id)
                    .order_by(DocumentVersionDB.version.desc())
                    .first()
                )
                content = latest_version.content if latest_version else ""
                metadata = self._deserialize_metadata(
                    latest_version.metadata_json if latest_version else db_doc.metadata_json
                )
                documents.append(DocModel(
                    url=db_doc.url, title=db_doc.title, content=content,
                    content_hash=db_doc.content_hash, last_modified=db_doc.last_modified,
                    crawled_at=db_doc.updated_at, metadata=metadata,
                ))
            return documents
        finally:
            session.close()

    def save_change(self, scan_id: int, document_id: int, change_type: str,
                    diff: Optional[str] = None, summary: Optional[str] = None) -> int:
        session = self.get_session()
        try:
            change = ChangeDB(scan_id=scan_id, document_id=document_id,
                              change_type=change_type, diff=diff, summary=summary)
            session.add(change)
            session.commit()
            return change.id
        finally:
            session.close()
