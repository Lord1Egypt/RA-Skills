# FastGithub Skill

代理服务，让 GitHub 访问速度飞起 🚀

## 简介

FastGithub 是一个 GitHub 加速器，通过本地代理服务器为 GitHub 提供访问加速。

**使用场景：**
- GitHub 访问速度慢
- Clone/Push 代码超时
- 下载 release 文件太慢

## 自动安装

### 一键启动

```bash
# 自动安装并启动
bash /workspace/skills/fastgithub/install.sh
```

### 手动安装步骤

#### 1. 解压安装包
```bash
tar -xzf fastgithub-linux-x64.tar.gz -C ~/fastgithub
```

#### 2. 启动服务
```bash
cd ~/fastgithub/publish
./fastgithub &
```

#### 3. 设置 Git 代理
```bash
export http_proxy=http://127.0.0.1:38457
export https_proxy=http://127.0.0.1:38457

# 永久生效
echo "export http_proxy=http://127.0.0.1:38457" >> ~/.bashrc
echo "export https_proxy=http://127.0.0.1:38457" >> ~/.bashrc
source ~/.bashrc
```

#### 4. 安装 CA 证书（可选，但推荐）
```bash
# Ubuntu/Debian
sudo cp ~/fastgithub/publish/cacert/fastgithub.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/fastgithub/publish/cacert/fastgithub.crt

# Windows (需要管理员权限)
# 双击证书文件 -> 安装到"受信任的根证书颁发机构"
```

---

## 使用命令

| 操作 | 命令 |
|------|------|
| 启动 | `bash /workspace/skills/fastgithub/start.sh` |
| 停止 | `bash /workspace/skills/fastgithub/stop.sh` |
| 重启 | `bash /workspace/skills/fastgithub/restart.sh` |
| 状态 | `ps aux \| grep fastgithub` |
| 测试 | `curl -x http://127.0.0.1:38457 https://github.com` |

---

## 文件结构

```
fastgithub/
├── install.sh          # 自动安装脚本
├── start.sh            # 启动脚本
├── stop.sh             # 停止脚本
├── restart.sh         # 重启脚本
├── fastgithub-linux-x64.tar.gz  # 安装包
└── SKILL.md           # 说明文档
```

---

## 触发条件

- "安装 FastGithub"
- "启动 GitHub 加速"
- "打开 GitHub 代理"
- "加速 GitHub 访问"

---

## 注意事项

1. **CA 证书** — 不安装证书会导致浏览器访问 GitHub 时显示不安全警告，但不影响 Git 操作

2. **代理端口** — 默认 `http://127.0.0.1:38457`

3. **系统要求** — Linux (x64), macOS, Windows

4. **权限** — 需要 sudo 安装 CA 证书

---

## 故障排除

### 无法连接
```bash
# 检查服务是否运行
ps aux | grep fastgithub

# 查看日志
tail -f /workspace/fastgithub.log
```

### Git 操作超时
```bash
# 确保代理已设置
echo $http_proxy
# 应该显示: http://127.0.0.1:38457
```

### 证书问题
```bash
# 临时跳过证书验证（不推荐）
git config --global http.sslVerify false
```