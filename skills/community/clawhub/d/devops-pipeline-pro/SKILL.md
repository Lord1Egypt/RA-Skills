---
name: DevOps Pipeline Pro
slug: devops-pipeline-pro
description: DevOps全流程自动化引擎，支持GitHub Actions / GitLab CI / Jenkins / ArgoCD等主流平台，覆盖CI/CD流水线编排、IaC基础设施管理、容器化部署、监控告警、日志分析、灰度发布与回滚。
version: 1.0.0
author: ai-gaoqian
tags:
  - devops
  - ci-cd
  - github-actions
  - gitlab-ci
  - docker
  - kubernetes
  - terraform
  - monitoring
metadata:
  openclaw:
    requires:
      - github-actions
      - docker
      - kubernetes
---

# DevOps Pipeline Pro

DevOps全流程自动化引擎，提供从代码提交到生产部署的全链路自动化能力，支持主流CI/CD平台、容器编排、基础设施即代码和可观测性管理。

## 触发条件

- "创建一个Node.js项目的CI流水线"
- "部署到Kubernetes"
- "排查这次构建失败的原因"
- "配置蓝绿部署策略"
- "检查集群健康状态"
- "回滚到上一个版本"
- "生成Terraform基础设施配置"

## 核心能力

| 能力 | 说明 |
|------|------|
| CI/CD编排 | GitHub Actions / GitLab CI / Jenkins流水线自动生成与优化 |
| 容器管理 | Dockerfile生成、镜像构建推送、K8s manifest编排 |
| IaC | Terraform / Ansible / Pulumi基础设施配置生成与管理 |
| 部署策略 | 滚动更新、蓝绿部署、金丝雀发布、A/B测试 |
| 监控告警 | 基于四大黄金指标（延迟/流量/错误/饱和度）的可观测性配置 |
| 日志分析 | 聚合ELK/Loki日志，AI分析异常模式 |
| 密钥管理 | HashiCorp Vault集成，环境变量安全注入 |
| 失败诊断 | 自动解析CI失败日志，定位根因并给出修复建议 |

## 执行流程

```
分析项目栈 → 选择最佳CI/CD平台 → 生成流水线配置
    → 容器化（如需要）→ K8s部署编排
    → 监控告警配置 → 执行部署 → 健康检查
```

## 输出格式

**流水线诊断报告**：
```
🔧 CI/CD 诊断报告
━━━━━━━━━━━━━━━━━━━━━━━
流水线: [名称] | 运行: #[N] | 状态: ❌ 失败
━━━━━━━━━━━━━━━━━━━━━━━
失败阶段: [stage名]
根因: [具体错误原因]
建议: [修复步骤和命令]
相关日志: [关键错误日志片段]
```

**部署状态**：
```
🚀 部署完成
━━━━━━━━━━━━━━━━━━━━━━━
应用: [名称] | 版本: [tag]
环境: [开发/测试/生产]
策略: [滚动/蓝绿/金丝雀]
镜像: [registry/image:tag]
节点: [N] 个Pod | 已就绪: [N]/[N]
健康检查: ✅ 通过
访问地址: [URL]
```

## 注意事项

- 生产环境部署前强制预览变更并人工确认
- 密钥和凭证绝不写入流水线日志
- K8s资源限制配置默认保守，可自定义调整
- IaC变更自动生成plan/apply报告并保留审计记录
