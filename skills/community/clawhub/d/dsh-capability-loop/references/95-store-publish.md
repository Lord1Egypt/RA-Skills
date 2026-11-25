# 95 · 上架技能商店（SkillHub / ClawHub）实操

> **网络边界**：本 skill **运行时不发起网络请求**；文中的 `clawhub.ai` / `skillhub.cn` / API URL 仅用于**人工核对**与**手动发布**，不参与技能执行。
>
> **结论先行**：DSH 的「技能市场」是 **SkillHub 的浏览/安装客户端，不是发布端**；SkillHub 上的 skill 主要来自 **ClawHub（OpenClaw 官方 registry）的同步**。所以「把 skill 上架商店」的可行路径是：
> **发布到 ClawHub → SkillHub 同步 → DSH 技能市场搜索/安装**。
> 本文给出可执行命令、证据来源和**尚未实测**的部分；照做前先读 §6。

## 1. 三层关系（先分清，避免走错入口）

| 层 | 是什么 | 你能做什么 |
|---|---|---|
| **ClawHub**（`clawhub.ai`） | OpenClaw 官方公开 registry，`clawhub` CLI 负责 login/publish/install | **发布 skill**、管理版本、搜索 |
| **SkillHub**（`skillhub.cn`） | 腾讯的国内镜像/精选社区，同步 ClawHub 全量 skill + 中文分类/精选/安全扫描 | 浏览、搜索；发布仍回 ClawHub（见 §6） |
| **DSH 技能市场**（插件 `@montersy123/dsh-skill-market`） | 侧边栏面板，读 SkillHub API，把 skill 装进 `~/.dsh/skills/<handle>--<slug>/` | 浏览/搜索/**一键安装**、启用/停用、更新/回滚、本地 zip 导入；**没有上架入口** |

## 2. 证据（2026-11-13 本机核对）

| 结论 | 证据 |
|---|---|
| 市场是 SkillHub 客户端，不含发布 | 插件 README：面板「把 SkillHub 的技能库变成可浏览、筛选、搜索、安装」；包内 `lib/index.js` 实读 **16 个路由**（`/state /skills /skill-detail /skill-file /skill-files /skill-security /skill-versions /categories /category-counts /build /enabled /import /install /installed /prefs /uninstall`），其中**没有向 SkillHub/ClawHub 发布或上传的路由**；唯一的「上传」是**本地导入** `POST /skill-market/api/import`（`client.js:2262-2274` `apiUpload`），不是上架 |
| 市场记录有 `origin=market/manual`、`latestVersion` | `%USERPROFILE%\.dsh\storages\@montersy123\dsh-skill-market\data\panel.json` 实读 |
| 市场上架 skill 的安装目录为 `<handle>--<slug>` | 本机 `~/.dsh/skills/clawhub-pskoett--self-improving-agent/` 等 |
| ClawHub **安装版**目录含 `_meta.json`（发布是否同写未实测） | 本机 `clawhub-halthelobster--proactive-agent/_meta.json` = `{"ownerId","slug","version","publishedAt"}` |
| 市场「已安装版本」取自 `SKILL.md` frontmatter `version` | 插件 `lib/index.js:1493-1504` `declaredVersionOf`：frontmatter 无 `version` 时为空（v2.2.0 本地导入实测 `version=` 空）；v2.2.1 起 frontmatter 声明 `version`，本地导入实测 `version=2.2.1` |
| SkillHub 的 clawhub 来源与自动同步 | `https://api.skillhub.cn/api/skills`：`source:"clawhub"`、`upstream_url:"https://clawhub.ai/<user>/<slug>"`、`namespace.canonicalName:"@clawhub_<user>/<slug>"`；详情接口 `latestVersion.changelog:"Synced by skillhub pipeline"` |
| 发布命令/登录方式 | `clawhub` npm 包 README（`https://registry.npmmirror.com/clawhub`）：`clawhub login`、`clawhub skill publish <dir> --slug ... --name ... --changelog ...`；Windows 配置在 `%APPDATA%\clawhub\config.json` |

## 3. 发布前准备（本 skill 已内置校验）

1. **版本与变更**：`version.json` bump（semver），`CHANGELOG.md` 写「改了什么/为什么/验证/回滚」。
2. **frontmatter 合法**：`SKILL.md` 的 `name` 为 kebab-case（≤64）、`description` ≤500 字符（建议 ≤200）；`name` 与 `version.json` 一致；**`version` 与 `version.json` 一致**（市场用它显示「已安装版本」，缺失会显示为空；`package-skill.ps1` 已校验：缺失 WARN、不一致 FAIL）。
3. **人读文档**：`README.md`（商店详情/概览）、`QUICKSTART.md`（首次上手）存在且与当前版本一致。
4. **脱敏**：无本机绝对路径、无凭证；脚本只写 `.tmp`/工作区。
5. **打包校验**：

```powershell
$ws = "<你的工作区>"                       # 例如 D:\work\my-dsh-workspace
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\package-skill.ps1" -SkillRoot "$ws\tools\capability-loop\skill\dsh-capability-loop" -OutDir "$ws\dist\skill-store" -Slug "dsh-capability-loop"
```

通过后得到 `manifest.json` + `SHA256SUMS.txt` + `dsh-capability-loop-vX.Y.Z.zip` + `PUBLISH-NOTES.md`。
**注意**：ZIP **只含技能目录**（单一顶层 `dsh-capability-loop/`，可直接被市场「本地导入」；manifest/SHA256/PUBLISH-NOTES 留在包目录留档，不进 ZIP）；**上架 ClawHub 不需要 ZIP**，直接发布目录（§4）。

## 4. 发布到 ClawHub（首次上架 / 后续更新同一条命令）

```powershell
# 0) 环境：Node.js 22.13+ 或 24+（本机 v22.23.4 满足）；Windows 用 npm.cmd
npm.cmd i -g clawhub
clawhub --version

# 1) 登录（设备码 + GitHub 授权；只做一次）
clawhub login
#    无浏览器/CI：clawhub login --token clh_xxx（token 用 clawhub token 打印/复用）

# 2) 发布（**发布打包目录，不要发布源码仓库根**：避免带入 .git/.tmp/截图/本机状态）
#    先跑 package-skill.ps1 得到 <包目录>\dsh-capability-loop-v<版本>\dsh-capability-loop
cd "<你的工作区>"
clawhub skill publish "<包目录>\dsh-capability-loop-v<版本>\dsh-capability-loop" `
  --slug "dsh-capability-loop" `
  --name "dsh-capability-loop" `
  --version "<版本>" `
  --changelog "v<版本>: <摘要>"

# 3) 首次发布后可核对
clawhub search "dsh-capability-loop"
```

- **更新**：改完 → bump `version.json` + 写 `CHANGELOG` → **重复同一条 publish 命令**（新 `--changelog`）。
- **组织发布**：`clawhub skill publish <dir> --owner <org> --changelog "..."`。
- **`_meta.json`**：安装版目录内可见 `{"ownerId","slug","version","publishedAt"}`（本机 4 个 clawhub 安装实例实证）；**发布时是否同写未实测**（本机无发布证据），以发布后实际产物为准——**出现后不要手工改它**，它会被当作来源记录。
- `--name` 是展示名；`SKILL.md` 的 `name` 是技能标识，两者别混。

## 5. 同步到 SkillHub 与 DSH 市场

1. SkillHub 由同步管线从 ClawHub 拉取（证据见 §2），**没有由你手动触发的入口**；同步时延未实测（§6）。
2. 同步后在 `https://skillhub.cn/skills` 搜索 slug，或直接查 API：
   `https://api.skillhub.cn/api/v1/skills/<slug>`（返回含 `source:"clawhub"`、`upstream_url`）。
3. 打开 DSH **Skill Market** 面板 → 搜索 → 安装；安装到 `~/.dsh/skills/<handle>--dsh-capability-loop/`。
4. **重启 DeepSeek Harness**，新会话即可调用。
5. 之后 `skill-status.ps1` 能读到面板里的 `latestVersion`，版本落后时只提示「去市场更新」。

**只想先给同事/自己装（不等人同步）**：市场面板支持「本地导入」ZIP（要求**单一顶层目录**，本脚本生成的 ZIP 已满足；41 条目/多顶层会被判「技能包缺少 SKILL.md」），或直接把目录拷到 `~/.dsh/skills/`——这只是安装，不产生商店记录。

## 6. 未实测项（照做前必读）

| 项 | 状态 | 原因 / 补测方式 |
|---|---|---|
| `clawhub login` 实际授权 | **未实测** | 需要你本人的 GitHub 授权；本机 shell 网络不可用（`npm` ETIMEDOUT、`Invoke-WebRequest` TLS 失败），无法在此完成 |
| `clawhub skill publish` 实际发布 | **未实测** | 同上；命令与参数来自 clawhub 官方 npm README，发布后以 `_meta.json` + `clawhub search` 验证 |
| `clawhub skill publish --dry-run` | **未确认** | README 只在 `package publish` 示例里出现 `--dry-run`；不要假定 skill 发布支持 |
| SkillHub 同步时延/是否全量 | **未实测** | 只证实「source=clawhub 且由 pipeline 同步」；以实际搜索为准 |
| SkillHub 是否有独立「上传/认领」入口 | **未确认** | API 有 `claim_state/claimable`（认领已收录 skill），认领 ≠ 发布；站点为 SPA，本机无法抓取路由 |
| `clawhub skill publish` 的版本号来源（`version.json` / frontmatter / `--version`） | **未确认** | 上游 README 未写；首发后核对 ClawHub/SkillHub 显示版本是否为 2.2.1。现已在 `version.json` + `SKILL.md` frontmatter 双处声明，降低歧义 |
| `SKILL.md` frontmatter 新增 `version` 键的接受度 | **部分实测** | 市场 `declaredVersionOf` 已实测读取（导入 `version=2.2.1`）；DSH 加载器对额外 frontmatter 键容忍：本机 `proactive-agent`（带 `version`/`author`）已被正常加载（间接证据），本 skill 重启后的直接验证未做；ClawHub 侧接受度未实测 |
| 商店排序/精选 | **不保证** | 新 skill 默认按下载/评分排序，短期搜不到不代表没同步 |

## 7. 回滚与撤下

- **版本回滚**：在 DSH 市场详情「版本历史」安装旧版本；ClawHub 侧保留已发布版本记录。
- **撤下/删除**：在 ClawHub 账号后台处理（CLI 未在 README 提供删除命令，**未实测**）；SkillHub 镜像随后同步。
- **本机回滚**：手工安装版可直接覆盖目录；商店安装版请走市场 UI，避免 `panel.json` 记录与实际不一致。

## 8. 一页检查清单

- [ ] `version.json` / `CHANGELOG.md` / `SKILL.md` 三处版本语义一致
- [ ] `name` kebab-case、`description` ≤500、`README.md`/`QUICKSTART.md` 已更新
- [ ] `package-skill.ps1` 通过（无 FAIL；敏感/本机路径 WARN 已人工确认）
- [ ] `capability-audit.ps1 -Strict` 无 FAIL
- [ ] `clawhub login` 完成（token 已存 `%APPDATA%\clawhub\config.json`）
- [ ] `clawhub skill publish ...` 成功，目录出现 `_meta.json`
- [ ] `clawhub search` / SkillHub API 能搜到
- [ ] DSH 市场可安装、重启后可调用；`skill-status.ps1` 显示商店已接管
