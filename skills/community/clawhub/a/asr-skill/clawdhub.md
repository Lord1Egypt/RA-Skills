# 发布到 ClawdHub 指南

## 🚀 一键发布

### 方式一：使用 Claw CLI（推荐）

1. **安装 Claw CLI**
   ```bash
   npm install -g @clawdhub/cli
   ```

2. **登录 ClawdHub**
   ```bash
   claw login
   ```
   按照提示输入你的ClawdHub账号和API密钥。

3. **发布Skill**
   ```bash
   claw publish
   ```
   CLI会自动读取 `skill.yml` 中的配置，打包并上传到ClawdHub。

### 方式二：手动上传

1. 打包项目文件：
   ```bash
   zip -r qwen-asr-skill.zip . -x "models/*" "uploads/*" "node_modules/*" "__pycache__/*" "*.log" ".env" ".git/*"
   ```

2. 访问 [ClawdHub官网](https://clawdhub.com)，登录你的账号

3. 点击"发布Skill"，选择刚才打包的zip文件

4. 填写Skill信息，系统会自动识别 `skill.yml` 中的配置

## 📋 发布前检查清单

✅ 确保所有必需文件都已包含：
- `skill.yml` - Skill配置文件
- `package.json` - Node.js依赖配置
- `requirements.txt` - Python依赖配置
- `index.js` - 主服务入口
- `asr.py` - 推理模块
- `README.md` - 使用说明
- `INSTALL.md` - 安装指南

✅ 确保 `.clawdignore` 配置正确，忽略了大文件和敏感信息

✅ 测试服务可以正常启动：
```bash
npm install
pip install -r requirements.txt
npm start
```

✅ 测试API接口正常：
```bash
curl http://localhost:3000/health
```

## ⚙️ 发布后配置

发布成功后，你可以在ClawdHub控制台配置：

1. **环境变量**：可以在控制台设置环境变量，覆盖默认配置
2. **资源限制**：配置CPU、内存、磁盘等资源限制
3. **访问控制**：设置Skill的公开/私有访问权限
4. **版本管理**：管理不同版本的Skill，支持回滚
5. **使用统计**：查看Skill的调用次数、延迟等统计数据

## 📝 版本更新

发布新版本时，只需更新 `skill.yml` 中的 `version` 字段，然后重新执行 `claw publish` 即可。

版本号遵循语义化版本规范：`主版本号.次版本号.修订号`
- 主版本号：不兼容的API更改
- 次版本号：新增功能，向下兼容
- 修订号：bug修复，向下兼容

## 🎯 ClawdHub 功能

发布后，你的Skill将获得以下能力：

- 🌐 全局CDN加速，全球用户低延迟访问
- 📊 详细的使用统计和监控
- 🔒 自动安全扫描和漏洞检测
- 📦 一键部署到Clawd边缘节点
- 💰 可选的付费使用设置
- 👥 用户评价和反馈系统
- 🔄 自动版本更新推送

## 📞 技术支持

如果发布过程中遇到问题：

1. 查看 [ClawdHub官方文档](https://docs.clawdhub.com)
2. 提交Issue到项目仓库
3. 联系ClawdHub技术支持

## 🏷️ 标签建议

为了让更多用户找到你的Skill，建议添加以下标签：
`asr` `speech-recognition` `dialect` `qwen` `语音识别` `方言` `ai` `openclaw`