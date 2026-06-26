---
name: soft-agent-module
description: |
  Agent模块（acore-agent）开发指南。涵盖Agent全生命周期管理（创建/编辑/发布/删除）、
  Dify平台集成、DeerFlow平台集成（后端预创建线程+前端跳转独立页面模式）、模板方法+工厂模式的多平台扩展架构、
  权限管理、标签管理、资源映射等完整知识。
  当用户提到Agent、agent、智能体、Dify Agent、DeerFlow Agent、Agent管理、Agent发布、dk_acore_agent、
  AgentController、AgentApplicationService、AgentDomainService、AgentPlatformGateway、
  DifyAgentPlatformGateway、DeerFlowAgentPlatformGateway、
  DeerFlowChatGateway、acore-agent 时使用。
  即使用户只是提到"Agent模块"或"acore-agent"也应主动触发。
---

# Agent模块（acore-agent）开发指南

本 skill 的目标：接到 Agent 新需求时，直接基于已有代码模式开发，无需重新读代码。

## 模块概述

Agent 模块是 AI 中台的智能体管理核心模块，随主应用聚合启动，不独立部署。

核心能力：
- Agent 全生命周期管理（创建/导入DSL/编辑/发布/取消发布/删除）
- 多平台集成（Dify 为主，DeerFlow 为新增，支持扩展 N8N/自定义平台）
- DeerFlow 平台集成（后端预创建线程+前端跳转独立页面模式）
- 模板方法 + 工厂模式的可扩展平台 Gateway 架构
- 权限管理（OWNER/COLLABORATOR/USER 三级角色）
- 标签/分类管理、资源映射
- 分页/滚动分页查询、多租户隔离
- 对外提供 client 接口（AgentQueryService）供 AIChat 等模块调用
- AI 聊天 @Agent 兼容 DeerFlow（AgentMessageStrategy 按 platformType 路由）

## 代码路径

- 后端：`acore-agent/src/main/java/com/giikin/acore/agent/`
- SQL建表：`acore-agent/sql/01_create_table_agent.sql`
- Mapper XML：`acore-agent/src/main/java/com/giikin/acore/agent/infrastructure/persistence/mapper/AgentMapper.xml`
- 文档：`acore-agent/doc/`（接口文档、工作流程、Dify API文档、实现方案）
- README：`acore-agent/README.md`
