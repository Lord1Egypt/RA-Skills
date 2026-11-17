# doc-holmes

[![GitHub Stars](https://img.shields.io/github/stars/docsor1212/doc-holmes?style=social&label=Star)](https://github.com/docsor1212/doc-holmes/stargazers)

保持原文排版的外文 PDF 精准翻译（triage A/B/C 分级 + BabelDOC 子进程引擎）。MIT 自有代码；AGPL 引擎（pdf2zh-next）只以子进程调用，零 vendor、零改源。

**China mirror (ModelScope 魔搭)**: <https://modelscope.cn/skills/Docsor/doc-holmes> — if you find this skill useful, a like there helps others find it.

## 开发

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python pymupdf pytest pytest-timeout
.venv/bin/python -m pytest tests/ -q          # 全套离线测试（桩引擎，数随版本增长）
.venv/bin/python -m pytest tests/ -q -k net   # 真网用例需 DOC_HOLMES_NET_TESTS=1
```

- 开发树：`src/doc_holmes/`；打包视图：`scripts/doc_holmes/`（由 `pkg` 阶段从 src 同步，断言一致）。
- 语料：`corpus/`（manifest 入库，PDF 本体 gitignore）。
- 宪章（不可违背）：**不内置任何端点/密钥，用户自带**；Coding Plan 订阅端点对分发默认拒绝（防用户封号；开发者自用需显式解锁）、AGPL 零 vendor 零改源、密钥全 env、C 级强制预览质量标注、每版发布前回归必跑。见 `plan.md` §0。

## 打包与发布

打包视图生成：`rsync -a --delete src/doc_holmes/ scripts/doc_holmes/`，随后跑五断言（双目录 pkg 脚本内嵌）。发布链走 SkillHub（中文包 SKILL_ZH.md）+ ClawHub（英文包 SKILL.md）双目录隔离。
