#!/usr/bin/env python3
# 全局配置文件

# 基础配置
BACKUP_ROOT = "~/.openclaw/skill-backups/"
PROPOSAL_DIR = "~/.openclaw/skill-proposals/"
KEEP_VERSIONS = 20

# 流程管控配置
REQUIRE_PROPOSAL_APPROVAL = True  # 是否强制要求方案审批才能修改
ENABLE_RISK_CONFIRM = True        # 是否开启修改前风险确认
RISK_CONFIRM_THRESHOLD = "中风险"  # 风险确认阈值
AUTO_RUN_TESTS = True             # 修改完成后自动运行测试
AUTO_ROLLBACK_ON_TEST_FAILURE = True  # 测试失败自动回滚

# 路径解析
BACKUP_ROOT = os.path.expanduser(BACKUP_ROOT)
PROPOSAL_DIR = os.path.expanduser(PROPOSAL_DIR)
