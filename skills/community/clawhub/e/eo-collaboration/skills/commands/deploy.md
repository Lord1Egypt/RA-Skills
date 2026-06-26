---
name: deploy
description: 部署指令，调度 DevOps 专家执行应用部署和 CI/CD 配置
whenToUse: 当需要进行应用部署、配置 CI/CD、设置监控时使用
allowedTools: ["Read", "Write", "Bash"]
context: inline
expert: devops
aliases: ["/deploy", "/部署", "/release"]
version: 1.0.1
---

# /deploy - 部署指令

> **v1.0.1 新增**: frontmatter 标准化，expert 映射到 DevOps 角色

## 功能
调度 DevOps 专家，执行应用部署。

## 参数
```
/deploy <环境> [options]

参数:
  <环境>      必填，部署环境
               值: dev | staging | production
  --rollback  可选，是否启用自动回滚
               值: true | false
               默认: false
  --notify    可选，部署后通知
               值: true | false
               默认: false
  --strategy <策略> 可选，部署策略
                     值: blue-green | canary | rolling
                     默认: rolling
```

## 执行流程

1. **环境确认** → 确认目标环境和配置
2. **健康检查** → 部署前检查
3. **执行部署** → 根据策略执行
4. **验证部署** → 冒烟测试
5. **监控** → 错误率/性能监控

## 输出格式

```markdown
# 🚀 部署报告 - [环境]

## 📋 部署信息
- **环境**: production
- **版本**: v2.6.0
- **策略**: rolling
- **时间**: 2026-04-01 12:00:00

## 📦 部署内容
| 服务 | 旧版本 | 新版本 | 状态 |
|------|--------|--------|------|
| frontend | v2.5.0 | v2.6.0 | ✅ |
| backend | v2.5.2 | v2.6.0 | ✅ |

## 🔄 部署过程

### Step 1: 健康检查
```
✅ 数据库连接正常
✅ Redis 连接正常
```

### Step 2: 滚动更新
```
[1/3] frontend - 启动新实例... ✅
[2/3] backend  - 启动新实例... ✅
```

### Step 3: 冒烟测试
```
GET /healthz - 200 OK (12ms) ✅
```

## 📊 部署结果
| 指标 | 值 |
|------|------|
| 持续时间 | 2m 34s |
| 成功率 | 100% |
| 回滚次数 | 0 |

## ✅ 状态: 部署成功
```

## 对应专家
- DevOps Engineer
- SRE Specialist
- Platform Engineer
