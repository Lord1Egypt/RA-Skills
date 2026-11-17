# 视觉样例库（Gallery）

真实公开数据的可复现样例（每例 = 数据 JSON + 复现命令；成品图 = 仓库内 `*_preview.svg` 矢量图，可直接查看）。
每例 = 成品图 + 数据 JSON + 复现命令；统计值经独立实现互拍与视觉验收。

## pbc_km

Mayo PBC 队列 KM 生存曲线（R survival::pbc，n=312 双盲 RCT；log-rank P=0.75 与文献一致）

```bash
python3 scripts/gen_figure.py -t km -d examples/gallery/pbc_km.json -o pbc_km.png --cjk
```

## ovarian_km

卵巢癌辅助化疗 RCT KM（R survival::ovarian，n=26；官方计数逐项对拍）

```bash
python3 scripts/gen_figure.py -t km -d examples/gallery/ovarian_km.json -o ovarian_km.png --cjk
```

## fleiss93_labbe

L'Abbé 图 #40（Fleiss 1993 阿司匹林 7 RCT；合并 RR=0.873 与独立实现逐位互拍）

```bash
python3 scripts/gen_figure.py -t labbe -d examples/gallery/fleiss93_labbe.json -o fleiss93_labbe.png --cjk
```

