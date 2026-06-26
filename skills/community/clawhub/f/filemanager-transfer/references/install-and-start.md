# 安装与启动

这个技能把 FileManager 三端可执行程序放在 `scripts/` 目录下：

- Windows amd64：`scripts/filemanager-windows-amd64.exe`
- Linux amd64：`scripts/filemanager-linux-amd64`
- macOS Apple Silicon：`scripts/filemanager-darwin-arm64`

## 配置

为传输脚本创建 `scripts/.env`：

```env
FILEMANAGER_BASE_URL=http://localhost:8080
FILEMANAGER_APPKEY=fm_app_xxxxxxxxxxxxxxxxx
```

如果 agent 运行环境已经提供密钥，也可以直接使用环境变量。不要在聊天、日志或最终回复中打印 AppKey。

## 启动服务

在技能目录下，根据当前系统选择对应的可执行程序。

-port安装scripts/.env中FILEMANAGER_BASE_URL链接的端口启动

Windows PowerShell：

```powershell
.\scripts\filemanager-windows-amd64.exe -host 0.0.0.0 -port [prot] -data-dir .\data
```

Linux：

```bash
chmod +x scripts/filemanager-linux-amd64
./scripts/filemanager-linux-amd64 -host 0.0.0.0 -port [prot] -data-dir ./data
```

macOS Apple Silicon：

```bash
chmod +x scripts/filemanager-darwin-arm64
./scripts/filemanager-darwin-arm64 -host 0.0.0.0 -port [prot] -data-dir ./data
```

常用参数：

- `-host`：监听地址。默认 `0.0.0.0`。
- `-port`：服务端口，无默认 ，必须按照FILEMANAGER_BASE_URL链接的端口。
- `-data-dir`：数据库和存储根目录，默认 `./data`。
- `-storage`：文件存储目录，默认 `data/storage`。
- `-db`：SQLite 数据库路径，默认 `data/filemanager.db`。
- `-max-upload-size`：最大上传请求大小，单位字节，默认 `10737418240`。
- `-reset-password`：重置管理员密码后退出。

## 首次运行检查

1. 启动服务并保持运行。
2. 打开 `FILEMANAGER_BASE_URL` 对应的 Web 页面。
3. 创建或获取用于 API 访问的 AppKey。
4. 把服务地址和 AppKey 写入 `scripts/.env` 或环境变量。
5. 正式传输重要文件前，先用小文件测试一次上传和下载。

## 远程 Agent 注意事项

当用户和 agent 不在同一台机器时，`FILEMANAGER_BASE_URL` 必须能被运行脚本的一侧访问。如果服务通过隧道、反向代理、VPN 或公网地址暴露，应使用那个可访问地址，而不是 `localhost`。
