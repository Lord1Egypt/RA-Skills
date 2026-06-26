#!/usr/bin/env python3
"""
AI 题目生成器模块
调用 LLM API 生成新的脑筋急转弯题目
"""

import json
import os
import random
import time
from typing import Optional, Dict, Any
from pathlib import Path

from session import Question


# 生成 Prompt 模板
GENERATE_PROMPT = {
    "zh": """请生成一道有趣的脑筋急转弯题目，以 JSON 格式返回，不要包含其他内容。

要求：
1. 题目要有趣、有创意
2. 答案要简洁（通常是1-3个字）
3. 提示要能帮助思考但不要太明显
4. 难度适中

JSON 格式：
{"question": "题目内容", "answer": "答案", "hint": "提示", "explain": "解释"}

现在请生成一道中文脑筋急转弯：""",

    "en": """Generate a fun brain teaser in JSON format. Return only the JSON, no other content.

Requirements:
1. Creative and interesting question
2. Short answer (1-3 words)
3. Helpful but not too obvious hint
4. Medium difficulty

JSON format:
{"question": "...", "answer": "...", "hint": "...", "explain": "..."}

Now generate an English brain teaser:""",

    "ja": """なぞなぞを一つ作ってください。JSONフォーマットのみで返してください。

要件：
1. 面白くて創造的な問題
2. 答えは短く（1-3文字）
3. ヒントは役に立つが、あまり明白すぎない
4. 難易度は中程度

JSONフォーマット：
{"question": "...", "answer": "...", "hint": "...", "explain": "..."}

なぞなぞを生成してください："""
}


class AIQuestionGenerator:
    """AI 题目生成器"""

    def __init__(self):
        self.config = self._load_config()
        self.client = None

        if self.config:
            self._init_client()

    def _load_config(self) -> Optional[Dict[str, str]]:
        """
        加载 API 配置

        优先级：
        1. 环境变量 BRAIN_TEASER_API_KEY
        2. Claude Code 配置 ~/.claude/settings.json
        3. OpenClaw 配置 ~/.openclaw/openclaw.json

        Returns:
            API 配置字典或 None
        """
        # 1. 环境变量优先
        if os.environ.get('BRAIN_TEASER_API_KEY'):
            return {
                'api_key': os.environ['BRAIN_TEASER_API_KEY'],
                'base_url': os.environ.get('BRAIN_TEASER_API_BASE'),
                'model': os.environ.get('BRAIN_TEASER_MODEL', 'glm-4-flash')
            }

        # 2. 读取 Claude Code 配置（智谱 AI）
        claude_settings_path = Path.home() / ".claude" / "settings.json"
        if claude_settings_path.exists():
            try:
                with open(claude_settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                env = settings.get('env', {})
                if env.get('ANTHROPIC_AUTH_TOKEN'):
                    return {
                        'api_key': env['ANTHROPIC_AUTH_TOKEN'],
                        'base_url': env.get('ANTHROPIC_BASE_URL'),
                        'model': env.get('ANTHROPIC_MODEL', 'glm-4-flash')
                    }
            except (json.JSONDecodeError, KeyError):
                pass

        # 3. 读取 OpenClaw 配置
        openclaw_path = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_path.exists():
            try:
                with open(openclaw_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 检查 gateway 配置
                gateway = config.get('gateway', {})
                if gateway.get('port'):
                    return {
                        'api_key': 'local',
                        'base_url': f"http://localhost:{gateway['port']}",
                        'model': 'glm-4-flash'
                    }
            except (json.JSONDecodeError, KeyError):
                pass

        # 无配置，禁用 AI 生成
        return None

    def _init_client(self):
        """初始化 API 客户端"""
        try:
            # 尝试使用 openai 库（兼容大多数 API）
            from openai import OpenAI

            self.client = OpenAI(
                api_key=self.config['api_key'],
                base_url=self.config['base_url']
            )
        except ImportError:
            # openai 库未安装
            self.client = None

    def is_available(self) -> bool:
        """检查 AI 生成器是否可用"""
        return self.config is not None and self.client is not None

    def generate_question(self, language: str) -> Optional[Question]:
        """
        生成新题目

        Args:
            language: 语言代码

        Returns:
            生成的题目或 None
        """
        if not self.is_available():
            return None

        prompt = GENERATE_PROMPT.get(language, GENERATE_PROMPT["en"])

        try:
            response = self.client.chat.completions.create(
                model=self.config['model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,  # 更高的温度增加创意
                max_tokens=500
            )

            content = response.choices[0].message.content.strip()

            # 尝试解析 JSON
            # 处理可能的 markdown 代码块
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

            data = json.loads(content)

            # 生成唯一 ID（AI 生成的题目 ID 从 10000 开始）
            question_id = int(time.time() * 1000) % 10000000 + 10000

            return Question(
                id=question_id,
                question=data.get("question", ""),
                answer=data.get("answer", ""),
                hint=data.get("hint", ""),
                explain=data.get("explain", ""),
                difficulty=2,
                source="ai_generated"
            )

        except Exception as e:
            print(f"AI 生成失败: {e}")
            return None

    def should_generate_new(self, unused_count: int, threshold: int = 5) -> bool:
        """
        判断是否需要生成新题

        Args:
            unused_count: 未使用题目数量
            threshold: 阈值

        Returns:
            是否需要生成
        """
        return self.is_available() and unused_count < threshold


def generate_question_simple(language: str) -> Optional[Question]:
    """
    简单的题目生成函数（不依赖类实例）

    Args:
        language: 语言代码

    Returns:
        生成的题目或 None
    """
    generator = AIQuestionGenerator()
    return generator.generate_question(language)


if __name__ == "__main__":
    # 测试 AI 生成器
    print("=== AI 生成器测试 ===")

    generator = AIQuestionGenerator()

    if generator.is_available():
        print(f"API 配置: {generator.config}")
        print(f"可用模型: {generator.config.get('model')}")

        # 尝试生成
        print("\n正在生成中文题目...")
        question = generator.generate_question("zh")
        if question:
            print(f"题目: {question.question}")
            print(f"答案: {question.answer}")
            print(f"提示: {question.hint}")
            print(f"解释: {question.explain}")
        else:
            print("生成失败")
    else:
        print("AI 生成器不可用")
        print("请设置环境变量 BRAIN_TEASER_API_KEY 或配置 ~/.claude/settings.json")
