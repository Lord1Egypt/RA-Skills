# outputs 目录

本目录存放财报深度解读助手生成的报告文件。

## 文件命名规则

- HTML 报告：`<公司名>_<报告期>_财报解读.html`
- 数据 JSON：`<公司名>_<报告期>_data.json`

## 说明

- 报告为自包含 HTML（内联 CSS，零外链，离线可开）。
- 每份报告生成后须通过硬闸 `scripts/earnings_lint.py` 校验（退出码 0 或 1）。
- 本目录下的文件可被 `publish_artifact` 发布交付。
