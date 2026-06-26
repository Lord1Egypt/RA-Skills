## 目标

让开发者（或 AI）在一台新机器上，完成 `cloudcc-cli` 的安装、模板项目创建、开发密钥配置，并能通过 `cc` 命令进行开发与发布。

---

## 安装 cloudcc-cli

### 全局安装

```bash
# Windows
npm i -g cloudcc-cli

# macOS（通常需要 sudo）
sudo npm i -g cloudcc-cli
```

### 验证版本

```bash
cc -v
```

> 说明：`cc` 是该 CLI 的统一入口命令之一（见本仓库 `package.json` 的 bin 配置）。

---

## 创建 CloudCC 模板项目

在你的工作目录下执行：

```bash
cc create project demo1
cd demo1
npm i
npm run serve
```

如果能在本地启动并访问页面，说明前端开发链路可用。

---

## 配置开发者密钥与安全标记

### 在 CloudCC CRM 后台获取

你需要一个具备“代码管理/开发者权限”的账号。

- **开发者密钥（CloudCCDev）**：在 CRM 后台「连接的应用程序」中新建后获取并复制。
- **安全标记（safetyMark）**：在个人设置中重置安全标记后，通过邮箱获取。

### 写入项目的 `cloudcc-cli.config.js`

模板项目根目录通常会有 `cloudcc-cli.config.js`（或你们约定的同名配置文件），核心原则：

- **多环境**：用 `use` 字段选择当前环境（如 `dev/uat/prod`）。
- **不要提交真实密钥到 Git**：建议 `.gitignore` 忽略配置文件，或用本地私密文件方式管理。

