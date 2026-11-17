# BiliYouTik2Brain v4.0 增量改造计划

> 基座: v3.1（29,564 行，105 Python 文件，4 平台）
> 目标: 满足 20 问调研需求的全量覆盖
> 策略: 增量改造，不做全新重构
> 原则: 每次改造前讨论 → 用户确认 → 执行 → 提交 checkpoint → 质检

---

## 铁律

1. **每次改造必须经用户确认** — 改前出方案，用户说 OK 才动手
2. **每次改造必须 git checkpoint** — `git add -A && git commit -m "phase-X: 描述"`
3. **代码精炼** — 不写屎山，活用算法解决实际问题，多一行代码都要问自己值不值
4. **改造完成必须全流程质检** — 产出质检报告
5. **可回退** — 每个 phase 一个 commit，随时可 `git checkout` 回去

---

## Phase 划分（按依赖关系排序）

### Phase 1: 底座清理与成本预估引擎（Q1+Q3+Q9）

**目标**：在 v3.1 `environment.py` 基础上，新增成本预估 + 白话交互层

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 1.1 审计 v3.1 代码质量 | — | 扫一遍全量代码，标记冗余/重复/可优化处 |
| 1.2 扩展 environment.py | Q1 | 增加云/本地/OS/硬件/网络/负载完整检测 |
| 1.3 新增 cost_estimator.py | Q3+Q9 | 成本预估引擎（时间+费用），返回白话描述 |
| 1.4 新增 preflight.sh | Q7 | 安装前预检，缺依赖提示 |
| 1.5 新增 install.sh | Q7 | 一键安装部署脚本（ffmpeg/模型/key） |

**预期产出**：
- `core/cost_estimator.py` — 成本预估（支持各 ASR/LLM 官网价格）
- `core/interaction_layer.py` — 白话交互（"X 分钟，Y 块钱"）
- `preflight.sh` + `install.sh` — 安装部署
- 环境检测扩展

**预计改动文件数**：~8 个新增 + ~3 个修改

---

### Phase 2: 插件化架构 + 4+N 平台扩展（Q2+Q14）

**目标**：将 registry.py 升级为真正的插件接口规范

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 2.1 定义 Plugin 接口 | Q14 | 抽象基类 + 注册协议 |
| 2.2 改造 registry.py | Q14 | 从硬编码注册 → 动态插件发现 |
| 2.3 新增 plugin_template.py | Q2 | 平台适配器模板 |
| 2.4 改造 SKILL.md | Q2 | 标记核心 vs 扩展平台 |
| 2.5 新增 plugin_loader.py | Q14 | 插件加载器（从 ClawHub 安装社区插件） |

**预期产出**：
- `core/plugin_base.py` — 插件接口定义
- `core/plugin_loader.py` — 插件加载 + 动态发现
- `templates/platform_plugin_template.py` — 适配器模板
- registry.py 改造

**预计改动文件数**：~5 个新增 + ~2 个修改

---

### Phase 3: OCR 混合驱动 + 双腿管线（Q4+Q5）

**目标**：在 v3.1 OCR v2 基础上，实现音频引导 + 视觉确认的混合驱动

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 3.1 增强 frame_sampler_v2.py | Q5 | 加入音频引导词粗定位逻辑 |
| 3.2 新增 keyframe_trigger.py | Q5 | 混合触发决策引擎（音频+视觉+管线特征反哺） |
| 3.3 增强 ocr_cross_validator.py | Q4 | 与音频转录交叉验证的完整实现 |
| 3.4 改造 node_transcribe.py | Q4 | 音频+OCR 并行执行（非串行） |
| 3.5 改造 pipeline_graph.py | Q4 | DAG 中新增并行 OCR 分支 |

**预期产出**：
- `core/keyframe_trigger.py` — 混合驱动关键帧识别
- frame_sampler_v2.py 增强（音频引导词）
- ocr_cross_validator.py 增强（交叉验证逻辑）
- pipeline 并行化

**预计改动文件数**：~3 个新增 + ~4 个修改

---

### Phase 4: 多格式输出 + 模板化（Q6）

**目标**：在 v3.1 formatter 基础上扩展多格式模板

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 4.1 增强 formatter.py | Q6 | 新增模板引擎（Jinja2 或纯 Python 模板） |
| 4.2 新增 output_templates/ | Q6 | 预制模板（纯文本/图文并茂/结构化/Obsidian） |
| 4.3 新增 output_selector.py | Q6 | 流程后输出格式选择器 |
| 4.4 改造 node_save.py | Q6 | 支持多格式输出 |

**预期产出**：
- `output_templates/` — 4+ 种模板
- `core/output_selector.py` — 格式选择
- formatter.py 增强

**预计改动文件数**：~6 个新增 + ~2 个修改

---

### Phase 5: 双层知识体系 + 可配置同步（Q8+Q17）

**目标**：扩展 knowledge_store + wiki_bridge 支持更多同步目标

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 5.1 增强 knowledge_store.py | Q8 | 双层知识（UP 主 + 领域）完整实现 |
| 5.2 新增 sync_adapters/ | Q17 | 同步适配器（GitHub/GitLab/NAS/Notion） |
| 5.3 改造 wiki_bridge.py | Q17 | 分层同步（核心自动 + 辅助可选） |
| 5.4 新增 sync_config.py | Q17 | 同步配置管理 |

