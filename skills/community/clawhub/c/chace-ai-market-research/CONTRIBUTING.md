# Contributing to AI Market Research Skill

感谢你关注本项目的贡献！🎉

## 行为准则

- 尊重所有贡献者
- 接受建设性反馈
- 专注于开源社区的最佳利益

## 如何贡献

### 报告 Bug

请在 [GitHub Issues](https://github.com/yourusername/ai-market-research-skill/issues) 提交：

- Bug 重现步骤
- 预期 vs 实际行为
- 环境信息（OpenClaw 版本、OS、Python 版本）
- 日志文件片段

### 提出新功能

1. 先搜索是否已有相关 Issue
2. 开新 Issue 描述：
   - 使用场景
   - 预期行为
   - 替代方案分析
3. 等待社区反馈后再开始编码

### 提交 PR

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 PR，描述：
   - 修改内容
   - 测试方法
   - 相关 Issue 链接

## 开发指南

### 代码风格

- Python: 遵循 PEP 8，使用 black 格式化
- Shell/Node: 2 空格缩进，单引号优先

### 测试

运行本地测试确保通过：
```bash
cd ~/.openclaw/workspace/.agents/skills/ai-market-research
bin/run --topic "test" --depth quick --compare_previous false
```

确认：
- 报告成功生成
- 无异常错误
- 输出格式正确

### 提交信息格式

```
feat: 添加自动来源发现功能
fix: 修复历史对比数据类型错误
docs: 更新 README 安装步骤
chore: 更新 .gitignore
```

## Release 流程

维护者发布新版本：

1. 更新版本号（SKILL.md + CHANGELOG.md）
2. 打 tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
3. 推送 tag: `git push origin v0.2.0`
4. GitHub Actions 自动构建发布
5. 在 ClawHub 提交更新申请（如适用）

## 依赖说明

本技能依赖以下外部服务，贡献时请确保：

- 不硬编码敏感配置（API keys、JWT）
- 提供环境变量文档（而非硬编码）
- 模拟数据层便于离线测试

## 许可证

贡献代码即同意 MIT 许可证条款（见 LICENSE 文件）。
