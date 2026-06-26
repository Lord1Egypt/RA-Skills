# 双平台发布指南 - GitHub + ClawHub

## 🎯 发布目标
将中文工具包同时发布到两个平台：
1. **GitHub** - 代码托管和开源社区
2. **ClawHub** - OpenClaw技能市场

## 📋 平台对比

### GitHub (代码托管)
```
✅ 优势:
• 代码版本控制
• 开源社区协作
• Issue跟踪和管理
• Pull Request代码审查
• GitHub Actions自动化
• 免费公开仓库

🎯 用途:
• 源代码托管
• 版本管理
• 协作开发
• 文档托管
• 问题跟踪
```

### ClawHub (技能市场)
```
✅ 优势:
• OpenClaw技能市场
• 一键安装和使用
• 技能发现和分享
• 版本管理和更新
• 用户反馈收集
• 技能统计数据

🎯 用途:
• 技能分发
• 用户安装
• 市场推广
• 使用统计
• 社区分享
```

## 🚀 双平台发布流程

### 阶段1: 准备阶段 (5分钟)

#### 1.1 检查项目状态
```powershell
# 进入项目目录
cd "C:\Users\你好\.openclaw\workspace\skills\chinese-toolkit"

# 检查Git状态
git status

# 检查文件结构
dir
```

#### 1.2 更新版本号
```powershell
# 获取当前版本
$currentVersion = node -e "console.log(require('./package.json').version)"
echo "当前版本: v$currentVersion"

# 更新版本号 (如果需要)
npm version patch --no-git-tag-version
$newVersion = node -e "console.log(require('./package.json').version)"
echo "新版本: v$newVersion"
```

### 阶段2: GitHub发布 (10分钟)

#### 2.1 配置GitHub远程仓库
```powershell
# 添加GitHub远程仓库
git remote add github https://github.com/utopia013-droid/luxyoo.git

# 验证配置
git remote -v
```

#### 2.2 提交和推送
```powershell
# 提交更改
git add .
git commit -m "发布中文工具包 v$newVersion"

# 创建标签
git tag "v$newVersion"

# 推送到GitHub
git push github master
git push github "v$newVersion"
```

#### 2.3 创建GitHub Release
```
访问: https://github.com/utopia013-droid/luxyoo/releases/new
填写:
• 标签: v[版本号]
• 标题: 中文工具包 v[版本号]
• 描述: [使用模板]
• 发布版本
```

### 阶段3: ClawHub发布 (10分钟)

#### 3.1 登录ClawHub
```powershell
# 登录ClawHub (使用GitHub OAuth)
npx clawhub login

# 验证登录
npx clawhub whoami
```

#### 3.2 准备技能包
```powershell
# 确保有SKILL.md文件
if (-not (Test-Path "SKILL.md")) {
    # 创建SKILL.md
    Copy-Content from template
}

# 更新package.json中的openclaw配置
# [脚本会自动处理]
```

#### 3.3 发布到ClawHub
```powershell
# 发布技能
npx clawhub publish . --version $newVersion --description "中文处理工具包"
```

#### 3.4 验证发布
```powershell
# 搜索技能
npx clawhub search chinese-toolkit

# 查看技能信息
npx clawhub info chinese-toolkit
```

### 阶段4: 验证和测试 (10分钟)

#### 4.1 GitHub验证
```powershell
# 克隆仓库测试
cd $env:TEMP
git clone https://github.com/utopia013-droid/luxyoo.git
cd luxyoo
npm install
node examples/simple_example.js
```

#### 4.2 ClawHub验证
```powershell
# 安装技能测试 (在另一个OpenClaw环境)
openclaw skills install chinese-toolkit

# 使用技能
node -e "const tools = require('chinese-toolkit'); console.log(tools.segment('测试'))"
```

## 🔧 自动化脚本

### 一键双平台发布脚本
```powershell
# dual_publish.ps1
param(
    [string]$VersionType = "patch",
    [string]$Message = "发布新版本"
)

Write-Host "🚀 开始双平台发布..." -ForegroundColor Green

# 1. 更新版本号
npm version $VersionType --no-git-tag-version
$version = node -e "console.log(require('./package.json').version)"
Write-Host "版本: v$version" -ForegroundColor Yellow

# 2. GitHub发布
Write-Host "发布到GitHub..." -ForegroundColor Cyan
git add .
git commit -m "$Message v$version"
git tag "v$version"
git push github master
git push github "v$version"

# 3. ClawHub发布
Write-Host "发布到ClawHub..." -ForegroundColor Cyan
npx clawhub publish . --version $version --description "$Message"

Write-Host "✅ 双平台发布完成!" -ForegroundColor Green
```

### 使用脚本
```powershell
# 小版本更新
.\dual_publish.ps1 -VersionType patch -Message "修复bug"

# 中版本更新
.\dual_publish.ps1 -VersionType minor -Message "添加新功能"
```

## 📊 发布检查清单

### GitHub检查清单
- [ ] 代码已提交到本地仓库
- [ ] GitHub远程仓库已配置
- [ ] 版本标签已创建
- [ ] 代码已推送到GitHub
- [ ] GitHub Release已创建
- [ ] Release描述完整
- [ ] 文档链接正确

