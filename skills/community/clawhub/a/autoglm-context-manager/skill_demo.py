"""
Context Manager Skill - Simplified version for testing integration.
This is a standalone version that demonstrates the skill interface.
"""

class ContextManagerSkill:
    """Context Manager skill for OpenClaw."""

    def __init__(self):
        self.agents = {}  # In-memory storage for demo
        self.files = {}  # In-memory file storage

    async def handle_message(self, message: str) -> str:
        """Handle user message and return response."""
        message = message.strip()

        # Agent management
        if "创建" in message and "agent" in message.lower():
            return self._create_agent(message)
        elif "列出" in message and "agent" in message.lower():
            return self._list_agents()
        elif "删除" in message and "agent" in message.lower():
            return self._delete_agent(message)

        # File operations
        elif "保存" in message or "创建文件" in message:
            return self._create_file(message)
        elif "显示" in message and "文件" in message:
            return self._list_files(message)
        elif "删除" in message and "文件" in message:
            return self._delete_file(message)

        # Search/Query
        elif "搜索" in message or "查找" in message or "检索" in message:
            return self._search(message)

        # Help
        elif "帮助" in message or "help" in message.lower():
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
   - 带详情搜索: "查找 '关键词' 相关内容，并获取详情"
   - 跨 Agent 搜索: "在所有 Agent 中搜索 '关键词'"

💡 提示: 输入 "帮助" 查看完整说明

注意: 这是简化演示版本。完整功能需要安装依赖：
pip install chromadb sentence-transformers fastapi uvicorn redis aiofiles openai"""

    def _create_agent(self, message: str) -> str:
        """Create an agent."""
        import re
        match = re.search(r"为\s+['\"]?([^'\"]+)['\"]?\s+创建", message)
        if match:
            agent_name = match.group(1).strip()
        else:
            match = re.search(r"创建\s+(?:一个\s+)?agent\s*[:：]?\s*['\"]?([^'\"]+)['\"]?", message)
            if match:
                agent_name = match.group(1).strip()
            else:
                return "❌ 无法解析 Agent 名称。请使用格式：'为 '项目名称' 创建一个 Agent'"

        agent_id = agent_name.lower().replace(" ", "_").replace("-", "_")
        self.agents[agent_id] = {
            "name": agent_name,
            "file_count": 0,
            "created_at": "刚刚"
        }

        return f"""✓ 已创建 Agent '{agent_name}' (ID: {agent_id})

💡 提示:
   - 使用 '将内容保存到 Agent {agent_id} 的文件 "filename.md" 中：[内容]' 来创建文件
   - 使用 '在 Agent {agent_id} 中搜索 "关键词"' 来搜索

注意: 这是简化演示版本，数据存储在内存中。重启后会清空。"""

    def _list_agents(self) -> str:
        """List all agents."""
        if not self.agents:
            return """📭 当前没有 Agent

创建一个 Agent:
   为 "项目名称" 创建一个 Agent

示例: 为 "研究项目" 创建一个 Agent"""

        result = f"📋 Agent 列表 ({len(self.agents)} 个):\n\n"
        for agent_id, agent_info in self.agents.items():
            result += f"  • {agent_info['name']} ({agent_id})\n"
            result += f"    文件数: {agent_info['file_count']}\n"
            result += f"    创建时间: {agent_info['created_at']}\n\n"

        return result

    def _delete_agent(self, message: str) -> str:
        """Delete an agent."""
        import re
        match = re.search(r"删除\s+agent\s*['\"]?([^'\"]+)['\"]?", message)
        if not match:
            return "❌ 无法解析 Agent ID。请使用格式：'删除 Agent 'agent_id'"

        agent_id = match.group(1).strip()

        if agent_id in self.agents:
            del self.agents[agent_id]
            # Also delete files
            self.files = {k: v for k, v in self.files.items() if not k.startswith(agent_id)}
            return f"✓ 已删除 Agent '{agent_id}'"
        else:
            return f"❌ Agent '{agent_id}' 不存在"

    def _create_file(self, message: str) -> str:
        """Create a file."""
        import re

        agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
        filename_match = re.search(r"文件\s*['\"]?([^'\"]+)['\"]?", message)

        if not agent_match or not filename_match:
            return """❌ 无法解析请求。请使用格式：
'将以下内容保存到 Agent 'agent_id' 的文件 'filename.md'中：[内容]'"""

        agent_id = agent_match.group(1).strip()
        filename = filename_match.group(1).strip()

        content_match = re.search(r"[:：](.+)", message, re.DOTALL)
        if not content_match:
            return "❌ 未找到文件内容。请在消息中包含文件内容。"

        content = content_match.group(1).strip()

        if agent_id not in self.agents:
            return f"❌ Agent '{agent_id}' 不存在。请先创建该 Agent。"

        file_id = f"{agent_id}_{filename}"
        self.files[file_id] = {
            "agent_id": agent_id,
            "filename": filename,
            "content": content,
            "created_at": "刚刚"
        }
        self.agents[agent_id]["file_count"] += 1

        return f"""✓ 文件 '{filename}' 已创建
   Agent: {agent_id}
   文件 ID: {file_id}

💡 提示:
   - 使用 '在 Agent {agent_id} 中搜索 "关键词"' 来检索此文件
   - 使用 '显示 Agent {agent_id} 的所有文件' 来查看所有文件

