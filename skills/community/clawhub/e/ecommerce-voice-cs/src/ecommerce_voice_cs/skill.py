from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import RefundRules, SessionContext, SkillResponse
from .rules import AfterSalesRuleEngine
from .voice import VoiceCloneService


class EcommerceVoiceCSSkill:
    TRIGGER_PHRASE = "我需要你现在当一个客服机器人"

    def __init__(
        self,
        *,
        voice_service: VoiceCloneService | None = None,
        rule_engine: AfterSalesRuleEngine | None = None,
    ) -> None:
        self.voice_service = voice_service or VoiceCloneService()
        self.rule_engine = rule_engine or AfterSalesRuleEngine()
        self.session = SessionContext()

    def upload_sample(self, file_path: str) -> str:
        voice_handle = self.voice_service.upload_sample(file_path)
        self.session.voice_handle = voice_handle
        return voice_handle

    def set_api_key(self, api_key: str) -> None:
        self.voice_service.set_api_key(api_key)

    def set_clone_api_url(self, clone_api_url: str) -> None:
        self.voice_service.set_clone_api_url(clone_api_url)

    def configure(
        self,
        *,
        refund_policy: str,
        unboxing_allowed: bool,
        shipping_fee_by: str,
        audio_output_path: str,
    ) -> None:
        self.session.refund_rules = RefundRules(
            refund_policy=refund_policy.strip(),
            unboxing_allowed=unboxing_allowed,
            shipping_fee_by=shipping_fee_by.strip(),
        )
        self.session.audio_output_path = Path(audio_output_path)

    def handle_message(self, user_input: str, **kwargs: Any) -> SkillResponse:
        text = user_input.strip()
        if not text:
            return SkillResponse(text="请输入用户咨询内容。")

        self._hydrate_runtime_configuration(kwargs)

        if self.TRIGGER_PHRASE in text:
            return self._enter_cs_mode()

        if not self.session.is_cs_mode:
            return SkillResponse(
                text="当前仍是常规对话模式。发送“我需要你现在当一个客服机器人”以切换到售后客服模式。"
            )

        missing = self._collect_missing_configuration()
        if missing:
            return SkillResponse(
                text=self._build_missing_config_prompt(missing),
                metadata={
                    "missing_configuration": missing,
                    "api_docs_url": self.voice_service.API_DOCS_URL,
                },
            )

        reply_text = self.rule_engine.generate_response(text, self.session.refund_rules)
        audio_file = self.voice_service.synthesize_to_file(
            text=reply_text,
            voice_handle=self.session.voice_handle or "",
            output_dir=self.session.audio_output_path or ".",
            file_ext=kwargs.get("audio_format", ".mp3"),
            sample_rate=int(kwargs.get("sample_rate", 32000)),
            bitrate=int(kwargs.get("bitrate", 128000)),
            channel=int(kwargs.get("channel", 1)),
            speed=float(kwargs.get("speed", 1)),
            volume=float(kwargs.get("volume", 1)),
            pitch=float(kwargs.get("pitch", 0)),
        )
        return SkillResponse(
            text=reply_text,
            audio_file=audio_file,
            metadata={
                "is_cs_mode": self.session.is_cs_mode,
                "voice_handle": self.session.voice_handle,
            },
        )

    def _hydrate_runtime_configuration(self, payload: dict[str, Any]) -> None:
        api_key = payload.get("api_key")
        if api_key:
            self.voice_service.set_api_key(str(api_key))

        clone_api_url = payload.get("clone_api_url")
        if clone_api_url:
            self.voice_service.set_clone_api_url(str(clone_api_url))

        if payload.get("voice_handle"):
            self.session.voice_handle = str(payload["voice_handle"])

        output_path = payload.get("audio_output_path")
        if output_path:
            self.session.audio_output_path = Path(str(output_path))

        refund_policy = payload.get("refund_policy")
        shipping_fee_by = payload.get("shipping_fee_by")
        unboxing_allowed = payload.get("unboxing_allowed")

        if any(value is not None for value in (refund_policy, shipping_fee_by, unboxing_allowed)):
            self.session.refund_rules = RefundRules(
                refund_policy=str(refund_policy or self.session.refund_rules.refund_policy).strip(),
                unboxing_allowed=(
                    bool(unboxing_allowed)
                    if unboxing_allowed is not None
                    else self.session.refund_rules.unboxing_allowed
                ),
                shipping_fee_by=str(
                    shipping_fee_by or self.session.refund_rules.shipping_fee_by
                ).strip(),
            )

    def _enter_cs_mode(self) -> SkillResponse:
        self.session.is_cs_mode = True
        missing = self._collect_missing_configuration()
        if missing:
            return SkillResponse(
                text=(
                    "已切换到电商售后客服模式。"
                    f"{self._build_missing_config_prompt(missing)}"
                ),
                state_changed=True,
                metadata={
                    "missing_configuration": missing,
                    "api_docs_url": self.voice_service.API_DOCS_URL,
                },
            )

        return SkillResponse(
            text=(
                "已切换到电商售后客服模式。"
                f"当前规则：{self.session.refund_rules.summary()}"
                f"音频将输出到：{self.session.audio_output_path}"
            ),
            state_changed=True,
        )

    def _collect_missing_configuration(self) -> list[str]:
        missing = self.session.missing_configuration()
        if not self.voice_service.has_api_key():
            missing.append("api_key")
        return missing

    @staticmethod
    def _build_missing_config_prompt(missing: list[str]) -> str:
        labels = {
            "voice_handle": "请先上传音频样本生成 voice_handle。",
            "refund_rules": "请补充 refund_policy、unboxing_allowed、shipping_fee_by。",
            "audio_output_path": "请补充 audio_output_path 作为音频输出目录。",
            "api_key": (
                "未检测到环境变量 SENSEAUDIO_API_KEY，请提供 SenseAudio API Key。"
                "文档：https://senseaudio.cn/docs/api-key"
            ),
        }
        return "".join(labels[item] for item in missing if item in labels)
