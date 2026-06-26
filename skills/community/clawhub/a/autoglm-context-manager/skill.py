"""
Context Manager Skill Implementation for OpenClaw.

This script provides the interface between OpenClaw and the Context Manager system.
"""
import sys
import os
import asyncio
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

# Add context-manager to path
CONTEXT_MANAGER_DIR = Path.home() / ".openclaw-autoclaw" / "workspace" / "context-manager"
sys.path.insert(0, str(CONTEXT_MANAGER_DIR))

try:
    from context_manager import context_manager
    from models import FileCreateType
    CONTEXT_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"Context Manager not available: {e}")
    CONTEXT_MANAGER_AVAILABLE = False


class ContextManagerSkill:
    """Context Manager skill for OpenClaw."""

    def __init__(self):
        self.context_manager = context_manager if CONTEXT_MANAGER_AVAILABLE else None

    async def handle_message(self, message: str) -> str:
        """
        Handle user message and return response.

        Args:
            message: User message

        Returns:
            Response text
        """
        if not CONTEXT_MANAGER_AVAILABLE:
            return "⚠️ Context Manager 不可用，请确保已安装依赖。"

        message = message.strip().lower()

        # Agent management
        if "创建" in message and "agent" in message:
            return await self._handle_create_agent(message)
        elif "列出" in message and "agent" in message:
            return await self._handle_list_agents()
        elif "删除" in message and "agent" in message:
            return await self._handle_delete_agent(message)

        # File operations
        elif "保存" in message or "创建文件" in message:
            return await self._handle_create_file(message)
        elif "显示" in message and "文件" in message:
            return await self._handle_list_files(message)
        elif "删除" in message and "文件" in message:
            return await self._handle_delete_file(message)

        # Search/Query
        elif "搜索" in message or "查找" in message or "检索" in message:
            return await self._handle_query(message)

        # Help
        elif "帮助" in message or "help" in message:
            return self._get_help()

        else:
            return """我理解你的请求，但需要更具体的信息。

我可以帮你：
🤖 管理 Agent
   - 创建 Agent: "为 '项目名称' 创建一个 Agent"
   - 列出 Agent: "列出所有 Agent"
   - 删除 Agent: "删除 Agent 'agent_id'"

📄 管理文件
   - 创建文件: "将以下内容保存到 Agent[agent_id] 的文件 'filename.md' 中：[内容]"
   - 列出文件: "显示 Agent 'agent_id' 的所有文件"
   - 删除文件: "删除 Agent 'agent_id' 的文件 'file_id'"

🔍 查询
   - 搜索: "在 Agent 'agent_id' 中搜索 '关键词'"
   - 基详情搜索: "查找 '关键词' 相关内容，并获取详情"
   - 跨 Agent 搜索: "在所有 Agent 中搜索 '关键词'"

💡 提示: 输入 "帮助" 查看完整说明"""

    async def _handle_create_agent(self, message: str) -> str:
        """Handle agent creation."""
        try:
            # Extract agent name
            import re
            match = re.search(r"为\s+['\"]?([^'\"]+)['\"]?\s+创建", message)
            if match:
                agent_name = match.group(1).strip()
            else:
                # Try alternative pattern
                match = re.search(r"创建\s+(?:一个\s+)?agent\s*[:：]?\s*['\"]?([^'\"]+)['\"]?", message)
                if match:
                    agent_name = match.group(1).strip()
                else:
                    return "❌ 无法解析 Agent 名称。请使用格式：'为 '项目名称' 创建一个 Agent'"

            # Generate agent ID
            agent_id = agent_name.lower().replace(" ", "_").replace("-", "_")

            # Create agent
            response = await self.context_manager.create_agent(
                agent_id=agent_id,
                name=agent_name,
                description=f"Agent for {agent_name}"
            )

            if response.success:
                return f"✓ 已创建 Agent '{agent_name}' (ID: {response.agent_id})\n   {response.message}"
            else:
                return f"❌ 创建 Agent 失败: {response.message}"

        except Exception as e:
            return f"❌ 创建 Agent 时出错: {str(e)}"

    async def _handle_list_agents(self) -> str:
        """Handle listing agents."""
        try:
            agents = await self.context_manager.list_agents()

            if not agents:
                return "📭 当前没有 Agent。创建一个吧！"

            result = f"📋 Agent 列表 ({len(agents)} 个):\n\n"
            for agent in agents:
                result += f"  • {agent.name} ({agent.agent_id})\n"
                result += f"    描述: {agent.description or 'N/A'}\n"
                result += f"    文件数: {agent.file_count}\n"
                result += f"    状态: {agent.status}\n\n"

            return result

        except Exception as e:
            return f"❌ 列出 Agent 时出错: {str(e)}"

    async def _handle_delete_agent(self, message: str) -> str:
        """Handle agent deletion."""
        try:
            import re
            match = re.search(r"删除\s+agent\s*['\"]?([^'\"]+)['\"]?", message)
            if not match:
                return "❌ 无法解析 Agent ID。请使用格式：'删除 Agent 'agent_id'"

            agent_id = match.group(1).strip()

            success = await self.context_manager.delete_agent(agent_id)

            if success:
                return f"✓ 已删除 Agent '{agent_id}'"
            else:
                return f"❌ 删除 Agent '{agent_id}' 失败"

        except Exception as e:
            return f"❌ 删除 Agent 时出错: {str(e)}"

    async def _handle_create_file(self, message: str) -> str:
        """Handle file creation."""
        try:
            import re

            # Parse agent ID and filename
            agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
            filename_match = re.search(r"文件\s*['\"]?([^'\"]+)['\"]?", message)

            if not agent_match or not filename_match:
                return """❌ 无法解析请求。请使用格式：
'将以下内容保存到 Agent 'agent_id' 的文件 'filename.md' 中：[内容]'"""

            agent_id = agent_match.group(1).strip()
            filename = filename_match.group(1).strip()

            # Extract content
            content_match = re.search(r"[:：](.+)", message, re.DOTALL)
            if not content_match:
                return "❌ 未找到文件内容。请在消息中包含文件内容。"

            content = content_match.group(1).strip()

            # Determine file type
            file_type = "text"
            if filename.endswith(".md"):
                file_type = "markdown"
            elif filename.endswith(".py"):
                file_type = "code"
            elif filename.endswith(".json"):
                file_type = "json"

            # Create file
            response = await self.context_manager.create_file(
                agent_id=agent_id,
                filename=filename,
                content=content,
                file_type=file_type
            )

            if response.success:
                return f"""✓ 文件 '{filename}' 已创建并索引
   Agent: {agent_id}
   文件 ID: {response.file_id}
   索引时间: {response.index_time_ms:.2f}ms

   提示: 使用 '在 Agent '{agent_id}' 中搜索 [关键词]' 来检索此文件"""
            else:
                return f"❌ 创建文件失败: {response.message}"

        except Exception as e:
            return f"❌ 创建文件时出错: {str(e)}"

    async def _handle_list_files(self, message: str) -> str:
        """Handle listing files."""
        try:
            import re
            match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
            if not match:
                return "❌ 无法解析 Agent ID。请使用格式：'显示 Agent 'agent_id' 的所有文件'"

            agent_id = match.group(1).strip()

            files = await self.context_manager.list_files(agent_id)

            if not files:
                return f"📭 Agent '{agent_id}' 中没有文件。"

            result = f"📄 Agent '{agent_id}' 的文件列表 ({len(files)} 个):\n\n"
            for file in files:
                result += f"  • {file.filename} (ID: {file.file_id})\n"
                result += f"    类型: {file.file_type}\n"
                result += f"    大小: {file.size} bytes\n"
                result += f"    标签: {', '.join(file.topic_tags) if file.topic_tags else '无'}\n"
                result += f"    创建时间: {file.created_at}\n\n"

            return result

        except Exception as e:
            return f"❌ 列出文件时出错: {str(e)}"

    async def _handle_delete_file(self, message: str) -> str:
        """Handle file deletion."""
        try:
            import re
            agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
            file_match = re.search(r"文件\s*['\"]?([^'\"]+)['\"]?", message)

            if not agent_match or not file_match:
                return "❌ 无法解析请求。请使用格式：'删除 Agent 'agent_id' 的文件 'file_id'"

            agent_id = agent_match.group(1).strip()
            file_id = file_match.group(1).strip()

            success = await self.context_manager.delete_file(agent_id, file_id)

            if success:
                return f"✓ 已删除 Agent '{agent_id}' 的文件 '{file_id}'"
            else:
                return f"❌ 删除文件失败"

        except Exception as e:
            return f"❌ 删除文件时出错: {str(e)}"

    async def _handle_query(self, message: str) -> str:
        """Handle query/search."""
        try:
            import re

            # Extract search query
            query_match = re.search(r"搜索\s+['\"]?([^'\"]+)['\"]?", message)
            if not query_match:
                query_match = re.search(r"查找\s+['\"]?([^'\"]+)['\"]?", message)
            if not query_match:
                query_match = re.search(r"检索\s+['\"]?([^'\"]+)['\"]?", message)

            if not query_match:
                return "❌ 无法解析搜索查询。请使用格式：'在 Agent 'agent_id' 中搜索 '关键词''"

            query = query_match.group(1).strip()

            # Check if agent_id is specified
            agent_id = None
            agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
            if agent_match:
                agent_id = agent_match.group(1).strip()

            # Check if details are requested
            require_details = "详情" in message or "详细" in message

            # Check if LLM is forced
            force_llm = "llm" in message or "分析" in message

            # Perform query
            response = await self.context_manager.query(
                query=query,
                agent_id=agent_id,
                limit=5,
                require_details=require_details,
                force_llm=force_llm
            )

            if not response.success:
                return f"❌ 查询失败: {response.error}"

            # Format results
            result = f"""🔍 搜索结果
   查询: {query}
   找到: {len(response.results)} 个文件
   时间: {response.total_time_ms:.2f}ms
   LLM 使用: {'是' if response.llm_used else '否'}
   缓存命中: {'是' if response.cache_hit else '否'}
"""

            if response.results:
                result += "\n📄 相关文件:\n"
                for i, r in enumerate(response.results, 1):
                    result += f"\n{i}. {r['filename']}\n"
                    result += f"   Agent: {r['agent_id']}\n"
                    result += f"   相似度: {r['combined_score']:.3f}\n"

            if response.details:
                result += "\n💡 详情:\n"
                for detail in response.details:
                    if "answer" in detail:
                        result += f"\n{detail['answer']}\n"
                    elif "type" in detail:
                        result += f"\n{detail.get('type', '')}: {detail.get('message', '')}\n"

            return result

        except Exception as e:
            return f"❌ 查询时出错: {str(e)}"

    def _get_help(self) -> str:
        """Get help text."""
        return """
🤖 Context Manager Skill - 帮助

我可以帮你管理多个 Agent 的长期上下文：

📋 Agent 管理
   创建 Agent:  '为 '项目名称' 创建一个 Agent'
   列出 Agent:  '列出所有 Agent'
   删除 Agent:  '删除 Agent 'agent_id''

📄 文件管理
   创建文件:  '将以下内容保存到 Agent 'agent_id' 的文件 'filename.md' 中：[内容]'
   列出文件:  '显示 Agent 'agent_id' 的所有文件'
   删除文件:  '删除 Agent 'agent_id' 的文件 'file_id''

🔍 查询与检索
   搜索:       '在 Agent 'agent_id' 中搜索 '关键词''
   带详情搜索: '查找 '关键词' 相关内容，并获取详情'
   跨 Agent:    '在所有 Agent 中搜索 '关键词''
   LLM 分析:    '用 LLM 分析 '关键词' 相关内容'

💡 示例对话
   用户：为 "研究项目" 创建一个 Agent
   AI：✓ 已创建 Agent '研究项目' (ID: research_project)

   用户：将以下内容保存到 Agent research_project 的文件 '文献.md' 中：
         深度学习是机器学习的一个子集...
   AI：✓ 文件 '文献.md' 已创建并索引

   用户：在 research_project 中搜索 "神经网络"
   AI：🔍 找到 3 个相关文件...

⚙️ 配置
   在 ~/.openclaw-autoclaw/workspace/context-manager/config.py 中调整参数

📚 更多信息
   查看完整文档: cat ~/.openclaw-autoclaw/workspace/context-manager/README.md
"""


async def main():
    """Main entry point for testing."""
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "帮助"

    skill = ContextManagerSkill()
    response = await skill.handle_message(message)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
