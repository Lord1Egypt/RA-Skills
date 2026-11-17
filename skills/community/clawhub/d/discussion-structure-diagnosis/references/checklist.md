# Structure Checklist — Discussion 结构逐条检查清单

## 用途
配合 rubric.md 使用。本文件提供**逐条检查**的结构化清单，便于用户自检或 LLM 逐项诊断。

## 使用方法
按顺序检查每一项，✓ 表示通过，✗ 表示缺失，⚠ 表示弱。

---

## Section 1: Move Coverage（动作覆盖度）

- [ ] **A. Revisit results and explore implications** — Discussion 是否重述了关键 Results 但又有"so what"？
- [ ] **B. Map to literature** — 是否将结果与先前文献对比（confirm / contrast / extend）？
- [ ] **C. Identify applications** — 是否指出实际应用（real-world / methodological / theoretical）？
- [ ] **D. State limitations** — 是否有 limitations 段？**【关键】**
- [ ] **E. Suggest future work** — 是否有 future directions 段？
- [ ] **F. Achievement/contribution statement** — 是否有显式 claim 本研究的成就/贡献？**【关键】**
- [ ] **G. Opening move** — 第一句是 achievement 还是 reboot？

## Section 2: Move Ordering（动作顺序）

- [ ] Opening 在最前（F or G）
- [ ] A (revisit results) 在 B (map to literature) 之前
- [ ] D (limitations) 在 E (future work) 之前
- [ ] F (contribution) 不放在最末尾
- [ ] 无 Conclusion 内容混入
- [ ] Discussion 与 Results 没有大段重复

## Section 3: Intro-Discussion Symmetry（首尾对称）

- [ ] Intro Block 1（importance）↔ Discussion closing（broader implications）对应
- [ ] Intro Block 2（research map）↔ Discussion B（map to literature）对应
- [ ] Intro Block 3（gap/problem）↔ Discussion A（your response）对应
- [ ] Intro Block 4（describe present paper）↔ Discussion F（contribution）对应

## Section 4: Opening Move（开篇）

- [ ] 不是 "In this study, we investigated..." 反模式
- [ ] 不是与 Intro 完全重复的段落
- [ ] 第一句是 achievement claim 或 reboot

## Section 5: Take-Home Message（核心信息）

- [ ] 读完第一段能概括 take-home
- [ ] 读完最后一段 take-home 仍然清晰
- [ ] 中间段落不偏离 take-home
- [ ] Closing 重申或扩展 take-home

## Section 6: Limitations（局限性）

- [ ] 至少有 1 个具体 limitation（不是 generic "Our study has limitations"）
- [ ] 多个 limitations 时有序组织（First, Second, Third...）
- [ ] 部分 limitations 是否有反驳证据（如果有则更好）
- [ ] 不是 pure self-flagellation（不纯自我贬低）

## Section 7: Future Work（未来方向）

- [ ] Future work 不止 "more research is needed"
- [ ] Future work 包含具体方向
- [ ] 至少部分 future work 包含具体 sample / method / variable
- [ ] Future work 与 limitations 对应

## Section 8: Anti-Pattern Check（反模式检查）

- [ ] ❌ 无 "In this study, we..." 开头
- [ ] ❌ 无 "The aim of the present study was to..." 单独成段（除非 reboot）
- [ ] ❌ 无 "More research is needed" 单独成句
- [ ] ❌ 无 Results 大段重复
- [ ] ❌ 无 limitation 在最前段

---

## 严重度判定

| 缺失项数 | 严重度 |
|---|---|
| 0-2 | Minor |
| 3-5 | Major |
| 6+ | Critical |

---

## 相关 example 文件

参见 `examples/` 目录下的所有 good/bad example 文件作为对照。