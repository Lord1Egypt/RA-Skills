# 构建阶段指南

当前版本阶段声明：
本阶段先形成稳定构建输入，再明确哪些平台可以进入最终生成、哪些只能停在本地安装或作者规范层。

## 目标

构建阶段负责把收口后的设计方案转成稳定的构建说明。
这里的重点是组织产物边界、选择模板、拼装能力、补齐脚本策略和说明，并明确平台兼容与发布边界。

## 输入

进入本阶段前，应当已经具备：

- 一份稳定的统一 spec
- 一份结构化 `spec.yaml` 草案或模板实例
- 一份设计决策摘要
- 目标平台列表
- 参考 Skill 或搜索结果判断
- 原子能力选择结果
- benchmark 决策

进入本阶段前的阻塞条件：

- 已确定 `primary_domain`
- 如果跨域，已确定 `peer_domains`
- `research_evidence.coverage_status` 已填写
- 研究缺口已通过 `open_gaps` 明确表达

命令路径约定：

- 如果当前目录是 `cocoloop-skill-factory/`，使用 `python3 utils/cli/<script>.py ...`
- 如果当前目录是工作区根目录，使用 `python3 cocoloop-skill-factory/utils/cli/<script>.py ...`

## 主动作

### 1. 整理统一 spec

把研究与设计结论整理成一份统一 spec。
建议先形成结构化 `spec.yaml`，再继续补齐其余构建文档。
统一 spec 建议至少包含：

- 基本目标
- 正式名称与展示名称
- 目标平台
- 触发方式
- 输入输出
- 依赖与权限
- 原子能力计划
- 模板计划
- 交付物清单
- benchmark 意图
- 如果适用，继续补 `visual_storytelling`

如果当前阶段已经形成 `spec.yaml`，还需要继续检查：

- 是否已经包含研究证据指针
- 是否已经明确调研覆盖状态和缺口
- 是否已经写出主任务域、并列补充域和平台 adapter
- 是否已经和当前预设包保持一致
- 如果任务属于视觉叙事型产物，是否已经写出 `visual_storytelling` 和 `design_md`
- 如果任务包含任何可视化输出，是否已经写出 `output_profile.has_visual_output`

如果当前收口的是规则补充、流程加固或方法论修订，也不能只停留在 spec。
需要同步生成一组可审查的样例产物，至少包括：

- `spec.yaml`
- `research-summary.md`
- `reference-skill-analysis.md`
- `design-summary.md`
- `spec.md`
- `build-plan.md`

这些产物必须按 `output/README.md` 的目录契约进入独立主题目录。

### 2. 选择模板

先看任务域预设，再看平台模板。
根据目标平台读取 `utils/template/` 下的模板文件。
模板选择至少看这几个维度：

- 平台
- Skill 复杂度
- 是否包含子 Skill
- 是否依赖外部方案
- 是否需要脚本化能力
- 当前平台是否允许声明公开兼容

### 3. 选择构建执行层

统一 spec 准备好后，调用 `sub-skills/skill-creator/SKILL.md`。
由构建规划层把 spec 转成文件结构建议、模板选择结论和内容装配步骤。

当前版本已经提供最小生成与校验链：

- `factory-skill-builder/scripts/render_skill_from_spec.cjs`
- `factory-skill-builder/scripts/validate_platform_skill.cjs --spec <spec.yaml>`
- `factory-skill-builder/scripts/build_skill_from_spec.cjs`

这条链路能生成最小 Skill 骨架并完成平台校验。
只有显式传入 `--package`，才会继续产出打包结果。
在干净环境里，先进入 `factory-skill-builder/` 并执行 `npm install`，准备 `yaml` 依赖。
如果要打包，还需要系统里至少存在 `zip` 或 `tar` 其中一个命令。
当前生成链会把 `utils/template/` 中的统一协议模板和所选平台模板复制到 `references/templates/`，把模板选择结果一并固化进产物。
如果 `spec.yaml` 中 `output_profile.has_visual_output` 为真，当前生成链还应继续：

- 生成 `references/design.md` 作为最终 Skill 的默认设计入口
- 复制 `ref/design-md/` 本地预设库到 `references/design-md/`
- 在最终 `SKILL.md` 中提示用户先读 `references/design.md`，也允许用户替换成自己的 `DESIGN.md`

更完整的发布器和平台专用安装器仍然属于后续补充项。

但在收口前必须继续给出：

- 当前平台是否属于 `supported_public`、`supported_authoring_only` 或 `supported_local_only`
- 如果不是 `supported_public`，是否已经停在作者规范或本地激活边界
- 如果是 `molili`，是否已经写出源目录、激活目录、软链接优先和调用验收步骤

### 4. 装配原子能力

读取 `atomic-capability/index.md` 和相应能力说明，把需要的能力映射到目标方案。
处理原则：

- 能复用已有原子能力，就不要重复发明
- 能脚本化的稳定动作，先标记为后续实现候选
- 仅靠文档说明就够的内容，不强行写成脚本

### 5. 补齐外部依赖说明

只要最终方案依赖外部方案、外部服务或第三方工具，就必须同步写清楚：

- 前置条件
- 接入步骤
- 使用方式
- 风险和限制
- 替代路径

### 6. 规划 benchmark

如果该任务适合比较验证，再读取 `utils/benchmark.md`。
如果不适合，就在最终交付中明确说明跳过原因。
当前版本只要求定义 benchmark 的进入条件、样本和判定方式，不要求提供自动执行脚本。

### 7. 提交与审查门槛

如果当前任务被定义为“已完成”，在收口前还需要继续检查：

- 相关要求是否已经写入正式 `prd`
- 是否已经形成设计文档
- 是否已经进入 `output/` 构建产物
- `output/` 目录是否符合统一契约
- 可提交的 git 子仓库是否已经完成提交
- 是否已经经过一次独立审查

## 最终产物建议结构

未来实际生成 Skill 包时，建议至少包含：

```text
<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/
  platform-manifests/
  scripts/ 或 utils/cli/
  assets/            # 只有确实需要时再创建
  sub-skills/        # 只有确实需要时再创建
```

平台差异可以通过模板文件或局部分支目录表达，但最终目录必须保持可读、可维护、可安装。

## 交付检查

交付前至少检查这些项目：

1. `SKILL.md` 能否独立解释技能做什么、何时使用、按什么顺序执行
2. 目录结构是否与目标平台模板一致
3. 后续需要实现的关键脚本是否已经定义清楚输入、输出和边界
4. 搜索与环境检测这类基础动作是否具备降级路径
5. 所有外部依赖是否都有接入说明
6. 是否已经明确目标平台对应的目录、元数据和安装路径要求
7. `molili` 是否仍被单独对待
8. benchmark 若被启用，比较对象和输出格式是否明确
9. 平台支持等级是否和 `platform-support-matrix.md` 保持一致

## 结束条件

本阶段结束时，应该得到一份稳定的构建计划、模板选择结果、交付边界说明，以及在条件满足时生成出的最小 Skill 骨架。
