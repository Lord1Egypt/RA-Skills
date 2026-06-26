---
name: baidu-pan-upload-skill
description: 百度网盘文件上传，支持分片上传、断点续传和进度监控。触发词：百度网盘上传、baidu pan upload、上传文件到网盘、upload to baidu pan、断点续传。适用场景：(1)上传本地文件到百度网盘指定目录 (2)大文件自动分片上传 (>4MB) (3)中断后断点续传 (4)自动创建远程目录。
---

# 百度网盘文件上传

## 前提

已有百度网盘开放平台授权（access_token有效），.env文件含AccessToken、AppKey、SecretKey。

先用 `baidu-pan-per-auth-skill` 完成授权获取token。

## 上传文件

```bash
python3 scripts/upload.py <local_file> <remote_dir> <env_path> [--overwrite]
```

### 参数

| 参数 | 说明 |
|------|------|
| local_file | 本地文件路径 |
| remote_dir | 网盘远程目录（如 `/docker镜像`、`/备份`） |
| env_path | .env文件路径（含AccessToken等凭据） |
| --overwrite | 覆盖同名文件（默认不覆盖） |

### 上传流程

所有文件统一走 **precreate → superfile2(tmpfile) × N → create** 流程：

- **≤4MB** → 1片快速上传
- **>4MB** → 自动分片（每片4MB），计算每片MD5校验

### 断点续传

上传中断后，重新运行**相同命令**即可自动续传：

1. 上传状态自动保存在源文件同目录下的 `.upload_state.json`
2. 重启时检测：文件MD5未变 → 跳过已上传分片 → 从断点继续
3. Ctrl+C 安全中断，状态自动保存
4. 上传完成后自动删除状态文件

### 进度监控

大文件上传时实时显示：

```
  [████████████░░░░░░░░] 60.0% | 1.1GB/1.9GB | 3.2MB/s | ETA 4m12s
```

### 示例

```bash
# 上传单个文件
python3 scripts/upload.py /tmp/report.pdf "/文档" /path/to/.env

# 上传大文件（自动分片+进度监控+断点续传）
python3 scripts/upload.py /backup/data.zip "/备份" /path/to/.env

# 覆盖已有文件
python3 scripts/upload.py /tmp/config.json "/配置" /path/to/.env --overwrite

# 中断后续传（重新运行相同命令即可）
python3 scripts/upload.py /backup/data.zip "/备份" /path/to/.env
```

## 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 分片大小 | 4MB | 百度网盘API限制 |
| 上传域名 | d.pcs.baidu.com | 分片上传专用域名 |
| 重试次数 | 3 | 每个分片失败后重试 |
| 远程路径格式 | /开头 | 如 `/docker镜像` |
| 状态文件 | .upload_state.json | 保存在源文件同目录 |

## 故障排查

| 错误 | 原因 | 解决 |
|------|------|------|
| errno: 2 | 路径格式错误 | 确保以 `/` 开头 |
| error_code: 31023 | token过期或uploadid过期 | 用 `baidu-pan-per-auth-skill` 刷新token |
| error_code: 31064 | 文件已存在 | 加 `--overwrite` 覆盖 |
| SSL/超时 | 网络波动 | 自动重试3次 |
| 上传中断 | Ctrl+C或网络断开 | 重新运行相同命令，自动断点续传 |
| 续传失败 | 源文件已变更 | 删除 `.upload_state.json` 重新上传 |

## 依赖

- curl（系统自带）
- Python 3.7+
- 有效的百度网盘access_token
