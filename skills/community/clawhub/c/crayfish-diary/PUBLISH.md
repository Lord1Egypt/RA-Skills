# GitHub 发布指南

## 快速发布步骤

### 1. 初始化 Git 仓库

```bash
cd /Users/italks/WorkBuddy/Claw/.codebuddy/skills/crayfish-diary
git init
```

### 2. 添加所有文件

```bash
git add .
```

### 3. 创建首次提交

```bash
git commit -m "feat: 初始化龙虾日记技能 v1.0.0

- 实现日记快速记录功能
- 支持年/月/日目录结构
- 自动生成每日摘要
- 支持标签分类
- 提供中英文文档"
```

### 4. 添加远程仓库

```bash
git remote add origin https://github.com/italks/crayfish-diary.git
```

### 5. 推送到 GitHub

```bash
git branch -M main
git push -u origin main
```

## 技能文件清单

已完成的技能文件：

```
crayfish-diary/
├── SKILL.md              # 技能主文档（必需）
├── README.md             # 英文说明文档
├── README_CN.md          # 中文说明文档
├── clawhub.json          # ClawHub 发布配置
├── scripts/
│   └── create_diary.py   # 日记创建脚本
├── assets/
│   └── crayfish_icon.svg # 龙虾图标
└── .gitignore            # Git 忽略文件配置
```

## 发布到技能平台

### WorkBuddy Skills

1. 打包技能：
```bash
cd /Users/italks/WorkBuddy/Claw/.codebuddy/skills
zip -r crayfish-diary.zip crayfish-diary/ -x "*.git*"
```

2. 访问 WorkBuddy 技能中心
3. 上传 `crayfish-diary.zip`

### ClawHub

1. 在 ClawHub 注册账户
2. 提交 GitHub 仓库地址：`https://github.com/italks/crayfish-diary.git`
3. 等待审核通过

## 版本更新流程

1. 修改代码
2. 更新 `clawhub.json` 中的 `version` 字段
3. 提交更改：
```bash
git add .
git commit -m "chore: 更新版本到 v1.x.x"
git push
```
4. 重新打包并发布

## 技能信息

- **名称**: crayfish-diary
- **版本**: 1.0.0
- **作者**: italks
- **仓库**: https://github.com/italks/crayfish-diary.git
- **许可证**: MIT

## 触发命令

- 开始记录: "帮我记一下"
- 结束记录: "结束记录"

## 功能特性

✅ 自动创建年/月/日目录结构  
✅ 智能标题提取  
✅ 标签分类支持  
✅ 每日摘要自动生成  
✅ Markdown 格式存储  
✅ 中英文双语文档
