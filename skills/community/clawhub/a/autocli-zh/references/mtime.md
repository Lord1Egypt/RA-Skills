# Mtime

## 常用模式

### 首页热门 / 编辑精选
```bash
autocli mtime hot --limit 5
autocli mtime hot --limit 5 --format json
```

## 最小说明

- `mtime hot` 当前可返回：`title`、`desc`、`image`、`link`、`section`。
- `image` 当前是图片外链，不是下载后的本地文件。
- 对 Telegram，若要稳定显示图片预览，不要直接裸发图片链接；优先使用 Markdown 链接触发预览。
- 当前已验证可用的 Telegram 展示格式是：

    ```md
    [title](link)
    - desc
    [-](image)
    ```

- 若一次发送多条，建议控制在 3–5 条，避免 Telegram 预览过长或折叠不稳定。
