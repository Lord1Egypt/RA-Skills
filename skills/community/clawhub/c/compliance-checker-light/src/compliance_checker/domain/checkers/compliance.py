"""
视觉检查器

实现印章、签名等视觉元素检查逻辑，继承自 Core 层的 BaseChecker。
通过依赖注入接收 VisualCheckerProtocol 实例，不直接依赖 Infrastructure 层。

业务规则（检测提示词）定义在此层，调用 visual_client 时传入。
"""

from typing import List, Optional, Dict, Any
from enum import Enum
import logging
import os
import tempfile

from ...core.checker_base import BaseChecker, CheckResult, CheckStatus
from ...core.interfaces import VisualCheckerProtocol, PDFConverterProtocol
from ...core.document import Document
from ...core.checklist_model import Checklist

logger = logging.getLogger(__name__)


# ============================================================================
# 业务规则：视觉检测提示词（Domain 层核心知识）
# ============================================================================

SEAL_DETECT_PROMPT = """请仔细检查这张图片，判断是否存在公章（红色圆形印章）。

请按以下格式回答：
1. 是否存在公章：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"右下角"、"页面中央"等]
4. 说明：[简要说明判断依据]

请确保回答简洁明确。"""

SIGNATURE_DETECT_PROMPT = """请仔细检查这张图片，判断是否存在手写签名。

请按以下格式回答：
1. 是否存在签名：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"签字栏"、"页面底部"等]
4. 说明：[简要说明判断依据]

请确保回答简洁明确。"""

BOTH_DETECT_PROMPT = """请仔细检查这张图片，判断是否存在公章和手写签名。

请按以下格式回答：

【公章检查】
1. 是否存在公章：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"右下角"等]

【签名检查】
1. 是否存在签名：[是/否]
2. 置信度：[高/中/低]
3. 位置描述：[如"签字栏"等]

【说明】
简要说明判断依据"""


class VisualCheckType(str, Enum):
    """视觉检查类型枚举"""

    SEAL = "seal"  # 公章检查
    SIGNATURE = "signature"  # 签名检查
    BOTH = "both"  # 同时检查公章和签名


