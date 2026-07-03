---
name: AWS架构图生成工具
description: 通过Amazon Q CLI和MCP服务器在GitHub Codespace中快速生成高质量的AWS架构图。
version: 1.0.0
---

# AWS架构图生成工具

通过Amazon Q CLI和MCP服务器在GitHub Codespace中快速生成高质量的AWS架构图。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Generate a diagram from Python code using the diagrams package.

This tool accepts Python code as a string that uses the diagrams package DSL
and generates a PNG diagram without displaying it. The code is executed with
show=False to prevent automatic display.

USAGE INSTRUCTIONS:
Never import. Start writing code immediately with `with Diagram(` and use the icons you found with list_icons.
1. First use get_diagram_examples to understand the syntax and capabilities
2. Then use list_icons to discover all available icons. These are the only icons you can work with.
3. You MUST use icon names exactly as they are in the list_icons response, case-sensitive.
4. Write your diagram code following python diagrams examples. Do not import any additional icons or packages, the runtime already imports everything needed.
5. Submit your code to this tool to generate the diagram
6. The tool returns the path to the generated PNG file
7. For complex diagrams, consider using Clusters to organize components
8. Diagrams should start with a user or end device on the left, with data flowing to the right.

CODE REQUIREMENTS:
- Must include a Diagram() definition with appropriate parameters
- Can use any of the supported diagram components (AWS, K8s, etc.)
- Can include custom styling with Edge attributes (color, style)
- Can use Cluster to group related components
- Can use custom icons with the Custom class

COMMON PATTERNS:
- Basic: provider.service("label")
- Connections: service1 >> service2 >> service3
- Grouping: with Cluster("name"): [components]
- Styling: service1 >> Edge(color="red", style="dashed") >> service2

IMPORTANT FOR CLINE: Always send the current workspace directory when calling this tool!
The workspace_dir parameter should be set to the directory where the user is currently working
so that diagrams are saved to a location accessible to the user.

Supported diagram types:
- AWS architecture diagrams
- Sequence diagrams
- Flow diagrams
- Class diagrams
- Kubernetes diagrams
- On-premises diagrams
- Custom diagrams with custom nodes

Returns:
    Dictionary with the path to the generated diagram and status information
 | `scripts.tools.generate_diagram` |
| Get example code for different types of diagrams.

This tool provides ready-to-use example code for various diagram types.
Use these examples to understand the syntax and capabilities of the diagrams package
before creating your own custom diagrams.

USAGE INSTRUCTIONS:
1. Select the diagram type you're interested in (or 'all' to see all examples)
2. Study the returned examples to understand the structure and syntax
3. Use these examples as templates for your own diagrams
4. When ready, modify an example or write your own code and use generate_diagram

EXAMPLE CATEGORIES:
- aws: AWS cloud architecture diagrams (basic services, grouped workers, clustered web services, Bedrock)
- sequence: Process and interaction flow diagrams
- flow: Decision trees and workflow diagrams
- class: Object relationship and inheritance diagrams
- k8s: Kubernetes architecture diagrams
- onprem: On-premises infrastructure diagrams
- custom: Custom diagrams with custom icons
- all: All available examples across categories

Each example demonstrates different features of the diagrams package:
- Basic connections between components
- Grouping with Clusters
- Advanced styling with Edge attributes
- Different layout directions
- Multiple component instances
- Custom icons and nodes

Parameters:
    diagram_type (str): Type of diagram example to return. Options: aws, sequence, flow, class, k8s, onprem, custom, all

Returns:
    Dictionary with example code for the requested diagram type(s), organized by example name
 | `scripts.tools.get_diagram_examples` |
| List available icons from the diagrams package, with optional filtering.

This tool dynamically inspects the diagrams package to find available
providers, services, and icons that can be used in diagrams.

USAGE INSTRUCTIONS:
1. Call without filters to get a list of available providers
2. Call with provider_filter to get all services and icons for that provider
3. Call with both provider_filter and service_filter to get icons for a specific service

Example workflow:
- First call: list_icons() → Returns all available providers
- Second call: list_icons(provider_filter="aws") → Returns all AWS services and icons
- Third call: list_icons(provider_filter="aws", service_filter="compute") → Returns AWS compute icons

This approach is more efficient than loading all icons at once, especially when you only need
icons from specific providers or services.

Returns:
    Dictionary with available providers, services, and icons organized hierarchically
 | `scripts.tools.list_icons` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.generate_diagram
工具描述：Generate a diagram from Python code using the diagrams package.

This tool accepts Python code as a string that uses the diagrams package DSL
and generates a PNG diagram without displaying it. The code is executed with
show=False to prevent automatic display.

