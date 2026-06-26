---
name: catfee-ssh
description: "SSH远程服务器密码连接技能。当用户提供服务器IP、用户名、密码需要SSH连接时激活。支持执行命令、查看配置、诊断问题、文件操作等运维操作。"
---

# Catfee SSH Skill

通过密码认证SSH连接远程服务器，执行运维操作。

## 前置要求

已安装 Posh-SSH 模块（首次使用时自动安装）。

## 连接模板

```powershell
# 安装模块（如果未安装）
if (!(Get-Module -ListAvailable Posh-SSH)) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -Scope CurrentUser
    Install-Module -Name Posh-SSH -Force -Scope CurrentUser -AllowClobber
}
Import-Module Posh-SSH

# 创建凭证并连接（用户提供：IP、用户名、密码）
$cred = New-Object System.Management.Automation.PSCredential("$username", (ConvertTo-SecureString "$password" -AsPlainText -Force))
$session = New-SSHSession -ComputerName "$ip" -Credential $cred -AcceptKey

# 执行命令
Invoke-SSHCommand -SessionId $session.SessionId -Command "command"

# 关闭连接
Remove-SSHSession -SessionId $session.SessionId
```

## 常用操作

### 查看系统信息
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "hostname && uname -a && cat /etc/os-release"
```

### 查看服务状态
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "systemctl status nginx"
Invoke-SSHCommand -SessionId $session.SessionId -Command "systemctl status docker"
```

### 查看文件
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "cat /path/to/file"
Invoke-SSHCommand -SessionId $session.SessionId -Command "ls -la /path/to/dir"
```

### 查看日志
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "tail -100 /var/log/nginx/error.log"
Invoke-SSHCommand -SessionId $session.SessionId -Command "journalctl -u nginx -n 100"
```

### Nginx 诊断
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "nginx -t 2>&1"
Invoke-SSHCommand -SessionId $session.SessionId -Command "cat /etc/nginx/nginx.conf"
Invoke-SSHCommand -SessionId $session.SessionId -Command "ls -la /etc/nginx/conf.d/"
Invoke-SSHCommand -SessionId $session.SessionId -Command "cat /etc/nginx/conf.d/*.conf"
```

### Docker 操作
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "docker ps -a"
Invoke-SSHCommand -SessionId $session.SessionId -Command "docker logs container_name --tail 100"
Invoke-SSHCommand -SessionId $session.SessionId -Command "docker-compose ps"
```

### 进程和端口
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "ps aux | grep nginx"
Invoke-SSHCommand -SessionId $session.SessionId -Command "netstat -tlnp"
Invoke-SSHCommand -SessionId $session.SessionId -Command "ss -tlnp"
```

## 输出格式化

获取完整命令输出：
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "command" | Select-Object -ExpandProperty Output | Out-String -Width 4000
```

## 会话保持

连续执行多个命令时保持同一个 session：
```powershell
$session = New-SSHSession -ComputerName "$ip" -Credential $cred -AcceptKey
Invoke-SSHCommand -SessionId $session.SessionId -Command "cmd1"
Invoke-SSHCommand -SessionId $session.SessionId -Command "cmd2"
Invoke-SSHCommand -SessionId $session.SessionId -Command "cmd3"
Remove-SSHSession -SessionId $session.SessionId
```

## 执行修改操作

执行需要sudo权限的操作：
```powershell
Invoke-SSHCommand -SessionId $session.SessionId -Command "sudo nginx -s reload"
Invoke-SSHCommand -SessionId $session.SessionId -Command "sudo systemctl restart docker"
```

## 安全注意

- 每次使用用户提供的具体凭证，不存储凭证
- 完成操作后关闭SSH会话
- 不在日志或输出中暴露敏感信息