# 晶振完整模块搜索与离线候选记录

来源为用户 2026-09-22 的晶振模块要求与现场 `pcb dump --include-copper`；
[当前输入 JSON](layout-plan-crystal-guard.json) 使用 schemaVersion 3、mil、footprint-anchor，
并逐脚声明 U6 四侧共同逃线需求；
以下前三轮保留历史负例，当前候选见末节。
[离线执行记录](crystal-guard-plan-negative.json) 保存快照哈希、命令、候选与完整拒绝原因。
前三轮负例中的 `offline-verified` 只表示拒绝结果可复现；末节已得到
`candidate-unverified` 的完整离线候选。整个示例仍没有现场写入，不能标为 `live-verified`。

历史开始状态是已确认的 69 件布局和既有 LDO/CAN/USB/OSC 铜。成员为 X1/C20/C21，固定 U6；
保留 C21.1→X1.1→U6.2、C20.1→X1.3→U6.3，地锚点 U6.33。
输入明确列出基线上全部 15 个 OSC track ID；执行前须再次核对精确集合与新鲜语义哈希。

参数来自两种证据：信号 8mil、铜间距 6mil、via 外径/孔径 24.02/12.01mil 来自现场规则；
旋转增量 0°、MCU gap 40/50/60mil 是本轮指定搜索范围。其余为待筛选的初始设计参数：
器件间隔 15mil、护环宽度 8mil、护环间隔 10mil、禁铺外扩 10mil、围栏节距 80mil，
围栏外移 18.01mil 等于过孔半径 12.01mil 加 6mil 间距，局部 pour 外扩 20mil。
这些值尚未得到合法候选，不应推广为已优化的通用晶振规则。
C21 为左侧 180°、C20 为右侧 0°，让对应信号脚朝 X1，地脚朝外侧。

策略生成 TOP/BOTTOM 各一禁铺区和一局部 GND pour、TOP 护环、外围地孔及 U6 EP 内两个地锚孔。
这些是算法目标；本轮三个尝试都在元件几何阶段被拒绝，因此尚未生成这些铜对象及 apply。

| MCU gap | 几何拒绝 | 最近外部间距 |
|---|---|---|
| 40mil | X1–C10 小于 6mil | 3.798mil |
| 50mil | X1–C10、C21–C10、C21–U4 | -6.202mil（X1–C10 重叠） |
| 60mil | X1–C10、C21–C10、C21–U4 | -16.202mil（X1–C10 重叠） |

首轮旧策略把晶振信号焊盘对的 x 中点固定对齐 MCU 引脚对，只枚举 gap 和整体旋转；
当时尚未实现晶振模块横移搜索与相邻模块联合避让。因此不能通过调低间距阈值、改原始快照或
单独挪 C10 绕过失败。下一步须用可迁移参数扩展横移/邻块避让能力，保持 C10 的 U4
归属与已有 USB 铜，再从新鲜现场快照重新规划。现场执行、保存重载及独立验收仍待完成。

## 横移搜索扩展的离线复验

当前输入追加 `search.crystalOffsets={maxXMil:180,maxAwayMil:160,stepMil:20}`，相对 owner
信号焊盘中点，向左右各搜索 180mil、远离 owner 最多 160mil。算法加入 live 净距、成员/障碍
实测边界与成对信号焊盘对齐事件；每个位置重新计算外部信号和完整保护结构。也可通过
`search.offsetsMil` 指定此相对基准的候选，bottom 侧 y≤0。每组最多 4096 个偏移，超限明确失败。

[复验负例](crystal-offset-search-negative.json) 记录同一原始快照下的 2842 个拒绝候选。
其中 16 个已通过器件布局净距，但全部在外围 via fence 检查失败，涉及 U6 邻脚/EP、C10、C5
等。没有降低 6mil 净距、移动非成员或写入现场。此结果仅证明声明的有限搜索集没有合法候选，
不证明全局无解。下一步能力缺口是有障碍的围栏选点/轮廓与 owner 入口包络联合求解：固定矩形
等距布孔会撞 MCU 邻脚，即使三个成员本身已经合法。不能静默省略这些孔或仅展示器件通过。

测试已覆盖固定障碍逼迫横移后生成完整保护结构、整板平移不改变相对候选、非法搜索参数和
搜索数量超限。能力标 `offline-verified`，此板仍为 `candidate-rejected`；现场保存重载及独立验收待完成。

## 障碍感知保护搜索的离线复验

