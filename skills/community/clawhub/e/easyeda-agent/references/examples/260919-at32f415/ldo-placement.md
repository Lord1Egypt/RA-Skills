# 样例：AMS1117 原理图、PCB 布局与顶层回流

## 来源

- `原理图.pdf` 第 1 页，“LDO-3V3降压电路”。
- `考试说明.pdf` 第 4 页的 LDO/滤波电容布局要求，第 7-8 页评分项。
- `物料清单.xlsx`：U2=`AMS1117-3.3`/C347222，C3/C5=`10uF`，C4/C6=`100nF`；展开实例见
  [bom-instances.json](bom-instances.json)。
- [source-connectivity.json](source-connectivity.json)：题图连接转录；仍须用真实库 pin/pad 映射核对。

第二轮参数化位置见 [ldo-layout-candidate.json](ldo-layout-candidate.json)，实际局部铜见
[ldo-route-live.json](ldo-route-live.json)。位置先由历史真实器件/pad 快照离线计算并交给独立
subagent 核查，随后在 `ceshi` 写入、保存、typed reload 并重新回读真实 bbox/pads；迁移时仍须
重复这套计算和回读，不能复制本 Demo 的绝对坐标。

状态：`live-verified`，范围仅限 U2/C3-C6 的局部布局与三网局部铜。U2.2/U2.4 与 C3-C6 的
原理图连接已逐端点对账；五件相对布局、15 段 TOP/20mil 铜和 0 过孔已保存并真实重开回读。
输入源到 C3、C6 到整板负载、整板铺铜与最终布通仍未完成。现场摘要见
[live-validation.json](live-validation.json)。

## 开始状态

- 原理图页已有 U2、C3-C6，器件身份和封装来自 BOM；PCB 已从同一原理图导入这些实例。
- 先确认 U2 的真实符号引脚和 SOT-223 焊盘，不从 `AMS1117` 名称推断现场 pin number。
- 该样例重排和布线 LDO 区，不给整板其他模块分配绝对坐标。

连接目标如下；这是本题的目标表，必须由 `sch read/connectivity` 回读证明：

| 对象 | 目标 |
|---|---|
| U2.1 `ADJ(GND)` | GND |
| U2.2 `VOUT(TAB)` | +3V3 |
| U2.3 `VIN` | +5V |
| U2.4 `TAB` | +3V3 |
| C3 10uF、C4 100nF | +5V ↔ GND |
| C5 10uF、C6 100nF | +3V3 ↔ GND |

## 参数

| 参数 | 本题值 | 迁移规则 |
|---|---|---|
| `core` | U2 | 换板后以实际 LDO 位号替换 |
| `inputOrder` | C3 → C4 | 按本题“先大后小”；其他器件以数据手册和项目要求为准 |
| `outputOrder` | C5 → C6 | 同上 |
| `inputNet/outputNet` | +5V / +3V3 | 从实际网表读取，大小写保持一致 |
| `placementGapMil` | 20-40 的初始搜索范围 | 由真实 bbox、焊盘和制造间距收敛，不是验收常数 |
| `powerWidthMil` | 主段 20，窄焊盘局部可到 8 | 仍须回读 PWR 规则和焊盘宽度 |
| `returnLayer` | TOP | 输入、输出电容 GND 均应有清楚的顶层回芯片路径 |

第二轮候选固定 U2 bbox center=`(1950,400)mil`、180°，将 C3/C4/C5/C6 都旋转到 90°：

| 器件 | 相对 U2 bbox center | 候选 bbox center | 目的 |
|---|---:|---:|---|
| C3 | `(-295,-50.6)mil` | `(1655,349.4)mil` | 输入 10uF，+5V pad 朝电源通道 |
| C4 | `(-206,-62.4)mil` | `(1744,337.6)mil` | 输入 100nF，位于 C3 与 VIN 之间 |
| C5 | `(+100,+227)mil` | `(2050,627)mil` | 输出 10uF，靠 VOUT/TAB |
| C6 | `(-50,+215.2)mil` | `(1900,615.2)mil` | 输出 100nF，与 C5 电源 pad 对齐 |

