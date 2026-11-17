# Changelog

## [1.0.0] - 2026-07-08

### Added
- 首发版本：6 大类 59 种银行公文模板（提示词从线上已验证源码提取，100% 复用，IP 即护城河）
- 写作脚本 `scripts/bankai_write.mjs`：CLI + 对话双形态，直连 DeepSeek 官方 OpenAI 兼容接口
- 反编造护栏：用户未提供的数据一律 `XX` 占位并附"需人工核实"清单，禁止凭空生成精确数字（银行场景致命雷区）
- 严格类型匹配：精确 id / 名称匹配，选错文档即报错并给候选，绝不静默猜错
- 超时与限流重试：AbortController 120s 超时 + 429/5xx 退避重试 3 次，避免永久挂起
- 私有化预留：`BASE_URL` 指向自建 OpenAI 兼容端点，数据不出行
- 调用层测试 `scripts/test_bankai.mjs`（`node --test`，5/5 通过）
- 提示词提取脚本 `scripts/extract_scenarios.mjs`（从源码重新生成 references/scenarios.mjs）
