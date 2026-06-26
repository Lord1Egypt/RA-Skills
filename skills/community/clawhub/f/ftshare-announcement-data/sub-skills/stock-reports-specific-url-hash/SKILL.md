# 通过 url_hash 下载 A 股研报 PDF

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 按 url_hash 下载研报文件 |
| 外部接口 | 研报 PDF 下载（由 handler 请求并落盘） |
| 请求方式 | GET（脚本内部） |
| 适用场景 | 从研报列表中获取 url_hash 后，下载单条研报 PDF 到本地 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `url_hash` | string | 是 | 研报文件的 url_hash，从研报列表接口获取 | `abc123...` | - |
| `output` | string | 否 | 保存文件名 | `report.pdf` | 默认 {url_hash}.pdf |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-reports-specific-url-hash --url-hash <hash> --output report.pdf
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

脚本输出 JSON，表示文件已保存到本地：

```json
{
    "saved_to": "/path/to/report.pdf",
    "size_bytes": 123456
}
```

### 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `saved_to` | String | 否 | 文件保存的绝对路径 | - |
| `size_bytes` | int | 否 | 文件大小 | 字节 |

## 注意事项

- `url_hash` 需先通过 `stock-reports-all-stocks-specific-date` 或 `stock-reports-single-stock-all-periods` 获取
- 文件保存为 PDF 格式
