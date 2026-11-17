# 发布手册：把 geo-plan-generator 上架 ClawHub 市场

本手册覆盖**从本地已准备好的代码，到用户在 WorkBuddy 里能搜到安装**的完整链路。  
你本地目录 `geo-plan-generator/` 已经 git 初始化并提交了第一版，下面的步骤从此开始。

---

## 整体链路（4 步）

```
① 本地代码  ──推──▶  ② GitHub 公开仓库
                               │
                               ▼
③ ClawHub 发布（CLI 或网页） ──▶  ④ 用户在 WorkBuddy 安装使用
```

预估耗时：第一次约 20–40 分钟（含账号注册）；后续升级版本只改第④步。

---

## 前置准备（一次性）

| 工具           | 用途            | 获取方式                               |
| ------------ | ------------- | ---------------------------------- |
| GitHub 账号    | 托管代码          | <https://github.com> （免费注册）        |
| Git          | 提交 + 推送       | 已装（你环境里有）                          |
| Node.js ≥ 18 | 装 ClawHub CLI | 你环境已有                              |
| ClawHub 账号   | 发布技能          | 用 GitHub 账号登录 <https://clawhub.ai> |



---

## 第①步 · 在 GitHub 创建公开仓库

1. 打开 <https://github.com/new>
2. 填写：
   - **Repository name**：`geo-plan-generator`（必须和 skill 的 name 一致）
   - **Description**：`AI-GEO 全域营销方案生成器 —— Word 提词器 + PPT 展示版两件套`
   - **Visibility**：选 **Public**（公开，否则 ClawHub 拉不到）
   - 不要勾 "Add a README"（本地已有，避免冲突）
3. 点 **Create repository**
4. 记下仓库地址，形如：`https://github.com/你的用户名/geo-plan-generator.git`

---

## 第②步 · 推送本地代码到 GitHub

在本地 `geo-plan-generator/` 目录下执行（替换 `你的用户名`）：

```bash
cd /c/Users/Administrator/WorkBuddy/2026-07-26-11-43-36/geo-plan-generator

# 关联远程仓库（替换成你自己的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/geo-plan-generator.git

# 把默认分支改名为 main（GitHub 现在默认 main）
git branch -m master main

# 首次推送
git push -u origin main
```

**验证**：刷新 GitHub 页面，能看到 `README.md` / `SKILL.md` / `references/methodology.md` 三个文件即成功。

> 如果 push 提示要登录：GitHub 现在不支持密码，用 **Personal Access Token**（设置 → Developer settings → PAT，勾 repo 权限）当密码填；或用 GitHub Desktop 客户端更省事。

---

## 第③步 · 发布到 ClawHub

### 方式 A · 命令行（推荐，最快）

```bash
# 安装 ClawHub CLI
npm install -g clawhub

# 用 GitHub 账号登录（浏览器弹窗授权）
clawhub login

# 发布技能
clawhub skill publish ./geo-plan-generator \
  --slug geo-plan-generator \
  --version 1.0.0 \
  --name "GEO 营销方案生成器" \
  --description "AI-GEO 全域营销方案生成器，交付 Word 提词器 + PPT 展示版两件套" \
  --category marketing \
  --tags "geo,marketing,content-creation,360-zhijian"
```

发布成功后命令行会给一个 ClawHub 页面链接（形如 `https://clawhub.ai/skills/geo-plan-generator`）。

### 方式 B · 网页上传（不想装 CLI 时用）

1. 打开 <https://clawhub.ai/import>
2. 授权 GitHub 登录
3. 选仓库 `你的用户名/geo-plan-generator`
4. 填表单：
   - Name：`GEO 营销方案生成器`
   - Slug：`geo-plan-generator`（自动带出）
   - Version：`1.0.0`
   - Category：`Marketing`
   - Tags：`geo, marketing, content-creation`
5. 点 Submit → 进入**审核队列**（一般 1–3 个工作日）

---

## 第④步 · 用户安装使用

审核通过后，任何 WorkBuddy 用户都能：

**方式一（对话）**：在 WorkBuddy 里说

> "帮我安装 geo-plan-generator 技能"

**方式二（命令行）**：

```bash
clawhub install geo-plan-generator
```

装完即可对 WorkBuddy 说："给 XX 公司出一份 GEO 方案"，技能会自动产出 Word + PPT 两件套。

---

## 后续升级版本

代码改完 → 提交 → 推送 → 重新 publish 即可：

```bash
# 本地改完文件后
git add .
git commit -m "feat: v1.1.0 - 增加 XX 能力"
git push

# 重新发布（version 改成 1.1.0）
clawhub skill publish ./geo-plan-generator --slug geo-plan-generator --version 1.1.0
```

---

## 常见问题

**Q：ClawHub 是什么？**  
A：WorkBuddy 生态的官方开源技能市场，免费发布、用户直接在应用内搜索安装。

**Q：发布要钱吗？**  
A：ClawHub 免费。

**Q：审核要多久？**  
A：首次 1–3 个工作日，主要是安全扫描 + 功能验证。

**Q：用户装了以后，我的 SKILL.md 里写的依赖（docx / pptxgenjs）会自动装吗？**  
A：不会。用户首次运行技能时，WorkBuddy 会在本地 node 环境里自动安装这两个包（技能脚本里已写 `npm install` 逻辑）。你在本地已验证过能跑通即可。

**Q：我能改作者名 / 加 Logo 吗？**  
A：作者名改 SKILL.md frontmatter 的 `author` 字段；Logo 暂不支持，ClawHub 用默认图标。

**Q：想撤下怎么办？**  
A：ClawHub 控制台里点 Unpublish 即可，不影响已安装用户的使用。

---

## 检查清单（发布前自查）

- [ ] GitHub 仓库是 **Public**
- [ ] 仓库里有 `SKILL.md` + `README.md` + `references/`（至少这三项）
- [ ] `SKILL.md` frontmatter 有 `name` / `version` / `description` / `license`
- [ ] 本地已 `git push` 成功（GitHub 网页能看到最新文件）
- [ ] ClawHub 账号已用 GitHub 登录
- [ ] skill 的 `name` 和 ClawHub `--slug` 完全一致
