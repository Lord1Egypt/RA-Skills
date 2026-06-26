---
name: cnblogs-publisher
description: Manage CNBlogs (博客园) articles via MetaWeblog API. Supports save drafts, publish, update, and delete posts.
allowed-tools: Bash(python3:*), Bash(pip3:*)
---

# CNBlogs Publisher Skill

通过 MetaWeblog API 管理博客园（CNBlogs）文章的 OpenClaw Skill。

## 功能特性

- ✅ **保存草稿** - 快速创建文章草稿
- 📋 **文章管理** - 获取列表、查看详情
- ✏️ **更新修改** - 修改已有文章内容
- 🚀 **一键发布** - 将草稿发布为正式文章
- 🗑️ **安全删除** - 删除文章（带确认机制）

## 快速开始

### 1. 配置环境变量

```bash
export CNBLOGS_BLOG_URL="https://rpc.cnblogs.com/metaweblog/your-blog-name"
export CNBLOGS_USERNAME="your-username"
export CNBLOGS_TOKEN="your-metaweblog-token"
```

获取 Token：博客园 → 设置 → 其他设置 → MetaWeblog 访问令牌

### 2. 保存第一篇草稿

```bash
# 创建文章
cat > mypost.md << 'EOF'
# 我的第一篇文章

Hello，这是我的第一篇博客！
EOF

# 保存到草稿箱
python scripts/save_draft.py "我的第一篇文章" "mypost.md" "随笔"
```

### 3. 发布文章

```bash
# 使用上一步返回的文章 ID
python scripts/publish.py 12345678
```

## 所有命令

| 命令 | 功能 | 示例 |
|:---|:---|:---|
| `get_blog_info.py` | 获取博客信息 | `python scripts/get_blog_info.py` |
| `list_drafts.py` | 获取文章列表 | `python scripts/list_drafts.py` |
| `get_post.py` | 获取单篇文章 | `python scripts/get_post.py 12345` |
| `save_draft.py` | 保存草稿 | `python scripts/save_draft.py "标题" "file.md" "分类"` |
| `update_draft.py` | 更新草稿 | `python scripts/update_draft.py 12345 "file.md" "分类"` |
| `publish.py` | 发布文章 | `python scripts/publish.py 12345` |
| `delete_post.py` | 删除文章 | `python scripts/delete_post.py 12345` |

## 完整文档

详细文档、API 参考、故障排除请访问：
https://github.com/suversal/cnblogs-publisher/blob/main/README.md

## 技术栈

- Python 3.7+
- MetaWeblog API
- xmlrpc.client

## 许可证

MIT License

---

**作者**: suversal  
**仓库**: https://github.com/suversal/cnblogs-publisher  
**版本**: 1.0.0
