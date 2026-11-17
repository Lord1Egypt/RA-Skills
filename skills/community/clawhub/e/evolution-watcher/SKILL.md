# evolution-watcher - 星型架构智能进化监控器

## 概述

`evolution-watcher` 是星型记忆架构的智能监控插件，负责自动发现、分析插件更新，为系统自我进化提供决策支持。它是实现“辅助自我进化系统”的第一阶段核心组件。

## 功能特性

### MVP 阶段 (v0.6.0)
- ✅ **自动监控**：定期检查 ClawHub 上已安装插件的新版本
- ✅ **版本对比**：识别当前版本与最新版本的差异
- ✅ **报告生成**：生成可读性强的升级报告（控制台 + Markdown）
- ✅ **安全设计**：仅读取信息，不执行任何自动升级操作

### 未来计划
- 🔄 变更日志解析与关键变化提取
- 🔄 影响评估（兼容性、收益、风险）
- 🔄 适配器自动调整建议
- 🔄 MSE 功能拆分试点支持

## 安装与配置

### 安装方法
```bash
# 从 ClawHub 安装（未来）
clawhub install evolution-watcher

# 或本地开发模式
cp -r evolution-watcher /root/.openclaw/workspace/skills/
```

### 配置文件
`config/monitor_sources.json`：
```json
{
  "clawhub": {
    "enabled": true,
    "check_frequency_hours": 24
  },
  "github": {
    "enabled": false,
    "repositories": [],
    "check_frequency_hours": 24
  }
}
```

## 使用方法

### 手动运行监控
```bash
cd /root/.openclaw/workspace/skills/evolution-watcher
python3 scripts/monitor.py --report
```

### 输出示例
```
🔄 evolution-watcher v0.6.0
📅 检查时间: 2026-03-17 22:00:00
📊 监控源: ClawHub (已安装 5 个插件)

📈 更新检测结果:
┌──────────────────────┬────────────┬────────────┬──────────┐
│ 插件                 │ 当前版本   │ 最新版本   │ 状态     │
├──────────────────────┼────────────┼────────────┼──────────┤
│ memory-sync-enhanced │ 2.0.0      │ 2.0.0      │ ✅ 最新   │
│ ontology            │ 1.0.4       │ 1.0.5       │ ⚠️ 可升级 │
│ self-improving      │ 1.2.16      │ 1.2.16      │ ✅ 最新   │
└──────────────────────┴────────────┴────────────┴──────────┘

📋 详细报告已保存: reports/updates_20260317_220000.md
```

### 报告文件结构
```
reports/
├── updates_20260317_220000.md     # 详细升级报告
├── updates_log.json               # 结构化监控日志
└── summary.json                   # 摘要统计
```

## 集成架构

### 在星型架构中的位置
```
⭐ 星型记忆架构
├── 核心: memory-sync-enhanced (MSE)
├── 插件: self-improving (SIPA)
├── 插件: ontology
├── 插件: memory-sync-protocol (MSP)
└── 新增: evolution-watcher (本插件)
```

### 数据流
1. **监控模块** → 调用 ClawHub CLI (`list`, `inspect`)
2. **分析模块** → 对比版本，生成差异分析
3. **报告模块** → 输出人类可读报告
4. **日志模块** → 记录监控历史（JSON 格式）

## 技术细节

### 监控逻辑
1. 读取 `clawhub list` 获取已安装插件列表
2. 对每个插件执行 `clawhub inspect <slug>` 获取最新版本
3. 对比 `current_version` (来自 list) 与 `latest_version` (来自 inspect)
4. 记录差异到结构化日志

### 安全机制
- 🔐 **零自动升级**：所有升级操作需手动执行
- 🔐 **只读操作**：仅调用信息查询命令，不修改系统
- 🔐 **完整日志**：所有监控操作都有审计日志
- 🔐 **配置可控**：监控频率、范围可配置

## 开发计划

### v0.1.0 (MVP)
- [x] 基础监控框架
- [x] ClawHub 版本检测
- [x] 报告生成

### v0.2.0
- [ ] 变更日志解析
- [ ] 初步影响评估
- [ ] GitHub 监控支持

### v0.3.0
- [ ] 适配器变更检测
- [ ] 升级建议排序
- [ ] 集成测试支持

## 注意事项

1. **网络依赖**：需要互联网连接访问 ClawHub API
2. **API 限制**：ClawHub API 可能有速率限制，请合理配置检查频率
3. **版本准确性**：依赖 ClawHub 的版本信息准确性
4. **向后兼容**：未来版本将保持配置文件兼容性

## 贡献与反馈

- **问题报告**：通过 GitHub Issues 或 ClawHub 评论
- **功能建议**：欢迎提出进化监控的新需求
- **开发贡献**：遵循标准插件开发流程

---

*进化是一个渐进的过程，而非一次革命。*