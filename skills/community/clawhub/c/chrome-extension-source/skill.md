---
name: chrome-extension-source
description: 从 Chrome Web Store 扩展页面 URL 提取并解包扩展完整源码(CRX3)。适用输入:chromewebstore.google.com/detail/... 的链接;产出:可读的源码目录。含直连/本地代理/镜像三级下载策略。
---

# 提取 Chrome 扩展源码(从 Web Store URL)

原理:商店 URL `...detail/<名称>/<32位扩展ID>` 中的 ID 即 CRX 包密钥。Google 更新服务无条件返回任意扩展的完整 CRX 包;CRX3 签名头仅用于安装校验,**净载荷是未加密的标准 ZIP**。

## Step 1 — 提取扩展 ID

从 URL 中取最后一段 32 字符、全部落在 `a-p` 的小写串:

```
https://chromewebstore.google.com/detail/retrobrowser+/bfnjglgpfagpjodchbnolljodolgalpf
                                        └────── 扩展 ID ──────┘
```

```bash
EXT_ID=$(echo "$URL" | grep -oE '[a-p]{32}$')
```

## Step 2 — 下载 CRX(三级策略,按序尝试)

### 2a. 直连(官方端点,首选)

```bash
curl -sL -o ext.crx \
  "https://clients2.google.com/service/update2/crx?response=redirect&os=win&arch=x86-64&os_arch=x86-64&nacl_arch=x86-64&prod=chromiumcrx&prodchannel=unknown&prodversion=131.0.0.0&acceptformat=crx2,crx3&x=id%3D${EXT_ID}%26uc"
```

`x` 参数 = URL 编码的 `id=<ID>&uc`。`prodversion` 给一个较新的 Chrome 版本号即可。

### 2b. 本地代理(直连超时/000 时)

1. 找代理:先查环境变量 `HTTP(S)_PROXY`;再查 Windows 注册表:

```bash
powershell.exe -NoProfile -Command "(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings').ProxyServer"
```

2. 验证可用(HTTP 与 SOCKS5 常见同端口双协议):

```bash
curl -s --max-time 15 -x http://HOST:PORT -o /dev/null -w "%{http_code}\n" https://www.google.com/generate_204   # 期望 204
```

3. 在原命令追加 `-x http://HOST:PORT` 重新下载。

### 2c. 镜像站(无代理时)

```bash
curl -sL "https://www.crxsoso.com/file/download/${EXT_ID}" -o ext.crx
```

注意:镜像可能返回 HTML 而非 CRX(需登录/CDN 防护)。**必须校验魔数**后再进 Step 3。

### 下载结果校验(必做)

```bash
head -c 4 ext.crx        # 必须是 "Cr24";出现 "<!d" 则拿到的是 HTML,换策略
ls -la ext.crx           # 体积应与扩展规模相称(几百 KB ~ 几十 MB)
```

## Step 3 — 剥离 CRX3 头并解包

CRX3 布局:魔数 `Cr24`(4B) + 版本号(4B) + 头长度(4B) + protobuf 头 + ZIP 净载荷。

```bash
python -c "
import struct, pathlib
d = pathlib.Path('ext.crx').read_bytes()
assert d[:4] == b'Cr24'
ver, hlen = struct.unpack('<II', d[4:12])
pathlib.Path('ext.zip').write_bytes(d[12+hlen:])
"
mkdir src && unzip -q ext.zip -d src
```

## Step 4 — 验证解包完整性

```bash
cat src/manifest.json | python -m json.tool | head -20   # 名称/版本/权限
find src -type f | wc -l
```

失败特征:`manifest.json` 缺失或体积异常小 → 下载不完整,回到 Step 2 换策略。

## 常见陷阱

- **Google 全域不通 ≠ 代理不可用**:先测 `google.com/generate_204`(204=通),`clients2.google.com` 与 `clients2.googleusercontent.com`(重定向终点)都要通。
- **镜像 HTML 伪装**:crxsoso 在未登录时返回详情页 HTML,魔数校验是唯一可靠判据。
- **无代理且镜像失败**:GitHub raw 等源码镜像(gitclone/ghfast.top 系)仅当扩展开源时有效,先 web_search 确认是否有官方仓库——开源仓库通常比 CRX 更新、带构建脚本。
- **`file://` 陷阱(分析侧)**:解包后的源码若要运行验证,`crypto.subtle`/AudioWorklet 等要求 secure context,用 `python -m http.server` 起本地服务。

## 合规边界

商店扩展源码不加密、可完整提取是公开事实;仅限用于审计、学习、互操作性分析。有知识产权顾虑的作者靠包内 license 校验保护,而非包本身。
