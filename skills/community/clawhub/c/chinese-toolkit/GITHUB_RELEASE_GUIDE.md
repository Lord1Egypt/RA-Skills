# GitHub发布指南

## 🎯 发布目标
将中文工具包发布到GitHub仓库：https://github.com/utopia013-droid/luxyoo

## 📋 发布前准备

### 1. 检查当前状态
```bash
# 进入项目目录
cd "C:\Users\你好\.openclaw\workspace\skills\chinese-toolkit"

# 检查Git状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v
```

### 2. 配置GitHub远程仓库
```bash
# 添加GitHub远程仓库
git remote add github https://github.com/utopia013-droid/luxyoo.git

# 或者使用SSH（推荐）
git remote add github git@github.com:utopia013-droid/luxyoo.git

# 验证远程仓库
git remote -v
```

### 3. 更新项目信息
确保以下文件正确：
- `package.json` - 版本号、描述、仓库URL
- `README.md` - 项目介绍、使用说明
- `CHANGELOG.md` - 更新日志
- `LICENSE` - 许可证文件

## 🚀 发布流程

### 步骤1: 更新版本号
```bash
# 查看当前版本
node -e "console.log(require('./package.json').version)"

# 更新版本号（选择一种方式）
# 方式A: 手动更新package.json中的version字段
# 方式B: 使用npm version命令
npm version patch  # 小版本更新 (1.0.0 → 1.0.1)
npm version minor  # 中版本更新 (1.0.0 → 1.1.0)
npm version major  # 大版本更新 (1.0.0 → 2.0.0)
```

### 步骤2: 提交更改
```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "发布版本 v1.0.0 - 中文工具包初始版本"

# 或者使用更详细的提交信息
git commit -m "feat: 发布中文工具包 v1.0.0

- 添加中文分词功能
- 添加拼音转换功能
- 添加文本统计功能
- 添加关键词提取功能
- 添加翻译功能
- 完善文档和示例"
```

### 步骤3: 推送到GitHub
```bash
# 推送到GitHub主分支
git push github master

# 或者推送到main分支（如果仓库使用main）
git push github master:main

# 创建并推送标签
git tag v1.0.0
git push github v1.0.0

# 或者一次性推送所有标签
git push github --tags
```

### 步骤4: 创建GitHub Release
```bash
# 使用GitHub CLI（如果已安装）
gh release create v1.0.0 \
  --title "中文工具包 v1.0.0" \
  --notes "初始版本发布，包含核心中文处理功能" \
  --target master

# 或者通过GitHub网页界面创建
# 1. 访问: https://github.com/utopia013-droid/luxyoo/releases/new
# 2. 选择标签: v1.0.0
# 3. 填写标题和描述
# 4. 上传文件（可选）
# 5. 点击"发布版本"
```

### 步骤5: 验证发布
```bash
# 克隆仓库验证
cd /tmp
git clone https://github.com/utopia013-droid/luxyoo.git
cd luxyoo

# 测试安装
npm install

# 运行测试
npm test

# 验证功能
node -e "const tools = require('./index.js'); console.log(tools.segment('测试中文分词'))"
```

## 📦 发布包准备

### 1. 创建发布包
```bash
# 创建压缩包
tar -czf chinese-toolkit-v1.0.0.tar.gz --exclude="node_modules" --exclude=".git" .

# 或者使用npm pack
npm pack

# 或者创建ZIP包
7z a chinese-toolkit-v1.0.0.zip . -xr!node_modules -xr!.git
```

### 2. 发布到npm（可选）
```bash
# 登录npm
npm login

# 发布包
npm publish

# 或者发布为公开包
npm publish --access public
```

### 3. 创建安装脚本
```bash
# 创建一键安装脚本
cat > install.sh << 'EOF'
#!/bin/bash
# 中文工具包安装脚本

echo "安装中文工具包..."

# 克隆仓库
git clone https://github.com/utopia013-droid/luxyoo.git
cd luxyoo

# 安装依赖
npm install

# 创建符号链接
npm link

echo "安装完成！"
echo "使用方法:"
echo "  const chineseTools = require('chinese-toolkit')"
echo "  const result = chineseTools.segment('你好世界')"
EOF

chmod +x install.sh
```

## 🔧 自动化发布脚本

