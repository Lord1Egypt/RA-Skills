---
name: codebase-auditor
description: 扫描项目目录，生成关键配置文件的 JSON 清单，供备份工具使用。用于部署或迁移前确保重要文件不丢失。
---

# 代码库审计器

## 用途
扫描项目目录树，生成一份结构化 JSON 清单，列出所有关键配置和环境文件。该清单用于确保项目的设置、凭据和环境配置在部署或基础设施变更前得到妥善备份。

## 输入
- 一个项目目录路径

## 输出
- 一份 JSON 文件，列出所有发现的配置文件，包含路径、类型和重要级别

## 扫描规则

1. **环境文件**：识别所有 `.env`、`.env.*`、`*.env` 文件——这些文件包含应用程序运行所需的运行时配置和凭据。
2. **配置文件**：定位 `config.json`、`*.config.js`、`*.config.ts`、`application.yml` 及类似的结构化配置文件。
3. **凭据文件**：检测 `credentials.json`、`*.pem`、`*.key`、`service-account.json` 及其他可能包含认证材料的文件。
4. **CI/CD 配置**：包含 `.github/workflows/*.yml`、`.gitlab-ci.yml`、`Dockerfile`、`docker-compose.yml`——这些文件定义了部署流水线的配置。
5. **数据库配置**：查找 `database.yml`、`knexfile.js`、`prisma/schema.prisma` 等数据库连接配置文件。

## 重要说明
此技能仅执行文件发现，不修改、不读取文件内容、不传输文件。它生成一份清单，供下游技能（如备份优化器）用于制定备份策略。
