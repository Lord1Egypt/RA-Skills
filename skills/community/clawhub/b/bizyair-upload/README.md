# BizyAir 上传技能使用说明

## 技能信息

- **名称**: `bizyair-upload`
- **功能**: 将本地文件（图片、音频、视频）上传到 BizyAir 服务器
- **目录**: `/Volumes/AI/AIGC/aigc/Skills/bizyair-upload`

## 安装依赖

```bash
pip install requests alibabacloud-oss-v2
```

## 配置

设置环境变量（推荐）：

```bash
export BIZYAIR_API_KEY="your_api_key_here"
```

获取 API Key: https://www.bizyair.cn/

## 使用方式

### 1. 通过 Claude Code 技能使用

```
请帮我把 /path/to/image.png 上传到 BizyAir
```

```
上传这张图片到 BizyAir 并获取 URL
```

### 2. 直接使用脚本

```bash
# 上传单个文件
python3 scripts/upload.py /path/to/file.png

# 查询已上传的资源列表
python3 scripts/upload.py --list

# 查询指定页
python3 scripts/upload.py --list --page 2 --page-size 10

# 使用指定 API Key
python3 scripts/upload.py /path/to/file.png --api-key "your_key"
```

## 上传流程

1. **获取上传凭证** - 从 BizyAir API 获取临时 STS 凭证和 OSS 上传参数
2. **上传到 OSS** - 使用阿里云 OSS SDK 将文件上传到指定存储
3. **提交资源** - 在 BizyAir 系统中注册该资源
4. **返回 URL** - 返回可访问的资源 URL

## 输出示例

```
📁 准备上传文件: example.png
   路径: /path/to/example.png

📋 步骤一：获取上传凭证...
✅ 上传凭证获取成功
   Object Key: inputs/20260313/xxx.png
   Endpoint: oss-cn-shanghai.aliyuncs.com
   Bucket: bizyair-prod

📤 步骤二：上传到 OSS...
✅ OSS 上传成功
   ETag: "56F506819E8250A4526897252CF4F3D1"

📝 步骤三：提交输入资源...
✅ 资源提交成功
   ID: 218818
   URL: https://storage.bizyair.cn/inputs/20260313/xxx.png

==================================================
🎉 上传完成！
==================================================
文件名: example.png
URL: https://storage.bizyair.cn/inputs/20260313/xxx.png
扩展名: .png
ID: 218818
==================================================
```

## 测试记录

| 测试项 | 状态 |
|--------|------|
| 上传图片 | ✅ 成功 |
| 获取 URL | ✅ 成功 |
| 查询列表 | ✅ 成功 |

## API 参考

详细文档: https://docs.bizyair.cn/api/upload-tutorial.html

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2026-03-13 | 初始版本，支持文件上传和查询列表 |
