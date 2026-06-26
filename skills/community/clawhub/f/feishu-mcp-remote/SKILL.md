---
name: feishu-mcp-remote
description: "飞书 MCP 远程服务调用技能 - 通过 HTTP API 调用飞书云文档、用户搜索、文件获取等 MCP 工具能力。支持 UAT/TAT 认证，实现 AI Agent 与飞书的深度集成。"
metadata:
  {
    "openclaw": { "emoji": "🔌" }
  }
---

# 飞书 MCP 远程服务调用技能

通过 HTTP API 形式调用飞书官方部署的 MCP 服务，实现 AI Agent 与飞书云文档、通讯录等能力的深度集成。

## 🎯 核心优势

- **免部署**：直接连接飞书官方 MCP 服务，无需本地配置
- **快速集成**：通过 HTTP POST 请求即可调用飞书能力
- **丰富工具**：支持云文档、用户搜索、文件获取等多种工具
- **灵活认证**：支持 UAT（用户身份）和 TAT（应用身份）两种认证方式

## 📋 支持的 MCP 工具

### 通用工具

| 工具名称 | 功能描述 | 支持认证 | 所需权限 |
|---------|---------|---------|---------|
| `search-user` | 根据关键词搜索企业内用户 | UAT | contact:user:search |
| `get-user` | 获取用户个人信息 | UAT/TAT | contact:contact.base:readonly |
| `fetch-file` | 获取文件内容（图片/附件） | UAT/TAT | docs:document.media:download |

### 云文档工具

| 工具名称 | 功能描述 | 支持认证 | 所需权限 |
|---------|---------|---------|---------|
| `search-doc` | 搜索云文档 | UAT | search:docs:read |
| `create-doc` | 创建云文档 | UAT/TAT | docx:document:create |
| `fetch-doc` | 查看云文档内容 | UAT/TAT | docx:document:readonly |
| `update-doc` | 更新云文档 | UAT/TAT | docx:document:write_only |
| `list-docs` | 获取文档列表 | UAT/TAT | wiki:wiki:readonly |
| `get-comments` | 查看文档评论 | UAT/TAT | docs:document.comment:read |
| `add-comments` | 添加文档评论 | UAT/TAT | docs:document.comment:create |

## 🔧 接入流程

### 第 1 步：初始化连接 (initialize)

```python
import requests
import json

url = "https://mcp.feishu.cn/mcp"
headers = {
    "Content-Type": "application/json",
    "X-Lark-MCP-TAT": "t-gxxxxxxxxxxxxxxxxxxxxx",  # 或使用 X-Lark-MCP-UAT
    "X-Lark-MCP-Allowed-Tools": "create-doc,fetch-doc,update-doc"
}

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2))
```

### 第 2 步：列出可用工具 (tools/list)

```python
payload = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}

response = requests.post(url, headers=headers, json=payload)
tools = response.json()["result"]["tools"]
for tool in tools:
    print(f"工具名：{tool['name']}")
    print(f"描述：{tool['description']}")
```

### 第 3 步：调用工具 (tools/call)

```python
# 示例：创建云文档
payload = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "create-doc",
        "arguments": {
            "title": "我的测试文档",
            "content": "# 你好\n这是通过 MCP 创建的文档"
        }
    }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2))
```

## 🔐 认证方式

### User Access Token (UAT)

代表用户身份，适用于需要模拟特定用户操作的场景。

