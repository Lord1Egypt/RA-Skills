#!/usr/bin/env python3
"""
自然语言意图识别器
将用户的自然语言转换为 Skill 命令
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Intent(Enum):
    """意图类型"""
    # Coordinator 相关
    COORD_START = "coord_start"
    COORD_SPAWN = "coord_spawn"
    COORD_STATUS = "coord_status"
    COORD_STOP = "coord_stop"
    
    # Permission 相关
    PERM_STATUS = "perm_status"
    PERM_MODE = "perm_mode"
    
    # Memory 相关
    MEMORY_SHOW = "memory_show"
    MEMORY_ADD = "memory_add"
    MEMORY_SEARCH = "memory_search"
    MEMORY_CLEAR = "memory_clear"
    
    # Task 相关
    TASK_CREATE = "task_create"
    TASK_PROGRESS = "task_progress"
    TASK_NEXT = "task_next"
    TASK_COMPLETE = "task_complete"
    TASK_LIST = "task_list"
    
    # Agent 相关
    AGENT_CREATE = "agent_create"
    AGENT_STATUS = "agent_status"
    AGENT_LIST = "agent_list"
    
    # 通用
    HELP = "help"
    STATUS = "status"
    UNKNOWN = "unknown"


@dataclass
class ParsedIntent:
    """解析后的意图"""
    intent: Intent
    confidence: float  # 0-1
    entities: Dict[str, str]
    raw_command: str
    explanation: str


class NaturalLanguageParser:
    """自然语言意图解析器"""
    
    # 意图模式匹配
    INTENT_PATTERNS = {
        # Coordinator
        Intent.COORD_START: [
            r"启动.*协作",
            r"开始.*团队",
            r"多.*Agent",
            r"协调.*模式",
            r"用团队",
            r"团队.*协作",
        ],
        Intent.COORD_SPAWN: [
            r"派.*Agent",
            r"派.*人",
            r"派生.*Agent",
            r"创建.*Worker",
            r"分配.*任务",
            r"让.*去做",
            r"让.*帮我",
        ],
        Intent.COORD_STATUS: [
            r".*状态",
            r"查看.*进展",
            r"团队.*怎样",
        ],
        Intent.COORD_STOP: [
            r"停止.*团队",
            r"退出.*协作",
            r"结束.*模式",
        ],
        
        # Permission
        Intent.PERM_STATUS: [
            r"权限.*状态",
            r"查看.*权限",
        ],
        Intent.PERM_MODE: [
            r"设置.*权限",
            r"权限.*模式",
        ],
        
        # Memory
        Intent.MEMORY_SHOW: [
            r"查看.*记忆",
            r"我的.*记忆",
            r"记住.*什么",
        ],
        Intent.MEMORY_ADD: [
            r"^记住.*",
            r"^记.*",
            r"添加.*记忆",
            r"新增.*记忆",
        ],
        Intent.MEMORY_SHOW: [
            r"查看.*记忆",
            r"看看.*记忆",
            r"我的.*记忆",
            r"记住.*什么",
        ],
        Intent.MEMORY_SEARCH: [
            r"搜索.*记忆",
            r"查找.*记忆",
        ],
        
        # Task
        Intent.TASK_CREATE: [
            r"创建.*任务",
            r"新建.*任务",
            r"帮我.*做",
            r"处理.*任务",
        ],
        Intent.TASK_PROGRESS: [
            r"任务.*进度",
            r"进展.*怎样",
            r"看看.*任务",
        ],
        
        # Agent
        Intent.AGENT_CREATE: [
            r"创建.*Agent",
            r"派个.*人",
            r"生成.*助手",
        ],
        
        # 通用
        Intent.HELP: [
            r"帮助",
            r"怎么用",
            r"有哪些.*功能",
            r"使用.*方法",
            r".*help.*",
        ],
        Intent.STATUS: [
            r"状态",
            r"怎么样",
            r"工作正常吗",
        ],
    }
    
    def __init__(self):
        self.intent_patterns = self.INTENT_PATTERNS
    
    def parse(self, text: str) -> ParsedIntent:
        """解析自然语言"""
        text = text.strip()
        text_lower = text.lower()
        
        # 尝试匹配每个意图
        best_match = None
        best_confidence = 0.0
        best_entities = {}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                # 不区分大小写匹配
                match = re.search(pattern, text_lower) or re.search(pattern, text)
                if match:
                    confidence = self._calculate_confidence(pattern, text_lower)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent
                        best_entities = self._extract_entities(text, intent)
        
        if best_match is None or best_confidence < 0.3:
            return ParsedIntent(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                entities={},
                raw_command=text,
                explanation="无法理解你的意图"
            )
        
        # 生成解释
        explanation = self._generate_explanation(best_match, best_entities, text)
        
        return ParsedIntent(
            intent=best_match,
            confidence=best_confidence,
            entities=best_entities,
            raw_command=text,
            explanation=explanation
        )
    
    def _calculate_confidence(self, pattern: str, text: str) -> float:
        """计算置信度"""
        # 清理 pattern 中的正则符号
        clean_pattern = pattern.replace("^", "").replace("$", "")
        
        # 精确匹配
        if clean_pattern in text:
            return 1.0
        
        # 如果已经匹配成功了（调用方已经确认有 match），返回高置信度
        # 这里只是辅助计算
        # 模糊匹配 - 用清理后的 pattern
        words = clean_pattern.replace(".*", " ").split()
        if not words:
            return 0.5
        match_count = sum(1 for w in words if w in text)
        return match_count / len(words)
    
    def _extract_entities(self, text: str, intent: Intent) -> Dict[str, str]:
        """提取实体"""
        entities = {}
        
        if intent in [Intent.COORD_SPAWN, Intent.TASK_CREATE, Intent.AGENT_CREATE]:
            # 提取任务描述
            entities["description"] = text
        
        elif intent == Intent.MEMORY_ADD:
            # 提取记忆内容
            entities["content"] = text.replace("记住", "").replace("记", "").strip()
        
        elif intent == Intent.MEMORY_SEARCH:
            # 提取搜索关键词
            entities["query"] = text.replace("搜索", "").replace("查找", "").strip()
        
        return entities
    
    def _generate_explanation(self, intent: Intent, entities: Dict, raw: str) -> str:
        """生成解释"""
        intent_explanations = {
            Intent.COORD_START: "🎯 识别为：启动多 Agent 协作模式",
            Intent.COORD_SPAWN: "🎯 识别为：派生新的 Worker Agent",
            Intent.COORD_STATUS: "🎯 识别为：查看团队状态",
            Intent.COORD_STOP: "🎯 识别为：停止协作模式",
            Intent.PERM_STATUS: "🎯 识别为：查看权限状态",
            Intent.MEMORY_SHOW: "🎯 识别为：查看记忆",
            Intent.MEMORY_ADD: "🎯 识别为：添加新记忆",
            Intent.MEMORY_SEARCH: "🎯 识别为：搜索记忆",
            Intent.TASK_CREATE: "🎯 识别为：创建新任务",
            Intent.TASK_PROGRESS: "🎯 识别为：查看任务进度",
            Intent.AGENT_CREATE: "🎯 识别为：创建新 Agent",
            Intent.HELP: "🎯 识别为：请求帮助",
            Intent.STATUS: "🎯 识别为：查看状态",
            Intent.UNKNOWN: "❓ 无法识别意图",
        }
        
        return intent_explanations.get(intent, "❓ 未知意图")
    
    def execute(self, parsed: ParsedIntent) -> str:
        """执行意图"""
        # 导入主模块
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        if parsed.intent == Intent.UNKNOWN:
            return f"""
{parsed.explanation}

