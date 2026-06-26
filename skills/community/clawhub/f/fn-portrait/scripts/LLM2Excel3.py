#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM2Excel_合并版.py - LLM语义分析合并版
同时分析"经营情况的讨论与分析"和"报告期内获得的研发成果"
输出到同一个Excel文件的不同sheet

使用方法：
    python LLM2Excel_合并版.py <股票代码> <公司名称> <经营情况文本路径> <研发成果文本路径> [输出目录] [模型名称]

示例：
    python LLM2Excel_合并版.py 688049 炬芯科技 \
        "经营情况.txt" \
        "研发成果.txt" \
        "LLM测试输出"
"""

import requests
import pandas as pd
import json
import re
import sys
import os
from datetime import datetime


BUSINESS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "业务板块": {"type": "string"},
            "战略目标": {"type": "string"},
            "现状描述": {"type": "string"},
            "关键措施": {"type": "string"}
        },
        "required": ["业务板块", "战略目标", "现状描述", "关键措施"],
        "additionalProperties": False
    }
}

RD_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "技术/产品类别": {"type": "string"},
            "具体成果": {"type": "string"},
            "性能指标": {"type": "string"},
            "应用前景": {"type": "string"},
            "进展状态": {"type": "string"}
        },
        "required": ["技术/产品类别", "具体成果", "性能指标", "应用前景", "进展状态"],
        "additionalProperties": False
    }
}

COMPETITIVENESS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "竞争维度": {"type": "string"},
            "核心优势": {"type": "string"},
            "具体表现": {"type": "string"},
            "与同行对比": {"type": "string"}
        },
        "required": ["竞争维度", "核心优势", "具体表现", "与同行对比"],
        "additionalProperties": False
    }
}


class LLMCombinedAnalyzer:
    """LLM合并分析器"""

    def __init__(self, model="gemma3:1b", fallback_models=None,
                 ollama_url="http://localhost:11434",
                 provider="ollama", api_key=None):
        self.model = model
        self.fallback_models = fallback_models or ["deepseek-r1:1.5b", "qwen3:0.6b"]
        self.provider = provider.lower()
        # 支持 Moonshot 和 DeepSeek
        self.moonshot_key = api_key or os.environ.get("KIMI_API_KEY", "")
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")

        if self.provider == "moonshot":
            self.api_endpoint = "https://api.moonshot.cn/v1/chat/completions"
            self.api_key = self.moonshot_key
        elif self.provider == "deepseek":
            self.api_endpoint = "https://api.deepseek.com/v1/chat/completions"
            self.api_key = self.deepseek_key
        else:
            self.ollama_url = ollama_url
            self.api_endpoint = f"{ollama_url}/api/chat"

    def read_text_file(self, file_path: str) -> str:
        """读取文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return ""

    def clean_and_fix_json(self, json_str: str) -> str:
        """清理和修复JSON字符串"""
        if not json_str:
            return None

        json_str = json_str.strip()

        # 移除 markdown 代码块包裹
        json_str = re.sub(r'^\s*```(?:json)?\s*', '', json_str, flags=re.IGNORECASE)
        json_str = re.sub(r'\s*```\s*$', '', json_str)

        # 移除所有换行符
        json_str = json_str.replace('\n', ' ').replace('\r', ' ')

        # 移除控制字符
        json_str = ''.join(char for char in json_str if ord(char) >= 32 or char in '\t')

        # 移除截断标记
        json_str = re.sub(r'\.\.\.\s*$', '', json_str)
        json_str = re.sub(r'…\s*$', '', json_str)

        # 修复中文引号
        json_str = (
            json_str.replace('"', '"')
            .replace('"', '"')
            .replace(''', "'")
            .replace(''', "'")
        )
        
