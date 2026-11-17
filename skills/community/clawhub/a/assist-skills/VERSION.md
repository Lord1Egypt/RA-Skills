# AI 开发助手使用参考说明版本说明

当前版本：v1.0.2-linlan

发布日期：2026-09

版本定位：麟览（LINLAN）公司定制版，基于 v0.1.1 模板调整为公司实际技术栈和工程场景

适用范围：麟览公司 AI 试点项目，覆盖 Trae、CodeBuddy、Claude Code 和 opencode。

## 1. 使用参考内容

v1.0.2-linlan 是 AI 开发助手使用参考说明的麟览公司定制版本，重点提供：

- 项目级参考入口：`AGENTS.md`（含麟览公司典型工程参考）
- 多工具参考桥接：`rules/trae-poc-rule.md`、`rules/codebuddy-poc-rule.md`（部署时复制改名为 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`）、`CLAUDE.md`
- 1WEEK/3DAY/1DAY 任务复杂度与参考产物
- context 模板与建议质量门槛
- 需求、设计、测试、审查、发布和 AI 使用记录模板
- 分层快捷指令：初始化项目、开始任务、完成任务为核心治理指令；梳理需求、开始设计、编写测试用例、开始编码、执行测试、审查代码、生成阶段汇总为按需能力指令
- 按需 workflow：`ai-pilot/reference/workflows/` 承载快捷指令详细流程，让 AI 更聚焦当前任务
- 测试执行记录参考：`test-execution-log.md`
- 效果评估参考口径：耗时（小时）、AI 输出采纳率（%）、人工修改量、返工次数（次）、测试指标、功能规模估算和 AI 生成代码占比（%）
- LINLAN 实际工程场景示例任务，包含 Java Spring Boot、Python Flask、代码生成器等

## 2. v1.0.2-linlan 更新说明（累计）

- 版本号对齐发布版本：参考资料包版本 = ClawHub 技能包版本，避免"项目里写 1.0.0、线上是 1.0.2"的困惑
- 手工部署步骤改为"只新增、不删除"：仅复制本包自身文件、并把规则复制改名到 `.trae`、`.codebuddy` 点目录，不再给出删除或强制覆盖项目目录的命令；脚本默认也不覆盖同名文件，可先用 `-DryRun` / `--dry-run` 预演
- 增加麟览（LINLAN）公司标识和品牌信息
- AGENTS.md 新增第15节：麟览公司试点工程参考（linlan-claw-ops / anli-loop / linlan-skills / linlan-super-ip / shrcj-rcqy-skills）
- CLAUDE.md 增加公司典型技术栈参考
- 示例任务替换为麟览实际工程场景（工伤待遇知识库 / 案例库CRUD / 数据序列化修复）
- AI使用记录模板增加麟览工程类型字段
- 快速指令卡更新示例场景
- 规则文件由 `.trae/rules/`、`.codebuddy/rules/` 迁到非隐藏目录 `rules/`（点号开头的条目在技能打包分发时会被过滤，导致规则文件丢失），部署时复制改名为目标项目的点目录文件
- 新增一键部署脚本 `scripts/deploy.ps1`（Windows）/ `scripts/deploy.sh`（macOS / Linux），一条命令完成全量复制与规则落位
- 新增包根目录最短入口 `deploy.cmd`（Windows，可双击运行，自动优先 `pwsh`、回退 PowerShell）和 `deploy.sh`（macOS / Linux，转发给 `scripts/deploy.sh`），团队成员无需记忆脚本路径即可一键部署
- 部署体验傻瓜化，提供五种递进方式：①跟 AI 说一句话自动部署；②双击（技能包内嵌在项目里时零输入）；③右键项目文件夹 →「发送到」→ 一键部署（`-Shortcuts` 一次性生成入口）；④命令行一行；⑤项目内嵌分发（`-Vendor`）——队友克隆仓库后双击 `tools\assist-skills\deploy.cmd` 即可，完全不需要安装本包
- `scripts/deploy.ps1` 新增 `-Auto`（自动识别目标项目根）、`-Vendor` / `-VendorDir`（把技能包内嵌到项目，自动排除 `_meta.json`、`.clawhubignore` 等安装元数据）、`-Shortcuts`（创建「发送到」菜单与桌面快捷方式）、`-Pause`（结束后等待回车，便于双击查看结果）
- 部署脚本健壮性加固：自动清洗路径中的 BOM / 零宽字符、路径比较忽略大小写（防止"看起来正确"的路径绕过目录安全校验）；内嵌布局自动识别（技能包位于项目子目录且带 `.git`/`pom.xml`/`package.json` 等标记时直接按项目根部署，缺标记时只需回车确认）；未指定目标时的用法提示取代原始异常堆栈

## 3. 工具兼容性矩阵

| 工具 | 规则入口 | 是否支持项目规则自动读取 | 是否可直接执行测试命令 | 适配说明 |
|---|---|---|---|---|
| Trae | `rules/trae-poc-rule.md` → 项目 `.trae/rules/poc-rule.md` | 是 | 是 | 已确认支持项目规则目录，推荐作为首选工具 |
| CodeBuddy | `rules/codebuddy-poc-rule.md` → 项目 `.codebuddy/rules/poc-rule.md` | 是 | 是 | 适合按需 workflow 推进任务和测试闭环 |
| Claude Code | `CLAUDE.md` | 是 | 是 | 适合复杂任务、命令验证和多文件修改 |
| opencode | `AGENTS.md` | 是 | 是 | 优先读取根目录 `AGENTS.md` |

## 4. 分发说明

试点项目接入时，将参考资料包内文件复制到项目根目录，并保留项目已有业务代码和测试。

推荐直接执行 `deploy.cmd`（Windows，可双击）或 `deploy.sh`（macOS / Linux）；也可以直接调用 `scripts/deploy.ps1`、`scripts/deploy.sh`，两者参数一致，脚本会完成下面的复制动作并自动落地工具规则。不使用脚本时按下面手工复制。

最省事的两种团队做法：

```text
1) 让 AI 代劳：在项目里对 AI 说"把 assist-skills 部署到当前项目"。
2) 一次内嵌、全员受益：deploy.cmd -Target <项目> -Vendor
   之后队友克隆仓库，双击 <项目>\tools\assist-skills\deploy.cmd 即可（零输入，无需安装本包）。
```

建议复制内容：

```text
AGENTS.md
CLAUDE.md
ai-pilot/
VERSION.md
rules/
scripts/
```

使用 Trae / CodeBuddy 时，另外把 `rules/trae-poc-rule.md`、`rules/codebuddy-poc-rule.md` 复制改名为项目根目录下的 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`。

真实任务产物建议沉淀到：

```text
ai-pilot/poc/{任务编号}/
```

## 5. 使用边界

- 请勿在参考资料包中放置生产密钥、Token、连接串、真实个人信息或敏感业务数据。
- 不建议所有任务都生成完整 8 个文件，可按 1WEEK/3DAY/1DAY 任务复杂度裁剪。
- 1WEEK/3DAY级任务建议整理 context，1DAY级任务可按复杂度选择是否整理。
- AI 输出不建议直接进入交付，应按项目既有 Review、构建检查和测试验证流程确认。
