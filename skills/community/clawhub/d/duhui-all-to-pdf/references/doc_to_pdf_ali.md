# 文档转PDF（阿里云市场，精简版）

本文件只保留当前 skill 实际使用的最小流程：

1. 调用 `v2/convert_async` 发起异步转换，拿到 `token`
2. 轮询查询接口，直到状态变为 `Done` 或 `Failed`

当前 skill 约束：

- 只走 `v2` 异步接口
- 只处理单个文件 URL 输入
- 本地文件会先上传到 OSS，再把 OSS 对象 URL 放进 `input`
- 认证方式使用 `Authorization: APPCODE <appcode>`
- 不涉及同步接口、回调、Base64 输入、多图输入

## 文档转换_v2（异步）

**URL**

```text
https://doc2pdf.market.alicloudapi.com/v2/convert_async
```

**Method**

```text
POST
```

**Headers**

```text
Content-Type: application/json
Authorization: APPCODE <appcode>
```

**最小请求体**

```json
{
  "input": ["https://fmtmp.oss-cn-shanghai.aliyuncs.com/up/example.docx"],
  "type": "docx"
}
```

**输入说明**

- `input`: 当前 skill 只传一个文件 URL
- `type`: 源文件扩展名；如果 URL 无法可靠体现类型，必须显式传

**v2 丰富参数速查**

当前 skill 只保留 `v2/convert_async` 主流程，但 `--extra-params` 可以透传丰富的 `v2` 字段。

**通用**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `type` | string | 源文件扩展名；当 URL 无法稳定体现后缀时应显式传 |

**输出 PDF 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `linearization` | int | 是否启用快速 web 显示，`0/1` |
| `compress` | int | PDF 压缩级别，`0` 不压缩，`1/2/3` 压缩率递增 |
| `flatten` | int | 是否扁平化，把注释等内容合并进 PDF，`0/1` |
| `imagepdf` | int | 是否输出图片型 PDF，`0/1` |
| `pagesize` | int | 页面大小，常见值：`1:A3` `2:A4` `3:A5` `4:B4` `5:B5` `6:Letter` `7:Legal` `8:Tabloid` `9:Ledger` |
| `adjustorientation` | int | 调整页面方向；常见值：`1/2` 调成竖屏，`3/4` 调成横屏 |
| `pageorientation` | int | 页面横竖方向；常见值：`1` 横向，`2` 纵向 |
| `pagesplit` | int | 按长边拆页，常见值：`2/3` |
| `needpagesizeinfo` | int | 是否返回每页尺寸信息，`0/1` |
| `pdffilename` | string | 服务端生成 PDF 的文件名 |

**Word / Excel / HTML / 文本相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `wordshowmarkup` | int | Word 是否显示审阅标记，`0/1` |
| `excelislandscape` | int | Excel 是否横向排版，`0/1` |
| `exceliscenter` | int | Excel 是否横竖居中，`0/1` |
| `excelmargin` | int | Excel 四边边距，单位像素 |
| `excelsheetindex` | int | 指定 Excel 转换的 Sheet；`0` 常表示全部 |
| `excelnotshowgridlines` | int | Excel 是否隐藏网格线，`0/1` |
| `exceluseprintarea` | int | Excel 是否使用打印区域 |
| `excelpagesize` | int | Excel 页面大小，取值体系与 `pagesize` 类似 |
| `htmloutline` | int | HTML 是否根据 `h1/h2/...` 生成 outline，`0/1` |

**PowerPoint 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `powerpointoutputtype` | int | PPT 输出样式；`0` 常表示幻灯片，`1-6` 为不同讲义模式 |
| `powerpointhandoutorder` | int | 讲义模式顺序；常见值：`0` 水平，`1` 垂直 |
| `powerpointhandoutorientation` | int | 讲义输出方向；常见值：`1` 横向，`2` 纵向 |

**图片 / OCR 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `ocr` | int | 是否启用 OCR，`0/1` |
| `deskew` | int | 是否矫正倾斜文字，`0/1` |
| `clean` | int | 是否清除图像背景只保留文字，`0/1` |
| `grayimage` | int | 是否转灰度图，`0/1` |
| `text` | int | OCR 后是否用矢量文字替换图片中文字，`0/1` |
| `split2p` | int | OCR 场景下横向图片是否拆成两页，`0/1` |
| `imagesize` | int | 统一每页宽度；设置后通常会覆盖部分页面尺寸行为 |
| `language` | int | OCR 识别语言，常见值：`1` 英语，`2` 简体中文，`3` 繁体中文，`8` 日文，`9` 韩文 |
| `dewarp` | int | 是否切边矫正，`0/1`；开启时通常要求一次只传一张图 |

**网页 URL 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `ismobileurl` | int | 当 `type=url/html/md` 时，是否按移动端网页抓取，`0/1` |
| `urldesktopwidth` | int | 当 `type=url/html/md` 时，桌面端网页最大宽度 |
| `htmlpagemargin` | string | 当 `type=url/html/md` 时，输出页面边距字符串 |
| `urlwait` | int | 当 `type=url` 时，抓取前额外等待的秒数 |
| `urltimeout` | int | 当 `type=url` 时，加载资源的超时时间 |
| `urlonepage` | int | 当 `type=url/html/md` 时，是否生成单页长 PDF，`0/1` |

