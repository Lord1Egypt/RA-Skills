# 🚗 CarKey

车辆信息查询技能 - 查询车辆位置和车况

---

## 首次使用

```
用户：查一下车在哪
助手：❌ 未找到认证信息

请提供认证信息，格式为：
  vehicleToken####accessToken
```

认证信息自动缓存，后续直接查询即可。

---

## 系统支持

| 系统 | 状态 |
|------|------|
| Linux | ✅ 支持 |
| macOS | ✅ 支持 |
| Windows (Git Bash/WSL) | ✅ 支持 |

---

## 依赖安装

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install curl jq
```

### Linux (CentOS/RHEL)
```bash
sudo yum install curl jq
```

### macOS
```bash
brew install curl jq
```

### Windows

**方式 1: Git Bash**
- 安装 [Git for Windows](https://git-scm.com/download/win)
- curl 和 jq 已包含

**方式 2: WSL**
```bash
wsl sudo apt-get install curl jq
```

---

## 缓存文件

| 文件 | Linux/macOS | Windows |
|------|-------------|---------|
| Token 缓存 | `~/.carkey_cache.json` | `%USERPROFILE%/.carkey_cache.json` |
| 查询历史 | `~/.carkey_history.json` | `%USERPROFILE%/.carkey_history.json` |