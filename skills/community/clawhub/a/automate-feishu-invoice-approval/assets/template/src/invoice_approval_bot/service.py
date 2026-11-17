"""发票识别与费用报销审批的核心业务编排服务。

本模块负责串联飞书消息接收、图片下载、Codex 视觉识别、发票查重、
审批表单渲染、审批提交和结果回执。各步骤的处理状态会同步写入本地存储，
便于审计、排查失败以及避免重复提交。
"""

from __future__ import annotations

import hashlib
import json
import logging
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

from .cards import build_invoice_confirmation_card, build_invoice_decision_card
from .config import Settings
from .errors import BotError, ConfigurationError
from .lark import LarkClient
from .mapping import (
    invoice_context,
    load_mapping,
    mapping_needs_upload,
    missing_required_fields,
    render_form,
)
from .risk import invoice_risk_reasons
from .storage import SubmissionStore
from .vision import CodexVisionExtractor

LOGGER = logging.getLogger(__name__)
# UUID v5 的固定命名空间，用于根据飞书消息 ID 生成可重复的审批请求 UUID。
UUID_NAMESPACE = uuid.UUID("f430ed74-e25e-4a91-97d3-91628da816c9")
def invoice_fingerprint(invoice: Mapping[str, Any]) -> str:
    """根据发票的关键业务字段生成稳定指纹，用于拦截重复报销。"""

    # 字符串字段统一去除首尾空格并转为大写，避免格式差异影响查重。
    parts = [
        str(invoice.get("seller_tax_id") or "").strip().upper(),
        str(invoice.get("invoice_code") or "").strip().upper(),
        str(invoice.get("invoice_number") or "").strip().upper(),
        str(invoice.get("issue_date") or "").strip(),
        str(invoice.get("total_amount") or "").strip(),
    ]
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    """分块计算文件的 SHA-256，避免读取大图时一次性占用过多内存。"""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_header_value(value: Any) -> str:
    """统一全角字符并移除 OCR 容易插入的空白或零宽格式字符。"""

    normalized = unicodedata.normalize("NFKC", str(value or ""))
    return "".join(
        character
        for character in normalized
        if not character.isspace() and unicodedata.category(character) != "Cf"
    )


def buyer_header_mismatches(
    invoice: Mapping[str, Any],
    required_buyer_name: str,
    required_buyer_tax_id: str,
) -> list[str]:
    """返回购方抬头不符合要求的具体原因；完全匹配时返回空列表。"""

    actual_name = str(invoice.get("buyer_name") or "").strip()
    actual_tax_id = str(invoice.get("buyer_tax_id") or "").strip()
    normalized_name = _normalize_header_value(actual_name)
    normalized_tax_id = _normalize_header_value(actual_tax_id).upper()
    mismatches = []

    if normalized_name != _normalize_header_value(required_buyer_name):
        if actual_name:
            mismatches.append(
                f"购方名称不符合要求：识别为“{actual_name}”，"
                f"应为“{required_buyer_name}”"
            )
        else:
            mismatches.append(f"未识别到购方名称，应为“{required_buyer_name}”")

    normalized_required_tax_id = _normalize_header_value(required_buyer_tax_id).upper()
    if normalized_tax_id != normalized_required_tax_id:
        if actual_tax_id:
            mismatches.append(
                f"购方税号不符合要求：识别为“{actual_tax_id}”，"
                f"应为“{required_buyer_tax_id}”"
            )
        else:
            mismatches.append(f"未识别到购方税号，应为“{required_buyer_tax_id}”")

    return mismatches


