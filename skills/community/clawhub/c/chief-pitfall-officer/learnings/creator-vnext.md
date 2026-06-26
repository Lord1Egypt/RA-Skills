# Creator vNext 种子

由 L6.5 Knowledge Update 在每次知识库更新后生成。下次执行时，L2 Creator 加载此文件，将已验证的知识增量注入执行指令。

---

## 种子格式

| 字段 | 说明 | 示例 |
| :--- | :--- | :--- |
| `seed_id` | 唯一标识 | vNext-2026-001 |
| `source_delta` | 来源 Knowledge Delta ID | KD-2026-002 |
| `target_phase` | 影响阶段 | 阶段二（方案选型）/ 阶段三（执行蓝图） |
| `instruction` | 注入 Creator 的指令 | "当用户提及火锅店装修时，优先引导其注意消防通道宽度合规要求" |
| `effective_from` | 生效版本 | v2.0.0 |
| `status` | active / superseded | active |

---

## 种子记录

<!-- 由 L6.5 在知识更新后自动生成或更新 -->

| seed_id | source_delta | target_phase | instruction | effective_from | status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| vNext-2026-001 | KD-2026-002 | 阶段二（方案选型） | 当用户提及火锅店/餐饮装修时，优先使用1200-2000元/㎡作为基准报价，而非原800-1500区间 | v2.1.0 | active |
| vNext-2026-002 | KD-2026-004 | 阶段二（方案选型） | 当用户提及餐饮门店硬装时，报价审计基准调整为1500-2200元/㎡，并预警实际价格可能偏高20% | v2.1.0 | active |
| vNext-2026-003 | KD-2026-005 | 阶段三（执行蓝图） | 当用户提及餐饮装修项目时，在"应急预案"模块强制加入"增项加价"防范SOP，包含报价锁定条款和增项审批流程 | v2.1.0 | active |
