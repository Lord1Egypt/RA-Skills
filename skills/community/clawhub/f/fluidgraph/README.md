# FluidGraph Skill — 发布包

本目录是 FluidGraph Skill 的**发布入口**。

| | |
|---|---|
| Skill 名称 | `fluidgraph` |
| Skill API 版本 | `1.0.0` |
| AnalysisResult schema | `2.0` |

完整能力说明见 **[SKILL.md](SKILL.md)** —— 那是给 Agent / Skill Runtime 读的契约文档。
本文件面向**发布者与运维**，说明怎么部署、怎么验证。

---

## 这个 Skill 做什么

把一个简化的稳态、不可压缩流体网络建模成图结构，计算节点压力、管路流量、流速与
压力损失，判定负载功能可靠性，并给出可解释的失败原因。

**所有数值由确定性求解器计算，不由模型产生。**

---

## 运行时要求

| 项 | 要求 |
|---|---|
| Python | **3.11+**（依赖标准库 `tomllib`） |
| 第三方依赖 | **无** |
| 磁盘 | < 1 MB |
| 网络 | 不需要（Core 与 Skill 层零网络依赖） |

Python 3.10 及以下需要额外装 `tomli` 作为 TOML 回退（见 `requirements.txt`）。

### 关于 LLM SDK

**Skill 本身不需要任何 LLM SDK。** `openai` 包只在 `agent/` 目录（DeepSeek 集成）里
才会用到，且 `agent/client.py` 内置了等价的 `urllib` 实现 —— 不装也能跑。

单测 `test_architecture_boundary.py` 会验证这一点。

---

## 快速验证

部署后跑这两条，能跑通就说明环境没问题：

```bash
# 1) 工具清单
python skill_runner.py --list

# 2) 实际算一个工况
python skill_runner.py analyze_scenario examples/example.toml v1_failure
```

预期第 2 条返回 `"ok": true`，且 `loads` 里 `L1` 的 `status` 是 `ISOLATED`、
`pressure` 是 `null`（**不是 0**）。

---

## 导出 Tool Schema

发布到不同平台时导出对应格式：

```bash
python skill_runner.py --schema                    # 原始（本项目的定义）
python skill_runner.py --schema --format openai     # OpenAI Chat Completions
python skill_runner.py --schema --format anthropic  # Anthropic Messages
python skill_runner.py --schema --format mcp        # MCP tools/list
```

三种格式产出同一批工具、同一批描述，只是外壳不同。

---

## 发布前检查

仓库根目录执行：

```bash
python scripts/check_release.py
```

会验证 12 项（见脚本输出），包括：必需文件存在、Schema 可导出、CLI 可运行、
测试通过、**仓库中不含 API Key**、源码中不含开发机绝对路径、无临时文件。

---

## 7 个工具

| 工具 | 用途 | 需要 LLM 吗 |
|---|---|---|
| `parse_network` | 解析校验，失败时返回全部问题的结构化诊断 | 否 |
| `analyze_scenario` | 单工况完整分析 | 否 |
| `analyze_all_scenarios` | 一次跑完全部工况 | 否 |
| `explain_load` | 解释单个负载的状态与原因 | 否 |
| `compare_scenarios` | 多工况逐负载对比 | 否 |
| `render_report` | 渲染 Markdown 报告 | 否 |
| `read_file` | 读取文本文件（只读，受路径白名单约束） | 否 |

**没有任何一个工具依赖模型。** 全部可以在命令行直接调用。

---

## 安全边界

- `read_file` **只读**，且受路径白名单约束（默认：项目根 / `examples/` / `outputs/`）
- 只读文本类扩展名，单文件 ≤ 256 KB
- **未配置白名单时拒绝一切读取**（安全默认是拒绝，不是放行）
- **Skill 无写盘能力** —— 配置修复只能由 Agent 内联生成 TOML 后重新解析
- 拒绝信息中不含被拒文件的内容

---

## 三条硬约束

这三条写在 `SKILL.md` 里，是所有消费方**必须**遵守的：

1. **`null` ≠ `0`** —— `null` 是没有有效计算值，不是"结果为零"
2. **`required_flow` ≠ `actual_flow` ≠ `min_flow`** —— 三个流量概念不能混
3. **Agent 不得自行计算任何物理量** —— 所有数值必须来自 `AnalysisResult`

另有第四条纪律：**业务参数（`min_pressure`、`resistance` 等）不得猜测**。
这些是工艺设计数据，只有用户知道。工具会如实报错，Agent 也应向用户询问。

---

## 目录结构

```
skill/
├── SKILL.md          Agent / Skill Runtime 读的能力契约
└── README.md         本文件：发布者 / 运维视角
```

运行时依赖的代码在仓库根目录：

```
fluid_network/        Core + Skill 层（零外部依赖）
agent/                DeepSeek 集成（唯一需要 LLM SDK 的地方）
examples/             可直接运行的示例网络
skill_runner.py       CLI 入口
```

发布为独立包时，把 `fluid_network/`、`examples/`、`skill_runner.py` 与 `skill/`
一起打包即可 —— 整个目录拷贝过去就能跑，**不需要包管理**。
