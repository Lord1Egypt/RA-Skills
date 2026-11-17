# 旧模块对象归属恢复

状态：`offline-verified`。命令构造、完整文件输入输出、T 结拆分、同网非目标铜保留、
重叠歧义拒绝和输入覆盖保护已有自动化测试；这是旧对象归属的离线对账工具，不是
布局/布线验收，也不操作 EDA。

当已执行模块需要重算，使用当时实际执行的候选、完整成功的 apply journal 和新鲜
`pcb dump --include-copper` 恢复明确归属。不能把新候选当成旧现场的标准答案。

```sh
easyeda pcb module-owned --candidate previous/candidate-01.json \
  --journal previous/candidate-01.journal.jsonl --board fresh-board.json \
  --out previous-module-owned.json
```

输出是可放入 `modules[].existingObjects` 的 JSON 数组。每项保留 `kind`、新鲜
`primitiveId`、完整原始 `expected` 对象，以及包含候选/journal 原文件 SHA-256 的
`source`。后续执行必须再次比较 expected，现场对象变化就重新采集、重新生成。

对账规则：

- 旧候选 apply 与 journal 的哈希、步骤编号、动作和 captured PID 必须一致且完整成功。
- 只恢复旧 `bundle.groundRoutes`、`vias`、`regions`、`pours`；OSC 信号铜仍由既有
  `replacePrimitiveIds` 单独管理，不进入这个数组。
- 地线 PID 原样存在时检查真实层、网络、线宽和端点。宿主 T 结分段导致旧 PID 消失时，
  仅允许新鲜共线子段完整且无重叠覆盖旧段；每条新段只能属于一个旧段，不能按 GND 网名收集。
- via/region/pour 必须同时匹配原 journal 的 PID 和旧候选真实几何；不因附近出现相似对象而替代。
- 丢失、缺测、额外重叠、归属混淆、部分 journal、几何或参数改变都失败，不能输出部分归属数组。
- 所有未被明确证明归属的对象原样保留。实际铺铜只通过父 pour 归属随重建处理，禁止按其网名删除。

该输出仅声明可以重新计算哪些旧对象，不代表新候选通过验收。重新计算仍需通道检查、
apply dry-run、串行写入、保存重载、新鲜回读和独立 module-check。
