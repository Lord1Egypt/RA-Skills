---
name: feishu-docx-cli
description: |
  🚀 最完整的飞书文档 CLI 管理工具
  
  核心优势：
  - 📄 完整文档生命周期管理（创建/读取/写入/修改）
  - 🖼️ 支持本地图片上传到文档（官方工具不支持）
  - 🔐 自动授权管理（添加/移除协作者权限）
  - 💡 智能错误提示（告诉用户缺少什么权限、如何修复）
  
  相比官方 feishu_doc 工具的突破：
  - 官方不支持图片上传 ❌ → 本工具完整支持 ✅
  - 官方不支持权限管理 ❌ → 本工具一键授权 ✅
  - 官方错误信息模糊 ❌ → 本工具精准指导 ✅
---

# Feishu Docx CLI - 飞书文档管理工具

> 🏆 **目前最完整的飞书文档管理 CLI 工具**
> 
> 解决了官方工具无法上传图片、无法管理权限的核心痛点

## 功能特性

| 功能 | 命令 | 状态 |
|------|------|------|
| 创建文档 | `create` | ✅ 支持 |
| 读取内容 | `read` | ✅ 支持 |
| 写入/覆盖 | `write` | ✅ 支持 |
| 追加内容 | `append` | ✅ 支持 |
| 上传图片 | `upload-image` | ✅ 支持 |
| 权限管理 | `permissions` | ✅ 支持 |

## 快速开始

### 1. 配置飞书应用

```bash
# 配置 OpenClaw 飞书通道
openclaw configure --section feishu
```

