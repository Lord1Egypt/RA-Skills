# 数黑棋子与中国规则数子

[English README](README.en.md)

这是一个 Codex skill，用于从围棋棋盘原图中识别 19 路棋盘、统计可见黑棋子，并按中国规则给出黑方数子结果。它也可以生成一张干净的结果棋盘图：圆形表示实际棋子，小方块表示算法推断的地盘，底部显示类似 `黑 197 子 胜` 的结果。

## 适用场景

- 用户上传围棋棋盘照片，想知道黑棋有多少颗。
- 用户问“黑多少子”“数子”“形势如何”，需要按中国规则计分。
- 用户希望生成一张清晰的结果棋盘图，而不是依赖计分软件截图。
- 需要区分实际棋子和被围住的空点地盘。

## 安装依赖

只在缺少依赖时安装：

```bash
python3 -m pip install -r scripts/requirements.txt
```

## 基本用法

生成 JSON、校验覆盖图和结果棋盘图：

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg \
  --json \
  --overlay /tmp/go-count-overlay.jpg \
  --result-image /tmp/go-result-board.jpg
```

只输出人类可读结果：

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg
```

如果自动识别棋盘不准，可以手动传入四个棋盘角点，按左上、右上、右下、左下的顺时针顺序：

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg \
  --corners "74,76 1100,53 1118,1031 72,1034" \
  --overlay /tmp/go-count-overlay.jpg \
  --result-image /tmp/go-result-board.jpg
```

如果传入的是四个最外侧网格交叉点，而不是木质棋盘边角，请加上：

```bash
--grid-corners
```

## 输出字段

- `black_stones`：棋盘上可见黑棋子数量。
- `white_stones`：棋盘上可见白棋子数量。
- `black_territory`：只被黑棋包围的空点数量。
- `white_territory`：只被白棋包围的空点数量。
- `black_area_chinese`：黑棋子数加黑方地盘数。
- `white_area_chinese`：白棋子数加白方地盘数。
- `black_result_chinese`：按中国规则估算黑方 `胜` 或 `负`。
- `area_total_ok`：黑白数子结果相加是否等于棋盘交叉点总数。
- `warnings`：低置信度、疑似计分覆盖图、单官或结果校验异常等提示。

## 结果解释

- 用户明确问“黑棋多少颗”时，优先报告 `black_stones`。
- 用户问“黑多少子”“数子”“形势”时，优先报告 `black_area_chinese`。
- 19 路棋盘按中国规则黑贴 3.75 子处理，黑方达到 `185` 子及以上判为胜。
- `board_ascii` 只表示棋子：`X` 是黑棋，`O` 是白棋。
- `result_ascii` 同时表示棋子和地盘：`X/O` 是棋子，`x/o` 是地盘，`.` 是中立空点。
- 如果 `area_total_ok` 为 `false`，或棋盘模糊、裁切、遮挡、有未提死子，应提示需要人工复核。

## 发布说明

发布到 skill 市场或 agent 配置时，默认使用中文展示名称、中文描述和中文默认提示。英文说明可链接到 GitHub 上的英文 README：

[https://github.com/imcaptor/count-go-black-stones/blob/main/README.en.md](https://github.com/imcaptor/count-go-black-stones/blob/main/README.en.md)
