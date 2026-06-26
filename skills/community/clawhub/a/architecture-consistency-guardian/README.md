# Architecture Consistency Guardian 架构一致性守卫

你的 AI 编程助手是不是也这样——修了一个 bug，却在三个文件里留下了旧变量名？改了状态机，但 fallback 还在偷偷把流量导回旧逻辑？

这个 [OpenClaw](https://github.com/openclaw/openclaw) Skill 专治这个病。它把 AI Agent 的默认姿势从“哪里报错补哪里”，切换为 **全局扫描 → 唯一真源 → 成组修改 → 残留审计 → 回归验证** 的完整工作流。它不只是教模型“写代码”，而是强制模型先对齐架构契约，再落地修改。

## 解决什么问题

AI Agent 或人类修代码时，常见的问题不是不会改，而是**只改半截**。例如只修当前文件、不追踪调用方；改了状态值、不检查其他模块是否还在用旧值；统一了配置路径，却把硬编码副本留在文档或脚本中；删除了旧模块，但兼容 fallback 仍在静默回流。

这个 Skill 的目标就是在这些场景里强制执行“先全局、后修改”的姿势，避免局部修复把系统进一步拉散。

## 适用场景

- 跨文件统一变量、字段、参数命名
- 状态机收口，统一状态值、迁移规则和写回入口
- 清理 legacy 路径、fallback 和已退役模块
- 统一配置来源，如数据库路径、环境变量、运行时配置
- 重构后同步文档与代码
- 修 bug 时发现根因可能是架构契约漂移

## 强制 8 阶段工作流

1. **归类**：判断一致性问题类别，如命名、状态机、配置路径。
2. **识别唯一真源**：找到权威文件，并标记竞争真源。
3. **全局扫描**：搜索所有相关引用，而不是只看当前文件。
4. **修改计划**：列出受影响文件和具体改动，再开始实施。
5. **成组执行**：按顺序修改真源、调用方、配置层、兼容层、测试与文档。
6. **残留审计**：确认旧名称、旧状态、旧路径、旧 fallback 是否仍存在。
7. **回归验证**：运行测试、验证零残留、确认配置解析和核心行为。
8. **结构化报告**：输出真源、影响范围、已改内容、残留兼容层和验证结果。

## 内置脚本

| 脚本 | 用途 |
|------|------|
| `scripts/grep_legacy.py` | 扫描旧名称、旧路径、旧状态残留 |
| `scripts/scan_contract_drift.py` | 检测多个竞争真源 |
| `scripts/summarize_impacts.py` | 聚合扫描结果并输出影响面摘要 |

## 使用示例

```bash
# 扫描 legacy 残留
python3 scripts/grep_legacy.py /path/to/project old_status_field legacy_module_name

# 检测契约漂移（多处定义同一个东西）
python3 scripts/scan_contract_drift.py /path/to/project

# 管道：legacy 扫描结果 → 影响面摘要
python3 scripts/grep_legacy.py /path/to/project old_name --json | \
  python3 scripts/summarize_impacts.py --source-of-truth config.py

# 管道：contract drift 结果 → 摘要
python3 scripts/scan_contract_drift.py /path/to/project --json | \
  python3 scripts/summarize_impacts.py --source-of-truth runtime_config.py
```

## JSON 输出协议

`grep_legacy.py` 与 `scan_contract_drift.py` 的 `--json` 现在使用统一外层协议，便于自动化链路、测试和后续扩展：

```json
{
  "tool": "grep_legacy",
  "schema_version": "1.0",
  "scan_root": "/repo",
  "generated_at": "2026-04-14T12:00:00Z",
  "results": [],
  "summary": {},
  "errors": []
}
```

其中 `results` 会根据工具类型携带不同的明细项，而 `summarize_impacts.py` 会根据 `tool` 字段自动识别来源并生成对应摘要。

## 工程化入口

```bash
# 编译检查
make compile

# 运行测试
make test

# 基础冒烟验证
make smoke
```

GitHub Actions 默认会在 Push 和 Pull Request 时执行脚本编译与测试。

## 目录结构

```text
architecture-consistency-guardian/
├── .github/workflows/ci.yml      # 持续集成
├── SKILL.md                      # 核心工作流与硬规则
├── Makefile                      # 本地开发命令入口
├── pyproject.toml                # 项目元数据与 pytest 配置
├── references/
│   ├── workflow.md               # 详细工作流与决策分支
│   ├── output_template.md        # 结构化报告模板
│   ├── risk_patterns.md          # 常见一致性风险模式
│   └── contract_template.md      # 架构契约文档模板
├── templates/
│   ├── consistency_report_template.md
│   └── architecture_contract_template.md
├── scripts/
│   ├── grep_legacy.py
│   ├── scan_contract_drift.py
│   └── summarize_impacts.py
└── tests/
    └── test_cli_workflows.py
```

## 安装

### ClawHub（推荐）

```bash
clawhub install architecture-consistency-guardian
```

### skills.sh

```bash
npx skills add upsightx/architecture-consistency-guardian
```

### 手动安装

```bash
cp -r architecture-consistency-guardian ~/.openclaw/skills/
```

## License

MIT
