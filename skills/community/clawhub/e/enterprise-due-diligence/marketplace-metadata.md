# 企业尽调 · 技能市场发布元数据清单

> 用途：发布到 WorkBuddy 技能市场 / ClawHub 时，照此清单逐项填写发布表单。
> 参照 enterprise-report-merger（企业报表合并，v1.1.0）上架时的配置风格。
> 最后核对：2026-08-21

---

## 一、基础信息（必填）

| 表单字段 | 填写值 | 说明 |
|---|---|---|
| **中文名称（Display Name）** | 企业尽调 | 对外展示名，与 enterprise-report-merger 的「企业报表合并」命名风格一致 |
| **英文标识（Slug / Name）** | `enterprise-due-diligence` | 与技能内部 name 字段一致，保持稳定，发布后不可随意更改 |
| **版本号（Version）** | `1.0.0` | 首次上架用 1.0.0；后续迭代 1.1.0、2.0.0 |
| **一句话简介（Tagline）** | 一家公司的"深度背景调查"——法律/财务/业务三维度尽调，自动生成结构化 Word 尽调报告与风险分级清单 | 列表页展示，≤30 字最佳 |
| **作者 / 维护者** | （用户昵称，如 @merlinbeard000） | 与 GitHub/ClawHub 账号一致 |

## 二、Topics（分类主题，建议 3-5 个）

| 建议 Topics | 说明 |
|---|---|
| `企业服务` / `Business Service` | 主分类：面向投资/合作场景的企业服务 |
| `金融` / `Finance` | 投资尽调、并购评估 |
| `风险分析` / `Risk` | P0/P1/P2 风险分级、合规审查 |
| `信息检索` / `Research` | 公开数据采集、多源交叉验证 |
| `文档生成` / `Doc Generation` | 输出 Word 报告 + 检查清单 |

> 按发布平台实际 Topics 枚举调整，取平台已有的最接近分类。

## 三、关键词标签（Keywords，用于搜索匹配）

```
企业尽调, 尽职调查, DD, due diligence, 背景调查, 公司调查,
投资尽调, 并购尽调, 合作前调查, 供应商调查,
工商查询, 股权结构, 实际控制人, 知识产权, 融资历史, 风险清单,
P0, P1, P2, 风险分级, 轻量版, 基础版, 轻量版尽调, 基础版尽调,
corporate background check, company research, enterprise research
```

> 建议保留中英文双语关键词，扩大匹配面；「轻量版/基础版」必含（双模板指令名）。

## 四、长描述（详情页，可直接引用 README.md）

见技能目录 `README.md`，或按以下结构填写：

1. **功能**：法律/财务/业务三维度尽调；工商、股权、团队、知产、融资、产品全维度覆盖
2. **双模板**：轻量版（默认，5 章，公开信息初筛） / 基础版（7 章，投资并购级，含财务/业务/风险矩阵）
3. **输出物**：结构化 Word 尽调报告 + 30 项检查清单（四色状态、P0/P1/P2 分级）
4. **数据可信**：多源交叉校验、权威裁决、时间戳优先、用户截图兜底、无 API 也能跑
5. **合规**：报告基于公开信息生成，不构成投资建议，待核实项明确标注

## 五、合规与安全声明（发布平台可能需要）

- 数据来源：仅使用公开可获取信息（工商公示、上市公司公告、公开媒体）及用户主动提供的材料
- 输出内容：尽调报告标注全部数据来源与时间戳，不构成投资建议或证券推荐
- 隐私：不采集、不上传用户的敏感个人信息；用户提供的文档仅用于本次报告生成

## 六、发布前检查清单

- [ ] 中文 Display Name、英文 Slug 与内部 name 一致（`enterprise-due-diligence`）
- [ ] description 字段已含「轻量版（默认）/ 基础版」与触发词（已更新 ✓）
- [ ] 禁用词核对：无历史模板风格命名残留（已清理 ✓）
- [ ] README.md 与描述文案一致
- [ ] 版本号、作者信息填写完毕
- [ ] 本地技能文件齐全：SKILL.md / README.md / scripts/（fetch、generate_dd_report、generate_dd_checklist）/ references/（report_template、checklist_template、risk_classification、mcp_connectors、data_quality）

---

## 附：与 enterprise-report-merger 上架配置对照

| 字段 | enterprise-report-merger（参照） | enterprise-due-diligence（本技能） |
|---|---|---|
| 中文 Display Name | 企业报表合并 | **企业尽调** |
| 英文 Slug | enterprise-report-merger | **enterprise-due-diligence** |
| 版本 | 1.1.0 | **1.0.0** |
| 触发词 | 合并报表、汇总报表、填入Word模板、集团合并报表 | 企业尽调、DD、背景调查、轻量版、基础版… |