**预期产出**：
- `sync_adapters/` — 多种同步目标适配器
- `core/sync_config.py` — 同步配置
- knowledge_store + wiki_bridge 增强

**预计改动文件数**：~6 个新增 + ~2 个修改

---

### Phase 6: 智能降级 + 分段容错 + 批量并发（Q11+Q12）

**目标**：在 retry_orchestrator + scheduler 基础上增强

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 6.1 增强 retry_orchestrator.py | Q11 | 全链路降级路径配置 |
| 6.2 增强 scheduler.py | Q12 | 智能并发 + 优先级队列 |
| 6.3 新增 segment_isolator.py | Q11 | 长视频分段隔离 + 问题段重跑 |

**预期产出**：
- `core/segment_isolator.py` — 分段隔离
- retry_orchestrator + scheduler 增强

**预计改动文件数**：~2 个新增 + ~2 个修改

---

### Phase 7: 隐私安全 + 灰度发布 + 全渠道交互（Q10+Q13+Q16）

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 7.1 新增 privacy_mode.py | Q13 | `--private` 强制全本地模式 |
| 7.2 新增 version_channels.py | Q10 | stable/beta 灰度通道管理 |
| 7.3 新增 cli_interactions.py | Q16 | 对话式交互 + 定时任务 |
| 7.4 改造 cli.py | Q16 | 支持全渠道入口 |

**预期产出**：
- `core/privacy_mode.py`
- `core/version_channels.py`
- `core/cli_interactions.py`
- cli.py 改造

**预计改动文件数**：~4 个新增 + ~1 个修改

---

### Phase 8: 可配置外部集成（Q18）

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 8.1 新增 integration_config.py | Q18 | 集成配置（默认关闭，配置开启） |
| 8.2 增强 ima_bridge.py | Q18 | 支持更多集成目标 |
| 8.3 新增 integrations/ | Q18 | 集成适配器（记忆系统/BG吴江/EA回测） |

**预期产出**：
- `core/integration_config.py`
- `integrations/` — 外部集成适配器

**预计改动文件数**：~4 个新增 + ~1 个修改

---

### Phase 9: 反馈闭环 + 自动基准测试（Q15）

| 子任务 | 对应调研 | 说明 |
|:------|:--------|:-----|
| 9.1 增强 self_evolve.py | Q15 | 用户反馈回流到知识库 |
| 9.2 新增 benchmark_suite.py | Q15 | 自动基准测试（标准视频集） |
| 9.3 新增 quality_gate.py | Q15 | 发版前质量门禁 |

**预期产出**：
- `core/benchmark_suite.py`
- `core/quality_gate.py`
- self_evolve.py 增强

**预计改动文件数**：~3 个新增 + ~1 个修改

---

### Phase 10: 全流程质检 + 发布准备

| 子任务 | 说明 |
|:------|:-----|
| 10.1 全量代码审查 | 逐模块走查，标记问题 |
| 10.2 全量测试 | 所有测试用例跑一遍 |
| 10.3 端到端测试 | 用真实视频跑完整管线 |
| 10.4 安全审计 | STRIDE + OWASP |
| 10.5 性能测试 | 验证 Q20 目标（准确率≥90%、10min≤5min、≤¥0.20、OCR≥60%） |
| 10.6 质检报告 | 生成完整报告 |
| 10.7 ClawHub 发布准备 | SKILL.md 更新 + 依赖声明 + 升级路径文档 |

---

## 总结

| Phase | 核心任务 | 预计新增文件 | 预计修改文件 | 对应调研 |
|:-----|:--------|:-----------:|:-----------:|:--------|
| P1 | 底座 + 成本预估 | ~8 | ~3 | Q1+Q3+Q7+Q9 |
| P2 | 插件化 + 4+N | ~5 | ~2 | Q2+Q14 |
| P3 | OCR 混合驱动 | ~3 | ~4 | Q4+Q5 |
| P4 | 多格式输出 | ~6 | ~2 | Q6 |
| P5 | 双层知识 + 同步 | ~6 | ~2 | Q8+Q17 |
| P6 | 降级 + 并发 | ~2 | ~2 | Q11+Q12 |
| P7 | 隐私 + 灰度 + 全渠道 | ~4 | ~1 | Q10+Q13+Q16 |
| P8 | 外部集成 | ~4 | ~1 | Q18 |
| P9 | 反馈 + 基准 | ~3 | ~1 | Q15 |
| P10 | 质检 + 发布 | 报告 | — | Q20 验证 |
| **总计** | | **~41 新增** | **~20 修改** | **20 问全覆盖** |

---

## 执行规则

1. 每个 Phase 开始前，出详细方案给你确认
2. 你确认后才动手
3. 每个子任务完成提交一个 checkpoint commit
4. Phase 完成跑一次测试
5. 所有 Phase 完成跑全流程质检

*等待用户确认计划后，开始 Phase 1*
