# Daily Backup - Remote Repo 创建指引

## 远程 repo 未创建时的处理

### 1. 在托管平台创建空 repo

在 GitHub / GitLab / 云服务器自建等平台创建空的远程仓库，获取其 SSH URL 或 HTTPS URL。

### 2. 添加 remote

```bash
git remote add origin <platform-ssh-url>
git push -u origin HEAD
```

### 3. 如使用 SSH config 简化（推荐）

在 `~/.ssh/config` 中预先配置好 host 别名，例如：

```
Host studio-backup
    HostName <实际IP或域名>
    User git
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

然后 git remote 设为：

```bash
git remote add studio-backup studio-backup:/path/to/repo.git
```

这样 git push 时使用 SSH config 中的配置，不会在 git URL 中暴露 IP 或 key。

**本工作室配置示例**（仅供参考）：
- `~/.ssh/config` 中 `Host studio-backup` 指向 `C:/git-repos/openclaw-workspace-{agentId}`（路径含 agentId 后缀区分不同 agent 仓库）
- git remote: `studio-backup`