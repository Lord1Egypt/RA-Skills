---
name: file-integrity
description: 文件拷贝或下载后自动进行 MD5/SHA 校验，保证完整性。覆盖：算哈希、复制后校验、下载后校验、生成/核对校验清单（兼容 GNU md5sum / BSD 格式）。当用户提到"下载后校验、md5 校验、checksum、校验和、文件完整性、哈希对比、sha256 校验"等需求时使用。纯 Python 标准库实现，无第三方依赖。
---

# File Integrity - 文件完整性校验

核心脚本：`scripts/verify.py`（纯标准库，Windows/macOS/Linux 通用，支持大文件分块读取）。

运行方式（用绝对路径最稳妥）：

```bash
python "C:/Users/chengzhenyang/.workbuddy/skills/file-integrity/scripts/verify.py" <子命令> [参数]
```

若脚本路径不同，以本文件所在目录下的 `scripts/verify.py` 为准。

## 六个子命令速查

| 子命令 | 用途 | 退出码语义 |
|---|---|---|
| `hash` | 计算单文件哈希 | 0 成功 / 2 IO 错误 |
| `verify <file> <expected>` | 单文件校验比对 | 0 通过 / 1 不符 / 2 错误 |
| `copy <src> <dst>` | 复制 + 复制后双向校验 | 同上 |
| `download <url> <dst>` | 下载 + 可选期望哈希校验 | 同上 |
| `record <dir>` | 生成目录校验清单 | 0 成功 |
| `check <dir> -c manifest` | 按清单批量校验 | 0 全通过 / 1 有缺失或不符 |

所有子命令支持 `--json`（`check`、`record` 也支持）；`--algo` 可选 `md5 sha1 sha256 sha512 sha3-256 blake2b`，除 `record` 外默认 `sha256`（`record` 默认 `md5`，与常见 `.md5` 清单习惯一致）。

## 典型场景

### 1. 下载文件后校验（官方给了 md5）

```bash
python .../verify.py download "https://example.com/tool.zip" ./tool.zip \
  --expected "5d41402abc4b2a76b9719d911017c592" --algo md5
```

- 哈希一致才落到正式路径；不一致时保留 `*.part-<时间戳>` 副本供排查，退出码 1。
- 未提供 `--expected` 时仍会算好哈希并输出，供人工比对。

### 2. 拷贝文件后校验（防 U 盘/网络盘拷坏）

```bash
python .../verify.py copy "D:/data.iso" "E:/backup/data.iso" --algo sha256
```

复制完成后自动对源和目标各算一次哈希并比对，不一致时保留损坏副本并报 FAIL。

### 3. 大批量校验（下载了一堆文件、备份还原后核对）

先在源端生成清单：

```bash
python .../verify.py record ./dataset -o ./dataset.md5          # 默认 md5
python .../verify.py record ./dataset -o ./dataset.sha256 --algo sha256
```

清单格式：`md5: <hash>  <相对路径>`，一行一个文件。

到目标端核对（自动跳过清单文件自身、拒绝路径越界）：

```bash
python .../verify.py check ./dataset -c ./dataset.md5
```

`check` 兼容 GNU `md5sum -c` 风格清单（`<hash>  <path>`，按长度识别算法）和 BSD 风格（`MD5 (file) = hash`），所以也能核对 `md5sum` / `certutil -hashfile` 生态产出的清单。

## 输出与判定约定

- 人类可读输出：`[OK]` / `[FAIL]` / `[MISS]` / `[ERROR]` 前缀。
- 期望哈希支持 hex（32/40/64/128 位按长度自动识别算法）或 BASE64 编码，`verify`/`download`/`check` 会自动归一化为小写 hex 再比对。
- **不要**凭 stdout 文本判断成败——用退出码：`0` 通过、`1` 校验不符、`2` 参数/IO 错误。

## 安全边界

- `copy` 拒绝源/目标互相嵌套的路径；`check` 拒绝清单中跳出根目录的路径（防恶意清单）。
- 校验失败时**不删除**任何文件（保留损坏副本/`.part` 文件供排查），由用户决定后续处理。
- 清单生成时排除 `.git`、`__pycache__` 目录。
