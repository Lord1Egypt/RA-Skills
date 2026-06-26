---
name: volcengine-storage-tos-test
description: Minimal TOS smoke tests. Validate AK/SK config, list buckets, and upload/download with Volcengine TOS. Supports both tosutil CLI and tos_manage.py script.
---

Category: test

# TOS 对象存储最小可行性测试

## Goals

- 验证 AK/SK/Region/Endpoint 配置正确。
- 验证 TOS 访问（列桶、上传、下载）。

## Prerequisites

- 已配置 AK/SK（环境变量或 `.env`）。
- 已准备一个可读写的 TOS Bucket。

---

## 方式一：使用 tos_manage.py 脚本（推荐）

依赖：`pip install tos`

### 1) 列出 Bucket

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py list-buckets --print-json
```

### 2) 列出对象

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py list-objects \
  --bucket <bucket> --prefix "" --max-keys 20 --print-json
```

### 3) 上传小文件

```bash
echo "tos-manage-test-$(date +%s)" > /tmp/tos-test.txt
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py upload \
  --bucket <bucket> --key tests/tos-test.txt --file /tmp/tos-test.txt --print-json
```

### 4) 获取元数据

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py head \
  --bucket <bucket> --key tests/tos-test.txt --print-json
```

### 5) 下载并校验

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py download \
  --bucket <bucket> --key tests/tos-test.txt --file /tmp/tos-test-down.txt
diff /tmp/tos-test.txt /tmp/tos-test-down.txt && echo "PASS: content matches" || echo "FAIL: content mismatch"
```

### 6) 生成预签名 URL

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py presign \
  --bucket <bucket> --key tests/tos-test.txt --expires 300 --print-json
```

### 7) 清理测试文件

```bash
python skills/storage/tos/volcengine-storage-tos/scripts/tos_manage.py delete \
  --bucket <bucket> --key tests/tos-test.txt --confirm
```

---

## 方式二：使用 tosutil CLI

tosutil 是火山引擎官方 TOS 命令行工具，需单独下载安装。
参考：https://www.volcengine.com/docs/6349/148772

### 1) 查看配置

```bash
tosutil config
```

### 2) 列出 Bucket

```bash
tosutil ls
```

### 3) 列出对象（指定 bucket）

```bash
tosutil ls tos://<bucket> -s --limited-num 20
```

### 4) 上传小文件

```bash
echo "tosutil-test-$(date +%s)" > /tmp/tosutil-test.txt
tosutil cp /tmp/tosutil-test.txt tos://<bucket>/tests/tosutil-test.txt
```

### 5) 下载并校验

```bash
tosutil cp tos://<bucket>/tests/tosutil-test.txt /tmp/tosutil-test-down.txt
diff /tmp/tosutil-test.txt /tmp/tosutil-test-down.txt && echo "PASS" || echo "FAIL"
```

### 6) 清理

```bash
tosutil rm tos://<bucket>/tests/tosutil-test.txt
```

---

## Expected Results

- `list-buckets` / `tosutil ls` 能返回至少一个 bucket。
- 上传成功返回 ETag / status 200。
- 下载文件内容与上传一致（`diff` 无输出）。
- `head` 返回正确的 content_length 和 content_type。
- 预签名 URL 可访问。

## 常见失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 403 AccessDenied | AK/SK 错误或无权限 | 检查 IAM 策略，确认允许 `tos:*` 或最小读写权限 |
| Endpoint 不可达 | Region 与 Endpoint 不匹配 | 端点格式为 `tos-{region}.volces.com` |
| NoSuchBucket | Bucket 名拼写或 Region 错误 | 先 `list-buckets` 确认桶存在 |
| 上传成功但下载内容不一致 | 网络中断或部分写入 | 检查 ETag 或重新上传 |
