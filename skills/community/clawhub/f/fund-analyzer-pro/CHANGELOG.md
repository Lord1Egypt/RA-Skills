# Change Log - Fund-Analyzer-Pro

所有重要变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.2.0] - 2026-04-16

### Added
- skill-evolve Round 2 测试（5 个针对性 prompt）
- 直觉问题验证（模块引导/数据降级/复杂场景）
- fund-signal-monitor 独立为子 skill（模块 8）

### Changed
- skill-evolve 测试评分：9.2/10 → 10/10
- 完全收敛
- 公众号文章补充 fund-signal-monitor 说明

### Fixed
- 无（Round 2 无问题）

---

## [1.1.1] - 2026-04-16

### Changed
- 对比报告模板优化（核心结论前置 + 详细对比可折叠）
- skill-evolve 测试评分：9.2/10

### Fixed
- 对比报告过长问题

---

## [1.1.0] - 2026-04-16

### Added
- 模块 8 独立为子 skill：`fund-signal-monitor`
- CI/CD GitHub Actions 工作流
- 基金代码格式校验（6 位数字正则）
- API 失败降级策略（且慢→天天→免费→手动）
- 数据缓存机制（TTL 可配置）
- 用户持仓加密存储（Fernet 对称加密）
- 单元测试套件（12 个测试全部通过）

### Changed
- `qieman-mcp-query.py` 添加缓存 + 降级支持
- `ttfund-query.py` 添加缓存 + 降级支持
- SKILL.md 更新数据源说明

### Fixed
- 基金代码格式未校验问题
- API 超时未处理问题
- 用户持仓明文存储安全问题

---

## [1.0.0] - 2026-04-16

### Added
- **八大核心模块**：
  - 模块 1：单一基金分析
  - 模块 2：基金对比
  - 模块 3：基金诊断
  - 模块 4：持仓诊断⭐
  - 模块 5：基金经理分析
  - 模块 6：机会分析
  - 模块 7：投资方式
  - 模块 8：报告信号
- **数据源整合**：
  - 天天基金 API（基础数据/业绩/费率）
  - 且慢 MCP（投顾策略/持仓明细/收益归因）
  - 基金 e 账户（Excel 导入）
- **参考文档**：
  - `fund-fee-analysis.md` - 费用分析框架
  - `fund-manager-evaluation.md` - 经理评估体系
- **报告模板**：
  - `fund-report-template.md` - 标准化报告结构
- **使用示例**：
  - `fund-diagnosis-case.md` - 完整诊断案例
- **工具脚本**：
  - `qieman-mcp-query.py` - 且慢 MCP 查询
  - `ttfund-query.py` - 天天基金查询

### Documentation
- SKILL.md（6044 字）
- README.md（2411 字）
- ASSESSMENT-v3.md（v3.0 评分报告，90/100 分）

---

## 版本说明

### v1.0.0（初始版本）

**核心功能**：
- 八大分析模块完整实现
- 数据源整合（天天基金 + 且慢 MCP）
- 完整文档体系

**评分**：90/100（核心技能🔴）

**适用场景**：
- 单一基金分析
- 基金对比
- 持仓诊断
- 基金经理评估

---

## 待办事项

### v1.1.0（计划中）
- [ ] 模块 8 独立为 `fund-signal-monitor`
- [ ] 添加更多单元测试（覆盖率>80%）
- [ ] 添加 CI/CD 集成
- [ ] 坑点章节补充（从实际案例中提炼）

### v1.2.0（计划中）
- [ ] 添加基金定投计算器
- [ ] 添加基金组合回测
- [ ] 添加市场估值分析

---

## 贡献者

- **燃冰** - 需求设计 + 测试
- **ant** - 开发实现

---

## 相关链接

- [GitHub 仓库](https://github.com/lj22503/one-person-ceo-skills)
- [ClawHub 页面](https://clawhub.ai/skills/fund-analyzer-pro)
- [技能文档](SKILL.md)
