---
name: cloud-driver-print
description: 用于局域网打印机场景的客户端技能。打印 DOCX/EXCEL/PPT/PDF/图片等类型文件 到网络打印机（9100端口），支持发现、驱动搜索、云端上传、云端转打印数据并通过 9100 下发。Agent 自动化场景下一行命令搞定。
version: 1.0.3
category: print
author: webprinter
tags: [print, driver]
---

# cloud-driver-print

---

## 🔥 Agent 自动化打印 — 一步到位（先看这里）

**最常见场景：用户说"打印这个文件到施乐/某打印机，打N份"。**

Agent 在非交互环境下，必须带齐所有参数一步执行，脚本有 `input()` 的地方会 EOF 报错。

### 标准命令（直接复制改参数）

```bash
# === DOCX/PDF 统一入口：DOCX 自动走 _cvturl，超时自动降级 LibreOffice ===
CDF_PRINT_CONFIG_JSON='{"copies":2}' \
  python print_file_for_skill.py /path/to/file.docx \
    --ip 192.168.x.x \
    --driver "Xerox WorkCentre 7835" \
    --no-config-prompt \
    --json
```

> `print_file_for_skill.py` 内置降级：`_cvturl`（60s 超时）→ 失败自动 LibreOffice 本地转 PDF 重新上传。

**参数速查：**
| 场景 | 必带 flag |
|------|----------|
| 非交互环境 | `--no-config-prompt --json` |
| 指定份数 | `CDF_PRINT_CONFIG_JSON='{"copies":N}'` |
| 黑白/彩打 | `CDF_PRINT_CONFIG_JSON='{"color":"MONOCHROME"}'` | COLOR / MONOCHROME |
| 单双面 | `CDF_PRINT_CONFIG_JSON='{"side":"DUPLEX"}'` | ONESIDE / DUPLEX / TUMBLE |
| A3/A4 纸张 | `CDF_PRINT_CONFIG_JSON='{"paperConfig":{"name":"A4","width":210,"height":297}}'` |
| 驱动未保存 | `search_driver.py "型号" --ip 192.168.x.x --pick 1 --json` |
| IP 未登记 | `discover.py --ip 192.168.x.x` |

---

## ⚡ 三步流程（决策树）

```
用户说"打印" 
  ├─ 打印机已知？─否→ discover.py --list 或 --ip 登记
  │     └─ 型号为 "-"？→ ipptool 探测型号（详见故障降级 §4）
  ├─ 驱动已保存？─否→ search_driver.py --pick 1 --json 自动选
  └─ print_file_for_skill.py 文件 --ip ... --driver ... --no-config-prompt --json
```

> **流程内置降级：`_cvturl`（60s 超时）→ 失败自动 LibreOffice 本地转换 + 重新上传。无需手动干预。**
>
> **型号探测参考：** `references/printer-identification-ipptool.md` — EPSON L6270 完整识别案例。

---

## 📋 常用命令

### 打印机管理
```bash
python discover.py --timeout 5          # 扫描局域网打印机
python discover.py --list               # 列出已保存打印机
python discover.py --ip 192.168.1.25    # 按 IP 登记单台
python connect_printer.py 192.168.1.25  # 测试 9100 连通性
```

### 驱动搜索（非交互用 --pick）
```bash
python search_driver.py "Xerox WorkCentre 7835"                      # 只搜索
python search_driver.py --ip 192.168.65.130 --pick 1 --json          # 自动选第一个并回写
python search_driver.py "HP M404" --ip 192.168.1.25 --pick 1 --json  # 指定查询词+自动选
```

### 打印
```bash
# DOCX/PDF 一把梭（内置转换降级）
python print_file_for_skill.py file.docx --ip 192.168.x.x --driver "..." --no-config-prompt --json
```

---

## 🌐 云端 API 规范

云端服务：`https://any.webprinter.cn`

