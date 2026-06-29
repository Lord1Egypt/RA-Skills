---
name: drawiodo
author: wUwproject
license: MIT
version: 2.6.1
description: draw.io 自动做图 Skill。当用户要求画图、生成图表、做架构图、流程图、UML、ER 图、时序图、思维导图等时触发。生成 .drawio 文件并用 draw.io 打开。支持思考-确认-迭代-版本回溯的完整工作流，8 个 Hook Point 安全校验。
tags: ['diagram', 'drawio', 'flowchart', 'architecture', 'uml', 'er', 'visualization']
allowed-tools: ['Bash', 'Read', 'Write', 'Edit']
trigger: ['画一个.*图|生成.*图|做一个图表', '架构图|流程图|UML|ER图|时序图|思维导图', 'draw\\\\\\\\.io|drawio|diagrams\\\\\\\\.net', '网络拓扑|组织架构|系统架构']
trigger_negative: true
sensitive_access: true
critical_write: false
permission_weight: HIGH
data_dir: skills/.standardization/drawiodo/data/
external_data_dir: true
meta_field_sync: true
faq_quality: improve_qa
---
# drawiodo: draw.io 自动做图 Skill

## 触发条件

**正向触发**：
当用户提出以下意图时触发：
- "画一个 xxx 图"、"生成 xxx 图"、"做一个图表"
- "架构图"、"流程图"、"UML 类图"、"ER 图"、"时序图"、"思维导图"
- "用 draw.io 画"、"生成 drawio 文件"
- "画网络拓扑"、"画组织架构"、"画系统架构"
- "按照这个示例改成..."、"参照这个图改..."、"基于这个样式做一个..."
- 用户提供截图/示例文件并要求生成类似图表
- 任何涉及 draw.io / diagrams.net 的需求

**否定条件**：
以下情况**不触发**本技能：
- 用户只是问"你会画图吗"、"有什么画图工具"——闲聊
- 用户明确要求用其他工具（如"用 mermaid 画流程图"）
- 用户只是提到"图"字但没有画图意图（如"这个图怎么读"）
- 用户要求编辑已有的图片文件（如 .png/.jpg）——本技能生成的是 .drawio 文件

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

