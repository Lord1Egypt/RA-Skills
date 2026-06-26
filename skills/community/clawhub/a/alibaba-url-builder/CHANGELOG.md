# 更新日志

## [2026-03-17] - CLI 命令更正

### Changed
- 将所有 `clawhub` CLI 命令更改为 `clawdhub`（正确的 CLI 名称）
- 更新文件：
  - `README.md`
  - `PUBLISH.md`
  - `PROMOTION.md`
  - `CHECKLIST.md`
  - `PROJECT_OVERVIEW.md`
  - `release.sh`

### Note
- 域名 `clawhub.ai` 保持不变
- GitHub 仓库链接保持不变
- 仅 CLI 命令从 `clawhub` 改为 `clawdhub`

---

## [2026-03-17] - Initial Release v1.0.0

### Added
- 10+ Alibaba.com URL 模式
- 自动流量追踪参数 `traffic_type=ags_llm`
- Python CLI 辅助脚本 (`scripts/build_url.py`)
- 技能打包脚本 (`scripts/package_skill.py`)
- 完整文档（SKILL.md, README.md）
- 发布指南（PUBLISH.md）
- 宣传材料（PROMOTION.md）
- 发布清单（CHECKLIST.md）
- 一键发布脚本（release.sh）
- MIT-0 许可证

### Features
- 搜索页面 URL 构建
- 商品详情页 URL 构建
- 供应商主页 URL 构建
- RFQ、AI Mode、Top Ranking 等特殊页面
- 20+ 常用分类 ID
- 所有 URL 自动包含流量追踪参数