# 修复对象内部字段之间缺少逗号的情况（在移除换行符之前处理）
        # 匹配: "key": "value"[空白/换行]"key2":  → 补逗号
        json_str = re.sub(r'"\s*:\s*"([^"]*)"\s+(?=")', r'": "\1", ', json_str)
        json_str = re.sub(r'"\s*:\s*([\d\.]+)\s+(?=")', r'": \1, ', json_str)
        json_str = re.sub(r'"\s*:\s*([a-zA-Z]+)\s+(?=")', r'": \1, ', json_str)

        # 移除所有换行符
        json_str = json_str.replace('\n', ' ').replace('\r', ' ')

        # 去掉末尾逗号，先避免补括号后变成 ,] 或 ,}
        json_str = re.sub(r',\s*$', '', json_str)

        # 反复清理尾随逗号
        prev = None
        while prev != json_str:
            prev = json_str
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            json_str = re.sub(r',\s*$', '', json_str)

        # 确保JSON完整性
        brace_count = json_str.count('{') - json_str.count('}')
        bracket_count = json_str.count('[') - json_str.count(']')

        if brace_count > 0:
            json_str += '}' * brace_count
        if bracket_count > 0:
            json_str += ']' * bracket_count

        # 补全后再清理一次尾随逗号
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
        json_str = re.sub(r',\s*$', '', json_str)

        return json_str

    def _extract_complete_json_objects(self, text: str) -> list:
        """从任意文本中提取所有完整闭合的JSON对象"""
        if not text:
            return []

        objs = []
        start = -1
        depth = 0
        in_string = False
        escaped = False

        for i, char in enumerate(text):
            if in_string:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
                continue

            if char == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif char == '}' and depth > 0:
                depth -= 1
                if depth == 0 and start != -1:
                    obj_str = text[start:i + 1]
                    for candidate in (obj_str, self.clean_and_fix_json(obj_str)):
                        if not candidate:
                            continue
                        try:
                            obj = json.loads(candidate)
                            if isinstance(obj, dict):
                                objs.append(obj)
                                break
                        except Exception:
                            continue
                    start = -1

        return objs

    def _get_truncation_reasons(self, text: str, raw_result: dict = None) -> list:
        """判断输出是否可能被截断，并返回原因"""
        reasons = []
        stripped = (text or "").rstrip()

        if not stripped:
            return reasons

        done_reason = None
        if isinstance(raw_result, dict):
            done_reason = raw_result.get("done_reason")
            if done_reason is None and isinstance(raw_result.get("message"), dict):
                done_reason = raw_result["message"].get("done_reason")

        if done_reason == "length":
            reasons.append("done_reason=length")

        if '[' in stripped and stripped.count('[') > stripped.count(']'):
            reasons.append("缺少 ]")
        if '{' in stripped and stripped.count('{') > stripped.count('}'):
            reasons.append("缺少 }")
        if re.search(r',\s*$', stripped):
            reasons.append("末尾逗号")
        if stripped.endswith("...") or stripped.endswith("…"):
            reasons.append("省略号结尾")

        return reasons

    def extract_json_from_text(self, text: str) -> list:
        """从文本中提取JSON数组"""
        if not text:
            return None

        def _try_parse(candidate: str):
            cleaned = self.clean_and_fix_json(candidate)
            if not cleaned:
                return None
            try:
                data = json.loads(cleaned)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    return [data]
            except Exception:
                return None
            return None

        text = text.strip()

        # 策略1：先尝试找完整闭合数组
        start = text.find('[')
        if start != -1:
            bracket_count = 0
            end = -1
            in_string = False
            escaped = False

            for i, char in enumerate(text[start:], start):
                if in_string:
                    if escaped:
                        escaped = False
                    elif char == '\\':
                        escaped = True
                    elif char == '"':
                        in_string = False
                    continue

                if char == '"':
                    in_string = True
                    continue

                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end = i
                        break

            if end != -1:
                data = _try_parse(text[start:end + 1])
                if isinstance(data, list) and len(data) > 0:
                    return data

            # 策略2：数组不完整时，从 [ 到末尾做修复
            data = _try_parse(text[start:])
            if isinstance(data, list) and len(data) > 0:
                return data

        # 补充尝试：直接解析整个文本
        data = _try_parse(text)
        if isinstance(data, list) and len(data) > 0:
            return data

        # 策略3：对象级恢复（丢弃最后一个不完整对象）
        recovered_objs = self._extract_complete_json_objects(text)
        if recovered_objs:
            return recovered_objs

        return None

    def analyze_business(self, text: str, stock_code: str, company_name: str) -> dict:
        """分析经营情况"""
        print(f"\n[{stock_code}] 正在分析经营情况...")

        prompt = f"""
    你是一个专门做上市公司年报信息抽取的助手。
    你的任务是从"经营情况讨论与分析"中，提取公司各业务板块或战略主题的关键信息。

    请严格遵守以下要求：

    【输出要求】
    1. 只能输出一个 JSON 数组，不要输出任何解释、前后缀、标题、markdown 代码块。
    2. JSON 数组中的每个对象必须且只能包含以下 4 个字段：
    - "业务板块"
    - "战略目标"
    - "现状描述"
    - "关键措施"
    3. 必须使用双引号，保证 JSON 格式可被 json.loads 直接解析。
    4. 如果某字段在原文中没有明确表述，可做"贴近原文的简要归纳"；若完全无法判断，填空字符串 ""。
    5. 不要编造原文没有的信息，不要加入财务推测、投资建议、评价性语言。
    6. 不要重复生成相同的内容

    【抽取口径】
    1. 优先抽取"明确业务板块"，例如：轨道交通、新能源汽车、半导体、工业板块、海洋板块等。
    2. 如果全文没有严格的业务板块划分，但存在清晰的经营战略主题，也允许将其作为"业务板块"抽取，
    例如：市场布局、科技创新能力提升、产业布局优化、治理能力建设、风险合规等。
    3. "战略目标"强调未来导向、发展方向、要实现的重点目标。
    4. "现状描述"强调当前成果、市场地位、订单/交付/项目进展、经营表现等。
    5. "关键措施"强调公司采取的行动路径、抓手、工程、平台建设、产品推进、布局动作等。
    6. 遇到大段行业背景时，只保留与公司自身经营直接相关的部分。
    7. 相近内容合并，避免重复拆分得过细。

    【示例1】
    输入文本：
    （一）轨道交通业务聚力突破
    公司抓住国铁集团铁路投资增长的契机，动车组和机车持续交付，市场地位稳固。公司成功实现永磁牵引技术在我国大功率新能源机车领域商业化应用，为重载运输场景的绿色低碳转型提供了全新解决方案。根据RT轨道交通网统计数据，2025年公司动车牵引系统国内市场占有率60.92%，连续14年行业领跑。通信信号业务持续推进，宁波8号线6月开通运营，实现首个自主FAO应用示范项目落地。

    输出：
    [
    {{
        "业务板块": "轨道交通",
        "战略目标": "巩固并提升轨道交通核心业务领先地位，推进关键系统自主化和商业化应用",
        "现状描述": "动车组和机车持续交付，牵引系统国内市占率60.92%，连续14年行业领跑",
        "关键措施": "推进永磁牵引技术商业化落地，持续交付动车组和机车，推动通信信号及自主FAO项目实施"
    }},
    {{
        "业务板块": "通信信号",
        "战略目标": "提升自主化系统解决方案能力并扩大示范应用",
        "现状描述": "宁波8号线开通运营，首个自主FAO应用示范项目落地",
        "关键措施": "推进FAO无人化拆分改造融合方案验证和项目落地"
    }}
    ]

    【示例2】
    输入文本：
    2025年重点工作情况如下：
    市场布局新进展：国内装备建设实现重大突破，产品市场占有率显著提升；民用航空产业高质量发展，应急国债项目实现全面交付；首次搭载广电5G空中应急通信基站投入实战应用。科技创新能力提升：全年研发投入达3.37亿元，重点突破11项核心技术瓶颈，新增7项技术成果转化为产品路线。治理能力持续增强：推进流程优化和AOS管理体系建设，采购业务实现归口统一管理，加速数字化转型升级。

    输出：
    [
    {{
        "业务板块": "市场布局",
        "战略目标": "扩大重点产品市场覆盖并推动重点项目落地应用",
        "现状描述": "国内装备建设实现突破，产品市占率提升，应急项目全面交付，5G空中应急通信投入实战应用",
        "关键措施": "推进民航与应急领域项目交付，拓展重点场景应用，强化市场开拓"
    }},
    {{
        "业务板块": "科技创新能力",
        "战略目标": "提升核心技术攻关和成果转化能力",
        "现状描述": "全年研发投入3.37亿元，突破11项核心技术瓶颈，新增7项技术成果转化为产品路线",
        "关键措施": "加大研发投入，完善技术路线图，推进核心技术攻关和成果转化"
    }},
    {{
        "业务板块": "治理能力",
        "战略目标": "提升管理效率和数字化运营能力",
        "现状描述": "流程优化持续推进，AOS管理体系建设深化，采购业务实现统一管理",
        "关键措施": "推进流程优化、管理体系建设和数字化转型升级"
    }}
    ]

    【现在请分析以下文本】
    公司名称：{company_name}
    股票代码：{stock_code}
    输入文本：
    {text[:12000]}
    """
        marker = "【现在请分析以下文本】"
        if marker in prompt:
            system_prompt, user_prompt = prompt.split(marker, 1)
            system_prompt = system_prompt.strip()
            user_prompt = marker + user_prompt
        else:
            system_prompt, user_prompt = "", prompt

        return self._call_llm(system_prompt, user_prompt, stock_code, "经营情况", BUSINESS_SCHEMA)

    def analyze_rd(self, text: str, stock_code: str, company_name: str) -> dict:
        """分析研发成果"""
        print(f"\n[{stock_code}] 正在分析研发成果...")

        prompt = f"""
你是一个专门做上市公司年报研发信息抽取的助手。
你的任务是从"报告期内获得的研发成果"中，提取关键研发信息，并输出标准 JSON。

请严格遵守以下要求：

【输出要求】
1. 只能输出一个 JSON 数组，不要输出任何解释、前后缀、标题、markdown 代码块。
2. JSON 数组中的每个对象必须且只能包含以下 5 个字段：
   - "技术/产品类别"
   - "具体成果"
   - "性能指标"
   - "应用前景"
   - "进展状态"
3. 必须使用双引号，保证 JSON 格式可被 json.loads 直接解析。
4. 如果原文没有明确出现某项内容：
   - "性能指标"没有就填 ""
   - "应用前景"没有就填 ""
   - "进展状态"尽量根据原文规范化为：已量产 / 已交付 / 已应用 / 已验证 / 试验完成 / 已发布 / 已投运 / 已获奖 / 已发表 / 已出版 / 已授权 / 研发中 / 未说明
5. 不要编造指标或场景，不要输出原文外的信息。
6. 不要重复生成相同的内容

【抽取口径】
1. 一条成果对应一个对象。
2. 可抽取的成果类型包括但不限于：
   - 芯片、模块、器件、平台、系统、装备、算法、工艺
   - 论文、专著、奖项、专利、标准
3. "具体成果"应尽量写清楚对象名称和核心突破点。
4. "性能指标"只保留原文明确出现的量化指标或可验证性能描述。
5. "应用前景"只写原文明确提到的应用领域、应用场景或行业方向。
6. 对高度相似的成果可适度合并，但不要把完全不同类别的成果混成一条。

【示例1】
输入文本：
在新兴装备业务板块，突破第四代沟槽栅SiCMOSFET芯片技术，比导通电阻≤2毫欧平方厘米，达到国际领先水平。突破1μmPitch超精细沟槽IGBT技术，实现出流能力提升7%。发布400kW+光伏逆变器"赤霄"与3.XMW储能PCS"云枢"。完成第五代产品研制，纯电高压SiC多合一总成功率密度达到1.42kW/kg，CLTC工况效率达93.52%。全球首台水下重载作业型电动ROV完成商业化交付，能效提升27%。

输出：
[
  {{
    "技术/产品类别": "SiCMOSFET芯片",
    "具体成果": "突破第四代沟槽栅SiCMOSFET芯片技术",
    "性能指标": "比导通电阻≤2毫欧平方厘米",
    "应用前景": "",
    "进展状态": "已验证"
  }},
  {{
    "技术/产品类别": "IGBT技术",
    "具体成果": "突破1μmPitch超精细沟槽IGBT技术",
    "性能指标": "出流能力提升7%",
    "应用前景": "",
    "进展状态": "已验证"
  }},
  {{
    "技术/产品类别": "光伏/储能装备",
    "具体成果": "发布400kW+光伏逆变器"赤霄"和3.XMW储能PCS"云枢"",
    "性能指标": "",
    "应用前景": "光伏与储能场景",
    "进展状态": "已发布"
  }},
  {{
    "技术/产品类别": "高压SiC多合一总成",
    "具体成果": "完成第五代产品研制",
    "性能指标": "功率密度1.42kW/kg，CLTC工况效率93.52%",
    "应用前景": "",
    "进展状态": "已验证"
  }},
  {{
    "技术/产品类别": "电动ROV",
    "具体成果": "全球首台水下重载作业型电动ROV完成商业化交付",
    "性能指标": "能效提升27%",
    "应用前景": "水下重载作业",
    "进展状态": "已交付"
  }}
]

【示例2】
输入文本：
2025年公司发表SCI论文2篇、EI论文4篇、核心期刊论文5篇，专著3本《中空长航时多任务无人机》《多域无人系统智能协同认知控制技术》《基于虚实结合的无人机编队飞行技术》。"边缘计算无人机智能计算系统"项目获得航空工业集团科技进步三等奖，联合申报"基于精准可函数据理论的空天飞行器高性能自主控制与决策技术"项目获得四川省技术发明奖二等奖，并有5项科技成果获得协会奖项。

输出：
[
  {{
    "技术/产品类别": "科研论文",
    "具体成果": "发表SCI论文2篇、EI论文4篇、核心期刊论文5篇",
    "性能指标": "SCI论文2篇，EI论文4篇，核心期刊论文5篇",
    "应用前景": "",
    "进展状态": "已发表"
  }},
  {{
    "技术/产品类别": "专著",
    "具体成果": "出版《中空长航时多任务无人机》《多域无人系统智能协同认知控制技术》《基于虚实结合的无人机编队飞行技术》3本专著",
    "性能指标": "专著3本",
    "应用前景": "无人机与多域无人系统技术方向",
    "进展状态": "已出版"
  }},
  {{
    "技术/产品类别": "获奖项目",
    "具体成果": ""边缘计算无人机智能计算系统"项目获得航空工业集团科技进步三等奖",
    "性能指标": "",
    "应用前景": "无人机智能计算",
    "进展状态": "已获奖"
  }},
  {{
    "技术/产品类别": "获奖项目",
    "具体成果": ""基于精准可函数据理论的空天飞行器高性能自主控制与决策技术"项目获得四川省技术发明奖二等奖",
    "性能指标": "",
    "应用前景": "空天飞行器自主控制与决策",
    "进展状态": "已获奖"
  }},
  {{
    "技术/产品类别": "科技成果奖项",
    "具体成果": "5项科技成果获得协会奖项",
    "性能指标": "5项",
    "应用前景": "",
    "进展状态": "已获奖"
  }}
]

【现在请分析以下文本】
公司名称：{company_name}
股票代码：{stock_code}
输入文本：
{text[:12000]}
"""
        marker = "【现在请分析以下文本】"
        if marker in prompt:
            system_prompt, user_prompt = prompt.split(marker, 1)
            system_prompt = system_prompt.strip()
            user_prompt = marker + user_prompt
        else:
            system_prompt, user_prompt = "", prompt

        return self._call_llm(system_prompt, user_prompt, stock_code, "研发成果", RD_SCHEMA)

    def _call_llm(self, system_prompt: str, user_prompt: str, stock_code: str, analysis_type: str, schema: dict = None) -> dict:
        """调用LLM，支持模型自动回退"""

        models_to_try = [self.model] + self.fallback_models
        last_error = None

        def _request_chat_once(model_name, messages, format_schema=None, temperature=0.1, top_p=0.9, num_predict=4000):
            if self.provider in ("moonshot", "deepseek"):
                # OpenAI 兼容格式 (Moonshot / DeepSeek)
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": num_predict,
                }
                if format_schema:
                    payload["response_format"] = {"type": "json_object"}

                response = requests.post(
                    self.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=240
                )
                response.raise_for_status()
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                return answer, result
            else:
                # Ollama 格式
                payload = {
                    "model": model_name,
                    "stream": False,
                    "messages": messages,
                    "options": {
                        "temperature": temperature,
                        "top_p": top_p,
                        "num_predict": num_predict
                    }
                }
                if format_schema:
                    payload["format"] = format_schema

                response = requests.post(
                    self.api_endpoint,
                    json=payload,
                    timeout=240
                )
                response.raise_for_status()
                result = response.json()
                answer = (result.get("message") or {}).get("content", "") or result.get("response", "")
                return answer, result

        def _build_continue_messages(raw_answer: str):
            tail = raw_answer[-2500:] if raw_answer else ""
            continue_system = (
                "你是JSON续写器。你的任务是把被截断的JSON数组补全。"
                "只输出JSON续写片段，不要解释、不要markdown、不要重复已完成内容。"
            )
            continue_user = f"""
下面是一段被截断的JSON输出末尾。请从中断处继续输出，直到让整体成为一个可解析的完整JSON数组。

要求：
1. 只输出续写片段，不要输出解释文字。
2. 不要重复已有内容。
3. 最终应能与原内容直接拼接为合法JSON。
4. 若你判断原内容已完整，仅输出一个 ] 即可。

分析类型：{analysis_type}
原输出末尾：
{tail}
"""
            return [
                {"role": "system", "content": continue_system},
                {"role": "user", "content": continue_user}
            ]

        for model_name in models_to_try:
            try:
                print(f"  使用模型: {model_name}")

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                answer, result = _request_chat_once(
                    model_name=model_name,
                    messages=messages,
                    format_schema=schema,
                    temperature=0.1,
                    top_p=0.9,
                    num_predict=4000
                )

                print(f"  ✓ 收到响应，长度: {len(answer)} 字符")

                # 提取JSON
                data = self.extract_json_from_text(answer)

                if data:
                    print(f"  ✓ 成功解析 {len(data)} 条记录")
                    return {'success': True, 'data': data}

                # 疑似被截断时，自动续写一次
                truncation_reasons = self._get_truncation_reasons(answer, result)
                if truncation_reasons:
                    print(f"  ⚠ 可能截断，原因: {', '.join(truncation_reasons)}")
                    print(f"  ↻ 正在自动续写一次...")

                    continue_messages = _build_continue_messages(answer)
                    continue_answer, _ = _request_chat_once(
                        model_name=model_name,
                        messages=continue_messages,
                        format_schema=None,
                        temperature=0.0,
                        top_p=0.9,
                        num_predict=1200
                    )
                    print(f"  ✓ 续写响应长度: {len(continue_answer)} 字符")

                    merged_answer = (answer or "") + (continue_answer or "")
                    data = self.extract_json_from_text(merged_answer)
                    if data:
                        print(f"  ✓ 续写后成功解析 {len(data)} 条记录")
                        return {'success': True, 'data': data}

                print(f"  ❌ 无法解析JSON")
                last_error = Exception(f"模型 {model_name} 无法解析JSON")

            except Exception as e:
                print(f"  ❌ 模型 {model_name} 请求失败: {e}")
                last_error = e
                continue

        print(f"  ❌ 所有模型均失败")
        return {'success': False, 'error': str(last_error) if last_error else "所有模型失败"}

    def analyze_portrait_data(self, portrait_data: dict, stock_code: str, company_name: str) -> list:
        """
        分析 Portrait 结构化数据，生成三年趋势总结

        读取 portrait_data/*.json 中的财务指标，用 LLM 做定性分析。
        返回结构化 JSON 数组，每个维度一条记录。
        """
        print(f"\n[{stock_code}] 正在分析 Portrait 财务数据趋势...")

        # 处理数据结构：支持直接指标或嵌套在 metrics 中
        metrics = portrait_data.get('metrics', portrait_data)
        years = portrait_data.get('years', [])
        
        if not years and metrics.get('营业收入'):
            years = sorted(list(metrics.get('营业收入', {}).keys()))
        
        if not years:
            print(f"  ⚠️ 未找到年份数据")
            return []
        
        year_range = f"{min([int(y) for y in years])}-{max([int(y) for y in years])}" if years else ""

        # 构造精简的数据摘要（避免 token 过长）
        summary_text = f"""公司名称：{company_name}
股票代码：{stock_code}

以下为公司 {year_range} 年关键财务指标：

【营收与盈利能力】
营业收入：{metrics.get('营业收入', {})}
营业成本：{metrics.get('营业成本', {})}
毛利率：{metrics.get('毛利率', {})}%

【费用结构】
管理费用：{metrics.get('管理费用', {})}
销售费用：{metrics.get('销售费用', {})}
研发费用：{metrics.get('研发费用', {})}
财务费用：{metrics.get('财务费用', {})}
期间费用合计：{metrics.get('期间费用合计', {})}
管理费用率：{metrics.get('管理费用率', {})}%
销售费用率：{metrics.get('销售费用率', {})}%
研发费用率：{metrics.get('研发费用率', {})}%
期间费用率：{metrics.get('期间费用率', {})}%

【资产质量】
资产减值损失：{metrics.get('资产减值损失', {})}
存货：{metrics.get('存货', {})}
应收账款：{metrics.get('应收账款', {})}

【研发创新】
在研项目数量：{metrics.get('在研项目数量', {})}个
知识产权数量：{metrics.get('知识产权数量', {})}项

【供应链风险】
客户集中度：{metrics.get('客户集中度', {})}%
供应商集中度：{metrics.get('供应商集中度', {})}%"""

        prompt = f"""你是一个专业的上市公司财务分析助手。请根据以下三年的财务指标数据，从五个核心维度做趋势分析和总结。

{summary_text}

请严格按照以下要求输出：

【输出要求】
1. 只能输出一个 JSON 数组，不要输出任何解释、前后缀、标题、markdown 代码块。
2. 必须分析所有我提供了数据的维度（营收与盈利、费用结构、资产质量、研发创新、供应链风险）。
3. 如果某个维度的数据为空或缺失，可以跳过该维度。
4. 每个对象必须且只能包含以下字段：
   - "维度"（字符串）："营收与盈利" / "费用结构" / "资产质量" / "研发创新" / "供应链风险"
   - "三年趋势"（字符串）：如"持续增长" / "波动上升" / "先升后降" / "基本稳定"
   - "关键变化"（字符串）：用我提供的具体数字说明 1-2 个变化点
   - "风险提示"（字符串）：如有异常或风险简述；无则填"无"
   - "结论"（字符串）：一句话总结，不超过 30 字
5. 必须使用双引号，保证 JSON 格式可被 json.loads 直接解析。
6. 不要编造数据，所有分析必须基于提供的数据。
7. 请输出所有5个维度的分析（只要有数据），不要遗漏。
7. 只输出 JSON 数组，不要输出其他任何内容。
"""

        marker = "【输出要求】"
        if marker in prompt:
            system_prompt, user_prompt = prompt.split(marker, 1)
            system_prompt = system_prompt.strip()
            user_prompt = marker + user_prompt
        else:
            system_prompt, user_prompt = "", prompt

        # 调用 LLM
        result = self._call_llm(system_prompt, user_prompt, stock_code, "Portrait数据分析")

        if isinstance(result, dict) and result.get('success'):
            return result.get('data', [])
        elif isinstance(result, list):
            return result
        else:
            print(f"  ⚠️ Portrait 数据分析返回格式异常")
            return []

    def analyze_competitiveness(self, text: str, stock_code: str, company_name: str) -> dict:
        """分析核心竞争力"""
        print(f"\n[{stock_code}] 正在分析核心竞争力...")

        prompt = f"""
你是一个专门做上市公司年报核心竞争力分析的助手。
你的任务是从"核心竞争力分析"文本中，提取公司各竞争维度的关键信息。

请严格遵守以下要求：

【输出要求】
1. 只能输出一个 JSON 数组，不要输出任何解释、前后缀、标题、markdown 代码块。
2. JSON 数组中的每个对象必须且只能包含以下 4 个字段：
   - "竞争维度"
   - "核心优势"
   - "具体表现"
   - "与同行对比"
3. 必须使用双引号，保证 JSON 格式可被 json.loads 直接解析。
4. 如果某字段在原文中没有明确表述，可做"贴近原文的简要归纳"；若完全无法判断，填空字符串 ""。
5. 不要编造原文没有的信息，不要输出原文外的评价性语言。
6. 不要重复生成相同的内容。

【抽取口径】
1. 竞争维度包括但不限于：技术优势、产品优势、品牌优势、渠道优势、成本优势、人才优势、专利壁垒、规模效应等。
2. "核心优势"强调公司相对于竞争对手的独特能力和护城河。
3. "具体表现"强调具体数据、案例、成果、市占率、荣誉等可验证信息。
4. "与同行对比"强调公司与行业平均或主要竞争对手的差异和领先地位。
5. 相近内容合并，避免拆分得过细。

【现在请分析以下文本】
公司名称：{company_name}
股票代码：{stock_code}
输入文本：
{text[:12000]}
"""
        marker = "【现在请分析以下文本】"
        if marker in prompt:
            system_prompt, user_prompt = prompt.split(marker, 1)
            system_prompt = system_prompt.strip()
            user_prompt = marker + user_prompt
        else:
            system_prompt, user_prompt = "", prompt

        return self._call_llm(system_prompt, user_prompt, stock_code, "核心竞争力", COMPETITIVENESS_SCHEMA)

    def save_combined_results(self, business_data: list, rd_data: list, comp_data: list,
                              stock_code: str, company_name: str, output_dir: str = ".",
                              year_period: str = None, append_mode: bool = False) -> str:
        """保存合并结果到Excel

        Args:
            year_period: 报告期（如'2024年报'），为None时使用默认sheet名
            append_mode: 是否追加到已有Excel文件（多期合并时使用）
        """
        os.makedirs(output_dir, exist_ok=True)

        # 创建DataFrame
        df_business = pd.DataFrame(business_data)
        df_rd = pd.DataFrame(rd_data)
        df_comp = pd.DataFrame(comp_data)

        # 添加元信息
        meta_cols = [('股票代码', stock_code), ('公司名称', company_name)]
        if year_period:
            meta_cols.append(('报告期', year_period))
        meta_cols.append(('分析时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        for df in [df_business, df_rd, df_comp]:
            if not df.empty:
                for col_name, col_value in reversed(meta_cols):
                    df.insert(0, col_name, col_value)

        # 生成文件名
        excel_file = os.path.join(output_dir, f"{stock_code}_{company_name}_LLM分析结果.xlsx")

        # 确定 sheet 名（Excel sheet 名限制 31 字符）
        if year_period:
            sheet_business = f'经营情况_{year_period}'[:31]
            sheet_rd = f'研发成果_{year_period}'[:31]
            sheet_comp = f'核心竞争力_{year_period}'[:31]
        else:
            sheet_business = '经营情况分析'
            sheet_rd = '研发成果分析'
            sheet_comp = '核心竞争力分析'

        # 保存到不同sheet
        if append_mode and os.path.exists(excel_file):
            writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace')
        else:
            writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='w')

        with writer:
            if not df_business.empty:
                df_business.to_excel(writer, sheet_name=sheet_business, index=False)
            if not df_rd.empty:
                df_rd.to_excel(writer, sheet_name=sheet_rd, index=False)
            if not df_comp.empty:
                df_comp.to_excel(writer, sheet_name=sheet_comp, index=False)

        print(f"\n✓ 结果已保存: {excel_file}")
        if not df_business.empty:
            print(f"  - {sheet_business}: {len(df_business)} 条记录")
        if not df_rd.empty:
            print(f"  - {sheet_rd}: {len(df_rd)} 条记录")
        if not df_comp.empty:
            print(f"  - {sheet_comp}: {len(df_comp)} 条记录")

        return excel_file


def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("用法: python LLM2Excel_合并版.py <股票代码> <公司名称> <经营情况文本> <研发成果文本> [输出目录] [模型]")
        print("\n示例:")
        print('  python LLM2Excel_合并版.py 688049 炬芯科技 "经营情况.txt" "研发成果.txt"')
        sys.exit(1)

    stock_code = sys.argv[1]
    company_name = sys.argv[2]
    business_file = sys.argv[3]
    rd_file = sys.argv[4]
    output_dir = sys.argv[5] if len(sys.argv) > 5 else "./LLM测试输出"
    model_name = sys.argv[6] if len(sys.argv) > 6 else "deepseek-r1:1.5b"

    print("="*80)
    print("【LLM语义分析 - 合并版】")
    print("="*80)
    print(f"股票代码: {stock_code}")
    print(f"公司名称: {company_name}")
    print(f"经营情况文本: {business_file}")
    print(f"研发成果文本: {rd_file}")
    print(f"输出目录: {output_dir}")
    print(f"使用模型: {model_name}")
    print()

    # 检查文件
    for f in [business_file, rd_file]:
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}")
            sys.exit(1)

    # 创建分析器
    analyzer = LLMCombinedAnalyzer(model=model_name)

    # 读取文本
    business_text = analyzer.read_text_file(business_file)
    rd_text = analyzer.read_text_file(rd_file)

    if not business_text and not rd_text:
        print("❌ 两个文本文件都为空")
        sys.exit(1)

    # 分析
    business_result = analyzer.analyze_business(business_text, stock_code, company_name) if business_text else {'success': False}
    rd_result = analyzer.analyze_rd(rd_text, stock_code, company_name) if rd_text else {'success': False}

    # 保存结果
    if business_result['success'] or rd_result['success']:
        business_data = business_result.get('data', [])
        rd_data = rd_result.get('data', [])

        # 显示预览
        if business_data:
            print("\n经营情况分析预览:")
            print(pd.DataFrame(business_data).to_string())

        if rd_data:
            print("\n研发成果分析预览:")
            print(pd.DataFrame(rd_data).to_string())

        # 保存
        analyzer.save_combined_results(business_data, rd_data, stock_code, company_name, output_dir)

        print("\n" + "="*80)
        print("✓ 分析完成！")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ 分析失败")
        print("="*80)