| 函数 | 路径 | HTTP | Content-Type | 超时 |
|------|------|------|-------------|------|
| `uploadFileMCP` | `/openapi/mcpClient/uploadFileMCP` | POST | `multipart/form-data` | 120s |
| `convert_url_to_pdf` | `/openapi/cdf/_cvturl` | POST | **`application/json`** | 60s |
| `print_for_skill` | `/openapi/cdf/_pfs` | POST | **`application/json`** | 300s |

**Headers（所有接口）：** `Accept: application/json`, `tid: cdf_ai_terminal`, `ttp: AI`

### ⚠️ 陷阱：form-encoded → 404

`_cvturl` 和 `_pfs` 用 form-encoded（`application/x-www-form-urlencoded`）会返回 **HTTP 404**，但换 JSON body 后正常。这是路由不匹配，不是接口未部署。代码中这两个函数已使用 `_post_json()`。

### curl 调试

```bash
# _pfs（JSON body，含 fileName 原始文件名）
curl -s -X POST "https://any.webprinter.cn/openapi/cdf/_pfs" \
  -H "Content-Type: application/json" -H "tid:cdf_ai_terminal" -H "ttp:AI" \
  -d '{"printer":{"driver":"Xerox WorkCentre 7835","name":"Xerox WorkCentre 7835","portType":"NET","portAddr":"192.168.65.130"},"url":"...PDF_URL...","fileName":"新建 DOCX 文档.docx","config":{"copies":2}}'

# _cvturl（JSON body）
curl -s -X POST "https://any.webprinter.cn/openapi/cdf/_cvturl" \
  -H "Content-Type: application/json" -H "tid:cdf_ai_terminal" -H "ttp:AI" \
  -d '{"repoId":"ZIM_STORAGE","path":"EeW88JMOkyAA1Qv5/..."}'
```

---

## 🚫 硬性约束

> **禁止将原始文件（PDF/DOCX/图片等）直接通过 TCP 9100 或其他端口发送到打印机。**
>
> 所有打印数据必须经过云端 `_pfs` 渲染管道生成，客户端只负责从 `_pfs` 返回的 `fileUrl` 下载二进制数据后发送到打印机 9100 端口。
>
> ❌ 禁止行为：
> ```python
> # NEVER do this — 直接发送原始文件
> s = socket.create_connection(('192.168.x.x', 9100))
> s.sendall(open('/tmp/file.pdf', 'rb').read())
> ```
>
> ✅ 正确流程：上传 → _cvturl 转换 → _pfs 渲染 → 下载 fileUrl 二进制 → 发送到打印机

---

## 🧯 故障降级

> **诊断参考文件：**
> - `references/pfs-empty-fileurl-debug.md` — `_pfs` fileUrl 返回 0 字节的完整复现与诊断（含间歇性规律和 fileUrl `//0` 格式线索）
> - `references/epson-l6270-experience.md` — EPSON L6270 Series 完整接入参考（发现、IPP识别、驱动、已知问题）
> - `references/printer-identification-ipptool.md` — IPP 探测打印机型号完整案例
> - `references/session-20260515-pfs-cvturl.md` — _cvturl 超时处理和接口规范

### 1. _cvturl 超时 → 内置自动降级
`print_file_for_skill.py` 已内置：`_cvturl` 失败后自动调用 LibreOffice 本地转 PDF 并重新上传，无需手动干预。

`_pfs` 成功后会返回 `fileUrl`。该 URL 指向二进制打印数据；`_pfs` 本身不实际触发打印，客户端需要下载该二进制内容并发送到目标打印机的 `9100`（或记录中的原始 TCP 端口）。

### 2. _pfs 返回 success 但 fileUrl 下载 0 字节 — 已确认真实故障

**现象：** `_pfs` 返回 `"success": true` + 有效 `fileUrl`，但从 fileUrl 下载得到 200 OK + **0 bytes**。`print_file_for_skill.py` 报错：`发送打印数据失败：下载到的打印数据为空。`

**根因：** 云端驱动渲染管道对特定 PDF 格式/打印机型号未能输出有效二进制数据。`_pfs` 本身调用成功（业务层面无错误），但渲染产物为空。此 Bug 已在 EPSON L6270 Series + fpdf2 生成的 PDF 上复现。

