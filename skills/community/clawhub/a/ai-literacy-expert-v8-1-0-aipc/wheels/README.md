# wheels/

本目录用于存放自定义或未发布的 Python wheel 包（.whl 文件）。

## 用途

当 `requirements.txt` 中声明的依赖包含无法从 PyPI 公开获取的包时，将对应的
`.whl` 文件放置在此目录下。`install-env.ps1` / `install-env.sh` 安装依赖时
会优先从 `wheels/` 目录查找。

## 当前状态

当前所有依赖（openvino、openvino-genai、modelscope、jsonschema）均可从
PyPI 公开获取，因此本目录暂为空。

> 说明：V7.3 起本地模型下载源已从 HuggingFace 切换为 ModelScope，
> `requirements.txt` 中以 `modelscope==1.39.1` 取代了 `huggingface_hub==0.24.0`，
> 以在国内网络下获得更稳定、更快的模型下载体验。

若未来需要添加自定义 wheel（如特定 OpenVINO 版本的自编译包），请：

1. 将 `.whl` 文件放入本目录
2. 在 `requirements.txt` 中使用 `./wheels/package_name-版本-cp310-...whl` 格式引用
3. 更新 `install-env.ps1` / `install-env.sh` 添加 `--find-links wheels/` 参数
