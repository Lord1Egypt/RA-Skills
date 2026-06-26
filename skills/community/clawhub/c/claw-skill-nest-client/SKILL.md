---
name: claw-skill-nest-client
description: 本地/私有 Claw Skill Nest（也可称“虾滑” / “Xiahua”）客户端，支持列出、上传、安装、更新技能；当用户提到上传到虾滑、上传到 Xiahua、从虾滑安装技能、从 Xiahua 安装技能、从本地 claw-skill-nest 安装/更新技能时使用；不用于 clawhub.com。
---

# Local Claw Skill Nest Client

本技能是 **本地/私有 Claw Skill Nest 的客户端**，也可以理解为本地技能仓库客户端；在当前语境里，**“虾滑”** 和 **“Xiahua”** 都指这个本地 Claw Skill Nest。

用于管理 skills：

- 列出（list）
- 上传（upload）
- 安装（install）
- 更新（update）

> 边界说明（重要）：
> - 仅面向 **local/private Claw Skill Nest**。
> - **“虾滑” / “Xiahua”** 在本技能中视为本地 Claw Skill Nest 的别称。
> - **不用于** ClawHub 公共仓库（clawhub.com）。

## 环境变量

- `SKILLHUB_URL` - 本地 Claw Skill Nest 服务地址（例如 `http://localhost:17890`）
- `SKILLHUB_API_KEY` - 本地 Claw Skill Nest API Key

## 典型触发语（本地语义）

- `列出本地 skill` / `list local skills`
- `上传本地 skill <file>` / `upload local skill <file>`
- `安装本地 skill <name>` / `install local skill <name>`
- `更新本地 skill <name>` / `update local skill <name>`
- `从本地 claw-skill-nest 安装 <name>`
- `从本地 claw-skill-nest 更新 <name>`
- `把这个 skill 上传到本地 claw-skill-nest`
- `上传到虾滑`
- `把这个技能传到虾滑`
- `从虾滑安装 <name>`
- `从虾滑更新 <name>`
- `虾滑里有什么 skill`
- `upload to Xiahua`
- `install <name> from Xiahua`
- `update <name> from Xiahua`
- `what skills are in Xiahua`

## 非适用场景

- `clawhub.com` 上的搜索、安装、发布（请使用 ClawHub 相关能力）
- 远程公共仓库同步

## 脚本入口（跨平台 TypeScript）

- 通用脚本：`scripts/manage_local_claw_skill_nest.ts`
- 运行方式（任意平台）：
  - `npx tsx scripts/manage_local_claw_skill_nest.ts 列出`
  - `npx tsx scripts/manage_local_claw_skill_nest.ts 安装 <name>`
  - `npx tsx scripts/manage_local_claw_skill_nest.ts 更新 <name>`
  - `npx tsx scripts/manage_local_claw_skill_nest.ts 上传 <本地文件路径> [skill名称] [描述]`

## 安装位置

Skills 将安装到 `~/.openclaw/workspace/skills/<name>`
