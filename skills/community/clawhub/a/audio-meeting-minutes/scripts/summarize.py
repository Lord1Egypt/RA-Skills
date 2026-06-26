# -*- coding: utf-8 -*-
"""熠小听 · AI 总结辅助模块（供 WorkBuddy Agent 参考）

本文件提供总结 prompt 模板和输出格式规范。
AI 总结由 WorkBuddy 内置 AI 完成，无需外部 API Key。
"""
import json

def build_summary_prompt(text, max_chars=14000):
    """生成总结 prompt，供 Agent 或外部 AI 使用"""
    return f"""你是一名资深的企业会议记录专家，擅长从口语化会议录音中提炼出专业、精炼的书面会议纪要。

【核心要求】
1. 你的工作是「提炼」而非「摘抄」——不要复制原文，用书面语言重新表述
2. 区分「讨论过程」和「最终结论」，只记录结论、决策、行动项
3. 口语化表达转化为规范的书面语
4. 演示/分享性质内容重点提炼「核心观点」和「参考价值」
5. 行动项必须具体可执行，格式：动词+内容
6. 标题精准概括核心议题，15字以内

请严格按以下JSON格式输出（只输出JSON）：
{{
  "meeting_title": "精准概括核心议题（15字以内）",
  "meeting_type": "技术分享/项目决策/工作汇报/头脑风暴/复盘总结",
  "meeting_summary": "3-4句书面语言概括背景、核心议题和主要结论",
  "key_conclusions": ["重要结论（完整书面句子）"],
  "decisions": [{{"content": "决策内容", "rationale": "决策依据"}}],
  "action_items": [{{"task": "具体行动(动词开头)", "owner": "负责人", "deadline": "截止时间", "priority": "高/中/低"}}],
  "participants": ["参会人或角色"],
  "agenda_items": [{{"title": "议题名称", "key_points": ["核心观点"], "outcome": "最终结论"}}],
  "risks_and_concerns": ["风险或待确认事项"],
  "next_steps": ["具体可执行的下一步"],
  "follow_up_required": ["需要跟进的事项"]
}}

会议记录（{len(text)}字）：
{text[:max_chars]}"""


def parse_json_response(content):
    """尝试从 AI 回复中提取 JSON"""
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
    raise ValueError("无法解析 JSON")
