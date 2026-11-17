# 文件夹整理器 / Directory Organizer

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `dir-organizer` v1.0.5 · LGD-Powered Utility Family · Zero-dependency

## English

One command for daily file chores: when the download folder holds hundreds of mixed files and finding anything means searching, sorting by hand is a drag — this tool does it in one command. Dry-run preview by default, `--apply` to actually execute, `--json` for machine-readable output. Success rc=0 / findings rc=1 / usage error rc=2.

### Usage
```bash
python scripts/dir_organizer.py --help
python scripts/dir_organizer.py            # preview (dry-run), nothing moves
python scripts/dir_organizer.py --apply    # perform the moves
python scripts/dir_organizer.py --json     # machine-readable report
```

It sorts by extension into images / docs / sheets / audio-video / archives / code / other subdirectories.

### Disclaimer
Efficiency aid only — back up important data before `--apply`.

## 中文

下载夹几百个文件混在一起，找东西全靠搜，归类又懒得手动拖——一条命令搞定；默认 dry-run 预览、`--apply` 才执行、`--json` 机器可读；成功 rc=0 / 发现问题 rc=1 / 用法错误 rc=2。

### 用法
```bash
python scripts/dir_organizer.py --help
python scripts/dir_organizer.py            # 预览（dry-run），不移动任何文件
python scripts/dir_organizer.py --apply  # 执行移动
python scripts/dir_organizer.py --json    # 机器可读报告
```

按扩展名归类到 图片 / 文档 / 表格 / 音视频 / 压缩包 / 代码 / 其他 子目录。

### 免责
效率辅助，`--apply` 前请备份重要数据。

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
