# 通过 url_hash 下载 A 股公告 PDF

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 按 url_hash 下载公告文件 |
| 外部接口 | 公告 PDF 下载（由 handler 请求并落盘） |
| 请求方式 | GET（脚本内部） |
| 适用场景 | 从公告列表中获取 url_hash 后，下载单条公告 PDF 到本地 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `url_hash` | string | 是 | 公告文件的 url_hash，从公告列表接口获取 | `169f21a0b04aa7291...` | - |
| `output` | string | 否 | 保存文件名 | `announcement.pdf` | 默认 {url_hash}.pdf |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-announcements-specific-url-hash --url-hash <hash> --output announcement.pdf
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

脚本输出 JSON，表示文件已保存到本地：

```json
{
    "saved_to": "/path/to/announcement.pdf",
    "size_bytes": 123456
}
```

### 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `saved_to` | String | 否 | 文件保存的绝对路径 | - |
| `size_bytes` | int | 否 | 文件大小 | 字节 |

## 注意事项

- `url_hash` 需先通过 `stock-announcements-all-stocks-specific-date` 或 `stock-announcements-single-stock-all-periods` 获取
- 文件保存为 PDF 格式
