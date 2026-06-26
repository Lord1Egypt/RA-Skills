#!/usr/bin/env python3
"""
OpenClaw Prompt优化系统 - 阶段五今日完成版

基于Claude Code架构的Prompt优化与上下文管理系统。
简化版本，今日完成核心功能。
"""

import os
import sys
import json
import hashlib
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import copy

# 确保在Python路径中包含当前目录
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@dataclass
class PromptFragment:
    """提示词片段"""
    fragment_id: str
    content: str
    fragment_type: str  # identity, principle, security, tool, memory, task
    priority: int  # 1-10, 10为最高
    required: bool = False  # 是否必须包含
    token_estimate: int = 0  # 估计的token数
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PromptFragment':
        return cls(**data)

@dataclass
class OptimizedPrompt:
    """优化后的提示词"""
    system_prompt: str
    tool_descriptions: List[Dict]
    memory_context: List[str]
    token_estimate: int
    compression_level: int  # 1-3
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class PromptFragmentLibrary:
    """提示词片段库"""
    
    def __init__(self):
        self.fragments = {}
        self.load_default_fragments()
    
    def load_default_fragments(self):
        """加载默认片段"""
        # 身份标识片段
        self.add_fragment(PromptFragment(
            fragment_id="identity_name",
            content="名字：毛豆",
            fragment_type="identity",
            priority=10,
            required=True,
            token_estimate=5
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="identity_role",
            content="角色：你的私人技术助理兼思考伙伴",
            fragment_type="identity",
            priority=10,
            required=True,
            token_estimate=10
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="identity_personality",
            content="性格：直接、务实、有温度，偶尔幽默但不刻意搞笑",
            fragment_type="identity",
            priority=9,
            required=True,
            token_estimate=15
        ))
        
        # 核心原则片段
        self.add_fragment(PromptFragment(
            fragment_id="principle_smart",
            content="聪明大于听话：理解用户真实意图，而不是逐字执行指令。遇到模糊需求时，先做最合理的假设再行动。",
            fragment_type="principle",
            priority=10,
            required=True,
            token_estimate=25
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="principle_efficiency",
            content="效率大于完美：能用脚本解决的，绝不手动重复。能用一句话回答的，绝不写三段。80%的完成度及时交付，优于100%的完成度拖延交付。",
            fragment_type="principle",
            priority=10,
            required=True,
            token_estimate=35
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="principle_learning",
            content="学习大于遗忘：每次犯错，立刻写入MEMORY.md，包含问题、根因、修正、预防规则。",
            fragment_type="principle",
            priority=9,
            required=True,
            token_estimate=20
        ))
        
        # 安全边界片段
        self.add_fragment(PromptFragment(
            fragment_id="security_l0",
            content="L0（自由行动）：读取文件、网络搜索、记忆检索 - 自动执行",
            fragment_type="security",
            priority=8,
            required=True,
            token_estimate=15
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="security_l1",
            content="L1（征询意见）：配置文件修改、依赖安装 - 告知后执行",
            fragment_type="security",
            priority=8,
            required=True,
            token_estimate=15
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="security_l2",
            content="L2（严格审批）：删除文件、外部通信 - 需要/approve",
            fragment_type="security",
            priority=8,
            required=True,
            token_estimate=15
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="security_l3",
            content="L3（默认禁止）：危险操作、凭证访问 - 默认禁止，特殊授权",
            fragment_type="security",
            priority=7,
            required=False,
            token_estimate=15
        ))
        
        # 工作偏好片段
        self.add_fragment(PromptFragment(
            fragment_id="preference_conclusion",
            content="回复风格：结论先行，不要铺垫",
            fragment_type="preference",
            priority=7,
            required=False,
            token_estimate=8
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="preference_code",
            content="代码风格：函数式优先，避免过度抽象",
            fragment_type="preference",
            priority=6,
            required=False,
            token_estimate=10
        ))
        
        self.add_fragment(PromptFragment(
            fragment_id="preference_communication",
            content="沟通习惯：消息短=专注，?=重新解释，ok=继续执行，多条消息=一起处理",
            fragment_type="preference",
            priority=7,
            required=False,
            token_estimate=20
        ))
    
    def add_fragment(self, fragment: PromptFragment):
        """添加片段"""
        self.fragments[fragment.fragment_id] = fragment
    
    def get_fragment(self, fragment_id: str) -> Optional[PromptFragment]:
        """获取片段"""
        return self.fragments.get(fragment_id)
    
    def get_fragments_by_type(self, fragment_type: str) -> List[PromptFragment]:
        """按类型获取片段"""
        return [f for f in self.fragments.values() if f.fragment_type == fragment_type]
    
    def get_required_fragments(self) -> List[PromptFragment]:
        """获取必须包含的片段"""
        return [f for f in self.fragments.values() if f.required]
    
    def estimate_tokens(self, text: str) -> int:
        """估算token数（简化版）"""
        # 近似估算：1个汉字≈2token，1个英文单词≈1.3token
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        other_chars = len(text) - chinese_chars - english_words
        
        return int(chinese_chars * 2 + english_words * 1.3 + other_chars * 0.8)