你可以用以下命令：
- "启动团队协作" → 启动多 Agent 模式
- "帮我创建个任务" → 创建任务
- "记住我喜欢 TypeScript" → 添加记忆
- "查看状态" → 查看整体状态
- "帮助" → 查看所有功能
"""
        
        # 根据意图执行相应操作
        if parsed.intent == Intent.COORD_START:
            from coordinator.coordinator import get_coordinator
            coord = get_coordinator()
            return coord.start()
        
        elif parsed.intent == Intent.COORD_STATUS:
            from coordinator.coordinator import get_coordinator
            coord = get_coordinator()
            return coord.status()
        
        elif parsed.intent == Intent.COORD_STOP:
            from coordinator.coordinator import get_coordinator
            coord = get_coordinator()
            return coord.stop()
        
        elif parsed.intent == Intent.PERM_STATUS:
            from permission.permission import get_permission_system
            perm = get_permission_system()
            return perm.get_status()
        
        elif parsed.intent == Intent.MEMORY_SHOW:
            from memory.memory import get_memory_system
            mem = get_memory_system()
            return mem.get_summary()
        
        elif parsed.intent == Intent.MEMORY_ADD:
            from memory.memory import get_memory_system
            mem = get_memory_system()
            content = parsed.entities.get("content", parsed.raw_command)
            return mem.add("user", content)
        
        elif parsed.intent == Intent.MEMORY_SEARCH:
            from memory.memory import get_memory_system
            mem = get_memory_system()
            query = parsed.entities.get("query", "")
            results = mem.search(query)
            return f"找到 {len(results)} 条结果:\n" + "\n".join(f"- {r.content}" for r in results)
        
        elif parsed.intent == Intent.TASK_CREATE:
            from workflow.workflow import get_workflow
            wf = get_workflow()
            description = parsed.entities.get("description", parsed.raw_command)
            return wf.create(description)
        
        elif parsed.intent == Intent.TASK_PROGRESS:
            from workflow.workflow import get_workflow
            wf = get_workflow()
            return wf.progress()
        
        elif parsed.intent == Intent.AGENT_CREATE:
            from agent.agent_tool import get_agent_tool, AgentInput
            agt = get_agent_tool()
            description = parsed.entities.get("description", "任务")
            input_data = AgentInput(description=description[:20], prompt=parsed.raw_command)
            output = agt.create_agent(input_data)
            return f"✅ Agent 已创建: {output.agent_id}\n状态: {output.status}"
        
        elif parsed.intent == Intent.HELP:
            from main import get_enhancement
            enh = get_enhancement()
            return enh.help()
        
        elif parsed.intent == Intent.STATUS:
            from main import get_enhancement
            enh = get_enhancement()
            return enh.status()
        
        return f"❓ 尚未实现: {parsed.intent}"


# 主函数：自然语言 → 执行结果
def process_natural_language(text: str) -> str:
    """处理自然语言输入"""
    parser = NaturalLanguageParser()
    
    # 1. 解析意图
    parsed = parser.parse(text)
    
    # 2. 显示识别结果
    result = [parsed.explanation, ""]
    
    # 3. 执行
    try:
        execution_result = parser.execute(parsed)
        result.append(execution_result)
    except Exception as e:
        result.append(f"❌ 执行出错: {e}")
    
    return "\n".join(result)


# 测试
if __name__ == "__main__":
    import sys
    
    parser = NaturalLanguageParser()
    
    test_phrases = [
        "启动团队协作",
        "帮我创建个任务",
        "记住我喜欢 TypeScript",
        "查看状态",
        "帮我看看记忆",
        "怎么使用",
    ]
    
    print("=== 自然语言意图识别测试 ===\n")
    
    for phrase in test_phrases:
        print(f"输入: {phrase}")
        parsed = parser.parse(phrase)
        print(f"  意图: {parsed.intent.value} (置信度: {parsed.confidence:.2f})")
        print(f"  解释: {parsed.explanation}")
        print()