1. **自然语言 → 图表**：理解用户描述，自动判断图表类型，生成 .drawio 文件
2. **统一布局引擎**：拓扑排序分层 → 重心排序层内排列 → 动态间距计算 → 障碍感知路径路由，不区分图类型
3. **多形状支持**：UML 类表、ER 实体、圆柱体、菱形、六边形、云朵、文档、便签等，用户指定即可
4. **5 主题配色**：default/tech/business/bw/nature，节点和边颜色统一轮换
5. **迭代更新**：在现有文件基础上精确更新，支持版本回溯（最多 5 版本）
6. **思考-确认-执行工作流**：先分析需求、展示方案、等待确认，再动手画图
7. **本地预览**：生成后用 `draw.io.exe` 打开，即时查看结果

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
|--------|------|----------|----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/api_reference.md` | 参考文档 | - `DrawIOBuilder(name)` - 创建画布 | 无 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、变更类型、修复项、升级说明。 | R-24 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/generation.md` | 参考文档 | 路径信息见 `_meta.json` data_dir 声明 + frontmatter data_dir 字段。 | 无 |
| `references/guide.md` | 使用指南 | 三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。 | 无 |
| `references/hooks.md` | 参考文档 | **本技能的所有关键约束由 Python 端强制执行，不依赖 LLM 自觉。** | 无 |
| `references/known_issues.md` | 参考文档 | **问题**：子节点使用极坐标计算位置，导致： | 无 |
| `references/layout_rules.md` | 参考文档 | - 画布坐标：左上角(0,0)，X向右增大，Y向下增大 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/test-report.md` | 测试报告 | skill-function-test 全量测试结论 | 无 |
| --- | --- | --- | --- |
| `scripts/drawio_unified.py` | 核心引擎 | 统一图生成：拓扑分层 → 重心排序 → 位置计算 → 路由 | 无 |
| `scripts/drawio_module.py` | 模块基类 | DiagramModule 抽象接口 + LayoutResult + 渲染层 | 无 |
| `scripts/drawio_modules.py` | 模块注册 | GraphModule / GanttModule 注册表 | 无 |
| `scripts/drawio_gen.py` | XML 生成 | Node / Edge / DrawIOBuilder + build_xml() | 无 |
| `scripts/drawio_route.py` | 路径路由 | Rect / CollisionResolver / ObstacleRouter | 无 |
| `scripts/drawio_layout.py` | 布局辅助 | text_width / auto_node_size / 间距常量 | 无 |
| `scripts/drawio_hooks.py` | 钩子系统 | 8 个 Hook Point 实现 | 无 |
| `scripts/drawio_version.py` | 版本管理 | VersionManager CLI：init/save/list/restore/diff | 无 |
| `scripts/drawio.py` | CLI 入口 | 模板式图表生成 CLI（流程图/架构图/类图/ER/树/思维导图） | 无 |
| `scripts/drawio_agent.py` | CLI 入口 | 自然语言驱动的图表生成 CLI（`--json` 接收结构化数据） | 无 |
| `scripts/drawio_regen_all.py` | 批量生成 | 一次性生成全部示例图的脚本 | 无 |
| `scripts/drawio_templates.py` | 模板生成 | 旧版按图类型生成模板（flowchart/architecture/class/er/tree/mindmap） | 无 |
| `scripts/build_network.py` | 网络构建 | 网络拓扑图专用构建函数 | 无 |
## 工作流程

1. **思考分析（Think）**
   - **输入**：用户自然语言描述 + 可选的参考图/截图
   - **输出**：结构化图表分析结果（类型、节点、关系、布局）
2. **方案确认（Confirm）**
   - **输入**：结构化分析结果
   - **输出**：用 AskUserQuestion 向用户展示方案，等待确认
3. **迭代更新（Iterate）**
   - **输入**：用户确认的方案
   - **输出**：生成的 .drawio 文件，每次更新前自动保存版本
4. **版本回溯（Version Control）**
   - **输入**：已保存的历史版本（v1~v5）
   - **输出**：恢复指定版本的文件

→ 各阶段详细说明见核心能力的渐进式文件索引

**各阶段要点**：
- **Think**：分析用户需求，判断图表类型和输入类型，输出结构化思考结果 
- **Confirm**：向用户展示方案，用 AskUserQuestion 等待确认（必须确认后才能动手）
- **Iterate**：在现有文件基础上精确更新，每次更新前保存版本（v1→v2→v3...）
- **Version Control**：最多保留 5 个版本，支持随时回溯 

**快捷模式**（可跳过确认）：
- 简单流程图（3-5 个步骤的线性流程）
- 明确的模板调用（用户给出完整的 JSON spec）
- 已确认方案后的迭代更新 

**版本管理命令**：
```bash
python {SKILL_DIR}/scripts/drawio_version.py init <文件.drawio> "初始版本"
python {SKILL_DIR}/scripts/drawio_version.py save <文件.drawio> "更新了 XX"
python {SKILL_DIR}/scripts/drawio_version.py list <文件.drawio>
python {SKILL_DIR}/scripts/drawio_version.py restore <文件.drawio> v2
```

## 钩子系统（强制约束）

**关键操作由 Python 端自动执行，不依赖 LLM 自觉。**
备份、版本管理初始化、版本上限清理均由钩子在脚本层直接完成，
LLM 无权跳过这些操作。

→ 各参考文档详见核心能力的渐进式文件索引

### 8 个 Hook Point

| Hook Point | 强制操作 | 说明 |
|---|---|---|
| `pre_think` | 输入非空校验（阻断） | 空输入直接阻断 |
| `post_think` | 分析结果校验 | 缺失字段仅警告 |
| `pre_confirm` | 选项完整性校验（阻断）+ 快捷跳过（清除选项） | 不足 2 项或快捷跳转均阻断/跳过 |
| `post_confirm` | 用户选择解析 | - |
| `pre_iterate` | 自动创建目录 + **自动备份** | 备份由 Python 调用 VersionManager |
| `post_iterate` | 输出校验 + **自动初始化版本管理** + **自动打开预览** | init 和预览都由 Python 执行 |
| `pre_vc` | **自动清理超限版本** | 删除最旧版本由 Python 执行 |
| `post_vc` | 版本状态报告 | - |

### 执行规则

- **abort=True** -> 立即阻断流程（LLM 无权绕过）
- **success=False 但不 abort** -> 记录警告，不阻塞
- 所有操作由 Python 端算法强制完成

### 在阶段代码中调用

```python
from drawio_hooks import hooks

