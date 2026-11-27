# 桌面 Agent 分发

创建或更新面向 Trae、WorkBuddy、Codex 或其他 Agent Skills 客户端的导入包时读取本文件。WorkBuddy开放平台规范核验日期：2026-10-26。

## 1. 共同基线

所有包都以稳定目录名 `fastgpt-workflow-assistant` 和根入口 `SKILL.md` 为核心，保留实际运行需要的 `references/`、`scripts/`、`assets/`。排除 `__pycache__`、`.pyc`、完整自测试夹具、打包脚本和工程调研资料。

发布前执行：

```powershell
uv run python scripts/test_skill.py
uv run python scripts/package_desktop_agents.py <skill目录> <输出目录>
```

导入后在目标客户端执行 `scripts/smoke_test_skill.py`。客户端无法运行 Python 时，只能标记“结构导入通过”，不能宣称脚本能力已验证。

## 2. Trae / TraeCode

Trae 官方文档说明，可以上传单个 `SKILL.md` 或包含该文件及相关资源的 ZIP。项目技能通常位于 `.trae/skills/<skill-name>/`，全局技能在 Windows 位于 `%userprofile%/.trae-cn/skills`；TraeCode CLI 还使用 `.traecli/skills/` 或 `~/.traecli/skills/`。名称使用小写字母、数字和连字符可同时兼容 IDE 与 CLI。

Trae 导入包采用：

```text
SKILL.md
references/
scripts/
assets/
agents/
```

即 ZIP 根目录直接包含 `SKILL.md`。在“设置 → 技能与命令 → 创建 → 上传”中选择 ZIP；项目级导入后确认文件实际落到 `.trae/skills/fastgpt-workflow-assistant/`。修改后刷新技能发现或重启客户端。

官方文档：

- https://docs.trae.cn/ide_skills
- https://docs.trae.cn/cli_skills

## 3. WorkBuddy

WorkBuddy开放平台要求SKILL.md使用YAML frontmatter，且以下8项均为非空字段：`name`、`display_name`、`display_name_en`、`description`、`description_zh`、`description_en`、`version`、`author`。可选examples_zh/examples_en提供使用示例。实际开放平台上传反馈限制ZIP路径只能为根文件或目录/文件。2.9.2起专用包采用ZIP根入口，去除外层技能目录，深层资源平铺并同步改写引用：

```text
SKILL.md
references/guide.md
scripts/create_workflow_from_template.py
assets/workflow-templates__fastgpt-v481-minimal.json
agents/openai.yaml
```

每个ZIP文件路径最多2段，不允许目录再次嵌套。模板加载器兼容平铺资源；目录映射、目录深度、资源目录清单与解压后模板生成一起回归。官网示意目录不能替代目标上传器的实际报错证据。

WorkBuddy 专用包会在不修改源码 `SKILL.md` 正文的前提下，生成扩展 frontmatter。不要把该扩展文件反向覆盖 Codex 安装目录，避免未知元数据影响其他客户端的校验。

上传开放平台时选择文件名带 `_WorkBuddy_import-ready.zip` 的专用包；普通 `fastgpt-workflow-assistant-vX.Y.Z.zip` 是通用包，不能替代开放平台发布包。打包器在创建前和读取实际ZIP后均校验frontmatter；回归对每个必填字段的缺失与空值分别测试。

在 WorkBuddy 的“技能 → 添加技能 → 上传技能”中导入 ZIP。导入前检查脚本和权限：本技能没有内置凭据或固定生产地址，但接口回归脚本会在用户显式提供 URL/标识和授权环境变量时访问目标服务，可能把测试问题发送到该服务。

官方文档：

- https://open.workbuddy.cn/en/docs/skill
- https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market

## 4. 通用 Agent Skills 目录包

支持 `.agents/skills/` 的客户端使用带外层技能目录的通用包：

```text
fastgpt-workflow-assistant/SKILL.md
```

解压后应得到 `.agents/skills/fastgpt-workflow-assistant/SKILL.md`，不要产生双重目录。Trae 支持启用项目 `.agents/skills/`；若同名技能同时存在于 `.trae/skills/`，Trae 优先使用后者。

## 5. Hermes Agent

`package_desktop_agents.py` 同时输出 `*_Hermes_folder.zip`。入口为 `fastgpt-workflow-assistant/SKILL.md`，使用标准 frontmatter，不注入 WorkBuddy 专属字段。安装目录、Linux 命令和无浏览器限制见 [Hermes 适配](Hermes适配.md)。生产包的生成测试会解压 Hermes 包并执行其冒烟测试；真实 Hermes 中的发现与执行仍须另行验证。

## 6. 状态与哈希

每个包记录：

- 技能版本和发布日期；
- 客户端目标与 ZIP 根结构；
- 文件数、ZIP SHA-256；
- 完整源码自测试结果；
- 包内冒烟测试结果；
- 已知运行时依赖和网络访问边界。

只在真实客户端成功导入后写“目标客户端导入通过”。本地 ZIP 结构检查通过时使用“候选可导入包”。

## 7. 发布包资源完整性

发布物需包含核心功能实际需要的脚本、模板及本地引用文件；不能把开发机另装的技能写成用户必须先调用的能力。跨平台接口说明应能独立使用；不需要的外部技能引用应移除。打包器对实际ZIP检查本地Markdown链接，完整源码自测还包括缺失资源应失败的回归。平台审核可能检查自然语言依赖，本地链接检查不等于平台审核通过。
