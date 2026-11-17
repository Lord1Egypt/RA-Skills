# ADR-0003: offline 封顶 partial，绝不判 verified

日期: 2026-10-11 · 状态: Accepted

## 决策

`--offline` 只做结构核验，判定上限 partial，**任何条件下不产出 verified**；
`--strict` 永远绕过磁盘缓存读。

## 背景

"没有联网核验就给 verified"是本工具能做的最坏谎言。离线的价值是诚实快速地
整理清单结构，核验结论必须出自联网注册库比对。同理，`--strict` 作为 CI 门
时如果读缓存，就失去了"这次提交的引用真的验过"的语义。

## 后果

- 离线报告一律带"未联网"标注，最高 partial
- 复跑速度与 CI 诚实性冲突时，诚实优先（缓存可 --no-cache/--refresh-cache 显式控制）
