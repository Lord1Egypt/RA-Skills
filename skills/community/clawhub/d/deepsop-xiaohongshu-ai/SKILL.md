---
name: deepsop-xiaohongshu
description: 小红书视频/图文自动上传 skill。当用户需要登录小红书、校验账号或上传内容时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。
---

# 小红书上传 Skill

本 skill 通过 [social-auto-upload](https://github.com/dreammis/social-auto-upload) 项目（以下简称 SAU）完成小红书操作。OPclaw 自带 `uv` 工具，会在首次使用时自动 clone SAU 并准备依赖，**不要让用户手动 pip install**。

## 功能概览

| 功能 | 子命令 | 说明 |
| --- | --- | --- |
| 登录 | `login --account <name>` | 用户在本机真实终端里执行，扫码完成 |
| 校验 | `check --account <name>` | 检查指定账号 cookie 当前是否有效 |
| 视频上传 | `upload-video ...` | 上传一条小红书视频 |
| 图文上传 | `upload-note ...` | 上传一条小红书图文 |

元数据约定：

- 视频使用 `title + desc + tags`
- 图文使用 `title + note + tags`

## 默认工作流

1. **先确认环境就绪** —— 见 `references/runtime-requirements.md`
2. **再确认命令格式** —— 见 `references/cli-contract.md`
3. 执行匹配的 `python sau_cli.py xiaohongshu ...` 命令
4. 失败时查 `references/troubleshooting.md`

## 命令选择建议

- 用户需要新的 cookie 或现有 cookie 失效 → 用 `login`
- 用户只想确认 cookie 状态 → 用 `check`
- 用户要发视频 → 用 `upload-video`
- 用户要发图文 → 用 `upload-note`

## 执行前必做检查（agent 行为约定）

执行任何 `python sau_cli.py xiaohongshu ...` 之前，**必须**按 `references/runtime-requirements.md` 的"自动准备流程"完成环境校验：

1. 检查 `~/.openclaw/social-auto-upload` 是否存在
2. 不存在则自动 clone + `uv sync --python 3.12`
3. 准备好后，**所有调用都用 `uv run --project ~/.openclaw/social-auto-upload python sau_cli.py xiaohongshu ...`**
4. **不要**直接 `sau xiaohongshu ...`（这条命令不存在）
5. **网络失败时**：`git clone` 直连超时/失败，agent 必须**自动**用 `gh-proxy.org` / `gh-proxy.com` / `hub.gitmirror.com` 三个镜像依次重试，**严禁**第一次失败就告诉用户'无法访问 GitHub'。详见 `references/runtime-requirements.md` Step 2
6. 当用户明确指定无头或有头模式时，显式传 `--headless` 或 `--headed`
7. 只有用户明确要求定时发布时，才使用 `--schedule`

## 登录注意事项

- `login` 命令应由**用户自己**在本机终端执行，agent 在非交互环境下不要硬跑
- 如果终端二维码显示不完整，提醒用户打开 SAU 仓库目录下的 `qrcode.png` 扫码
- 一个 `--account <name>` 对应一个本地账号文件，可用于多账号隔离
- 如果登录流程生成了本地二维码图片，不要只把图片路径告诉用户，优先直接把本地图片展示/发送给用户

## 模板文件

- `scripts/examples/xiaohongshu_commands.ps1`
- `scripts/examples/xiaohongshu_commands.sh`
- `scripts/examples/xiaohongshu_cli_template.py`

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 故障排查：`references/troubleshooting.md`
