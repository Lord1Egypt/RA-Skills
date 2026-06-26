"""
LLM Decision - 编排器的 LLM 决策模块

让编排器能够使用 LLM 自动：
1. 分解任务
2. 决策下一步动作
3. 整合结果
"""

import json
import re
from typing import Dict, Any, List, Optional, Callable


class LLMDecisionMaker:
    """
    LLM 决策器
    
    使用 LLM 进行编排决策
    
    Example:
        >>> decision_maker = LLMDecisionMaker(llm_fn=my_llm_call)
        >>> decision = decision_maker.decide(task, history, available_models)
    """
    
    def __init__(
        self,
        llm_fn: Callable = None,
        verbose: bool = True,
    ):
        """
        Args:
            llm_fn: LLM 调用函数，签名为 fn(prompt: str) -> str
            verbose: 是否打印详细信息
        """
        self.llm_fn = llm_fn
        self.verbose = verbose
    
    def decide(
        self,
        task: str,
        history: List[Dict[str, Any]],
        available_models: List[str],
        available_tools: List[str] = None,
    ) -> Dict[str, Any]:
        """
        决策下一步动作
        
        Args:
            task: 原始任务
            history: 子任务历史
            available_models: 可用模型列表
            available_tools: 可用工具列表
            
        Returns:
            决策结果: {"action": "delegate"|"finish", "params": {...}}
        """
        # 构建决策 prompt
        prompt = self._build_decision_prompt(task, history, available_models, available_tools)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🤖 LLM 决策中...")
            print(f"{'='*60}")
        
        # 调用 LLM
        if self.llm_fn:
            response = self.llm_fn(prompt)
        else:
            # 没有提供 LLM 函数，使用启发式规则
            response = self._heuristic_decision(task, history)
        
        if self.verbose:
            print(f"\n📝 LLM 响应:")
            print(response[:500] + "..." if len(response) > 500 else response)
        
        # 解析响应
        decision = self._parse_response(response)
        
        if self.verbose:
            print(f"\n✅ 决策: {decision['action']}")
            if decision['action'] == 'delegate':
                print(f"   指令: {decision['params'].get('instruction', '')[:50]}...")
                print(f"   模型: {decision['params'].get('model', 'default')}")
        
        return decision
    
    def _build_decision_prompt(
        self,
        task: str,
        history: List[Dict[str, Any]],
        available_models: List[str],
        available_tools: List[str] = None,
    ) -> str:
        """构建决策 prompt"""
        
        # 格式化历史
        history_str = self._format_history(history)
        
        # 格式化模型
        models_str = self._format_models(available_models)
        
        # 格式化工具
        tools_str = self._format_tools(available_tools)
        
        prompt = f"""你是一个智能编排器，负责分解任务并委派给子 Agent。

==== 当前状态 ====
原始任务: {task}

==== 子任务历史 ====
{history_str}

==== 可用模型 ====
{models_str}

==== 可用工具 ====
{tools_str}

==== 决策规则 ====
1. 如果任务已完成或有足够信息，返回 finish
2. 如果需要更多信息，返回 delegate 创建子任务
3. 每次只委派一个子任务
4. 根据任务类型选择合适的模型：
   - 搜索/简单任务 → glm（便宜快速）
   - 代码/分析任务 → kimi（长上下文）
   - 创意/写作任务 → gemini（创意好）
   - 复杂推理任务 → sonnet（推理强）

==== 输出格式 ====
必须返回 JSON 格式（不要有其他内容）：

委派子任务:
{{
  "action": "delegate",
  "reasoning": "为什么需要这个子任务",
  "params": {{
    "instruction": "具体的子任务描述（清晰、可执行）",
    "context": ["相关背景信息"],
    "tools": ["web_search"],
    "model": "glm"
  }}
}}

完成任务:
{{
  "action": "finish",
  "reasoning": "为什么任务已完成",
  "params": {{
    "answer": "最终答案"
  }}
}}

现在请决策下一步动作："""
        
        return prompt
    
    def _format_history(self, history: List[Dict[str, Any]]) -> str:
        """格式化历史"""
        if not history:
            return "暂无子任务执行历史"
        
        lines = []
        for i, h in enumerate(history, 1):
            status = "✅" if h.get("success") else "❌"
            model = h.get("model", "unknown")
            instruction = h.get("instruction", "N/A")[:60]
            output = h.get("output", "")[:100]
            
            lines.append(f"[{i}] {status} {model}")
            lines.append(f"    任务: {instruction}...")
            if output:
                lines.append(f"    结果: {output}...")
        
        return "\n".join(lines)
    
    def _format_models(self, models: List[str]) -> str:
        """格式化模型列表"""
        model_info = {
            "glm": "便宜、快速、中文好",
            "kimi": "长上下文、代码强",
            "gemini": "创意好、多模态",
            "sonnet": "均衡、推理稳",
            "opus": "最强推理",
        }
        
        lines = ["| 模型 | 特点 |", "|------|------|"]
        for m in models:
            info = model_info.get(m, "通用")
            lines.append(f"| {m} | {info} |")
        
        return "\n".join(lines)
    
    def _format_tools(self, tools: List[str] = None) -> str:
        """格式化工具列表"""
        if not tools:
            return "web_search, web_fetch, read, write, exec（根据任务自动选择）"
        
        tool_info = {
            "web_search": "网页搜索",
            "web_fetch": "网页抓取",
            "read": "读取文件",
            "write": "写入文件",
            "exec": "执行命令",
        }
        
        return ", ".join(f"{t}({tool_info.get(t, '')})" for t in tools)
    
    def _heuristic_decision(
        self,
        task: str,
        history: List[Dict[str, Any]],
    ) -> str:
        """启发式决策（当没有 LLM 时）"""
        if not history:
            # 第一轮：委派搜索任务
            return json.dumps({
                "action": "delegate",
                "reasoning": "第一轮，开始收集信息",
                "params": {
                    "instruction": f"搜索并收集关于 '{task}' 的信息",
                    "context": [],
                    "tools": ["web_search", "web_fetch"],
                    "model": "glm",
                }
            }, ensure_ascii=False)
        else:
            # 有历史：整合并完成
            outputs = [h.get("output", "") for h in history if h.get("success")]
            answer = "\n\n".join(outputs) if outputs else "无法完成任务"
            
            return json.dumps({
                "action": "finish",
                "reasoning": "已收集足够信息",
                "params": {
                    "answer": answer,
                }
            }, ensure_ascii=False)
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """解析 LLM 响应"""
        # 尝试提取 JSON
        try:
            # 尝试直接解析
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # 尝试从 markdown 代码块中提取
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试找到 JSON 对象
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # 解析失败，返回默认
        return {
            "action": "finish",
            "reasoning": "无法解析 LLM 响应",
            "params": {
                "answer": response,
            }
        }


