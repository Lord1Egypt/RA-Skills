# Architecture Diagram Generator — Design Document (v2)

## Context

当前 `export_svg.py` 包含复杂的自动布局引擎（`_layout_free_flow`、`_content_router`、`_render_free_flow_svg`），产出却是网格堆叠的卡片，不是真正的架构图。更关键的是：**Python 代码太重，沙箱频繁出问题**——依赖链长、`importlib.metadata` 不稳定、`__file__` 在 Jupyter 中未定义。

参考项目 [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) 走了完全不同的路：**SKILL.md 定义设计系统，Claude 按规则直接生成 HTML+SVG，零 Python 依赖。**

本文档设计 v2 重构方案：**核心架构图生成完全脱离 Python，由 Claude 读取 SKILL.md → 直接输出 HTML+SVG。Python 只做 JSON 校验和格式转换（draw.io/excalidraw/mermaid）。**

## 核心决策

### 1. Python 轻量化

| 当前 | v2 |
|------|-----|
| `export_svg.py` 1500+ 行布局引擎 | 保留 300 行核心常量，移除自动布局 |
| `export_html.py` 200+ 行内嵌 SVG 构建 | 改为直接输出预生成的 SVG |
| `--export` 默认调 9 个 Python 函数 | Claude 生成 HTML+SVG（主），Python 格式转换（备） |
| 依赖 `importlib.metadata`、`math`、`pathlib` | 只依赖 `json`、`pathlib`（stdlib） |
| 沙箱需 `pip install kai-business-blueprint` | 沙箱只需 `json.load()` + 写文件，或 Claude 直接生成 |

### 2. Claude 生成架构图的具体机制

不是"Claude 在对话中手写 SVG"，而是：

```
1. Claude 读取 blueprint JSON（或用户自然语言描述）
2. Claude 读取 SKILL.md 中的设计系统规范
3. Claude 生成 HTML+SVG 文本 → 写入文件
4. 输出：单个 .html 文件
```

**在沙箱环境中**，不需要 `pip install`：
```python
# 沙箱只需这两行——无第三方依赖
import json
blueprint = json.load(open("solution.blueprint.json"))
# 然后 Claude 根据 blueprint 数据直接生成 HTML+SVG 字符串并写入文件
```

**Python 脚本完全退出架构图渲染**——它只做：
- `--plan`：将用户需求写入 blueprint JSON
- `--validate`：校验 blueprint 结构
- `--format drawio/excalidraw/mermaid`：从 blueprint 生成对应格式（这些格式有成熟的 Python 库/字符串拼接即可）

### 3. Blueprint Schema 适配

当前 schema **已有足够字段**，不需要扩展：

| 设计系统概念 | Blueprint 字段 | 映射方式 |
|------------|---------------|---------|
| 组件类型/颜色 | `systems[].category` | frontend/backend/database/cloud/security/external |
| L→R 数据流 | `flowSteps[].seqIndex` + `nextStepIds` | 按 seqIndex 排序，L→R 排列 |
| Region 边界 | `systems[].properties.type` | `type == "aws"` → 包在 AWS Region 框内 |
| 消息总线 | `systems[].properties.service == "sqs"` 等 | SQS/EventBridge/SNS → MessageBus 颜色 |
| 组件副标题 | `systems[].description` 或 `properties.features` | 取前 2-3 个特征 |
| 组件大小 | 根据 `capabilities` 数量决定 | 0-1 cap → 小框(60px)，2-4 → 中框(80px)，5+ → 大框(120px) |

**不需要新增字段。** 所有视觉决策都从现有字段推导。

## 设计系统（从参考项目继承）

### 颜色 Palette

| 类型 | 填充色 | 边框色 | 用途 |
|------|--------|--------|------|
| Frontend | `rgba(8,51,68,0.4)` | `#22d3ee` | Web、移动端、UI |
| Backend | `rgba(6,78,59,0.4)` | `#34d399` | Lambda、API Gateway、服务 |
| Database | `rgba(76,29,149,0.4)` | `#a78bfa` | DynamoDB、RDS、S3 |
| AWS/Cloud | `rgba(120,53,15,0.3)` | `#fbbf24` | Region 框、CloudFront |
| Security | `rgba(136,19,55,0.4)` | `#fb7185` | Security Group、WAF |
| MessageBus | `rgba(251,146,60,0.3)` | `#fb923c` | SQS、SNS、EventBridge |
| External | `rgba(30,41,59,0.5)` | `#94a3b8` | 第三方 API、SaaS |

