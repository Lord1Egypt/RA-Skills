# 昌叔专属软件开发助手 - 快速开始指南

## 欢迎使用昌叔助手！

这是为你量身定制的专属软件开发助手，专注于系统管理、编程开发、数据库操作和AI应用。

## 快速安装

### 1. 确保环境准备就绪

```bash
# 检查Python版本（需要3.8+）
python --version

# 检查Node.js版本（可选，需要16+）
node --version
```

### 2. 安装依赖

```bash
# 进入skill目录
cd ~/.hermes/skills/devops/changshu-dev-assistant

# 安装Python依赖
pip install pyyaml

# （可选）安装其他依赖
pip install requests psutil
```

### 3. 配置助手

```bash
# 复制配置文件模板
cp templates/config.example.yaml config.yaml

# 编辑配置文件（根据你的需求调整）
vim config.yaml
```

### 4. 初始化助手

```bash
# 运行初始化
python scripts/changshu-assistant.py init
```

## 基本使用

### 启动助手

```bash
# 查看帮助
python scripts/changshu-assistant.py help

# 查看状态
python scripts/changshu-assistant.py status

# 直接提问
python scripts/changshu-assistant.py ask "如何优化达梦数据库查询？"
```

### 代码审查

```bash
# 审查Python代码
python scripts/changshu-assistant.py review --file app.py

# 审查SQL文件
python scripts/changshu-assistant.py review --file query.sql
```

### 系统诊断

```bash
# 运行系统诊断
python scripts/changshu-assistant.py diagnose
```

## 常用场景

### 场景1: 日常开发工作

```bash
# 早上开始工作
python scripts/changshu-assistant.py status

# 代码审查
python scripts/changshu-assistant.py review --file src/main.py

# 性能优化
python scripts/changshu-assistant.py optimize --file slow_query.sql
```

### 场景2: 数据库工作

```bash
# SQL优化
python scripts/changshu-assistant.py sql-optimize --file query.sql

# 存储过程开发
python scripts/changshu-assistant.py procedure --name user_sync

# 数据库诊断
python scripts/changshu-assistant.py db-diagnose
```

### 场景3: 系统运维

```bash
# 系统监控
python scripts/changshu-assistant.py monitor

# 日志分析
python scripts/changshu-assistant.py logs --file /var/log/app/error.log

# 自动化脚本
python scripts/changshu-assistant.py script --task "daily_backup"
```

### 场景4: AI开发

```bash
# Prompt优化
python scripts/changshu-assistant.py prompt --file system_prompt.txt

# 模型集成
python scripts/changshu-assistant.py model-integrate --provider openai

# 性能评估
python scripts/changshu_assistant_main.py chat  # 模型通过环境变量配置
```

## 配置说明

### 主要配置项

```yaml
# 助手基本信息
assistant:
  name: "昌叔助手"           # 助手名称
  personality: "专业、高效、贴心"  # 性格特点
  language: "zh-CN"         # 语言设置

# 功能模块开关
features:
  system: true              # 系统管理
  code: true               # 代码开发
  database: true           # 数据库专精
  ai: true                 # AI开发
  knowledge: true          # 知识管理

# 集成服务配置
integrations:
  claude_code:
    enabled: true
    path: "/usr/local/bin/claude"

# 用户偏好设置
preferences:
  output_format: "structured"  # 输出格式
  code_style: "pep8"          # 代码风格
  db_type: "dameng"           # 数据库类型
  ai_provider: "local"        # AI提供商
```

## 高级功能

### 知识库集成

助手支持本地知识库管理，可以：

```bash
# 生成文档
python scripts/changshu-assistant.py docs --topic "系统架构"
```

### Claude Code集成

与Claude Code协同工作：

```bash
# 发送任务给Claude Code
python scripts/changshu-assistant.py claude --task "code_review"

# 接收Claude Code结果
python scripts/changshu-assistant.py claude --result
```

## 常见问题

### Q: 如何离线使用？
A: 助手支持完全离线模式，只需确保本地模型和数据已下载。

### Q: 如何与现有工具集成？
A: 助手支持与Git、Docker、Kubernetes等工具的深度集成。

### Q: 数据安全如何保障？
A: 所有数据本地存储，支持加密，不会上传到云端。

### Q: 如何扩展功能？
A: 模块化设计，可以轻松添加新的功能模块。

## 技巧和建议

### 1. 提高效率

- 使用快捷键和别名
- 配置自动化脚本
- 利用知识库快速查找

### 2. 最佳实践

- 定期更新知识库
- 保持配置文件同步
- 记录常用命令

### 3. 故障排除

- 查看日志文件
- 检查配置文件
- 运行诊断命令

## 获取帮助

```bash
# 查看完整帮助
python scripts/changshu-assistant.py help

# 查看特定命令帮助
python scripts/changshu-assistant.py <command> --help
```

## 下一步

1. ✅ 完成安装和配置
2. ✅ 运行初始化
3. 📚 阅读完整文档
4. 🚀 开始使用助手

---

**昌叔，准备开始高效工作吧！** 🎯

如有问题，随时询问助手或查看完整文档。