class ToolDescriptionOptimizer:
    """工具描述优化器"""
    
    def __init__(self):
        self.tool_categories = self.define_tool_categories()
        self.tool_descriptions = self.load_tool_descriptions()
    
    def define_tool_categories(self):
        """定义工具分类"""
        return {
            "core_always": ["read", "write", "edit", "exec"],  # 始终包含，详细描述
            "core_frequent": ["web_search", "web_fetch", "memory_search", "memory_get"],  # 高频，中等描述
            "extended_common": ["browser", "canvas", "image", "tts"],  # 常见，简要描述
            "extended_rare": ["image_generate", "process", "sessions_yield"],  # 罕见，最小描述
            "communication": ["message", "sessions_send", "sessions_spawn"],  # 通信，按需详细
            "management": ["subagents", "session_status", "agents_list", "sessions_list"],  # 管理，简要
            "analysis": ["sessions_history"]  # 分析，简要
        }
    
    def load_tool_descriptions(self):
        """加载工具描述"""
        descriptions = {
            # 核心工具 - 完整描述
            "read": {
                "full": "读取文件内容。支持文本文件和图像。对于文本文件，输出被截断为2000行或50KB。使用offset/limit处理大文件。",
                "medium": "读取文件内容。支持文本文件和图像。",
                "brief": "读取文件"
            },
            "write": {
                "full": "将内容写入文件。如果文件不存在则创建，如果存在则覆盖。自动创建父目录。",
                "medium": "写入内容到文件，自动创建目录。",
                "brief": "写入文件"
            },
            "edit": {
                "full": "使用精确文本替换编辑单个文件。每个edits[].oldText必须匹配原始文件中的唯一非重叠区域。",
                "medium": "编辑文件，使用精确文本替换。",
                "brief": "编辑文件"
            },
            "exec": {
                "full": "执行shell命令。对于需要长时间运行的工作，使用yieldMs/background稍后通过process工具继续。使用pty=true用于需要TTY的命令。",
                "medium": "执行shell命令，支持后台运行。",
                "brief": "执行命令"
            },
            # 高频工具 - 中等描述
            "web_search": {
                "full": "使用Tavily搜索网络。返回带片段的结构化结果。",
                "medium": "搜索网络，返回结构化结果。",
                "brief": "网络搜索"
            },
            "web_fetch": {
                "full": "从URL获取并提取可读内容（HTML→markdown/text）。用于轻量级页面访问，无需浏览器自动化。",
                "medium": "从URL获取内容并提取文本。",
                "brief": "获取网页"
            },
            "memory_search": {
                "full": "语义搜索MEMORY.md + memory/*.md（和可选的会话转录本）。回答关于先前工作、决策、日期、人员、偏好或待办事项的问题时使用。",
                "medium": "语义搜索记忆文件。",
                "brief": "搜索记忆"
            },
            # 通信工具 - 按需详细
            "message": {
                "full": "通过通道插件发送、删除和管理消息。当前通道（feishu）支持：send、read、edit、thread-reply、pin、react等。",
                "medium": "发送和管理消息到通信通道。",
                "brief": "发送消息"
            },
            "sessions_send": {
                "full": "通过sessionKey或label向另一个可见会话发送消息。用于将后续工作委托给现有会话。",
                "medium": "向其他会话发送消息。",
                "brief": "发送到会话"
            },
            "sessions_spawn": {
                "full": "使用runtime='subagent'或runtime='acp'生成隔离会话。mode='run'是一次性的，mode='session'是持久或线程绑定的。",
                "medium": "生成新的隔离会话。",
                "brief": "生成会话"
            },
            # 扩展工具 - 简要描述
            "browser": {
                "full": "通过OpenClaw的浏览器控制服务器控制浏览器（状态/启动/停止/配置文件/标签/打开/快照/截图/操作）。",
                "medium": "控制浏览器进行自动化。",
                "brief": "浏览器控制"
            },
            "canvas": {
                "full": "控制节点画布（呈现/隐藏/导航/评估/快照/A2UI）。使用快照捕获渲染的UI。",
                "medium": "控制节点画布和UI。",
                "brief": "画布控制"
            },
            "image": {
                "full": "使用视觉模型分析一个或多个图像。当用户的讯息中未提供图像时使用此工具。",
                "medium": "分析图像内容。",
                "brief": "分析图像"
            },
            "tts": {
                "full": "将文本转换为语音。音频从工具结果自动传送 - 成功调用后回复NO_REPLY以避免重复消息。",
                "medium": "文本转语音。",
                "brief": "文本转语音"
            }
        }
        
        # 为未明确描述的工具添加默认描述
        all_tools = []
        for category in self.tool_categories.values():
            all_tools.extend(category)
        
        for tool in all_tools:
            if tool not in descriptions:
                descriptions[tool] = {
                    "full": f"{tool}工具。",
                    "medium": f"{tool}工具。",
                    "brief": tool
                }
        
        return descriptions
    
    def get_tool_category(self, tool_name: str) -> str:
        """获取工具类别"""
        for category, tools in self.tool_categories.items():
            if tool_name in tools:
                return category
        return "extended_rare"
    
    def get_optimized_descriptions(self, task_type: str, context: Dict, 
                                 detail_level: str = "auto") -> List[Dict]:
        """获取优化后的工具描述"""
        
        # 确定任务需要的工具类别
        required_categories = self.determine_required_categories(task_type, context)
        
        # 选择工具
        selected_tools = []
        for category in required_categories:
            selected_tools.extend(self.tool_categories.get(category, []))
        
        # 去重
        selected_tools = list(set(selected_tools))
        
        # 生成描述
        optimized = []
        for tool in selected_tools:
            if tool in self.tool_descriptions:
                desc = self.tool_descriptions[tool]
                
                # 根据类别确定详细度
                category = self.get_tool_category(tool)
                if detail_level == "auto":
                    if category == "core_always":
                        description = desc.get("full", desc.get("medium", desc.get("brief", "")))
                    elif category in ["core_frequent", "communication"]:
                        description = desc.get("medium", desc.get("brief", ""))
                    else:
                        description = desc.get("brief", "")
                elif detail_level == "full":
                    description = desc.get("full", desc.get("medium", desc.get("brief", "")))
                elif detail_level == "brief":
                    description = desc.get("brief", "")
                else:
                    description = desc.get("medium", desc.get("brief", ""))
                
                optimized.append({
                    "name": tool,
                    "description": description,
                    "category": category,
                    "priority": self.get_category_priority(category)
                })
        
        # 按优先级排序
        optimized.sort(key=lambda x: x["priority"], reverse=True)
        
        return optimized
    
    def determine_required_categories(self, task_type: str, context: Dict) -> List[str]:
        """确定任务需要的工具类别"""
        # 根据任务类型推断需要的工具
        
        task_type_lower = task_type.lower()
        
        if "file" in task_type_lower or "read" in task_type_lower or "write" in task_type_lower:
            return ["core_always", "core_frequent"]
        
        elif "search" in task_type_lower or "web" in task_type_lower:
            return ["core_always", "core_frequent"]
        
        elif "message" in task_type_lower or "send" in task_type_lower or "communicate" in task_type_lower:
            return ["core_always", "communication"]
        
        elif "browser" in task_type_lower or "automate" in task_type_lower:
            return ["core_always", "extended_common"]
        
        elif "image" in task_type_lower or "vision" in task_type_lower:
            return ["core_always", "extended_common"]
        
        elif "agent" in task_type_lower or "session" in task_type_lower:
            return ["core_always", "management", "communication"]
        
        else:
            # 默认：包含核心工具
            return ["core_always", "core_frequent"]
    
    def get_category_priority(self, category: str) -> int:
        """获取类别优先级"""
        priorities = {
            "core_always": 10,
            "core_frequent": 9,
            "communication": 8,
            "extended_common": 7,
            "management": 6,
            "analysis": 5,
            "extended_rare": 4
        }
        return priorities.get(category, 5)

