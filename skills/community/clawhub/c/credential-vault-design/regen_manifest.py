#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regen_manifest.py — 为重发技能包重算 manifest.json + ATTESTATION.md（本地·无网络）"""
import hashlib, json, sys, datetime
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
SKILL_NAME = sys.argv[2] if len(sys.argv) > 2 else "统一凭据保险库"
VERSION = sys.argv[3] if len(sys.argv) > 3 else "2.0.0"

SKIP_DIRS = {"__pycache__", ".git", "_meta"}
SKIP_SUFFIX = {".tmp", ".pyc"}
files = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file():
        continue
    if any(part in SKIP_DIRS for part in p.parts):
        continue
    if p.suffix in SKIP_SUFFIX:
        continue
    rel = str(p.relative_to(ROOT)).replace("\\", "/")
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    files.append({"path": rel, "sha256": sha})

# 包指纹：按路径顺序拼接所有 sha256 后整体哈希
concat = "".join(f["sha256"] for f in files).encode()
fingerprint = hashlib.sha256(concat).hexdigest()

now = datetime.datetime.now(datetime.timezone.utc)
ts_utc = now.isoformat()
ts_local = now.astimezone().isoformat()

manifest = {
    "schema": "ownership-attestation/1.0",
    "package": SKILL_NAME,
    "version": VERSION,
    "author": "SynomosAI",
    "year": "2026",
    "timestamp_utc": ts_utc,
    "timestamp_local": ts_local,
    "package_fingerprint_sha256": fingerprint,
    "files": files,
}
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")

rows = "\n".join(f"| {f['path']} | {f['sha256']} |" for f in files)
attest = f"""# 权属证明与许可声明

> 本声明置于每个对外发布物的显著位置（SKILL.md 末尾 / 文档头部 / 包根）。
> 品牌署名统一用「SynomosAI」，不得出现个人真名、在职公司或内部路径。

## 1. 著作权 ©
© 2026 SynomosAI. 保留所有权利。
本作品（含软件代码与文档）的著作权归 SynomosAI 所有。

## 2. 知识版权声明
本作品所汇集的方法论、对比分析、结构化知识与合成内容（"知识内容"），
其编排与原创表达归 SynomosAI 所有。未经书面许可，不得复制、转载、摘编、转售，
或用于训练任何模型 / 商业系统。
（软件代码依随附 LICENSE 的许可条款使用；本知识版权声明不限制 LICENSE 已授予的权利。）

## 3. 免责声明（AS IS）
本作品按「现状」提供，不提供任何明示或暗示的担保，包括但不限于适销性、
特定用途适用性及非侵权担保。使用风险由使用者自行承担，因使用本作品所致
任何直接或间接损失，作者不承担责任。

## 4. 发布时间戳
- 发布时间（UTC）：{ts_utc}
- 发布时间（本地）：{ts_local}

## 5. 作品指纹（内容哈希）
- 包指纹 SHA-256：{fingerprint}
- 本指纹由发布包内全部文件的哈希按确定顺序合成，可作为该版本
  「于上述时间由 SynomosAI 发布」的完整性标识。篡改任一文件即导致指纹变化。
- 加强权属：可将本指纹锚定至可信时间戳服务（RFC3161 TSA）或区块链，
  形成不可抵赖的「在先发表」证据（该步骤需外部服务，须经确认后单独执行）。

## 附：文件清单与逐文件哈希
| 文件 | SHA-256 |
|---|---|
{rows}
"""
(ROOT / "ATTESTATION.md").write_text(attest, "utf-8")
print(f"✔ 已重算 {len(files)} 个文件；包指纹 {fingerprint[:16]}...")
print(f"  → {ROOT/'manifest.json'}  {ROOT/'ATTESTATION.md'}")
