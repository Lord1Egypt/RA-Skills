# Windows 启动器与便携打包

## 1. 铁律：编码与行尾

| 文件类型 | 必须 |
|---|---|
| `.bat` / `.cmd` | **纯 ASCII + CRLF**（内容里不要有中文，中文只放文件名） |
| `.ps1` / `.txt`（含中文） | **UTF-8 带 BOM + CRLF** |
| `.html` / `.js` / `.mjs` | UTF-8 无 BOM |

写入后必须校验：

```powershell
$b = [IO.File]::ReadAllBytes($p)
$nonAscii = @($b | Where-Object { $_ -gt 127 }).Count     # 必须为 0（bat）
# CRLF 计数 > 0，孤立 LF 计数必须为 0
```

一键规范化：`scripts/normalize-encoding.ps1 <目录>`

## 2. Node 发现（四段式）

双击启动时**用户的 PATH 里通常没有 node**（WorkBuddy 的托管 Node 只注入它自己的进程），而且 `dir` **不支持路径中间的通配符**。

```bat
set "NODEEXE="
set "NV=%USERPROFILE%\.workbuddy\binaries\node\versions"

rem 1) 枚举版本目录，取最新
for /f "delims=" %%d in ('dir /b /ad /o-n "%NV%" 2^>nul') do (
  if not defined NODEEXE if exist "%NV%\%%d\node.exe" set "NODEEXE=%NV%\%%d\node.exe"
)
rem 2) PATH
if not defined NODEEXE for /f "delims=" %%p in ('where node 2^>nul') do (
  if not defined NODEEXE set "NODEEXE=%%p"
)
rem 3) 显式绝对路径兜底
rem 4) %ProgramFiles%\nodejs / %LOCALAPPDATA%\Programs\nodejs
```

❌ 错误写法：`dir /b /s "...\versions\*\node.exe"` —— 中间通配符静默返回空，再被 `2>nul` 吞掉，表现为"Node 明明装了却报找不到"。

## 3. 分离式后台启动（关窗不停服务）

前台 `"%NODEEXE%" src\launch.mjs` 会被"关掉黑窗口"杀掉，导致浏览器标签页 `ERR_CONNECTION_REFUSED`。

```bat
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Process -FilePath '%NODEEXE%' -ArgumentList 'src\launch.mjs' -WorkingDirectory '%APPDIR%' -WindowStyle Hidden"
```

- `-ArgumentList` 用**相对路径** + `-WorkingDirectory`，规避路径含空格时的引号地狱
- 等待用 `ping -n 4 127.0.0.1 >nul`，**不要用 `timeout`**（stdin 被重定向时报 "Input redirection is not supported" 且退出码变 1）
- 就绪探测用裸 TCP，避免代理干扰：
  ```powershell
  $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',8777); $c.Close()
  ```

## 4. 工作目录

`cd /d "%~dp0"` 只有在 .bat 与 `src\` 同目录时才对。**文件被复制到桌面后就指向桌面了** → 找不到 `src\launch.mjs`。

便携包用固定结构 + 显式拼接：

```bat
set "HERE=%~dp0"
if "%HERE:~-1%"=="\" set "HERE=%HERE:~0,-1%"
set "APPDIR=%HERE%\app"
```

## 5. 便携包结构

```
FTA Studio\
  runtime\node.exe          内置 Node（约 89 MB）
  app\src                   后端
  app\public                前端
  app\examples              示例
  启动 FTA Studio.bat
  停止 FTA Studio.bat
  安装到本机.bat / install.ps1
  卸载.bat / uninstall.ps1
  使用说明.txt
```

生成：`scripts/build-portable.ps1 -SourceDir <项目> -OutDir <输出>`

- 模板在 `assets/launchers/`，直接复制后按需替换
- 打包后**必须解压到另一个路径实测一次**，证明不依赖原路径

## 6. 安装 / 卸载

安装（**不需要管理员权限**）：

```powershell
$dst = Join-Path $env:LOCALAPPDATA 'FTA Studio'
Copy-Item $src\runtime $dst -Recurse
Copy-Item $src\app     $dst -Recurse
$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'FTA Studio.lnk'))
$lnk.TargetPath = Join-Path $dst '启动 FTA Studio.bat'
$lnk.WorkingDirectory = $dst
$lnk.Save()
```

卸载：先 `Stop-Process` 掉 `CommandLine -match 'launch\.mjs'` 的 node，再删目录与两个快捷方式。

## 7. 沙箱限制（WorkBuddy 环境）

- `Add-Type`、COM 实例化（`New-Object -ComObject`）、`ProcessStartInfo`、直接 `cmd /c` 可能被安全策略拦截
- 需要回收站语义时，退化方案：**移动到备份目录**（可恢复），不要用 `rm`/`del /F`
- 测试 .bat 时用 Node `spawn('cmd.exe', ['/c', bat])`，中文文件名会被参数编码破坏 → 测试时复制成 ASCII 临时名

## 8. 便携包体积参考

| 项 | 大小 |
|---|---|
| 源码 | ~380 KB |
| node.exe | ~89 MB |
| 解压后总计 | ~87.5 MB |
| zip（Optimal） | ~32.7 MB |