这组数值最初是从特定快照推导的搜索起点，当前 Demo 已现场采用并重开回读。C3-U4、C4-U2、
C5-U2 的 bbox 间隙约 12mil；迁移时必须把 U4、C10、R7、SW1、X1、C21 一并回读。
12mil 不是考试阈值。

PCB 坐标使用 mil、y 向上。位置计算基于焊盘和 bbox：先定 U2，再沿 VIN 侧按
`电源源头 → C3 → C4 → U2.VIN` 留直通通道；沿 VOUT 侧按
`U2.VOUT/TAB → C5 → C6 → +3V3 负载` 留通道。GND 焊盘朝向共同的顶层回流走廊。
这些是相对关系；不要复制另一块板的绝对 XY。
上述箭头表示铜线触达电容电源焊盘的顺序；电容仍并联在电源和 GND 之间，绝不能串联供电。
输出 `VOUT/TAB → C5 → C6 → 负载` 是本样例选择的布局方案，原题没有给唯一 PCB 路径。
迁移时结合实际稳压器手册、两只电容靠 VOUT 及顶层短地回路的要求重新决定，不把箭头当通用定律。

## 命令与步骤

### 1. 读取并核对原理图

```bash
easyeda sch read --page <SCHEMATIC_DOC_UUID> --project ceshi > /tmp/at32-ldo-read.json
easyeda sch connectivity --page <SCHEMATIC_DOC_UUID> --project ceshi > /tmp/at32-ldo-connectivity.json
```

从两个输出提取 U2、C3-C6 的 primitiveId、bbox、pins 和 pin→net，生成只包含这五件的
`/tmp/at32-ldo-measured.json`。空网引脚必须明确是 `nc` 或 `unconnected`；本模块不应靠新增
同名标签掩盖断线。

```bash
easyeda sch layout-plan --from /tmp/at32-ldo-measured.json \
  --out /tmp/at32-ldo-layout.json --report /tmp/at32-ldo-report.json
```

该命令只计算，不写编辑器。核对布局里的引脚位置和导线接触点，再用现有
`sch modify` / `sch wire` / `sch apply` 把同一份计划落地；现场 primitiveId 要从本轮新鲜读取中取。

```bash
easyeda sch read --page <SCHEMATIC_DOC_UUID> --project ceshi
easyeda sch check --page <SCHEMATIC_DOC_UUID> --project ceshi --json
easyeda sch drc --project ceshi --json
easyeda sch save --doc <SCHEMATIC_DOC_UUID> --project ceshi
```

### 2. 计算 PCB 相对位置并移动

```bash
easyeda pcb list --include-bbox --include-pads --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb nets --doc <PCB_DOC_UUID> --project ceshi
```

由 U2 的 VIN、VOUT/TAB、GND 焊盘中心和五个 bbox 计算目标中心。旋转会改变 anchor→center 偏移，
所以先单独旋转，再按 bbox center 移动；每个 `<...>` 都来自本轮参数计算。

```bash
easyeda pcb modify --id <U2_ID> --patch '{"rotation":<ROTATION>}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <U2_ID> --center --x <U2_X_MIL> --y <U2_Y_MIL> --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C3_ID> --center --x <C3_X_MIL> --y <C3_Y_MIL> --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C4_ID> --center --x <C4_X_MIL> --y <C4_Y_MIL> --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C5_ID> --center --x <C5_X_MIL> --y <C5_Y_MIL> --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C6_ID> --center --x <C6_X_MIL> --y <C6_Y_MIL> --doc <PCB_DOC_UUID> --project ceshi
```

回读 bbox 与 pads，确认没有重叠、所有件在顶层，且 U2.2/U2.4 都在输出侧的 +3V3 铜路径中。
旋转和 `--center` 移动分开执行；不能在同一条 `pcb modify` 中假设 anchor→center 偏移不变。

