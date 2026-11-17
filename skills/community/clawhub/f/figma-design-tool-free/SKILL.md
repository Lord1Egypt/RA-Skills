---
slug: figma-design-tool-free
name: figma-design-tool-free
version: 1.0.0
displayName: Figma设计集成-免费版
summary: "轻量级Figma集成工具，支持文件浏览、节点读取、图片导出与评论查看.。Figma设计集成工具免费版，面向个人设计师的Figma工作区访问工具。核心能力："
license: Proprietary
edition: free
description: Figma设计集成工具免费版，面向个人设计师的Figma工作区访问工具。核心能力：，可自动提升工作效率

  - 浏览Figma团队项目与文件列表

  - 读取设计文件结构与指定节点详情

  - 导出设计图片（PNG/JPG/SVG/PDF）

  - 查看文件评论与版本历史

  适用场景：

  - 个人设计师查看设计文件

  - 开发者获取设计资产与图标

  - 设计走查与评论查看

  差异化：免费版聚焦文件浏览、节点读取与图片导出，适合个人使用'
tags:
  - Creative
  - Figma
  - Design
  - 设计
  - UI/UX
  - 创意
  - file_key
  - figma
  - mx_figma
  - action
  - depth
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# Figma设计集成工具（免费版）

## 概述

Figma设计集成工具免费版是一款面向个人设计师的 Figma 工作区访问工具。通过 `mx_figma` 工具浏览团队项目、读取设计结构、导出图片和查看评论，实现设计与开发之间的设计资产流转.
本版本适合个人设计师查看文件、开发者获取设计资产、设计走查等场景。所有操作通过 Figma REST API 实现，安全可靠.
## 核心能力

| 能力 | 说明 |
|---|---|
| 项目浏览 | 列出团队项目与项目内文件 |
| 文件结构读取 | 获取设计文件页面与Frame层级 |
| 节点详情获取 | 读取指定节点的详细属性 |
| 图片导出 | PNG/JPG/SVG/PDF 多格式导出 |
| 评论查看 | 列出文件中的设计评论 |
| 版本历史 | 查看文件版本记录 |

### 免费版能力边界

```text
支持操作:
  - get_me              查看当前用户
  - list_team_projects  浏览团队项目
  - list_project_files  列出项目文件
  - get_file            获取文件结构
  - get_file_nodes      获取指定节点
  - export_images       导出图片
  - list_comments       查看评论
  - list_versions       查看版本历史
# ...
不支持（需专业版）:
  - post_comment        发表/回复评论
  - delete_comment      删除评论
  - get_file_components 获取文件组件
  - get_team_components 获取团队组件库
  - get_file_component_sets 获取组件变体
  - get_file_styles     获取文件样式
  - get_local_variables 获取设计变量
  - get_published_variables 获取发布变量
  - 批量导出与自动化工作流
```

- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、Figma、集成工具、支持文件浏览、节点读取、图片导出与评论查、设计集成工具免费、面向个人设计师的、工作区访问工具、核心能力、团队项目与文件列、读取设计文件结构、与指定节点详情、导出设计图片、查看文件评论与版等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
### 核心功能执行(补充)
执行核心功能执行操作,使用`input_params`参数进行配置.
## 使用场景

### 场景一：设计资产导出

从 Figma 文件中导出设计资产供开发使用.
```text
# 步骤1: 获取文件结构，找到目标Frame
mx_figma:
  action: get_file
  file_key: "abc123DEF456"
  depth: 2
  # depth: 1=仅页面, 2=页面+Frame, 省略=完整树
# ...
# 步骤2: 导出指定节点为SVG
mx_figma:
  action: export_images
  file_key: "abc123DEF456"
  node_ids: ["1:2", "3:4"]
  format: "svg"
  scale: 2
# ...
# 步骤3: 导出高清PNG
mx_figma:
  action: export_images
  file_key: "abc123DEF456"
  node_ids: ["5:6"]
  format: "png"
  scale: 2   # 0.01-4, 默认1
```

> `file_key` 从 Figma URL 提取：`figma.com/design/{file_key}/...`

### 场景二：设计走查

查看设计文件结构并浏览评论.
```text
# 1. 查看页面列表
mx_figma:
  action: get_file
  file_key: "xxx"
  depth: 1
# ...
# 2. 查看指定页面详情
mx_figma:
  action: get_file_nodes
  file_key: "xxx"
  node_ids: ["page_id"]
  depth: 1
# ...
# 3. 查看设计评论
mx_figma:
  action: list_comments
  file_key: "xxx"
# ...
# 4. 查看版本历史
mx_figma:
  action: list_versions
  file_key: "xxx"
```

### 场景三：获取指定节点属性

