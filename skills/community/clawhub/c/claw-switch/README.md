# OpenClaw Switch v2.1

简单的 OpenClaw 模型切换工具。

## 功能

- 模型切换：通过自然语言或命令切换 AI 模型
- 任务路由：根据任务类型自动推荐合适的模型
- 状态查询：查看当前激活的模型
- 模型列表：显示所有可用模型及其特性

## 支持的模型

当前 OpenClaw 2026.3.2 版本支持以下模型：

✅ **可用:**
- Gemini 3 Flash (`google/gemini-3-flash-preview`) - 图片、多模态任务
- OpenRouter Auto (`openrouter/openrouter/auto`) - 默认兜底

⚠️ **已注册但运行时不可用:**
- 其他模型在 OpenClaw 2026.3.2 运行时报告 "Unknown model"

## 安装

### 方法 1：手动安装
```bash
# 1. 复制 skill 文件到 OpenClaw skills 目录
mkdir -p ~/.openclaw/skills/clawswitch
cp -r clawswitch-v2.1/* ~/.openclaw/skills/clawswitch/

# 2. 重启 gateway
openclaw gateway restart
```

### 方法 2：通过 ClawHub（推荐）
访问 https://clawhub.ai 上传并安装此 skill。

## 使用方法

### 在 OpenClaw TUI 中
```
use gemini          # 切换到 Gemini 3 Flash
use openrouter      # 切换到 OpenRouter
status              # 查看当前模型
help                # 显示帮助
```

### 任务路由示例
```
帮我识别这张图片      # 自动切换到 Gemini
写一段代码          # 切换到 OpenRouter
分析这个文档        # 切换到 OpenRouter
```

## 兼容性说明

- OpenClaw 版本：2026.3.2
- 测试状态：已测试 Gemini 和 OpenRouter 可用
- 其他模型因 OpenClaw 运行时兼容性问题暂时不可用

## 版本

v2.1 - 2026-03-09

## 许可证

MIT License
