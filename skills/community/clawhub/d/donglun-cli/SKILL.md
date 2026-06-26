---
name: donglun-poster
description: 在东方热线论坛（东论）发帖、回帖、浏览热帖、查看帖子和回复。支持从环境变量或配置文件读取 token，无需登录。
allowed-tools: Read, Bash(cd *), Bash(python:scripts/post_donglun.py *)
---

# 东论发帖/回帖/浏览 Skill

Token 通过环境变量 `CNOOL_API_TOKEN` 或 `config.json` 配置。

## 使用方式

### 浏览热帖

```bash
# 获取最近7天热帖（默认）
python scripts/post_donglun.py --hot

# 获取最近3天热帖
python scripts/post_donglun.py --hot -d 3

# 分页浏览
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

### 发帖

```bash
# 发帖（需要提供标题）
python scripts/post_donglun.py -t "帖子标题" -c "帖子内容"

# 从文件读取内容
python scripts/post_donglun.py -t "长文分享" -c @article.txt
```

### 回帖

```bash
# 回复指定帖子
python scripts/post_donglun.py -r "10939082" -c "回复内容"

# 从文件读取内容
python scripts/post_donglun.py -r "10939082" -c @reply.txt
```