### PowerShell自动化脚本
```powershell
# publish_to_github.ps1
param(
    [string]$Version = "patch",
    [string]$Message = "发布新版本"
)

Write-Host "🚀 开始发布到GitHub..." -ForegroundColor Green

# 1. 更新版本号
Write-Host "1. 更新版本号..." -ForegroundColor Cyan
npm version $Version

# 2. 获取新版本号
$version = node -e "console.log(require('./package.json').version)"
Write-Host "新版本: v$version" -ForegroundColor Yellow

# 3. 提交更改
Write-Host "2. 提交更改..." -ForegroundColor Cyan
git add .
git commit -m "$Message v$version"

# 4. 创建标签
Write-Host "3. 创建标签..." -ForegroundColor Cyan
git tag "v$version"

# 5. 推送到GitHub
Write-Host "4. 推送到GitHub..." -ForegroundColor Cyan
git push github master
git push github "v$version"

# 6. 创建Release
Write-Host "5. 创建GitHub Release..." -ForegroundColor Cyan
gh release create "v$version" `
    --title "中文工具包 v$version" `
    --notes "$Message" `
    --target master

Write-Host "✅ 发布完成！" -ForegroundColor Green
Write-Host "📦 版本: v$version" -ForegroundColor Yellow
Write-Host "🔗 仓库: https://github.com/utopia013-droid/luxyoo" -ForegroundColor Cyan
```

### 使用脚本
```powershell
# 小版本更新
.\publish_to_github.ps1 -Version patch -Message "修复bug"

# 中版本更新
.\publish_to_github.ps1 -Version minor -Message "添加新功能"

# 大版本更新
.\publish_to_github.ps1 -Version major -Message "重大更新"
```

## 📊 发布检查清单

### 发布前检查
- [ ] 代码测试通过
- [ ] 文档完整
- [ ] 版本号已更新
- [ ] 提交信息清晰
- [ ] 依赖项已更新
- [ ] 许可证文件正确
- [ ] README.md完整

### 发布中检查
- [ ] 代码已提交
- [ ] 标签已创建
- [ ] 代码已推送到GitHub
- [ ] GitHub Release已创建
- [ ] 发布包已上传（可选）
- [ ] npm发布完成（可选）

### 发布后检查
- [ ] 仓库页面正常显示
- [ ] Release页面正常
- [ ] 安装测试通过
- [ ] 功能测试通过
- [ ] 文档链接正确
- [ ] 问题反馈渠道畅通

## 🛠️ 故障排除

### 常见问题
```
❌ 问题: 推送被拒绝
✅ 解决:
1. 先拉取最新代码: git pull github master
2. 解决冲突后重新推送
3. 使用强制推送（谨慎）: git push github master -f

❌ 问题: npm发布失败
✅ 解决:
1. 检查npm登录状态: npm whoami
2. 检查包名是否重复
3. 更新版本号重新发布

❌ 问题: GitHub CLI错误
✅ 解决:
1. 安装GitHub CLI: winget install GitHub.cli
2. 登录: gh auth login
3. 检查权限
```

### 权限问题
```bash
# 检查SSH密钥
ssh -T git@github.com

# 生成SSH密钥（如果没有）
ssh-keygen -t ed25519 -C "your-email@example.com"

# 添加SSH密钥到GitHub
# 1. 复制公钥: cat ~/.ssh/id_ed25519.pub
# 2. 添加到GitHub: https://github.com/settings/keys
```

## 📈 发布后工作

### 1. 更新文档
```bash
# 更新使用示例
# 更新API文档
# 更新常见问题
```

### 2. 宣传推广
```bash
# 在OpenClaw社区分享
# 在GitHub Trending关注
# 在技术博客介绍
# 在社交媒体宣传
```

### 3. 收集反馈
```bash
# 创建Issue模板
# 设置讨论区
# 收集用户反馈
# 规划下一版本
```

### 4. 维护更新
```bash
# 定期更新依赖
# 修复报告的问题
# 添加新功能
# 优化性能
```

## 🎯 最佳实践

### 版本管理
```
🔢 语义化版本:
• MAJOR.MINOR.PATCH (例如: 1.2.3)
• MAJOR: 不兼容的API更改
• MINOR: 向后兼容的功能添加
• PATCH: 向后兼容的问题修复

📝 提交规范:
• feat: 新功能
• fix: 修复bug
• docs: 文档更新
• style: 代码格式
• refactor: 代码重构
• test: 测试相关
• chore: 构建过程或辅助工具
```

### 发布策略
```
📅 发布周期:
• 小版本: 每周或每两周
• 中版本: 每月或每季度
• 大版本: 每半年或每年

🔄 发布流程:
1. 开发功能
2. 编写测试
3. 更新文档
4. 代码审查
5. 版本发布
6. 验证测试
7. 宣传推广
```

### 质量保证
```
✅ 代码质量:
• 代码审查
• 自动化测试
• 持续集成
• 性能测试

📊 监控指标:
• 下载量
• 用户反馈
• 问题报告
• 使用情况
```

---
**指南版本**: v1.0
**创建时间**: 2026年2月23日
**适用场景**: GitHub仓库发布

**立即开始，发布你的中文工具包！** 🚀📦

**让世界使用你的开源项目！** 🌍💻