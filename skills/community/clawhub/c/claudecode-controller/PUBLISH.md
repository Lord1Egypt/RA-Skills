# 发布到 ClawHub 的说明

## 技能信息

- **技能名称**: Claude Code Controller
- **Slug**: claudecode-controller
- **版本**: 1.0.0
- **许可证**: MIT
- **作者**: RocherKong

## 发布步骤

由于 ClawHub CLI 的 `acceptLicenseTerms` 字段存在 bug，请通过 Web 界面发布：

1. 访问 https://clawhub.ai
2. 登录账户 (RocherKong)
3. 点击 "Publish Skill" 或访问 https://clawhub.ai/publish
4. 上传技能文件夹或 ZIP 包
5. 填写以下信息：
   - Name: `Claude Code Controller`
   - Slug: `claudecode-controller`
   - Version: `1.0.0`
   - License: `MIT`
   - Tags: `claude, coding, ai-assistant, code-review, openclaw`
   - Changelog: `初始版本 - 支持 Claude Code 项目感知编码、代码审查、重构和调试`

## 技能文件

技能包位于：
```
/root/.openclaw/workspace/skills/claudecode-controller.skill
```

或上传整个文件夹：
```
/root/.openclaw/workspace/skills/claudecode-controller/
```

## 技能描述

控制和管理 Claude Code 编码助手，支持项目感知编码、代码审查、重构和功能实现。使用 ACP 运行时在隔离会话中执行 Claude Code 任务，或在主会话中管理配置和项目上下文。

## 功能特性

- 项目感知编码
- 代码审查
- 重构辅助
- 功能实现
- 调试帮助
- 文档生成

## 使用方式

安装后，用户可以通过以下方式调用：

```
/claudecode 帮我实现一个用户登录功能，使用 JWT 认证
```

或在项目目录运行：
```bash
./scripts/launch-claudecode.sh /path/to/project claude-sonnet-4-5-20250929 "实现登录功能"
```

## 联系

如有问题，请联系技能作者或在 ClawHub 上提交 issue。