### ClawHub检查清单
- [ ] ClawHub已登录
- [ ] SKILL.md文件存在
- [ ] package.json配置正确
- [ ] 技能包结构完整
- [ ] 发布命令成功
- [ ] 技能可搜索到
- [ ] 技能信息可查看

### 通用检查清单
- [ ] 版本号已更新
- [ ] 文档已更新
- [ ] 示例代码可运行
- [ ] 测试通过
- [ ] 许可证文件正确
- [ ] 依赖项已更新

## 🛠️ 故障排除

### GitHub问题
```
❌ 问题: 推送被拒绝
✅ 解决:
1. 先拉取最新代码: git pull github master
2. 解决冲突后重新推送
3. 使用强制推送 (谨慎)

❌ 问题: 标签已存在
✅ 解决:
1. 删除旧标签: git tag -d v1.0.0
2. 删除远程标签: git push github --delete v1.0.0
3. 使用新版本号
```

### ClawHub问题
```
❌ 问题: 登录失败
✅ 解决:
1. 检查GitHub OAuth授权
2. 重新登录: npx clawhub logout && npx clawhub login
3. 检查网络连接

❌ 问题: 发布失败 - 技能名已存在
✅ 解决:
1. 修改技能名称
2. 或者联系技能所有者
3. 使用不同的名称
```

### 通用问题
```
❌ 问题: 版本号冲突
✅ 解决:
1. 统一两个平台的版本号
2. 使用语义化版本
3. 先更新版本再发布

❌ 问题: 依赖项问题
✅ 解决:
1. 检查package.json依赖
2. 更新依赖版本
3. 测试兼容性
```

## 📈 发布后管理

### 版本同步
```
🔢 版本管理策略:
• 两个平台使用相同版本号
• 先更新GitHub，再更新ClawHub
• 版本变更记录在CHANGELOG.md
• 语义化版本规范
```

### 更新流程
```
🔄 更新发布流程:
1. 开发新功能/修复bug
2. 更新版本号
3. 提交到GitHub
4. 发布到ClawHub
5. 更新文档
6. 通知用户
```

### 用户支持
```
💬 支持渠道:
• GitHub Issues: 技术问题
• ClawHub反馈: 使用问题
• 社区论坛: 讨论交流
• 邮件支持: 商业支持
```

## 🎯 最佳实践

### 代码质量
```
✅ GitHub最佳实践:
• 清晰的提交信息
• 完整的代码审查
• 自动化测试
• 持续集成

✅ ClawHub最佳实践:
• 完整的SKILL.md
• 清晰的安装说明
• 详细的使用示例
• 完善的错误处理
```

### 文档管理
```
📚 文档策略:
• README.md: 项目概述
• API_DOCUMENTATION.md: API文档
• examples/: 使用示例
• CHANGELOG.md: 更新日志
• CONTRIBUTING.md: 贡献指南
```

### 社区建设
```
👥 社区策略:
• 积极回复问题
• 接受功能请求
• 鼓励贡献
• 分享经验
```

## 📞 支持资源

### GitHub资源
```
🔗 官方资源:
• GitHub文档: https://docs.github.com
• GitHub社区: https://github.com/community
• GitHub学习: https://skills.github.com

🛠️ 开发工具:
• GitHub CLI: https://cli.github.com
• GitHub Desktop: https://desktop.github.com
• GitHub Actions: https://github.com/features/actions
```

### ClawHub资源
```
🔗 官方资源:
• ClawHub网站: https://clawhub.com
• GitHub仓库: https://github.com/openclaw/clawhub
• 文档: https://docs.clawhub.com

🛠️ 开发工具:
• ClawHub CLI: npx clawhub
• 技能开发模板
• 发布指南
```

### 学习资源
```
🎓 学习平台:
• OpenClaw文档: https://docs.openclaw.ai
• 技能开发指南
• 最佳实践案例
• 视频教程
```

## 🎉 成功庆祝

### 发布成功标志
```
🎊 双平台发布成功!

📦 GitHub:
• 仓库: https://github.com/utopia013-droid/luxyoo
• Release: https://github.com/utopia013-droid/luxyoo/releases
• 星标: ⭐ [你的星标数]

🛒 ClawHub:
• 技能: chinese-toolkit
• 市场: https://clawhub.com
• 安装: openclaw skills install chinese-toolkit
```

### 宣传推广
```
📢 推广渠道:
1. GitHub标星和分享
2. ClawHub技能推荐
3. OpenClaw社区公告
4. 社交媒体宣传
5. 技术博客分享
```

### 下一步计划
```
🚀 发展计划:
• 收集用户反馈
• 优化功能和性能
• 扩展用户群体
• 建立开发者社区
• 探索商业化机会
```

---
**指南版本**: v1.0
**创建时间**: 2026年2月23日
**适用场景**: GitHub + ClawHub双平台发布

**立即开始，发布你的项目到双平台！** 🚀📦

**让更多人使用和贡献你的开源项目！** 🌍💻