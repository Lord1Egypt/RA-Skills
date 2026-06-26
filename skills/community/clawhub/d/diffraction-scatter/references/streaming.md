# Streaming for Large Datasets / 大批量流式处理

## Principles / 原则

1. Read file-by-file and frame-by-frame / 逐文件、逐帧读取
2. Write outputs frame-by-frame / 逐帧输出结果
3. Do not keep a whole batch in memory / 不把整批图像留在内存里

## Recommendations / 建议

- For Eiger / HDF5, provide the dataset path and channel when possible / 尽量提供 `dataset path` 和通道
- Prefer `csr` for throughput / 高吞吐优先 `csr`
- Prefer `splitpixel` for accuracy / 精度优先 `splitpixel`
- Prefer WSL2 / conda-forge for heavy Windows workloads / Windows 大规模任务优先 WSL2 / conda-forge

## What the bundled runner already does / 本技能脚本的流式特征

- HDF5 frame iteration via generators / 输入端：HDF5 逐帧 `yield`
- Per-frame `.csv/.h5/.npz` writing / 输出端：每帧立刻写 `.csv/.h5/.npz`
- JSONL progress events / 进度端：JSONL 事件流
