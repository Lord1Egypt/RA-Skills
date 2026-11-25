# 能力覆盖对照

对照对象：[arjun988/blender-skills](https://github.com/arjun988/blender-skills) v1.3.0 —— 94 个技能 / 269 文件 / 292.2 KB / **0 行可执行代码**。

目的：证明「它能做的事，这里都能做」，且每条都有**可判定标准**与**可执行支撑**。下表按能力族而不是文件名列，因为对方 94 个技能里有大量重叠（同一件事按资产类型重复一遍）。

| 能力族 | 对方的做法 | 本技能对应 | 可执行支撑 |
|---|---|---|---|
| 统筹 / 导演调度（做整场景、多人协作、阶段推进） | `blender-director` 式总控提示词 | `SKILL.md` 三铁律 + `art-pipeline.md` Stage 0–7 + Brief 模板 | `asset_qa.py` 在 Stage 7 卡 gate |
| 参考图匹配（像不像） | `reference-image-match`：填表 → 相机 → 几何 → 材质 → 灯光 → 比对循环 | `art-reference-match.md` 九步闭环 + 分析模板 + 视觉验收清单 | MCP 截图逐轮比对；`standards.md §6` 相机/朝向口径 |
| 通用建模 / 块面 | 文字流程 | `modeling.md §1–2`（灰模 → 中模 → 高模的判据） | 面数审计、非流形/零面积面检查 |
| 硬表面（布尔、bevel、板缝） | 布尔与 bevel 的经验描述 | `modeling.md §3`：cutter 放 `COL_Booleans`、保留 live boolean、布尔后 bevel、宽度分级 | 非流形检查；`COL_` 归属审计 |
| 道具 | 面数档位表 | `modeling.md §4` + `standards.md §3` | `--tier standard/hero/small` |
| 载具 | 面数档位 | `modeling.md §5`（车身分级、可驾驶内构、轮轴枢轴） | `--tier vehicle/drivable`；scale/pivot 审计 |
| 建筑 / 环境 / 模块化 kit | 尺度与模块表 | `modeling.md §6` + `art-standards.md` 建筑尺度表 | `--tier module`；UV 图集包效率 |
| 植被 / 散射 | 少量描述 | `modeling.md §7` + `gn-vfx-sim.md §2`（GN 散射、代理、风摆） | 面数/材质数审计；GN 资产命名 `GN_` |
| 角色 / 生物 | 流程叙述 | `modeling.md §8`（比例、拓扑环、面部布线） | `--tier character/npc/crowd` |
| 雕刻 | 笔刷与层级 | `modeling.md §9`（multires、Dyntopo 选择、细节预算） | evaluated 三角面审计 |
| 重拓扑 | `retopo` 提示词 | `modeling.md §10`（极点管理、环线、影响区） | 影响数 ≤4、非流形检查 |
| UV | `uv-workflow` 概览 | `uv-texture.md §1–3`（接缝规则、TD 公式、pack、margin、UDIM） | **UV 存在 / pack 效率 / texel density 自动算** |
| 贴图 / 烘焙 / ORM | 参数列举 | `uv-texture.md §4–6`（bake 设置、cage、ORM 打包、色彩空间） | 贴图命名、分辨率、`_N/_ORM` 必须 Non-Color |
| 材质 / Master material / lookdev | PBR 描述 | `art-materials-lookdev.md`（数值表、材质数预算、lookdev 顺序） | 材质数、空槽、默认名审计 |
| 灯光 / 相机 / 渲染 | 三点光与采样建议 | `art-lighting-render.md`（色温表、采样、AgX、pass、无头渲染） | 渲染失败可复现命令；不影响静态审计 |
| 合成 / 调色 | 简单描述 | `lighting-render.md §6`（pass 组合、AgX vs Filmic、LUT 位置） | — |
| 绑定 / 权重 | `rigging` 提示词 | `rig-anim.md §1–3`（骨架层级、IK/FK、权重上限、变形测试） | **每顶点影响数自动统计** |
| 动画 / 面部 | 帧数建议 | `rig-anim.md §4–5`（帧率、走跑跳时长表、NLA、面部方案） | Action 命名 `AN_` 审计 |
| 毛发 / 布料 | 简述 | `rig-anim.md §6`、`gn-vfx-sim.md §4` | 缓存/代理提示 |
| 几何节点 / 程序化 | `geometry-nodes` 技巧 | `gn-vfx-sim.md §1–2`（生成器套路、Expose 规范、性能规则） | `GN_` 命名审计 |
| 物理 / 破碎 / FX | 列举 | `gn-vfx-sim.md §3–4`（刚体、布料、破碎、缓存） | — |
| 优化 / LOD | `optimization` + `lod` 提示词 | `optimize-export.md §1–2`（审计清单、LOD 生成与比例） | **LOD 链断号/缺 LOD0 自动检测**；三角比 |
| 碰撞 | 命名约定 | `optimize-export.md §3`（`_COL`、UCX/UBX、代理规则） | 命名与面数审计 |
| 引擎导出 | 导出参数表 | `optimize-export.md §4–6`（FBX/GLB/USD 参数 + Unity/UE/Godot 差异） | `--export-gate` 卡 `COL_Export`；变换审计 |
| QA / 验收清单 | `qa-review` + `validation-checklist` | `art-qa.md`（清单 + P0–P3 分级 + verdict 模板） | **`asset_qa.py` 全量落地** |
| 命名 / collection 规范 | `naming-conventions` | `standards.md §1–2` | 前缀与默认名审计、七层 collection 检查 |
| 面数 / 预算 | `polycount-budgets` | `standards.md §3` | `--tier` 12 档 |
| 流水线编排 | `asset-pipeline` | `art-pipeline.md` + 本表 | — |
| MCP 执行 | `mcp-tools` / `mcp-integration`（社区版工具表） | `art-mcp-execution.md`（**官方 add-on v1.0.3 的真实工具与限制**） | 批量 payload / 超时 / 后台模式坑 |
| 风格 / 世界观 / 情绪（60+ 包） | 每包 500–1100 字氛围文案 | `art-style-recipes.md` 配方表 + **`style_presets.py` 12 个可一键套用的 look** | 明确标注：表是美术方向提示；脚本部分是**可渲染的真实参数**（世界/雾/色温/相机/AgX） |

## 我们额外有的

| 项 | 说明 |
|---|---|
| **可执行审计** | `asset_qa.py`：13 类检查，`--tier` 12 档，JSON 报告，退出码可接 CI |
| **可执行风格** | `style_presets.py`：12 look 一键落地（世界/雾/三点光色温/相机/AgX），12×2 构建×2 引擎实测通过 |
| **量化验收** | look 也能量化（`mean` / `p05` / `p95` / 白场黑场占比），"太暗/过曝/灰平" 不再是主观判断 |
| **双构建实测** | 5.3.0（`02f0899d78e3`）与 5.2.4（`cd5dc428cce1`）双跑通过 |
| **版本守卫** | 每段 bpy 标适用版本；5.3 新能力不污染 5.2 兼容路径 |
| **官方工具口径** | 只写官方 add-on v1.0.3 真实存在的工具，不写社区版附加能力 |
| **可核对来源** | 数值标注来源与核验日期；MIT 归属在 `art-NOTICE.md` |

## 对方有而我们不做的

| 项 | 原因 |
|---|---|
| 60+ 风格包全文 | 64% 的 references < 300 B（多为一句话占位），属美术 brief 不是工程规格；压成配方表后信息密度更高且不误导 |
| 多宿主 `.claude/skills/` 目录复制分发 | 会造成内容多份漂移；改用「清单 + 软链」，且绝不再复制实体（ClawHub 曾因单文件超扫描预算被判 `CRITICAL`） |
| 其 bpy 片段 | `remove_doubles` / `transform_apply` 一类覆盖度低于 `knowledge/blender/plugin-code-templates.md`，且无版本守卫 |
| Poly Haven / Hyper3D / Hunyuan3D 工具 | 不在官方 MCP add-on v1.0.3 的 20 个工具内，照抄会写错工具名 |
