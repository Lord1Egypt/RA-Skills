---
name: cad-file-reader
slug: cad-file-reader
displayName: CAD 图纸识图与证据提取
version: 0.41.3
license: CC-BY-NC-SA-4.0
author: lis
i18n: true
locale: zh-CN
locales: [zh-CN, en-US]
description: "识图测量候选；不做算量，final_quantity=false。触发词：识图。"
---

# CAD 图纸识图与证据提取（cad-file-reader）

## 识图契约红线（硬规则，禁止绕行）
- 算量技能**不得单独识别 DWG/DXF/PDF**：识图必须由 `cad-file-reader` 完成一次，产出统一契约后各算量技能共享复用（同一张图只解析一次）。
- **禁止算量技能自行 `import ezdwg/read_cad`、自带或重新下载 cad-file-reader 来解图**；底座缺失时如实标 `unavailable`，不得降级成“自己解图”。
- 用户要算量 = 必须先走 `cad-file-reader → 契约 → 算量`；计算入口默认拒绝直接 DWG，开发/回归调试才能用显式 `CAD_ALLOW_DIRECT=1` 逃生。
- `lis-skill-bus` 是连接 cad-file-reader 契约与各算量技能的唯一定接线；算量结果必须带契约来源（图号/坐标证据）。
- **DWG 解码兜底（仅特殊变体才需要，普通图不强制）**：正常 DWG 由内置 ezdwg 直读即可，不依赖任何外部 CAD/看图 App；只有 ezdwg/libredwg 都读不了的 ACAD 新变体/损坏卷（实测例：sample-site结构 2#/3# 图审版）才用独立 `ODAFileConverter` 兜底转 DXF 复扫。ODA 是免费可选后端，不随技能强制安装；**禁止调用“CAD快速看图”等看图 App 的 GUI 或内嵌 ODA 库当解析后端**（它们只暴露导 PDF/打印，无公开 CLI，grep 不到转换器）。ODA 转换只能在**复制副本**上执行，禁止覆盖原图；转换后必须回读校验图层/文字/图元，副本 DXF ≠ 图纸原件，不能把转换产物当原图证据。
- **内存双档**：常规识图默认 `CAD_MEM_LIMIT_MB=4096`（mem_guard 默认）；仅实测超 4GB 的真实大图且串行跑时临时覆盖 `CAD_MEM_LIMIT_MB=8192`，不全局改默认；mem_guard 只在识图子进程内自终止，不杀 WorkBuddy/Codex。


> **融合入口**：本技能可单独使用；若手上是一整套图纸、要跨专业出一张总表，用 `cad-suite` 一个入口即可跑完发现→识图→关系→聚合→跨专业对照→算量→出表，不必逐个调用。口径与红线在 cad-suite 里是同一份。

本技能只做**识图、证据提取、候选解释和测量候选**，可输出长度、面积、体积的识图候选值、计算式和复核边界；不把候选值冒充最终工程量、清单量、材料量、造价或结算量。结构混凝土/钢筋算量已迁到 `tujian-suanliang`，装饰、安装、钢结构、市政算量分别交给对应专项 skill。

## 详细说明（按需读取，只搬未删）

安装与依赖、平台支持矩阵、bus/五件套联动、图层与块语义、PDF 分流、测量候选、专业识图路由、塔吊识图、跨图聚合、自测预检、命令速查与工作流的完整章节已外移到 `references/on-demand.md`。本文保留识图契约红线、执行原则、可靠性策略、统一候选契约、边界与授权；安装或排查细节时先读该文件同名小节。
## 执行原则

- 先用低内存 `cad_scan` 读文字、图层、块名、图框和几何候选；确需实体树/渲染时再用 `read_cad`。
- 自动结果必须带证据坐标、图框、图层、口径和复核边界；缺输入时列缺口，不编造数量或合规结论。
- 规范/图集资料只做元数据与版本风险提示，不复制全文、不输出条文符合性结论。
- 命令均相对技能根目录执行；输出文件写入当前项目工作目录，不写系统目录。
- 大图先扫描、按需局部展开；高内存/高 CPU 立即暂停。
- 首次扫描可用 `--cache-dir` 建立本机证据缓存；同图重复查询命中缓存。缓存只保存识图证据，不保存最终工程量。
- 总图/场地识图新增 `building_outline` 分类（建筑屋顶外轮廓、地下室外轮廓），可给布置/算量技能提供多栋主体轮廓候选；它只是图层+几何候选，不保证选中“主楼”，也不把多个轮廓层自动合并。

## 可靠性策略（快速失败）

- 大图先过预检；空文件、坏图、加密图和不支持版本快速失败，批量逐图记录缺口，单图失败不中断。
- `--budget` 控制阶段预算，`--cap-mb` 控制内存；超时或内存闸终止写入台账。
- PDF 可疑页截图、触发条件和关闭开关见 `docs/reliability.md`。

## 统一候选契约（cad-file-reader/v0）

装饰、安装、钢结构、市政和测量候选 JSON 会额外写入 `contract`：

- `candidates[]` 只放 `confirmed_evidence` 和 `inferred_candidate`；`review_candidates[]` 只放 `review_required`。
- `confirmed_evidence`：有直接文字、图层、几何、块或标注证据，且置信度 ≥ 0.90。
- `inferred_candidate`：由邻近关系、图层语义、块内容或规则推断，置信度 0.50–0.89。
- `review_required`：低置信、缺比例/单位/图层/块定义、文字绑定不明、几何冲突、重复、图框外或几何不完整；不进入默认汇总主线。
- `review_reasons[]` 使用标准英文词表，`review_notes` 保留中文说明；`source_schema` 固定为 `cad-file-reader/v0`，`final_quantity` 固定为 `false`。
- 契约溯源统一为 `cad-contract/v1`：`contract_id`、`source_sha256`、`reader_version`、`run_manifest` 追加在 `contract` 内，旧 v0 字段语义不变；`contract_id` 不含墙钟时间，`run_manifest` 才记录命令、参数与起止时间。
- 交付或交接前可校验：`scripts/cad_validate.sh 输出.json`。
- **输出深度（用户可选）**：默认完整输出；追加 `--concise` 使用精简契约省 Token（候选只保留主干字段 id/类别/图层/文本/置信度/复核原因/来源文件）；`--full` 或 `--with-evidence` 恢复完整证据。环境变量 `CAD_CONCISE=1` 可全局设为精简默认。

## 边界

- 不做设计合规审查、施工方案判断、清单计价、结算审计或规范条文解释。
- 测量候选不是最终工程量；专项算量 skill 必须继续完成扣减、重叠、做法映射、损耗、分账和台账。
- 不输出最终工程量、材料量、造价或结算量；只输出识图候选、几何证据、测量候选（`final_quantity=false`）和复核原因。
- 自动提取不能替代设计单位、翻样、清单编制和正式授权规范全文。
- 不把公司内部路径、项目结果或规范全文写入技能发布内容。

## 授权与保留

CC-BY-NC-SA-4.0，仅限非商业用途。商业使用（含承接造价/算量咨询业务）须另行取得作者书面授权；作者保留全部商业权利（商业使用、再发布、封装收费、授予第三方商业授权）。条款全文见 `LICENSE.md`。

