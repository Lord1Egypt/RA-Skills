# AI Agent Capability Analyzer

基于对ClawHub.ai生态系统的深度调研，专门设计的AI技能智能分析和推荐工具。

## 功能特点

- **智能需求分析**: 理解用户的具体使用场景
- **精准技能推荐**: 从1,588个AI/ML技能中推荐最佳选项  
- **安全评估**: 基于100/3规则进行安全性评级
- **技能对比**: 多维度比较不同技能的优劣势
- **安装指导**: 提供一键安装命令和使用建议

## 安装方法

```bash
# 克隆到ClawHub技能目录
# 技能已自动安装到: ~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/ai-capability-analyzer/

# 设置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件填入你的API密钥
```

## 使用示例

### 基本查询
```bash
# 分析需求并推荐技能
node analyze.cjs --query "我需要处理YouTube视频下载"

# 比较多个技能
node analyze.cjs --compare "capability-evolver,self-improving-agent"

# 安全性检查
node analyze.cjs --security-check "youtube-downloader-skill"
```

### 在OpenClaw中使用
直接告诉你的AI代理：
- "分析一下哪个AI技能最适合我的文档摘要需求"
- "比较Capability Evolver和Self-Improving Agent的区别"  
- "推荐一些安全的AI开发工具"

## 技术架构

- **语言**: Node.js (CommonJS)
- **数据源**: 内置基于调研的技能数据库
- **扩展性**: 支持通过API集成实时ClawHub数据
- **安全性**: 本地处理优先，支持沙箱运行

## 安全特性

✅ **100/3规则验证**: 自动检查技能是否满足安全标准  
✅ **权限最小化**: 只请求必要的系统权限  
✅ **隐私保护**: 用户数据本地处理，不上传敏感信息  
✅ **透明度**: 所有推荐都有明确的数据来源和评分依据

## 开发背景

这个技能是基于对ClawHub.ai生态系统的全面调研而创建的，填补了当前平台缺少智能技能推荐工具的空白。调研发现：

- AI/ML类别占总技能的48.3%（1,588个技能）
- 用户在选择技能时面临信息过载问题
- 安全性是用户最关心的问题之一
- 缺少专业的技能比较和分析工具

## 贡献和改进

欢迎提交PR来：
- 添加更多技能到数据库
- 改进推荐算法
- 增强安全评估功能
- 添加多语言支持

## 许可证

MIT License - 免费使用、修改和分发