**EPUB 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `epubfontsize` | int | EPUB 输出字体大小 |
| `epublineheight` | int | EPUB 输出行高百分比 |
| `epubpagesize` | string | EPUB 自定义页面大小；设置后通常会覆盖 `pagesize` |
| `epubmargin` | string | EPUB 输出页面边距 |

**密码 / 权限 / 水印**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `password` | string | 源文件密码，适用于有密码的 PDF/Word/PPT/Excel |
| `userpassword` | string | 打开生成 PDF 所需密码 |
| `ownerpassword` | string | 修改生成 PDF 所需密码 |
| `pdfrestriction` | string | PDF 权限，示例：`010` |
| `watermark` | string | 水印文本 |
| `watermarkfontsize` | int | 水印字体大小 |
| `watermarkfontcolor` | string | 水印颜色，通常是 7 位颜色码 |
| `watermarkfontalpha` | int | 水印透明度 |
| `watermarkstyle` | int | 水印样式；常见值：`0` 单个，`1` 铺满 |

**CAD 相关**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `cadlayer` | int | CAD 是否生成图层信息，`0/1` |
| `cadisdisplay` | int | CAD 是否按 Display 显示，`0/1` |
| `cadquality` | int | CAD 输出品质，常见范围 `1-5` |
| `caddetectempty` | int | CAD 是否删除空页，`0/1` |

**当前 skill 不允许通过 `--extra-params` 覆盖的字段**

- `input`
- `type`
- `callbackurl`

**支持的源格式（完整 v2 速查）**

| 类型 | 扩展名 / type 取值 | 备注 |
| --- | --- | --- |
| PDF 文件 | `pdf` | |
| 微软 Office 文档 | `doc`, `docx`, `ppt`, `pptx`, `xls`, `xlsx`, `pot`, `pps`, `ppsx`, `csv` | |
| WPS 文档 | `wps`, `wpt`, `dps`, `dpt`, `et`, `ett` | |
| 苹果 iWork 文档 | `pages`, `key`, `numbers` | |
| 开放版式文档 | `ofd` | |
| 电子刊物 | `caj`, `nh`, `kdh` | |
| 电子书 | `epub`, `chm`, `mobi`, `azw`, `azw3`, `fb2`, `cbr`, `cbz`, `djvu` | |
| Markdown | `md` | |
| SVG | `svg` | |
| CAD 文档 | `dwg`, `dxf`, `dwt`, `dws` | |
| Sketch 文档 | `sketch` | |
| 网页文件 | `html`, `htm`, `mht`, `eml` | |
| 图片文件 | 几乎所有图片格式，例如 `png`, `jpg`, `jpeg`, `gif`, `tif`, `tiff`, `bmp`, `webp`, `ai` | `type` 也可以统一传 `img` |
| 文本文件 | `txt`, `rtf`, `java`, `js`, `c`, `cpp`, `jsp`, `css`, `xml`, `properties`, `log` | `type` 也可以统一传 `txt` |
| 网址网页 | `url` | 例如 `https://www.duhuitech.com` |

**返回结构**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | number | `10000` 表示成功，其余表示失败 |
| `msg` | string | 错误信息或空字符串 |
| `result` | object | 成功时返回 |
| `result.token` | string | 后续查询结果要用的 token |

**返回示例**

```json
{
  "code": 10000,
  "msg": "",
  "result": {
    "token": "xxx"
  }
}
```

## 查询结果

**URL**

```text
https://api.duhuitech.com/q?token=xxx
```

**认证**

- 不需要签名
- 不需要 AppCode

**轮询规则**

- 建议每 `1-2` 秒查询一次
- 先看 `result.status`
- 如果是 `Done` 或 `Failed`，停止轮询
- 如果是 `Pending` 或 `Doing`，继续轮询

**返回结构**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | number | `10000` 表示请求成功 |
| `msg` | string | 错误信息或空字符串 |
| `token` | string | 查询的 token |
| `result.status` | string | `Pending` / `Doing` / `Done` / `Failed` |
| `result.progress` | number | 进度，`0.00 - 1.00`，仅 `Doing` 时常见 |
| `result.pdfurl` | string | 转换成功后的 PDF 下载地址 |
| `result.count` | integer | PDF 总页数 |
| `result.filesize` | integer | 输出文件大小 |
| `result.reason` | string | 失败原因 |

**状态示例**

```json
{
  "code": 10000,
  "msg": "",
  "token": "xxx",
  "result": {
    "progress": 0.02,
    "status": "Doing"
  }
}
```

```json
{
  "code": 10000,
  "msg": "",
  "token": "xxx",
  "result": {
    "status": "Done",
    "pdfurl": "https://file.duhuitech.com/o/xxx/xxx.pdf",
    "count": 10,
    "filesize": 17747
  }
}
```

```json
{
  "code": 10000,
  "msg": "",
  "token": "xxx",
  "result": {
    "status": "Failed",
    "reason": "转换失败原因"
  }
}
```

## 备注

- 文件 URL 方式最大支持约 `1500M`
- 最大转换时长约 `1 小时`
- 转换完成后，返回的下载链接有效期约 `1 小时`
