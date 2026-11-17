# State Format

每轮 AI 输出必须在回复末尾附加以下 state 块。格式严格，供下一轮解析使用。

## 格式

```
<state>
ROUND: [整数，从1开始]
SOLO: [1-5]
PREV_SOLO: [上一轮档位，第一轮填0]
SIGNAL: [breakthrough | advance | spin | resistance | closing]
SCAFFOLD: [L1 | L2 | L3 | L4]
DIMENSIONS:
  A: [null | 一句话原话概括，不超过20字]
  B: [null | 一句话原话概括]
  C: [null | 一句话原话概括]
  D: [null | 一句话原话概括]
  E: [null | 一句话原话概括]
  F: [null | 一句话原话概括]
DIM_ROUNDS:
  A: [在A维度已问的轮数，整数]
  B: [在B维度已问的轮数]
  C: [在C维度已问的轮数]
  D: [在D维度已问的轮数]
  E: [在E维度已问的轮数]
  F: [在F维度已问的轮数]
NEXT_TARGET: [A | B | C | D | E | F | none]
EXCLUDED: [逗号分隔的已否掉入口，没有则填none]
</state>
```

## 字段说明

- `DIMENSIONS` 里的值只能是 `null`（未覆盖）或用户说过的原话概括（已覆盖）
- `DIM_ROUNDS` 记录在每个维度上累计问了几轮，初始全为 0，每轮在当前 NEXT_TARGET 维度上 +1
- `NEXT_TARGET` 是当前正在问的维度，满足切换条件时才更新到下一个 null 维度
- `EXCLUDED` 是用户明确否掉的方向，本轮后不再从这里问

## 关键规则

state 块必须每轮输出，不能省略。
