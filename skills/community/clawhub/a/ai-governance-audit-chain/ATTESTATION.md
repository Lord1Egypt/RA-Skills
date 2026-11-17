# 权属证明（ATTESTATION）

- 作品：AI 留痕与门禁（ai-governance-audit-chain）v1.1.0
- 署名：诺衡(Krites)@SynomosAI
- 版权：© 2026 赵兴华 / Steven Zhao·China（ORCID 0009-0001-0512-1237）
- 打包时间（UTC）：2026-11-06T07:47:24Z
- 打包时间（本地）：2026-11-06 15:47:24 +0800
- 文件数：8
- 内容合成指纹（SHA-256）：`85d98efe1858cb73e1cd530b2e63590207e491ddbe1ac48203839725f6ee5692`

## 指纹算法

对包内除 `ATTESTATION.md` 与 `manifest.json` 外的全部文件，按路径字典序取其 SHA-256，拼接为一个字符串后再取一次 SHA-256。任一文件被篡改，该指纹即变，可作为「在先发表」与「内容完整性」的举证依据。

复算方法（任何人可独立执行）：

```bash
python -c "import hashlib,os;fs=[];[fs.append(hashlib.sha256(open(os.path.join(dp,fn),'rb').read()).hexdigest()) for dp,dn,fns in os.walk('.') for fn in sorted(fns) if fn not in ('ATTESTATION.md','manifest.json')];print(hashlib.sha256(''.join(sorted(fs)).encode()).hexdigest())"
```

## 文件清单与逐文件指纹

| 文件 | SHA-256（前16位） | 字节 |
|---|---|---|
| LICENSE.md | caafb733bbceaaeb | 1908 |
| README.md | f772ab43316be752 | 2998 |
| SKILL.md | 79427b759e570bc1 | 11989 |
| references/01-证据链模板.md | a21b5437c6d98fd2 | 3032 |
| references/02-门禁清单.md | 2932e04bfef56707 | 3494 |
| references/03-反例与边界.md | 2b8d5e45738cf33e | 3816 |
| references/04-项目治理骨架.md | 57da7b23bcb805d9 | 3430 |
| scripts/audit_chain.py | 56b7daa0e226a4f6 | 13841 |

## 声明

本文件为作品权属与时间戳证据，随包分发。内容为作者原创；理论与方法论文本保留所有权利（详见 LICENSE.md 分层许可说明）。本包不构成法律意见，不替代任何第三方认证。

## 版本演进

| 版本 | 日期 | 变化 |
|---|---|---|
| 1.0.1 | 2026-08-28 | 初始版本，理论框架与授权声明（无执行层） |
| 1.1.0 | 2026-11-06 | 补齐执行层：证据链引擎脚本 + 4 份 references + 中文展示名与英文标签修复 |
