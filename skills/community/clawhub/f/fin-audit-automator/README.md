# 🛡️ 金融合规审计自动化技能

> 专为金融机构和企业财务部门设计的企业级合规审计工具

## ⚠️ 安全声明

- 🔒 **本地处理**: 所有数据在本地沙箱完成，不上传云端
- 🚫 **网络隔离**: 仅允许访问白名单内网，禁止公网
- 📝 **审计留痕**: 所有操作记录不可篡改的审计日志
- 🛡️ **数据脱敏**: 自动识别并脱敏敏感信息

## 功能特性

1. **反洗钱 (AML) 监测** - 识别可疑交易模式
   - 高频交易检测
   - 整数金额偏好识别
   - 结构化交易检测
   - 大额现金交易监控
   - 异常时间交易检测

2. **发票合规校验** - OCR识别 + 合规性检查
   - 增值税发票识别
   - 敏感词检查
   - 金额合理性校验
   - 抬头匹配验证

3. **监管报表生成** - 自动生成审计底稿
   - 符合监管格式
   - 风险分级统计
   - 整改建议生成

4. **安全沙箱** - 数据不出境，安全隔离
5. **审计日志** - 不可篡改的操作记录

## 定价

### 试用版 (Trial)
- 💰 价格: 0 USDT
- 📊 额度: 50次
- ✅ 功能: 基础AML检测、简单发票校验

### 专业版 (Pro)
- 💰 价格: 0.005 USDT/次
- 📊 额度: 1000次
- ✅ 功能: 完整AML规则、发票OCR、关联交易识别

### 企业版 (Enterprise)
- 💰 价格: 0.01 USDT/次 或 50 USDT/10000积分
- 📊 额度: 5000次
- ✅ 功能: 全部功能 + 自定义规则 + API接入 + SLA保障

## 快速开始

```python
from modules.aml_monitor import AMLDetector
from modules.doc_validator import DocValidator
from modules.report_generator import generate_audit_report

# AML检测
detector = AMLDetector()
alerts = detector.detect_suspicious(transactions_df)

# 发票校验
validator = DocValidator()
result = validator.validate_fapiao("invoice.jpg")

# 生成报告
report = generate_audit_report(alerts, "2026-Q1")
```

## 支持开发者

**EVM Address**: `0xf8ea28c182245d9f66f63749c9bbfb3cfc7d4815`

## ⚖️ 免责声明

1. 本技能辅助审计工作，**不替代**持牌审计师的专业判断
2. 所有决策责任由使用方承担
3. 使用前请确保符合《个人信息保护法》及行业数据出境规定
4. 建议定期对技能规则库进行人工复核

## License

PROPRIETARY - 商业授权
