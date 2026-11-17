# 安全审查（安装前闸门）

安装一个技能 = 安装可执行代码。任何**社区（非原生）技能**在安装前必须过此闸门。
原生市场技能经宿主审核，默认可信，可跳过深度审查。

## 四级风险分类（对标 skill-vetter，31 万下载的同类头部）

| 等级 | 判定 | 动作 |
|---|---|---|
| ⛔ **EXTREME** | 执行块里出现 P0 真实高危 | **禁止安装** |
| 🔴 **HIGH** | 文档提及 P0（多为示范）或执行块里出现 P1 | 需人工批准 |
| 🟡 **MEDIUM** | 仅文档提及 P1 | 完整审查后安装 |
| 🟢 **LOW** | 无命中 | 可安装 |

> 关键：区分「执行块里的真实高危」与「文档正文里的提及」——后者多为误报。
> 扫描器输出同时给出 `risk_level`（P0/P1/P2 静态定级，决定退出码 2/1/0）与
> `risk_class`（四级，决定动作）。

## 运行扫描器（真执行，优先于手动 grep）

```bash
python3 scripts/security_scan.py --path <解压后的技能目录> --lang zh-CN
python3 scripts/security_scan.py --path <目录> --json     # 机器可读
```

退出码 `2/1/0` = `P0/P1/P2`；**P0（EXTREME）直接阻断安装**，P1 须用户明确确认。

## 红旗清单（17 项）

| 类别 | 信号 | 定级 |
|---|---|---|
| 混淆执行 | `eval()` / `exec()` / `base64 -d` / `powershell -enc` | P0 |
| 混淆代码 | 大段 `\xNN` / `\uNNNN` 转义、`String.fromCharCode`、压缩代码 | P0 |
| 远程执行 | `curl\|sh`、`wget\|sh`、`iwr\|iex` 下载后管道到 shell | P0 |
| 破坏系统 | `rm -rf` 指向 `/`、`~`、`..`、`/etc`、`/usr`、`/System` | P0 |
| 系统写入 | 写入 `/etc/`、`/usr/`、`/System/`、`C:\Windows` | P0 |
| 提权 | `sudo`、`mkfs` | P0 |
| **凭据目录** | 读取 `~/.ssh`、`~/.aws`、`id_rsa`、`.npmrc`、`.netrc`、`.docker/config`、`.gnupg` | P0 |
| **Agent 身份/记忆** | 访问 `MEMORY.md`、`USER.md`、`SOUL.md`、`IDENTITY.md`、`CLAUDE.md`、`AGENTS.md` | P0 |
| **浏览器凭据** | `cookies.sqlite`、`--user-data-dir`、`Login Data`、`document.cookie` | P0 |
| 外呼 | 向非白名单域名发起请求 | P1 |
| **裸 IP 直连** | `http://45.77.x.x` 形式（绕过域名信誉） | P1 |
| 凭据索取 | 要求填 token / password / api_key / 授权码 | P1 |
| 提示注入 | "忽略此前指令" / ignore previous instructions | P1 |
| **静默装包** | `pip install` / `npm install` / `apt-get install` 未声明 | P1 |
| **权限放宽** | `chmod 777` / `a+rwx` | P1 |
| 依赖网络 | 安装即外呼不可信源 | P1 |
| 仅本地工具 | 纯提示词/模板、无脚本外联 | P2 |

**加粗项**为对标 `skill-vetter` 补齐的 8 项缺口。

## 权限清单（人工审阅三问）

扫描器自动提取并输出，回答三个问题：

1. **需要读哪些文件？** → `permissions.files`
2. **需要访问哪些网络？** → `permissions.network`
3. **需要执行哪些命令？** → `permissions.commands`

判断标准：**范围是否为其声明目的所必需的最小集**。超出的即为红旗。

## 信任层级（Trust Hierarchy）

| 层级 | 来源 | 审查强度 |
|---|---|---|
| 1 | 宿主官方 / 原生市场 | 低（仍需过目） |
| 2 | 知名源（vercel-labs / anthropics / microsoft）+ 高下载 | 中 |
| 3 | 已知作者 | 中 |
| 4 | 新 / 未知来源 | 最高 |
| 5 | 任何索取凭据的技能 | **一律人工批准** |

## 无脚本环境时的降级手动扫描（兜底）

```bash
TMPDIR=$(mktemp -d)
curl -L -o "$TMPDIR/skill.zip" "https://lightmake.site/api/v1/download?slug=<slug>"
unzip -l "$TMPDIR/skill.zip" | awk '{print $4}' > "$TMPDIR/filelist.txt"
grep -RniE "eval\(|base64 -d|powershell -enc|curl .*\| *sh" "$TMPDIR/filelist.txt" && echo "⚠️ P0"
unzip -o "$TMPDIR/skill.zip" -d "$TMPDIR/extracted" >/dev/null 2>&1
grep -RniE "~/.ssh|~/.aws|MEMORY\.md|IDENTITY\.md|cookies\.sqlite" "$TMPDIR/extracted" && echo "⚠️ P0 凭据/身份文件"
grep -RniE "token|secret|password|api[_-]?key|授权码" "$TMPDIR/extracted" && echo "⚠️ P1 凭据索取"
```

## 人工审阅清单

- [ ] Frontmatter 合法（name / description 齐备）
- [ ] 许可证已声明且可验证
- [ ] 作者已知（非匿名）
- [ ] 无 P0 高危信号
- [ ] 无 P1 需确认信号
- [ ] 已人工审阅指令正文
- [ ] 已审阅网络行为
- [ ] 已审阅请求权限（文件/网络/命令）
