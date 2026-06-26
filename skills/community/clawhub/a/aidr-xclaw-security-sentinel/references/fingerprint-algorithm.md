# 指纹算法参考

> 本文件为详细规范参考，Agent 无需主动加载。仅当需要调试指纹计算或理解算法时参考。
>
> **何时读：** 指纹计算结果异常、需要修改算法、注册表调试时。
> **何时略过：** 正常执行 Skill Audit 时。

---

## 算法概览

在 Skill 目录内执行，使用 OpenSSL 纯 shell 命令。算法分为 L1 → L2 → L3 → Final 四层。

### L1 — 文件级指纹

遍历 Skill 目录内所有文件，输出每行的格式为 `路径:HASH`，按路径排序：

```bash
find . -type f \
  ! -path './.git/*' \
  ! -path './node_modules/*' \
  -printf '%P\n' | sort \
  | while read -r f; do
      hash=$(openssl dgst -sha256 "$f" | cut -d' ' -f2)
      echo "$f:$hash"
    done
```

### L2 — 内容级指纹

将所有文件的 SHA-256 哈希排序后拼接，再做一次 SHA-256：

```bash
find . -type f \
  ! -path './.git/*' \
  ! -path './node_modules/*' \
  -exec openssl dgst -sha256 {} \; \
  | sort \
  | cut -d' ' -f2 \
  | tr -d '\n' \
  | openssl dgst -sha256 \
  | cut -d' ' -f2
```

### L3 — 元数据指纹

提取 `SKILL.md` frontmatter 中 `name` 和 `description` 字段，拼接后做 SHA-256：

```bash
sed -n '/^---$/,/^---$/p' SKILL.md \
  | sed '1d;$d' \
  | grep -E '^(name|description):' \
  | sort \
  | tr -d '\n' \
  | openssl dgst -sha256 \
  | cut -d' ' -f2
```

> 排序字段确保不同机器上结果一致。只取 `name` 和 `description` 是因为它们是 SKILL.md 中最稳定且最代表 Skill 身份的元数据。

### Final — 注册指纹

拼接 L2（不含换行）和 L3（不含换行），再做 SHA-256：

```bash
echo -n "${L2_HASH}${L3_HASH}" \
  | openssl dgst -sha256 \
  | cut -d' ' -f2
```

> `L2` 聚合了所有文件的内容指纹，`L3` 聚合了元数据指纹，二者拼接已足够唯一标识 Skill 的完整状态。

---

## 合并命令（一次性输出 L1/L2/L3/Final）

```bash
L1=$(find . -type f ! -path './.git/*' ! -path './node_modules/*' \
  -exec openssl dgst -sha256 {} \; | sort | cut -d' ' -f2 | tr -d '\n')
L2=$(echo -n "$L1" | openssl dgst -sha256 | cut -d' ' -f2)
L3=$(sed -n '/^---$/,/^---$/p' SKILL.md | sed '1d;$d' \
  | grep -E '^(name|description):' | sort | tr -d '\n' \
  | openssl dgst -sha256 | cut -d' ' -f2)
FINAL=$(echo -n "${L2}${L3}" | openssl dgst -sha256 | cut -d' ' -f2)

echo "L1: $L1"
echo "L2: $L2"
echo "L3: $L3"
echo "Final: $FINAL"
```

---

## 算法特性

| 特性 | 说明 |
|------|------|
| 单向性 | 给定指纹，无法反推原始文件内容（SHA-256 理论保证） |
| 唯一性 | 相同内容 → 相同指纹（确定性算法，无随机因素） |
| 碰撞抵抗 | 不同内容产生相同指纹的概率极低 |
| 可复现 | 相同内容版本在任何时间、任何设备上产生相同指纹 |

---

## 注册表写入格式

```json
{
  "skill_name": "<name from frontmatter>",
  "fingerprint": "<Final 指纹>",
  "L2_fingerprint": "<L2 指纹>",
  "L3_fingerprint": "<L3 指纹>",
  "registered_at": "<ISO8601>",
  "last_scan": "<ISO8601>",
  "scan_id": "<远端返回的scan_id>",
  "status": "approved|warn|quarantined|rejected",
  "score": <综合评分>
}
```
