# 发布到 ClawHub 指南

## 前提条件

1. **安装 ClawHub CLI**
   ```bash
   npm i -g clawhub
   ```

2. **登录 ClawHub**
   ```bash
   clawhub login
   ```
   会打开浏览器进行 GitHub 授权。

3. **验证登录**
   ```bash
   clawhub whoami
   ```

## 发布步骤

### 方式 1：使用 clawhub publish 命令（推荐）

```bash
cd /Users/xubangbang/.openclaw/workspace/agents/SKILL-01/skills/china-install-skills/

clawhub publish . \
  --slug china-install-skills \
  --name "China Install Skills" \
  --version 1.0.0 \
  --changelog "v1.0.0 - 初始版本：搜索、下载、安装、一键安装、每周自动更新检查"
```

### 方式 2：手动打包上传

1. **打包 ZIP**
   ```bash
   cd /Users/xubangbang/.openclaw/workspace/agents/SKILL-01/skills/
   zip -r china-install-skills.zip china-install-skills/ \
     -x "*.git*" -x "*.DS_Store" -x "__pycache__/*"
   ```

2. **上传到 ClawHub**
   - 访问 https://clawhub.com/upload
   - 上传 `clawhub-browser.zip`
   - 填写技能信息

## 发布后验证

```bash
# 搜索技能
clawhub search "china-install-skills"

# 或访问网页
https://clawhub.com/skills?q=china-install-skills
```

## 更新技能

```bash
# 修改版本号和 changelog
# 编辑 _meta.json: "version": "1.0.1"

# 重新发布
clawhub publish . --slug china-install-skills --version 1.0.1 --changelog "修复 xxx 问题"
```

## 注意事项

1. **slug 必须唯一** - 如果已被占用，需要换一个
2. **版本号语义化** - 使用 `major.minor.patch` 格式
3. **许可证** - 确保使用开源许可证（MIT-0、MIT、Apache-2.0 等）
4. **安全检查** - 确保脚本没有危险操作

## 中国大陆发布提示

由于网络原因，发布时可能需要：
- 使用稳定的网络环境
- 或使用代理/加速器
- 或等待网络状况好的时候

---

**当前技能信息：**
- 📦 Slug: `china-install-skills`
- 🏷️ 版本：`1.0.0`
- 📝 描述：中国大陆专用 ClawHub 技能安装工具
- 📄 许可证：MIT-0