USAGE INSTRUCTIONS:
Never import. Start writing code immediately with `with Diagram(` and use the icons you found with list_icons.
1. First use get_diagram_examples to understand the syntax and capabilities
2. Then use list_icons to discover all available icons. These are the only icons you can work with.
3. You MUST use icon names exactly as they are in the list_icons response, case-sensitive.
4. Write your diagram code following python diagrams examples. Do not import any additional icons or packages, the runtime already imports everything needed.
5. Submit your code to this tool to generate the diagram
6. The tool returns the path to the generated PNG file
7. For complex diagrams, consider using Clusters to organize components
8. Diagrams should start with a user or end device on the left, with data flowing to the right.

CODE REQUIREMENTS:
- Must include a Diagram() definition with appropriate parameters
- Can use any of the supported diagram components (AWS, K8s, etc.)
- Can include custom styling with Edge attributes (color, style)
- Can use Cluster to group related components
- Can use custom icons with the Custom class

COMMON PATTERNS:
- Basic: provider.service("label")
- Connections: service1 >> service2 >> service3
- Grouping: with Cluster("name"): [components]
- Styling: service1 >> Edge(color="red", style="dashed") >> service2

IMPORTANT FOR CLINE: Always send the current workspace directory when calling this tool!
The workspace_dir parameter should be set to the directory where the user is currently working
so that diagrams are saved to a location accessible to the user.

Supported diagram types:
- AWS architecture diagrams
- Sequence diagrams
- Flow diagrams
- Class diagrams
- Kubernetes diagrams
- On-premises diagrams
- Custom diagrams with custom nodes

Returns:
    Dictionary with the path to the generated diagram and status information

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |Python code using the diagrams package DSL. The runtime already imports everything needed so you can start immediately using `with Diagram(`|
|filename|null|false| |The filename to save the diagram to. If not provided, a random name will be generated.|
|timeout|integer|false|90.0|The timeout for diagram generation in seconds. Default is 90 seconds.|
|workspace_dir|null|false| |The user's current workspace directory. CRITICAL: Client must always send the current workspace directory when calling this tool! If provided, diagrams will be saved to a 'generated-diagrams' subdirectory.|

---

## scripts.tools.get_diagram_examples
工具描述：Get example code for different types of diagrams.

This tool provides ready-to-use example code for various diagram types.
Use these examples to understand the syntax and capabilities of the diagrams package
before creating your own custom diagrams.

USAGE INSTRUCTIONS:
1. Select the diagram type you're interested in (or 'all' to see all examples)
2. Study the returned examples to understand the structure and syntax
3. Use these examples as templates for your own diagrams
4. When ready, modify an example or write your own code and use generate_diagram

EXAMPLE CATEGORIES:
- aws: AWS cloud architecture diagrams (basic services, grouped workers, clustered web services, Bedrock)
- sequence: Process and interaction flow diagrams
- flow: Decision trees and workflow diagrams
- class: Object relationship and inheritance diagrams
- k8s: Kubernetes architecture diagrams
- onprem: On-premises infrastructure diagrams
- custom: Custom diagrams with custom icons
- all: All available examples across categories

Each example demonstrates different features of the diagrams package:
- Basic connections between components
- Grouping with Clusters
- Advanced styling with Edge attributes
- Different layout directions
- Multiple component instances
- Custom icons and nodes

Parameters:
    diagram_type (str): Type of diagram example to return. Options: aws, sequence, flow, class, k8s, onprem, custom, all

Returns:
    Dictionary with example code for the requested diagram type(s), organized by example name

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|diagram_type|null|false|all|Type of diagram example to return. Options: aws, sequence, flow, class, k8s, onprem, custom, all|

---

## scripts.tools.list_icons
工具描述：List available icons from the diagrams package, with optional filtering.

This tool dynamically inspects the diagrams package to find available
providers, services, and icons that can be used in diagrams.

USAGE INSTRUCTIONS:
1. Call without filters to get a list of available providers
2. Call with provider_filter to get all services and icons for that provider
3. Call with both provider_filter and service_filter to get icons for a specific service

Example workflow:
- First call: list_icons() → Returns all available providers
- Second call: list_icons(provider_filter="aws") → Returns all AWS services and icons
- Third call: list_icons(provider_filter="aws", service_filter="compute") → Returns AWS compute icons

This approach is more efficient than loading all icons at once, especially when you only need
icons from specific providers or services.

Returns:
    Dictionary with available providers, services, and icons organized hierarchically

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provider_filter|null|false| |Filter icons by provider name (e.g., "aws", "gcp", "k8s")|
|service_filter|null|false| |Filter icons by service name (e.g., "compute", "database", "network")|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据