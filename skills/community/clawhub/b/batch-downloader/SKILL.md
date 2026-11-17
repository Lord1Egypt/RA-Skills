---
name: batch-downloader
description: "批量下载影视/音频资源：夸克网盘直链、BT磁力、B站，含风控评估、断点续传、完整性校验与归档。"
---

# 批量下载工作流

触发场景：网盘批量下载、夸克下载、磁力/BT 下载、影视全集下载、音频课程批量下载、下载续做/断点恢复。

## 铁律（动手前必答，老板 2026-08-30 定）

1. **风控评估**：会不会触发平台风控/封号？（夸克批量大文件 = 账号封禁的教训）
2. **备份源**：≥2 个独立来源（夸克 / BT磁力 / 迅雷 / 百度 / B站），主源被封立刻切备源。
3. **失败成本**：量化损失（时间、账号、会员费）。
4. **状态持久化**：脚本/凭证/清单放 `workspace/state/`，**禁止 /tmp**（重启即失）。

## 工作流（7 步）

1. 确认资源源 + 备份源（先评估风险边界，老板点头再动手）
2. 准备凭证：夸克 cookie 用 `get_quark_cookies.js` 导出（CDP → 127.0.0.1:18800）
3. 拿文件清单：`fid\t相对路径` 的 TSV（夸克）或磁力清单（BT）
4. 下载：
   - 夸克 → `quark_download.py`（客户端 UA 拿直链 + aria2c -x16 -s16）
   - BT/磁力 → `bt_download.py`（aria2c + 79 tracker + 高并发）
   - B站 → `yt-dlp -f "bestvideo+bestaudio" --merge-output-format mkv`
5. 校验：ffprobe 全量（moov atom / duration 非空）
6. 归档：`organize_media.py` 重命名 + 移动到目标目录
7. 汇报：成功/失败/总大小/位置，失败文件单独列出

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/get_quark_cookies.js` | CDP 导出夸克 cookie（Netscape 格式） |
| `scripts/quark_download.py` | 夸克批量下载（客户端 UA 绕过 size limit + aria2c 高并发 + 断点续传 + 跳过已存在） |
| `scripts/bt_download.py` | 磁力批量下载（tracker 增强 + 并发控制 + 校验） |
| `scripts/check_quark_unban.py` | 夸克下载接口解封检测（风控后恢复探测） |
| `scripts/organize_media.py` | ffprobe 校验 + 正则重命名 + 归档移动 |

## 关键参数速查（踩坑沉淀）

- 夸克客户端 UA：`Mozilla/5.0 ... quark-cloud-drive/2.5.56 Chrome/100.0.4896.160 Electron/18.3.5.12 Safari/537.36 Channel/pckk_other_ch`（绕过 size limit 的关键）
- 下载接口：`POST https://drive-pc.quark.cn/1/clouddrive/file/download` body=`{"fids":[fid]}`
- **直链绑定获取 IP**：拿直链和下载必须同一台机器
- **cookie 有效期约 3 小时**（__puus/__pus），跨时段需重新导出
- **aria2c 并发最优 = 3 路 × 16 分片**（>8 路 × 16 分片 = 128 连接会触发限流 → 空壳文件）
- 空壳文件特征：ffprobe 报 `moov atom not found` → 删掉重下（`--continue` 断点续传）
- 夸克免费账号 53M 视频就报 `23018 size limit`，会员才解锁；账号级封禁 = 全文件 401 + base64 加密串
- BT 小体积种子 ≠ 快（seeders 少反而卡 metadata）；TPB API（apibay.org）最干净，需代理 127.0.0.1:7897

## 凭证安全

- cookie/凭证**永不写入 skill 或代码**，从外部文件读（`--cookie /path/to/cookies.txt`）
- cookie 文件放 `workspace/state/credentials/`（已 gitignore）
