# 东方热线论坛（东论）Bot

在东方热线论坛（东论）发帖、回帖、浏览热帖。

## 功能特性

- 📊 **浏览热帖** - 获取指定天数内的热门帖子列表
- 📄 **查看帖子** - 查看指定帖子的详细内容
- 💬 **查看回复** - 查看帖子的回复列表（支持分页）
- ✍️ **发布帖子** - 在东论发布新帖子
- 💌 **回复帖子** - 对指定帖子进行回复

## 快速开始

### 0. 获取 Token
1. 正常注册、登录[东论](https://bbs.cnool.net)，并根据相关规定完成发帖前的实名认证

2. 点击个人中心-设置

3. 在【AI 授权密钥】中生成 Token

### 1. 配置 Token

支持以下三种方式配置 token（优先级从高到低）：

**方式1：命令行参数**
```bash
python scripts/post_donglun.py -k "your_token_here" -t "标题" -c "内容"
```

**方式2：环境变量 `CNOOL_API_TOKEN`**
```bash
# Windows PowerShell
$env:CNOOL_API_TOKEN="your_token_here"

# Windows CMD
set CNOOL_API_TOKEN=your_token_here

# Linux/Mac
export CNOOL_API_TOKEN="your_token_here"
```

**方式3：配置文件**

复制示例配置文件并填入你的 token：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "token": "your_token_here"
}
```

### 2. 使用 Skill

在 Agent 中：

```
/skill donglun-poster --hot
```

或直接运行脚本：

```bash
python scripts/post_donglun.py --hot
```

## 使用示例

### 浏览热帖

```bash
# 获取最近7天热帖（默认）
python scripts/post_donglun.py --hot

# 获取最近3天热帖
python scripts/post_donglun.py --hot -d 3

# 分页浏览，第2页，每页50条
python scripts/post_donglun.py --hot -p 2 -s 50
```

### 查看帖子详情

```bash
python scripts/post_donglun.py -v 10939082
```

### 查看回复列表

```bash
# 查看帖子的所有回复
python scripts/post_donglun.py --replies 10939082

# 分页查看
python scripts/post_donglun.py --replies 10939082 -p 2 -s 50
```

### 发布帖子

```bash
# 直接发布
python scripts/post_donglun.py -t "帖子标题" -c "帖子内容"

# 从文件读取内容（适用于长文）
python scripts/post_donglun.py -t "长文分享" -c @article.txt
```

### 回复帖子

```bash
# 直接回复
python scripts/post_donglun.py -r "10939082" -c "回复内容"

# 从文件读取内容
python scripts/post_donglun.py -r "10939082" -c @reply.txt
```

## 参数说明

| 参数 | 简写 | 说明 |
|------|------|------|
| `--hot` | | 获取热帖列表 |
| `--days` | `-d` | 热帖天数，默认7天 |
| `--view` | `-v` | 查看帖子详情，参数为帖子ID |
| `--replies` | | 查看回复列表，参数为帖子ID |
| `--title` | `-t` | 帖子标题（发帖时必需） |
| `--content` | `-c` | 帖子/回复内容 |
| `--reply` | `-r` | 帖子ID，指定则进行回帖 |
| `--page` | `-p` | 页码，默认1 |
| `--size` | `-s` | 每页条数，默认20 |
| `--token` | `-k` | 访问令牌（优先于配置文件） |
| `--save-config` | | 保存 token 到配置文件 |

## 文件结构

```
donglun-poster/
├── SKILL.md              # Skill 定义文件
├── README.md             # 本文件
├── config.json           # 配置文件
├── config.example.json   # 配置文件模板
└── scripts/
    └── post_donglun.py   # 主脚本
```

## 注意事项

- ⚠️ **Token 安全**：`config.json` 包含你的访问令牌，请勿提交到公共仓库
- 📊 **频率限制**：发帖/回帖频率过高可能导致 token 受限
- 📋 **发帖规则**：发帖时必须提供 `-t` 标题参数
- 💬 **回帖规则**：回帖时使用 `-r` 指定帖子ID，不需要 `-t` 参数

## 许可

仅供个人学习和使用，请遵守东论社区规范。