# 快速开始指南 - 中文工具包发布

## 🚀 立即执行 (5分钟完成)

### 步骤1: 进入目录
```powershell
cd "C:\Users\你好\.openclaw\workspace\skills\chinese-toolkit"
```

### 步骤2: 运行修复和发布脚本
```powershell
.\fix_and_publish.ps1
```

### 步骤3: 如果ClawHub未登录
```powershell
# 手动登录ClawHub
npx clawhub login

# 然后重新运行脚本
.\fix_and_publish.ps1
```

## 🔧 手动执行步骤 (如果脚本失败)

### 1. 配置Git
```powershell
git config --global user.name "utopia013-droid"
git config --global user.email "utopia013@gmail.com"
```

### 2. 添加GitHub远程仓库
```powershell
git remote add github https://github.com/utopia013-droid/luxyoo.git
```

### 3. 更新版本号
```powershell
npm version patch --no-git-tag-version
```

### 4. 提交代码
```powershell
git add .
git commit -m "发布中文工具包 v1.0.0"
git tag v1.0.0
```

### 5. 推送到GitHub
```powershell
git push github master
git push github v1.0.0
```

### 6. 登录ClawHub
```powershell
npx clawhub login
```

### 7. 发布到ClawHub
```powershell
npx clawhub publish . --version 1.0.0 --description "中文处理工具包"
```

## 📊 验证发布

### 验证GitHub
```powershell
# 访问: https://github.com/utopia013-droid/luxyoo
# 应该能看到你的代码
```

### 验证ClawHub
```powershell
# 搜索技能
npx clawhub search chinese-toolkit

# 查看技能信息
npx clawhub info chinese-toolkit
```

## 🚨 常见问题解决

### 问题1: "remote origin already exists"
```powershell
# 查看现有远程仓库
git remote -v

# 删除错误的远程仓库
git remote remove origin

# 添加正确的远程仓库
git remote add github https://github.com/utopia013-droid/luxyoo.git
```

### 问题2: "error: src refspec main does not match any"
```powershell
# 检查当前分支
git branch

# 如果使用master分支
git push github master

# 如果使用main分支
git push github main
```

### 问题3: "Not logged in. Run: clawhub login"
```powershell
# 登录ClawHub
npx clawhub login

# 按照提示操作
```

## 📞 支持

### 如果所有方法都失败：
```
1. 截图错误信息
2. 访问: https://github.com/utopia013-droid/luxyoo/issues
3. 创建新的issue
4. 粘贴错误信息
```

### 紧急联系：
```
📧 邮箱: utopia013@gmail.com
🔗 GitHub: utopia013-droid
```

## 🎉 成功标志

### 发布成功后：
```
✅ GitHub仓库有代码
✅ GitHub有v1.0.0标签
✅ ClawHub能搜索到技能
✅ 可以安装: openclaw skills install chinese-toolkit
```

### 庆祝活动：
```
🎊 在GitHub标星自己的项目
🎊 在OpenClaw社区分享
🎊 记录发布经验
🎊 规划下一步功能
```

---
**最后提醒：**

**运行这个命令开始：**
```powershell
cd "C:\Users\你好\.openclaw\workspace\skills\chinese-toolkit"
.\fix_and_publish.ps1
```

**祝你发布顺利！** 🚀🎉