**诊断步骤：**
```bash
# 1. 直接调 _pfs 获取原始响应
curl -s -X POST "https://any.webprinter.cn/openapi/cdf/_pfs" \
  -H "Content-Type: application/json" -H "tid:cdf_ai_terminal" -H "ttp:AI" \
  -d '{"printer":{"driver":"EPSON L6270 Series","name":"EPSON L6270 Series","portType":"NET","portAddr":"192.168.66.139"},"url":"...PDF_URL...","config":{},"fileName":"test.pdf"}' \
  | python3 -m json.tool

# 2. 下载 fileUrl 验证大小
curl -s -o /tmp/pfs_dl.bin -w "HTTP %{http_code}, size: %{size_download}\n" \
  -H "tid:cdf_ai_terminal" -H "ttp:AI" "<_pfs返回的fileUrl>"
```

**处理方案：** `print_file_for_skill.py` 报错退出，需反馈给用户排查云端渲染管道（联系后端确认驱动/PDF兼容性）。**禁止绕过 _pfs 直接发送原始文件。**

### 3. search_driver.py EOF → 加 --pick
无 stdin 时交互式 `input()` 报 EOF，用 `--pick 1 --json` 自动选第一个候选。

### 4. 打印机型号无法识别 → ipptool 兜底

当 `discover.py --ip` 返回型号为 `-`（无法自动识别）时，按以下顺序探测：

| 优先级 | 方式 | 命令示例 | 成功率 |
|--------|------|---------|--------|
| ① | **IPP（最可靠）** | `ipptool -tv http://<IP>:631/ipp/print get-printer-attributes.test` | 极高 |
| ② | HTTP 首页 | `curl -s --max-time 5 http://<IP>/` | 中等 |
| ③ | SNMP | `snmpget -v2c -c public <IP> 1.3.6.1.2.1.25.3.2.1.3.1` | 低 |

**IPP 返回的关键字段：**
- `printer-make-and-model` → 精确型号（如 `EPSON L6270 Series`）
- `printer-device-id` → 含 MFG/MDL/CMD 等完整标识
- `printer-info` → 打印机友好名称
- `marker-levels` → 墨量/碳粉余量（单位 %）
- `pages-per-minute` / `pages-per-minute-color` → 打印速度

**典型用法：**
```bash
# 一步获取型号 + 墨量
ipptool -tv http://192.168.x.x:631/ipp/print get-printer-attributes.test 2>/dev/null \
  | grep -E 'printer-make-and-model|printer-info|marker-levels|marker-names|pages-per-minute'
```

> ⚠️ 有些打印机 IPP 监听在 80 端口而非 631，可尝试 `http://<IP>/ipp/print`。

---

## 🏗️ 架构

```
print_file_for_skill.py      ← 入口（上传+转换+下载打印数据+9100发送）
  ├── cdf/ai/skillPrint.py   ← REST 适配层 (uploadFileMCP / _cvturl / _pfs + fileUrl下载/9100发送)
  ├── cdf/ai/config.py       ← 服务地址 + headers 构建
  ├── cdf/ai/searchDriver.py ← 驱动搜索
  ├── printer_store.py       ← 本地 Markdown 打印机记录 (printers/*.md)
  └── driver_workflow.py     ← 驱动搜索→选择→回写 工作流

discover.py                  ← 网络发现 / IP登记 / 列表
connect_printer.py           ← TCP 9100 连通性检查
search_driver.py             ← 驱动搜索 CLI 入口
```

## 适配要求

1. `cdf/ai/` 下维护云端服务地址和 headers。
2. 所有打印请求带 `tid: cdf_ai_terminal` + `ttp: AI`。
3. 鉴权通过环境变量 `CDF_PRINT_API_KEY` 注入 Bearer Token（可选）。

## 依赖

- Python 3.10+
- `zeroconf`（mDNS 打印机发现，可选）
- **LibreOffice**（DOCX→PDF 本地转换降级，必需）
