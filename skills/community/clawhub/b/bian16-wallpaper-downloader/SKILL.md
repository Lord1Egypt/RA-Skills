---
name: bian16-wallpaper-downloader
description: Download 4K mobile wallpapers specifically from pic.netbian.com (彼岸图网), including WeChat QR login flow, token-based original image download, 3-minute rate-limit spacing, 4K validation, and cleanup of non-4K files. Use when the user explicitly wants 彼岸图网 / pic.netbian.com wallpapers, 手机壁纸, 二次元竖屏图, or wants to batch download and verify true 4K images from that site.
---

# 彼岸图网 4K 手机壁纸下载

当用户明确要从**彼岸图网**下载手机壁纸、4K 壁纸、二次元竖屏壁纸时使用本 skill。

## 工作流

### 1. 确认需求
先确认这些参数：
- 数量（默认 20）
- 保存目录（默认 `/data/wallpapers/anime/bian16`）
- 下载间隔（默认 180 秒）
- 是否只保留真 4K（默认是）

### 2. 登录彼岸图网
彼岸图网 4K 原图需要登录后才能下载。

推荐流程：
1. 用浏览器打开任意彼岸图网详情页，例如：`https://pic.netbian.com/tupian/42413.html`
2. 点击“注册登录”或“高清原图(2400x3840)”触发登录弹窗
3. 让用户用微信扫码后，按页面提示回复验证码
4. **如果出现滑块验证**：
   - 默认策略：**暂停自动化，明确请用户手动完成滑块/验证码**
   - 不要承诺可以稳定自动通过滑块
   - 不要反复高频重试、乱点、或持续刷新页面
   - 可以在用户明确同意时尝试一次视觉 AI / 浏览器自动化辅助，但**失败后必须立即回退到人工处理**
5. 登录成功后，读取浏览器 cookie：
   ```js
   () => document.cookie
   ```
6. Cookie 中通常至少应包含：
   - `RcGFvmluserid`
   - `RcGFvmlauth`
   - `RcGFvmlusername`

如果页面仍显示“注册登录”而 cookie 不完整，说明登录没有同步到当前浏览器，需要重新刷新页面并重新登录。
如果刚刚经历过滑块验证，也要在验证通过后重新读取当前浏览器 cookie，再继续下载流程。

### 3. 执行下载脚本
下载脚本：`scripts/download.py`

示例：
```bash
python3 /root/.openclaw/workspace/skills/bian16-wallpaper-downloader/scripts/download.py \
  --cookie 'COOKIE_STRING' \
  --count 20 \
  --interval 180 \
  --outdir /data/wallpapers/anime/bian16
```

脚本会：
- 扫描 `shoujibizhi` 分类页，收集详情页 ID
- 调用 `/e/extend/netbiandownload.php?id=xxx` 获取 token
- 再用 token 下载真正的 4K 原图
- 自动跳过宽度 `< 2000` 的非 4K 图片
- 每张图片下载后等待 `--interval` 秒

### 4. 校验与清理
校验脚本：`scripts/verify_4k.py`

只检查：
```bash
python3 /root/.openclaw/workspace/skills/bian16-wallpaper-downloader/scripts/verify_4k.py \
  --dir /data/wallpapers/anime/bian16
```

检查并删除非 4K：
```bash
python3 /root/.openclaw/workspace/skills/bian16-wallpaper-downloader/scripts/verify_4k.py \
  --dir /data/wallpapers/anime/bian16 \
  --delete
```

### 5. 按需读取参考说明
当需要理解 token 下载链路、JPEG 多 SOF 分辨率判断、或登录状态异常时，读取：
- `references/download-notes.md`

## 关键注意事项
- 必须登录后再下载 4K，否则只能拿到缩略图或中分辨率图
- 遇到滑块验证时，默认让用户手动完成；不要对自动过滑块做稳定性承诺
- 如需尝试视觉 AI / 浏览器自动化辅助过滑块，最多只做低次数尝试；失败后立即转人工
- 必须设置下载间隔，默认 3 分钟，避免触发彼岸图网限制
- 不要默认所有下载结果都是真 4K，下载后必须校验分辨率
- 有些图片即使通过 token 下载，仍可能不是 4K，需要删除并补齐
- JPEG 可能包含多个 SOF 标记，校验分辨率时应取最后一个 SOF 标记
