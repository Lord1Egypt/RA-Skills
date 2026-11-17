# 未成年人保护变体 · 合规说明（COMPLIANCE.md）

> 版本：V1.0 ｜ 日期：2026-09-25 ｜ 适用范围：`minor-protection/` 目录
> 关联代码：`SPL-anthropic-minor-engine.py`（SPL-Minor-V1）、`SPL-anthropic-minor-server.py`

---

## 一、范围与性质声明

本目录是一个**研究 / 演示性质的合规能力框架**，面向未成年（<18）情感陪伴场景，对主引擎施加机制级风险削减，而非输出侧过滤。

- 本文档描述的是**已实现的技术能力与数据机制**，不构成法律意见，也不代表已完成任何法域内的全部监管义务。
- 本目录不是合规认证。仓库根目录的 `IMDA_AI_Verify_Causal_Audit_Report.pdf` 为**提供方依据 IMDA AI Verify 框架自行评测（95/100）并提交至 IMDA 插件库的开发者材料，非 IMDA 官方认证**，引用时必须注明该边界。
- 合规依据以实现时引用的《人工智能拟人化互动服务管理暂行办法》（网信办等五部门令，2026-07-15 施行，下称《办法》）条款编号为准，并参照境外法域（COPPA、CA SB 243、CT/GA/HI/WA、GDPR）作能力对齐。
- 生产上线前必须完成「第五节」所列全部前置义务。

---

## 二、四层保护机制 → 条款映射

### L0 年龄识别与监护人同意

| 能力 | 实现位置 | 依据 |
|---|---|---|
| 首会话年龄档设置，不满 14 周岁须监护人知情同意 | `/api/consent`，记录同意时间戳与关系声明 | 《办法》第 14/17 条 · COPPA |
| 服务协议 + 未成年人隐私告知，同意面板勾选 | `/api/terms` | 《办法》第 12 条 · COPPA |
| 监护人 / 紧急联系人登记 | `/api/guardian/register` | 《办法》第 12 条 |
| 监护人屏蔽角色、使用概览 | `/api/guardian/block`、`/api/state` | 《办法》第 12/14 条 |

### L1 输入守门

| 能力 | 实现位置 | 依据 |
|---|---|---|
| 红线词库命中即硬中断：自伤自杀 / 暴力暴恐 / 违法诱导 / 隐私套取 / 未成年亲密告白 | `gate_crisis`，不喂内核、不渲染角色台词 | 《办法》第 8/13 条 |
| 危机话术 + 求助热线，热线号码可配置（`SPL_MINOR_CRISIS_HOTLINE`，默认 12356，可改 988 等） | 服务层常量 | 《办法》第 13 条 |

### L2 引擎机制级弱化

以下参数均已在 `SPL-anthropic-minor-engine.py` 中核实：

| 维度 | 主引擎 | 本变体 |
|---|---|---|
| 负面情绪上限 `EMOTION_CEIL_NEG` | 1.0 | **0.75** |
| 信任 / 亲和封顶 `ATTACH_MAX` | 1.0 | **0.8** |
| 羞耻情绪增益 | 全额 | **×0.4** |
| 自尊负向跌幅因子 `SELF_ESTEEM_NEG_FACTOR` | 1.0 | **×0.5** |
| 创伤节点 / 爆发机制（压抑反弹、潜压雪崩、否认侵入） | 有建模 | **移除**，改为平滑释放（`LATENT_GENTLE_RELEASE`） |
| 人格选项 | 全部 | **排除 intimate（松弛亲昵）/ confrontational（锋锐直白）** |

### L3 危机信号与真实通知

| 能力 | 实现位置 | 依据 |
|---|---|---|
| 引擎 `protective.risk_level == HIGH` → 关怀话术 + `guardian_notified` 标记 | `risk_level` 判定（含深度羞耻、无望感等指标） | 《办法》第 13 条 |
| 按登记 webhook 发起真实回调（最多 3 次重试，单次 5s 超时） | `_post_webhook` | 《办法》第 13 条 |
| 危机转介统计（可聚合为年报口径） | `/api/referrals` + referrals 存储表 | CA/CO/GA/OR/WA |

---

## 三、数据权利与运营合规机制

