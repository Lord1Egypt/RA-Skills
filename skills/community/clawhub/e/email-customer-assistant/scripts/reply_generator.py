#!/usr/bin/env python3
"""
reply_generator.py — AI回复生成模块
基于邮件内容生成多语言回复建议
用户确认后再发送，安全可控
"""

import json
import time
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReplyGenerator:
    """AI回复生成器"""

    # 支持的语言
    SUPPORTED_LANGUAGES = {
        "zh": "中文",
        "en": "英文",
        "ja": "日文",
        "ko": "韩文",
        "zh-tw": "繁体中文",
        "es": "西班牙文",
        "fr": "法文",
        "de": "德文"
    }

    def __init__(self, ai_config: Dict[str, Any]):
        """
        初始化回复生成器

        Args:
            ai_config: AI配置字典
        """
        self.ai_config = ai_config
        self.provider = ai_config.get("provider", "openai")
        self.api_key = ai_config.get("api_key", "")
        self.model = ai_config.get("model", "gpt-4o-mini")
        self.base_url = ai_config.get("base_url", "https://api.openai.com/v1")
        self.max_tokens = ai_config.get("max_tokens", 1000)
        self.temperature = ai_config.get("temperature", 0.7)
        self.timeout = ai_config.get("timeout", 30)

    # ─────────────────────────────────────────────────────────────
    # 核心生成方法
    # ─────────────────────────────────────────────────────────────

    def _call_ai_api(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        通用AI API调用

        Args:
            messages: 消息列表
            model: 模型名称（可选）
            **kwargs: 其他参数

        Returns:
            AI响应文本
        """
        import openai

        # 初始化客户端
        client_kwargs = {
            "api_key": self.api_key,
            "timeout": self.timeout
        }
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        client = openai.OpenAI(**client_kwargs)

        response = client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature)
        )

        return response.choices[0].message.content.strip()

    def _build_system_prompt(self, language: str = "zh") -> str:
        """构建系统提示词"""
        lang_name = self.SUPPORTED_LANGUAGES.get(language, "中文")

        return f"""你是一位专业、友善的客服代表，擅长用{lang_name}撰写邮件回复。

回复要求：
1. 语言风格专业、礼貌、简洁
2. 针对性回复客户问题，不废话
3. 如果需要进一步信息，主动询问
4. 如无法解决问题，说明会转交相关部门
5. 适当使用表情符号增加亲和力（但不要过度）
6. 回复长度适中，一般不超过200字
7. 用{lang_name}撰写

请根据以下邮件内容，生成一封专业的回复邮件。"""

    def generate_reply(
        self,
        email_data: Dict[str, Any],
        language: str = "zh",
        tone: str = "professional",
        custom_instruction: Optional[str] = None
    ) -> str:
        """
        生成回复建议

        Args:
            email_data: 邮件数据字典，至少包含 sender, subject, body
            language: 回复语言代码（zh/en/ja/ko等）
            tone: 语气风格（professional/friendly/formal/casual）
            custom_instruction: 自定义指令（可选）

        Returns:
            生成的回复内容
        """
        sender = email_data.get("sender", "")
        subject = email_data.get("subject", "")
        body = email_data.get("body", "")
        category = email_data.get("category", "")

        # 构建用户提示词
        user_prompt_lines = [
            f"**原邮件发件人：** {sender}",
            f"**原邮件主题：** {subject}",
        ]

        if category:
            user_prompt_lines.append(f"**邮件分类：** {category}")

        user_prompt_lines.extend([
            f"**原邮件内容：**\n{body[:2000]}",  # 限制body长度
            ""
        ])

        if custom_instruction:
            user_prompt_lines.append(f"**自定义要求：** {custom_instruction}")

        if tone != "professional":
            user_prompt_lines.append(f"**语气风格：** {tone}")

        user_prompt = "\n".join(user_prompt_lines)

        messages = [
            {"role": "system", "content": self._build_system_prompt(language)},
            {"role": "user", "content": user_prompt}
        ]

        try:
            reply = self._call_ai_api(messages)
            return reply
        except Exception as e:
            print(f"[ReplyGenerator] ❌ 生成回复失败: {e}")
            return f"【自动回复】感谢您的来信。我们已收到您的邮件（主题：{subject}），将在1-2个工作日内给予回复。"

    def generate_reply_multi_language(
        self,
        email_data: Dict[str, Any],
        languages: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        生成多语言回复建议

        Args:
            email_data: 邮件数据
            languages: 语言列表（默认 ['zh', 'en']）

        Returns:
            {语言代码: 回复内容} 的字典
        """
        if languages is None:
            languages = ["zh", "en"]

        results = {}
        for lang in languages:
            if lang not in self.SUPPORTED_LANGUAGES:
                print(f"[ReplyGenerator] ⚠️ 不支持的语言: {lang}，跳过")
                continue
            try:
                reply = self.generate_reply(email_data, language=lang)
                results[lang] = reply
                print(f"[ReplyGenerator] ✅ {self.SUPPORTED_LANGUAGES[lang]}回复生成成功")
            except Exception as e:
                print(f"[ReplyGenerator] ❌ {self.SUPPORTED_LANGUAGES[lang]}回复生成失败: {e}")
                results[lang] = ""

        return results

    # ─────────────────────────────────────────────────────────────
    # 回复确认与发送
    # ─────────────────────────────────────────────────────────────

    def confirm_and_preview(
        self,
        email_data: Dict[str, Any],
        reply: str,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """
        生成回复预览（供用户确认）

        Args:
            email_data: 原邮件数据
            reply: 生成的回复
            language: 语言

        Returns:
            预览信息字典
        """
        lang_name = self.SUPPORTED_LANGUAGES.get(language, "中文")

        preview = {
            "original_email": {
                "sender": email_data.get("sender", ""),
                "subject": email_data.get("subject", ""),
                "date": email_data.get("date", ""),
                "category": email_data.get("category", "")
            },
            "reply": {
                "content": reply,
                "language": lang_name,
                "language_code": language,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "confirm_url": "mailto:{}?subject={}&body={}".format(
                email_data.get("sender", ""),
                "Re: " + (email_data.get("subject", "") or ""),
                reply.replace("\n", "%0A").replace(" ", "%20")
            ),
            "status": "pending_confirmation"
        }
        return preview

    def apply_modification(
        self,
        original_reply: str,
        modification_instruction: str
    ) -> str:
        """
        根据用户修改指令调整回复

        Args:
            original_reply: 原始回复
            modification_instruction: 修改指令

        Returns:
            修改后的回复
        """
        messages = [
            {
                "role": "system",
                "content": "你是一个文本编辑器，根据用户的修改指令调整回复内容。只返回修改后的内容，不要额外解释。"
            },
            {
                "role": "user",
                "content": f"**原始回复：**\n{original_reply}\n\n**修改指令：**\n{modification_instruction}"
            }
        ]

        try:
            modified = self._call_ai_api(messages)
            return modified
        except Exception as e:
            print(f"[ReplyGenerator] ❌ 修改回复失败: {e}")
            return original_reply

    # ─────────────────────────────────────────────────────────────
    # 快捷方法
    # ─────────────────────────────────────────────────────────────

    def quick_reply(
        self,
        email_data: Dict[str, Any],
        template: str = "acknowledge"
    ) -> str:
        """
        使用预设模板快速回复

        Args:
            email_data: 邮件数据
            template: 模板名称

        Returns:
            模板回复内容
        """
        templates = {
            "acknowledge": {
                "zh": f"感谢您的来信。我们已收到您的邮件（主题：{email_data.get('subject', '')}），"
                      f"将在1-2个工作日内给予回复。\n\n此致\n客服团队",
                "en": f"Thank you for your email regarding '{email_data.get('subject', '')}'. "
                      f"We have received your message and will respond within 1-2 business days.\n\nBest regards,\nCustomer Support"
            },
            "received": {
                "zh": f"您好，感谢您的来信。我们已收到您的邮件，将尽快处理。\n\n如有任何问题，请随时联系我们。\n\n此致\n客服团队",
                "en": f"Hello, thank you for reaching out. We have received your email and will handle it promptly.\n\n"
                     f"Please feel free to contact us if you have any questions.\n\nBest regards,\nCustomer Support"
            },
            "investigating": {
                "zh": f"感谢您的来信。我们已了解您的情况，目前正在处理中，"
                      f"预计将在3个工作日内给您回复。\n\n此致\n客服团队",
                "en": f"Thank you for bringing this to our attention. We are currently investigating your issue "
                      f"and expect to provide an update within 3 business days.\n\nBest regards,\nCustomer Support"
            }
        }

        lang = email_data.get("language", "zh")
        template_dict = templates.get(template, templates["acknowledge"])
        return template_dict.get(lang, template_dict.get("zh", ""))


# ─────────────────────────────────────────────────────────────────
# 独立运行测试
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import yaml

    print("=" * 60)
    print("回复生成模块测试")
    print("=" * 60)

    # 尝试加载配置
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        ai_cfg = config.get("ai", {})
    except FileNotFoundError:
        print("⚠️  config.yaml 未找到，使用空配置测试")
        ai_cfg = {}

    generator = ReplyGenerator(ai_cfg)

    # 测试邮件数据
    test_email = {
        "sender": "john.doe@company.com",
        "subject": "Product inquiry about your enterprise plan",
        "body": "Hello, I am interested in your enterprise plan. "
                "Could you please send me the pricing details and feature comparison? "
                "We have about 500 employees and need multi-language support. "
                "Looking forward to your response.",
        "category": "咨询",
        "language": "en"
    }

    # 测试单语言回复生成
    print("\n📝 测试单语言回复生成（英文）...")
    reply = generator.generate_reply(test_email, language="en")
    print(f"\n✅ 生成的回复：\n{reply}")

    # 测试多语言回复生成
    print("\n\n📝 测试多语言回复生成（中/英/日）...")
    multi_replies = generator.generate_reply_multi_language(
        test_email,
        languages=["zh", "en", "ja"]
    )
    for lang, reply_text in multi_replies.items():
        print(f"\n🌐 [{lang}] 回复：\n{reply_text}")

    # 测试回复预览
    print("\n\n📝 测试回复预览...")
    preview = generator.confirm_and_preview(test_email, reply, language="en")
    print(f"\n📋 预览信息：")
    print(f"  原始邮件: {preview['original_email']['sender']}")
    print(f"  回复语言: {preview['reply']['language']}")
    print(f"  生成时间: {preview['reply']['generated_at']}")
    print(f"  状态: {preview['status']}")

    print("\n✅ 测试完成")
