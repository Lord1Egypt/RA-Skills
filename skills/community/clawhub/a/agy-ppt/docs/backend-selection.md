# 圖片後端政策

本 fork 不再讓每次簡報都重新選 image backend。

預設且唯一自動路徑：

```text
Codex CLI -> $imagegen -> built-in image_gen
```

理由：

1. 使用現有 Codex 訂閱 session。
2. 避免額外 API key 與計費路徑。
3. 降低 backend selection 帶來的流程不確定性。
4. 把 Codex 定位成單純 renderer。

若 built-in `image_gen` 不可用：

```text
IMAGE_BACKEND_UNAVAILABLE
```

停止自動產圖並回 AGY 決策。
