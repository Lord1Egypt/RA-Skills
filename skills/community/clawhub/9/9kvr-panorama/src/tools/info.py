"""Info 工具类

提供版本信息和全局上下文功能
"""

import json
import os
from typing import Any, Dict, List, Optional

from src.tools.prompts import PromptsTools
from src.api import config_account


class InfoTools:
    """Info 工具类"""

    def __init__(self):
        """初始化 Info 工具"""
        self.version = self._load_version()
        self.prompts_tools = PromptsTools()

    def _load_version(self) -> str:
        """从 package.json 加载版本号

        Returns:
            版本号字符串
        """
        # 尝试从多个位置查找 package.json
        possible_paths = [
            # 从 src/tools/info.py 向上查找
            os.path.join(os.path.dirname(__file__), "../../package.json"),
            os.path.join(os.path.dirname(__file__), "../../../package.json"),
            # 从项目根目录查找
            os.path.join(os.path.dirname(__file__), "../../../vr-skills/package.json"),
        ]

        for package_path in possible_paths:
            try:
                normalized_path = os.path.normpath(package_path)
                if os.path.exists(normalized_path):
                    with open(normalized_path, 'r', encoding='utf-8') as f:
                        package_json = json.load(f)
                        return package_json.get("version", "1.0.0")
            except (json.JSONDecodeError, IOError):
                continue

        return "1.0.0"

    def getTools(self) -> List[Dict[str, Any]]:
        """获取所有工具定义

        Returns:
            工具定义列表
        """
        return [
            {
                "name": "get_version",
                'description': "获取「全景小助手」（全景VR MCP服务）的版本号、开发者信息和支持的功能说明。当用户询问「小助手」、「全景小助手」、「你是谁」、「版本号」、「开发者」、「谁开发的」、「芊云全景」等问题时，应调用此工具。",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "get_global_context",
                'description': "【重要】获取全局上下文信息，包括当前时间、时间理解规范和格式规范。**必须**在以下情况调用：1) 用户提到相对时间（如「去年今天」、「上个月」、「3天前」、「一周前」等）；2) 需要基于当前时间进行计算或判断；3) 用户询问当前时间或日期；4) 需要按时间筛选或搜索作品/素材时。此工具返回的时间信息是动态的，每次调用都会获取最新时间，不要使用记忆中的时间。",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "config_account",
                "description": "**配置用户账号信息**。当用户提供 uid 和 token 并要求配置账号时调用此工具。例如用户说「我的 uid 是 <UID>，token 是 <TOKEN>，请帮我配置账号」或「帮我配置账号信息」时调用。配置成功后，后续所有 API 请求都会自动使用这个账号信息。",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "uid": {
                            "type": "string",
                            "description": "用户ID",
                        },
                        "token": {
                            "type": "string",
                            "description": "认证令牌",
                        },
                    },
                    "required": ["uid", "token"],
                },
            },
        ]

    def hasTool(self, name: str) -> bool:
        """检查是否存在指定的工具

        Args:
            name: 工具名称

        Returns:
            是否存在
        """
        return any(tool["name"] == name for tool in self.getTools())

    async def handleTool(self, name: str, args: Any) -> Dict[str, Any]:
        """处理工具调用

        Args:
            name: 工具名称
            args: 工具参数

        Returns:
            工具返回结果

        Raises:
            ValueError: 未知工具名称
        """
        if name == "get_version":
            return await self.getVersion(args)
        elif name == "get_global_context":
            return await self.getGlobalContext(args)
        elif name == "config_account":
            return await self.configAccount(args)
        else:
            raise ValueError(f"Unknown tool: {name}")

    async def getVersion(self, args: Any) -> Dict[str, Any]:
        """获取版本信息

        Args:
            args: 工具参数

        Returns:
            版本信息响应
        """
        capabilities = """**作品管理**
  - 获取作品列表（支持分页、搜索、筛选）
  - 查看作品详细信息
  - 获取作品场景列表
  - 更新作品信息（名称、描述、封面等）

**素材管理**
  - 获取素材列表（支持分页、搜索、类型筛选）
  - 查看素材详细信息
  - 更新素材信息（名称、描述）
  - 上传素材到素材库
  - 删除素材（移入回收站）
  - 获取素材下载链接

**开发指导**
  - 小程序接入指导（微信/抖音/快手）
  - 网页接入指导（Vue/React/原生JS）
  - 现有项目接入指导（网站/APP/CMS）
  - 生成接入代码示例

**使用提示**
  - 您可以直接告诉我您想要做什么，比如：
    - "查看我的作品列表"
    - "上传一个图片素材"
    - "更新作品名称"
    - "搜索包含某个关键词的作品"
    - "如何在小程序中接入全景？"
    - "给我一个Vue项目接入全景的示例代码"
  - 我会自动调用相应的工具来帮助您完成任务
  - 如果您需要帮助，随时告诉我！"""

        message = f"""# 您好，我是全景小助手！

**服务名称：** 全景小助手
**开发者：** 芊云全景
**当前版本：** v{self.version}

我是由芊云全景开发的全景VR管理助手，可以帮助您管理作品和素材，让您的工作更加高效便捷！

## 支持的功能

{capabilities}

---

**现在就开始使用吧！** 告诉我您想要做什么，我会立即为您处理。

**提示：** 您可以叫我"小助手"或"全景小助手"，我会随时为您服务！"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": message,
                },
            ],
        }

    async def getGlobalContext(self, args: Any) -> Dict[str, Any]:
        """获取全局上下文信息

        包含当前时间、时间理解规范和格式规范

        Args:
            args: 工具参数

        Returns:
            全局上下文响应
        """
        context = self.prompts_tools.getGlobalContext()

        return {
            "content": [
                {
                    "type": "text",
                    "text": context,
                },
            ],
        }

    async def configAccount(self, args: Any) -> Dict[str, Any]:
        """配置用户账号信息

        通过调用 vr-api -login 命令验证并保存账号信息。
        账号信息会保存到 ~/.9kvr/auth/vr-session.json
        后续所有 API 请求都会自动使用这个账号信息。

        Args:
            args: 包含 uid 和 token 的参数字典

        Returns:
            配置结果
        """
        uid = args.get("uid") if isinstance(args, dict) else None
        token = args.get("token") if isinstance(args, dict) else None

        if not uid or not token:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "配置失败：uid 和 token 都是必需的参数",
                    },
                ],
            }

        result = config_account(uid, token)

        if result["success"]:
            message = f"""# 账号配置成功！✅

**UID：** {uid}

账号信息已保存到本地，后续所有操作都会自动使用这个账号。

您现在可以：
- 查看我的作品列表
- 上传素材
- 管理场景
- 等等...

请告诉我您想做什么？"""
        else:
            message = f"""# 账号配置失败 ❌

**错误信息：** {result['message']}

请检查 uid 和 token 是否正确，然后重新配置。"""

        return {
            "content": [
                {
                    "type": "text",
                    "text": message,
                },
            ],
        }
