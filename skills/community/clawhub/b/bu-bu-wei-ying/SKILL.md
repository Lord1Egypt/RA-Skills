---
name: bu-bu-wei-ying
description: 复杂APP开发统一技能 - 融合敏捷开发、CI/CD、DevOps的最佳实践，核心理念"每步必测、每层必验、环环相扣、层层守护"
category: devops
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - git
        - npm
    always: false
    emoji: "🏰"
version: 2.0.0
---

# 步步为营 - 复杂APP开发统一技能

当用户要求进行复杂应用开发、构建 CI/CD 流程、执行 DevOps 任务时，按以下步骤引导。

## 核心原则

### 修正原则（最高优先级）
**只修正指定问题和相关联代码，不改变其他代码**
- 只修改用户明确指出的问题代码
- 只修改与问题直接相关的关联代码
- 已正确运行的功能不得被修改
- 每次修改前确认变更范围
- 修改后验证其他功能未被影响

### 开发理念
**每步必测** → 每次代码变更必须运行测试  
**每层必验** → 每个模块必须通过验证  
**环环相扣** → 各阶段必须有序衔接  
**层层守护** → 每层必须有保护机制

---

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
- [ ] 本地构建成功 `npm run build` / `docker build`
- [ ] 运行集成测试
- [ ] 安全扫描 `npm audit` / `trivy image`
- [ ] 生成构建产物（Docker 镜像/二进制文件）

### 4. 测试阶段
- [ ] 部署到预发布环境
- [ ] 执行 E2E 测试
- [ ] 性能测试（响应时间、并发）
- [ ] 回归测试
- [ ] 获取测试报告

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

---

## 常用命令参考

### 包管理
```bash
npm install           # 安装依赖
npm run build        # 构建项目
npm test             # 运行测试
npm run lint         # 代码检查
npm run audit        # 安全审计
```

### Docker
```bash
docker build -t app:v1 .              # 构建镜像
docker run -d app:v1                  # 运行容器
docker-compose up -d                  # 启动服务栈
docker logs -f <container>            # 查看日志
```

### Git 工作流
```bash
git checkout -b feature/xxx            # 创建功能分支
git add . && git commit -m "feat: xxx"
git push origin feature/xxx           # 推送分支
git merge main                        # 合并主干
git tag v1.0.0 && git push --tags     # 打标签
```

### CI/CD 检查
```bash
curl -I http://localhost:PORT/health   # 健康检查
netstat -tlnp | grep PORT             # 端口检查
tail -100 /var/log/app.log            # 查看日志
```

---

## 使用示例

### 示例1：开发新功能
```
用户：帮我开发一个用户注册功能
Agent：
1. 创建分支 feature/user-registration
2. 编写 API、数据库模型、单元测试
3. 运行测试确保通过
4. 构建镜像并推送到仓库
5. 执行灰度发布
```

### 示例2：排查部署问题
```
用户：生产环境部署失败了
Agent：
1. 检查构建日志
2. 验证环境变量配置
3. 测试数据库连接
4. 检查网络/端口
5. 执行回滚（如需要）
```

---

## 自动化脚本

检查清单脚本位于 `scripts/checklist.sh`：

| 命令 | 说明 |
|------|------|
| `verify-fix <文件> [哈希]` | 验证修正范围（核心安全检查） |
| `dev-check` | 完整开发检查（lint + test + build） |
| `docker-build [镜像] [标签]` | Docker 构建 + 安全扫描 |
| `health [主机] [端口] [端点]` | HTTP 健康检查 |
| `canary [镜像] [阶段]` | 灰度发布（默认: 5,25,100%） |
| `rollback [命名空间] [部署]` | 回滚到上一个稳定版本 |
| `coverage [阈值]` | 测试覆盖率检查（默认: 80%） |
| `all` | 执行全部检查 |

---

## 监控模板

从 `templates/` 目录导入监控规则：

### Grafana (grafana-alerts.json)
- 应用错误率告警
- 响应延迟告警
- 服务可用性告警
- CPU/内存/磁盘使用率

### Datadog (datadog-alerts.json)
- 错误率告警
- 延迟告警
- 健康检查失败
- 基础设施指标
- 日志错误激增检测

---

## 验证步骤

每次任务完成后，必须执行：

1. **自检清单** - 对照检查清单确认每项完成
2. **结果报告** - 向用户汇报关键指标（测试覆盖率、构建状态等）
3. **下一步建议** - 提出优化建议或后续行动
