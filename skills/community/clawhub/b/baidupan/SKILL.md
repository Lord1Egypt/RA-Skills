---
name: baidupan
description: 百度网盘自动化工具，支持上传、下载、列表、同步等操作。
homepage: https://github.com/houtianze/bypy
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["bypy"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "bypy",
              "label": "Install bypy (pip)",
            },
          ],
      },
  }
---

# BaiduPan（百度网盘）

百度网盘自动化工具，基于 `bypy` 实现。支持文件上传、下载、列表查看、同步等操作。

## 前置要求

首次使用需要**授权登录**：

```bash
# 运行授权命令
{baseDir}/scripts/auth.sh

# 按提示操作：
# 1. 复制显示的链接到浏览器打开
# 2. 登录百度账号并授权
# 3. 复制授权码
# 4. 粘贴回终端
```

授权一次，长期有效（直到百度token过期）。

---

## 核心功能

| 功能 | 命令 | 说明 |
|:---|:---|:---|
| 查看网盘文件 | `list.sh` | 列出指定目录内容 |
| 下载文件 | `download.sh` | 从网盘下载到本地 |
| 上传文件 | `upload.sh` | 从本地上传到网盘 |
| 同步目录 | `sync.sh` | 双向或单向同步 |
| 查看配额 | `quota.sh` | 查看网盘空间使用情况 |

---

## 功能详解

### 1. 查看网盘文件 (list.sh)

```bash
# 列出根目录
{baseDir}/scripts/list.sh

# 列出指定目录
{baseDir}/scripts/list.sh /我的视频/项目

# 显示文件详情（含大小、修改时间）
{baseDir}/scripts/list.sh /我的视频 --detail
```

### 2. 下载文件 (download.sh)

```bash
# 下载单个文件到当前目录
{baseDir}/scripts/download.sh /我的视频/长城素材/video1.mp4

# 下载到指定目录
{baseDir}/scripts/download.sh /我的视频/长城素材/video1.mp4 --out ~/Downloads/

# 下载整个目录
{baseDir}/scripts/download.sh /我的视频/长城素材/ --out ~/Downloads/长城素材/

# 覆盖已存在文件
{baseDir}/scripts/download.sh /我的视频/video.mp4 --out ~/Downloads/ --force
```

### 3. 上传文件 (upload.sh)

```bash
# 上传单个文件到网盘根目录
{baseDir}/scripts/upload.sh ~/Downloads/video.mp4

# 上传到指定目录
{baseDir}/scripts/upload.sh ~/Downloads/video.mp4 --remote /我的视频/项目/

# 上传整个目录
{baseDir}/scripts/upload.sh ~/Downloads/长城素材/ --remote /我的视频/

# 覆盖网盘上已存在文件
{baseDir}/scripts/upload.sh ~/Downloads/video.mp4 --remote /我的视频/ --force
```

### 4. 同步目录 (sync.sh)

```bash
# 从网盘同步到本地（网盘为主）
{baseDir}/scripts/sync.sh down /我的视频/项目 ~/本地备份/项目/

# 从本地同步到网盘（本地为主）
{baseDir}/scripts/sync.sh up ~/本地项目/ /我的视频/项目/

# 双向同步（谨慎使用）
{baseDir}/scripts/sync.sh both ~/本地项目/ /我的视频/项目/
```

### 5. 查看配额 (quota.sh)

```bash
{baseDir}/scripts/quota.sh
```

输出示例：
```
网盘配额：2.0 TB
已使用：1.2 TB (60%)
剩余可用：800 GB
```

---

## 视频项目工作流

### 场景：从网盘下载素材进行剪辑

```bash
# 1. 查看网盘素材目录
{baseDir}/scripts/list.sh /视频素材/长城春晚/

# 2. 下载所有素材到本地
{baseDir}/scripts/download.sh /视频素材/长城春晚/ --out ~/龙虾项目/长城赞助春晚/raw/

# 3. 剪辑完成后，上传成品回网盘
{baseDir}/scripts/upload.sh ~/龙虾项目/长城赞助春晚/output/final.mp4 --remote /视频成品/
```

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|:---|:---|:---|
| `Not authorized` | 未授权或授权过期 | 运行 `auth.sh` 重新授权 |
| `Network error` | 网络问题 | 检查网络，稍后重试 |
| `File not found` | 路径错误 | 检查网盘路径，区分大小写 |
| `Quota exceeded` | 网盘空间不足 | 清理网盘或购买会员 |
| `Rate limited` | 请求过于频繁 | 等待几分钟后重试 |

---

## 注意事项

1. **授权安全**：授权信息保存在本地 `~/.bypy/` 目录，不要分享给他人
2. **大文件传输**：上传/下载大文件可能需要较长时间，请保持网络稳定
3. **路径格式**：网盘路径以 `/` 开头，如 `/我的视频/项目/`
4. **免费额度**：百度网盘对非会员有下载限速，大文件建议开通会员或使用百度云同步盘

---

## 相关链接

- bypy 项目：https://github.com/houtianze/bypy
- 百度网盘开放平台：https://pan.baidu.com/union