### 3. 走电源与顶层 GND 回流

用 `easyeda pcb track --help` 确认当前签名。每段起止点取焊盘末端，示例形态如下：

```bash
easyeda pcb track --x1 <X1> --y1 <Y1> --x2 <X2> --y2 <Y2> \
  --layer 1 --width 20 --net +5V --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb track --x1 <X1> --y1 <Y1> --x2 <X2> --y2 <Y2> \
  --layer 1 --width 20 --net +3V3 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb track --x1 <X1> --y1 <Y1> --x2 <X2> --y2 <Y2> \
  --layer 1 --width <PAD_SAFE_WIDTH> --net GND --doc <PCB_DOC_UUID> --project ceshi
```

需要多段时保持 45°或直线，并让顶层 GND 连回 U2.1；不能用底层铺铜的“同网”替代本题要求的
顶层回流观察。完成整板 GND 铜后再 `pour-rebuild`。

本次 Demo 的每段实际参数、primitiveId、路径理由和第一版输入 GND 的删除重建记录位于
[ldo-route-live.json](ldo-route-live.json)。复现时对 `segments[]` 逐项替换当前焊盘/转折坐标，
再执行上面的 typed `pcb track`；它是参数数据，不是可跨板复制的固定坐标答案。本轮实际修正使用：

```bash
easyeda pcb track-delete --ids 863ce641b2f229da,0d6ca5f1d717cf0d,164df762a004264f,8e77a8c59db709ba \
  --doc 2e719e9419653c72 --project ceshi
easyeda pcb track --x1 1744 --y1 365.2 --x2 1773 --y2 394.2 \
  --layer 1 --width 20 --net GND --doc 2e719e9419653c72 --project ceshi
easyeda pcb track --x1 1773 --y1 394.2 --x2 1773 --y2 460 \
  --layer 1 --width 20 --net GND --doc 2e719e9419653c72 --project ceshi
easyeda pcb track --x1 1773 --y1 460 --x2 1803.6 --y2 490.6 \
  --layer 1 --width 20 --net GND --doc 2e719e9419653c72 --project ceshi
```

这一修正来自实际回读：第一版路径从 C3/C4 汇合点绕向 U2，出现回头/重复风险；第二版保留
C3-C4 公共地段，从 C4.2 以 45°-直线-45°进入 U2.1。不能只凭命令成功判断，应继续运行下列回读。

```bash
easyeda pcb track-list --net +5V --layer 1 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb track-list --net +3V3 --layer 1 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb track-list --net GND --layer 1 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb net-path --from C3.1 --through C4.1 --to U2.3 --layer 1 \
  --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb net-path --from C3.2 --to U2.1 --layer 1 \
  --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb layout-lint --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb check --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb drc --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb save --doc <PCB_DOC_UUID> --project ceshi
easyeda doc reload <PCB_DOC_UUID> --project ceshi --json
```

重开后再次执行 `pcb list/track-list/check/drc`。只有实际输出证明连接、间距和保存均存在时，才把
该次实例标为 `live-verified`。

`pcb net-path` 用于读取铜图并证明指定焊盘间的轨迹关系；若当前安装版尚未提供该命令，保留
各项 `list` 原始输出做离线构图，不用截图或“同网名”替代路径证据，也不因此改走 GUI。

本次新 CLI 在旧连接器 1.5.1 上按 fail-closed 规则返回
`result.arcsAvailable is not true`，没有把未知圆弧读取误当成“无圆弧”。因此当前现场路径结论来自
保存重开后的原始 pads/tracks/vias 离线重建；加载能回传 `shape/rotation/specialPad` 与
`arcsAvailable` 的连接器后，还要复跑 shape-aware `pcb net-path`，不能把这次预期拒绝写成 PASS。

## 观测

