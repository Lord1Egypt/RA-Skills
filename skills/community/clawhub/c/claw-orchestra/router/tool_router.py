"""
Tool Router - 工具分配路由

AOrchestra 的核心洞察之三：编排器为每个子任务选择合适的工具子集，而不是给所有 Agent 一样的工具。

工具选择策略：
1. 任务类型 → 工具需求
2. 安全约束 → 工具限制
3. 效率优化 → 最小工具集

工具分类：
- 搜索类：web_search, web_fetch
- 文件类：read, write, edit
- 执行类：exec, process
- 浏览器类：browser, canvas
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum
import re


class ToolCategory(Enum):
    """工具类别"""
    SEARCH = "search"       # 搜索工具
    FILE = "file"           # 文件工具
    EXEC = "exec"           # 执行工具
    BROWSER = "browser"     # 浏览器工具
    MESSAGE = "message"     # 消息工具
    ALL = "all"             # 全部工具


# 工具注册表
TOOL_REGISTRY: Dict[str, ToolCategory] = {
    # 搜索类
    "web_search": ToolCategory.SEARCH,
    "web_fetch": ToolCategory.SEARCH,
    "tavily": ToolCategory.SEARCH,
    
    # 文件类
    "read": ToolCategory.FILE,
    "write": ToolCategory.FILE,
    "edit": ToolCategory.FILE,
    
    # 执行类
    "exec": ToolCategory.EXEC,
    "process": ToolCategory.EXEC,
    
    # 浏览器类
    "browser": ToolCategory.BROWSER,
    "canvas": ToolCategory.BROWSER,
    
    # 消息类
    "message": ToolCategory.MESSAGE,
    "tts": ToolCategory.MESSAGE,
}


@dataclass
class ToolSet:
    """工具集"""
    tools: List[str]
    categories: Set[ToolCategory] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = set()
        for tool in self.tools:
            category = TOOL_REGISTRY.get(tool, ToolCategory.ALL)
            self.categories.add(category)
    
    def has_category(self, category: ToolCategory) -> bool:
        return category in self.categories
    
    def __contains__(self, tool: str) -> bool:
        return tool in self.tools


# 预定义工具集
TOOL_SETS: Dict[str, ToolSet] = {
    "minimal": ToolSet(tools=[]),
    "search": ToolSet(tools=["web_search", "web_fetch"]),
    "file": ToolSet(tools=["read", "write"]),
    "code": ToolSet(tools=["read", "write", "edit", "exec"]),
    "browser": ToolSet(tools=["browser", "canvas"]),
    "full": ToolSet(tools=["web_search", "web_fetch", "read", "write", "edit", "exec", "browser", "canvas"]),
}


class ToolRouter:
    """
    工具分配路由器
    
    根据任务特征选择工具子集
    
    Example:
        >>> router = ToolRouter()
        >>> tools = router.select("搜索 LangChain 的最新版本")
        >>> print(tools)  # ["web_search", "web_fetch"]
    """
    
    def __init__(
        self,
        available_tools: List[str] = None,
        default_set: str = "search",
        safe_mode: bool = False,
        verbose: bool = False,
    ):
        self.available_tools = available_tools or list(TOOL_REGISTRY.keys())
        self.default_set = default_set
        self.safe_mode = safe_mode
        self.verbose = verbose
    
    def select(
        self,
        task: str,
        hint: str = None,
        additional_tools: List[str] = None,
    ) -> List[str]:
        """
        选择工具子集
        
        Args:
            task: 任务描述
            hint: 额外提示
            additional_tools: 额外需要的工具
            
        Returns:
            工具列表
        """
        # 1. 判断需要的工具类别
        categories = self._infer_categories(task, hint)
        
        # 2. 根据类别选择工具
        tools = self._select_by_categories(categories)
        
        # 3. 添加额外工具
        if additional_tools:
            for tool in additional_tools:
                if tool in self.available_tools and tool not in tools:
                    tools.append(tool)
        
        # 4. 安全模式过滤
        if self.safe_mode:
            tools = self._filter_safe_tools(tools)
        
        # 5. 去重
        tools = list(dict.fromkeys(tools))
        
        if self.verbose:
            print(f"\n📍 工具选择:")
            print(f"   任务: {task[:50]}...")
            print(f"   类别: {[c.value for c in categories]}")
            print(f"   工具: {tools}")
        
        return tools
    
    def _infer_categories(self, task: str, hint: str = None) -> Set[ToolCategory]:
        """推断需要的工具类别"""
        task_lower = task.lower()
        hint_lower = (hint or "").lower()
        combined = task_lower + " " + hint_lower
        
        categories = set()
        
        # 搜索相关
        search_keywords = ["搜索", "查找", "调研", "收集", "search", "find", "research", "最新"]
        if any(kw in combined for kw in search_keywords):
            categories.add(ToolCategory.SEARCH)
        
        # 文件相关
        file_keywords = ["文件", "读取", "写入", "编辑", "file", "read", "write", "edit"]
        if any(kw in combined for kw in file_keywords):
            categories.add(ToolCategory.FILE)
        
        # 执行相关
        exec_keywords = ["执行", "运行", "命令", "代码", "exec", "run", "command", "code", "实现"]
        if any(kw in combined for kw in exec_keywords):
            categories.add(ToolCategory.EXEC)
        
        # 浏览器相关
        browser_keywords = ["浏览器", "网页", "截图", "browser", "webpage", "screenshot"]
        if any(kw in combined for kw in browser_keywords):
            categories.add(ToolCategory.BROWSER)
        
        # 消息相关
        message_keywords = ["发送", "消息", "通知", "send", "message", "notify"]
        if any(kw in combined for kw in message_keywords):
            categories.add(ToolCategory.MESSAGE)
        
        # 默认搜索
        if not categories:
            categories.add(ToolCategory.SEARCH)
        
        return categories
    
    def _select_by_categories(self, categories: Set[ToolCategory]) -> List[str]:
        """根据类别选择工具"""
        tools = []
        
        for tool, category in TOOL_REGISTRY.items():
            if tool not in self.available_tools:
                continue
            
            # 如果类别匹配，或需要全部工具
            if category in categories or ToolCategory.ALL in categories:
                tools.append(tool)
        
        return tools
    
    def _filter_safe_tools(self, tools: List[str]) -> List[str]:
        """安全模式：过滤危险工具"""
        # 危险工具（安全模式下移除）
        dangerous_tools = {"exec", "process", "write", "edit"}
        return [t for t in tools if t not in dangerous_tools]
    
    def get_tool_set(self, name: str) -> ToolSet:
        """获取预定义工具集"""
        return TOOL_SETS.get(name, TOOL_SETS[self.default_set])


# === 便捷函数 ===

def select_tools(
    task: str,
    available_tools: List[str] = None,
    safe_mode: bool = False,
) -> List[str]:
    """
    快速工具选择的便捷函数
    
    Example:
        >>> tools = select_tools("搜索 LangChain 的最新版本")
        >>> print(tools)  # ["web_search", "web_fetch"]
    """
    router = ToolRouter(available_tools=available_tools, safe_mode=safe_mode)
    return router.select(task)