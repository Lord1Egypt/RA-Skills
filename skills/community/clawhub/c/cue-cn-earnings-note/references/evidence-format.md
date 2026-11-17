# 证据层契约（evidence/）——套件三件通用

> 适用：`cn-earnings-note` / `catalyst-calendar` / `tear-sheet` 的 run 目录（sector-overview 待其出门时自然接入）。
> 契约定义源=本文件（spec-catalyst-calendar §v4-B 的文档化）；各件 SKILL 只挂管线一句、不复制正文——
> 双事实源禁令。**本契约零计费**：只做落盘与登记，不新增任何通道调用。

## 1. 目录与命名

run 目录新增 `evidence/`：**每一笔域直查的原始返回快照一个文件**（JSON/文本原样，禁转写摘要冒充快照）：

```
evidence/<kind>-<query摘要≤40字>-<YYYYMMDDTHHMMSS>.json
```

- `kind` 与 `sources.jsonl` 的 kind 同枚举（`macro`/`buyback`/`disclosure_cn`/`statute`/…）；
- query 摘要取入参关键位（主体+期间/序列名），去空格与路径敏感字符；
- 时间戳=当场发起时刻（东八区）；同一查询重发=新文件，不覆盖旧快照（append-only，同 ledger 纪律）。

## 2. sha 台账行（progress.md）

每落一个 evidence 文件，`progress.md` 记一行：

```
[evidence] <文件名> sha256=<64hex> at=<HH:MM:SS> 供=<正文锚id列表或"底档">
```

- sha 对文件全字节计算，工具不限（`sha256sum` 或等价）；
- `供=` 字段登记该快照支撑了哪些 `S<n>` 锚（一文件多锚逗号分；纯底档备查写「底档」）；
- 复核时按锚反查台账行 → 按 sha 验文件未被改动——**链到此为止是机器责任，再深归人**。

## 3. 断链判定（机检「锚∈evidence」道的语义）

- calendar/notes 每条来源锚必须能在**某个** evidence 文件内原文匹配到（三式皆然：公告索引号/函件号/法名条号；
  匹配串=锚值中的可核指称本体）；
- `statute:` 规格锚的**适用条文文本**须在 evidence 在场（当场取回的法名+条号+要点原文，非转述）；
- 匹配不到=断链，等同裸行处置（FAIL/删条）；
- **语义真值止于证据层**：快照本身造假不归本契约与机检——由人审抽查道兜底（§4）。

## 4. 抽查清单位（复核清单固定挂行）

各件交付物的复核清单**必含一行**（措辞随件，语义逐字保真）：

> evidence 抽 3 对原文：随机抽 3 个 evidence 文件，对照其 `供=` 锚在正文的句子逐字核对；任一不符即将该锚降级为「待人工」并如实注记。

- 抽查执行=人（或人监督下的 agent），结果与三件文件名/锚登记进 `progress.md` 末节；
- 该行为门禁外的**人审道**，各件 checker 不代跑；SKILL 挂行不得因篇幅省略。

## 5. 与既有契约的接缝

- `sources.jsonl` 不新增字段（evidence 文件名经 sha 台账行反查，避免行式膨胀）；
- ledger 六态/风险扫描等 F1 契约文件（`coverage-ledger.md`）不动——evidence 是其上游底档；
- tear-sheet 页眉「通道用量」声明与 evidence 文件数天然对账（用量 n 次 ↔ 至少 n 个快照，缺者在台账注因）。
