---
name: target-demo
slug: cue-target-demo
version: "0.1.0"
summary: "合成靶件：给体检流程做离线演示用，不属于任何真包。"
description: "合成靶件（虚构）。面文里刻意留一处声明与实做不一致：frontmatter 写了 bins 却没写 recommendedSkills，而正文那条命令引用了通道腿。"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
inputs:
  - user-material
produces:
  - text-draft
---

# target-demo（合成靶）

正文第一步：跑 `python3 -B scripts/demo.py --selftest`，末行自报断言数。
取证那一腿：`cue-research`（本包面文里说它可选）。