注意: 这是简化演示版本，实际系统会进行向量索引。"""

    def _list_files(self, message: str) -> str:
        """List files for an agent."""
        import re
        match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
        if not match:
            return "❌ 无法解析 Agent ID。请使用格式：'显示 Agent 'agent_id' 的所有文件'"

        agent_id = match.group(1).strip()

        if agent_id not in self.agents:
            return f"❌ Agent '{agent_id}' 不存在。"

        agent_files = [(k, v) for k, v in self.files.items() if v["agent_id"] == agent_id]

        if not agent_files:
            return f"📭 Agent '{agent_id}' 中没有文件。"

        result = f"📄 Agent '{agent_id}' 的文件列表 ({len(agent_files)} 个):\n\n"
        for file_id, file_info in agent_files:
            result += f"  • {file_info['filename']} (ID: {file_id})\n"
            result += f"    大小: {len(file_info['content'])} bytes\n"
            result += f"    创建时间: {file_info['created_at']}\n\n"

        return result

    def _delete_file(self, message: str) -> str:
        """Delete a file."""
        import re
        agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
        file_match = re.search(r"文件\s*['\"]?([^'\"]+)['\"]?", message)

        if not agent_match or not file_match:
            return "❌ 无法解析请求。请使用格式：'删除 Agent 'agent_id' 的文件 'file_id'"

        agent_id = agent_match.group(1).strip()
        file_id = file_match.group(1).strip()

        full_file_id = f"{agent_id}_{file_id}"

        if full_file_id in self.files:
            del self.files[full_file_id]
            self.agents[agent_id]["file_count"] -= 1
            return f"✓ 已删除 Agent '{agent_id}' 的文件 '{file_id}'"
        else:
            return f"❌ 文件 '{file_id}' 不存在"

    def _search(self, message: str) -> str:
        """Search for content."""
        import re

        query_match = re.search(r"搜索\s+['\"]?([^'\"]+)['\"]?", message)
        if not query_match:
            query_match = re.search(r"查找\s+['\"]?([^'\"]+)['\"]?", message)
        if not query_match:
            query_match = re.search(r"检索\s+['\"]?([^'\"]+)['\"]?", message)

        if not query_match:
            return "❌ 无法解析搜索查询。请使用格式：'在 Agent 'agent_id' 中搜索 '关键词''"

        query = query_match.group(1).strip()

        agent_id = None
        agent_match = re.search(r"agent\s*['\"]?([^'\"]+)['\"]?", message)
        if agent_match:
            agent_id = agent_match.group(1).strip()

        require_details = "详情" in message or "详细" in message

        # Simple keyword search (demo)
        results = []
        for file_id, file_info in self.files.items():
            if agent_id and file_info["agent_id"] != agent_id:
                continue

            content = file_info["content"].lower()
            query_lower = query.lower()

            # Simple relevance calculation
            relevance = 0
            if query_lower in content:
                relevance = content.count(query_lower) * 0.3
            # Add bonus for word matches
            query_words = query_lower.split()
            for word in query_words:
                if word in content:
                    relevance += 0.2

            if relevance > 0:
                results.append({
                    "file_id": file_id,
                    "agent_id": file_info["agent_id"],
                    "filename": file_info["filename"],
                    "relevance": min(relevance, 1.0),
                    "content": file_info["content"] if require_details else None
                })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        if not results:
            return f"""🔍 搜索结果
   查询: {query}
   找到: 0 个文件

💡 提示:
   - 尝试不同的关键词
   - 确保文件已创建
   - 使用 "列出所有 Agent" 查看可用的 Agent"""

        result = f"""🔍 搜索结果
   查询: {query}
   Agent: {agent_id or "所有"}
   找到: {len(results)} 个文件

📄 相关文件:
"""

        for i, r in enumerate(results[:5], 1):
            result += f"\n{i}. {r['filename']}\n"
            result += f"   Agent: {r['agent_id']}\n"
            result += f"   相关性: {r['relevance']:.2f}\n"

            if r["content"]:
                content_preview = r["content"][:200]
                if len(r["content"]) > 200:
                    content_preview += "..."
                result += f"   内容: {content_preview}\n"

        return result

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

💡 示例对话
   用户：为 "研究项目" 创建一个 Agent
   AI：✓ 已创建 Agent '研究项目' (ID: research_project)

   用户：将以下内容保存到 Agent research_project 的文件 '文献.md' 中：
         深度学习是机器学习的一个子集...
   AI：✓ 文件 '文献.md' 已创建

   用户：在 research_project 中搜索 "神经网络"
   AI：🔍 找到 3 个相关文件...

⚠️ 注意事项
   - 这是简化演示版本，数据存储在内存中
   - 重启后数据会清空
   - 完整功能需要安装依赖：
     pip install chromadb sentence-transformers fastapi uvicorn redis aiofiles openai

📚 完整文档
   查看完整文档:
   cat ~/.openclaw-autoclaw/workspace/context-manager/README.md

🔧 完整系统
   运行完整系统:
   cd ~/.openclaw-autoclaw/workspace/context-manager
   pip install -r requirements.txt
   python main.py
"""


# Export for OpenClaw
async def main():
    """Main entry point for testing."""
    import sys
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "帮助"

    skill = ContextManagerSkill()
    response = await skill.handle_message(message)
    print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
