# 各渠道输出格式合约

`validate_publish_output.py` 依据本文件逐渠道校验。P0 阻断发布，P1 提示人工决定。

## 微信（wechat_snippet.html）

- P0：文件不存在，或非 HTML 片段。
- P0：不含任何 `<section` 包裹块。
- P0：文末不含 `<v2></v2>`。
- P0：含 `<script` 或 `<style` 或 `position:fixed` / `position:absolute`。
- P0：含外联 `class="`（保留白名单：`class="_135editor"` 仅在通过 135 编辑器建稿时允许；可粘贴模式应无 class）。
- P0：未通过 `scripts/validate_wechat_layout.py` 的唯一基线校验（标题 23px、小标题 18px、正文 16px/1.8、颜色/间距/背景/结构任一漂移）。
- P1：正文段落未发现 `font-size:16px` 或 `line-height:1.8`（疑似未应用正文样式）。

## LinkedIn（linkedin-post.md）

- P0：文件不存在。
- P0：含 Markdown 标题 `#`、列表 `- `、`**` 加粗或反引号代码块（平台不支持格式化）。
- P0：含内部备注标记（如 `【内部】`、`内部备注`、`待定`、`Gate`、`审核过程`），或作者内部笔名/代号（发布物一律用真实姓名或中性表达，笔名清单由私有 profile 的 `pen_names` 提供）。
- P1：字符数 > 3000（LinkedIn 长文体验下降，建议压缩）。
- P1：末尾未出现任何 `#话题` 标签。

## 独立 HTML（standalone.html）

- P0：文件不存在，或不以 `<!DOCTYPE html>` / `<html` 开头。
- P0：不含 `<title` 或页面标题为空。
- P0：含科技电路风关键词（如 `circuit`、`grid-glow`、`neon`、`linear-gradient` 用于背景发光）。
- P1：不含目录（`<nav` 或 `id="toc"` 缺失）。

## 入库台账（archive-ledger.json）

- P0：JSON 解析失败。
- P0：最新一条记录缺必填字段：`title`、`channels`、`generated_at`、`status`。
- P1：`status` 取值不在 `[draft, published, archived]`。

## 项目归档排版

- P0（启用 `--require-root-layout` 时）：根目录 `篇名-排版-日期.html` 或 `篇名-排版-日期_snippet.html` 不存在。
- P0：根目录排版文件与发布目录 `wechat_preview.html` / `wechat_snippet.html` 内容不一致。

## 通用

- P0：任何渠道文件含对话痕迹（如 `好的，`、`我来`、`，以下是`）、流程元信息（如 `本文档旨在`、`下文将`）。
- P0：任何渠道文件含未脱敏凭据（如 `ntn_`、`sk-`、`ghp_`、裸 token 字符串）。