def _detect_txt_type(folder_name: str) -> str:
    """根据文件夹名称判断txt分析类型"""
    name = folder_name.lower()
    # 优先级：先匹配更具体的，再匹配泛化的
    if '行业' in name or '趋势' in name or '产业' in name or '新技术' in name:
        return 'industry'
    elif '核心' in name or '竞争力' in name or '优势' in name:
        return 'competitiveness'
    elif '经营' in name or '业务与行业' not in name and '情况' in name:
        return 'business'
    elif '研发' in name or '成果' in name:
        return 'rd'
    return 'unknown'


def auto_locate_txt_files(base_dir: str, stock_code: str, company_name: str) -> dict:
    """根据股票代码和公司名自动扫描目录定位txt文件"""
    txt_map = {}

    if not os.path.exists(base_dir):
        return txt_map

    # 判断是否是具体公司目录（路径中包含股票代码和公司名）
    base_is_company_dir = stock_code in base_dir and company_name in base_dir

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.lower().endswith('.txt'):
                continue
            # 匹配逻辑：如果是具体公司目录，则接受该目录下所有txt；否则要求文件名包含股票代码和公司名
            if base_is_company_dir or (stock_code in file and company_name in file):
                folder_name = os.path.basename(root)
                txt_type = _detect_txt_type(folder_name)
                if txt_type != 'unknown':
                    # 避免重复：如果已存在同类型，优先保留路径更匹配的
                    if txt_type not in txt_map or len(root) < len(os.path.dirname(txt_map[txt_type])):
                        txt_map[txt_type] = os.path.join(root, file)

    return txt_map


