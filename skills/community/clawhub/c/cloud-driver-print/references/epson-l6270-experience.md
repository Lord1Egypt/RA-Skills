# EPSON L6270 Series 接入参考

> 完整记录 EPSON L6270 Series 打印机的发现、识别、驱动匹配与打印实战。

## 基本信息

| 项目 | 值 |
|------|-----|
| 型号 | EPSON L6270 Series |
| 类型 | 墨仓式彩色喷墨一体机 |
| 色彩 | 4色 (CMYK: Black/Cyan/Magenta/Yellow) |
| 双面 | 支持（长边/短边翻转） |
| 速度 | 黑白 13ppm / 彩色 7ppm |
| 最高分辨率 | 4800×1200 dpi |
| 支持纸张 | A4/A5/A6, Letter, Legal, 4×6, 5×7, 信封等 |
| 自有协议 | ESC/P-R (application/vnd.epson.escpr) |

## IPP 探测（首选识别方式）

EPSON L6270 的 `discover.py --ip` 直接探测返回型号为 `-`，需用 IPP 获取：

```bash
ipptool -tv http://192.168.66.139:631/ipp/print get-printer-attributes.test
```

### 关键 IPP 字段

```text
printer-make-and-model        = EPSON L6270 Series
printer-device-id             = MFG:EPSON;MDL:L6270 Series;CMD:ESCPL2,...
printer-info                  = EPSON L6270 Series
marker-names                  = Black ink, Cyan ink, Magenta ink, Yellow ink
marker-levels                 = 8, 47, 60, 69  (当前墨量 %)
marker-low-levels             = 15, 15, 15, 15
pages-per-minute              = 13
pages-per-minute-color        = 7
sides-supported               = one-sided, two-sided-short-edge, two-sided-long-edge
print-color-mode-supported    = color, monochrome, auto-monochrome, process-monochrome, auto
```

### 快速提取命令

```bash
ipptool -tv http://192.168.66.139:631/ipp/print get-printer-attributes.test 2>/dev/null \
  | grep -E 'printer-make-and-model|printer-info|marker-names|marker-levels|pages-per-minute|sides-supported|print-color-mode'
```

## 驱动匹配

```bash
python search_driver.py "EPSON L6270 Series" --ip 192.168.66.139 --pick 1 --json
```

结果：精确匹配 `EPSON L6270 Series`，score=1.0，已安装。

## 已知问题

### 1. _pfs 渲染 0 字节（间歇性）

首次/冷启动时 `_pfs` 可能返回空数据。详见 `references/pfs-empty-fileurl-debug.md`。

**规律**：重试 2-4 次后正常（推测驱动预热）。成功的 fileUrl 以 `//0` 结尾。

### 2. _cvturl 超时

DOCX → PDF 云端转换持续超时 60s，自动降级 LibreOffice 本地转换，不影响打印。

### 3. 打印机断连

收到非预期数据（如裸发 PDF 到 9100）后，打印机可能短暂断网（ping 100% 丢包，数分钟恢复）。

### 4. 墨量偏低提醒

黑色墨量仅 8%（低于 15% 低墨警告阈值），建议备墨。

## 打印命令模板

```bash
# 基础打印
python print_file_for_skill.py file.docx \
  --ip 192.168.66.139 \
  --driver "EPSON L6270 Series" \
  --no-config-prompt --json

# 彩色双面 2 份
CDF_PRINT_CONFIG_JSON='{"copies":2,"color":"COLOR","sides":"two-sided-long-edge"}' \
  python print_file_for_skill.py file.docx \
  --ip 192.168.66.139 \
  --driver "EPSON L6270 Series" \
  --no-config-prompt --json
```
