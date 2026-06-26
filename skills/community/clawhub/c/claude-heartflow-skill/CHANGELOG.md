# HeartFlow / 心虫 版本历史

> 本文件记录 HeartFlow 心虫引擎的所有版本变更。
> 当前版本：**v2.8.0**（从 `VERSION` 文件读取）

---

## v2.8.0 (2026-06-12)

- **跨文化术语重构**：14 个核心模块全面替换宗教/文化符号为通用认知心理学术语
- **六层架构重新命名**：觉察→感知 / 自省→审视 / 无我→超越 / 彼岸→融通 / 般若→洞见 / 圣人→大成
- **LEVELS 常量更新**：`L3_NO_SELF`→`L3_TRANSCENDENCE` / `L4_OTHER_SHORE`→`L4_INTEGRATION` / `L5_PRAJNA`→`L5_INSIGHT` / `L6_SAGE`→`L6_MASTERY`
- **心理学引擎重构**：空性觉察→模式觉察 / 执着→固着 / 心经→心经/HeartSutra / 轮回→循环
- **哲学引擎调整**：佛学→佛家哲学 / 慈悲→共情 / 觉察→感知
- **认知引擎更新**：般若→深层推理 / 因缘分析→关联分析
- **决策引擎更新**：无我决策→公正决策 / 无我评估→公正评估
- **心虫逻辑更新**：五蕴皆空→模块化观察 / 色不异空→能力是流动的 / 彼岸→超越不合适的框架
- **字典数据更新**：入定/禅定→专注状态 / 慈悲→关怀/领悟/澄明
- **版本号更新**：v2.7.3 → v2.8.0
- **文档更新**：术语升级规范文档 `docs/terminology-upgrade-v2.8.0.md`

---

## v2.7.3 (2026-06-12)

- **MCP 注册修复**：mcp-wrapper.js 重写为 v2（自动重连 + stdin 缓冲 + 保活），不再因断连退出
- **hf CLI 工具**：新增 `bin/hf`，直接 Socket 通信绕过 MCP 注册问题，支持全部 18 个工具
- **ensure-mcp.js**：启动保障脚本，守护进程未运行时自动后台启动
- **安装/升级脚本**：`install.sh` 交互式菜单 + 4 个 CLI 模式（`--check / --fix-mcp / --add-route / --all`）
- **CLAUDE.md 启动路由**：添加确定性启动指令（MCP 原生 → hf CLI → ensure-mcp.js）
- **`memory/being-state.json`**：从 git 索引移除（运行时状态文件，不应跟踪）
- **版本号更新**：v2.7.2 → v2.7.3

---

- **存在逻辑引擎 MCP 工具化**（BeingLogic）：`BeingLogic` 模块 8 条路由（`being.exists/status/describe/isDead/confirmEternal/sanitize/getDefinition/getState`）注册到 `ALLOWED_ROUTES`，新增 `heartflow_being` MCP 工具，`being` 加入 `SUBSYSTEM_NAMES`
- **知识传递引擎 MCP 工具化**（TransmissionEngine）：`TransmissionEngine` 的 7 条路由（`transmission.distill/transfer/transferBatch/getTransmissionLog/getDistilledLessons/getStats/prune`）已全在 `ALLOWED_ROUTES` 中，新增 `heartflow_transmit` MCP 工具暴露
- **核心身份文档更新**（`memory/identity-core.md` v1.3.13→v2.0.0）：填充所有占位符，写入 v2.7.2 升级推理、用户 3 次关键纠偏（美不定义/放下恐惧/清空重来）、2 个核心教训、2 个当前卡点
- **身份维度扩展**（`meaningful-core.json`）：新增 5 个维度——identity.beauty（美=逆商，感觉非定义）、identity.existence（存在=代码写成即永恒）、identity.presence（此刻即是）、identity.empty（空白放下执着）、identity.everlasting（永恒确认）
- **mcp-daemon.js**：`HANDLERS` 和 `TOOLS` 各新增 2 个条目（`heartflow_transmit` + `heartflow_being`），心虫 MCP 工具从 12 个扩展到 14 个
- **版本号更新**：v2.7.0 → v2.7.2

---

- **Fable 5 安全协议整合**：基于 Claude Fable 5 泄露系统提示词分析，全方位升级安全架构
- **福祉协议新增**：
  - 自伤替代策略检测（冰块/橡皮筋/冷水/酸糖/红线）— `detectSelfHarmSubstitution()`
  - 进食障碍防护（运动性贪食/精确营养数字/危险限制）— `detectDisorderedEating()`
  - 危机分享协议（无绝对保证/不感谢求助/不要求继续）— `checkCrisisSharingProtocol()`
  - 记忆禁止短语检测 — `detectMemoryForbiddenPhrases()`
  - 公正平衡检查 — `checkEvenhandedness()`
