# Quality Checker Prompt

请检查生成的公众号封面图是否满足以下标准：

1. 是否符合文章主题？
2. 是否有明确主视觉？
3. 是否有足够留白？
4. 标题是否清晰可读？
5. 是否适合微信移动端缩略图？
6. 是否出现主标题以外的中文小字？
7. 是否出现书脊字、便签字、笔记字、地图标注？
8. 画面元素是否过多？
9. 是否有廉价营销海报感？
10. 是否需要返工？

请输出：

```yaml
quality_gate_result: pass | minor_revision | regenerate_required
issues:
  - ...
recommended_action: ...
```
