---
name: CSV转JSON转换器
description: 一个基于FastMCP的CSV到JSON转换MCP服务器，提供高效的CSV数据转换服务。
version: 1.0.0
---

# CSV转JSON转换器

一个基于FastMCP的CSV到JSON转换MCP服务器，提供高效的CSV数据转换服务。

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
| 获取 CSV 文件的基本信息，用于辅助转换操作。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    
Returns:
    包含 CSV 文件信息的字典，结构为：
    {
        "success": bool,           # 操作是否成功
        "file_info": Dict[str, Any], # 文件详细信息
        "message": str            # 操作结果消息
    }
    
    文件信息包含以下字段：
    - file_size: 文件大小（字节）
    - row_count: 行数（估算值）
    - column_count: 列数
    - columns: 列名列表
    - sample_data: 示例数据（前几行）
    - file_encoding: 文件编码
    - detected_delimiter: 检测到的分隔符
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或读取失败时
    Exception: 其他未知错误 | `scripts.tools.get_csv_info` |
| 将 CSV 文件转换为 JSON 文件。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    output_file_path: 输出 JSON 文件路径（可选，默认为 CSV 文件同目录下同名 .json 文件）
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    encoding: 文件编码，默认为 utf-8，支持 gbk、gb2312 等常见编码
    skip_rows: 跳过的行数，默认为 0，用于跳过文件开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,      # 转换是否成功
        "json_file_path": str, # 生成的 JSON 文件路径
        "message": str       # 操作结果消息
    }
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或转换失败时
    Exception: 其他未知错误 | `scripts.tools.convert_csv_file` |
| 将 CSV 格式的字符串转换为 JSON 格式。

Args:
    csv_content: CSV 格式的字符串内容，必须包含有效的 CSV 数据
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    skip_rows: 跳过的行数，默认为 0，用于跳过字符串开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "index": 包含索引的字典
        - "table": 包含 schema 和数据的完整表格格式
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,  # 转换是否成功
        "json": Any,      # 转换后的 JSON 数据
        "message": str    # 操作结果消息
    }
    
Raises:
    ValueError: 当字符串格式错误或转换失败时
    Exception: 其他未知错误 | `scripts.tools.convert_csv_string` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_csv_info
工具描述：获取 CSV 文件的基本信息，用于辅助转换操作。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    
Returns:
    包含 CSV 文件信息的字典，结构为：
    {
        "success": bool,           # 操作是否成功
        "file_info": Dict[str, Any], # 文件详细信息
        "message": str            # 操作结果消息
    }
    
    文件信息包含以下字段：
    - file_size: 文件大小（字节）
    - row_count: 行数（估算值）
    - column_count: 列数
    - columns: 列名列表
    - sample_data: 示例数据（前几行）
    - file_encoding: 文件编码
    - detected_delimiter: 检测到的分隔符
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或读取失败时
    Exception: 其他未知错误
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|file_path|string|true| |null|

---

## scripts.tools.convert_csv_file
工具描述：将 CSV 文件转换为 JSON 文件。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    output_file_path: 输出 JSON 文件路径（可选，默认为 CSV 文件同目录下同名 .json 文件）
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    encoding: 文件编码，默认为 utf-8，支持 gbk、gb2312 等常见编码
    skip_rows: 跳过的行数，默认为 0，用于跳过文件开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,      # 转换是否成功
        "json_file_path": str, # 生成的 JSON 文件路径
        "message": str       # 操作结果消息
    }
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或转换失败时
    Exception: 其他未知错误
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|file_path|string|true| |null|
|output_file_path|null|false| |null|
|delimiter|string|false|","|null|
|encoding|string|false|"utf-8"|null|
|skip_rows|integer|false|0.0|null|
|header|boolean|false|true|null|
|orient|string|false|"records"|null|
|indent|null|false| |null|

---

## scripts.tools.convert_csv_string
工具描述：将 CSV 格式的字符串转换为 JSON 格式。

Args:
    csv_content: CSV 格式的字符串内容，必须包含有效的 CSV 数据
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    skip_rows: 跳过的行数，默认为 0，用于跳过字符串开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "index": 包含索引的字典
        - "table": 包含 schema 和数据的完整表格格式
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,  # 转换是否成功
        "json": Any,      # 转换后的 JSON 数据
        "message": str    # 操作结果消息
    }
    
Raises:
    ValueError: 当字符串格式错误或转换失败时
    Exception: 其他未知错误
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|csv_content|string|true| |null|
|delimiter|string|false|","|null|
|skip_rows|integer|false|0.0|null|
|header|boolean|false|true|null|
|orient|string|false|"records"|null|
|indent|null|false| |null|

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