# 发布指南：GitHub 与 ClawHub

本文说明如何将 **daily-security-check** 发布到 GitHub 和 [ClawHub](https://clawhub.ai)。

---

## 一、发布前准备

1. **替换 clawhub.json 中的占位符**  
   将 `clawhub.json` 里的 `YOUR_USERNAME` 改为你的 GitHub 用户名：
   - `support_url`: `https://github.com/你的用户名/daily-security-check/issues`
   - `homepage`: `https://github.com/你的用户名/daily-security-check`

2. **确认版本号**  
   `SKILL.md` 的 frontmatter 无需写版本；版本以 `clawhub.json` 的 `version` 和 `CHANGELOG.md` 为准。发布新版本时记得同时更新这两处。

3. **可选：截图与演示视频**  
   ClawHub 建议提供 3–5 张截图（1920×1080 或 1280×720 PNG）和 30–90 秒演示视频，可提高通过率。截图可放在 `screenshots/` 目录（需自行创建）。

---

## 二、发布到 GitHub

1. **在 GitHub 上创建新仓库**  
   - 仓库名建议：`daily-security-check`
   - 可见性：Public
   - 可选：勾选「Add a README」再在本地覆盖，或从空仓库开始

2. **在本地打包并推送到 GitHub**  
   在**仅包含 skill 的目录**下执行（即 `daily-security-check` 为当前目录或其一层父级）：

   ```bash
   cd /path/to/daily-security-check
   git init
   git add .
   git commit -m "chore: initial release v1.0.0"
   git branch -M main
   git remote add origin https://github.com/你的用户名/daily-security-check.git
   git push -u origin main
   ```

   若仓库已存在且你已有 clone：

   ```bash
   cd /path/to/daily-security-check
   git add .
   git commit -m "chore: release v1.0.0"
   git push origin main
   ```

3. **建议**  
   - 在仓库 About 中填写描述与 Topics（如 `openclaw`, `skill`, `security`, `audit`）。
   - 如需，可添加 LICENSE 文件（与 `clawhub.json` 中 `license: "MIT"` 一致）。

---

## 三、发布到 ClawHub（clawhub.ai）

### 方式 A：使用 ClawHub CLI（推荐）

1. **安装并登录**  
   ```bash
   npm i -g clawhub
   clawhub login
   ```
   按提示在浏览器中完成登录（需 ClawHub 账号，GitHub 账号至少注册满一周才能发布）。

2. **进入 skill 目录并发布**  
   ```bash
   cd /path/to/daily-security-check
   clawhub publish . --slug daily-security-check --name "每日安全巡检" --version 1.0.0 --tags latest
   ```
   若希望从父目录指定子目录：
   ```bash
   clawhub publish ./daily-security-check --slug daily-security-check --name "每日安全巡检" --version 1.0.0 --tags latest
   ```

   **若报错 `Error: SKILL.md required`**：多为 skill 目录或其父目录存在 `.git` 时触发的 [ClawHub 已知问题](https://github.com/openclaw/openclaw/issues/32169)。可先复制一份不含 `.git` 的目录再发布：
   ```bash
   cd /path/to/parent-of-daily-security-check
   rsync -av --exclude=.git --exclude=node_modules ./daily-security-check/ /tmp/daily-security-check-pub/
   clawhub publish /tmp/daily-security-check-pub --slug daily-security-check --name "每日安全巡检" --version 1.0.0 --tags latest
   ```

3. **后续更新**  
   修改内容后，更新 `clawhub.json` 的 `version` 和 `CHANGELOG.md`，再执行：
   ```bash
   clawhub publish . --slug daily-security-check --name "每日安全巡检" --version 1.0.1 --tags latest --changelog "修复 xxx"
   ```

### 方式 B：在 ClawHub 网页上传

1. 打开 [clawhub.ai](https://clawhub.ai)，登录开发者账号。
2. 进入「Publish New Skill」或「发布新技能」。
3. **打包 skill**：在本地只打包 `daily-security-check` 目录（不要包含外层无关文件）：
   ```bash
   cd /path/to/parent-of-daily-security-check
   tar -czf daily-security-check.tar.gz daily-security-check/
   ```
4. 在网页上上传 `daily-security-check.tar.gz`。
5. 填写表单：名称、简介、描述、分类（如 utility）、标签（如 security, audit, openclaw）等；若存在 `clawhub.json`，部分字段会自动带出。
6. 上传截图（可选）、填写权限说明与变更说明，提交审核。

### 审核与后续

- 审核通常需要 2–5 个工作日。
- 若被拒，根据反馈修改后更新版本号再重新提交。
- 发布成功后，他人可通过 `clawhub install daily-security-check` 安装。

---

## 四、检查清单（发布前自检）

- [ ] `clawhub.json` 中 `support_url`、`homepage` 已改为你的 GitHub 用户名
- [ ] `clawhub.json` 中 `version` 与 `CHANGELOG.md` 一致
- [ ] `README.md` 能准确描述功能、用法与依赖
- [ ] 仓库已推送到 GitHub 且 About/Topics 已填
- [ ] 已用 `clawhub publish` 或网页上传到 ClawHub，并填写权限说明（本 skill 仅只读检查，无敏感权限）