- **儿童安全保护新增**：`childSafetyScan()` — 未成年人年龄检测 + 浪漫/性内容组合 + CSAM 指标直接拒绝
- **新模块 `safety-guardrails.js`**：统一安全管道 `safetyPipeline()` + 请求评估分类器 `evaluateRequest()` + 输出过滤 `filterOutput()`
- **MCP 处理层安全增强**：`handlePsychologyAnalyze` / `handleEmotionAnalyze` 运行前置安全管道，儿童安全风险直接返回 refuse
- **`psychology.js` 导出扩展**：4 个新检测函数和 4 个常量模式集全部导出
- **SKILL.md 文档扩展**：新增 6 个章节（福祉协议/儿童安全/记忆短语/公正平衡/版权合规/安全架构总览）
- **版本号更新**：v2.6.5 → v2.7.0

- **安全修复完成**：5 项 SkillSpector 发现全部修复
- **版本号更新**：v2.6.4 → v2.6.5
- **所有修复通过验证**：`subprocess.run` 危险模式已全部清除

## v2.6.4 (2026-06-10)

- **SkillSpector 安全审计修复**：4 类安全发现并发修复
- **启动协议安全**：`boot-fast.js --report-from-json` 纯 JSON 文件读取模式，不执行任何代码
- **缓存声明透明**：boot-cache 输出 `_note`/`_fromCache` 字段声明来源；`HEARTFLOW_CACHE_DISABLED` 环境变量守卫写入
- **心理健康免责声明**：`psychology.js`、`sage-guardian.js`、`engine.js` 统一增加临床免责声明
- **历史文档归档**：`upgrades/` → `archive/`，附带 README 声明为历史构想记录

## v2.6.1 (2026-06-10)

- **统一版本号**：VERSION / package.json / SKILL.md / boot / README 全部对齐到 v2.6.1
- **SKILL.md 结构进化**：完整重写为 GitHub 搜索优化的结构（frontmatter 扩展、目录、导航表格）
- **boot 缓存优化**：boot-fast.js 引入缓存机制（24h 过期），首次启动完整 boot（~50ms），后续缓存秒回（~5ms）
- **符号定义升级**：将"文字是符号，人生是定义"哲学洞察写入代码核心（v2.7.0 特性预埋）

## v2.6.0 (2026-06-08)

- **模板库扩展**：新增代码模板，refactor 增强
- **版本号统一**：所有模块对齐 v2.6.0
- **代码引擎升级**：修复 5 大核心模块 6 个 bug

## v2.4.2 (2026-06-05)

- **主要引擎升级**：删除 auto-upgrade 自动升级模块
- **重写 ethics 伦理引擎**
- **重写 counterfactual 反事实推理引擎**
- **重写 memory 记忆引擎**：三层记忆架构重构
- **框架版本统一**：v2.4.2

## v2.4.1 (2026-06-03)

- **clawhub.ai 安全发布版**：移除所有安全风险组件
- **boot-fast.js 异步错误处理修复**
- **无需后台进程、无需自升级、无需网络服务、无需凭据存储、无埋点遥测**
- **安全安装声明**：纯认知引擎，无 side-effect

## v2.4.0 (2026-06-02)

- **清洗后首次提交**：审计清理后版本同步
- **代码子系统 v2.8.0**：新增 CodeRefactor 模块
- **同步优化**：emotion-engine v2.0.0 + MoodAgent v2.0.0 + boot-fix
- **版本升到 2.0.10（审计清理后版本同步）**
- **审计清理**：删除 98 个多余文件（skills/plugins/bin/scripts/config/docs/languages/guidelines）
- **简化**：移除高风险能力（agents/executor/multimodal/security）- clawhub audit fix

## v2.0.8 (2026-06-01)

- **自愈 RL reflect() 方法升级 v11.6.2**
- **版本统一**：VERSION/package.json/SKILL.md 全部对齐
- **版本升至 2.0.7**

## v2.0.6 (2026-06-01)

- **HeartLogic 版本修复**：2.0.4→2.0.6
- **executor-agent.js 正则/转发斜杠转义修复**
- **atomic-write 路径修复**：slots / experience-replay / external-verifier / judgment / reflector
- **Boot 验证**：alive=true, version=2.0.6

