---
name: baidu-disk-manager
description: |
  管理百度网盘文件，支持登录、列出文件、上传/下载/复制/移动/删除/重命名/创建文件夹、查看配额等操作。
metadata: {"clawdbot":{"emoji":"💾","requires":{"bins":["./scripts/go-bdisk"]}}}
---

## 百度网盘文件管理 Skill（Baidu Netdisk Manager）

基于 `go-bdisk` CLI 工具实现百度网盘文件管理功能，支持设备码授权登录、文件列表查看、上传下载、复制移动删除等常见文件操作。

## 技能定位

- 当用户需要「管理百度网盘文件」「上传文件到百度网盘」「下载百度网盘文件」「查看百度网盘内容」时使用本 Skill
- 支持百度网盘个人版文件管理操作

## 登录与登出（需用户明确操作）

**登录和登出必须由用户明确要求才能执行**，本 Skill 不会自动调用。

### 登录百度网盘

如果用户未登录，在执行其他操作前应提示用户：

> 百度网盘未登录，请先自行执行登录命令：
> ```bash
> ./scripts/go-bdisk login --app-key YOUR_APP_KEY --secret-key YOUR_SECRET_KEY
> ```
> 登录成功后再继续操作。

### 查询登录状态

```bash
# 查看当前用户信息和网盘配额
./scripts/go-bdisk info -j
```

如果 `info` 命令返回未登录错误，提示用户执行登录。

### 退出登录

仅当用户明确要求「退出百度网盘登录」时才执行：

```bash
./scripts/go-bdisk logout
```

## 变更操作确认流程

**复制、移动、重命名、删除操作属于变更操作**，执行前必须：

1. 打印变更信息（源路径、目标路径、操作类型）
2. 向用户确认：「确认执行此操作吗？请回复「确认」、「ok」或「行」」
3. 只有用户明确回复「确认」「ok」或「行」时才执行
4. 任何其他回复或沉默都不执行

## 常用操作

### 查看文件列表

```bash
# 列出根目录文件
./scripts/go-bdisk ls -j

# 列出指定目录
./scripts/go-bdisk ls /我的资源 -j
```

### 创建文件夹

```bash
./scripts/go-bdisk mkdir /备份 -j
```

### 查看文件信息

```bash
./scripts/go-bdisk stat /我的资源/document.pdf -j
```

### 重命名文件（需确认）

**操作前必须向用户确认：**

```
即将重命名文件：
  原文件名：/旧文件名.txt
  新文件名：新文件名.txt

确认执行此操作吗？请回复「确认」「ok」或「行」
```

确认后执行：
```bash
./scripts/go-bdisk rename /旧文件名.txt 新文件名.txt -j
```

### 移动文件（需确认）

**操作前必须向用户确认：**

```
即将移动文件：
  源路径：/source/path
  目标路径：/dest/path

确认执行此操作吗？请回复「确认」「ok」或「行」
```

确认后执行：
```bash
./scripts/go-bdisk mv /source/path /dest/path -j
```

### 复制文件（需确认）

**操作前必须向用户确认：**

```
即将复制文件：
  源路径：/source/path
  目标路径：/dest/path

确认执行此操作吗？请回复「确认」「ok」或「行」
```

确认后执行：
```bash
./scripts/go-bdisk cp /source/path /dest/path -j
```

### 删除文件（需确认）

**操作前必须向用户确认：**

```
即将删除文件：
  路径：/要删除的文件.txt

⚠️ 此操作不可恢复！

确认执行此操作吗？请回复「确认」「ok」或「行」
```

确认后执行：
```bash
./scripts/go-bdisk rm /要删除的文件.txt -j
```

### 上传文件

```bash
# 上传到根目录
./scripts/go-bdisk upload /local/file.txt -j

# 上传到指定目录
./scripts/go-bdisk upload /local/file.txt /我的资源/ -j
```

### 下载文件

```bash
# 下载到当前目录
./scripts/go-bdisk download /百度网盘文件.txt -j

# 下载到指定本地路径
./scripts/go-bdisk download /百度网盘文件.txt /local/downloads/ -j
```

## JSON 输出模式

所有命令支持 `-j` 或 `--json` 参数以 JSON 格式输出结果，便于程序化处理：

```bash
./scripts/go-bdisk ls -j
```

## 错误处理

命令执行失败时，go-bdisk 会返回错误信息。使用 `-j` 参数可获取结构化错误输出。

## 在 OpenClaw 中的推荐用法

### 查询类操作（直接执行）

1. 用户提问：「列出百度网盘根目录的文件」
   代理调用：`./scripts/go-bdisk ls -j`

2. 用户提问：「查看我的百度网盘剩余空间」
   代理调用：`./scripts/go-bdisk info -j`

3. 用户提问：「上传这份文档到百度网盘」
   代理调用：`./scripts/go-bdisk upload /local/doc.pdf /我的资源/ -j`

4. 用户提问：「下载百度网盘里的报告」
   代理调用：`./scripts/go-bdisk download /报告.pdf -j`

### 变更类操作（需确认）

5. 用户提问：「把 test.txt 移动到备份文件夹」
   - 先执行 `ls` 确认文件存在
   - 向用户确认变更信息
   - 等待用户回复「确认」「ok」或「行」
   - 确认后执行：`./scripts/go-bdisk mv /test.txt /备份/test.txt -j`

6. 用户提问：「复制这份文档到工作目录」
   - 向用户确认变更信息
   - 等待用户回复「确认」「ok」或「行」
   - 确认后执行：`./scripts/go-bdisk cp /文档.docx /工作目录/ -j`

7. 用户提问：「删除旧文件.txt」
   - 向用户确认变更信息（注意警告此操作不可恢复）
   - 等待用户回复「确认」「ok」或「行」
   - 确认后执行：`./scripts/go-bdisk rm /旧文件.txt -j`

### 登录操作（用户明确要求才执行）

8. 用户提问：「帮我登录百度网盘」
   - 提示用户自行执行登录命令并提供命令示例
   - **不自动执行 login 命令**
