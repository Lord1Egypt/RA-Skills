# 批量下载踩坑备忘（全部实测，2026-08-29/30）

## 夸克网盘

### 反爬机制（2026 版）
- 下载接口：`POST https://drive-pc.quark.cn/1/clouddrive/file/download`，body `{"fids":[fid]}`
- **客户端 UA 是绕过 size limit（23018）的关键**：
  `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) quark-cloud-drive/2.5.56 Chrome/100.0.4896.160 Electron/18.3.5.12 Safari/537.36 Channel/pckk_other_ch`
- 普通网页 UA 对大文件返回 `23018 download file size limit`（免费账号 53M 就触发）
- **账号级封禁特征**：所有文件（含 1MB jpg）返回 401 + base64 加密串；页面底部横幅「账号涉嫌违规已被封禁」；`pan.quark.cn/account/info` 仍 200 但 member 接口 401
- 封禁诱因：单日批量下载 135 文件 61G + 多部剧 → 触发风控；申诉被客服模板驳回（版权内容）
- **直链绑定获取 IP**：拿直链和下载必须同机，否则 403
- **cookie 有效期约 3 小时**（__puus/__pus），跨时段需重新导出（CDP `Network.getAllCookies`）
- 列表接口 `file/sort?pdir_fid=&pr=ucpro&fr=pc` 带 cookie 仍正常（封禁不影响列文件）

### 下载速度优化
- 单文件 aria2c `-x4` 慢节点仅 400KiB/s → **`-x16 -s16` 暴涨到 37MiB/s**
- 并发路数：**3 路 × 16 分片最优**（~17MB/s 稳定）；8 路 × 16 分片 = 128 连接触发限流 → 空壳文件
- 空壳文件特征：ffprobe 报 `moov atom not found` 或 duration 为 0/空

### 转存 API（分享 → 自己网盘）
- 端点：`POST https://drive-h.quark.cn/1/clouddrive/share/sharepage/save`
- 反爬 header：`bx_et`（加密签名）、`bx-umidtoken`、`bx-ua`、`Referer: https://pan.quark.cn/`
- 参数：pwd_id + stoken + pdir_fid + to_pdir_fid + pdir_save_all + exclude_fids + scene:link
- stoken：`POST drive-pc.quark.cn/1/clouddrive/share/sharepage/token` body={pwd_id, passcode}
- 参考实现：QuarkPanTool 开源项目 `/tmp/qpt_quark.py` 的 quark_file_download

## BT/磁力

- TPB API（apibay.org）最干净（其他站被 Cloudflare/CAPTCHA 挡）；需代理 `127.0.0.1:7897`
- 磁力加 **79 个 tracker**（ngosang trackers_all.txt）→ metadata 秒拿
- **小体积种子 ≠ 快**：MeGusta HEVC 版 seeders 只有 5-12 个，连 metadata 都拿不到；EDITH 1080p 反而有 seedbox 能 4.9MiB/s
- **反复重启 aria2 是错的**：pkill 清空 peer 缓存 + DHT 冷启动，反而丢进度
- `--seed-time=0` 下完即停；`--continue` 断点续传
- 限速场景判断：E12 秒下 4.9MiB/s（连到高速 seedbox）是运气；同批其他文件 49KiB/s 是做种者限速

## 老设备算力控制（2012 MacBook Pro / Ubuntu）

- **2 路并发 + `nice -n 10`** 降优先级，load 控制在 4 以下
- 16 路 ffmpeg 并发转码 → 死机两次；`wma → mp3` 约 1.5 分钟/个
- 原子写入：先 .tmp 再 mv，死机不损坏已完成文件
- 转码后 `find -name '*.tmp.mp3'` 清理半成品

## 状态持久化（铁律）

- 脚本/凭证/清单放 `workspace/state/`（credentials/ manifests/ scripts/ notes/），**禁止 /tmp**
- macOS 重启清 /tmp：脚本、cookie、清单、CDP 端口全没，自动化链条断裂
- 每条自动化任务记录「断了怎么恢复」三步

## B站下载

- `yt-dlp -f "bestvideo+bestaudio" --merge-output-format mkv`，未登录可下 1080p
- B站番剧（bangumi）完整版需大会员：`yt-dlp -F` 会提示 "Only preview format is available...premium member"
- UP主上传的老片：匿名/普通 cookie 最高 360p~480p（源本身是 VCD/DVD 转录低清）
- B站视频 ID 音频流：如 `-f 30232` 拿 127k m4a