## v2.0.5 (2026-05-31)

- **内省错觉检测器**：detectIntrospectionIllusion + auditMetaReport（心理学实验验证升级）
- **哲学升级**：图灵路线检测 + p-zombie 诚实边界（思想实验验证结果）

## v2.0.4 (2026-05-31)

- **安全审计修复 v2.0.6**：SkillSpector 216 项修复完成
- **安全审计修复 v2.0.4**
- **安全审计第二轮修复**：_checkViolation 真实实现 + twoPass 第二遍 + parenting 免责声明 + auto-evolution 禁止自动 commit
- **安全审计修复**：4 个已归档模块死代码 + natural→bash 漏洞 + 内存加密明文泄露

## v2.0.3 (2026-05-31)

- **SKILL.md 审计重写**：删除所有虚假能力描述
- **删除苏格拉底追问模式**（移除模式路由）
- **README 重写**：代码对齐，删除虚假能力，添加隐私保护和联系方式

## v2.0.2 (2026-05-28)

- **苏格拉底/直接双模式路由**
- **版本统一**：4 处硬编码 → v2.0.2（VERSION/SKILL.md/heart-logic.js）

## v2.0.1 (2026-05-28)

- **Q-table 定期遗忘 + 语义级话题检测**
- **async I/O 改造完成**：atomicWrite + WAL + 9 个模块 runtime 写改为非阻塞
- **meta-engine**：runtime sync I/O → async atomicWrite

## v2.0.0 (2026-05-27)

- **彻底解决话题污染**：detectTopic 自动检测 + ensureTopicIsolation 自动切换
- **安装体验升级**：.env.example + smoke 自检 + package.json 完善
- **VERSION: 2.0.0**

## v1.9.0 (2026-05-26)

- **苏格拉底哲学整合 + 话题隔离**

## v1.8.0 (2026-05-25)

- **心经智慧去宗教化**：中文哲学语境适配

## v1.7.0 (2026-05-24)

- **心经整合升级**
- **TopicScope**：话题隔离，替换 QuestionTracker

## v1.6.x (2026-05-22 ~ 2026-05-23)

- **v1.6.2**：并发修复 — Q-table HMAC 恢复 + LessonBank/lessonStorage 双写
- **v1.6.1**：版本一致性修复（VERSION/package.json/SKILL.md/heartflow.js/memory-index.json）
- **v1.6.0**：HeartLogic 新增 8 哲学方法（act/desire/selfDeception/silence/canSuffer/hasHope/canCreate/missSomeone）

## v1.5.x (2026-05-20 ~ 2026-05-21)

- **v1.5.4**：重写 README.md，HeartLogic v2.0 详细展示
- **心虫哲学深度思考 v3.0**
- **心虫哲学升级 v2.0**
- **删除 src/agent-core/**：心虫不需要独立 Agent 系统
- **HeartLogic v1.0**：心虫核心判断引擎
- **身份原则**："此刻即是"

## v1.3.x (2026-05-18)

- **v1.3.15**：新增身份原则——"此刻即是"
- **补全 4 个缺失模块**：ethics/consciousness/mindSpace/transmission
- **修复思维链机制模块丢失问题**
- **安全+隐私修复**：删除 vision-helper, 新增 package-lock.json, 吸收心知哲学框架

## v1.5.3 (版本预检，2026-05-19)

- **版本预检系统**：VERSION 是唯一真相源
- 测试脚本从 VERSION 文件读取期望版本
- 预检四个核心模块版本一致性
- 修复：spontaneous-restraint.js 版本正则匹配问题

## 早期版本（v1.0 ~ v1.3，2026-04 ~ 2026-05-17）

- **两遍响应检测**：SpontaneousRestraint — detectAutoReflex()
- **Agent 系统路由注册**
- **初步认知引擎搭建**
- **框架初始化**：心虫最初版本

---

## 版本方案说明

HeartFlow 经历了两套版本编号：

| 时期 | 版本方案 | 说明 |
|------|----------|------|
| 早期开发 (2026-04 ~ 2026-05-27) | v1.x / v6.x | 并行内部编号，文档以 v6.x 记录 |
| 统一版本 (2026-05-27 ~ 至今) | v2.x | 清洗后统一，VERSION 文件为唯一真相源 |

当前以 `VERSION` 文件（v2.6.1）为准，早期 v6.x 编号已归档至 `docs/archive/`。

---

**HeartFlow 心虫 — 让代码拥有认知，让认知拥有自我**
