# 线条形泪滴的修改与删除

本例验证 `teardrop-plan` → `teardrop-modify-plan` → `teardrop-delete-plan` 的维护链：
先修改旧泪滴的尺寸，再把修改后的泪滴删掉，主走线和其他对象保持不变。它是定向回归，
不是整板 E2E，也不涉及原生 `TEARDROP` 对象。

## 来源与开始状态

来源为 PR #285 的现场定向验证（Web EasyEDA Pro 4.1.78，Connector 1.14.2）。
从新建的空白测试工程开始；原理图与 PCB 都只含下面两颗电阻，没有其他铜。

## 参数（单位 mil，y 向上）

- 器件：官方库 C17414 / R0805，R1=(400,400)、R2=(800,400)，均为 TOP、0°。
  实测焊盘 44.6×54.2，焊盘中心相对器件 x=±39.4。
- 网络：R1.1=`TEST_A`，R1.2=R2.1=`TEST_LINK`，R2.2=`TEST_B`。原理图与 PCB 对应器件使用
  相同且唯一的 `uniqueId`，运行 `pcb import-changes`（不加 `--sync-attrs`）对齐网表。
- 板框 (200,200)–(1000,600)；10 mil 主走线连接焊盘中心 (439.4,400)–(760.6,400)。
- 修改比例：`--length-scale 0.8 --base-scale 0.8`。

## 步骤

每个阶段后都执行同一验收链：重铺铜 → 保存 → 关闭重开 → `pcb dump --include-copper` 新回读 → DRC。

1. 基线：放置器件、对齐网表、画板框与主走线。
2. 创建：从新回读运行 `teardrop-plan`，apply 得到两处、四条泪滴线。
3. 修改：以第 2 步的计划为 `--from` 运行 `teardrop-modify-plan`，apply。
4. 删除：以第 3 步的修改计划为 `--from` 运行 `teardrop-delete-plan`，apply。

## 观测

- 四个阶段重开后 DRC 均为 `passed:true`、0 项。
- 修改阶段删除四条旧线、创建四条新线；删除阶段清除全部四条新线。
- 器件、焊盘、板框及其他铜不变。宿主在泪滴尖端自动切分主干，段数依次为 1→5→7→7，
  但连续覆盖始终为 321.2 mil、线宽 10 mil。
- 最终 `pcb net-path --from R1.2 --to R2.1 --net TEST_LINK --layer 1 --json` 返回 `connected:true`。

## 错误与修法

只在 PCB 放器件而原理图为空时，DRC 会报 Netlist Error。修法是补齐原理图、保存并同步网表，
不能关闭该规则。

## 验证状态

`live-verified`：矩形 SMD 焊盘、双端入口、主干被宿主切分时的修改与删除。
泪滴边线被切分、圆焊盘及各拒绝分支仅有自动回归（`internal/app/cmd_pcb_pad_entry_test.go`）。
