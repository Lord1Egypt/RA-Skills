# 文件上传/下载能力说明

这些能力与普通 `kb ...` 命令不同，原因是它们需要处理二进制文件、本地文件系统，或返回可直接wget下载的临时链接。

## 1. Agent 入参

### 上传
本地文件上传到AIS

- `localPath`：MCP server / Python 脚本所在机器上的真实文件路径
- `pathName`：AIS 知识库中的目标目录
- `fileName`：可选；若不传，程序会取 `localPath` 的文件名

### 下载
AIS文件下载到本地

- `code`：远端文件或文档的稳定标识
- `localPath`：MCP server / Python 脚本所在机器上的真实保存路径
- `extractIs`：可选；是则下载提取清洗后的 md 内容，否则下载原文件
- `overwrite`：可选；默认不覆盖已有文件

### 生成下载链接
生成可wget下载文件的临时链接

- `code`：远端文件或文档的稳定标识
- `extractIs`：可选；是则下载提取清洗后的 md 内容，否则下载原文件