# 配置说明

## 全局配置项

### 基础配置
- 备份路径：`~/.openclaw/skill-backups/`
- 每个技能默认保留版本数：20个（稳定版除外，永久保留）
- 优化方案存储路径：`~/.openclaw/skill-proposals/`

### 流程管控配置
```python
# 是否强制要求方案审批才能修改技能
REQUIRE_PROPOSAL_APPROVAL = True

# 是否开启修改前风险确认
ENABLE_RISK_CONFIRM = True

# 风险等级阈值，高于此等级需要二次确认
RISK_CONFIRM_THRESHOLD = "中风险"  # 可选: 低风险/中风险/高风险

# 是否自动运行测试用例
AUTO_RUN_TESTS = True

# 测试不通过是否自动回滚
AUTO_ROLLBACK_ON_TEST_FAILURE = True
```

## 配置修改方法
直接修改对应脚本头部的变量值即可生效，无需重启。