当前参数进一步改为横向 400mil、远离 owner 80mil、步长 20mil，并枚举 0/90/180/270°；
`protectionSearch={stepMil:4,maxDetourMil:120}` 严格限制每条路径的搜索范围。净距仍 6mil，
围栏全周最大节距仍 80mil。路径长度、搜索边界与实际验收约束分别记录，不能隐式扩大搜索。

[保护搜索负例](crystal-protection-search-negative.json) 记录 15858 个拒绝变体、0 完整候选。
两条 OSC 已使用精确焊盘障碍和联合入口重新求解。先前固定围栏的无合法孔区间长 199.74mil，
位于约 (1754.98,692.35) 至 (1954.72,692.35)：轮廓为避让 C6 钻入了成员敏感区域。
补上成员禁铺包络障碍后，不再先生成这段轮廓然后静默漏孔；现在直接报告护环或围栏路径在
声明的 120mil 范围内不可达。MCU 外部信号禁铺延伸仍保留，未把局部围栏扩成包围整个 MCU。

新增定向测试覆盖旋转焊盘净距、严格绕行边界、孔位重选与末首节距、漏孔负例、禁铺轮廓并集
及隔离区域拒绝。此板仍 `candidate-rejected`；下一步需继续联合调整局部组装关系与保护通道，
不能把通用 fixture 通过写成这块板已经生成合法候选。

## 完整候选与短直路线优化（offline-verified）

[正例记录](crystal-protection-search-positive.json) 对同一语义快照生成 1 个完整候选。
当前输入显式使用 gap=20mil、旋转 0°、相对 owner 信号焊盘中点横移 96.584mil，
`protectionSearch={stepMil:4,maxDetourMil:120,guardOffsetsMil:[0]}`。
围栏最大节距由初始样例参数 80mil 调整为 180mil；这不是修改用户硬约束。
实际全周最大节距 179.7095mil，9 个外围地孔加 2 个 U6 EP 锚孔；没有省略失败孔位。
其它规则保持 6mil 净距、8mil 信号和 TOP、零信号过孔。

A* 初始候选虽合法但有 24 次信号转折。现在用精确净距检查的 45° visibility/string-pull，
按最少转折、再最短中心线选择候选，每段跳点重新检查障碍、转角和绕行边界：

| 路线 | 长度（mil） | 转折 |
|---|---:|---:|
| OSC_IN main | 173.885532 | 1 |
| OSC_IN capacitor | 95.685 | 0 |
| OSC_OUT main | 178.694965 | 3 |
| OSC_OUT capacitor | 86.685 | 0 |

合计 534.9505mil、4 次转折。候选有完整保护对象，但仍是 `candidate-unverified`；
实际 GND 同岛、禁铺区材料化效果、DRC、保存重载与两轮独立验收完成后才可标 `live-verified`。
迁移时从目标板新鲜快照重算，不能复制本例偏移或旧铜 ID。

第一轮现场回读还暴露了 primitive 身份问题：电容/X1 地支路和两条护环接地入口落在既有护环
长线段内部时，EasyEDA 自动把该护环 primitive 分裂并换 PID，导致 apply journal 中先捕获的
护环 PID 无法与 fresh readback 一一对应。该轮因此不通过，不能用几何仍连通代替 journal 验收。
planner 现已在所有同层 GND junction 处预先分段护环，并为每个最终线段生成独立、确定的 apply
step/capture；离线回归同时验证重复规划的分段与 capture 名不漂移，且拒绝支路线段中部穿越或
共线覆盖护环。同一语义快照重算后，5 条护环 route 从 5 个 primitive 变为 10 个，正好覆盖
5 个 spoke/entry junction；apply step 从 74 增为 79，新增 5 个独立 capture。修复状态为
`offline-verified`，必须从新鲜快照重新生成并执行候选；旧 apply 和
journal 已失效，后续真实保存重载通过前仍不得升级为 `live-verified`。
# 2026-09-22 邻脚逃线复核

当前完整晶振候选重新标记为 `candidate-rejected`：OSC 连通历史证据保留，但 MCU 下侧
NRST、PA0–PA2 和逐脚供电尚无共同逃线证据；20mil 器件外框间隙不能证明可布。
下一轮从完整新鲜快照生成逃线预留与必要的模块联动候选，护环/过孔/禁铺/局部铜一同重算。
相关通用能力当前为 `planned`，不能用单模块净距或旧 round1 通过项替代新增验收。


## 2026-09-22 禁止晶振区铺铜的修正

