# Changelog

## [1.2.0] - 2026-08-08
### Fixed
- **修复失败退点后的计费漏损**：平台按 `X-OC-Request-Id` 永久去重，退点却不释放该键，导致「上游失败退点 → 重试」拿到结果不扣点；详情的幂等键不含时间戳，某个商标失败一次后对该组织永久免费。现在退点会释放幂等键，重试重新正常扣点（平台侧 `refundPoints({ releaseRequestId: true })`）
- **错误响应字段不再被吞**：402 的 `rechargeUrl`、失败退点的 `refundedPoints`、429 的 `retryAfterSeconds` 与 `httpStatus` 现在原样透传到 CLI 输出，agent 可直接引导用户充值
- **`export-status` 移除无效轮询代码**：循环体无条件返回、`attempts` 从不自增，超时常量与文案全部不可达；改为单次查询 + `pending`/`hint` 字段，由调用方稍后重跑
- **超时不再覆盖不到响应体**：此前 `clearTimeout` 在读 body 之前触发，响应体挂起会永久卡死
- **参数解析不再把选项当取值**：`--query --page 1` 曾真的查询字符串 `"--page"` 并扣 1 点；现在报参数错误，并新增 `--key=value` 写法
- **`--lang en` 下的未知错误返回英文**，未知异常保留原始原因，`CHINA_TM_DEBUG=true` 附带 stack
- **导出 tmid 自动去重**（CLI 与平台两侧）：导出按条数阶梯计价，重复 tmid 会把用户推进更贵的档
- 未知命令不再先报「缺少环境变量」；新增 `--help` / `-h` 别名
- 体验点口径修正为 **100 点 / 90 天**（与平台 `DEFAULT_TRIAL_POINTS` 对齐，此前文档写的 10 点 / 30 天为陈述错误）

### Changed
- `--page` 大于 1 在 CLI 本地直接拒绝，不再消耗一次往返；`--pageSize` 不再参与请求（平台固定 50），传入时仅在 stderr 提示
- 重试码表与平台对齐：`SERVER_ERROR` / `UPSTREAM_TIMEOUT` / `NETWORK_ERROR` 自动重试；`UPSTREAM_ERROR`（平台已退点）与 `RATE_LIMITED` 不再空转重试
- `ALLOW_HTTP=true` 时在 stderr 警告 token 将明文传输

### Added
- CLI 测试套件 `scripts/cli.test.mjs`（`npm test`，node:test，零第三方依赖，21 个用例）
- **开源**：源代码以 Apache-2.0 发布（`LICENSE` + `NOTICE`）。商标不随许可证转移（Apache-2.0 §6），调用平台 API 及其返回数据仍受 `API_TERMS_OF_USE.md` 约束
- `SECURITY.md` 补漏洞报告入口（私下邮件、3 个工作日回复、30 天修复窗口）
- README 补前置条件（需 tm.zhengquai.com 账号与 API Key）与许可证边界说明

## [1.1.0] - 2026-07-14
### Changed
- 统一计费口径：详情每条 2 点（同一商标已购详情后再次查看不重复扣点）；新注册组织赠送 10 点体验点（30 天有效）；点价 ¥1 = 5 点；导出最高档改为 101 条及以上 = 10 点
- 平台入口统一为 https://tm.zhengquai.com（注册 /register、API Key 生成 /settings、充值 /billing），移除旧双域名表述
- 翻页暂不支持：每次查询固定返回第一页前 50 条，page 大于 1 返回 PAGINATION_NOT_SUPPORTED 且不扣点
### Added
- 幂等请求头 X-OC-Request-Id（8-64 位，[A-Za-z0-9_-]），网络重试不重复扣点（CLI 自动处理）
- 失败自动退点说明：查询失败返回 500 SERVER_ERROR 含 refundedPoints；详情上游失败返回 502 UPSTREAM_ERROR；导出任务创建失败自动退点
- 点数不足返回 HTTP 402，body 含 rechargeUrl（https://tm.zhengquai.com/billing）

## [1.0.0] - 2026-03-28
### Added
- Initial release
- Trademark search, detail, export capabilities
- OpenAI agents.yaml integration
- CLI tool for debugging and testing
- Bilingual documentation (Chinese + English)
- GDPR, CCPA, OFAC compliance documentation
- Data residency disclosure
- Legal disclaimer
