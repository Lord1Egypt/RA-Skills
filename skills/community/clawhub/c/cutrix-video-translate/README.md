# Cutrix Python SDK — OpenClaw / ClawHub skill

This folder is a **ClawHub-compatible skill** that teaches OpenClaw-class agents how to use the official Cutrix Python SDK (`cutrix-video-translate-sdk` on PyPI). It is not a second implementation of the API.

Official references:

- [ClawHub Quickstart — publish a skill](https://docs.openclaw.ai/clawhub/quickstart#publish-a-skill)
- [ClawHub CLI (`clawhub`)](https://docs.openclaw.ai/clawhub/cli)
- [Skill format](https://docs.openclaw.ai/clawhub/skill-format)

---

## Publish to Claw Hub（发布到 OpenClaw Hub / ClawHub）

ClawHub 是 OpenClaw 的 **技能与插件注册表**。安装进 OpenClaw 用 `openclaw skills …`；**注册、登录、上传自己的技能**用 **`clawhub` CLI**（见上 Quickstart）。

### 1. 前置条件

1. 在 [clawhub.ai](https://clawhub.ai/) 注册并完成 **GitHub 绑定**（平台对账号/GitHub 有年龄与信任要求，以官网为准）。
2. 本目录根下有 **`SKILL.md`**（必填），且 frontmatter 里 **`author`** 为你的 ClawHub **发布者标识**（与账号一致）。
3. 发布到 ClawHub 的技能按官方说明以 **MIT-0** 许可发布（可自由使用与再分发；详见 CLI 文档中 `skill publish` 说明）。

### 2. 安装 `clawhub` CLI

```bash
npm i -g clawhub
# 或
pnpm add -g clawhub
```

验证：

```bash
clawhub --help
```

### 3. 登录

本机浏览器 OAuth（默认）：

```bash
clawhub login
clawhub whoami
```

无头 / CI：在 ClawHub 网页创建 API token 后：

```bash
clawhub login --token clh_...
```

国内网络若需代理，CLI 会读取 `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY`（见 [CLI 文档](https://docs.openclaw.ai/clawhub/cli#http-proxy)）。

### 4. 发布本技能（推荐命令）

在**本技能目录**下执行（路径按你克隆仓库的位置调整）：

```bash
cd clawhub/cutrix-python-sdk

clawhub skill publish . \
  --slug cutrix-python-sdk \
  --name "Cutrix Python SDK" \
  --version 1.1.0 \
  --changelog "Sync README-aligned language tables and translate/get_task docs"
```

说明：

- **`--version`**：须为 **semver**，且通常与 `SKILL.md` frontmatter 里的 `version` **一致**；每次发新版递增 semver，并同步修改 `SKILL.md` 中的 `version`。
- **`--slug`**：Hub 上的技能标识；首发布后若要改名可用官方 `skill rename` 等流程（见 CLI 文档）。
- **`--changelog`**：建议每次发布都写一句变更说明。
- **`--owner`**：若你以组织发布且账号有权限，可按 CLI 文档追加 `--owner <handle>`。

官方 Quickstart 中的等价示例见：[Publish a skill](https://docs.openclaw.ai/clawhub/quickstart#publish-a-skill)。

**旧式别名：**部分环境仍支持顶层 `clawhub publish`；以 `clawhub skill publish` 与 `clawhub --help` 为准。

发布前可查看子命令全部参数：

```bash
clawhub skill publish --help
```

若你维护多个技能目录，也可用 **`clawhub sync`** 扫描并批量同步（见 [CLI 文档](https://docs.openclaw.ai/clawhub/cli#sync)）。

### 5. 发布后

- 在网页或通过 `clawhub inspect <slug>` 查看元数据、版本与扫描状态。
- 用户在 OpenClaw 侧安装示例（Quickstart）：`openclaw skills install <skill-slug>`。

---

## WorkBuddy / 小龙虾生态（国内助手）

许多国产 AI 助手（口语里常叫「小龙虾」）支持与 **Cursor Agent Skills** 类似的「技能目录」：根文件为 `SKILL.md`，旁挂 `README.md`、脚本与 `requirements.txt`。

- 若产品支持从本仓库或压缩包「导入技能」，请直接选择 **`clawhub/cutrix-python-sdk`** 目录。
- 若产品要求技能放在固定路径（例如项目下的 `.cursor/skills/<name>/`），可将整个 **`cutrix-python-sdk`** 文件夹复制过去，保持 `SKILL.md` 在目录根部。
- 具体菜单名称以各产品文档为准；本技能不依赖境外服务即可被代理读取，**实际调用 Cutrix API 仍需网络可达 `https://www.cutrix.cc` 与用户自备的 API Key**。

---

## Local smoke check

```bash
pip install -r requirements.txt
python scripts/check_install.py
```

## Repository layout

The Python SDK lives under `src/cutrix/` at the repo root. This skill only documents how to **install and call** that package from agent-generated code.
