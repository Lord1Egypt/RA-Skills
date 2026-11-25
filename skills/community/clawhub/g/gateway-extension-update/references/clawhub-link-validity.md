# ClawHub 链接有效性与面板徽章（「不可用」的诊断与修复）

被 `openclaw-extension-update` 分支 C 引用。用于：Control UI 技能面板（`/settings/skills`）上某技能显示「不可用」/「待审核」/「ClawHub 链接无效」，而同一技能在 `openclaw skills list --json` 里字段全 true；或要给缺 `ownerHandle` 的旧格式 ClawHub 安装补 owner 归属。

## 一、先分清面板上的两种「状态」

| 位置 | 取值 | 含义 |
|---|---|---|
| 状态页签 | 就绪 / 需要设置 / 已禁用 | **可用性**：`disabled` → 已禁用；未禁用且无缺失依赖 → 就绪；未禁用但 `missing` 非空 → 需要设置 |
| **裁决徽章**（本文件主题） | **不可用** / 未发现风险 / 待处理 / 待审核 / 已阻止 | **ClawHub 安全裁决**，与「能不能用」无关 |

⇒ 「不可用」= `verdict.unavailable`，语义是**裁决拉不到**，不是技能坏了。同一页面另有独立徽章：`invalidLink`（ClawHub 链接无效）、`notScannedByClawHub`（未经 ClawHub 扫描）、`missingRequirements`（缺少必要条件）。

裁决徽章取值规则（实测读 UI 包确认）：

- 该技能**查不到裁决记录** → 「不可用」
- 有记录且 `ok && decision === "pass"` → 「未发现风险」
- `securityStatus` 为 `pending` / `not-run` → 「待处理」
- 否则按 `securityStatus` 落：`malicious` → 「已阻止」，`suspicious` → 「待审核」，其余 → 「不可用」

**判决性字段**：`openclaw skills info <技能名> --json` 里的 `clawhub.valid` / `clawhub.ownerHandle`。两者齐全 ⇒ 裁决键拼得全，徽章会正常解析。

## 二、裁决键拼不全的常见根因：缺 `ownerHandle`

裁决按 **`registry + slug + ownerHandle + version`** 取，键值来自该技能的 `clawhub` 块，源头是技能目录里的 `.clawhub/origin.json`。

CLI 早期版本写入的**旧格式**（`origin.json` 与 lockfile 条目）**都没有 `ownerHandle`**：

```json
{ "version": 1, "registry": "https://clawhub.ai", "slug": "agent-memory-framework",
  "installedVersion": "1.0.0", "installedAt": 1785750102186,
  "artifact": { "kind": "archive", "sha256": "…" }, "skillFile": { "path": "SKILL.md", "sha256": "…" } }
```

**只要该 slug 在 ClawHub 上被多家共用**，缺 owner 就无法消歧 ⇒ 查不到裁决 ⇒ 徽章「不可用」：

```
clawhub inspect <slug>        → Found multiple skills with the slug "…"; specify which one you want
curl .../api/v1/skills/<slug> → {"code":"AMBIGUOUS_SKILL_SLUG", …}
openclaw skills verify <slug> → Skill "<slug>" not found on ClawHub
```

slug 独家时通常仍能解析 —— 所以这类缺陷**只在重名 slug 上显形**（实测本机 48 个 ClawHub 来源技能里只有 3 个缺 `ownerHandle`，且这 3 个的 slug 都重名）。

**盘点命令**（列出全部缺 owner 的 ClawHub 来源技能）：

```bash
python3 - <<'PY'
import json, glob, os
roots = ("<workspace>/skills", "<workspace>/.agents/skills", os.path.expanduser("~/.agents/skills"))
for r in roots:
    for p in glob.glob(os.path.join(r, "*", ".clawhub", "origin.json")):
        d = json.load(open(p))
        if not d.get("ownerHandle"):
            print(os.path.basename(os.path.dirname(os.path.dirname(p))), "| slug =", d.get("slug"))
PY
```

## 三、网关的校验规则（决定「改了能不能变 valid」）

网关 `resolveClawHubSkillStatusLinkSync` 的判定顺序（实测读 `dist/worker/worker.mjs`）：

