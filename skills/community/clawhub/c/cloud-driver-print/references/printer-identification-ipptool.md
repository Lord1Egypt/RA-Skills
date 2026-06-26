# 打印机型号识别实战：EPSON L6270 Series

## 场景

`discover.py --ip 192.168.66.139` 返回型号为 `-`（无法自动识别）。

## 探测过程

| 方式 | 命令 | 结果 |
|------|------|------|
| SNMP | `snmpget -v2c -c public 192.168.66.139 1.3.6.1.2.1.25.3.2.1.3.1` | ❌ 无响应 |
| HTTP 首页 | `curl -s http://192.168.66.139/` | 🔸 仅获知 SEIKO EPSON，无型号 |
| **IPP** | `ipptool -tv http://192.168.66.139:631/ipp/print get-printer-attributes.test` | ✅ **完整识别** |

## IPP 返回关键字段（截取）

```
printer-info = EPSON L6270 Series
printer-make-and-model = EPSON L6270 Series
printer-device-id = MFG:EPSON;CMD:ESCPL2,...,URF;MDL:L6270 Series;...
pages-per-minute = 13
pages-per-minute-color = 7
color-supported = true
sides-supported = one-sided,two-sided-short-edge,two-sided-long-edge
marker-names = Black ink, Cyan ink, Magenta ink, Yellow ink
marker-levels = 8, 47, 60, 69
```

## 获得的信息

- **型号**：EPSON L6270 Series（墨仓式喷墨）
- **色彩**：支持彩色（4色 CMYK）
- **速度**：黑白 13ppm / 彩色 7ppm
- **双面**：支持
- **墨量**：黑 8%（低）、青 47%、洋红 60%、黄 69%
- **分辨率**：最高 4800×1200 dpi
- **驱动**：`search_driver.py "EPSON L6270 Series"` 精确匹配 score=1.0

## 结论

IPP 是最可靠的打印机型号识别方式。即使在 SNMP 禁用、Web 界面需要 JS 的情况下，IPP（631 端口）通常都是可用的，且返回完整设备信息。
