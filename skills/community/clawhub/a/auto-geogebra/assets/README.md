# assets —— README 演示素材（可复现）

- `demo1…demo7-*.png`：七个示例的引擎预览图（由 `tools/ggb-export` 真机导出时以 `--png` 生成）；
- `demo.gif`：README 顶部轮播（由 `make-demo-gif.py` 合成，含自动裁白边与统一画布）；
- `make-demo-gif.py`：复现脚本 —— `python make-demo-gif.py`（依赖 Pillow）。

## 复现路径

1. 用 `tools/ggb-export/export_ggb.mjs` 重新导出各示例（加 `--png` 得到预览图，文件名对齐 `demoN-*.png`）；
2. 运行 `python make-demo-gif.py` 重新合成 GIF。

## 关于录制脚本（*.tape 说明）

本项目演示素材是 **GeoGebra 画布渲染结果的合成**，不是终端录制，因此仓库不提供 vhs `*.tape`；
等价的可复现脚本即 `make-demo-gif.py`（与预览图生成链一起入库，任何人可重跑）。

如果你偏好终端录制（例如录制验证器/冒烟运行过程），可自行安装 [vhs](https://github.com/charmbracelet/vhs) 后使用如下模板：

```tape
Output demo-validate.gif
Set Shell "bash"
Set FontSize 16
Set Width 1000
Set Height 620
Type "python scripts/smoke_test.py"
Enter
Sleep 4s
```

<sub>模板仅示意，未在本仓库 CI 中执行（无 vhs 依赖）。</sub>
