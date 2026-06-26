---
name: filemanager-transfer
description: "本技能适用于发送文件/远程发送文件/分享文件给用户，以及用户提供的FileManager下载连接需要下载文件，是否是FileManager下载连接可获取scripts/.env中获取FILEMANAGER_BASE_URL确定"
---

# FileManager Transfer

当用户与 agent 远程环境之间传递文件时，使用这个技能。`scripts/` 里的 FileManager 程序负责提供文件中转服务，Python 脚本只是调用 API 的便捷封装。

## 首次使用

1. 访问https://github.com/mrknow001/FileManager/releases下载可执行程序
2. 启动scripts目录下服务端程序
3. 访问web页面设置密码或者使用./filemanager-linux-amd64 -reset-password your_password初始化密码
4. 访问后台创建appkey

5. 配置`scripts/.env`

## 使用流程

1. 先判断传输方向：
   - agent 发给用户：上传文件，创建带密码的分享链接，把链接和密码给用户。
   - 用户发给 agent：让用户通过 FileManager 上传，或提供 FileManager 文件 ID，然后下载。
3. 脚本用法只参考 `references/transfer-script.md`。
4. 脚本失败时，不要盲猜。先阅读错误，参考 `references/troubleshooting.md` 修复配置或服务状态，然后重试一次。
5. 如果 FileManager 可访问但脚本仍失败，可按 references 中`api.md`记录的 API 行为兜底，并向用户说明已尝试的操作。

## 参考文档

- `references/install-and-start.md`：安装、配置和启动 FileManager 服务。
- `references/transfer-script.md`：`scripts/filemanager_transfer.py` 的上传、分享、下载命令。
- `references/troubleshooting.md`：常见失败原因和恢复步骤。

## 规则

- 不要硬编码或泄露 `FILEMANAGER_APPKEY`。
- 除非用户明确只需要上传保存，否则创建分享链接时必须设置非空密码(默认4位数字字母组合)。
- 临时传输优先使用短有效期分享。
- 输出应聚焦于链接、密码、文件 ID 或本地保存路径。