- 电气：U2.2 与 U2.4 均为 +3V3；四只电容没有接反输入/输出侧；无新 NC 或浮空。
- 几何：五件 bbox 无重叠；两侧电容贴近对应焊盘，且未堵住焊接/扇出方向。
- 流向：+5V 先经过 C3/C4 区再到 VIN；+3V3 从 VOUT/TAB 清楚引出；GND 顶层回 U2.1。
- 制造：轨宽不超过窄焊盘；实际规则、`check` 与官方 DRC 分别记录。
- 现场：15 段均为 TOP/20mil，0 via、0 dangling、0 floating-island、0 duplicate、0 acute、
  0 non-orthogonal、0 foreign-pad overlap、0 clearance finding；69 件仍为 0 overlap、0 outside、
  0 tight-spacing。shape-aware `pcb check` 已用同一现场数据复测；旧连接器235个pads缺source shape
  的边界记录在 `limitations`。
- 官方 DRC 当前只有 216 个 `Connection Error`。整板尚未布通，所以它不能替代局部路径证明；
  本轮没有新增短路、间距或线宽类型。
- 独立 subagent 只读原题和保存重开后的原始回读，确认局部路径、线宽、转角、0 via、0重复和
  0异网碰撞成立；同时指出 U2.4 出线中心距焊盘上缘0.85mil、整板三网仍是局部岛、丝印与
  通用 decap 距离告警仍待后续步骤处理。20mil轨迹铜与U2.4矩形焊盘充分相交，shape-aware
  `pcb check` 已在同一现场数据上复测为非 dangling；迁移时仍要从真实焊盘端部重算。

## 常见错误与修法

| 错误 | 证据 | 修法 |
|---|---|---|
| 只接 U2.2，漏 TAB/U2.4 | `sch read` 的 U2.4 无 +3V3 | 修连接源数据并重新生成，不靠同名标签遮掩 |
| C3/C4 或 C5/C6 对调到另一侧 | pin→net 表与目标表不符 | 改连接；仅移动位置不能修电气错误 |
| 用中心点判断“靠近” | bbox/pad 显示实际焊盘仍很远 | 基于焊盘中心和可布通通道重算目标中心 |
| 移动后直接连续写旧 ID | 回读缺件或 partial | 新鲜 `pcb list`，按实际状态重算，避免盲重试 |
| GND 只靠底层铜 | 顶层 U2.1 到电容地没有连续路径 | 增加顶层短回流，再重铺铜并复查 |
| 用固定 30mil 半径判断大焊盘连接 | 旧 `pcb check` 把 U2.1/U2.4 铜面内的端点误报 dangling | 已改为按实际 pad shape/rotation 判断；同一现场复测 dangling=0，不手工补一根假线 |
| 旧连接器缺 `arcsAvailable` 或 pad shape | `pcb net-path` 返回 unknown/error | 更新 typed 连接器后复测；禁止退化为 AABB 假 PASS |
| 把 `beautify` 圆角当泪滴 | 没有真实 pad-to-track 泪滴对象 | 标记泪滴为 `unsupported`；补齐 typed 创建/回读接口后再重建铺铜 |

## 验证状态

- `offline-verified`：来源页、BOM、连接目标、命令名称和参数语义已核对。
- `live-verified`：第二轮相对布局已写入并保存重开；15 段局部铜和 0 via 已回读，离线铜图
  找到输入电源、输出电源及四条 TOP GND 目标路径。
- `incomplete outside scope`：输入/输出整板主干、双面 GND、泪滴、丝印、100% 布通和最终
  PCB DRC=0 尚未执行。
- 新 shape-aware `pcb net-path` 已通过离线反例测试，但当前 Web 连接器缺显式圆弧可用性与
  pad shape，现场正确拒绝；加载新版连接器后须复跑。
- 独立 Agent 已按上述盲核方式完成本轮检查；后续连接器升级后的 `pcb net-path` 仍须再次独立复测。
