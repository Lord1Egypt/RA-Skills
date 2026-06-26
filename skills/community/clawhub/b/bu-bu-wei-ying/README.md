# 🏰 步步为营 (Bu Bu Wei Ying)

> 复杂APP开发统一技能 - 融合敏捷开发、CI/CD、DevOps的最佳实践

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-green.svg)](https://clawhub.com/skill/bu-bu-wei-ying)

## 核心理念

| 原则 | 说明 |
|------|------|
| **每步必测** | 每次代码变更必须运行测试 |
| **每层必验** | 每个模块必须通过验证 |
| **环环相扣** | 各阶段必须有序衔接 |
| **层层守护** | 每层必须有保护机制 |

## ⚡ 核心原则：修正范围控制

**只修正指定问题和相关联代码，不改变其他代码**

- ✅ 只修改用户明确指出的问题代码
- ✅ 只修改与问题直接相关的关联代码  
- ✅ 已正确运行的功能不得被修改
- ✅ 每次修改前确认变更范围
- ✅ 修改后验证其他功能未被影响

## 功能特性

- 📋 **完整开发流程检查清单** - 6阶段标准化开发流程
- 🔧 **自动化脚本** - 一键执行验证、构建、发布、回滚
- 📊 **监控模板** - Grafana/Datadog 告警规则开箱即用
- 🌐 **多语言支持** - 中文 + 英文双语版本
- 🛡️ **风险矩阵** - Pitfall 提示避免常见错误

## 安装

### ClawHub (推荐)
```bash
clawhub install bu-bu-wei-ying
```

### 手动安装
```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/bu-bu-wei-ying.git

# 或复制 SKILL.md 到你的 skills 目录
cp SKILL.md ~/.hermes/skills/bu-bu-wei-ying/SKILL.md
```

## 使用方法

### 场景 1：开发新功能
```
用户：帮我开发一个用户注册功能
Agent：
1. 创建分支 feature/user-registration
2. 编写 API、数据库模型、单元测试
3. 运行测试确保通过
4. 构建镜像并推送到仓库
5. 执行灰度发布
```

### 场景 2：排查部署问题
```
用户：生产环境部署失败了
Agent：
1. 检查构建日志
2. 验证环境变量配置
3. 测试数据库连接
4. 检查网络/端口
5. 执行回滚（如需要）
```

## 开发流程检查清单

### 1. 需求分析阶段
- [ ] 明确功能需求和非功能需求
- [ ] 拆分任务为可执行的子任务
- [ ] 预估时间和资源
- [ ] 确定验收标准

### 2. 代码开发阶段
- [ ] 创建功能分支 `git checkout -b feature/xxx`
- [ ] 编写代码并遵循编码规范
- [ ] 编写单元测试（覆盖率 > 80%）
- [ ] 运行本地 lint/static analysis
- [ ] 进行代码审查

### 3. 构建阶段
- [ ] 本地构建成功
- [ ] 运行集成测试
- [ ] 安全扫描
- [ ] 生成构建产物

### 4. 测试阶段
- [ ] 部署到预发布环境
- [ ] 执行 E2E 测试
- [ ] 性能测试
- [ ] 回归测试

### 5. 发布阶段
- [ ] 创建 Release Tag
- [ ] 更新 CHANGELOG
- [ ] 执行灰度发布（5% → 25% → 100%）
- [ ] 监控系统指标
- [ ] 准备回滚方案

### 6. 运维监控阶段
- [ ] 确认监控告警正常
- [ ] 检查日志聚合
- [ ] 验证备份机制
- [ ] 文档更新

## 自动化脚本

```bash
# 验证修正范围（核心安全功能）
./scripts/checklist.sh verify-fix <file>

# 完整开发检查
./scripts/checklist.sh dev-check

# Docker 构建 + 安全扫描
./scripts/checklist.sh docker-build [镜像名] [标签]

# HTTP 健康检查
./scripts/checklist.sh health [主机] [端口] [端点]

# 灰度发布（默认: 5,25,100%）
./scripts/checklist.sh canary [镜像] [阶段]

# 回滚
./scripts/checklist.sh rollback [命名空间] [部署]

# 测试覆盖率检查
./scripts/checklist.sh coverage [阈值]

# 执行全部检查
./scripts/checklist.sh all
```

## 监控模板

### Grafana
导入 `templates/grafana-alerts.json`，包含：
- 应用错误率 > 5%
- P95 响应延迟 > 1s
- 服务不可用
- CPU/内存/磁盘使用率

### Datadog
导入 `templates/datadog-alerts.json`，包含：
- 错误率告警
- 延迟告警
- 健康检查失败
- 日志错误激增检测

## 项目结构

```
bu-bu-wei-ying/
├── SKILL.md              # 中文主版本
├── SKILL-en.md          # 英文版本
├── LICENSE              # MIT-0 许可证
├── README.md            # 本文件
├── scripts/
│   └── checklist.sh      # 自动化脚本
└── templates/
    ├── grafana-alerts.json    # Grafana 监控模板
    └── datadog-alerts.json    # Datadog 监控模板
```

## 许可证

本项目采用 [MIT No Attribution](LICENSE) 许可证：

- ✅ 可自由使用、修改、分发
- ✅ 包括商业用途
- ❌ 无需署名
- ❌ 不提供任何担保

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**🏰 步步为营 - 每步必测，每层必验，环环相扣，层层守护**
