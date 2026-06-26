"""Prompts 工具类

管理全局提示词，通过 MCP Prompts 功能提供给 AI
"""

from datetime import datetime
from typing import List, Dict, Any


class PromptsTools:
    """Prompts 工具类"""

    def __init__(self):
        """初始化 Prompts 工具"""
        pass

    def getPrompts(self) -> List[Dict[str, Any]]:
        """获取所有可用的 prompts

        Returns:
            Prompt 列表
        """
        return [
            {
                "name": "markdown_format_guide",
                "description": "Markdown 格式和链接规范，强制要求使用可点击的 Markdown 链接格式",
                "arguments": [],
            },
            {
                "name": "global_context_guide",
                "description": "全局上下文使用指南，说明何时应该调用 get_global_context 工具获取当前时间和规范",
                "arguments": [],
            },
            {
                "name": "account_config_guide",
                "description": "账号配置指南，当用户说「帮我配置账号信息」或提供 uid/token 时使用",
                "arguments": [],
            },
        ]

    def hasPrompt(self, name: str) -> bool:
        """检查是否存在指定的 prompt

        Args:
            name: Prompt 名称

        Returns:
            是否存在
        """
        return any(prompt["name"] == name for prompt in self.getPrompts())

    def getPrompt(self, name: str) -> Dict[str, Any]:
        """获取指定的 prompt 内容

        Args:
            name: Prompt 名称

        Returns:
            Prompt 内容

        Raises:
            ValueError: 未知 prompt 名称
        """
        if name == "markdown_format_guide":
            return {
                "description": "Markdown 格式和链接规范，强制要求使用可点击的 Markdown 链接格式",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": self._get_markdown_format_prompt(),
                        },
                    },
                ],
            }
        elif name == "global_context_guide":
            return {
                "description": "全局上下文使用指南，说明何时应该调用 get_global_context 工具获取当前时间和规范",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": self._get_global_context_guide_prompt(),
                        },
                    },
                ],
            }
        elif name == "account_config_guide":
            return {
                "description": "账号配置指南，当用户说「帮我配置账号信息」或提供 uid/token 时使用",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": self._get_account_config_guide_prompt(),
                        },
                    },
                ],
            }
        else:
            raise ValueError(f"Unknown prompt: {name}")

    def getGlobalContext(self) -> str:
        """获取简短的全局提示词

        包含当前时间信息和基本规范，供工具返回结果时使用
        每次调用都会动态生成最新的时间信息

        Returns:
            全局上下文字符串
        """
        current_time = self._get_current_time_string()
        now = datetime.now()
        last_year_date = f"{now.year - 1}年{now.month:02d}月{now.day:02d}日"

        return f"""# 全局上下文信息

## 当前时间
**当前时间：** {current_time}
**时间理解：**
- "去年今天" = {last_year_date}
- 所有相对时间（如"上个月"、"3天前"）都基于当前时间计算

## 【强制要求】输出格式规范

**重要：你必须严格遵守以下格式要求，否则会被视为错误！**

### 1. 所有回复必须使用 Markdown 格式
- 禁止直接返回 JSON 格式的原始数据
- 必须将工具返回的 JSON 数据格式化为易读的 Markdown 格式
- 使用 Markdown 语法来格式化文本（标题、列表、表格等）

### 2. 链接格式（强制要求）
- 禁止直接返回纯 URL，例如：`https://example.com`
- 必须使用 Markdown 链接格式：`[链接文本](链接地址)`
- 链接文本应该清晰描述链接内容，不要使用"点击这里"等模糊文本

### 3. 数据展示格式
当工具返回 JSON 数据时，你必须：
- 将作品列表格式化为表格或列表形式
- 将链接字段（如 `play_url`、`copyLink` 等）转换为 Markdown 链接
- 使用标题、列表、表格等 Markdown 元素来组织信息
- 突出重要信息（如作品名称、播放链接等）

### 4. 示例格式
**错误示例（禁止）：**
```json
{{
  "code": 1,
  "data": [{{
    "work_name": "作品名称",
    "play_url": "https://web.9kvr.cn/tour/123"
  }}]
}}
```

**正确示例（必须）：**
## 作品列表

| 作品名称 | 播放链接 |
|---------|---------|
| 作品名称 | [查看作品](https://web.9kvr.cn/tour/123) |

或者：

### 作品名称
- **播放链接：** [查看作品](https://web.9kvr.cn/tour/123)

### 5. 验证标准
- 所有链接必须可以直接点击
- 数据以易读的 Markdown 格式展示
- 不要直接展示原始 JSON 数据（除非用户明确要求）

**请确保你的所有回复都遵循以上规范！**"""

    def _get_current_time_string(self) -> str:
        """获取当前时间的格式化字符串

        Returns:
            格式化的时间字符串，格式：YYYY年MM月DD日 HH:mm:ss
        """
        now = datetime.now()
        return now.strftime("%Y年%m月%d日 %H:%M:%S")

    def _get_markdown_format_prompt(self) -> str:
        """获取 Markdown 格式提示词

        Returns:
            Markdown 格式规范文本
        """
        return """【重要规范】你必须严格遵守以下格式要求：

1. **所有回复必须使用 Markdown 格式**
   - 使用 Markdown 语法来格式化文本
   - 标题使用 #、##、### 等
   - 列表使用 - 或 1.
   - 代码使用 `代码` 或 ```代码块```

2. **链接格式（强制要求）**
   - 禁止直接返回纯 URL，例如：https://example.com
   - 必须使用 Markdown 链接格式：[链接文本](链接地址)
   - 示例：
     - 作品链接：[查看作品](https://web.9kvr.cn/tour/1)
     - 图片链接：[查看图片](https://web.9kvr.cn/image.jpg)
     - 下载链接：[下载文件](https://web.9kvr.cn/download/file.zip)

3. **链接文本要求**
   - 链接文本应该清晰描述链接内容
   - 不要使用"点击这里"、"链接"等模糊文本
   - 使用有意义的描述，例如："查看作品详情"、"下载素材文件"

4. **特殊情况处理**
   - 如果工具返回的数据中包含 URL 字段，必须将其转换为 Markdown 链接格式
   - 如果返回多个链接，使用列表格式展示
   - 示例：
     ```
     - [作品1](https://web.9kvr.cn/tour/1)
     - [作品2](https://web.9kvr.cn/tour/2)
     ```

5. **验证标准**
   - 所有链接必须可以直接点击
   - 链接文本和地址都要正确
   - 不要混合使用纯 URL 和 Markdown 链接

请确保你的所有回复都遵循以上规范，特别是链接格式！"""

    def _get_global_context_guide_prompt(self) -> str:
        """获取全局上下文使用指南提示词

        Returns:
            全局上下文使用指南文本
        """
        current_time = self._get_current_time_string()
        now = datetime.now()
        last_year_date = f"{now.year - 1}年{now.month:02d}月{now.day:02d}日"

        return f"""【重要】全局上下文工具使用指南

当你需要处理以下情况时，**必须**先调用 `get_global_context` 工具获取最新的全局上下文信息：

1. **时间相关查询**
   - 用户提到相对时间，如"去年今天"、"上个月"、"3天前"、"一周前"等
   - 用户询问"现在几点了"、"今天是什么日期"等
   - 需要基于当前时间进行任何计算或判断

2. **时间筛选和搜索**
   - 用户要求按时间筛选作品或素材（如"查找上个月上传的作品"）
   - 需要理解时间范围（如"最近一周"、"这个月"等）

3. **格式规范确认**
   - 需要确认输出格式要求时
   - 需要了解 Markdown 格式规范时

**调用方式：**
- 工具名称：`get_global_context`
- 无需参数，直接调用即可
- 工具会返回包含当前时间、时间理解规范和格式规范的完整信息

**重要提示：**
- 时间信息是动态的，每次调用都会获取最新时间
- 不要使用记忆中的时间，必须通过工具获取最新时间
- 在处理任何时间相关任务前，都应该先调用此工具

**示例场景：**
- 用户说"查看去年今天上传的作品" → 先调用 `get_global_context` 获取当前时间和"去年今天"的具体日期
- 用户说"上个月有哪些素材" → 先调用 `get_global_context` 了解当前时间，然后计算"上个月"的具体时间范围

**当前时间：** {current_time}
**"去年今天"：** {last_year_date}"""

    def _get_account_config_guide_prompt(self) -> str:
        """获取账号配置指南

        当用户说「帮我配置账号信息」或提供 uid/token 时使用。

        Returns:
            账号配置指南文本
        """
        return """【重要】账号配置指南

## 触发条件
当用户说以下内容时，必须执行账号配置：
- "帮我配置账号信息"
- "我的 uid 是 xxx token 是 xxx"
- "登录"
- "配置账号"
- 或提供任何 uid 和 token 信息

## 配置流程

### Step 1: 解析用户信息
从用户输入中提取：
- uid（用户ID）
- token（认证令牌）

### Step 2: 调用 vr-api 初始化命令
使用 subprocess 执行以下命令：
```bash
vr-api -login -uid <用户的uid> -token <用户的token>
```

### Step 3: 验证结果
- 如果成功：告诉用户"账号配置成功，已登录为 xxx"
- 如果失败：告诉用户具体的错误信息

## 重要提示
- vr-api 会自动将 session 保存到 ~/.9kvr/auth/vr-session.json
- 之后所有 API 请求都会自动使用这个 session
- 只需配置一次，后续无需再提供 uid/token

## 示例对话

用户：我的 uid 是 <UID> token 是 <TOKEN>，请帮我配置
AI：
1. 执行配置命令
2. 报告结果：账号配置成功！您已登录为「<USER_NAME>」（UID: <UID>）

用户：帮我配置账号信息，uid=<UID>, token=<TOKEN>
AI：
1. 执行配置命令
2. 报告结果"""
