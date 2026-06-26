# Contributing Guide

感谢你对 Fitness Personal Assistant 的贡献！在提交 PR 之前，请阅读以下内容。

---

## 🚀 快速开始

### 1. Fork 仓库

访问 [https://github.com/leozvc/fitness-personal-assistant](https://github.com/leozvc/fitness-personal-assistant) 并点击 "Fork" 按钮。

### 2. 克隆到本地

```bash
git clone https://github.com/YOUR_USERNAME/fitness-personal-assistant.git
cd fitness-personal-assistant
```

### 3. 配置开发环境

```bash
# 复制配置模板
cp config.example.json ~/.openclaw/workspace/body-management-data/config.json

# 编辑配置 (填入你的 API 凭证)
nano ~/.openclaw/workspace/body-management-data/config.json

# 测试安装
./scripts/meal-to-intervals.sh --health-check
```

---

## 📝 贡献流程

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或 fix/bugfix-description
```

### 2. 修改代码

- 保持代码风格一致
- 添加必要的注释
- 更新相关文档

### 3. 测试

```bash
# 饮食记录测试
./scripts/meal-to-intervals.sh --text "早餐一个鸡蛋"

# 状态报告测试
./scripts/intervals-status-reporter.sh
```

### 4. 提交

```bash
git add .
git commit -m "feat: 添加新功能描述"

# 或使用 conventional commits:
# feat: 添加新食物类别识别
# fix: 修复 API 连接超时问题
# docs: 更新 README 配置说明
# refactor: 优化代码结构
```

### 5. 推送到远程

```bash
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

- 填写清晰的 PR 描述
- 引用相关的 issue (如果有的话)
- 等待维护者 review

---

## 📋 代码规范

### Shell 脚本

```bash
#!/bin/bash
set -euo pipefail  # 始终使用这些设置

# 变量命名：大写 + 下划线
MY_VARIABLE="value"

# 函数命名：小写 + 下划线
my_function() {
    local local_var="local variable"
    # ...
}
```

### Markdown 文档

- 使用英文标题和代码块
- 中文注释说明关键逻辑
- 链接使用相对路径

---

## 🎯 优先级高的贡献

| 类型 | 说明 | 优先级 |
|------|------|--------|
| 📊 中文食物数据库 | 补充更多中国食材的营养数据 | 🔴 P0 |
| 🔌 其他平台集成 | MyFitnessPal, Google Fit 等 | 🟡 P1 |
| 🧪 单元测试 | 添加自动化测试用例 | 🟡 P1 |
| 🎨 UI 改进 | ASCII art 图表美化 | 🟢 P2 |
| 📖 多语言翻译 | 将文档翻译成其他语言 | 🟢 P2 |

---

## 💡 常见问题

### Q: 如何添加新的食物类别？

A: 编辑 `scripts/meal-to-intervals.sh` 中的 `estimate_nutrition_item()` 函数:

```bash
# 在你的分类中添加
if echo "$name_lower" | grep -qE "(你的食物类别)"; then
    printf "%.2f %.2f %.2f %.2f\n" calories protein fat carbs
    return
fi
```

### Q: 如何测试自定义食物？

A: 使用干跑模式:

```bash
./scripts/meal-to-intervals.sh --dry-run --text "午餐一份宫保鸡丁"
```

---

## 📄 License

通过提交代码，你同意你的贡献遵循 MIT License。

---

**感谢你的贡献！🎉**
