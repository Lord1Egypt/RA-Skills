# 自动化部署配置

## Git 仓库配置
```json
{
  "git": {
    "url": "http://192.168.1.169:8015/peninsula/points",
    "branch": "main",
    "auth": {
      "type": "http",
      "username": "",
      "password": ""
    }
  }
}
```

## 服务器配置
```json
{
  "server": {
    "host": "",
    "port": 22,
    "user": "root",
    "deployPath": "/www/wwwroot/points",
    "backupPath": "/www/backup/points"
  }
}
```

## 项目配置
```json
{
  "project": {
    "name": "points",
    "type": "nodejs+java",
    "nodeVersion": "20",
    "javaVersion": "17",
    "build": {
      "node": {
        "installCmd": "npm install",
        "buildCmd": "npm run build",
        "outputDir": "dist"
      },
      "java": {
        "installCmd": "",
        "buildCmd": "mvn clean package",
        "outputDir": "target",
        "jarFile": ""
      }
    },
    "deploy": {
      "restartCmd": "",
      "healthCheck": ""
    }
  }
}
```

## 使用说明

1. **首次配置**：
   - 填写 Git 用户名密码（或配置 SSH Key）
   - 填写服务器 SSH 信息
   - 确认项目构建命令

2. **SSH Key 配置**（推荐）：
   ```bash
   # 生成 SSH Key
   ssh-keygen -t ed25519 -C "openclaw-deploy" -f ~/.ssh/openclaw_deploy
   
   # Git 仓库：将公钥添加到 Git 服务器
   cat ~/.ssh/openclaw_deploy.pub
   
   # 部署服务器：将公钥添加到服务器
   ssh-copy-id -i ~/.ssh/openclaw_deploy.pub user@server
   ```

3. **宝塔面板配置**：
   - 确保服务器 SSH 端口开放（默认 22）
   - 确保部署目录有写入权限
   - 配置好 Node.js 和 Java 运行环境

---

**注意**：敏感信息（密码、密钥）不要直接写在这里，使用环境变量或加密存储。
