# 简单文档工作流

**适用**：< 800 字 且无明显结构信号的短文/资讯。

## 流程

1. **理解内容**：快速读一遍，确定主题和一句话摘要
2. **转 md**（若非 md 输入）：
   - 保留原文段落结构
   - 把"注意"/"提示"这类明显标记转成 `<Callout>`
   - 其他一律用纯 md
3. **写入 `source.md`**（若原始输入非 md）
4. **生成 `article.mdx`**：基于 source.md，按 `component-selection.md` 最小必要地插入组件
5. **图片处理**：若有图片，先整理到 `images/` 或记下 URL
6. **调图片本地化**：`node <skill>/scripts/image-localize.mjs <post-dir>`
7. **调渲染**：`node <skill>/scripts/render.mjs <post-dir>/article.mdx`
8. **写 meta.json**：按 `meta-schema.md` 填字段（从 MEMORY.md 读默认值，缺失字段询问）
9. **汇报**：打印 preview 路径 + 组件清单 + 阅读时间预估

## 渐进式输出

每完成一步立即告知作者（"骨架建好了"→"图片处理完成 3 张"→"预览：path"），不等全部完成再统一汇报。

## 示例输入/输出

**输入**：一段话描述 OpenAI 新发布的 API 功能，约 500 字，配 1 张图。

**产出**：
- `source.md`（若原始是纯文本）
- `article.mdx`（可能只加一个 Callout info 标识关键能力）
- `images/hero.png`
- `meta.json`
- `preview.html`
