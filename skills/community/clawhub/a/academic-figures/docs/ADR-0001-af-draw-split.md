# ADR-0001：af_draw / gen_figure 巨石模块分阶段拆解

- 状态：Partially adopted（v6.2.0 af_resilience / v6.5.0 af_shared / v6.9.0 GENERATORS wrapper 通路已落地；af_draw 渲染层与 gen_figure 编排仍在拆分推进中，行预算锁 <3600 与 sync_engine 镜像门禁随本 ADR 约束执行）
- 日期：2026-10-23
- 决策人：主理人（用户）；执笔：ZCode 会话

## 背景

v5.8.0 时点：`scripts/af_draw.py` 4,702 行（37+ 图型渲染全部内联）、`scripts/gen_figure.py`
3,506 行（CLI+校验+stats 粘合）。行预算守卫（tests/run_tests.py
TestV40000）曾在 v2.8/v5.7.0 两次松绑。巨石化的真实代价：

1. **回归面**：任何图型改动都在同一命名空间，互相踩踏风险随行数增长；
2. **审计面**：只读审计/新贡献者定位成本高；
3. **发包面**：平台打包单文件体积与加载时间。

## 决策

分四刀拆解（每刀独立发版、金标 37/37+全量电池双闸保护，禁止一刀多动）：

| 刀 | 内容 | 目标 |
|---|---|---|
| 第一刀 | `af_v23_charts.py` 中与 af_draw 重复的旧渲染函数退役（先审引用） | -400 行 |
| 第二刀 | stats 粘合层出 `af_stats_glue.py`（`_run_cox_forest`/`_run_cox_subgroup`/`--stats auto` 等 CLI 无关部分） | gen_figure <3000 |
| 第三刀 | af_draw 按族拆 `af_draw_medical.py`（km/cif/nomogram/roc…）与 `af_draw_meta.py`（forest/funnel/galbraith…） | 单文件 <2500 |
| 第四刀 | 主题/期刊预设/字体注册表出 `af_theme.py` | 单文件 <2000 |

## 约束

- 每刀发版前：全量电池 + 金标回归（templates/*.json 结构基线 ±60% 尺寸带）+ SH 指纹比对；
- **不改任何对外行为**：CLI 参数、输出文件、stderr 文案逐字节兼容；
- 拆分期间冻结新图型（避免在移动中的地板上铺砖）。

## 后果

- 短期：无用户可见变化；行预算守卫随每刀收紧（本次 3600 为上限，第二刀后应收回 3400）；
- 长期：审计与贡献成本下降，为"图型贡献格式"（长期路线）铺路。