class InvoiceApprovalService:
    """处理飞书发票图片并按配置生成或提交费用报销审批。"""

    def __init__(
        self,
        settings: Settings,
        *,
        lark: Optional[LarkClient] = None,
        store: Optional[SubmissionStore] = None,
        vision: Optional[CodexVisionExtractor] = None,
    ) -> None:
        # 先创建数据目录，再初始化映射、飞书客户端、存储和视觉识别器。
        settings.ensure_directories()
        self.settings = settings
        self.mapping = load_mapping(settings.mapping_path)
        self.lark = lark or LarkClient(settings.lark_cli_bin)
        self.store = store or SubmissionStore(settings.database_path)
        self.vision = vision or CodexVisionExtractor(
            codex_bin=settings.codex_bin,
            schema_path=settings.invoice_schema_path,
            output_dir=settings.codex_output_dir,
            project_dir=settings.project_dir,
            timeout_seconds=settings.codex_timeout_seconds,
            model=settings.codex_model,
        )
        # 环境变量中的审批定义 Code 优先于映射文件中的配置。
        self.approval_code = settings.approval_code or str(
            self.mapping.get("approval_code", "")
        ).strip()
        if not self.approval_code or self.approval_code.startswith("请替换"):
            raise ConfigurationError("请配置真实的费用报销 approval_code")

    def _safe_reply(self, message_id: str, text: str, suffix: str) -> None:
        """尽力回复用户；回复失败不能覆盖已经完成的主业务状态。"""

        if not self.settings.reply_enabled:
            return
        try:
            # 使用带消息 ID 的幂等键，防止重试时重复发送相同回执。
            self.lark.reply(message_id, text, f"{message_id}-{suffix}")
        except Exception as exc:
            LOGGER.exception("回复飞书消息失败")
            self.store.update(message_id, reply_error=str(exc)[:2000])

    def _review_reason(
        self, invoice: Mapping[str, Any], missing: list[str]
    ) -> Optional[str]:
        """汇总所有需要人工复核的原因；无需复核时返回 None。"""

        reasons = list(invoice.get("review_reasons") or [])
        if invoice.get("document_type") != "invoice":
            reasons.append("图片未被可靠识别为发票")
        confidence = float(invoice.get("overall_confidence") or 0)
        if confidence < self.settings.min_confidence:
            reasons.append(
                f"总体置信度 {confidence:.2f} 低于阈值 {self.settings.min_confidence:.2f}"
            )
        if missing:
            reasons.append("缺少必填字段：" + "、".join(missing))
        if invoice.get("needs_review"):
            reasons.append("Codex 标记此票据需要人工复核")
        return "；".join(dict.fromkeys(str(reason) for reason in reasons)) or None

    def _build_approval_payload(
        self,
        record: Mapping[str, Any],
        invoice: Mapping[str, Any],
        *,
        upload_files: bool,
    ) -> Dict[str, Any]:
        """在用户确认后上传附件并构造最终审批请求。"""

        message_id = str(record["message_id"])
        sender = str(record.get("sender_open_id") or "")
        image_path = Path(str(record["image_path"]))
        event = json.loads(str(record["event_json"]))
        if not isinstance(event, dict):
            raise BotError("数据库中的原始飞书事件不是 JSON 对象")

        approval_file: Dict[str, str] = {}
        for upload_type in ("image", "attachment"):
            if not mapping_needs_upload(self.mapping, upload_type):
                continue
            if upload_files:
                approval_file[f"{upload_type}_code"] = (
                    self.lark.upload_approval_file(image_path, upload_type)
                )
            else:
                approval_file[f"{upload_type}_code"] = (
                    f"DRY_RUN_{upload_type.upper()}_CODE"
                )

        context = {
            "invoice": invoice_context(
                invoice,
                self.mapping.get("expense_type_options"),
            ),
            "event": {
                "event_id": event.get("event_id"),
                "message_id": message_id,
                "chat_id": event.get("chat_id"),
                "sender_open_id": sender,
            },
            "approval_file": approval_file,
            "constants": self.mapping.get("constants", {}),
        }
        form = render_form(self.mapping, context)
        approval_uuid = str(
            uuid.uuid5(UUID_NAMESPACE, f"feishu-invoice:{message_id}")
        ).upper()
        payload = {
            "approval_code": self.approval_code,
            "open_id": sender,
            "form": json.dumps(form, ensure_ascii=False, separators=(",", ":")),
            "uuid": approval_uuid,
        }
        self.store.update(
            message_id,
            status="ready",
            approval_uuid=approval_uuid,
            approval_request_json=payload,
        )
        return payload

    def _safe_update_card(
        self,
        source_message_id: str,
        token: str,
        card: Mapping[str, Any],
    ) -> None:
        """尽力更新卡片；更新失败不覆盖审批的最终业务状态。"""

        if not token:
            return
        try:
            self.lark.update_card(token, card)
        except Exception as exc:
            LOGGER.exception("更新飞书确认卡片失败")
            self.store.update(
                source_message_id,
                reply_error=f"更新确认卡片失败：{str(exc)[:1800]}",
            )

    def process_event(self, event: Mapping[str, Any]) -> None:
        """处理单个飞书消息事件，并将全流程状态持久化。"""

        # 本服务只消费图片消息，文本及其他类型消息直接忽略。
        if event.get("message_type") != "image":
            return
        message_id = str(event.get("message_id") or "")
        if not message_id:
            LOGGER.warning("忽略缺少 message_id 的图片事件")
            return

        # begin 对 event_id 和 message_id 有唯一约束，确保事件重投时不会重复处理。
        if not self.store.begin(event):
            LOGGER.info("忽略重复事件 message_id=%s", message_id)
            return

        try:
            # 配置了发送者白名单时，只允许名单内用户触发自动报销流程。
            sender = str(event.get("sender_id") or "")
            if self.settings.allowed_senders and sender not in self.settings.allowed_senders:
                self.store.update(message_id, status="rejected_sender")
                self._safe_reply(message_id, "未授权该账号自动发起费用报销。", "sender")
                return

            # 从事件中解析 image_key，下载原图并记录本地路径与文件摘要。
            self.store.update(message_id, status="downloading")
            image_key = self.lark.resolve_image_key(event)
            image_path = self.lark.download_image(
                message_id, image_key, self.settings.images_dir
            )
            image_hash = file_sha256(image_path)
            self.store.update(
                message_id,
                status="recognizing",
                image_path=str(image_path),
                image_sha256=image_hash,
            )

            # 将原图交给 Codex 视觉模型，得到符合 JSON Schema 的结构化发票信息。
            invoice = self.vision.extract(image_path, message_id)
            fingerprint = invoice_fingerprint(invoice)
            self.store.update(
                message_id,
                status="recognized",
                invoice_json=invoice,
                invoice_fingerprint=fingerprint,
            )

            # 审批只接收本公司的购方抬头；明确告知提交者具体不匹配的字段。
            header_mismatches = buyer_header_mismatches(
                invoice,
                self.settings.required_buyer_name,
                self.settings.required_buyer_tax_id,
            )
            if header_mismatches:
                mismatch_reason = "；".join(header_mismatches)
                self.store.update(
                    message_id,
                    status="buyer_header_mismatch",
                    error=mismatch_reason,
                )
                self._safe_reply(
                    message_id,
                    "发票购方信息不符合要求，未提交审批：" + mismatch_reason,
                    "buyer-header",
                )
                return

            risk_reasons = invoice_risk_reasons(invoice)
            if risk_reasons:
                risk_reason = "；".join(risk_reasons)
                self.store.update(
                    message_id,
                    status="invoice_risk_rejected",
                    error=risk_reason,
                )
                self._safe_reply(
                    message_id,
                    "发票存在风险，未提交审批：" + risk_reason,
                    "invoice-risk",
                )
                return

            # 业务查重只针对已经成功提交的审批，避免同一张发票重复报销。
            duplicate = self.store.duplicate_instance(fingerprint, message_id)
            if duplicate:
                self.store.update(
                    message_id,
                    status="duplicate",
                    error=f"同一发票已提交：{duplicate}",
                )
                self._safe_reply(
                    message_id,
                    f"检测到该发票已经提交过，未重复报销。审批实例：{duplicate}",
                    "duplicate",
                )
                return

            # 非发票、低置信度、缺少必填字段或模型主动标记存疑时均不自动提交。
            required = self.mapping.get("required_invoice_fields", [])
            if not isinstance(required, list):
                raise ConfigurationError("required_invoice_fields 必须是数组")
            missing = missing_required_fields(invoice, required)
            review_reason = self._review_reason(invoice, missing)
            if review_reason:
                self.store.update(
                    message_id, status="needs_review", error=review_reason
                )
                self._safe_reply(
                    message_id,
                    "发票已识别，但暂未提交审批，需要人工复核：" + review_reason,
                    "review",
                )
                return

            # 先生成完整审批上下文，确保类别选项及所有模板字段都可用。
            preview_invoice = invoice_context(
                invoice,
                self.mapping.get("expense_type_options"),
            )
            card = build_invoice_confirmation_card(
                preview_invoice,
                message_id,
                dry_run=self.settings.dry_run,
            )
            self.store.update(
                message_id,
                status="sending_confirmation",
            )
            card_message_id = self.lark.send_card(
                sender,
                card,
                f"{message_id}-confirm-card",
            )
            self.store.update(
                message_id,
                status="pending_confirmation",
                card_message_id=card_message_id,
                error=None,
            )
        except Exception as exc:
            # 任一步骤失败都统一落库并通知用户，确保失败过程可追踪。
            LOGGER.exception("处理发票消息失败 message_id=%s", message_id)
            self.store.update(message_id, status="failed", error=str(exc)[:4000])
            self._safe_reply(
                message_id,
                "发票处理失败，未提交费用报销。原因：" + str(exc)[:800],
                "failed",
            )

    def process_card_action(self, event: Mapping[str, Any]) -> None:
        """处理确认卡片的提交或暂不提交按钮回调。"""

        if event.get("type") != "card.action.trigger":
            return
        try:
            raw_value = event.get("action_value")
            if isinstance(raw_value, str):
                action_value = json.loads(raw_value)
            elif isinstance(raw_value, Mapping):
                action_value = dict(raw_value)
            else:
                return
        except json.JSONDecodeError:
            LOGGER.warning("忽略 action_value 非法的卡片回调")
            return
        if not isinstance(action_value, dict):
            return

        action = str(action_value.get("action") or "")
        source_message_id = str(action_value.get("source_message_id") or "")
        card_message_id = str(event.get("message_id") or "")
        event_id = str(event.get("event_id") or "")
        operator_id = str(event.get("operator_id") or "")
        token = str(event.get("token") or "")
        if (
            action not in {"submit", "decline"}
            or not source_message_id
            or not card_message_id
            or not event_id
            or not operator_id
        ):
            LOGGER.warning("忽略字段不完整的卡片回调 event_id=%s", event_id)
            return

        record = self.store.get(source_message_id)
        if not record:
            LOGGER.warning("确认卡片没有对应的发票记录：%s", source_message_id)
            return
        if (
            str(record.get("card_message_id") or "") != card_message_id
            or str(record.get("sender_open_id") or "") != operator_id
        ):
            LOGGER.warning(
                "拒绝非原提交人的卡片操作 source=%s operator=%s",
                source_message_id,
                operator_id,
            )
            return
        if not self.store.claim_decision(
            source_message_id,
            card_message_id=card_message_id,
            event_id=event_id,
            operator_id=operator_id,
            action=action,
        ):
            LOGGER.info("忽略重复或已处理的卡片操作 event_id=%s", event_id)
            return

        try:
            invoice = json.loads(str(record["invoice_json"]))
            if not isinstance(invoice, dict):
                raise BotError("数据库中的发票识别结果不是 JSON 对象")

            if action == "decline":
                self.store.update(
                    source_message_id,
                    status="declined",
                    error="提交人选择暂不提交",
                )
                self._safe_update_card(
                    source_message_id,
                    token,
                    build_invoice_decision_card(invoice, status="declined"),
                )
                return

            duplicate = self.store.duplicate_instance(
                str(record.get("invoice_fingerprint") or ""),
                source_message_id,
            )
            if duplicate:
                self.store.update(
                    source_message_id,
                    status="duplicate",
                    instance_code=duplicate,
                    error=f"同一发票已提交：{duplicate}",
                )
                self._safe_update_card(
                    source_message_id,
                    token,
                    build_invoice_decision_card(
                        invoice,
                        status="duplicate",
                        instance_code=duplicate,
                    ),
                )
                return

            real_submit = self.settings.auto_submit and not self.settings.dry_run
            payload = self._build_approval_payload(
                record,
                invoice,
                upload_files=real_submit,
            )

            if not self.settings.auto_submit:
                final_status = "ready_for_review"
                self.store.update(
                    source_message_id,
                    status=final_status,
                    error="BOT_AUTO_SUBMIT=false",
                )
                instance_code = None
            elif self.settings.dry_run:
                final_status = "confirmed_dry_run"
                self.store.update(
                    source_message_id,
                    status=final_status,
                    error="BOT_DRY_RUN=true",
                )
                instance_code = None
            else:
                self.store.update(source_message_id, status="submitting")
                response = self.lark.create_approval(payload)
                instance_code = response.get("data", {}).get("instance_code")
                if not instance_code:
                    raise BotError("创建审批响应中缺少 data.instance_code")
                final_status = "submitted"
                self.store.update(
                    source_message_id,
                    status=final_status,
                    approval_response_json=response,
                    instance_code=str(instance_code),
                    error=None,
                )

            self._safe_update_card(
                source_message_id,
                token,
                build_invoice_decision_card(
                    invoice,
                    status=final_status,
                    instance_code=str(instance_code) if instance_code else None,
                ),
            )
        except Exception as exc:
            LOGGER.exception(
                "处理确认卡片失败 source_message_id=%s", source_message_id
            )
            self.store.update(
                source_message_id,
                status="failed",
                error=str(exc)[:4000],
            )
            record = self.store.get(source_message_id)
            invoice = {}
            if record and record.get("invoice_json"):
                try:
                    parsed = json.loads(str(record["invoice_json"]))
                    if isinstance(parsed, dict):
                        invoice = parsed
                except json.JSONDecodeError:
                    pass
            self._safe_update_card(
                source_message_id,
                token,
                build_invoice_decision_card(invoice, status="failed"),
            )
            self._safe_reply(
                source_message_id,
                "确认提交失败，未创建费用报销。原因：" + str(exc)[:800],
                "confirm-failed",
            )

    def run_forever(self) -> None:
        """持续消费发票图片消息和确认卡片操作。"""

        for event in self.lark.stream_invoice_events(
            ready_timeout=self.settings.lark_ready_timeout_seconds
        ):
            if event.get("type") == "card.action.trigger":
                self.process_card_action(event)
            else:
                self.process_event(event)
