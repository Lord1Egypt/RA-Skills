---
name: anzhuang-suanliang
slug: anzhuang-suanliang
displayName: 安装算量 · 概算底稿与物资计划双口径
version: 0.4.38
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "安装出概算与物资计划；不出金额、不替代结算。触发词：安装算量、桥架、喷淋。"
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
locales: [zh-CN, en-US]
---

# 安装算量（概算清单 + 物资计划双口径）

## 识图契约红线（硬规则，禁止绕行）

- 算量技能**不得单独识别 DWG/DXF/PDF**：识图只能由 `cad-file-reader` 做一次，产出统一契约后各技能共享复用。
- **禁止自行 `import ezdwg/read_cad`、自带或重新下载 cad-file-reader 解图**；底座缺失如实标 `unavailable`，不得降级成「自己解图」。
- 算量入口不提供任何图纸直读或“开发直读”逃生开关：DWG/DXF/DWT 一律按退出码 `23` 停止；算量结果必须带契约来源（图号/坐标证据）。
- `lis-skill-bus` 是契约与算量技能之间的唯一定接线。
- DWG 解码兜底（ezdwg 读不了的 ACAD 新变体/损坏卷）只能在底座内用 `ODAFileConverter` 在副本上转 DXF 复扫校验；本技能不得调用 CAD/看图 App/ODAFileConverter。
- 内存双档：默认 `CAD_MEM_LIMIT_MB=4096`；仅实测超 4GB 真实大图且串行跑时临时 8192，不改全局默认；mem_guard 只终止识图子进程。

## 入口闸门（固定退出码，禁止 fallback）

未安装依赖时唯一正确行为是**停止**：打印固定提示并原样回显安装命令，不得改用其它解析器，也不得内置解析图纸。

| 退出码 | 含义 | 处理 |
|---|---|---|
| `0` | 依赖就绪 | 继续 |
| `20` | 缺 `cad-file-reader` 或版本 < 0.41.0 | 停止，回显安装命令 |
| `21` | 缺 `lis-skill-bus` 或版本 < 0.1.11 | 停止，回显安装命令 |
| `22` | 契约无效（版本/结构/来源/哈希/单位） | 停止，回 `cad-file-reader` 重新生成 |
| `23` | 直接传入 DWG/DXF/DWT | 停止，改走契约 |
| `24` | 证据不足，或只有手工来源却要求正式量 | 停止；仅手工契约可出 `final_quantity=false` 草稿 |

固定提示：`本技能不直接识图，请先安装并调用 cad-file-reader 生成 cad-contract.json，再经 lis-skill-bus 传入；不许 fallback 到内置解析。`


## 口径摘要（全文见 `references/on-demand.md`）

- 管长＝WIRE/PIPE/CABLETRAY 单线中心线水平投影（含弧长），不含立管与竖向。
- 回路匹配＝线段中点就近标注（默认 30m）；电线展开＝(管长＋两端 1.5m/端)×芯数；电缆＝管长＋两端预留。
- 桥架单段 ≤ `tray_max_segment_mm`（默认 50m）才计入，超长段按异常单列。
- 订货量＝净量×(1+损耗)，规则见 `references/loss_rules.json`；规范口径分快算量/GB 50856 清单/商务概算/物资计划。
- 未标注管径按邻近已标注兜底并标推测；立管同号跨图只计 1 根并标 [推测]。

图层匹配、市政管长、版本概况与口径全文见 `references/on-demand.md`。
## 强依赖底座（cad-file-reader，不做弱化）

`cad-file-reader >= 0.41.0` 与 `lis-skill-bus >= 0.1.11` 是**显式强依赖**：DWG/DXF/DWT/PDF 解析、图层/文字/块/图框/几何与测量候选全部由底座完成，一次解图全项目复用；本技能只做安装专业口径的量算、扣减、损耗、分账与台账，输出概算底稿/物资计划草稿。缺底座或版本不足必须报错，不静默用错数据。

- 先跑 `python3 scripts/mep_plan.py --check-deps`：缺依赖 exit 20/21（缺 reader 20、缺 bus 21）并打印安装命令；本技能不自动下载、不自带解图器。
- `mep_scan.sh --contract` 只消费契约 JSON、不再打开 DWG；`mep_plan.py` 只读 `.scan.json`；Python ≥3.10 + openpyxl。
- 契约经 `lis-skill-bus` 按 `cad-contract/v1` 共享，不回退本技能解图；手工契约必须 `--allow-manual`，结果 `final_quantity=false`。完整架构见 `references/base-contract.md`。

## 依据

规范只存口径与边界，不复制全文。参考 GB 50856、GB 50500、GB 50015、GB 50084、GB 50116、GB 51309、GB 51348、GB 50974、GB 50261、GB 50303、GB 55024 和 GB 50166；详见 `README.md` 与 `references/standard_rules.json`。

## 边界（必须随结果告知）

1. 输出是概算底稿和物资计划草稿；不是定额级清单、结算量或竣工计量。
2. 不输出金额、单价、措施费、规费和税金。
3. 未含竖向实测长度、管件、套管；立管识别只按图面编号折算；支架仅按间距估算。
4. 回路标注覆盖不到的管长归「图层分档-未出量」，并给出主规格候选；不擅自按主规格回填数量，需人工确认后分档。
5. 水专业邻近管段兜底只是计划口径补充，抽查主干变径点后再提报。
6. 同一设备出现在多张图时按各图分别计数后合计，跨图重复需人工剔除。
7. 天正自定义实体的投影线可能与实际管线有出入，抽查 3~5 处回图核对后再提报。
8. 设备/材料表跨图重复会标注“跨图重复”；乱码名称不得猜测。
9. `CAD测量候选核对` 中的值只作识图证据，`final_quantity=false`；不得直接当管长、材料量或结算量。

## 判定与升级路径

- 交付必须附“匹配率 + 歧义回路数 + 需人工核对项 + 规范约束覆盖状态”。
- 需要定额级清单、对量、结算或竣工计量：超出本技能边界，改用专业软件建模。

## lis-skill-bus 联动

- 算量链必须安装并先查 bus；命中 `cad-contract/v1` 后直接复用，不重复解图。
- 安装核心 section 为 `circuits` / `route_segments`；已有契约输入时只读消费，禁止本技能自行解图。
- 安装、路径优先级和 Windows 用法见 `docs/bus-integration.md`。

## QTO 联动

可选目录级登记规则见 `docs/integration.md`；只登记输入、输出与缺口，不替代本技能算法和复核。

## 运行时

`scripts/*.sh` 自动解析 Python、cad-file-reader 和依赖路径。排障与手工安装见 `docs/runtime.md`。

## 授权与保留

CC-BY-NC-SA-4.0，仅限非商业用途。商业使用（含承接造价/算量咨询业务）须另行取得作者书面授权；作者保留全部商业权利（商业使用、再发布、封装收费、授予第三方商业授权）。条款全文见 `LICENSE.md`。

