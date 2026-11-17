# 业务规则 - cookie-manager

> 来源: SKILL.md v3.0 风控规则表 + 工作流步骤

## 规则列表

- 多账号操作间隔: 多账号Cookie保活/切换操作间隔必须≥17分钟,防止触发平台风控 (来源: 01电商运营手册§十10.1风控安全线)
- Cookie年龄WARNING阈值: Cookie有效但age≥5天时发出WARNING告警,建议续期 (来源: P1-14保活频率优化)
- Cookie年龄CRITICAL阈值: Cookie有效但age≥25天时发出CRITICAL告警,需立即续期 (来源: 业务连续性保障)
- 保活频率: 每2天执行一次定时保活检查所有闲鱼Cookie (来源: P1-14优化,原3天)
- 健康度保活阈值: 健康度评分<60时触发HTTP保活访问 (来源: v4.0设计文档§3.7.6)
- 健康度评分公式: 年龄>7天扣(age-7)*5(最多扣30分) + HTTP失效扣50分,满分100 (来源: SKILL.md步骤6)
- 连续失败告警阈值: 3次连续失败写入tenant_notification告警 (来源: SKILL.md步骤6)
- 批量失效触发条件: ≥2个Cookie同时失效时启动降级运营模式 (来源: SKILL.md步骤2)
- 降级运营模式: 暂停Cron发布+自动发货,保留客服回复(仅回复不发货,使用降级模板) (来源: 01手册§十风控安全线)
- 恢复后首次操作延迟: Cookie恢复后首次操作延迟≥5分钟,确保Cookie稳定 (来源: SKILL.md步骤5)
- 4端Cookie同步: 以fishclaw-mcp JSON为权威源,通过unb字段比对.env/global_config.yml/auto-reply API一致性 (来源: SKILL.md步骤4)
- 多租户Cookie恢复SOP: 三级降级策略(备份恢复→备用Cookie切换→紧急告警) (来源: 05文档§四DEF-66)
- 存储路径统一: data/content/cookies/{tenant_id}/{platform}_{account}.json (来源: SKILL.md存储路径统一)
- 同步重试: 4端同步失败时逐端重试3次 (来源: SKILL.md异常处理)
- Cookie切换风控: Cookie切换触发风控时立即停止切换,等待≥17分钟后重试 (来源: 01手册§十10.1)
