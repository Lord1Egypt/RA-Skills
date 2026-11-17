# 版本与更新

技能可以检查是否有新版本，但不得自行下载或替换文件。更新必须由作者明确同意。

## 当前版本

以技能目录下的 `VERSION.md` 为准。读取它，不要凭记忆报版本号。

## 什么时候检查

在下面这些时机检查，且每天最多一次：

- 本次会话第一次使用黑石相关能力时；
- 云端调用出现可能由版本不兼容造成的错误时，这时可以无视每日限制重新检查。

检查记录写在 `~/.blackstone/skill-state.json`：

```json
{"installed_version":"1.3.2","available_version":"1.3.3","last_checked":"2026-08-09T10:00:00Z","last_updated":"2026-08-08T10:00:00Z"}
```

文件不存在时可以新建。距离 `last_checked` 不足24小时且没有版本错误时跳过检查。

## 只检查，不自动更新

请求：

```text
GET https://blackstone.wansu.tech/api/public/skills/longform-fiction/manifest
```

返回 `version`、`tarball_url`、`download_url`、`install_dir`、`file_count` 和文件哈希清单。

- 远端版本不高于本地版本：继续当前任务，不额外打扰作者。
- 远端版本高于本地版本：只提示一次，不下载任何文件：

  > 黑石写作技能有新版本 x.y.z。要现在更新吗？更新只会替换黑石技能自己的目录，不会改正文、其他技能或客户端配置。

- 作者同意：按“作者同意后的更新”执行。
- 作者拒绝、跳过或没有回应：继续当前任务，本次会话不再提示。
- 检查失败：记录 `last_checked`，使用当前版本继续；只有当前问题确实可能由旧版本引起时才说明检查失败。

## 作者同意后的更新

只有作者在当前对话里明确表示同意更新，才执行下面步骤：

1. 再次确认目标是黑石技能目录，不动正文、其他技能和客户端配置。
2. 把 `tarball_url` 指向的 `.tar.gz` 下载到临时目录。
3. 解压到另一个临时目录，不直接覆盖正在使用的技能目录。
4. 按清单逐项核对 `sha256`，并检查文件数、Skill 名称和版本号；任一项不符就放弃更新。
5. 校验通过后替换黑石技能目录，删除新清单里不存在的旧版技能文件。
6. 更新 `skill-state.json` 的 `installed_version`、`last_checked` 和 `last_updated`。
7. 报告已安装版本、校验结果，以及新版本是否需要新开会话才能生效。

优先使用 tar.gz：

```bash
tar -xzf <包> -C <临时目录>
```

这条不可用时，按 `https://blackstone.wansu.tech/install/blackstone.md` 的安装协议选择当前系统支持的 zip 解压方式。不要预设有 `python3`，不要在 Linux 上用 `tar -xf` 解 zip。

更新失败时不要反复重试，也不要留下半新半旧的技能目录。保留原版本并说明更新未完成；当前写作任务继续使用原版本。

## 上报版本

发起设备授权时，在 `client` 里带上 `skill_version`，见 [account.md](account.md)。这让服务端知道哪些版本还在使用，从而判断旧接口能否下线。
