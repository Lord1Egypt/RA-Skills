# Changelog

All notable changes to this project will be documented in this file.

## [2.1.1] - 2026-03-17

### Added
- **166 条规则** - 新增 4 条测试通过的规则
- **加密货币扩展**: 莱特币地址 (ltc_address)、瑞波币地址 (xrp_address)
- **新凭证**: Telegram Bot Token、Discord Token

### Fixed
- 配置文件更新，确保新规则生效

### Performance
- 正则表达式预编译，性能提升 5-10%
- 短文本优化，跳过 <3 字符文本

### Testing
- 增加 20 个场景测试，通过率 100%
- 性能测试: 100字符 0.5ms, 1000字符 2.2ms

---

## [2.1.0] - 2026-03-17

### Added
- **162 条规则** - 新增 16 条
- **加密货币**: 6 条 (BTC/ETH/USDT/私钥/助记词)
- **中国政务**: 6 条 (社会信用代码/组织机构代码/税务登记号/军官证)
- **国际证件**: 4 条 (美国护照/ITIN/香港/台湾身份证)
- **生物识别**: 2 条 (指纹/虹膜/人脸数据)
- **规则探索文档**: docs/RULE_EXPLORATION.md

### Categories Added
- crypto: 6 条
- government: 6 条
- intl_id: 4 条
- biometric: 2 条

---

## [2.0.0] - 2026-03-17

### Added
- **146 条规则** - 大幅扩展规则库
- **20+ 行业覆盖** - 金融、医疗、汽车、销售、人力资源、物流等
- **个人模式 (personal)** - 轻量化配置，自动脱敏
- **规则分类统计** - 支持 `agent-dlp rules` 命令

### Categories Added
- 凭证密钥: 45 条 (OpenAI/GitHub/AWS/阿里云/微信等)
- 金融: 19 条 (银行卡/股票/加密货币/工资)
- 人力资源: 11 条 (工号/社保/公积金)
- 物流: 11 条 (快递单/运单/地址)
- 医疗: 10 条 (病历/医保/诊断)
- 汽车: 6 条 (车架号/行驶证)
- 销售: 6 条 (客户信息/订单)
- 医药: 5 条 (处方/药品)
- 法规: 4 条 (合同/专利)
- 其他: 29 条

### Changed
- 性能优化 - 正则预编译
- CLI 增强 - 新增 rules 命令
- 配置简化 - 支持 personal 模式

### Fixed
- 修复部分规则匹配问题

---

## [1.0.0] - 2026-03-14

### Added
- 初始版本
- 25 条基础规则
- 入口防护 (Input Guard)
- 记忆保护 (Memory Guard)
- 工具管控 (Tool Guard)
- 出口过滤 (Output Filter)
- 审计日志 (Audit Logger)

### Features
- Prompt Injection 检测
- 敏感信息检测 (身份证、手机、邮箱)
- API Key 检测 (AWS/GitHub/Slack)
- 危险工具审批

---

## [0.0.1] - 2026-03-10

### Added
- 项目初始化
- 基础 DLP 框架
