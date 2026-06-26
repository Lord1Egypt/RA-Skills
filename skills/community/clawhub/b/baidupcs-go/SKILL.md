# BaiduPCS-Go Skill

百度网盘命令行客户端工具技能。提供文件上传、下载、转存、分享等操作的命令行封装。

## 技能描述

BaiduPCS-Go 是一个仿 Linux shell 风格的百度网盘命令行客户端，支持多平台（Windows、Linux、macOS），提供丰富的网盘操作命令。

## 核心功能

- **账号管理**: 登录、切换、退出百度账号
- **文件操作**: 上传、下载、删除、移动、重命名、拷贝
- **分享功能**: 创建分享、转存他人分享、取消分享
- **离线下载**: 支持 HTTP/HTTPS/FTP/磁力链等协议
- **回收站**: 查看、还原、删除回收站文件
- **配置管理**: 查看和修改程序配置项

## 使用场景

当用户需要：
1. 通过命令行操作百度网盘文件
2. 批量上传或下载网盘文件
3. 转存他人分享的网盘链接
4. 管理网盘分享链接
5. 使用离线下载功能
6. 查看网盘配额和文件信息

## 前置要求

1. 已安装 BaiduPCS-Go 程序
2. 已登录百度账号
3. 了解基础命令行操作

## 命令说明

详细命令列表和使用方法参见 [BaiduPCS-Go.md](./BaiduPCS-Go.md)

## 注意事项

- 普通用户请将 `max_parallel` 和 `max_download_load` 设置为 1，避免触发限速
- SVIP 用户建议 `max_parallel` 设置为 10-20，`max_download_load` 设置为 1-2
- 下载文件默认保存到程序所在目录的 `download/` 目录
- 上传文件默认采用分片上传，支持秒传
- 谨慎修改 `appid`、`user_agent` 等配置项

## 配置文件路径

- Windows: `%APPDATA%\BaiduPCS-Go`
- Linux/macOS: `$HOME/.config/BaiduPCS-Go`
- 可通过环境变量 `BAIDUPCS_GO_CONFIG_DIR` 指定