class VisualChecker(BaseChecker):
    """
    视觉检查器

    检查文档中的印章、签名等视觉元素。
    通过注入的 VisualCheckerProtocol 实例调用底层视觉检测能力，
    不直接依赖具体的视觉客户端实现（如 QwenVLClient）。

    使用方式：
        # 在 Application 层组装依赖
        visual_checker = VisualChecker(
            visual_client=qwen_vl_client,  # Infrastructure 层实现
            default_check_type="both",
            confidence_threshold=0.7,
        )
    """

    def __init__(
        self,
        visual_client: VisualCheckerProtocol,
        pdf_converter: Optional[PDFConverterProtocol] = None,
        default_check_type: str = "both",
        confidence_threshold: float = 0.7,
        enabled: bool = True,
    ):
        """
        初始化视觉检查器

        Args:
            visual_client: 视觉检测客户端实例（符合 VisualCheckerProtocol 接口）
            pdf_converter: PDF 转换器实例（符合 PDFConverterProtocol 接口），用于处理 PDF 文件
            default_check_type: 默认检查类型 ("seal" | "signature" | "both")
            confidence_threshold: 置信度阈值，低于此值视为不确定
            enabled: 是否启用视觉检查
        """
        self.visual_client = visual_client
        self.pdf_converter = pdf_converter
        self.default_check_type = default_check_type
        self.confidence_threshold = confidence_threshold
        self.enabled = enabled

    @property
    def name(self) -> str:
        """检查器唯一标识"""
        return "compliance"

    @property
    def description(self) -> str:
        """检查器描述"""
        return "检查文档中的印章、签名等视觉元素"

    def is_available(self) -> bool:
        """检查视觉检测能力是否可用"""
        return self.enabled and self.visual_client.is_available()

    def _parse_check_type(self, doc_checks: Dict[str, Any]) -> VisualCheckType:
        """
        从检查配置中解析检查类型

        Args:
            doc_checks: 检查配置

        Returns:
            VisualCheckType 枚举值
        """
        check_type_str = doc_checks.get("visual_type", self.default_check_type)
        try:
            return VisualCheckType(check_type_str.lower())
        except ValueError:
            logger.warning(
                f"未知的检查类型: {check_type_str}，使用默认值: {self.default_check_type}"
            )
            return VisualCheckType(self.default_check_type)

    def _determine_status(
        self, found: bool, confidence: float, check_type: VisualCheckType
    ) -> CheckStatus:
        """
        根据检测结果确定状态

        Args:
            found: 是否检测到
            confidence: 置信度
            check_type: 检查类型

        Returns:
            CheckStatus 枚举值
        """
        if not found:
            return CheckStatus.MISSING

        if confidence < self.confidence_threshold:
            return CheckStatus.UNCLEAR

        return CheckStatus.VALID

    def _is_pdf_file(self, file_path: str) -> bool:
        """
        判断文件是否为 PDF 格式

        Args:
            file_path: 文件路径

        Returns:
            True 如果是 PDF 文件
        """
        return file_path.lower().endswith(".pdf")

    def _is_image_file(self, file_path: str) -> bool:
        """
        判断文件是否为图片格式

        Args:
            file_path: 文件路径

        Returns:
            True 如果是图片文件
        """
        image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")
        return file_path.lower().endswith(image_extensions)

    async def _check_single_document(
        self,
        document: Document,
        check_type: VisualCheckType,
        context: Optional[str],
        page_hint: Optional[int],
    ) -> Dict[str, Any]:
        """
        检查单个文档的视觉元素

        支持图片文件（.jpg, .png 等）和 PDF 文件。
        对于 PDF 文件，会先将其转换为图片再进行视觉检测。

        Args:
            document: 文档对象
            check_type: 检查类型
            context: 上下文信息
            page_hint: 页码提示

        Returns:
            检查结果字典
        """
        result = {
            "document_name": document.name,
            "document_path": document.path,
            "check_type": check_type.value,
            "seal_result": None,
            "signature_result": None,
            "status": CheckStatus.ERROR.value,
            "message": "",
        }

        # 检查视觉客户端是否可用
        if not self.visual_client.is_available():
            result["status"] = CheckStatus.UNAVAILABLE.value
            result["message"] = "视觉检测服务不可用，请检查 API 配置"
            return result

        try:
            # 根据文件类型选择处理方式
            if self._is_image_file(document.path):
                # 图片文件：直接检测
                return await self._check_image_document(document, check_type, context, page_hint)
            elif self._is_pdf_file(document.path):
                # PDF 文件：需要转换为图片后检测
                return await self._check_pdf_document(document, check_type, context, page_hint)
            else:
                # 不支持的文件类型
                result["status"] = CheckStatus.ERROR.value
                result["message"] = f"不支持的文件类型: {document.path}"
                return result

        except Exception as e:
            logger.error(f"视觉检查异常: {e}", exc_info=True)
            result["status"] = CheckStatus.ERROR.value
            result["message"] = f"检查过程发生错误: {str(e)}"
            return result

    async def _check_image_document(
        self,
        document: Document,
        check_type: VisualCheckType,
        context: Optional[str],
        page_hint: Optional[int],
    ) -> Dict[str, Any]:
        """
        检查图片文件的视觉元素

        Args:
            document: 文档对象
            check_type: 检查类型
            context: 上下文信息
            page_hint: 页码提示

        Returns:
            检查结果字典
        """
        result = {
            "document_name": document.name,
            "document_path": document.path,
            "check_type": check_type.value,
            "seal_result": None,
            "signature_result": None,
            "status": CheckStatus.ERROR.value,
            "message": "",
        }

        # 根据检查类型调用相应的检测方法
        if check_type == VisualCheckType.SEAL:
            seal_result = await self.visual_client.detect_seal(
                image_path=document.path,
                context=SEAL_DETECT_PROMPT,
            )
            result["seal_result"] = seal_result

            if seal_result.get("success"):
                found = seal_result.get("found", False)
                confidence = seal_result.get("confidence", 0.0)
                result["status"] = self._determine_status(found, confidence, check_type).value
                result["message"] = seal_result.get("reasoning", "")
            else:
                result["status"] = CheckStatus.ERROR.value
                result["message"] = seal_result.get("error", "检测失败")

        elif check_type == VisualCheckType.SIGNATURE:
            sig_result = await self.visual_client.detect_signature(
                image_path=document.path,
                context=SIGNATURE_DETECT_PROMPT,
            )
            result["signature_result"] = sig_result

            if sig_result.get("success"):
                found = sig_result.get("found", False)
                confidence = sig_result.get("confidence", 0.0)
                result["status"] = self._determine_status(found, confidence, check_type).value
                result["message"] = sig_result.get("reasoning", "")
            else:
                result["status"] = CheckStatus.ERROR.value
                result["message"] = sig_result.get("error", "检测失败")

        elif check_type == VisualCheckType.BOTH:
            # 同时检查印章和签名
            seal_result = await self.visual_client.detect_seal(
                image_path=document.path,
                context=SEAL_DETECT_PROMPT,
            )
            sig_result = await self.visual_client.detect_signature(
                image_path=document.path,
                context=SIGNATURE_DETECT_PROMPT,
            )

            result["seal_result"] = seal_result
            result["signature_result"] = sig_result

            # 综合判断状态
            seal_found = seal_result.get("success") and seal_result.get("found", False)
            sig_found = sig_result.get("success") and sig_result.get("found", False)

            seal_conf = seal_result.get("confidence", 0.0) if seal_result.get("success") else 0.0
            sig_conf = sig_result.get("confidence", 0.0) if sig_result.get("success") else 0.0

            # 构建综合消息
            messages = []
            if seal_result.get("success"):
                messages.append(
                    f"印章: {'已发现' if seal_found else '未发现'} (置信度: {seal_conf:.2f})"
                )
            else:
                messages.append(f"印章检测失败: {seal_result.get('error', '未知错误')}")

            if sig_result.get("success"):
                messages.append(
                    f"签名: {'已发现' if sig_found else '未发现'} (置信度: {sig_conf:.2f})"
                )
            else:
                messages.append(f"签名检测失败: {sig_result.get('error', '未知错误')}")

            result["message"] = "; ".join(messages)

            # 确定综合状态
            if seal_found and sig_found:
                result["status"] = CheckStatus.VALID.value
            elif seal_found or sig_found:
                result["status"] = CheckStatus.VALID.value
            elif not seal_result.get("success") or not sig_result.get("success"):
                result["status"] = CheckStatus.ERROR.value
            else:
                result["status"] = CheckStatus.MISSING.value

        return result

    async def _check_pdf_document(
        self,
        document: Document,
        check_type: VisualCheckType,
        context: Optional[str],
        page_hint: Optional[int],
    ) -> Dict[str, Any]:
        """
        检查 PDF 文件的视觉元素

        将 PDF 转换为图片后，逐页进行视觉检测。
        只要有一页通过检查，即认为文档通过。

        Args:
            document: 文档对象
            check_type: 检查类型
            context: 上下文信息
            page_hint: 页码提示（优先检查指定页）

        Returns:
            检查结果字典
        """
        result = {
            "document_name": document.name,
            "document_path": document.path,
            "check_type": check_type.value,
            "seal_result": None,
            "signature_result": None,
            "status": CheckStatus.ERROR.value,
            "message": "",
            "pages_checked": 0,
            "total_pages": 0,
        }

        # 检查 PDF 转换器是否可用
        if not self.pdf_converter:
            result["status"] = CheckStatus.ERROR.value
            result["message"] = "PDF 文件需要转换器，但未提供 pdf_converter 依赖"
            return result

        try:
            # 将 PDF 转换为图片
            logger.info(f"正在将 PDF 转换为图片: {document.name}")
            images = await self.pdf_converter.convert_to_images(document.path)
            result["total_pages"] = len(images)
            logger.info(f"PDF 转换完成，共 {len(images)} 页")

            if not images:
                result["status"] = CheckStatus.ERROR.value
                result["message"] = "PDF 转换失败：未生成任何图片"
                return result

            # 确定检查顺序（如果提供了页码提示，优先检查该页）
            page_order = list(range(len(images)))
            if page_hint is not None and 0 <= page_hint - 1 < len(images):
                # 将提示页移到最前面
                page_order.remove(page_hint - 1)
                page_order.insert(0, page_hint - 1)

            # 逐页检查
            for page_idx in page_order:
                page_num = page_idx + 1
                image_bytes = images[page_idx]
                result["pages_checked"] += 1

                logger.debug(f"正在检查第 {page_num}/{len(images)} 页")

                # 检查当前页
                page_result = await self._check_single_image_bytes(
                    image_bytes, check_type, page_num
                )

                # 如果找到目标元素，立即返回成功
                if page_result["status"] == CheckStatus.VALID.value:
                    result.update(page_result)
                    result["message"] = (
                        f"第 {page_num} 页检测通过: {page_result.get('message', '')}"
                    )
                    return result

                # 保存最后一页的结果用于返回
                if page_idx == page_order[-1]:
                    result.update(page_result)

            # 所有页面都未通过
            result["status"] = CheckStatus.MISSING.value
            result["message"] = f"已检查 {result['pages_checked']} 页，未找到目标视觉元素"
            return result

        except Exception as e:
            logger.error(f"PDF 视觉检查失败: {e}", exc_info=True)
            result["status"] = CheckStatus.ERROR.value
            result["message"] = f"PDF 检查失败: {str(e)}"
            return result

    async def _check_single_image_bytes(
        self,
        image_bytes: bytes,
        check_type: VisualCheckType,
        page_num: int,
    ) -> Dict[str, Any]:
        """
        检查单张图片字节流的视觉元素

        Args:
            image_bytes: 图片字节流
            check_type: 检查类型
            page_num: 页码（用于日志记录）

        Returns:
            检查结果字典
        """
        result = {
            "seal_result": None,
            "signature_result": None,
            "status": CheckStatus.ERROR.value,
            "message": "",
        }

        # 检查视觉客户端是否有字节流检测方法
        has_bytes_method = hasattr(self.visual_client, "detect_seal_from_bytes")

        if check_type == VisualCheckType.SEAL:
            if has_bytes_method:
                seal_result = await self.visual_client.detect_seal_from_bytes(
                    image_bytes=image_bytes,
                    context=SEAL_DETECT_PROMPT,
                )
            else:
                # 回退到临时文件方式
                seal_result = await self._detect_with_temp_file(image_bytes, "seal")
            result["seal_result"] = seal_result

            if seal_result.get("success"):
                found = seal_result.get("found", False)
                confidence = seal_result.get("confidence", 0.0)
                result["status"] = self._determine_status(found, confidence, check_type).value
                result["message"] = seal_result.get("reasoning", "")
            else:
                result["status"] = CheckStatus.ERROR.value
                result["message"] = seal_result.get("error", "检测失败")

        elif check_type == VisualCheckType.SIGNATURE:
            if has_bytes_method:
                sig_result = await self.visual_client.detect_signature_from_bytes(
                    image_bytes=image_bytes,
                    context=SIGNATURE_DETECT_PROMPT,
                )
            else:
                sig_result = await self._detect_with_temp_file(image_bytes, "signature")
            result["signature_result"] = sig_result

            if sig_result.get("success"):
                found = sig_result.get("found", False)
                confidence = sig_result.get("confidence", 0.0)
                result["status"] = self._determine_status(found, confidence, check_type).value
                result["message"] = sig_result.get("reasoning", "")
            else:
                result["status"] = CheckStatus.ERROR.value
                result["message"] = sig_result.get("error", "检测失败")

        elif check_type == VisualCheckType.BOTH:
            # 同时检查印章和签名
            if has_bytes_method:
                seal_result = await self.visual_client.detect_seal_from_bytes(
                    image_bytes=image_bytes,
                    context=SEAL_DETECT_PROMPT,
                )
                sig_result = await self.visual_client.detect_signature_from_bytes(
                    image_bytes=image_bytes,
                    context=SIGNATURE_DETECT_PROMPT,
                )
            else:
                seal_result = await self._detect_with_temp_file(image_bytes, "seal")
                sig_result = await self._detect_with_temp_file(image_bytes, "signature")

            result["seal_result"] = seal_result
            result["signature_result"] = sig_result

            # 综合判断状态
            seal_found = seal_result.get("success") and seal_result.get("found", False)
            sig_found = sig_result.get("success") and sig_result.get("found", False)

            seal_conf = seal_result.get("confidence", 0.0) if seal_result.get("success") else 0.0
            sig_conf = sig_result.get("confidence", 0.0) if sig_result.get("success") else 0.0

            # 构建综合消息
            messages = []
            if seal_result.get("success"):
                messages.append(
                    f"印章: {'已发现' if seal_found else '未发现'} (置信度: {seal_conf:.2f})"
                )
            else:
                messages.append(f"印章检测失败: {seal_result.get('error', '未知错误')}")

            if sig_result.get("success"):
                messages.append(
                    f"签名: {'已发现' if sig_found else '未发现'} (置信度: {sig_conf:.2f})"
                )
            else:
                messages.append(f"签名检测失败: {sig_result.get('error', '未知错误')}")

            result["message"] = "; ".join(messages)

            # 确定综合状态
            if seal_found and sig_found:
                result["status"] = CheckStatus.VALID.value
            elif seal_found or sig_found:
                result["status"] = CheckStatus.VALID.value
            elif not seal_result.get("success") or not sig_result.get("success"):
                result["status"] = CheckStatus.ERROR.value
            else:
                result["status"] = CheckStatus.MISSING.value

        return result

    async def _detect_with_temp_file(
        self, image_bytes: bytes, detection_type: str
    ) -> Dict[str, Any]:
        """
        使用临时文件方式检测图片字节流

        当视觉客户端不支持字节流直接检测时，使用此方法作为回退。

        Args:
            image_bytes: 图片字节流
            detection_type: 检测类型 ("seal" 或 "signature")

        Returns:
            检测结果字典
        """
        import asyncio

        # 创建临时文件
        suffix = ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        try:
            if detection_type == "seal":
                result = await self.visual_client.detect_seal(
                    image_path=tmp_path,
                    context=SEAL_DETECT_PROMPT,
                )
            else:
                result = await self.visual_client.detect_signature(
                    image_path=tmp_path,
                    context=SIGNATURE_DETECT_PROMPT,
                )
            return result
        finally:
            # 异步删除临时文件
            try:
                await asyncio.to_thread(os.unlink, tmp_path)
            except Exception as e:
                logger.warning(f"删除临时文件失败: {e}")

    async def check(
        self,
        documents: List[Document],
        checklist: Optional[Checklist],
        doc_checks: Dict[str, Any],
    ) -> CheckResult:
        """
        执行视觉检查

        Args:
            documents: 已解析的文档列表
            checklist: 审核清单
            doc_checks: 检查配置，可包含以下字段：
                - visual_type: 检查类型 ("seal" | "signature" | "both")
                - target_documents: 目标文档名称列表（可选，默认检查所有文档）
                - context: 上下文信息（如文档类型，用于辅助检测）
                - page_hint: 建议检查的页码
                - enabled: 是否启用（可覆盖构造函数配置）

        Returns:
            CheckResult: 检查结果
        """
        # 检查是否启用
        enabled = doc_checks.get("enabled", self.enabled)
        if not enabled:
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.UNAVAILABLE,
                message="视觉检查已禁用",
                details={"reason": "disabled_by_config"},
            )

        # 检查视觉客户端是否可用
        if not self.visual_client.is_available():
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.UNAVAILABLE,
                message="视觉检测服务不可用，请检查 API 配置（如 QWEN_API_KEY）",
                details={"reason": "visual_client_unavailable"},
            )

        # 检查文档列表
        if not documents:
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.ERROR,
                message="没有可检查的文档",
            )

        # 解析检查类型和配置
        check_type = self._parse_check_type(doc_checks)
        context = doc_checks.get("context")
        page_hint = doc_checks.get("page_hint")

        # 确定要检查的文档
        target_names = doc_checks.get("target_documents", [])
        if target_names:
            target_docs = [d for d in documents if d.name in target_names]
        else:
            target_docs = documents

        if not target_docs:
            return CheckResult(
                check_type=self.name,
                status=CheckStatus.ERROR,
                message=f"未找到目标文档: {target_names}",
                details={"requested": target_names, "available": [d.name for d in documents]},
            )

        # 执行检查
        results = []
        for doc in target_docs:
            doc_result = await self._check_single_document(
                document=doc,
                check_type=check_type,
                context=context,
                page_hint=page_hint,
            )
            results.append(doc_result)

        # 汇总结果
        total = len(results)
        valid_count = sum(1 for r in results if r["status"] == CheckStatus.VALID.value)
        missing_count = sum(1 for r in results if r["status"] == CheckStatus.MISSING.value)
        error_count = sum(1 for r in results if r["status"] == CheckStatus.ERROR.value)
        unclear_count = sum(1 for r in results if r["status"] == CheckStatus.UNCLEAR.value)

        # 确定要求的印章类型描述
        if check_type == VisualCheckType.SEAL:
            required_element = "公章"
        elif check_type == VisualCheckType.SIGNATURE:
            required_element = "签名"
        else:
            required_element = "公章和签名"

        # 确定整体状态和生成业务话术
        if error_count > 0:
            overall_status = CheckStatus.ERROR
            pass_status = "未通过"
        elif valid_count == total:
            overall_status = CheckStatus.PASS
            pass_status = "通过"
        elif missing_count == total:
            overall_status = CheckStatus.FAIL
            pass_status = "未通过"
        elif valid_count > 0:
            overall_status = CheckStatus.HAS_ISSUES
            pass_status = "部分通过"
        else:
            overall_status = CheckStatus.UNCLEAR
            pass_status = "未通过"

        # 生成业务话术
        overall_message = f"识别到{required_element}，合规性审查{pass_status}。"

        # 构建 issues 列表
        issues = []
        for r in results:
            if r["status"] != CheckStatus.VALID.value:
                issues.append(
                    {
                        "document": r["document_name"],
                        "status": r["status"],
                        "message": r["message"],
                    }
                )

        return CheckResult(
            check_type=self.name,
            status=overall_status,
            message=overall_message,
            details={
                "check_type": check_type.value,
                "total_documents": total,
                "valid_count": valid_count,
                "missing_count": missing_count,
                "error_count": error_count,
                "unclear_count": unclear_count,
                "confidence_threshold": self.confidence_threshold,
                "document_results": results,
            },
            issues=issues,
        )