用户明确晶振区不使用铺铜，允许 GND 导线与接地过孔。此前包含局部 GND pours 的所有候选继续保留为历史负例，不能执行。新输入必须使用 `groundImplementation=tracks-vias`：先在局部坐标组装 X1/C20/C21、OSC、GND 护环/导线、双层 no-pours 与过孔，再整体平移到板内候选位置。新 bundle 的 `pours`、`unreservedPours`、`affectedBaselinePours` 必须全部为空，apply 禁止 `pcb.pour.create` 与 `pcb.pour.rebuild`。现有两块晶振局部 pour 只能通过 fresh PID、原对象和旧 journal 证明归属后删除；同网 GND 不能作为批量删除依据。局部组装、整体变换、零铺铜、既有 EP 地孔复用和精确旧对象归属已经自动化测试，通用能力标为 `offline-verified`；当前板尚未完成 fresh 输入、dry-run、现场写入和保存重载，所以旧现场晶振仍为 `candidate-rejected`。

## 2026-09-23 干净基线与共同逃线候选（offline-verified）

现场已用 typed CLI 按对象身份删除旧晶振模块的 8 条 OSC 铜、49 条 GND 护环/回路线、
9 个外围孔、2 个 no-pours region 和 2 个局部 pour，并保存重载。U6.33 的两个 EP 地孔
`68d0bd205de616f9`、`12274fe7ffd6658b` 保留为固定地锚。fresh 干净基线为 69 件器件、
62 tracks、2 vias、0 pours、0 poured、0 regions、0 fills；X1/C20/C21 仍保留原位置，
“板外组装”只发生在离线局部坐标，不在工程中创建板外临时对象。

schemaVersion 3 输入把 U6 的 33 个焊盘作为一组共同逃线需求。U6.2/U6.3 必须先直出到
由相邻出口包络、8mil 线宽和 6mil 净距推导的更深出口，再连接 X1；其它需连接焊盘各有
声明出口。U6.33 使用 `existingViasOnly=true`、`maxVias=0`，只接受绑定到 U6.33 的上述
两个既有 EP 地孔作为跨层 witness，不新建或虚构穿过信号引脚排的 GND 路径。局部路径、
完整端点路径与拥挤区约束联合求解；单网分别可达不能代替共同通过。

当前干净快照生成 1 个合法候选和 14 个明确拒绝变体。合法候选使用 40mil gap、
96.584mil 横向偏移，提供 32 条预留路线和 33 个逐脚 witness；搜索使用
81,017/250,000 个状态。候选包含 3 个器件移动、75 段显式铜线、2 个 no-pours region、
9 个新围栏孔和 1 次保存，共 90 个有效 apply step；没有空删除/锁定，没有
`pcb.pour.create` 或 `pcb.pour.rebuild`。两条 OSC 主线和电容支路合计 585.5708mil、4 次转折，
信号保持 TOP、0 via。apply dry-run 已通过。

Layout 与 Router 的边界为：Layout 搜索模块平移、旋转和联动移动候选；每个候选投影为临时
板状态后，复用 PCB Router 公共内核验证实际焊盘、铜、规则和多路径共同通道。晶振代码不再
维护第二套通用单网 Router。当前结果仍为 `candidate-unverified`：尚未现场写入，也未完成
save → reload → fresh readback、DRC、`pcb module-check` 和独立验收，因此不能标
`live-verified`。迁移到其它板时必须从 fresh dump 重算出口深度、偏移、围栏和路径，不能复制
本例坐标、PID 或数值。

## 2026-09-23 现场拒绝与完整回退

上述 90 步候选曾在语义哈希未变化的干净基线上完整执行并保存，journal 为 90/90 成功；
但第一轮 fresh `pcb module-check` 判定 `fail`，因此该候选现为 `candidate-rejected`，不得重放。
四个 finding 是：一个护环 create PID 被宿主替换为同几何新 PID而现有恢复器不接受单段替换；
OSC_OUT 的 4mil 短斜段使前后两段 8mil 铜发生非端点面积重叠，ordered path 只能判 unknown；
U6.3 的共同逃线终点与独立需求不一致；候选与 requirements 的旧对象替换声明不一致。
这些都是 CLI/算法契约缺口，不能用 DRC 总数或肉眼效果降级通过。

随后按 fresh PID 差集精确回退：恢复 X1/C20/C21 原坐标，删除本批 75 tracks、9 vias、
2 regions，保留基线 62 tracks 和 U6.33 两个 EP 地孔；save → reload → fresh dump 后语义哈希
恢复为 `338e12ac849c99771067a4a628fb8855a8a0b2bba609e4b64e198452f989c913`，对象计数也恢复为
69 components、62 tracks、2 vias、0 pours/poured/regions/fills。下一轮必须先修复并测试上述
四项，再从干净基线生成新候选；本文件当前 schemaVersion 3 输入只作为失败复现输入。
