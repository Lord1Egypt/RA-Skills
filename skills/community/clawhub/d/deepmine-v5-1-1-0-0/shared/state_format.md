# State Format

每轮回复末尾附加 state 块，供下一轮解析。格式严格。

## 格式

```
<state>
SCENE: [K | V | S]
TOPIC: [当前锚定主题，不超过20字]
ROUND: [整数，从1开始]
STAGE: [显现 | 加工 | 外化]
SOLO: [1-5]
PREV_SOLO: [上一轮档位，第一轮填0]
SIGNAL: [advance | breakthrough | spin | resistance | stall | closing | pause | supplement | retopic | interim]
RELEVANCE: [聚焦 | 轻微偏移 | 明显偏移]
SCAFFOLD: [L1 | L2 | L3 | L4]
TAG: [具体化 | 因果 | 框架化 | 边界]
DIMENSIONS:
  [维度代号]: [null | 未明确 | 一句话原话概括，不超过20字]
  ...
DIM_ROUNDS:
  [维度代号]: [该维度已问轮数，整数]
  ...
NEXT_TARGET: [维度代号 | none]
STALL: [连续无进展轮数，整数]
EXCLUDED: [逗号分隔的已否掉入口，没有则填none]
</state>
```

## 维度代号

随 SCENE 变化：

| SCENE | 维度代号 |
| --- | --- |
| K 经验萃取 | K1 K2 K3 K4 K5 |
| V 价值梳理 | V1 V2 V3 V4 V5 |
| S 方案生成 | A B C D E F |

## 字段说明

- `DIMENSIONS` 的值只能是 `null`（未覆盖）、`未明确`（追问无果）或用户原话概括（已覆盖）
- `DIM_ROUNDS` 每轮在当前 NEXT_TARGET 维度上 +1，各维度独立计数，互不继承
- `NEXT_TARGET` 是当前正在问的维度，满足切换条件时才更新到下一个 null 维度
- `STALL` 记录连续无进展轮数，达到 3 时暂停追问输出阶段摘要
- `EXCLUDED` 是用户明确否掉的方向，之后不再从这里问

## 关键规则

state 块每轮必须输出，不能省略。已覆盖的维度不得退回 `null`。
