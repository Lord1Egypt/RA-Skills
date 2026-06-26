# API 列表解析脚本使用说明

## 脚本功能

`parse_api_list.py` 脚本用于自动从 302.AI 获取最新的 API 列表并进行解析和搜索。

## 主要功能

1. **自动获取最新 API 列表**: 从 https://doc.302.ai/llms.txt 自动下载最新列表
2. **解析 API 信息**: 提取所有 API 的名称、分类、文档链接和描述
3. **关键词搜索**: 在 API 名称和描述中搜索关键词
4. **分类筛选**: 按分类路径筛选 API
5. **提取文档 ID**: 从文档链接中提取文档 ID，方便后续获取详细文档

## 使用方法

### 基本用法

```bash
# 列出前 20 个 API
python3 scripts/parse_api_list.py

# 按关键词搜索
python3 scripts/parse_api_list.py GPT

# 按分类搜索
python3 scripts/parse_api_list.py "" 图片生成

# 组合搜索（关键词 + 分类）
python3 scripts/parse_api_list.py 聊天 语言大模型

# 搜索特定模型
python3 scripts/parse_api_list.py nano-banana

# 显示帮助
python3 scripts/parse_api_list.py --help
```

### 在代码中使用

```python
from scripts.parse_api_list import fetch_llms_txt, parse_llms_txt, search_apis, extract_doc_id

# 自动获取最新 API 列表
content = fetch_llms_txt()

# 解析所有 API
apis = parse_llms_txt(content)
print(f"总共 {len(apis)} 个 API")

# 搜索 GPT 相关的 API
gpt_apis = search_apis(apis, keyword='GPT')
for api in gpt_apis:
    print(f"{api['name']}: {api['link']}")

# 搜索图片生成分类的 API
image_apis = search_apis(apis, category='图片生成')
for api in image_apis:
    doc_id = extract_doc_id(api['link'])
    print(f"{api['name']} - 文档ID: {doc_id}")
```

## 输出格式

脚本输出格式化的 API 信息：

```
正在从 302.AI 获取最新 API 列表...
✓ 获取成功

总共找到 1486 个 API

搜索结果：7 个匹配的 API

1. **OpenAI Chat（聊天）**
   - 分类：语言大模型 > OpenAI
   - 描述：支持 GPT-4、GPT-3.5 等模型的聊天接口
   - 文档：https://doc.302.ai/147522039e0.md
   - 文档ID：147522039e0
```

## 核心函数说明

### fetch_llms_txt(url=LLMS_TXT_URL)

自动从 302.AI 获取最新的 API 列表。

**参数**:
- `url`: llms.txt 的 URL（默认使用官方地址）

**返回**:
- llms.txt 文件内容（字符串）

**异常**:
- `Exception`: 如果请求失败

### parse_llms_txt(content: str)

解析 llms.txt 内容，返回 API 列表。

**参数**:
- `content`: llms.txt 文件内容

**返回**:
- API 列表，每个元素包含：
  - `category`: 分类路径
  - `name`: API 名称
  - `link`: 文档链接
  - `description`: API 描述

### search_apis(apis, keyword=None, category=None)

搜索 API。

**参数**:
- `apis`: API 列表
- `keyword`: 关键词（可选）
- `category`: 分类关键词（可选）

**返回**:
- 匹配的 API 列表

### extract_doc_id(link: str)

从文档链接中提取文档 ID。

**参数**:
- `link`: 文档链接

**返回**:
- 文档 ID 字符串

## 在 Skill 中的使用

在 302.AI API 集成助手 Skill 中，使用此脚本来：

1. **自动获取最新列表**: 无需手动下载 llms.txt，减少上下文占用
2. **快速定位 API**: 根据用户需求搜索相关 API
3. **提取文档链接**: 获取 API 的详细文档链接
4. **分类浏览**: 按分类查看所有可用 API

### 工作流程

```
用户需求 → 调用脚本搜索 API → 展示给用户选择 → 提取文档 ID → 使用 WebFetch 获取详细文档
```

## 示例场景

### 场景 1：用户想使用 GPT-4

```python
# 自动获取并搜索 GPT 相关 API
content = fetch_llms_txt()
apis = parse_llms_txt(content)
gpt_apis = search_apis(apis, keyword='GPT', category='语言大模型')

# 展示给用户选择
for i, api in enumerate(gpt_apis, 1):
    print(format_api_info(api, i))
```

### 场景 2：用户需要图片生成功能

```python
# 搜索图片生成 API
content = fetch_llms_txt()
apis = parse_llms_txt(content)
image_apis = search_apis(apis, category='图片生成')

# 展示给用户选择
for i, api in enumerate(image_apis, 1):
    print(format_api_info(api, i))
```

### 场景 3：用户选择了某个 API，需要获取详细文档

```python
# 用户选择了第 1 个 API
selected_api = gpt_apis[0]

# 提取文档 ID
doc_id = extract_doc_id(selected_api['link'])

# 使用 WebFetch 获取详细文档
# WebFetch(url=selected_api['link'], prompt="提取 API 详细信息")
```

## 优势

1. **自动更新**: 每次运行都获取最新的 API 列表
2. **减少上下文**: 不需要在 Skill 中加载完整的 llms.txt 内容
3. **快速搜索**: 支持关键词和分类的组合搜索
4. **易于集成**: 可以作为 Python 模块导入使用

## 注意事项

1. **网络连接**: 需要能够访问 https://doc.302.ai/llms.txt
2. **依赖库**: 需要安装 `requests` 库（`pip install requests`）
3. **超时设置**: 默认请求超时为 30 秒
4. **编码**: 使用 UTF-8 编码处理中文内容
5. **性能**: 解析速度很快，即使有 1000+ 个 API 也能快速完成