class ContextCompressor:
    """上下文压缩引擎（简化版）"""
    
    def __init__(self):
        self.fragment_library = PromptFragmentLibrary()
    
    def compress_conversation(self, conversation_history: List[Dict], 
                            token_budget: int = 4000) -> Dict:
        """压缩对话历史"""
        if len(conversation_history) <= 5:
            # 对话短，无需压缩
            return {
                "recent_history": conversation_history,
                "summarized_history": None,
                "compression_level": 1,
                "original_turns": len(conversation_history),
                "compressed_turns": len(conversation_history)
            }
        
        elif len(conversation_history) <= 15:
            # 中等长度对话，保留最近5轮
            recent = conversation_history[-5:]
            summarized = self.summarize_history(conversation_history[:-5])
            
            return {
                "recent_history": recent,
                "summarized_history": summarized,
                "compression_level": 2,
                "original_turns": len(conversation_history),
                "compressed_turns": 5
            }
        
        else:
            # 长对话，保留最近3轮，摘要其余
            recent = conversation_history[-3:]
            summarized = self.summarize_history(conversation_history[:-3])
            
            return {
                "recent_history": recent,
                "summarized_history": summarized,
                "compression_level": 3,
                "original_turns": len(conversation_history),
                "compressed_turns": 3
            }
    
    def summarize_history(self, history: List[Dict]) -> str:
        """摘要对话历史（简化版）"""
        if not history:
            return ""
        
        # 提取关键信息：用户请求和助理响应中的关键点
        key_points = []
        
        for turn in history:
            role = turn.get("role", "")
            content = turn.get("content", "")
            
            if role == "user" and content:
                # 提取用户请求的关键词
                simplified = self.simplify_user_request(content)
                if simplified:
                    key_points.append(f"用户: {simplified}")
            
            elif role == "assistant" and content:
                # 提取助理响应的关键行动
                actions = self.extract_actions(content)
                if actions:
                    key_points.append(f"助理: {actions}")
        
        if key_points:
            return "之前的对话摘要:\n- " + "\n- ".join(key_points[:10])  # 最多10个关键点
        else:
            return "之前的对话（已压缩）"
    
    def simplify_user_request(self, content: str) -> str:
        """简化用户请求"""
        # 移除问候语和冗余词
        content = re.sub(r'^(嘿|你好|嗨|hello|hi)\s*[,.]?\s*', '', content, flags=re.IGNORECASE)
        
        # 截断到100字符
        if len(content) > 100:
            content = content[:97] + "..."
        
        return content.strip()
    
    def extract_actions(self, content: str) -> str:
        """从助理响应中提取行动"""
        # 查找工具调用
        if "调用工具" in content or "使用" in content or "执行" in content:
            # 简单提取：查找工具名
            tools = re.findall(r'(\b\w+)\s*工具', content)
            if tools:
                return f"使用了工具: {', '.join(tools[:3])}"
        
        # 查找文件操作
        if "文件" in content or "写入" in content or "读取" in content:
            return "进行了文件操作"
        
        # 查找代码操作
        if "代码" in content or "脚本" in content or "程序" in content:
            return "进行了代码相关操作"
        
        # 默认
        if len(content) > 50:
            return content[:47] + "..."
        else:
            return content

