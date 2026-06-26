"""
完整性检查器

实现文档完整性检查逻辑，继承自 Core 层的 BaseChecker。
通过依赖注入接收 SemanticMatcherProtocol 实例，不直接依赖 Infrastructure 层。
"""

import re
from typing import List, Optional, Dict, Any
import logging

from ...core.checker_base import BaseChecker, CheckResult, CheckStatus
from ...core.interfaces import SemanticMatcherProtocol
from ...core.document import Document
from ...core.checklist_model import Checklist, RequiredDocument
from ...core.result_model import CompletenessResult, DocumentMatch, MatchType

logger = logging.getLogger(__name__)


class CompletenessChecker(BaseChecker):
    """
    完整性检查器

    检查必需文档是否已上传，支持文件名精确匹配和语义匹配。
    语义匹配通过注入的 SemanticMatcherProtocol 实现，不直接依赖 LLM/Embedding。
    """

    def __init__(
        self,
        matcher: SemanticMatcherProtocol,
        similarity_threshold: float = 0.75,
        use_semantic: bool = True,
    ):
        """
        初始化完整性检查器

        Args:
            matcher: 语义匹配器实例（符合 SemanticMatcherProtocol 接口）
            similarity_threshold: 语义匹配阈值（默认0.75）
            use_semantic: 是否使用语义匹配
        """
        self.matcher = matcher
        self.similarity_threshold = similarity_threshold
        self.use_semantic = use_semantic

    @property
    def name(self) -> str:
        """检查器唯一标识"""
        return "completeness"

    @property
    def description(self) -> str:
        """检查器描述"""
        return "检查必需文档是否已上传，支持文件名语义匹配"

    def _exact_match(
        self, file_name: str, required_doc: RequiredDocument
    ) -> Optional[DocumentMatch]:
        """
        精确匹配检查

        匹配逻辑：
        1. 文件名包含清单名称
        2. 文件名包含任一别名
        3. 去除扩展名后匹配
        """
        names = [required_doc.name] + required_doc.aliases
        clean_file_name = re.sub(
            r"\.(pdf|docx?|jpg|jpeg|png|tiff|bmp)$", "", file_name, flags=re.IGNORECASE
        )

        for name in names:
            # 直接包含匹配
            if name in file_name:
                return DocumentMatch(
                    document_name=required_doc.name,
                    status=CheckStatus.VALID,
                    matched_file=file_name,
                    match_type=MatchType.EXACT,
                    similarity=1.0,
                    requirement="必须上传",
                )

            # 清理后匹配
            clean_name = re.sub(
                r"\.(pdf|docx?|jpg|jpeg|png|tiff|bmp)$", "", name, flags=re.IGNORECASE
            )
            if clean_name in clean_file_name or clean_file_name in clean_name:
                return DocumentMatch(
                    document_name=required_doc.name,
                    status=CheckStatus.VALID,
                    matched_file=file_name,
                    match_type=MatchType.ALIAS,
                    similarity=0.95,
                    requirement="必须上传",
                )

        return None

    async def _semantic_match(
        self, file_name: str, required_doc: RequiredDocument
    ) -> Optional[DocumentMatch]:
        """
        语义匹配检查

        使用注入的 matcher 计算相似度，不直接调用 LLM/Embedding。
        """
        if not self.use_semantic:
            return None

        names = [required_doc.name] + required_doc.aliases

        try:
            best_match, similarity = await self.matcher.find_best_match(file_name, names)

            if similarity >= self.similarity_threshold:
                return DocumentMatch(
                    document_name=required_doc.name,
                    status=CheckStatus.VALID,
                    matched_file=file_name,
                    match_type=MatchType.SEMANTIC,
                    similarity=round(similarity, 2),
                    requirement="必须上传",
                )
        except Exception as e:
            logger.warning(f"语义匹配失败: {e}")

        return None

    async def match_document(self, file_name: str, required_doc: RequiredDocument) -> DocumentMatch:
        """
        匹配单个文档

        匹配优先级：
        1. 精确匹配
        2. 语义匹配
        3. 未匹配
        """
        # 1. 尝试精确匹配
        exact_result = self._exact_match(file_name, required_doc)
        if exact_result:
            return exact_result

        # 2. 尝试语义匹配
        if self.use_semantic:
            semantic_result = await self._semantic_match(file_name, required_doc)
            if semantic_result:
                return semantic_result

        # 3. 未匹配
        return DocumentMatch(
            document_name=required_doc.name,
            status=CheckStatus.MISSING,
            matched_file=None,
            match_type=MatchType.NONE,
            similarity=0.0,
            requirement="必须上传",
        )

    async def check(
        self,
        documents: List[Document],
        checklist: Optional[Checklist],
        doc_checks: Dict[str, Any],
    ) -> CheckResult:
        """
        执行完整性检查

        Args:
            documents: 已上传的文档列表
            checklist: 审核清单
            doc_checks: 检查配置（来自清单的 checks 配置）

        Returns:
            CheckResult: 检查结果
        """
        if not checklist:
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.ERROR,
                message="缺少审核清单",
            )

        file_names = [doc.name for doc in documents]
        required_docs = checklist.required_documents

        details: List[DocumentMatch] = []
        uploaded_count = 0
        missing_count = 0

        # 为每个必需文档寻找匹配
        for req_doc in required_docs:
            if not req_doc.required:
                continue

            matched = False
            best_match: Optional[DocumentMatch] = None

            for file_name in file_names:
                match_result = await self.match_document(file_name, req_doc)

                if match_result.status != CheckStatus.MISSING:
                    matched = True
                    if best_match is None or match_result.similarity > best_match.similarity:
                        best_match = match_result

            if matched and best_match:
                details.append(best_match)
                uploaded_count += 1
            else:
                # 未找到匹配
                details.append(
                    DocumentMatch(
                        document_name=req_doc.name,
                        status=CheckStatus.MISSING,
                        matched_file=None,
                        match_type=MatchType.NONE,
                        similarity=0.0,
                        requirement="必须上传",
                    )
                )
                missing_count += 1

        # 确定整体状态
        total_required = len([d for d in required_docs if d.required])

        # 构建缺失文件名列表
        missing_names = [d.document_name for d in details if d.status == CheckStatus.MISSING]
        missing_names_str = "、".join(missing_names) if missing_names else "无"

        if missing_count == 0:
            status = CheckStatus.PASS
            pass_status = "通过"
        elif uploaded_count == 0:
            status = CheckStatus.INCOMPLETE
            pass_status = "未通过"
        else:
            status = CheckStatus.INCOMPLETE
            pass_status = "未通过"

        # 生成业务话术
        message = f"完整审查情况：{uploaded_count}/{total_required}个文件存在，{missing_names_str}缺少，完整性审查{pass_status}。"

        # 构建 CompletenessResult
        completeness_result = CompletenessResult(
            status=status,
            total_required=total_required,
            uploaded=uploaded_count,
            missing=missing_count,
            details=details,
        )

        return CheckResult(
            check_type=self.name,
            status=status,
            message=message,
            details={
                "completeness_result": completeness_result.model_dump(),
                "total_required": total_required,
                "uploaded": uploaded_count,
                "missing": missing_count,
                "matches": [
                    {
                        "document_name": d.document_name,
                        "status": d.status.value,
                        "matched_file": d.matched_file,
                        "match_type": d.match_type.value,
                        "similarity": d.similarity,
                    }
                    for d in details
                ],
            },
        )
