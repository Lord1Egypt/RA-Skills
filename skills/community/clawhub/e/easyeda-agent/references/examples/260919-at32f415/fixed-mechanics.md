# 样例：90×50mm 板框、原点、安装孔与固定器件

## 来源

- `考试说明.pdf` 第 2 页：板框、原点、R3、锁定及四个 M3 孔。
- `考试说明.pdf` 第 3 页：U6、CARD1、CN1 的位置和角度。
- `物料清单.xlsx`：SCREW1-SCREW4 为 M3 实例；U6 为 AT32F415KBU7-4；CARD1 为 TF-115；
  唯一位号、封装和值见 [bom-instances.json](bom-instances.json)。

状态：`live-verified`。在 Web 3.2.203 的 `ceshi` 工程 PCB UUID `2e719e9419653c72` 中，本批固定坐标按 footprint anchor
写入；90×50mm、R3、10mil 板框、显示原点、四孔、U6、CARD1 和 CN1 的题定 y/角度均在
保存后回读保持。精简证据见 [live-validation.json](live-validation.json)。旧验证记录中曾出现整页
刷新恢复；它不再是允许的执行路径，后续持久化验证必须由有界 typed `doc reload` 完成。

## 开始状态

- `ceshi` 工程的目标 PCB UUID `2e719e9419653c72` 已与当前原理图绑定，板上存在 69 个导入实例；不要依赖重绑后可能变化的 Board 显示名。
- 尚未铺铜或布线；改板框不会遗留铜。
- 用 `pcb list --include-bbox` 确认 SCREW1-SCREW4、U6、CARD1、CN1 的新鲜 primitiveId。
- 题面只给“坐标位置”，没有定义 anchor/center。把 `coordinateSemantic` 作为显式来源参数；
  本 Demo 记录为 `footprint-anchor`。迁移题若来源未定义且 typed 元数据不能证明语义，则停止
  放置并标记该能力 `unsupported`，不得从属性面板或截图推断。

## 参数

换算常数：`1 mm = 39.37007874 mil`。保留 mm 作为题目源值，mil 只作为 CLI 输入。

| 对象 | mm 参数 | CLI mil 参数 |
|---|---:|---:|
| 板宽 × 高 | 90 × 50 | 3543.307 × 1968.504 |
| 圆角半径 | 3 | 118.110 |
| 板框线宽 | 0.254 | 10.000 |
| SCREW1 | (3,47) | (118.110,1850.394) |
| SCREW2 | (87,47) | (3425.197,1850.394) |
| SCREW3 | (3,3) | (118.110,118.110) |
| SCREW4 | (87,3) | (3425.197,118.110) |
| U6 | (45,25) | (1771.654,984.252) |
| CARD1 | (79.5,25) | (3129.921,984.252) |
| CN1 | (x,42) | (x,1653.543)，x 在关键路径布局后求解 |

上表只完成数值换算，不声明坐标基准。执行参数另有
`coordinateSemantic = footprint-anchor | bbox-center`。本轮来源参数为 `footprint-anchor`，typed
回读负责核对写入的 x/y、rotation 和 bbox；迁移到其他来源或封装时必须重新提供或由 typed
元数据证明该参数。

板框的数据坐标取 `[0,0]` 到 `[3543.307,1968.504]`，所以左下显示原点设置为 `(0,0)`。
若迁移到已有非零坐标板框，先读 `centerlineBBox`，再根据接口回读的 offset 语义计算显示原点；
不能移动全板几何来伪造坐标显示。

## 命令与步骤

### 1. 读取当前板和器件

```bash
easyeda pcb board-info --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb layers --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb outline-get --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb list --include-bbox --include-pads --doc <PCB_DOC_UUID> --project ceshi
```

记录当前铜层数、板框状态和目标实例 ID。若板上已有铜，先另存证据并决定是否重建；本样例不在
带铜状态下直接改轮廓。

### 2. 生成并写入真圆弧板框

`outline-round` 使用一个锁定的 BOARD_OUTLINE polyline，四角为原生 90° ARC，线宽固定 10mil。
先看 dry-run 的 `outlineFormat/source/width/height/radius/locked`：

```bash
easyeda pcb outline-round --rect 0,0,3543.307,1968.504 --radius 118.110 \
  --dry-run --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb outline-round --rect 0,0,3543.307,1968.504 --radius 118.110 \
  --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb outline-get --doc <PCB_DOC_UUID> --project ceshi
```

验收读取 `centerlineBBox`，不用含描边的 rendered bbox 判断尺寸：

- `width≈3543.307mil`、`height≈1968.504mil`；
- `radius≈118.110mil`、`sourceArcs=4`（`nativeArcs` 同值）、`outlineFormat=arc-polyline`；
- `arcs/legacyArcs=0`，因为本例的圆角保存在 polyline source 中，不是旧式独立 arc 图元；
- `lineWidth=10mil`、`locked=true`。

允许的差值只来自输出小数舍入，不通过增大板框补偿描边。

### 3. 设置显示原点

```bash
easyeda pcb origin get --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb origin set --x 0 --y 0 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb origin get --doc <PCB_DOC_UUID> --project ceshi
```

`origin set` 只改变编辑器显示坐标，不移动器件或板框。保存原点前后的板框和一个器件数据坐标，
确认它们完全不变；回读 offset 为 `(0,0)`。

### 4. 读取坐标语义参数，旋转、放置并锁定固定器件

