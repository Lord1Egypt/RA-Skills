# OpenClaw 本地测试指南

## 当前 skill 结构

```
~/.openclaw/skills/cross-border-intel/
├── SKILL.md           # Skill manifest (OpenClaw 读取)
├── lib/               # Shell 脚本库
├── scripts/           # 可执行脚本
├── local.sqlite3      # 本地数据库
└── templates/         # 模板文件
```

## 测试方案

### 方案 A：直接测试 TypeScript 代码（推荐用于开发）

创建一个测试脚本，直接调用编译后的 TypeScript 代码：

```bash
cd ~/.openclaw/skills/cross-border-intel
node /path/to/beansmile-claw-skills/packages/cross-border-intel/dist/index.js
```

### 方案 B：通过 Shell 脚本包装（兼容 OpenClaw）

创建 shell 脚本包装器来调用 TypeScript 代码。

### 方案 C：符号链接到开发目录

将 OpenClaw skill 目录链接到你的开发目录。

## 开始测试

### 1. 构建 TypeScript skill

```bash
cd /Users/zhuqiangyi/Beansmile/beansmile-claw-skills

# 使用 Node 20
nvm use 20

# 安装依赖
pnpm install

# 构建
pnpm --filter @beansmile/skill-cross-border-intel build
```

### 2. 创建测试脚本

在 OpenClaw skill 目录中创建一个测试包装器。