**获取方式：**
参考 [获取 user_access_token](https://open.larkoffice.com/document/server-docs/api-call-guide/calling-process/get-access-token?#4d916fe0)

**使用示例：**
```python
headers["X-Lark-MCP-UAT"] = "u-gxxxxxxxxxxxxxxxxxxxxx"
```

### Tenant Access Token (TAT)

代表应用身份，适用于服务端到服务端的调用场景。

**获取方式：**
```python
def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, json=payload)
    return response.json()["tenant_access_token"]

# 使用
tat = get_tenant_access_token("cli_xxxxx", "xxxxxxxx")
headers["X-Lark-MCP-TAT"] = tat
```

## 📝 完整示例类

```python
class FeishuMCPClient:
    """飞书 MCP 远程服务客户端"""
    
    def __init__(self, token, token_type="TAT", allowed_tools=None):
        """
        初始化 MCP 客户端
        
        Args:
            token: 访问凭证 (UAT 或 TAT)
            token_type: 凭证类型，"UAT" 或 "TAT"
            allowed_tools: 允许使用的工具列表
        """
        self.base_url = "https://mcp.feishu.cn/mcp"
        self.token = token
        self.token_type = token_type
        self.allowed_tools = allowed_tools or []
        self.session_id = None
        
    def _get_headers(self):
        """获取请求头"""
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.token_type == "UAT":
            headers["X-Lark-MCP-UAT"] = self.token
        else:
            headers["X-Lark-MCP-TAT"] = self.token
            
        if self.allowed_tools:
            headers["X-Lark-MCP-Allowed-Tools"] = ",".join(self.allowed_tools)
            
        return headers
    
    def _request(self, method, params=None):
        """发送 MCP 请求"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method
        }
        
        if params:
            payload["params"] = params
            
        response = requests.post(
            self.base_url,
            headers=self._get_headers(),
            json=payload
        )
        
        return response.json()
    
    def initialize(self):
        """初始化 MCP 会话"""
        result = self._request("initialize")
        if "result" in result:
            self.session_id = result["result"].get("protocolVersion")
            print(f"MCP 会话初始化成功，协议版本：{self.session_id}")
        return result
    
    def list_tools(self):
        """列出可用工具"""
        result = self._request("tools/list")
        if "result" in result and "tools" in result["result"]:
            tools = result["result"]["tools"]
            print(f"可用工具数量：{len(tools)}")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        return result
    
    def call_tool(self, tool_name, arguments):
        """调用工具"""
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        result = self._request("tools/call", params)
        
        # 检查是否执行失败
        if "result" in result and result["result"].get("isError"):
            error_text = result["result"]["content"][0]["text"]
            print(f"工具执行失败：{error_text}")
            
        return result
    
    # ========== 便捷方法 ==========
    
    def create_doc(self, title, content="", folder_token=None):
        """创建云文档"""
        arguments = {
            "title": title,
            "content": content
        }
        if folder_token:
            arguments["folder_token"] = folder_token
            
        return self.call_tool("create-doc", arguments)
    
    def fetch_doc(self, doc_id):
        """查看云文档"""
        return self.call_tool("fetch-doc", {"docID": doc_id})
    
    def update_doc(self, doc_id, content, block_id=None):
        """更新云文档"""
        arguments = {
            "docID": doc_id,
            "content": content
        }
        if block_id:
            arguments["block_id"] = block_id
            
        return self.call_tool("update-doc", arguments)
    
    def search_doc(self, query, creator_id=None):
        """搜索云文档"""
        arguments = {
            "query": query
        }
        if creator_id:
            arguments["creator_id"] = creator_id
            
        return self.call_tool("search-doc", arguments)
    
    def search_user(self, query):
        """搜索用户"""
        return self.call_tool("search-user", {"query": query})
    
    def list_docs(self, folder_token, page_size=20):
        """获取文档列表"""
        arguments = {
            "folder_token": folder_token,
            "page_size": page_size
        }
        return self.call_tool("list-docs", arguments)
    
    def get_comments(self, doc_id):
        """获取文档评论"""
        return self.call_tool("get-comments", {"docID": doc_id})
    
    def add_comment(self, doc_id, comment):
        """添加文档评论"""
        arguments = {
            "docID": doc_id,
            "comment": comment
        }
        return self.call_tool("add-comments", arguments)


# ============ 使用示例 ============

if __name__ == "__main__":
    # 初始化客户端
    client = FeishuMCPClient(
        token="t-gxxxxxxxxxxxxxxxxxxxxx",  # 替换为你的 TAT
        token_type="TAT",
        allowed_tools=["create-doc", "fetch-doc", "update-doc", "search-doc"]
    )
    
    # 初始化会话
    client.initialize()
    
    # 列出可用工具
    client.list_tools()
    
    # 创建文档
    result = client.create_doc(
        title="测试文档",
        content="# 你好\n这是通过 MCP 创建的文档"
    )
    print(f"创建结果：{result}")
    
    # 假设获得了文档 ID
    doc_id = result["result"]["content"][0]["text"]  # 实际需要从响应中提取
    
    # 查看文档
    doc_content = client.fetch_doc(doc_id)
    print(f"文档内容：{doc_content}")
    
    # 更新文档
    update_result = client.update_doc(
        doc_id=doc_id,
        content="\n## 更新内容\n这是追加的内容"
    )
    print(f"更新结果：{update_result}")
```

## ⚠️ 注意事项

### 权限申请

1. **根据工具申请权限**：每个工具需要特定的 API 权限
2. **UAT vs TAT**：
   - UAT 适合个人场景（如搜索用户）
   - TAT 适合应用场景（如批量创建文档）
3. **权限开通**：参考 [申请 API 权限](https://open.larkoffice.com/document/ukTMukTMukTM/uQjN3QjL0YzN04CN2cDN)

### 工具限制

- **文件大小**：fetch-file 限制 5MB 以内
- **文档类型**：search-doc 仅支持 doc、docx
- **评论类型**：get-comments/add-comments 仅支持文字、emoji、文档类型
- **不支持的内容**：多维表格、电子表格、OKR、任务、日程等

### 错误处理

```python
# 错误响应格式
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}

# 常见错误码
ERROR_CODES = {
    "-32700": "Parse error - 检查 JSON 格式",
    "-32600": "Invalid Request - JSON-RPC 结构错误",
    "-32601": "Method not found - 方法不存在",
    "-32602": "Invalid params - 参数错误",
    "-32603": "Internal error - 服务端异常",
    "-32030": "Rate Limited - 请求频率超限",
    "-32011": "UAT TAT Required - 缺少认证凭证",
    "-32003": "Param Validate Error - 凭证无效或过期",
    "-32042": "Invalid Content Type - Content-Type 错误"
}
```

### 最佳实践

1. **工具列表缓存**：initialize 和 tools/list 只需调用一次
2. **错误重试**：遇到 500 错误可重试 1-2 次
3. **频率控制**：避免短时间内大量调用（429 限流）
4. **日志记录**：记录 log_id 便于问题排查

## 🚀 快速开始

**告诉 SuperMike：**

1. **创建飞书文档**
> "用 MCP 创建一个飞书文档，标题是'项目周报'，内容是'# 本周工作\n1. 完成功能开发\n2. 修复 3 个 bug'"

2. **查看文档内容**
> "读取这个飞书文档：https://xxx.feishu.cn/docx/ABC123def"

3. **搜索用户**
> "搜索用户'张三'，获取他的 open_id"

4. **更新文档**
> "在文档 https://xxx.feishu.cn/docx/ABC123def 末尾追加内容：'\n## 更新记录\n2026-03-09 更新'"

---

_技能版本：v1.0_  
_创建日期：2026-03-09_  
_作者：SuperMike_
