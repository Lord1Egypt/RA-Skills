# ai-data-delivery · v0.1.2

让 FDE 和数据产品经理把一个业务问题，变成**能看懂定义、能核对结果、能交给应用或 Agent 使用的数据语义**。

已有表、字段说明、指标或关系图，就从它们继续；只有部分资料也能开始。你提供业务问题和材料，使用本 skill 的 Agent 整理模型、运行工具并解释结果。可选的本地工作台负责编辑、试算、保存和导出，本身不内置大模型。

[MIT](LICENSE) · [安全边界](SECURITY.md) · [本版验证](references/v0.1.2-validation.md)

## 它具体帮你做什么

| 你遇到的问题 | 用它得到什么 | 需要你判断什么 |
| --- | --- | --- |
| 表很多，不知道一个业务问题该用哪些 | 复用已有结构、关系和说明，形成当前问题的对象、字段、指标映射 | 真实业务身份、粒度和口径，不能靠同名字段猜 |
| BI、报表、AI给出不同数字 | 在同一范围和快照中核对指标值与输入明细，定位过滤、NULL、去重或关联放大问题 | 哪个口径才是本次被认可的定义 |
| 建好了语义，却不知道怎么给Agent用 | 带来源的指标上下文包，消费前核对是否过期；已有引擎可另做明确范围的接口联调 | 实际消费者、可见范围及尚未实现的能力 |
| 改字段或公式后怕影响已有应用 | 引用/漂移检查、重算与历史证据；已过期结果不继续显示为当前通过 | 哪些业务变更已获授权、哪些要保留历史 |

## 第一次：先完成一次练习

在解压后的 skill 目录执行；需要 Python 3.10+，依赖只有 PyYAML：

```bash
python -m pip install -r requirements.txt
python scripts/start.py --project ./work/demo --demo
```

打开终端打印的本机网址，首页点击 **“开始数值与明细练习”**，再点击执行。模型、模拟快照和字段已经准备好，不必先写 YAML。

这份练习解释为什么 A、A、NULL 三条输入，记录行数是3、非空计数是2、去重非空计数是1。查看明细、换指标、预览相关语义，然后在“交付与版本”下载结果。未填独立预期只记“完成计算”；练习通过不等于生产验收。

关闭后继续同一个项目：

```bash
python scripts/start.py --project ./work/demo
```

不要再次带 `--demo` 覆盖项目。零售练习可用新目录加 `--demo retail`。首次启动不会申请数据库密码、调用外部模型或终止其他服务。

## FDE：拿真实资料打通一个问题

向已安装本 skill 的 Agent 直接说：

> 使用 ai-data-delivery。我需要回答【具体业务问题】，DDL/已有模型在【路径】，可用快照在【路径，可暂缺】。先复用已有结构，只补当前问题需要的定义；请给出可读口径、可执行验证与消费交接，说明未验证范围。项目保存到【目录】。

Agent负责选择工具、准备输入与解释缺口；你核对映射和实际消费者。已有模型与独立SQLite快照时，也可直接打开：

```bash
python scripts/start.py --project ./work/customer-a --model ./semantic.yaml --sample ./snapshot.sqlite --provenance deidentified
```

只有SQLite/MySQL DDL时，将 `--model` 换成 `--ddl ./source.sql`，省略快照。`deidentified`只是你对样本来源的声明，不会自动脱敏。没有数据时可以建草案，但不会生成“数值验证通过”。

完整但不强制的路径见 [FDE快速上手](references/quickstart-fde.md)。`rebuild.py` 是另行授权的高级本机服务辅助工具，首次使用和语义建模都不需要运行它。

## 数据产品经理：描述业务，直接看结果

无需先学SQL或维护模型文件。可直接说：

> 使用 ai-data-delivery。我想统计【对象和指标】，范围是【主体/时间/状态】，现有资料在【路径】。请先用人话说明包含与排除，给我必要的候选解释，只问会改变结果的问题；把确认后的口径和实际结果放到我能查看的位置。

你主要看三件事：**算谁、怎么算、结果由哪些记录组成**。对业务决定按实际授权确认；数据是否真实、计算是否正确仍需验证。修改文字描述不会自动改变计算公式，Agent/FDE应同步修改并重算。

没有资料时也可以先梳理问题；不能据此声称已有数据库、接口或可执行结果。操作路径见 [产品经理快速上手](references/quickstart-pm.md)。

## 交出去的是什么

给人查看时，先打开交付ZIP中的 **00-human-review.html**，或在工作台直接下载“可视化验收页”：可展开思维导图串起问题、对象、指标、映射与证据，点开就是业务说明和预期/实际对照；FDE可展开技术定义。PM按业务范围与正反例核对，FDE按粒度、字段、关联与消费结果核对。具体见[如何人眼验收](references/human-review.md)。图由同一模型生成，不能拿它与模型互相一致就证明业务正确。

工作台“交付与版本”可下载模型、可读字典、场景约定、确认记录、问题与验证证据；项目备份另含SQLite及导入附件。CLI也能输出指标数值/明细和按问题选择的Agent上下文包。

上下文包是文件，不是生产API。源模型变化后，消费方需要重新执行检查；它不会自动撤回已经发出的文件。真正的问数服务、身份认证和行列权限仍由目标系统承担。见 [指标与上下文消费路径](references/metric-context.md) 与 [元数据到消费](references/metadata-to-consumption.md)。

## 按需要继续

- [工作台操作](workbench/README.md)：导入、建模、检查、历史与导出。
- [模型合同](references/contract.md)、[补齐会话](references/onboarding.md)：具体字段、确认和映射。
- [问题诊断](references/diagnosis-playbook.md)、[全部工具](references/tools.md)：遇到问题再查，不必先全部跑一遍。
- [既有项目证据](references/evidence/traffic/README.md)、[大会机制取舍](references/conference-practices-2026.md)：按来源和证据范围理解，不把案例效果当收益承诺。
- [领域起步包](starter_packs/README.md)、[标准边界](references/standards.md)：候选模型与规范适用性需核对。
- [分阶段交付](references/delivery-playbook.md)、[大型项目故事地图](references/story-map.md)：供较大任务裁剪，不是所有任务的必经流程或工期保证。

## 本版变化与安装

v0.1.2统一包内、文档与后续市场发布版本；继承本地v0.0.12功能。新增一条首次启动入口，收拢FDE/PM路线，并修复环境继承、网络请求和服务生命周期的已知问题。当前验证和未验证范围见 [本版记录](references/v0.1.2-validation.md)。旧版记录保留为历史，不代表新包平台审计已经通过。

把完整目录安装到宿主支持的 skills 位置，再请 Agent 使用 `ai-data-delivery`；具体安装方式以宿主为准。无需为了使用本 skill 另装 ai-delivery-spec。下载包保留所有运行工具和示例，开发测试目录只在源码仓库。

维护者在源码仓库运行：

```bash
python -m unittest discover -s tests -v
python mocks/run_mock.py --all
python maintainer/build_skill.py --out dist
```

**English:** Chinese-first documentation; users may interact in any language. Give your agent a business question and existing materials, or run `scripts/start.py --project ./work/demo --demo` for a local synthetic walkthrough. This is a semantic delivery and verification toolkit, not a production query gateway, universal SQL compiler, OWL reasoner or permission service.
