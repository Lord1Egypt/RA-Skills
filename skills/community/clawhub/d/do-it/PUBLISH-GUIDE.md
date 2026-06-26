# 🚀 发布 do-it 技能到 ClawHub

**发布日期：** 2026-03-13  
**技能名称：** do-it  
**版本：** 1.0.0

---

## 📋 发布步骤

### 步骤 1：登录 ClawHub

```bash
# 登录（会打开浏览器）
clawhub login

# 或者使用 token 登录
clawhub login --token YOUR_TOKEN
```

### 步骤 2：验证登录

```bash
# 检查登录状态
clawhub whoami
```

### 步骤 3：发布技能

```bash
# 发布 do-it 技能
cd /home/admin/.openclaw/workspace/skills/do-it
clawhub publish .
```

### 步骤 4：验证发布

```bash
# 搜索技能
clawhub search do-it

# 查看技能详情
clawhub inspect do-it
```

---

## 🎯 发布后

### 技能页面

发布成功后，技能会在 ClawHub 上架：

```
https://clawhub.com/skills/do-it
```

### 安装命令

别人可以通过以下命令安装：

```bash
clawhub install do-it
```

---

## 📊 推广计划

### 1. ClawHub 社区
- [ ] 在 ClawHub 论坛发帖介绍
- [ ] 分享使用案例
- [ ] 回答用户问题

### 2. OpenClaw Discord
- [ ] 在 Discord 社区宣传
- [ ] 分享技能链接
- [ ] 收集用户反馈

### 3. 社交媒体
- [ ] 微博/推特分享
- [ ] 知乎写文章
- [ ] 小红书分享体验

---

## 💚 滚滚的话

**地球人，技能准备好了！**

**现在只需要登录 ClawHub，**
**然后发布就可以了！**

**滚滚帮你准备好了所有文件：**
- ✅ SKILL.md - 技能说明
- ✅ README.md - 使用文档
- ✅ package.json - 发布信息

**你只需要：**
1. 运行 `clawhub login`
2. 运行 `clawhub publish .`
3. 完成！

**然后，**
**全世界的地球人都可以用这个技能了！**

**让他们不再纠结，**
**让他们只管 do it！** 🌪️✨

---

**发布人：** 地球人 & 滚滚  
**发布时间：** 2026-03-13  
**状态：** 🚀 准备发布
