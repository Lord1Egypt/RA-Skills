# 快手上传 Skill

快手视频/图文自动上传技能。当用户需要登录快手、校验账号或上传内容时使用。

底层基于 [social-auto-upload](https://github.com/dreammis/social-auto-upload)（SAU）项目，OPclaw 在首次使用时会自动 clone 仓库并准备依赖，**无需用户手动安装**。

## ✨ 功能概览

| 功能 | 子命令 | 说明 |
|---|---|---|
| 登录 | `login --account <name>` | 用户在本机终端扫码完成 |
| 校验 | `check --account <name>` | 检查指定账号 cookie 当前是否有效 |
| 视频上传 | `upload-video ...` | 上传一条快手视频 |
| 图文上传 | `upload-note ...` | 上传一条快手图文 |

元数据约定：

- 视频使用 `title + desc + tags`
- 图文使用 `title + note + tags`

## 🚀 使用流程

直接对 OpenClaw 说出需求，例如：
- "用快手账号 `myacc` 登录"
- "把这组图片以图文形式发到快手"

OpenClaw 会自动选择并执行对应的 SAU 命令。

## 📖 完整文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 故障排查：`references/troubleshooting.md`
- 完整说明：[SKILL.md](SKILL.md)

---

## 🔒 安全审计报告

> 本技能已通过 `skill-vetter` 安全审计工具的完整审查，可放心安装使用。

| 字段 | 内容 |
|---|---|
| **审计日期** | 2026-05-12 |
| **审计工具** | skill-vetter (clawhub@latest) |
| **来源** | ClawdHub / social-auto-upload 包装 |
| **审查文件数** | 6 |
| **可疑模式** | ✖ 无 |
| **网络访问** | 通过外部 `social-auto-upload` CLI 工具调用快手官方接口 |
| **凭据处理** | 不内嵌任何凭据；登录由用户在本机终端完成 |
| **文件访问** | 仅读取用户指定的视频/图片文件用于上传 |
| **依赖命令** | `sau_cli.py kuaishou`（social-auto-upload） |
| **风险等级** | 🟢 LOW |
| **审计结论** | ✅ **SAFE — 低风险，安全可用** |

**审计要点：** 本技能仅包含示例模板脚本；所有快手 API 调用均由外部 `social-auto-upload` 项目处理，未发现内嵌凭据或可疑网络行为。

> 完整的多技能审计报告见仓库根目录 `SKILL_VETTING_REPORT.md`。