### 字体
- JetBrains Mono（Google Fonts CDN）
- 组件名：14px / 600
- 副标签：11px / 400
- 注解：9px
- Region 标签：10px / 600

### 布局规则
- L→R 数据流：Clients(左) → Frontend → Backend → Database(右)
- Region 虚线框：`rx="12"`, `stroke-dasharray="8,4"`, 琥珀色
- 组件圆角：`rx="6"`, 1.5px 描边
- Z 序：箭头 → 节点遮罩 → 节点样式 → 文字 → Legend

## SKILL.md 结构

遵循**渐进披露**原则，SKILL.md 本身不塞设计系统细节：

```
SKILL.md（路由层，<100行）
  ├── 何时触发架构生成（关键词：architecture diagram, 架构图, --export）
  ├── 读取 references/architecture-design-system.md（完整设计系统）
  ├── 读取 references/architecture-templates/serverless.md（模板）
  └── Claude 生成 HTML+SVG → 写入文件

references/architecture-design-system.md（设计系统，~80行）
  ├── 颜色 Palette
  ├── 字体与间距
  ├── 视觉元素（Region框、组件框、箭头）
  └── Z 序规则

references/architecture-templates/（模板库）
  ├── serverless.md（AWS Serverless 模板）
  ├── microservices.md（微服务模板）
  └── three-tier.md（三层架构模板）
```

## Python 代码改动

### 删除（~900 行）

| 文件 | 删除内容 |
|------|---------|
| `export_svg.py` | `_content_router()`、`_layout_free_flow()`、`_render_free_flow_svg()`、`export_svg_auto()` |
| `export_html.py` | `_build_architecture_svg()` 整个函数 |

### 保留（~600 行）

| 文件 | 保留内容 |
|------|---------|
| `export_svg.py` | 设计常量（`C_LIGHT`、`C_DARK`、字体、尺寸）、箭头/节点渲染函数、`export_svg()` 三层布局（回退用）、`export_*_svg()` 专业视图 |
| `export_drawio.py` | 完整保留 |
| `export_excalidraw.py` | 完整保留 |
| `export_mermaid.py` | 完整保留 |
| `cli.py` | 简化：`--export` 默认触发 Claude 生成（见下），`--format drawio/excalidraw/mermaid/all` 调 Python |

### `cli.py` 中 `--export` 新逻辑

**关键设计：** `--export` 既要保证向后兼容（Python 产出基础文件），也要让 Agent 有机会生成增强版架构图。

```python
if args.export:
    blueprint_path = Path(args.export)
    blueprint = load_json(blueprint_path)
    stem = blueprint_path.stem
    export_dir = blueprint_path.parent / f"{stem}.exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    fmt = args.export_format or "svg"
    
    if fmt == "svg":
        # Python 产出经典三层布局 SVG（向后兼容，确保有文件产出）
        export_svg(blueprint, export_dir / "solution.svg", theme=args.theme)
        # Agent 在沙箱外读取 blueprint → 按 SKILL.md 生成增强版 HTML+SVG
        # 这是 Agent 的下一步动作，不在 CLI 中执行
        return 0
    
    elif fmt == "drawio":
        export_drawio(blueprint, export_dir / "solution.drawio")
    elif fmt == "excalidraw":
        export_excalidraw(blueprint, export_dir / "solution.excalidraw")
    elif fmt == "mermaid":
        export_mermaid(blueprint, export_dir / "solution.mermaid.md")
    elif fmt == "all":
        # Python 产出所有格式（向后兼容）
        export_svg(blueprint, export_dir / "solution.svg", theme=args.theme)
        export_capability_map_svg(blueprint, export_dir / "capability-map.svg", theme=args.theme)
        export_swimlane_flow_svg(blueprint, export_dir / "swimlane-flow.svg", theme=args.theme)
        export_product_tree_svg(blueprint, export_dir / "product-tree.svg", theme=args.theme)
        export_matrix_svg(blueprint, export_dir / "capability-matrix.svg", theme=args.theme)
        export_drawio(blueprint, export_dir / "solution.drawio")
        export_excalidraw(blueprint, export_dir / "solution.excalidraw")
        export_mermaid(blueprint, export_dir / "solution.mermaid.md")
        # Agent 可在此基础上额外生成增强版架构图 HTML
        return 0
```

