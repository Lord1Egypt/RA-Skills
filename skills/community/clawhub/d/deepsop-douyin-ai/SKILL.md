---
name: deepsop-douyin
description: 抖音视频自动上传 skill。当用户需要登录抖音、校验账号或上传视频时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。
---

# 抖音上传 Skill

本 skill 通过 [social-auto-upload](https://github.com/dreammis/social-auto-upload) 项目（以下简称 SAU）完成抖音操作。OPclaw 自带 `uv` 工具，会在首次使用时自动 clone SAU 并准备依赖，**不要让用户手动 pip install**。

## 功能概览

| 功能 | 子命令 | 说明 |
| --- | --- | --- |
| 登录 | `login --account <name>` | 用户在本机真实终端里执行，扫码完成 |
| 校验 | `check --account <name>` | 检查指定账号当前是否有效 |
| 视频上传 | `upload-video ...` | 上传一条抖音视频 |

## 默认工作流

1. **先确认环境就绪** —— 见 `references/runtime-requirements.md`
2. **再确认命令格式** —— 见 `references/cli-contract.md`
3. 执行匹配的 `python sau_cli.py douyin ...` 命令
4. 失败时查 `references/troubleshooting.md`

## 执行前必做检查（agent 行为约定）

执行任何 `python sau_cli.py douyin ...` 之前，**必须**按 `references/runtime-requirements.md` 的"自动准备流程"完成环境校验：

1. 检查 `~/.openclaw/social-auto-upload` 是否存在
2. 不存在则自动 clone + `uv sync`
3. 准备好后，**所有调用都用 `uv run --project ~/.openclaw/social-auto-upload python sau_cli.py douyin ...`**
4. **不要**直接 `sau douyin ...`（这条命令不存在）
5. **网络失败时**：`git clone` 直连超时/失败，agent 必须**自动**用 `gh-proxy.org` / `gh-proxy.com` / `hub.gitmirror.com` 三个镜像依次重试，**严禁**第一次失败就告诉用户'无法访问 GitHub'。详见 `references/runtime-requirements.md` Step 2

## 登录注意事项

- `login` 命令应由**用户自己**在本机终端执行，agent 在非交互环境下不要硬跑
- 如果终端二维码显示不完整，提醒用户打开仓库目录下的 `qrcode.png` 扫码
- 一个 `--account <name>` 对应一个本地账号文件，可用于多账号隔离

## 模板文件

- `scripts/examples/douyin_commands.ps1`
- `scripts/examples/douyin_commands.sh`
- `scripts/examples/douyin_cli_template.py`

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 故障排查：`references/troubleshooting.md`