从样例参数或当前题目来源读取 `coordinateSemantic`。用 `pcb list --include-bbox` 回读原生 `x/y`
与 `(bbox.min+bbox.max)/2`，只核对所选转换的结果。若来源语义缺失或 typed 回读无法表达所需
坐标，停止该步骤并记录接口缺口；不得凭截图猜中心。下面 `<..._ID>` 来自步骤 1 的新鲜结果。

若确认界面坐标对应 footprint anchor，使用 `--patch` 写 x/y：

```bash
easyeda pcb modify --id <CARD1_ID> \
  --patch '{"x":3129.921,"y":984.252,"rotation":90}' --doc <PCB_DOC_UUID> --project ceshi
```

若确认界面坐标对应 bbox center，先旋转、重读 bbox，再使用 `--center`。以下完整命令属于这个
分支，在完成现场语义探测前不得照抄执行：

```bash
easyeda pcb modify --id <SCREW1_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW1_ID> --center --x 118.110 --y 1850.394 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW2_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW2_ID> --center --x 3425.197 --y 1850.394 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW3_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW3_ID> --center --x 118.110 --y 118.110 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW4_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <SCREW4_ID> --center --x 3425.197 --y 118.110 --doc <PCB_DOC_UUID> --project ceshi

easyeda pcb modify --id <U6_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <U6_ID> --center --x 1771.654 --y 984.252 --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <CARD1_ID> --patch '{"rotation":90}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <CARD1_ID> --center --x 3129.921 --y 984.252 --doc <PCB_DOC_UUID> --project ceshi

easyeda pcb lock --ids <SCREW1_ID>,<SCREW2_ID>,<SCREW3_ID>,<SCREW4_ID>,<U6_ID>,<CARD1_ID> \
  --doc <PCB_DOC_UUID> --project ceshi
```

CN1 暂不锁 x。先旋转为 180°，把 y 设为 1653.543mil；x 在 CAN 120Ω、ESD 和顶层通道一起
排布后写入。下面仍是 `bbox-center` 分支；若现场确认 anchor 语义，改为 `--patch` 写 x/y：

```bash
easyeda pcb modify --id <CN1_ID> --patch '{"rotation":180}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <CN1_ID> --center --x <CN1_X_MIL> --y 1653.543 --doc <PCB_DOC_UUID> --project ceshi
```

### 5. 回读、保存与重开

写后立即读取可能带 `staleRisk`，它是事实提示而非拒绝。该次读取可用于定位明显差异，但最终
持久化证据必须走保存、重开、再读取：

```bash
easyeda pcb save --doc <PCB_DOC_UUID> --project ceshi
easyeda doc reload <PCB_DOC_UUID> --project ceshi --json
easyeda pcb outline-get --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb origin get --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb list --include-bbox --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb layout-lint --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb check --doc <PCB_DOC_UUID> --project ceshi --json
```

若 `doc reload` 在 Web 版留下持续加载动画，不循环重试或继续写入：保存错误和当前 typed
回读，将持久化结果标为 `incomplete`。先修复 `doc reload/open` 接口，再执行同一组读取；
禁止刷新浏览器或从工程树手工恢复。

## 观测

- 板框：中心线尺寸、R3、10mil 线宽、4 个原生弧和锁定状态都由 `outline-get` 返回。
- 原点：显示 offset 已设置，板框/器件数据坐标没有变化。
- 坐标语义：执行记录保存显式 `coordinateSemantic`，并用 typed x/y 与 bbox 回读核对转换结果。
- 固定件：六个实例按已确认的题目坐标语义、rotation、TOP layer 和 locked 回读均符合题目值。
- 半固定件：CN1 按同一坐标语义的 y/rotation 符合题目，x 有来源于 CAN 通道的参数记录。
- 机械：孔/器件完整 bbox 在中心线板框内；LCD 等后续禁放区不与六个固定件冲突。

## 常见错误与修法

| 错误 | 证据 | 修法 |
|---|---|---|
| 用 rendered bbox 得到 90.254×50.254mm | bbox 包含 10mil 描边 | 改读 `centerlineBBox/width/height` |
| 用折线近似圆角 | `sourceArcs=0` 或 source 无 ARC | 重新运行当前 `outline-round`，不得用旧 `--segments` 路径 |
| 来源未定义就假定题面坐标是中心 | 无法证明 anchor/center 映射 | 将语义标 `unsupported`；先补 typed 元数据或来源参数，再选 `--patch` 或 `--center` |
| 在 center 语义分支先移动后旋转 CARD1 | 旋转改变 anchor→center 偏移 | 先旋转、再读取、再按 center 移动 |
| 把显示原点当几何平移 | 所有器件坐标改变 | 恢复几何，使用 `pcb origin set` |
| 修改后只看即时读取 | 输出带 `staleRisk` 或重开后值消失 | `pcb save` → `doc reload` → 最终回读 |
| CN1 提前固定 x | CAN/ESD 顶层通道被堵 | 保留 x 自由，排完关键路径再求解 |

## 验证状态

- `offline-verified`：单位换算、原生 ARC 参数、origin/modify/lock 命令签名及离线测试。
- `live-verified`：本批为 footprint anchor；中心线 90×50mm、R3、10mil、4 个原生弧、原点、
  六个固定件和 CN1 约束均在保存及整页刷新后保持。
- 已知例外：CN1 在题定 y=42mm/180°时，rendered bbox 顶边约超中心线板框 1.17mil；焊盘在板内。
  保留题目约束并用 typed bbox/pad/region 数据判定真实本体与 courtyard，不静默改 y；数据不足
  时保留例外为未验证。
