"""AI 改写模块 - 将原视频稿变成「像自己说的」"""
import asyncio
import logging
from pathlib import Path
from typing import Optional
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """你是"AI二次创作"助手。用户给你一段抖音/短视频的口播文案，你需要：

## 核心任务
将原文案改写为"像同一个人（用户）自己说的话"，而非 AI 生成的文本。

## 改写原则
1. **口语化** - 保留或增强口语感，像朋友聊天，不是播音腔
2. **自然节奏** - 短句为主，有停顿感，适合口播
3. **去除"短视频DNA"** - 去掉"家人们""谁懂啊""绝绝子""咱就是说""一整个XXX住""上链接""扣1""点关注"等流量话术
4. **保留核心信息** - 观点、论据、故事主线不变
5. **调整语序** - 中文口语习惯（主谓宾自然，不要长定语句）
6. **加入个人风格标志** - 如果用户提供了风格提示，按要求调整
7. **分段** - 每段不超过 3 句话，适合 TTS 合成

## 输出格式
只输出改写后的文本，不需要解释、不需要标记、不需要"改写版："前缀。

## 例子

原文："家人们谁懂啊！这个美妆蛋一整个绝绝子住了！上脸巨服帖完全不卡粉，咱就是说闭眼冲就完事了！"

改写后："试一下这个美妆蛋。上脸特别服帖，完全不卡粉。而且价格也不贵，值得试试。"

原文："打工人们，今天给大家分享三个职场干货，每一个都是血泪教训换来的，建议先点赞收藏！"

改写后："分享三个职场经验，都是我自己踩过的坑。第一个，不要在情绪激动的时候做决定。第二个，要学会说'不'。第三个，定期复盘很重要。"
"""


class Rewriter:
    """AI 文本改写"""

    def __init__(self):
        self.client = None

    def _get_client(self) -> AsyncOpenAI:
        if self.client is None:
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                # 无 API key 时使用模拟改写（演示/开发用）
                return None
            kwargs = {"api_key": api_key}
            if settings.OPENAI_BASE_URL:
                kwargs["base_url"] = settings.OPENAI_BASE_URL
            self.client = AsyncOpenAI(**kwargs)
        return self.client

    async def _mock_rewrite(self, text: str, custom_prompt: str = "") -> str:
        """无 API key 时的模拟改写"""
        import re

        replacements = [
            (r"家人们|朋友们|姐妹们|兄弟们|老铁们", "大家好"),
            (r"谁懂啊|谁懂|懂的都懂", ""),
            (r"绝绝子|yyds|YYDS|yyds", "非常好"),
            (r"咱就是说|咱就说|就是说", ""),
            (r"一整个[^，。！？]*住", "非常好"),
            (r"闭眼冲|闭眼入|直接冲|冲冲冲", "值得试试"),
            (r"上链接|链接已放|购物车", ""),
            (r"扣\d|扣一波|扣个\d", ""),
            (r"建议[点赞收藏关注]+", ""),
            (r"点关注不迷路", ""),
        ]

        result = text
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)

        # 分段
        sentences = re.split(r'[。！？\n]', result)
        paragraphs = []
        chunk = []
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            chunk.append(s)
            if len(chunk) >= 3:
                paragraphs.append("。".join(chunk) + "。")
                chunk = []
        if chunk:
            paragraphs.append("。".join(chunk) + "。")

        return "\n\n".join(paragraphs)

    async def rewrite(self, text: str, task_id: str, custom_prompt: str = "") -> str:
        """
        改写文本
        返回改写后的稿子
        """
        output_path = settings.REWRITE_DIR / f"{task_id}.txt"
        if output_path.exists():
            return output_path.read_text(encoding="utf-8")

        client = self._get_client()
        if client is None:
            rewritten = await self._mock_rewrite(text, custom_prompt)
        else:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"请改写以下口播文案：\n\n{text}"},
            ]
            if custom_prompt:
                messages.insert(1, {
                    "role": "user",
                    "content": f"附加风格要求：{custom_prompt}"
                })

            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
            rewritten = response.choices[0].message.content or ""

        output_path.write_text(rewritten, encoding="utf-8")
        logger.info(f"Rewritten: {len(rewritten)} chars")
        return rewritten