1. 本地无 `origin.json`、而 lockfile 有对应条目 → `invalidLink`（“tracked by the lockfile but is missing local ClawHub origin metadata”）
2. `origin.json` 格式损坏，或其 `slug` 非法 → `invalidLink`（“Malformed ClawHub origin metadata …” / “Invalid ClawHub origin slug …”）
3. lockfile 本身损坏，或**按 slug 取不到条目** → `invalidLink`（“Malformed … lockfile …” / “… is not tracked by the … lockfile”）
4. **目录必须是 `<skillsDir>/<slug>`（扁平）** —— 期望值 = `resolveWorkspaceSkillInstallDir(workspaceDir, slug)`，与该技能实际目录的 realpath 不等 → `invalidLink("… not in the expected ClawHub install directory")`
5. 逐字段同一性，任一不等即 `invalidLink("… does not match the … lockfile")`：
   - `lock.version == origin.installedVersion`
   - `lock.installedAt == origin.installedAt`
   - 归一后的 registry 相等
   - 且以下各项与 lockfile 对应项**逐项相等**：`ownerHandle`、`requestedReference`、`trustState`、`sourceUrl`、`artifact{kind,sha256,integrity}`、`skillFile{path,sha256}`、`fileTreeSha256`
6. 全过 → `{ status: "linked", valid: true, ownerHandle: … }`

两条推论（都实测踩过）：

- **`clawhub install @owner/slug` 修不了这个**：它**不覆盖**同名扁平目录，而是新建 `skills/@owner/<name>/` 并追加 lockfile 键 `@owner/<name>`。该位置**永远过不了第 4 条**（实测：只留 scoped 副本时 `skills info` 报 `invalid` + 目录原因）。同族：`lz-skill-vetter-plus` 报 `invalid` + lockfile 原因 —— 它的锁键是 scoped 形式，而查找按 slug。
- **新旧格式不能混用**：origin 用新格式（只有 `fingerprint`、无 `artifact`/`skillFile`）时，lockfile 条目必须**同构**（同样去掉 `artifact` / `skillFile` / `fileTreeSha256`），否则第 4 条判假；反之亦然。

## 四、修复步骤

1. **备份**：整个技能目录 + `<workspace>/.clawhub/lock.json` 到 `/tmp`（记路径）。
2. **核对在装载荷属于哪个 owner**：
   `diff -r --exclude=.clawhub --exclude=_meta.json --exclude=skill-card.md <现有目录> <目标 owner 的下载目录>`
   **只有载荷逐字相同（或差异仅为自动生成的 `skill-card.md` / `_meta.json`）才可直接改归属**；载荷不同则先决定以哪份为准 —— **改归属 ≠ 换内容**，两 owner 内容不一致时停下来问主人。
3. **把 CLI 新格式的 `origin.json`（含 `ownerHandle`）落到扁平期望目录**；同批替换 `_meta.json` 与 `skill-card.md` 为目标 owner 那份，保持记录自洽。
4. **把 lockfile 条目改成与 origin 同构**：加 `ownerHandle`、对齐 `installedAt`，去掉旧 `artifact` / `skillFile` / `verification`。
   - 用**大括号配对的定点替换**，不要整体 `json.dump` 重写整份 lockfile；写完 `json.loads` 校验，并断言**其余条目逐字段未变**（取两边除目标键外的字典做相等比较）。
   - 旧 `verification` 块里挂着**别的 owner** 的扫描结论与卡片 URL ⇒ 一并移除，否则会把别人的裁决记在自己名下（移后下次 verify 会重取）。
   - 写盘用 `os.replace` 原子替换；键数前后各报一次。
5. **移出重复副本**：把 `skills/@owner/<name>/` 移入隔离目录（**不要 `rm`**），并删掉它那条 scoped 锁键。
6. **验证（两条都要）**：
   ```bash
   openclaw skills info <技能名> --json   # 期望 status: linked / valid: true / ownerHandle 有值，且 filePath 落在扁平目录
   openclaw skills verify <slug>          # 期望不再 "not found on ClawHub"；输出 pageUrl=https://clawhub.ai/<owner>/skills/<slug>、publisherHandle=<owner>
   openclaw skills check --json           # 期望总量不变、该技能唯一且未被白名单挡
   ```
7. **报告真值**：修复只让裁决**可解析**，不改裁决内容。实测修好后徽章是**「待审核」**（该技能扫描结论 `suspicious` / `security.status_not_clean`），**不是**「未发现风险」—— 那是真实扫描结论，不是本次没修好。把它讲成「未发现风险」是虚报。

## 五、边界与陷阱

- 只做**元数据**操作：不动 `SKILL.md` / `references/` / `assets/`；不代主人决定「该用哪个 owner 的发布」。
- 「可用性」与「裁决」是两个面：`skills list --json` 字段全 true 只证明**可用**，不证明徽章会显示「未发现风险」。主人问「为什么不可用」时先把这两层分开答，再往下查。
- 没有 `gio trash` 时也不要退回 `rm`：移入隔离目录并留下路径。
- 改完徽章可能需刷新面板；若仍显示旧值，再考虑是否需要重启网关（本 agent 不用 exec 重启）。