def decompose_task(
    task: str,
    num_subtasks: int = 3,
    llm_fn: Callable = None,
) -> List[Dict[str, Any]]:
    """
    使用 LLM 分解任务
    
    Example:
        >>> subtasks = decompose_task("调研 LangChain", num_subtasks=3)
        >>> # 返回 3 个子任务
    """
    prompt = f"""请将以下任务分解为 {num_subtasks} 个独立的子任务，每个子任务可以并行执行。

任务: {task}

返回 JSON 数组格式：
[
  {{
    "instruction": "子任务描述",
    "model": "glm|kimi|gemini|sonnet",
    "tools": ["web_search", ...]
  }},
  ...
]

只返回 JSON，不要其他内容："""

    if llm_fn:
        response = llm_fn(prompt)
    else:
        # 默认分解
        return [
            {"instruction": f"搜索 {task} 的基本信息", "model": "glm", "tools": ["web_search"]},
            {"instruction": f"搜索 {task} 的最新进展", "model": "glm", "tools": ["web_search"]},
            {"instruction": f"总结 {task} 的核心要点", "model": "kimi", "tools": []},
        ]
    
    # 解析响应
    try:
        return json.loads(response)
    except:
        # 尝试提取 JSON 数组
        match = re.search(r'\[[\s\S]*\]', response)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        
        # 失败，返回默认
        return [
            {"instruction": task, "model": "glm", "tools": ["web_search"]},
        ]


# 导出
__all__ = [
    "LLMDecisionMaker",
    "decompose_task",
]