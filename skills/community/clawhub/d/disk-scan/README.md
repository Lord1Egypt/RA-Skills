# 磁盘占用扫描 / Disk Usage Scan

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `disk-scan` v1.0.5 · LGD-Powered Utility Family · Zero-dependency

## English

Disk full and you don't know what ate the space, with the file manager taking forever to show it — one command solves it. Read-only scan: Top-N largest files plus a per-subdirectory size ranking to locate space hogs quickly. rc=0 ok / rc=1 findings / rc=2 usage.

### Usage
```bash
python scripts/disk_scan.py --help
python scripts/disk_scan.py -p <dir> --top 100 --recursive
python scripts/disk_scan.py -p <dir> --json
```

### Disclaimer
Read-only probe — no files are changed. Still, back up important data before any cleanup you act on from the results.

## 中文

盘满了不知道谁吃的空间，资源管理器算半天还看不清——一条命令搞定；只读扫描：Top N 大文件 + 各子目录大小排行，快速定位空间杀手；成功 rc=0 / 发现问题 rc=1 / 用法错误 rc=2。

### 用法
```bash
python scripts/disk_scan.py --help
python scripts/disk_scan.py -p <目录> --top 100 --recursive
python scripts/disk_scan.py -p <目录> --json
```

### 免责
只读探查，不改动任何文件；依据结果执行清理前请备份重要数据。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
