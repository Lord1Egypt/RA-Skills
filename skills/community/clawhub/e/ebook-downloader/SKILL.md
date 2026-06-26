---
name: ebook-downloader
description: 下载中文电子书到用户电脑。通过搜索读书派(dushupai.com)等资源站获取城通网盘下载链接，自动完成密码输入、API调用获取直链、curl下载、zip解压等全流程。当用户提到"下载电子书"、"下载这本书"、"找一下某本书的电子版"、"帮我下个epub/mobi/azw3"、"下载 XX 到电脑"等与获取电子书相关的表述时使用此 skill。即使用户只说了书名并暗示想要获取，也应触发此 skill。
---

# 电子书下载 Skill

## 整体流程

```
搜索书名 → 找到读书派页面 → 获取城通网盘链接和密码 → 浏览器自动解密 → 调用API获取直链 → curl下载 → Python解压 → 清理临时文件
```

## Step 1: 搜索下载源

用 web_search 搜索书名 + 关键词，优先找读书派(dushupai.com)的资源：

```
搜索: "《书名》 dushupai.com 下载"
备选: "《书名》 电子书下载 epub mobi"
```

读书派的页面 URL 格式为 `https://www.dushupai.com/book-content-{id}.html`。

## Step 2: 获取城通网盘链接

用 web_fetch 访问读书派的下载页面 `/download-book-{id}.html`，从中提取：
- 城通网盘链接（格式：`https://url89.ctfile.com/f/{userid}-{fileid}-{hash}?pwd=XXXX`）
- 提取码（通常是 `8866`）

## Step 3: 浏览器自动解密城通网盘

用 browser_action 工具完成城通网盘的密码验证流程：

```
1. navigate 到城通网盘链接（会重定向到 z701.com）
2. snapshot 获取页面元素
3. fill 密码输入框 + click "解密文件"按钮 + wait 5秒
4. snapshot 确认解密成功（看到"立即下载"按钮）
```

## Step 4: 调用API获取真实下载URL

解密成功后，通过 JavaScript 获取页面变量并调用城通网盘 API：

**获取变量：**
```javascript
JSON.stringify({
  api_server: api_server,   // "https://webapi.ctfile.com"
  userid: userid,
  file_id: file_id,
  share_id: share_id,       // 通常为空
  file_chk: file_chk,
  start_time: start_time,
  wait_seconds: wait_seconds,
  verifycode: verifycode
})
```

**调用下载API（必须用 async IIFE 包裹）：**
```javascript
(async () => {
  try {
    var url = api_server + '/get_file_url.php?uid=' + userid
      + '&fid=' + file_id + '&folder_id=0&share_id=' + share_id
      + '&file_chk=' + file_chk + '&start_time=' + start_time
      + '&wait_seconds=' + wait_seconds + '&mb=0&app=0&acheck=0'
      + '&verifycode=' + verifycode + '&rd=' + Math.random();
    var headers = typeof getAjaxHeaders === 'function' ? getAjaxHeaders() : {};
    var resp = await fetch(url, {headers: headers});
    var data = await resp.json();
    return JSON.stringify(data);
  } catch(e) { return 'Error: ' + e.message; }
})()
```

API 返回 `code: 200` 时，`downurl` 字段即为真实下载地址，`file_size` 为文件大小（字节）。

## Step 5: curl 下载文件

```bash
cd ~/Desktop && curl -L -o "书名.zip" "<downurl>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://z701.com/" \
  --max-time 600
```

注意事项：
- 文件较大时（>8MB），用后台模式运行 curl，然后轮询检查文件大小直到与 `file_size` 一致
- 下载完成后用 `file` 命令验证是否为有效 Zip 文件

## Step 6: Python 解压（处理中文编码）

城通网盘的 zip 文件名使用 GBK 编码，macOS 的 `unzip` 会乱码。必须用 Python 解压：

```python
import zipfile, os

outdir = '书名'
os.makedirs(outdir, exist_ok=True)

with zipfile.ZipFile('书名.zip', 'r') as z:
    for info in z.infolist():
        try:
            name = info.filename.encode('cp437').decode('gbk')
        except:
            name = info.filename
        basename = os.path.basename(name)
        if not basename:
            continue
        ext = os.path.splitext(basename)[1].lower()
        if ext in ('.epub', '.azw3', '.mobi', '.pdf', '.txt'):
            outpath = os.path.join(outdir, basename)
            data = z.read(info.filename)
            with open(outpath, 'wb') as f:
                f.write(data)
            print(f'Extracted: {outpath} ({len(data)} bytes)')

print('Done!')
```

## Step 7: 清理并报告

- 删除 zip 文件：`rm 书名.zip`
- 用 `ls -lh` 列出解压后的文件
- 向用户报告下载结果，说明每种格式的用途：
  - **EPUB**: 适合大多数电子书阅读器和手机 App
  - **AZW3**: 适合 Kindle 设备
  - **MOBI**: 适合旧版 Kindle 或其他兼容设备

## 备选下载源

如果读书派没有资源，按以下优先级尝试：

1. **sobooks.cc** — 搜索书名，找城通网盘链接
2. **wxbooks.com** — 类似流程
3. **Z-Library** (zh.z-library.sk) — 需要登录，作为最后手段

## 常见问题处理

| 问题 | 解决方案 |
|------|----------|
| curl 超时 | 用后台模式 `is_background: true`，轮询文件大小 |
| 城通网盘链接 404 | 链接可能过期，重新从读书派获取 |
| zip 文件名乱码 | 必须用 Python + cp437→gbk 解码，不要用 unzip |
| API 返回非 200 | 可能需要等待，检查 wait_seconds 字段 |
| evaluate 中 await 报错 | 必须用 `(async () => { ... })()` 包裹 |
| 下载的是 HTML 而非 zip | 说明拿到的是中间页面，需要通过浏览器+API获取真实链接 |
