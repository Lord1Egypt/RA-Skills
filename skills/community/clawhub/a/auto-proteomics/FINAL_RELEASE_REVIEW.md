# Auto-Proteomics Final Release Review

English | 中文

## Candidate status

This repository is now close to the next public release candidate, but this file is a final review aid only.
No publish action has been executed from this document.

当前仓库已接近下一次公开发布候选状态，但本文件仅用于最终核对。
本文件不触发任何发布动作。

## Current public release boundary

Publicly shipped now:
- `dda-lfq-processed`
- processed DDA LFQ protein-level downstream analysis
- one clear two-group comparison path: `group-a` vs `group-b`

Visible but not publicly shipped:
- `dia-quant` - internal prototype only
- `dda-identification` - scaffold only
- `phospho-differential` - scaffold only
- enrichment execution - not shipped
- multi-omics execution - not shipped

## 当前公开边界

当前公开 shipped：
- `dda-lfq-processed`
- processed DDA LFQ 蛋白层级 downstream analysis
- 一条明确的双组比较路径：`group-a` vs `group-b`

当前保留可见但未公开交付：
- `dia-quant` - 仅 internal prototype
- `dda-identification` - 仅 scaffold
- `phospho-differential` - 仅 scaffold
- enrichment execution - 未 shipped
- multi-omics execution - 未 shipped

## Final pre-publish checks

1. Confirm public wording remains honest in:
   - `README.md`
   - `SKILL.md`
   - `RELEASE_SUMMARY.md`
   - `references/WORKFLOW_INDEX.yaml`
2. Confirm non-shipped branches are not described as public support.
3. Rebuild staged tree and package:

```bash
python3 scripts/release/stage_release.py && \
python3 scripts/release/build_skill_package.py && \
python3 scripts/release/check_public_package.py
```

4. Confirm package excludes:
   - `dist/`
   - `.git/`
   - `__pycache__/`
   - `*.pyc`
   - `examples/*/results/`
   - `mock`
   - `NEXT_STEPS.md`
   - `ROADMAP.md`
5. Spot-check routing:
   - processed DDA downstream -> public match
   - processed DIA quantification -> internal prototype only
6. Re-read release notes / summary and ensure they do not imply broader public proteomics support than the checked-in boundary.

## Practical publish decision

Ready for final human review before publish:
- package mechanics verified
- public surface tightened
- bilingual release summary prepared
- internal prototype branches remain visible but explicitly non-shipped

Not yet done:
- actual GitHub / ClawHub publish action
- final human wording approval

## Recommended next action

Use this file together with `RELEASE_SUMMARY.md` and `references/RELEASE_CHECKLIST.md` for the final release review pass.
