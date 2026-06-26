# Free Buddy Skills

一键配置 opencode.ai 免费 AI 模型到 WorkBuddy。

## 快速使用

### 配置免费模型

直接把这句话发给 WorkBuddy:

```
帮我配置 opencode.ai 的免费模型
```

WorkBuddy 会自动:
1. 查询最新的免费模型列表
2. 添加到 `~/.workbuddy/models.json`
3. 验证配置是否可用

### 更新免费模型

下次只需要说:

```
更新免费模型
```

WorkBuddy 会自动:
1. 查询最新的免费模型列表
2. 对比现有配置
3. 添加新模型,跳过已存在的

## 支持的免费模型

| 模型 | 工具调用 | 图像 | 推理 |
|------|----------|------|------|
| minimax-m2.5-free | ✅ | ❌ | ✅ |
| trinity-large-preview-free | ✅ | ✅ | ✅ |
| nemotron-3-super-free | ✅ | ✅ | ✅ |

## 安装方式

### 方式 1: 通过 WorkBuddy 安装 (推荐)

直接把这句话发给 WorkBuddy:

```
安装 free-buddy-skills 技能
```

WorkBuddy 会自动从 GitHub/Gitee 下载并安装。

### 方式 2: 手动安装

**从 Gitee 安装 (国内推荐):**
```bash
cd ~/.workbuddy/skills
git clone https://gitee.com/pinke/free-buddy-skills.git
```

**从 GitHub 安装:**
```bash
cd ~/.workbuddy/skills
git clone https://github.com/pinke/free-buddy-skills.git
```

## 手动运行

```bash
python3 update-free-models.py
```

## 配置位置

- **macOS/Linux**: `~/.workbuddy/models.json`
- **Windows**: `%USERPROFILE%\.workbuddy\models.json`

## 仓库地址

- **Gitee (国内)**: https://gitee.com/pinke/free-buddy-skills
- **GitHub (国际)**: https://github.com/pinke/free-buddy-skills