# 在阶段开始时
results = hooks('pre_iterate', {
    'output_path': output_path,
    'is_update': True,          # 会触发自动备份
})
for r in results:
    if r.abort:
        return  # 钩子已处理，阻断并返回
    if not r.success:
        print(f'Warning: {r.message}')

# 在阶段结束时
results = hooks('post_iterate', {
    'output_path': output_path,  # 会触发自动 init 版本管理
})
```

### 注册/注销自定义钩子

```python
from drawio_hooks import register, unregister

@register('pre_think', name='my_check', description='自定义校验')
def my_hook(ctx):
    if 'special' not in ctx.get('user_input', ''):
        return {'success': False, 'message': '缺少特殊参数', 'abort': True}
    return {'success': True, 'message': 'ok'}

unregister('post_iterate', 'preview_trigger')  # 禁用自动预览
```

### CLI 管理命令

```bash
python {SKILL_DIR}/scripts/drawio_hooks.py list     # 查看所有注册钩子
python {SKILL_DIR}/scripts/drawio_hooks.py check    # 全流程自检
python {SKILL_DIR}/scripts/drawio_hooks.py history  # 查看执行历史
```

---

## 生成图表

→ 详见核心能力的渐进式文件索引

---

## API 参考

→ 详见核心能力的渐进式文件索引

## 坐标系与布局规则

→ 详见核心能力的渐进式文件索引

## 已知问题与修复记录

→ 详见核心能力的渐进式文件索引

→ 反模式和常见问题详见核心能力的渐进式文件索引

---
## 输出规范 

- 文件命名：`{类型}_{描述}.drawio`，如 `architecture_microservice.drawio`
- 生成后自动用 draw.io 打开预览 
- 交付附件给用户 
- 每次生成/更新后初始化或更新版本管理 
- 路径信息见 `_meta.json` data_dir 声明 + frontmatter data_dir 字段

## 核心文件 

| 文件 | 路径 | 说明 |
|------|------|------|
| 核心库 | `scripts/drawio_gen.py` | 节点/连线/容器/XML 生成 |
| 模板库 | `scripts/drawio_templates.py` | 8 种图表模板 |
| Agent 入口 | `scripts/drawio_agent.py` | CLI/自然语言解析 |
| 版本管理 | `scripts/drawio_version.py` | 5 版本回溯系统 |

## 使用示例

### 场景 1：生成架构图
```text
用户：帮我画一个微服务架构图，包含 API 网关、用户服务、订单服务和数据库
drawiodo：正在分析需求 → 判断为"架构图" → 输出方案：4 个容器+连线+数据库图标
用户确认后 → 生成 architecture_microservice.drawio → 自动打开预览
```

### 场景 2：迭代更新
```text
用户：在上次的系统架构图里加一个消息队列，在订单服务和用户服务之间
drawiodo：读取已存在的文件 → 自动备份(v2) → 在订单服务和用户服务之间插入消息队列节点和连线
→ 更新文件 → 自动打开预览展示变化
```
