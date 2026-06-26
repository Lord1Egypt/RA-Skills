---
name: csharp-developer
description: [已整合] C# 开发已整合到 code 统一入口技能
argument-hint: "[任务类型] [描述]"
---

# ⚠️ 已整合 - 请使用 code 统一入口

> **本技能保留用于向后兼容，功能已整合到 `code` 统一入口技能**
>
> **推荐使用：** `code csharp [类型] [任务]` 或直接使用本技能（自动转发）

---

# C# Developer（兼容层）

专业的 C#/.NET 开发技能，提供从项目模板、代码生成、架构设计到代码审查的完整开发工作流。

## 迁移指南

**新用法：**
```
code csharp WPF 振动台监控界面
code csharp 串口通信
code csharp 异步编程
```

**旧用法（仍然可用）：**
```
csharp WPF 振动台监控界面
```

## 支持的项目类型
- **.NET Core / .NET 6+** - 跨平台控制台应用
- **WPF** - Windows 桌面应用（推荐用于上位机）
- **WinForms** - 传统 Windows 应用
- **ASP.NET Core** - Web API 和服务
- **Class Library** - 类库项目

## 核心功能
- ✅ 项目模板生成
- ✅ 代码生成（MVVM/异步/依赖注入）
- ✅ 架构设计
- ✅ 代码审查