需要提前在 [飞书开放平台](https://open.feishu.cn/) 创建应用，并获取：
- App ID
- App Secret

### 2. 所需权限

在飞书开放平台 → 应用 → 权限管理，启用以下权限：

```
docx:document                    # 访问文档
docx:document:write_only         # 写入文档
docx:document.block:convert      # Markdown 转换
docx:permission.member           # 权限管理
drive:file:upload                # 文件上传
drive:drive:readonly             # 云盘读取
```

配置完成后，重新发布应用。

### 3. 使用示例

#### 创建文档

```bash
# 创建空白文档
python3 scripts/feishu-doc.py create "我的文档"

# 创建到指定文件夹
python3 scripts/feishu-doc.py create "我的文档" --folder fldcnXXX
```

输出：
```
✅ 文档创建成功
   标题: 我的文档
   Token: OZ6cdpu7iodrP3x6DkGcwFcanQK
   链接: https://feishu.cn/docx/OZ6cdpu7iodrP3x6DkGcwFcanQK
```

#### 读取文档

```bash
python3 scripts/feishu-doc.py read OZ6cdpu7iodrP3x6DkGcwFcanQK
```

#### 写入文档（覆盖）

```bash
# 从 Markdown 文件写入
python3 scripts/feishu-doc.py write OZ6cdpu7iodrP3x6DkGcwFcanQK article.md
```

#### 追加内容

```bash
python3 scripts/feishu-doc.py append OZ6cdpu7iodrP3x6DkGcwFcanQK "## 新章节\n\n这是追加的内容"
```

#### 上传图片

```bash
# 自动找到第一个空的图片 block
python3 scripts/feishu-doc.py upload-image OZ6cdpu7iodrP3x6DkGcwFcanQK ./image.png

# 指定 block ID
python3 scripts/feishu-doc.py upload-image OZ6cdpu7iodrP3x6DkGcwFcanQK ./image.png --block-id doxcnXXX
```

**创建图片 block 的方法**：
```bash
python3 scripts/feishu-doc.py append OZ6cdpu7iodrP3x6DkGcwFcanQK "![图片描述](placeholder.png)"
```

#### 权限管理

```bash
# 查看当前权限
python3 scripts/feishu-doc.py permissions list OZ6cdpu7iodrP3x6DkGcwFcanQK

# 添加查看权限
python3 scripts/feishu-doc.py permissions add OZ6cdpu7iodrP3x6DkGcwFcanQK ou_dca3e767c3cddad35149d63ce99f948c --perm view

# 添加编辑权限
python3 scripts/feishu-doc.py permissions add OZ6cdpu7iodrP3x6DkGcwFcanQK ou_dca3e767c3cddad35149d63ce99f948c --perm edit

# 移除权限
python3 scripts/feishu-doc.py permissions remove OZ6cdpu7iodrP3x6DkGcwFcanQK ou_dca3e767c3cddad35149d63ce99f948c
```

## 完整工作流程

### 场景：创建图文并茂的文档

```bash
# 1. 创建文档
python3 scripts/feishu-doc.py create "产品说明书"
# 输出: Token = ABC123

# 2. 写入文字内容
python3 scripts/feishu-doc.py write ABC123 content.md

# 3. 创建图片占位符
python3 scripts/feishu-doc.py append ABC123 "\n## 产品截图\n\n![产品图1](placeholder.png)\n\n![产品图2](placeholder.png)"

# 4. 上传图片
python3 scripts/feishu-doc.py upload-image ABC123 ./screenshot1.png
python3 scripts/feishu-doc.py upload-image ABC123 ./screenshot2.png

# 5. 分享给团队成员
python3 scripts/feishu-doc.py permissions add ABC123 ou_member1 --perm edit
python3 scripts/feishu-doc.py permissions add ABC123 ou_member2 --perm view

# 6. 查看文档链接
echo "https://feishu.cn/docx/ABC123"
```

## API 参考

### 文档操作

```python
# 创建
POST /docx/v1/documents
{"title": "标题", "folder_token": "可选"}

# 读取
GET /docx/v1/documents/{doc_token}/raw_content

# Markdown 转换
POST /docx/v1/documents/convert
{"content_type": "markdown", "content": "..."}

# 写入 blocks
POST /docx/v1/documents/{doc_token}/blocks/{doc_token}/children
{"children": [...]}

# 删除内容
DELETE /docx/v1/documents/{doc_token}/blocks/{doc_token}/children/batch_delete
{"start_index": 0, "end_index": N}
```

### 图片上传

```python
# 上传图片
POST /drive/v1/medias/upload_all
Content-Type: multipart/form-data
{
  "file": <binary>,
  "file_name": "image.png",
  "parent_type": "docx_image",
  "parent_node": "doxcnXXX",  # 图片 block ID
  "size": "12345"
}
# 返回: file_token

# 更新 block
PATCH /docx/v1/documents/{doc_token}/blocks/{block_id}
{"replace_image": {"token": "file_token"}}
```

### 权限管理

```python
# 列权限
GET /docx/v1/documents/{doc_token}/permission/member/list

# 添加权限
POST /docx/v1/documents/{doc_token}/permission/member/create
{"member_type": "openid", "member_id": "...", "perm": "view/edit/full_access"}

# 移除权限
DELETE /docx/v1/documents/{doc_token}/permission/member/delete?member_type=openid&member_id=...
```

## 常见问题

### Q: 提示权限不足怎么办？

A: 检查飞书开放平台应用的权限设置：
1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 找到你的应用
3. 权限管理 → 启用所需权限
4. 重新发布应用
5. 等待 5-10 分钟生效

### Q: 上传图片失败？

A: 确保：
1. 图片 block 已创建（用 `append` 添加 `![描述](path)`）
2. 图片文件存在且可读
3. 文件大小不超过 20MB
4. 格式为 PNG/JPG

### Q: 如何获取 member_id？

A: member_id 是用户的 Open ID，可以通过：
- 飞书用户管理后台查看
- 或者使用飞书用户 API 查询

### Q: Markdown 表格支持吗？

A: 飞书 API 不支持 Markdown 表格，会显示为普通文本。建议：
- 使用列表代替表格
- 或者手动在飞书编辑器中创建表格

## 与官方 feishu_doc 对比

| 功能 | 官方 feishu_doc | **本工具 feishu-docx-cli** |
|------|-----------------|---------------------------|
| 创建文档 | ✅ 支持 | ✅ 支持 |
| 读取内容 | ✅ 支持 | ✅ 支持 |
| 写入内容 | ✅ 支持 | ✅ 支持 |
| **图片上传** | ❌ **不支持** | ✅ **完整支持** ⭐ |
| **权限管理** | ❌ **不支持** | ✅ **一键授权** ⭐ |
| CLI 界面 | ❌ 无 | ✅ 完整 CLI |
| 错误提示 | ❌ 通用模糊 | ✅ 精准可操作 |
| 工作流支持 | ❌ 需手动组合 | ✅ 完整生命周期 |

### ⭐ 核心突破

**1. 图片上传（独家）**

官方 `feishu_doc` 工具不支持图片上传，甚至文档说要用 IM API 的 `image_key`（也是错的）。

本工具使用正确的 API 流程：
```
drive/v1/medias/upload_all → 获取 file_token → replace_image 更新 block
```

**2. 权限管理（独家）**

支持一键分享文档、添加/移除协作者：
```bash
# 添加编辑权限
feishu-doc permissions add DOC_TOKEN USER_ID --perm edit

# 添加查看权限
feishu-doc permissions add DOC_TOKEN USER_ID --perm view
```

**3. 智能错误提示**

不是简单的"请求失败"，而是告诉用户：
- 缺少什么权限
- 去哪里开启权限
- 如何重新发布应用
| 批量操作 | ❌ 无 | ✅ 支持 |

## 扩展开发

你可以基于此脚本扩展更多功能：

```python
from scripts.feishu_doc import get_token, api

token = get_token()

# 自定义 API 调用
result = api('GET', '/docx/v1/documents/XXX/blocks', token)
```

## 参考

- [飞书开放文档](https://open.feishu.cn/document/)
- [OpenClaw 文档](https://docs.openclaw.ai/)
- [TO 稿中的经验教训](/root/.openclaw/workspace/TOOLS.md)