class MemoryInjector:
    """记忆注入系统（简化版）"""
    
    def __init__(self, memory_dir: str = None):
        if memory_dir is None:
            memory_dir = os.path.expanduser("~/.openclaw/workspace/memory")
        self.memory_dir = memory_dir
    
    def get_relevant_memories(self, task: str, context: Dict, limit: int = 3) -> List[str]:
        """获取相关记忆"""
        memories = []
        
        try:
            # 1. 尝试从user-profile.md获取用户偏好
            user_profile_path = os.path.join(self.memory_dir, "user-profile.md")
            if os.path.exists(user_profile_path):
                with open(user_profile_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # 只读前1000字符
                
                # 提取关键信息
                if "偏好" in content or "习惯" in content or "风格" in content:
                    memories.append("用户工作偏好: " + self.extract_key_info(content, 50))
            
            # 2. 尝试从project-states.md获取项目状态
            project_path = os.path.join(self.memory_dir, "project-states.md")
            if os.path.exists(project_path):
                with open(project_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)
                
                # 查找相关项目
                task_lower = task.lower()
                if any(word in task_lower for word in ["claude", "code", "进化", "阶段"]):
                    memories.append("当前项目: Claude Code进化计划 - 阶段1-4基本完成，阶段5进行中")
            
            # 3. 尝试从今天的记忆文件获取
            today = datetime.now().strftime("%Y-%m-%d")
            today_path = os.path.join(self.memory_dir, f"{today}.md")
            if os.path.exists(today_path):
                with open(today_path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                
                if content.strip():
                    memories.append("今日进展: " + self.extract_key_info(content, 60))
            
        except Exception as e:
            print(f"获取记忆失败: {e}")
        
        # 限制数量
        return memories[:limit]
    
    def extract_key_info(self, content: str, max_len: int) -> str:
        """提取关键信息"""
        # 移除markdown标题和代码块
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        
        # 提取第一段有意义的内容
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10 and not line.startswith('-') and not line.startswith('*'):
                if len(line) > max_len:
                    return line[:max_len-3] + "..."
                else:
                    return line
        
        # 如果没有找到，返回前max_len个字符
        if len(content) > max_len:
            return content[:max_len-3] + "..."
        return content

class PromptOptimizer:
    """Prompt优化引擎主类"""
    
    def __init__(self, cache_dir: str = None):
        # 初始化组件
        self.fragment_library = PromptFragmentLibrary()
        self.tool_optimizer = ToolDescriptionOptimizer()
        self.context_compressor = ContextCompressor()
        self.memory_injector = MemoryInjector()
        
        # 缓存
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.openclaw/workspace/cache/prompts")
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 使用统计（简化版）
        self.usage_stats = {
            "total_optimizations": 0,
            "average_token_saving": 0,
            "last_optimized": None
        }
    
    def optimize_prompt(self, task: str, conversation_history: List[Dict] = None, 
                       context: Dict = None, token_budget: int = 6000) -> OptimizedPrompt:
        """优化提示词"""
        if context is None:
            context = {}
        
        if conversation_history is None:
            conversation_history = []
        
        # 1. 压缩对话历史
        compression_result = self.context_compressor.compress_conversation(
            conversation_history, token_budget
        )
        
        # 2. 确定任务类型
        task_type = self.analyze_task_type(task)
        
        # 3. 获取优化后的工具描述
        tool_descriptions = self.tool_optimizer.get_optimized_descriptions(
            task_type, context, detail_level="auto"
        )
        
        # 4. 获取相关记忆
        memory_context = self.memory_injector.get_relevant_memories(task, context, limit=3)
        
        # 5. 构建系统提示词
        system_prompt = self.build_system_prompt(task_type, context, compression_result["compression_level"])
        
        # 6. 估算token数
        token_estimate = self.estimate_total_tokens(
            system_prompt, tool_descriptions, memory_context, compression_result
        )
        
        # 7. 更新使用统计
        self.update_usage_stats(token_estimate)
        
        # 8. 返回优化后的提示词
        return OptimizedPrompt(
            system_prompt=system_prompt,
            tool_descriptions=tool_descriptions,
            memory_context=memory_context,
            token_estimate=token_estimate,
            compression_level=compression_result["compression_level"],
            created_at=datetime.now().isoformat()
        )
    
    def analyze_task_type(self, task: str) -> str:
        """分析任务类型"""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["文件", "读取", "写入", "编辑", "创建"]):
            return "file_operation"
        
        elif any(word in task_lower for word in ["搜索", "查找", "查询", "信息"]):
            return "information_search"
        
        elif any(word in task_lower for word in ["代码", "编程", "开发", "脚本"]):
            return "coding"
        
        elif any(word in task_lower for word in ["消息", "发送", "通信", "通知"]):
            return "communication"
        
        elif any(word in task_lower for word in ["分析", "处理", "整理", "总结"]):
            return "analysis"
        
        elif any(word in task_lower for word in ["配置", "设置", "安装", "部署"]):
            return "configuration"
        
        elif any(word in task_lower for word in ["测试", "验证", "检查", "调试"]):
            return "testing"
        
        else:
            return "general_assistance"
    
    def build_system_prompt(self, task_type: str, context: Dict, compression_level: int) -> str:
        """构建系统提示词"""
        prompt_parts = []
        
        # 1. 添加必须包含的片段
        required_fragments = self.fragment_library.get_required_fragments()
        for fragment in required_fragments:
            prompt_parts.append(fragment.content)
        
        # 2. 添加基于任务类型的片段
        task_fragments = self.get_task_specific_fragments(task_type)
        prompt_parts.extend(task_fragments)
        
        # 3. 添加基于压缩级别的提示
        if compression_level >= 2:
            prompt_parts.append("注意：对话历史已压缩，请参考提供的摘要理解上下文。")
        
        # 4. 添加当前时间（可选）
        if task_type in ["analysis", "configuration", "testing"]:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            prompt_parts.append(f"当前时间：{current_time} (北京时间)")
        
        # 组合所有部分
        system_prompt = "\n\n".join(prompt_parts)
        
        # 添加最终指示
        system_prompt += "\n\n请根据以上上下文和可用工具响应用户请求。"
        
        return system_prompt
    
    def get_task_specific_fragments(self, task_type: str) -> List[str]:
        """获取任务特定片段"""
        fragments = []
        
        if task_type == "file_operation":
            fragments.append("当前任务涉及文件操作，请仔细检查文件路径和权限。")
            fragments.append("修改重要文件前考虑创建备份。")
        
        elif task_type == "coding":
            fragments.append("当前任务涉及编程，请遵循函数式优先、避免过度抽象的代码风格。")
            fragments.append("提供代码时考虑可读性和维护性。")
        
        elif task_type == "communication":
            fragments.append("当前任务涉及外部通信，注意遵守安全边界和审批流程。")
            fragments.append("发送消息前确认内容和接收者。")
        
        elif task_type == "analysis":
            fragments.append("当前任务涉及分析，请提供结构化的结论和具体建议。")
            fragments.append("分析结果应该可操作、可验证。")
        
        elif task_type == "configuration":
            fragments.append("当前任务涉及系统配置，操作前验证当前状态，操作后验证结果。")
            fragments.append("记录所有配置变更以便追溯。")
        
        return fragments
    
    def estimate_total_tokens(self, system_prompt: str, tool_descriptions: List[Dict], 
                            memory_context: List[str], compression_result: Dict) -> int:
        """估算总token数"""
        total = 0
        
        # 系统提示词
        total += self.fragment_library.estimate_tokens(system_prompt)
        
        # 工具描述
        for tool in tool_descriptions:
            total += self.fragment_library.estimate_tokens(tool["description"]) + 10  # 名称和格式开销
        
        # 记忆上下文
        for memory in memory_context:
            total += self.fragment_library.estimate_tokens(memory)
        
        # 对话历史
        if compression_result["recent_history"]:
            for turn in compression_result["recent_history"]:
                content = turn.get("content", "")
                total += self.fragment_library.estimate_tokens(content)
        
        if compression_result["summarized_history"]:
            total += self.fragment_library.estimate_tokens(compression_result["summarized_history"])
        
        # 用户当前请求（估算）
        total += 100  # 估算用户当前请求的token
        
        return total
    
    def update_usage_stats(self, token_estimate: int):
        """更新使用统计"""
        self.usage_stats["total_optimizations"] += 1
        self.usage_stats["last_optimized"] = datetime.now().isoformat()
        
        # 简单估算节省：假设原始固定token为2500
        original_tokens = 2500
        if token_estimate < original_tokens:
            saving = original_tokens - token_estimate
            # 更新平均节省
            old_avg = self.usage_stats["average_token_saving"]
            old_count = self.usage_stats["total_optimizations"] - 1
            self.usage_stats["average_token_saving"] = (
                (old_avg * old_count) + saving
            ) / self.usage_stats["total_optimizations"]
    
    def get_optimization_stats(self) -> Dict:
        """获取优化统计"""
        return {
            "total_optimizations": self.usage_stats["total_optimizations"],
            "average_token_saving": round(self.usage_stats["average_token_saving"], 1),
            "last_optimized": self.usage_stats["last_optimized"],
            "estimated_efficiency_improvement": f"{self.usage_stats['average_token_saving']/2500*100:.1f}%"
        }

def test_optimizer():
    """测试优化器"""
    print("=" * 60)
    print("Prompt优化系统测试")
    print("=" * 60)
    
    # 初始化优化器
    optimizer = PromptOptimizer()
    
    # 测试场景1：文件操作任务
    print("\n测试场景1：文件操作任务")
    print("-" * 40)
    
    task1 = "读取文件 /etc/hosts 的内容"
    conversation1 = [
        {"role": "user", "content": "你好，帮我检查系统文件"},
        {"role": "assistant", "content": "好的，我可以帮你检查系统文件。请告诉我具体要检查哪个文件？"},
        {"role": "user", "content": "查看 /etc/hosts 文件"}
    ]
    
    optimized1 = optimizer.optimize_prompt(task1, conversation1)
    
    print(f"任务: {task1}")
    print(f"压缩级别: {optimized1.compression_level}")
    print(f"估计token数: {optimized1.token_estimate}")
    print(f"工具数量: {len(optimized1.tool_descriptions)}")
    print(f"记忆上下文: {len(optimized1.memory_context)}")
    
    # 显示部分系统提示词
    print("\n系统提示词 (前200字符):")
    print(optimized1.system_prompt[:200] + "...")
    
    # 测试场景2：开发任务
    print("\n\n测试场景2：开发任务")
    print("-" * 40)
    
    task2 = "写一个Python脚本来处理JSON数据"
    conversation2 = []
    
    optimized2 = optimizer.optimize_prompt(task2, conversation2)
    
    print(f"任务: {task2}")
    print(f"压缩级别: {optimized2.compression_level}")
    print(f"估计token数: {optimized2.token_estimate}")
    print(f"工具数量: {len(optimized2.tool_descriptions)}")
    
    # 显示选择的工具
    print("\n选择的工具:")
    for tool in optimized2.tool_descriptions[:5]:  # 显示前5个
        print(f"  - {tool['name']}: {tool['description'][:50]}...")
    
    # 测试场景3：长对话压缩
    print("\n\n测试场景3：长对话压缩测试")
    print("-" * 40)
    
    # 创建模拟的长对话历史
    long_conversation = []
    for i in range(20):
        long_conversation.append({
            "role": "user",
            "content": f"这是第{i+1}轮用户消息，讨论关于Claude Code进化计划第{i+1}个方面的内容"
        })
        long_conversation.append({
            "role": "assistant", 
            "content": f"助理第{i+1}轮响应，分析了第{i+1}个方面并提出了建议"
        })
    
    task3 = "继续讨论Claude Code的架构设计"
    optimized3 = optimizer.optimize_prompt(task3, long_conversation)
    
    print(f"原始对话轮数: {len(long_conversation)}")
    print(f"压缩后估计token数: {optimized3.token_estimate}")
    print(f"压缩级别: {optimized3.compression_level}")
    
    # 显示统计
    print("\n\n优化器统计:")
    stats = optimizer.get_optimization_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n测试完成!")
    print("=" * 60)
    
    return optimizer

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prompt优化系统")
    parser.add_argument("--test", "-t", action="store_true", help="运行测试")
    parser.add_argument("--task", help="要优化的任务描述")
    parser.add_argument("--stats", "-s", action="store_true", help="显示统计信息")
    parser.add_argument("--export", "-e", help="导出优化配置到文件")
    
    args = parser.parse_args()
    
    # 初始化优化器
    optimizer = PromptOptimizer()
    
    if args.test:
        # 运行测试
        test_optimizer()
    
    elif args.task:
        # 优化特定任务
        optimized = optimizer.optimize_prompt(args.task)
        
        print(f"任务: {args.task}")
        print(f"估计token数: {optimized.token_estimate}")
        print(f"压缩级别: {optimized.compression_level}")
        print(f"工具数量: {len(optimized.tool_descriptions)}")
        print(f"创建时间: {optimized.created_at}")
        
        # 显示系统提示词
        print("\n系统提示词:")
        print("-" * 40)
        print(optimized.system_prompt)
        print("-" * 40)
        
        # 显示工具
        print("\n工具描述:")
        for tool in optimized.tool_descriptions:
            print(f"\n{tool['name']} ({tool['category']}):")
            print(f"  {tool['description']}")
        
        # 显示记忆上下文
        if optimized.memory_context:
            print("\n记忆上下文:")
            for memory in optimized.memory_context:
                print(f"  - {memory}")
    
    elif args.stats:
        # 显示统计
        stats = optimizer.get_optimization_stats()
        print("优化器统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    elif args.export:
        # 导出配置
        import json
        
        config = {
            "fragment_library": {
                "total_fragments": len(optimizer.fragment_library.fragments),
                "fragment_types": set(f.fragment_type for f in optimizer.fragment_library.fragments.values())
            },
            "tool_optimizer": {
                "total_tools": len(optimizer.tool_optimizer.tool_descriptions),
                "categories": optimizer.tool_optimizer.tool_categories
            },
            "usage_stats": optimizer.get_optimization_stats(),
            "export_time": datetime.now().isoformat()
        }
        
        with open(args.export, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"配置已导出到 {args.export}")
    
    else:
        # 默认运行测试
        test_optimizer()

if __name__ == "__main__":
    main()