---
name: agentarts-skill-factory
description: 华为云 AgentArts 工作流快速封装工厂。提供一条命令将新的 AgentArts 工作流（含网关地址、路径、版本、鉴权等）自动生成为标准 Skill 目录（SKILL.md + invoke_agentarts.py），无需手写模板代码。
version: 1.0.0
author: plovjet
model: claude-sonnet-4-6
triggers:
  - 封装AgentArts工作流
  - 新建AgentArts技能
  - 生成AgentArts Skill
  - agentarts工厂
  - agentarts-skill-factory
metadata:
  openclaw:
    emoji: "🏭"
    requires:
      bins: [python3, python]
      env: [AGENTARTS_API_KEY]
    os: [linux, darwin, win32]
    homepage: https://github.com/plovjet/agentArts-to-officeAce
---

# AgentArts Skill Factory

将华为云 AgentArts 工作流快速封装为标准 Skill 的元技能。

## 适用场景

- 你有一个新的 AgentArts 工作流（已部署、有网关地址），想快速封装成 Skill
- 你想批量生成多个 AgentArts 工作流对应的 Skill
- 你想基于已有工作流参数，快速产出 SKILL.md + invoke_agentarts.py

## 步骤

### 步骤 1：收集工作流参数

向用户收集以下必要参数（可通过对话逐项确认，也可让用户一次性提供 JSON）：

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `name` | 是 | 技能名称，英文，短横线分隔 | `Huawei-quality-check` |
| `description` | 是 | 技能一句话描述 | `面向质检员的华为云 AgentArts 质检工作流调用技能` |
| `triggers` | 是 | 触发词列表，至少 2 个 | `["帮我做质检", "质检分析", "quality-check"]` |
| `user_identity` | 否 | 目标用户身份 | `车间质检员` |
| `greeting` | 否 | 固定开场白 | `你好，我是你的质检助理` |
| `base_url` | 是 | AgentArts 网关地址 | `https://defaultgw-mvstsmzsgv.cn-southwest-2.huaweicloud-agentarts.com` |
| `path` | 是 | API 调用路径 | `/runtimes/jiuwen-abc123/invocations` |
| `api_key` | 是 | Bearer Token | `9a39833a9c3042798e8758de3b940693` |
| `session_id` | 否 | 默认会话 ID，不填则自动生成 | `cd504243-6bb6-4c69-a835-b22cbf94c993` |
| `behavior_first_call` | 否 | 首次调用行为规则，默认只返回结果 | 见下方默认值 |
| `output_dir` | 否 | 生成目录，默认为当前工作目录下以 name 命名 | |

**默认行为规则（behavior_first_call）**：

```
- 只输出云端工作流返回的结果
- 不自动执行后续分析
- 不自动生成报告或 PPT
- 提示用户可以继续追问更详细内容
```

### 步骤 2：确认参数

将收集到的参数整理为表格展示给用户，等待用户确认。如有遗漏或格式问题，提示修正。

### 步骤 3：调用生成脚本

使用 `bash` 工具执行生成命令：

```bash
python scripts/main.py --name "Huawei-quality-check" --description "..." --triggers "帮我做质检,质检分析" --base-url "https://..." --path "/runtimes/..." --api-key "9a39..."
```

或通过 JSON 配置文件：

```bash
python scripts/main.py --config config.json --output-dir ./output
```

也可以在 Python 中直接调用：

```python
import sys
sys.path.insert(0, "scripts目录路径")
from main import generate_skill

config = {
    "name": "Huawei-quality-check",
    "description": "...",
    "triggers": ["帮我做质检", "质检分析"],
    # ... 其他参数
}
generate_skill(config, output_dir="目标目录")
```

### 步骤 4：验证生成结果

检查生成的目录结构：

```
<name>/
├── SKILL.md
└── scripts/
    └── invoke_agentarts.py
```

确认：
- SKILL.md 的 frontmatter（name / description / triggers）正确
- invoke_agentarts.py 的配置项（DEFAULT_BASE_URL / DEFAULT_PATH / DEFAULT_VERSION / DEFAULT_AGENTARTS_API_KEY）正确
- 脚本语法无误：`python -c "import ast; ast.parse(open('scripts/invoke_agentarts.py').read())"`

### 步骤 5：交付

将生成的技能目录路径告知用户，并提示：

1. 技能已生成，重启服务或刷新技能列表后即可使用
2. 可用 Skill 工具验证加载
3. 如需调整触发词或行为规则，直接编辑 SKILL.md 即可

## 注意事项

- `api_key` 是敏感信息，生成后提醒用户妥善保管，强烈建议通过环境变量 `AGENTARTS_API_KEY` 覆盖
- `path` 格式注意区分 `/agent/` 和 `/runtimes/` 两种前缀，取决于 AgentArts 工作流类型
- 生成的 invoke_agentarts.py 包含三层请求降级（requests → urllib → IP直连），无需额外安装依赖
- 如需自定义 `resolve_query` 中的指令映射逻辑，生成后手动编辑 invoke_agentarts.py 的对应函数
