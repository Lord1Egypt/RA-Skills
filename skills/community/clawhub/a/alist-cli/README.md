# AList CLI for OpenClaw

> **ClawHub**: https://clawhub.ai/leeshunee/alist-cli | `clawhub install alist-cli`


基于 AList API 的文件管理工具，供 OpenClaw AI 助手使用。

## 功能

- 登录认证
- 文件列表/浏览
- 文件上传/下载
- 创建文件夹
- 删除/移动文件
- 搜索文件
- 获取文件直链

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/KinemaClawWorkspace/alist-cli.git
cd alist-cli

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
export ALIST_URL="https://your-alist-server"
export ALIST_USERNAME="your_username"
export ALIST_PASSWORD="your_password"
```

## 配置

设置环境变量：

```bash
export ALIST_URL="https://your-alist-server"
export ALIST_USERNAME="your_username"
export ALIST_PASSWORD="your_password"
```

## 使用

```bash
alist login
alist ls /
alist upload local.txt /remote.txt
alist get /file.txt
alist mkdir /folder
alist rm /file.txt
alist mv /old /new
alist search keyword
alist whoami
```

## CLI 选项

| 命令 | 说明 |
|------|------|
| login <user> <pass> | 登录 |
| ls [path] | 列出文件 |
| get <path> | 获取文件信息 |
| mkdir <path> | 创建文件夹 |
| upload <local> <remote> | 上传文件 |
| rm <path> | 删除文件 |
| mv <src> <dst> | 移动文件 |
| search <keyword> [path] | 搜索 |
| whoami | 当前用户 |

## 项目结构

```
alist-cli/
├── README.md
├── SKILL.md
├── LICENSE
├── requirements.txt
├── scripts/
│   └── alist_cli.py
└── references/
    └── openapi.json
```

## License

CC BY 4.0 - 必须著名来源，允许自由使用