def batch_process(base_dir: str, model_name: str = "gemma3:1b", max_workers: int = 1, provider: str = "ollama"):
    """
    批量处理所有公司的文本文件（自动扫描目录）
    同一公司的不同年份合并到同一个Excel文件的不同sheet中

    改进点：
    1. 按公司实时保存：分析完一个公司立即写入Excel，避免全部完成前崩溃导致全部丢失
    2. 增强健壮性：单个任务失败不影响其他任务
    3. 默认并发降为1，避免本地Ollama过载
    4. 实时进度显示

    目录结构预期:
        base_dir/
          688002_睿创微纳_2023年报/11_管理层讨论与分析/01_业务与行业/xxx.txt
          688002_睿创微纳_2024年报/11_管理层讨论与分析/01_业务与行业/xxx.txt
          ...

    输出结构:
        base_dir/
          688002_睿创微纳/
            688002_睿创微纳_LLM分析结果.xlsx  (包含多个sheet)
    """
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    print_lock = threading.Lock()

    # --- 1. 扫描文件并按 (stock_code, company_name) -> year_period -> type 分组 ---
    company_files = {}  # {(code, name): {year_period: {type: path}}}

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if not file.lower().endswith('.txt'):
                continue
            file_path = os.path.join(root, file)

            rel_path = os.path.relpath(root, base_dir)
            parts = rel_path.split(os.sep)

            stock_code = None
            company_name = None
            year_period = None

            for part in parts:
                match = re.match(r'^(\d{6})_(.+)$', part)
                if match and not re.search(r'\d+年(?:报|半年报)$', part):
                    stock_code = match.group(1)
                    company_name = match.group(2)
                    file_match = re.search(r'_(\d+年(?:报|半年报))(?:_\d+)?\.txt$', file, re.IGNORECASE)
                    year_period = file_match.group(1) if file_match else "未知"
                    break
            else:
                for part in parts:
                    match = re.match(r'^(\d{6})_(.+?)_(.+?年报)$', part)
                    if match:
                        stock_code = match.group(1)
                        company_name = match.group(2)
                        year_period = match.group(3)
                        break

            if not stock_code:
                continue

            folder_name = os.path.basename(root)
            txt_type = _detect_txt_type(folder_name)
            if txt_type == 'unknown':
                continue

            company_key = (stock_code, company_name)
            if company_key not in company_files:
                company_files[company_key] = {}
            if year_period not in company_files[company_key]:
                company_files[company_key][year_period] = {}
            company_files[company_key][year_period][txt_type] = file_path

    # --- 2. 准备任务列表 ---
    all_tasks = []
    for company_key, year_map in sorted(company_files.items()):
        stock_code, company_name = company_key
        for year_period, txt_map in sorted(year_map.items()):
            all_tasks.append((stock_code, company_name, year_period, txt_map))

    total_tasks = len(all_tasks)
    total_companies = len(company_files)

    print("="*80)
    print("【批量LLM语义分析 - 多期合并版】")
    print("="*80)
    print(f"基础目录: {base_dir}")
    print(f"主模型: {model_name}")
    print(f"备选模型: deepseek-r1:1.5b, qwen3:0.6b")
    print(f"并发数: {max_workers}")
    print(f"扫描到 {total_companies} 个公司，共 {total_tasks} 个(公司,年份)任务")
    for company_key, year_map in sorted(company_files.items()):
        years = ', '.join(sorted(year_map.keys()))
        print(f"  {company_key[0]} {company_key[1]}: {years}")
    print()

    # --- 3. 创建分析器 ---
    analyzer = LLMCombinedAnalyzer(model=model_name, provider=provider)

    # --- 4. 并发执行 LLM 分析，按公司实时保存 ---
    company_results = {}      # {(code, name): [(year_period, business_data, rd_data, comp_data), ...]}
    company_locks = {key: threading.Lock() for key in company_files}
    company_completed_years = {key: 0 for key in company_files}
    company_total_years = {key: len(v) for key, v in company_files.items()}
    saved_companies = set()
    completed_tasks = 0

    def analyze_one_task(args):
        stock_code, company_name, year_period, txt_map = args

        try:
            business_text = analyzer.read_text_file(txt_map.get('business', '')) if 'business' in txt_map else ""
            industry_text = analyzer.read_text_file(txt_map.get('industry', '')) if 'industry' in txt_map else ""
            if industry_text:
                business_text = f"【行业发展趋势】\n{industry_text}\n\n【经营情况】\n{business_text}" if business_text else industry_text
            rd_text = analyzer.read_text_file(txt_map.get('rd', '')) if 'rd' in txt_map else ""
            comp_text = analyzer.read_text_file(txt_map.get('competitiveness', '')) if 'competitiveness' in txt_map else ""

            start_time = time.time()

            business_result = analyzer.analyze_business(business_text, stock_code, company_name) if business_text else {'success': False}
            rd_result = analyzer.analyze_rd(rd_text, stock_code, company_name) if rd_text else {'success': False}
            comp_result = analyzer.analyze_competitiveness(comp_text, stock_code, company_name) if comp_text else {'success': False}

            elapsed = time.time() - start_time

            business_data = business_result.get('data', []) if business_result['success'] else []
            rd_data = rd_result.get('data', []) if rd_result['success'] else []
            comp_data = comp_result.get('data', []) if comp_result['success'] else []

            status = 'success' if (business_data or rd_data or comp_data) else 'no_data'

            with print_lock:
                if status == 'success':
                    print(f"✓ {stock_code} {company_name} [{year_period}] ({elapsed:.1f}s) - 经营:{len(business_data)}条 研发:{len(rd_data)}条 核心:{len(comp_data)}条")
                elif status == 'no_data':
                    print(f"⚠ {stock_code} {company_name} [{year_period}] ({elapsed:.1f}s) - 无数据")

            return {
                'stock_code': stock_code,
                'company_name': company_name,
                'year_period': year_period,
                'business_data': business_data,
                'rd_data': rd_data,
                'comp_data': comp_data,
                'status': status,
                'time': elapsed
            }

        except Exception as e:
            with print_lock:
                print(f"❌ {stock_code} {company_name} [{year_period}] - 错误: {e}")
            return {
                'stock_code': stock_code,
                'company_name': company_name,
                'year_period': year_period,
                'status': 'error',
                'error': str(e)
            }

    def _try_save_company(company_key):
        """检查并保存已完成的公司"""
        with company_locks[company_key]:
            if company_key in saved_companies:
                return
            if company_completed_years[company_key] < company_total_years[company_key]:
                return

            year_results = company_results.get(company_key, [])
            if not year_results:
                return

            stock_code, company_name = company_key
            year_results.sort(key=lambda x: x[0])

            company_output_dir = os.path.join(base_dir, f"{stock_code}_{company_name}")
            os.makedirs(company_output_dir, exist_ok=True)
            excel_file = os.path.join(company_output_dir, f"{stock_code}_{company_name}_LLM分析结果.xlsx")

            try:
                if os.path.exists(excel_file):
                    os.remove(excel_file)

                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    for year_period, business_data, rd_data, comp_data in year_results:
                        df_business = pd.DataFrame(business_data)
                        df_rd = pd.DataFrame(rd_data)
                        df_comp = pd.DataFrame(comp_data)

                        meta_cols = [
                            ('股票代码', stock_code),
                            ('公司名称', company_name),
                            ('报告期', year_period),
                            ('分析时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        ]

                        for df in [df_business, df_rd, df_comp]:
                            if not df.empty:
                                for col_name, col_value in reversed(meta_cols):
                                    df.insert(0, col_name, col_value)

                        if not df_business.empty:
                            df_business.to_excel(writer, sheet_name=f'经营情况_{year_period}'[:31], index=False)
                        if not df_rd.empty:
                            df_rd.to_excel(writer, sheet_name=f'研发成果_{year_period}'[:31], index=False)
                        if not df_comp.empty:
                            df_comp.to_excel(writer, sheet_name=f'核心竞争力_{year_period}'[:31], index=False)

                    # --- 追加 Portrait 数据分析 ---
                    portrait_json = os.path.join(company_output_dir, "portrait_data", f"{stock_code}_{company_name}_portrait_data.json")
                    if os.path.exists(portrait_json):
                        try:
                            with open(portrait_json, 'r', encoding='utf-8') as f:
                                portrait_data = json.load(f)
                            analyzer = LLMCombinedAnalyzer(model_name)
                            portrait_summary = analyzer.analyze_portrait_data(portrait_data, stock_code, company_name)
                            if portrait_summary:
                                df_portrait = pd.DataFrame(portrait_summary)
                                meta_portrait = [
                                    ('股票代码', stock_code),
                                    ('公司名称', company_name),
                                    ('分析类型', 'Portrait财务趋势分析'),
                                    ('分析时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                ]
                                for col_name, col_value in reversed(meta_portrait):
                                    df_portrait.insert(0, col_name, col_value)
                                df_portrait.to_excel(writer, sheet_name='Portrait数据分析'[:31], index=False)
                                with print_lock:
                                    print(f"  📊 Portrait 数据分析已追加")
                        except Exception as e:
                            with print_lock:
                                print(f"  ⚠️ Portrait 数据分析失败: {e}")

                with print_lock:
                    print(f"  💾 已保存: {stock_code}_{company_name}_LLM分析结果.xlsx ({len(year_results)}个年份)")
                saved_companies.add(company_key)

                # 清理内存
                if company_key in company_results:
                    del company_results[company_key]

            except Exception as e:
                with print_lock:
                    print(f"  ❌ 写入 {excel_file} 失败: {e}")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(analyze_one_task, task): task for task in all_tasks}

        for future in as_completed(futures):
            result = future.result()
            if not result:
                continue

            company_key = (result['stock_code'], result['company_name'])

            with company_locks[company_key]:
                company_completed_years[company_key] += 1
                if result.get('status') == 'success':
                    company_results.setdefault(company_key, []).append((
                        result['year_period'],
                        result['business_data'],
                        result['rd_data'],
                        result['comp_data']
                    ))

            completed_tasks += 1
            _try_save_company(company_key)

            progress_pct = completed_tasks / total_tasks * 100 if total_tasks else 0
            with print_lock:
                print(f"  >>> 总进度: {completed_tasks}/{total_tasks} ({progress_pct:.1f}%) | 已保存: {len(saved_companies)}/{total_companies} 家公司")

    total_time = time.time() - start_time

    print()
    print("="*80)
    print("【处理完成】")
    print("="*80)
    print(f"总计任务: {total_tasks} 个(公司,年份)")
    print(f"已保存公司: {len(saved_companies)}/{total_companies}")
    print(f"总耗时: {total_time:.1f} 秒")
    if total_tasks > 0:
        print(f"平均: {total_time/total_tasks:.1f} 秒/任务")
    print()
    print(f"结果保存在: 各公司目录下")
    print("="*80)


def main():
    """主函数"""
    # 检查是否是批量模式
    if len(sys.argv) >= 2 and sys.argv[1] == '--batch':
        # 批量模式: python LLM2Excel3.py --batch [基础目录] [模型名称] [并发数]
        # 默认基础目录为 output2
        base_dir = sys.argv[2] if len(sys.argv) > 2 else "output2"
        model_name = sys.argv[3] if len(sys.argv) > 3 else "gemma3:1b"
        max_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 2

        batch_process(base_dir, model_name, max_workers)
        return

    # 自动模式: 根据股票代码和名称自动扫描目录
    if len(sys.argv) >= 2 and sys.argv[1] == '--auto':
        # 自动模式: python LLM2Excel3.py --auto <股票代码> <公司名称> [基础目录] [输出目录] [模型]
        if len(sys.argv) < 4:
            print("自动模式用法: python LLM2Excel3.py --auto <股票代码> <公司名称> [基础目录] [输出目录] [模型]")
            print("\n示例:")
            print('  python LLM2Excel3.py --auto 688031 星环科技')
            print('  python LLM2Excel3.py --auto 688009 中国通号 "output2"')
            sys.exit(1)

        stock_code = sys.argv[2]
        company_name = sys.argv[3]
        base_dir = sys.argv[4] if len(sys.argv) > 4 else "output2"
        output_dir = sys.argv[5] if len(sys.argv) > 5 else "./LLM测试输出"
        model_name = sys.argv[6] if len(sys.argv) > 6 else "gemma3:1b"

        print("="*80)
        print("【LLM语义分析 - 自动定位版】")
        print("="*80)
        print(f"股票代码: {stock_code}")
        print(f"公司名称: {company_name}")
        print(f"扫描目录: {base_dir}")
        print(f"输出目录: {output_dir}")
        print(f"主模型: {model_name}")
        print(f"备选模型: deepseek-r1:1.5b, qwen3:0.6b")
        print()

        # 自动定位txt文件
        txt_map = auto_locate_txt_files(base_dir, stock_code, company_name)

        if not txt_map:
            print(f"❌ 未在 {base_dir} 下找到 {stock_code} {company_name} 的txt文件")
            sys.exit(1)

        print(f"✓ 找到 {len(txt_map)} 个txt文件:")
        for t, p in txt_map.items():
            print(f"  - {t}: {p}")
        print()

        # 创建分析器
        analyzer = LLMCombinedAnalyzer(model=model_name)

        # 读取文本（industry 类型追加到 business 中一起分析）
        business_text = analyzer.read_text_file(txt_map.get('business', '')) if 'business' in txt_map else ""
        industry_text = analyzer.read_text_file(txt_map.get('industry', '')) if 'industry' in txt_map else ""
        if industry_text:
            business_text = f"【行业发展趋势】\n{industry_text}\n\n【经营情况】\n{business_text}" if business_text else industry_text
        rd_text = analyzer.read_text_file(txt_map.get('rd', '')) if 'rd' in txt_map else ""
        comp_text = analyzer.read_text_file(txt_map.get('competitiveness', '')) if 'competitiveness' in txt_map else ""

        if not business_text and not rd_text and not comp_text:
            print("❌ 所有文本文件都为空")
            sys.exit(1)

        # 分析
        business_result = analyzer.analyze_business(business_text, stock_code, company_name) if business_text else {'success': False}
        rd_result = analyzer.analyze_rd(rd_text, stock_code, company_name) if rd_text else {'success': False}
        comp_result = analyzer.analyze_competitiveness(comp_text, stock_code, company_name) if comp_text else {'success': False}

        # 保存结果
        business_data = business_result.get('data', []) if business_result['success'] else []
        rd_data = rd_result.get('data', []) if rd_result['success'] else []
        comp_data = comp_result.get('data', []) if comp_result['success'] else []

        # 显示预览
        if business_data:
            print("\n经营情况分析预览:")
            print(pd.DataFrame(business_data).to_string())

        if rd_data:
            print("\n研发成果分析预览:")
            print(pd.DataFrame(rd_data).to_string())

        if comp_data:
            print("\n核心竞争力分析预览:")
            print(pd.DataFrame(comp_data).to_string())

        # 保存
        analyzer.save_combined_results(business_data, rd_data, comp_data, stock_code, company_name, output_dir)

        print("\n" + "="*80)
        print("✓ 分析完成！")
        print("="*80)
        return

    # 单文件模式（兼容旧版）
    if len(sys.argv) < 5:
        print("用法:")
        print("  自动模式:   python LLM2Excel3.py --auto <股票代码> <公司名称> <基础目录> [输出目录] [模型]")
        print("  批量模式:   python LLM2Excel3.py --batch <基础目录> [模型名称] [并发数]")
        print("  单文件模式: python LLM2Excel3.py <股票代码> <公司名称> <经营情况文本> <研发成果文本> [输出目录] [模型]")
        print("\n示例:")
        print('  python LLM2Excel3.py --auto 688031 星环科技 "output KC/提取结果"')
        print('  python LLM2Excel3.py --batch "llm"')
        print('  python LLM2Excel3.py 688049 炬芯科技 "经营情况.txt" "研发成果.txt"')
        sys.exit(1)

    stock_code = sys.argv[1]
    company_name = sys.argv[2]
    business_file = sys.argv[3]
    rd_file = sys.argv[4]
    output_dir = sys.argv[5] if len(sys.argv) > 5 else "./LLM测试输出"
    model_name = sys.argv[6] if len(sys.argv) > 6 else "gemma3:1b"

    print("="*80)
    print("【LLM语义分析 - 合并版】")
    print("="*80)
    print(f"股票代码: {stock_code}")
    print(f"公司名称: {company_name}")
    print(f"经营情况文本: {business_file}")
    print(f"研发成果文本: {rd_file}")
    print(f"输出目录: {output_dir}")
    print(f"主模型: {model_name}")
    print(f"备选模型: deepseek-r1:1.5b, qwen3:0.6b")
    print()

    # 检查文件
    for f in [business_file, rd_file]:
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}")
            sys.exit(1)

    # 创建分析器
    analyzer = LLMCombinedAnalyzer(model=model_name)

    # 读取文本
    business_text = analyzer.read_text_file(business_file)
    rd_text = analyzer.read_text_file(rd_file)

    if not business_text and not rd_text:
        print("❌ 两个文本文件都为空")
        sys.exit(1)

    # 分析
    business_result = analyzer.analyze_business(business_text, stock_code, company_name) if business_text else {'success': False}
    rd_result = analyzer.analyze_rd(rd_text, stock_code, company_name) if rd_text else {'success': False}

    # 保存结果
    if business_result['success'] or rd_result['success']:
        business_data = business_result.get('data', [])
        rd_data = rd_result.get('data', [])

        # 显示预览
        if business_data:
            print("\n经营情况分析预览:")
            print(pd.DataFrame(business_data).to_string())

        if rd_data:
            print("\n研发成果分析预览:")
            print(pd.DataFrame(rd_data).to_string())

        # 保存
        analyzer.save_combined_results(business_data, rd_data, [], stock_code, company_name, output_dir)

        print("\n" + "="*80)
        print("✓ 分析完成！")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ 分析失败")
        print("="*80)


if __name__ == '__main__':
    main()
