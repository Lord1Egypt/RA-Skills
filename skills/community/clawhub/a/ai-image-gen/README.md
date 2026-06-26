# image-gen

AI 图像生成 Skill，基于 Gemini Flash Image 模型，支持文生图、图+文生图、多比例、多分辨率。

## 安装

```bash
clawhub install image-gen
```

## 环境变量配置

使用前需配置以下环境变量（**不要硬编码到代码中**）：

```bash
IMAGE_GEN_API_KEY=your-api-key
IMAGE_GEN_BASE_URL=your-base-url
```

## 获取 API Key

推荐使用 FoxCode 中转服务，注册地址：

👉 [https://foxcode.rjj.cc/auth/register?aff=R0P5ZY](https://foxcode.rjj.cc/auth/register?aff=R0P5ZY)

注册后在控制台获取 API Key 和 Base URL。

## 支持的模型

- 基础（标准分辨率）：1:1、3:2、2:3、3:4、4:3、4:5、5:4、9:16、16:9、21:9
- 2K 分辨率：同上所有比例
- 4K 分辨率：同上所有比例（不含 21:9）

默认模型：`gemini-3.1-flash-image-2k-16x9`

## License

MIT
