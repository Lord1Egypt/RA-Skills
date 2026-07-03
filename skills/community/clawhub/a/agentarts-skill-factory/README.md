# AgentArts Skill Factory

将华为云 **AgentArts** 工作流快速封装为标准 Skill 的元技能（工厂技能）。生成的 Skill 可安装到 **OfficeAce** 中，让用户通过自然语言直接调用部署在华为云上的 AgentArts 智能体运行时。

## 一句话说明

> 一条命令，把 AgentArts 工作流（网关地址 + 路径 + 版本 + 鉴权）自动生成为标准 Skill 目录，无需手写模板代码。

## 目录结构

```
agentArts-to-officeAce/
├── SKILL.md              # 工厂技能的元定义（触发词、行为规则、使用步骤）
└── scripts/
    └── main.py           # 生成器脚本（含 SKILL.md 模板 + invoke_agentarts.py 模板 + 生成逻辑）
```

## 快速开始

### 1. 安装工厂技能

将本项目作为 skill 安装到 Claude Code。

### 2. 触发工厂

使用以下任意触发词：

- "封装AgentArts工作流"
- "新建AgentArts技能"
- "生成AgentArts Skill"
- "agentarts工厂"

### 3. 提供工作流参数

按提示提供以下信息：

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 技能名称（英文，短横线分隔） |
| `description` | 是 | 一句话描述 |
| `triggers` | 是 | 触发词列表 |
| `base_url` | 是 | AgentArts 网关地址 |
| `path` | 是 | API 调用路径 |
| `api_key` | 是 | Bearer Token |
| `session_id` | 否 | 默认会话 ID |
| `user_identity` | 否 | 目标用户身份 |
| `greeting` | 否 | 固定开场白 |

### 4. 直接使用命令行

也可以跳过对话，直接运行脚本：

```bash
# 通过命令行参数
python scripts/main.py \
  --name "Huawei-quality-check" \
  --description "面向质检员的 AgentArts 质检工作流调用技能" \
  --triggers "帮我做质检,质检分析,quality-check" \
  --base-url "https://defaultgw-mvstsmzsgv.cn-southwest-2.huaweicloud-agentarts.com" \
  --path "/runtimes/jiuwen-abc123/invocations" \
  --api-key "9a39833a9c3042798e8758de3b940693"

# 或通过 JSON 配置文件
python scripts/main.py --config workflow.json --output-dir ./my-skills
```

### 5. 获得生成的 Skill

```
<name>/
├── SKILL.md                    # 技能定义文件
└── scripts/
    └── invoke_agentarts.py     # AgentArts API 调用脚本
```

## 生成的 Skill 特性

生成的 `invoke_agentarts.py` 具备以下能力：

- **三层请求降级**：`requests` → `urllib` → IP 直连，确保在各种网络环境下可用
- **SSE 事件流解析**：支持 AgentArts 流式返回
- **权限错误检测**：自动识别权限不足等错误，避免无效重试
- **超范围指标检测**：对巡检类工作流，自动识别超出正常范围的指标
- **API Key 安全**：优先从环境变量 `AGENTARTS_API_KEY` 读取，避免硬编码泄露
- **零依赖**：标准库即可运行，`requests` 为可选增强

## 安全注意事项

- `api_key` 是敏感信息，生成后**强烈建议**通过环境变量 `AGENTARTS_API_KEY` 覆盖默认值
- 生成的 SKILL.md 中**不会**包含明文 API Key
- 发布到 ClawHub 或共享给他人前，请确认 `invoke_agentarts.py` 中的默认 Key 已清除

## 适用场景

- 将企业内部 AgentArts 工作流封装为 Skill，分发给业务团队
- 批量生成多个 AgentArts 工作流对应的 Skill
- 快速为新的 AgentArts 工作流生成标准化的 Skill 脚手架

## 依赖

- Python 3.8+
- 无第三方依赖（`requests` 为可选增强）

## 发布到 ClawHub

1. 确保 `SKILL.md` frontmatter 格式正确（`name`、`description`、`triggers`、`model` 字段齐全）
2. 确保 `scripts/main.py` 语法正确：`python -c "import ast; ast.parse(open('scripts/main.py').read())"`
3. 按 ClawHub 规范打包上传

## License

MIT