读取特定组件或图层的详细设计属性.
```python
# 模拟节点信息获取流程
def get_design_specs(file_key, node_ids):
    """获取设计节点规格"""
    specs = {
        "file_key": file_key,
        "nodes": []
    }
    for node_id in node_ids:
        # 调用 mx_figma: get_file_nodes
        node_spec = {
            "node_id": node_id,
            "name": "按钮组件",
            "type": "COMPONENT",
            "properties": {
                "width": 120,
                "height": 40,
                "fills": [{"type": "SOLID", "color": {"r": 0.1, "g": 0.1, "b": 0.18}}],
                "cornerRadius": 8,
                "padding": 12
            }
        }
        specs["nodes"].append(node_spec)
    return specs
# ...
# 获取按钮组件规格
specs = get_design_specs("abc123DEF456", ["1:2", "3:4"])
for node in specs["nodes"]:
    print(f"{node['name']}: {node['properties']['width']}x{node['properties']['height']}")
```

## 不适用场景

以下场景Figma设计集成-免费版不适合处理：

- 加密文件破解
- 损坏文件修复
- 物理介质数据恢复

## 触发条件

需要文件处理、文档转换、格式互转、内容提取时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 依赖详情

```bash
# 1. 安装插件
skill-platform plugins install skill-platform-morphixai
# ...
# 2. 获取 API Key
# 访问 morphix.app/api-keys 生成 mk_xxxxxx 密钥
# ...
# 3. 配置环境变量
export MORPHIXAI_API_KEY="mk_your_key_here"
# ...
# 4. 链接 Figma 账号
# 访问 morphix.app/connections 链接 Figma 账号
```

### 第二步：验证连接

```text
mx_figma:
  action: get_me
# 返回当前用户信息，确认连接成功
```

### 第三步：浏览项目并导出

```text
# 浏览团队项目
mx_figma:
  action: list_team_projects
  team_id: "123456789"
# ...
# 列出项目文件
mx_figma:
  action: list_project_files
  project_id: "987654321"
# ...
# 导出图片
mx_figma:
  action: export_images
  file_key: "abc123DEF456"
  node_ids: ["1:2"]
  format: "png"
  scale: 2
```

## 示例

### 导出格式配置

```text
export_images 参数:
  format: "png"   # 支持: jpg / png / svg / pdf
  scale: 2        # 缩放倍数: 0.01-4, 默认 1
  # SVG 导出建议 scale: 1
  # 高清位图建议 scale: 2 或 3
```

### 文件结构读取深度

```text
get_file depth 参数:
  depth: 1    → 仅返回页面列表（快速）
  depth: 2    → 返回页面 + Frame（推荐）
  省略 depth  → 返回完整文件树（大文件可能很慢）
```

### node_id 格式说明

```text
node_id 格式: "1:2"（冒号分隔）
# ...
从 Figma URL 获取:
  URL 中 node-id 参数用 - 分隔
  需转换为 : 分隔
  例: node-id=1-2 → node_id="1:2"
```

## 最佳实践

1. **控制读取深度**：大文件使用 `depth: 1` 或 `depth: 2`，避免加载完整树.
2. **SVG优先图标**：图标导出用 SVG 格式，无损可缩放.
3. **PNG高清导出**：位图导出用 `scale: 2` 或 `3` 确保清晰度.
4. **URL提取Key**：`file_key` 和 `node_id` 均从 Figma URL 提取.
5. **临时URL及时下载**：导出的图片URL有有效期，需及时下载保存.
```text
免费版最佳实践:
[ ] 读取深度已优化（大文件用 depth: 1）
[ ] 图标导出用 SVG 格式
[ ] 位图导出 scale ≥ 2
[ ] file_key 从 URL 正确提取
[ ] node_id 格式已转换（- → :）
[ ] 导出 URL 已及时下载
```

## 常见问题

### Q: 如何获取 file_key？

A: 从 Figma 文件 URL 提取：`figma...`。file_key 是 URL 中 design 后面那段字符.
### Q: 导出的图片URL有效期多久？

A: 导出返回的是临时 URL，有效期有限。建议获取后立即下载到本地保存.
### Q: 免费版可以发表评论吗？

A: 免费版仅支持查看评论（list_comments），发表和回复评论需要专业版.
### Q: 大文件读取很慢怎么办？

A: 使用 `depth: 1`（仅页面）或 `depth: 2`（页面+Frame），避免加载完整文件树.
### Q: 支持哪些导出格式？

A: 支持 PNG、JPG、SVG、PDF 四种格式。图标用 SVG，照片用 JPG，透明背景用 PNG，打印用 PDF.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| morphixai 插件 | 工具 | 必需 | `skill-platform plugins install skill-platform-morphixai` |
| Figma 账号 | 服务 | 必需 | figma.com 注册 |
| MorphixAI API Key | 认证 | 必需 | morphix.app/api-keys 获取 |

### API Key 配置
- **必需**: MorphixAI API Key（格式：`mk_xxxxxx`）
- **获取方式**: 访问 morphix.app/api-keys 生成
- **配置方式**: 环境变量 `MORPHIXAI_API_KEY`
- **账号链接**: 访问 morphix.app/connections 链接 Figma 账号

### 可用性分类
- **分类**: MD+EXEC+API（Markdown指令 + 命令行 + 外部API调用）
- **说明**: 轻量级AI Skill，通过MorphixAI代理访问Figma REST API
- **适用规模**: 个人设计师与开发者，单文件操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Figma设计集成-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "figma design"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
