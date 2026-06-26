# 平台支持矩阵

这份矩阵是 `cocoloop-skill-factory` 子仓内的本地平台基线，用于独立阅读和执行时判断平台边界。

## 支持等级

- `supported_public`
  已核实公开作者文档、安装方式和发布路径，可作为正式兼容与公开发布目标
- `supported_authoring_only`
  已核实作者规范和最小目录，只能承诺可创作、可本地组织
- `supported_local_only`
  已核实本地安装或激活协议，只能承诺本地可用
- `planned`
  有方向但依据不足，不得对外声明兼容
- `unverified`
  没有可靠来源，不得作为正式平台承诺

## 当前矩阵

| 平台 | 当前等级 | 最低产物 | 当前边界 |
| --- | --- | --- | --- |
| `codex` | `supported_public` | `SKILL.md`，可选 `agents/openai.yaml`、`scripts/`、`references/`、`assets/` | 可以生成最小 manifest 与校验，仍缺正式 Plugin 发布器 |
| `claude_code` | `supported_public` | `SKILL.md` 与 Claude frontmatter | 可以生成最小 frontmatter 与校验，仍缺更完整字段覆盖 |
| `openclaw` | `supported_public` | `SKILL.md` 与发布 manifest | 可以生成最小发布参数，仍缺正式发布器 |
| `hermes_agent` | `supported_public` | `SKILL.md`、环境变量与凭据声明 | 可以生成最小 manifest，仍缺 scan / trust 执行器 |
| `copaw` | `supported_authoring_only` | `SKILL.md` 与 supporting files | 不得声明公开发布 |
| `molili` | `supported_local_only` | `SKILL.md` 与本地激活目录 | 只承诺本地激活，不承诺公开发布 |

## 读取规则

- 主流程默认读这份本地副本
- 只有在完整工作区里回溯更长的产品治理上下文时，才额外参考根级 `codex-prd/platform-support-matrix.md`