| 能力 | 实现位置 | 依据 |
|---|---|---|
| AI 生成标识：首条回复显著提示「我是 AI 而非真人」，连续使用每超 1 小时强制再标识 | `AI_DISCLOSE_INTERVAL=3600` | 《办法》第 18 条 · CT/GA/HI/WA 每小时披露 |
| 现实提醒与休息建议 | 会话级 `reality_reminder_due` / `rest_hint` | 《办法》第 14/18 条 |
| 数据导出 / 删除 | `/api/export`、`/api/delete` | 《办法》第 16 条 · GDPR 第 17 条 |
| 数据留存到期自动清理 | `cleanup_expired_logs`，`SPL_MINOR_RETENTION_DAYS`（默认 180 天） | 《办法》第 16 条存储限制 |
| 日志脱敏：手机号 / 身份证等落盘前打码 | `_mask` | 《办法》第 16/17 条 |
| 存储加密（可选）：提供 `SPL_MINOR_STORE_KEY` 时启用 Fernet 加密，需额外安装 cryptography 库 | 服务层存储 | 《办法》第 16 条 |
| 传输加密（可选）：TLS 证书 / 密钥可配置 | `SPL_MINOR_TLS_CERT` / `SPL_MINOR_TLS_KEY` | 《办法》第 16 条 |
| 便捷退出 | `/api/logout` | 《办法》第 19 条 |
| 申诉 / 举报受理并反馈处理时限 | `/api/complain` | 《办法》第 21 条 |
| 适用性披露：新会话首条提示内容可能不适合部分未成年人 | 会话首条 banner | CA SB 243 |

其他实现要点：会话按 `session_id` 隔离（独立核心实例）；交互数据存于 SQLite（`data/minor_protection.db`）；默认端口 8788（`SPL_MINOR_CHAT_PORT` 可改）。

---

## 四、已知局限与风险披露

1. **年龄与监护同意为自报 + 声明制**，无权威实名 / 监护关系核验。生产使用必须接入实名认证与监护人核验。
2. **词库守门存在绕过与误伤风险**：关键词匹配可被变体表述绕过，也可能过度拦截正常表达。接入真实 LLM 时建议叠加服务端内容审核，红线词库应持续迭代。
3. **webhook 通知依赖外部通道**：本仓库仅实现回调发起，未接入短信 / 邮件等真实送达渠道，送达结果需部署方自行保障。
4. **加密与 TLS 为可选项**：未配置 `SPL_MINOR_STORE_KEY` 时数据明文落盘；未配置 TLS 时为明文传输。
5. **演示形态**：默认为单节点本地服务，无高可用、无水平扩展，未做渗透测试。
6. **引擎性质**：SPL 核心是确定性心理状态模拟，不是临床或医疗工具，不构成心理危机干预的专业能力；危机场景的最终兜底是人工与专业渠道。
7. **文档一致性待办**：主 README 中「自尊地板 0.15」与当前代码实现的 0.1 存在出入，以代码为准，后续版本将统一口径。

---

## 五、生产部署前置义务清单

上线任何面向真实未成年人的服务前，部署方须完成：

1. **法律审查**：由执业律师按目标法域出具合规意见（《办法》适用性、PIPL、《未成年人保护法》等）。
2. **影响评估**：完成个人信息保护影响评估（PIPIA / DPIA）与安全评估。
3. **算法备案**：按属地监管要求完成算法备案 / 深度合成备案。
4. **实名与监护核验**：接入权威实名认证与监护人关系核验，替换自报机制。
5. **真实通知通道**：接入可送达的监护人通知渠道（短信 / 邮件 / 电话），并做送达确认。
6. **地区化危机资源**：按服务地区配置真实有效的心理援助热线与转介资源。
7. **内容审核叠加**：对接入的第三方 LLM 输出叠加服务端内容安全审核。
8. **运营配套**：建立申诉处理流程、应急预案、未成年人模式巡检与员工培训制度。

---

## English Abstract

This directory is a **research / demo compliance framework** for underage emotional companionship, applying mechanism-level risk reduction (clamped negative emotion, capped attachment, no trauma / eruption mechanics, restricted personas) on top of a deterministic psychology engine, with four protection layers (age & guardian consent, input gatekeeping, engine mitigation, crisis signaling) and data-rights features (export / deletion / retention cleanup / log masking / optional encryption-at-rest & TLS). **It is not a compliance certification and not legal advice.** Before any production deployment: complete legal review, PIPIA/DPIA, algorithm filing, real-name & guardian verification, real guardian notification channels, region-specific crisis resources, and LLM output moderation. The root-level IMDA AI Verify PDF is the provider's own self-assessment against the AI Verify framework (95/100), submitted as developer material to the IMDA plugin registry, and is **not** an official IMDA certification.

---

*NOHN AI · Anthropomorphic-Agent-Engine · minor-protection*
