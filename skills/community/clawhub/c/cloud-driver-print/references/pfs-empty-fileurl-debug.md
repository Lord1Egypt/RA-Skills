# _pfs fileUrl 0字节故障诊断记录

## 故障概述

云端 `_pfs` 对 EPSON L6270 Series 驱动渲染**间歇性**产出 0 字节打印数据。`_pfs` 本身返回 `success: true`，业务层无错误，但 `fileUrl` 下载内容为空。

## 复现场景 #1 — fpdf2 极简 PDF

| 项目 | 值 |
|------|-----|
| 打印机 | EPSON L6270 Series @ 192.168.66.139:9100 |
| 驱动 | EPSON L6270 Series（精确匹配，score=1.0） |
| 输入文件 | test_print.pdf（fpdf2 生成，1320 bytes，纯文字） |
| 上传 URL | `https://any.webprinter.cn/repoview/.../5a20ced198af4aeca4555a69da7e0c46.pdf` |
| 日期 | 2026-05-16 |
| 尝试次数 | 2次，均失败 |

### _pfs 响应（失败）

```json
{
  "reason": null,
  "success": true,
  "fileUrl": "https://any.webprinter.cn/repoview/.../cdf/92kylwdP-bfn8i8yqtkow/",
  "taskId": "92kylwdP-bfn8jfa0wfsw"
}
```

fileUrl 下载：**HTTP 200, size: 0 bytes**

---

## 复现场景 #2 — LibreOffice 生成 PDF（间歇性失败）

| 项目 | 值 |
|------|-----|
| 输入文件 | 新建DOCX文档.docx → LibreOffice 转 PDF（9357 bytes，2页） |
| 上传 URL | `.../420c6d01061a4ebab40673e48decf509.docx` → `.../00df49f9cd5c404395a401868712c240.pdf` |
| 日期 | 2026-05-16 |

### 失败模式（3次连续）

```json
// fileUrl 末尾是 "/" — 渲染产物为空
"fileUrl": "https://any.webprinter.cn/.../cdf/92kylwdP-bfn93qhucpvk/"
```
下载：**HTTP 200, size: 0 bytes**

### 成功模式（第4次）

```json
// fileUrl 末尾是 "//0" — 渲染成功！
"fileUrl": "https://any.webprinter.cn/.../cdf/92kylwdP-bfn9ttmtjdhc//0"
"rawPrint": { "bytes": 963212 }
```
下载：**HTTP 200, size: 963212 bytes** ✅

### 持续成功的后续请求

之后的所有打印（含 copies=2、彩色双面）均成功，fileUrl 均为 `//0` 结尾，数据量正常（1.7MB 左右）。

---

## 根因分析

1. **间歇性**：同一打印机、同一 PDF 内容，前 3-5 次 `_pfs` 失败 → 之后突然正常。排除 PDF 内容差异。
2. **fileUrl 格式差异是关键线索**：
   - 失败：`.../cdf/92kylwdP-bfn93qhucpvk/`（`/` 结尾）
   - 成功：`.../cdf/92kylwdP-bfn9ttmtjdhc//0`（`//0` 结尾，可能表示任务的第 0 个分片/产物）
3. **可能的根因**：云端渲染节点首次处理某打印机驱动时需要冷启动（加载驱动/预热），前几次请求触发渲染任务但未等到产物完成即返回 `fileUrl`。后续请求命中已预热的驱动缓存，正常产出。
4. **`_pfs` 接口行为**：`success: true` 仅表示请求被接受，不保证渲染产物非空。

## 诊断步骤

```bash
# 1. 直接调 _pfs 获取原始响应
curl -s -X POST "https://any.webprinter.cn/openapi/cdf/_pfs" \
  -H "Content-Type: application/json" -H "tid:cdf_ai_terminal" -H "ttp:AI" \
  -d '{"printer":{"driver":"EPSON L6270 Series","name":"EPSON L6270 Series","portType":"NET","portAddr":"192.168.66.139"},"url":"...PDF_URL...","config":{},"fileName":"test.pdf"}' \
  | python3 -m json.tool

# 2. 下载 fileUrl 验证大小
curl -s -o /tmp/pfs_dl.bin -w "HTTP %{http_code}, size: %{size_download}\n" \
  -H "tid:cdf_ai_terminal" -H "ttp:AI" "<_pfs返回的fileUrl>"

# 3. 检查 fileUrl 格式 — "//0" 结尾表示成功几率高，"/" 结尾可能为空
```

## 处理方案

`print_file_for_skill.py` 报错退出时，重试 2-3 次（云端驱动可能需要预热）。如果持续失败，反馈给用户排查云端 EPSON L6270 驱动渲染管道。

## 附加发现：_cvturl 超时

`_cvturl` 对 DOCX 文件持续超时（60s），自动降级 LibreOffice 本地转换。此问题可能与本会话的网络环境/文件大小相关，但不影响最终打印结果。LibreOffice 降级链路运行稳定。

## 附加发现：打印机断连

TCP 9100 裸发 PDF 到 EPSON L6270 后，打印机会短暂断网（ping 100% 丢包，所有端口不可达，约数分钟后恢复）。推测是打印机解析原始 PDF 导致网络栈锁定。**这是 skill 中禁止裸发的另一个原因。**
