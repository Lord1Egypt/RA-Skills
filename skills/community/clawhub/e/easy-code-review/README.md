# AI代码审核助手 (Code Review Assistant)

<div align="center">

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**教会小龙虾成为你的专属代码审核助手**

[功能介绍](#功能介绍) • [安装使用](#安装使用) • [上传指南](#上传到clawhub) • [配置说明](#配置说明)

</div>

---

## 📖 功能介绍

本技能为OpenClaw（小龙虾）赋予智能代码审核能力，主要功能包括：

### ✅ 需求符合性检查
- 分析AI修改的代码是否符合原始需求描述
- 识别过度设计或偏离需求的修改
- 提供符合性评分和改进建议

### 🔍 非必要修改检测
- 识别与需求无关的文件修改
- 标记可疑的配置文件变更
- 评估修改的风险等级

### 📊 代码质量审查
- 检查代码风格一致性
- 识别常见安全漏洞
- 提供最佳实践建议

### 🎯 变更影响分析
- 分析修改的影响范围
- 评估对现有功能的影响
- 识别潜在的副作用

---

## 🚀 安装使用

### 前置要求
- OpenClaw 版本 >= 2026.2
- Git（用于获取代码变更）

### 安装方式

#### 方式1：从ClawHub安装（推荐）
```
访问 https://clawhub.ai/skills
搜索 "easy-code-review"
点击安装
```

#### 方式2：手动安装
```bash
# 1. 下载本skill到OpenClaw的skills目录
git clone <repository-url>
cp -r easy-code-review /path/to/openclaw/skills/easy-code-review

# 2. 重启OpenClaw或重新加载skills
```

### 使用示例

#### 示例1：审核最近的代码修改
```
用户：帮我review一下最近的git commit，检查是否符合需求
小龙虾：[执行审核并输出报告]
```

#### 示例2：验证特定需求
```
用户：审核这段代码修改
需求：添加用户登录功能，支持用户名密码登录并返回token

修改的文件：
- src/auth/login.ts
- src/models/user.ts
- package.json

小龙虾：[分析修改并输出详细报告]
```

---

## 📤 上传到ClawHub

### 步骤1：准备Skill包

确保你的skill包含以下文件：

```
easy-code-review/
├── SKILL.md              # 必需：核心技能描述文件
├── references/           # 可选：参考资料
│   └── review-guidelines.md
├── scripts/              # 可选：辅助脚本
│   └── analyze_changes.py
└── README.md             # 可选：说明文档
```

### 步骤2：验证SKILL.md格式

确保 `SKILL.md` 包含正确的YAML前置信息：

```yaml
---
name: easy-code-review             # 必需：技能名称（唯一标识）
description: AI代码审核助手...      # 必需：技能描述
version: 1.0.0                     # 必需：版本号
author: Your Name                  # 推荐作者信息
permissions:                       # 必需：权限声明
  - file.read
  - file.write
  - git.read
tags:                              # 推荐：标签便于搜索
  - code-review
  - ai-assistant
min_openclaw_version: 2026.2      # 推荐：最低版本要求
---
```

### 步骤3：创建ClawHub账号

1. 访问 **https://clawhub.ai**
2. 注册账号并登录
3. 完成开发者认证（如需要）

### 步骤4：上传Skill

#### 方法A：Web界面上传

1. 登录ClawHub后，进入 **"My Skills"** 页面
2. 点击 **"Upload New Skill"**
3. 选择你的skill文件夹或打包的zip文件
4. 填写技能信息：
   - 技能名称
   - 简短描述
   - 详细说明
   - 分类标签
   - 截图（可选）
5. 点击 **"Publish"** 发布

#### 方法B：CLI工具上传

```bash
# 安装ClawHub CLI
npm install -g clawhub-cli

# 登录
clawhub login

# 上传skill
clawhub publish ./easy-code-review

# 或指定路径
clawhub publish --path ./openclaw-autosql
```

### 步骤5：审核与发布

- ClawHub会自动验证skill格式和内容
- 可能需要人工审核（首次上传）
- 审核通过后即可公开或私有分享

---

## ⚙️ 配置说明

### 自定义审核行为

在项目中创建 `.claw/review-config.yaml`：

```yaml
review:
  # 审核严格程度：strict（严格）| normal（正常）| loose（宽松）
  strictness: normal
  
  # 关注的重点领域
  focus_areas:
    - requirement_alignment    # 需求符合性
    - unnecessary_changes      # 非必要修改
    - code_quality            # 代码质量
    - security                # 安全问题
  
  # 忽略的文件模式
  ignore_patterns:
    - "*.test.ts"
    - "*.spec.js"
    - "dist/**"
    - "node_modules/**"
  
  # 自定义规则
  custom_rules:
    - "不允许修改.env文件"
    - "package.json修改需要确认"
    - "禁止删除测试文件"
  
  # 输出格式
  output_format: markdown  # markdown | json | html
```

### Git Hook集成

自动在提交前执行审核：

```bash
# 创建pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# 自动执行代码审核
echo "正在执行代码审核..."
claw skill run easy-code-review --staged
EOF

chmod +x .git/hooks/pre-commit
```

### CI/CD集成

在GitHub Actions中使用：

```yaml
# .github/workflows/code-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      
      - name: Setup OpenClaw
        run: |
          # 安装OpenClaw
          curl -fsSL https://get.openclaw.ai | sh
      
      - name: Run Code Review
        run: |
          claw skill run easy-code-review \
            --commit ${{ github.event.pull_request.head.sha }} \
            --output json > review-report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: review-report
          path: review-report.json
```

---

## 📚 输出示例

### 标准审核报告

```markdown
# 代码审核报告

## 概览
- 审核时间：2026-03-11 15:30:00
- 修改文件数：4
- 总体评分：8/10
- 风险等级：🟢 低风险

## 需求符合性检查

### 原始需求
添加用户登录功能，支持用户名密码登录并返回token

### 关键要点提取
- 功能点1: 用户名密码验证
- 功能点2: 生成并返回token
- 功能点3: 登录失败处理

### 修改分析
| 修改文件 | 修改内容 | 符合性 | 说明 |
|---------|---------|-------|------|
| src/auth/login.ts | 新增登录逻辑 | ✅ | 直接实现登录功能 |
| src/models/user.ts | 添加验证方法 | ✅ | 支持用户验证 |
| package.json | 添加jwt库 | ✅ | 支持token生成 |
| tsconfig.json | 修改编译选项 | ⚠️ | 非必要修改 |

## 非必要修改检测

### ✅ 必要修改（3个）
- src/auth/login.ts：核心功能文件
- src/models/user.ts：用户验证逻辑
- package.json：添加依赖

### ⚠️ 可疑修改（1个）
- tsconfig.json：配置文件修改，建议确认是否必要

### ❌ 不必要修改（0个）
无

## 改进建议

1. 建议撤销tsconfig.json的修改，除非确实需要
2. 添加单元测试覆盖登录功能
3. 考虑添加登录失败次数限制
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- [OpenClaw官网](https://openclaw.ai)
- [ClawHub技能市场](https://clawhub.ai)
- [OpenClaw文档](https://docs.openclaw.ai)
- [Skill开发指南](https://docs.openclaw.ai/skills)

---

<div align="center">

**如果这个skill对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by OpenClaw Community

</div>