**Agent 的增强流程（CLI 之外）：**
1. `--export` 完成后，Agent 读取 blueprint JSON
2. Agent 按 SKILL.md 设计系统规范生成架构图 HTML+SVG
3. 写入 `{stem}.html` 到同目录

### 沙箱兼容

沙箱不是独立运行的——调用链是 `用户 → Agent(Claude/OpenAI/GLM) → tool call → 沙箱执行Python`。

沙箱中 Agent 始终可用，所以架构生成流程是：
1. Agent 在沙箱中 `json.load()` 读取 blueprint
2. Agent 读取 SKILL.md 设计系统规范
3. Agent 生成 HTML+SVG 字符串 → 通过沙箱 `write_file` 或 `Path.write_text()` 写入
4. 返回给用户

沙箱不再需要 `pip install kai-business-blueprint`：
```python
# 极简沙箱用法——只需 stdlib
import json
from pathlib import Path

blueprint = json.loads(Path("solution.blueprint.json").read_text())
# Agent 根据 blueprint 数据 + SKILL.md 设计系统，直接生成 HTML+SVG 并写入文件
```

**Python 脚本在沙箱中的角色：JSON 加载 + 校验。** 架构图渲染完全由 Agent 承担。

## 回退策略

由于调用链中 Agent 始终存在（Agent → tool call → 沙箱 → Agent 继续），**不存在"无 Agent 可用"的回退场景**。但保留以下回退以防代码层面断裂：

1. **`--export` 时 Python 仍产出 `solution.svg`（三层布局经典版）** — 确保 `--format all` 向后兼容
2. **`export_html.py` 不再自己构建 SVG** — 改为接受预生成的 SVG 内容参数

三个保障：
- `--export` 至少产出 `solution.svg`（Python 经典布局）
- Agent 可在此基础上额外生成 HTML+SVG 架构图
- `drawio/excalidraw/mermaid` 格式由 Python 稳定产出

## 实施阶段

| 阶段 | 内容 | 可回滚？ |
|------|------|---------|
| **Phase 1** | 写 `references/architecture-design-system.md` + 模板 | ✅ 只加文件 |
| **Phase 2** | 更新 SKILL.md 添加架构图生成路由 | ✅ 只改 SKILL.md |
| **Phase 3** | 删除 `_content_router`、`_layout_free_flow`、`_render_free_flow_svg` | ⚠️ 需确认无外部依赖 |
| **Phase 4** | 简化 `cli.py` 和 `export_html.py` | ⚠️ 需测试沙箱兼容 |
| **Phase 5** | 测试 `aws-serverless.blueprint.json` 生成效果 | — |

## 评审问题应对

| Codex 评审问题 | 应对 |
|---------------|------|
| `export_html.py` 导入断裂 | **`export_html.py` 的 `_build_architecture_svg()` 不再自己构建 SVG**，改为接受预生成的 SVG 字符串参数，或回退到三层布局。删除对 `_content_router`、`_layout_free_flow`、`_render_free_flow_svg` 的 import |
| "CLI plans, Claude generates" 无明确机制 | **CLI 产出基础文件（Python 经典布局），Agent 在此基础上生成增强版**。CLI 不返回 0 空文件 |
| 非交互环境无 Claude | **调用链始终是 Agent → tool call → 沙箱 → Agent**。不存在离线调用场景 |
| Blueprint 字段不够 | 所有视觉决策从现有字段推导，不需新增 schema |
| SKILL.md 膨胀 | 设计系统放 `references/`，SKILL.md 只引用 |
| `--format all` 其他导出 | **保留所有 Python SVG 导出器在 `--format all` 中**，确保向后兼容 |
| 测试文件断裂 | Phase 3 删除 `test_content_router_and_layout.py` 或重写 |
