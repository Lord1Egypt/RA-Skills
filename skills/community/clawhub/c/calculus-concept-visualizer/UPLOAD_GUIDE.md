# Calculus Concept Visualizer - 上传 ClawHub 指南

本文档指导如何将本 Skill 上传到 https://clawhub.ai/daigxok

---

## 前置准备

### 1. 确认文件完整性

确保以下文件已准备就绪：

```
calculus-concept-visualizer/
├── SKILL.md                    [已创建]
├── hermes.config.yaml          [已创建]
├── README.md                   [已创建]
├── prompts/                    [已创建]
├── tools/                      [已创建]
└── tests/                      [已创建]
```

### 2. 注册 ClawHub 账号

1. 访问 https://clawhub.ai
2. 点击 "Sign Up" 使用 GitHub 账号登录
3. 确认用户名设置为 `daigxok`

---

## 上传步骤

### 方法一：通过 OpenClaw CLI 上传（推荐）

#### 步骤 1: 登录 ClawHub

```powershell
openclaw login
```

#### 步骤 2: 验证并打包

```powershell
cd C:\Users\admin\openclaw-skills\calculus-concept-visualizer
openclaw skills validate
openclaw skills pack -o calculus-concept-visualizer.zip
```

#### 步骤 3: 上传

```powershell
openclaw skills publish --username daigxok
```

### 方法二：手动上传

1. 打包 Skill 为 zip 文件
2. 访问 https://clawhub.ai/daigxok
3. 点击 "+ New Skill"
4. 填写信息：
   - Name: `calculus-concept-visualizer`
   - Description: `基于多表征理论和动态可视化的微积分概念理解助手`
   - Version: `1.0.0`
   - Author: `代国兴`
   - Tags: `calculus, visualization, education, geogebra, 高等数学`
5. 上传 zip 文件并发布

---

## 验证上传

```powershell
# 从 ClawHub 安装测试
openclaw skills install daigxok/calculus-concept-visualizer
openclaw skills list | findstr calculus
openclaw run daigxok/calculus-concept-visualizer --concept limit
```

---

## 成功标志

- [ ] 在 https://clawhub.ai/daigxok 看到 Skill
- [ ] 能成功安装和运行
- [ ] 功能测试通过

---

**作者: 代国兴**
**日期: 2026-04-08**
