# L3 编排层（`orchestration/`）

本目录与包根 [`SKILL.md`](../SKILL.md)、L1 [`common/`](../common/)、L2 [`products/`](../products/) **物理隔离**；跨场景约定见 [`orchestration-contract.md`](orchestration-contract.md)，运行时契约详版见 [`../references/top-level-runtime-contract.md`](../references/top-level-runtime-contract.md)。

## 职责（与 L2 的边界）

- **L2 `products/`**：单一蝉镜产品；手册为 **`{产品目录名}-SKILL.md`**，可执行代码在 **`scripts/`**（含 `cli_capabilities.py`）。  
- **L3 本目录**：组合多个 L2 能力，形成新的业务能力；**每个场景子目录仅一个** **`{场景目录名}-SKILL.md`**，**可**附带 `scripts/`、`templates/`、`README.md`（人类向补充，不作第二份路由手册）。  
- **跨场景约定**：[`orchestration-contract.md`](orchestration-contract.md) 为共用约定，**不**替代各场景 `-SKILL.md`。

## 目录约定

| 类型 | 位置 | 内容 |
|------|------|------|
| **跨场景约定** | [`orchestration-contract.md`](orchestration-contract.md) | 协作顺序、`outcome_code`、渐进路由 |
| **业务场景** | `<scene>/` | **一个** `<scene>-SKILL.md` + **`scripts/`**（可选模板、README） |

## 与顶层入口的关系

- Agent **始终**从 [`../SKILL.md`](../SKILL.md) 进入。  
- 命中 L3 后打开 **`orchestration/<scene>/<scene>-SKILL.md`**，再按其中指引调用 `scripts/` 及各 `products/` 能力。
- 调用任意 `scripts/` 前，须阅读包根 [`../SKILL.md`](../SKILL.md) **「运行时契约」**（蝉镜 API、本地凭据文件、`ffmpeg`/`ffprobe`、环境变量与副作用说明）。

## Workflow 统一约束

- 所有 L3 场景文档应采用统一模板：`Step + 脚本名 + 输入 + 输出 + 下一步 + 失败分支`。
- 失败分支必须映射 `outcome_code` 统一语义：`ok`、`need_param`、`auth_required`、`upstream_error`、`timeout`。
- 需要跨产品降级时，必须先征得用户确认。
