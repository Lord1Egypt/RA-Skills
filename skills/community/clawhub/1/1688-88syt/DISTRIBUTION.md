# 88syt-skill 分发说明

## 内容物

- **`SKILL.md`**：技能入口，列出能力范围并指向 `references/`。
- **`references/`**：各场景操作细则与**完整请求示例**（含固定 `skillName` / `skillVersion` / `site` 与 `userId`、`x-api-userid` 约定）。
- **`prompts/`**：仅用于**维护者生成/更新**技能时的输入参考，**不包含**在对外分发的技能包中；分发前请删除或不要打包该目录。

## 使用方（智能体 / 平台）

1. 将 **`SKILL.md` 与整个 `references/` 目录** 一并部署或挂载为同一路径层级，保证 `SKILL.md` 内相对链接可访问。
2. 不要将 **`prompts/`** 暴露给终端用户或下游智能体。
3. 对客侧须遵守技能内 **中文输出**、**免责声明**、**高风险二次确认**、**禁止暴露 fin-agent.1688.com**、**外链追加 `tracelog=88sytskill`** 等约束。

## 版本与标识

- 技能包内请求体固定：`skillName: 88syt-skill`，`skillVersion: 0.1.0`，`site: 1688`。
- 升级接口或字段时，应同步更新 `references/` 中对应文件及本说明中的版本描述（如有）。

## 维护流程建议

1. 仅修改 **`prompts/`** 作为需求草稿时，运行一次「根据 `prompts/index.md` 重新生成 skill」的流程，将结果写回 **`SKILL.md` / `references/`**，**勿改** `prompts/` 内文件作为线上引用源。
2. 发布前检查：`SKILL.md` 链接均可打开；示例 JSON 与当前网关一致；`DISTRIBUTION.md` 与包内容一致。
