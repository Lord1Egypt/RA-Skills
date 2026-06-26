#!/bin/bash
# Hugo 博客发布环境变量配置示例
# 将此文件复制到 ~/.zshrc 或 ~/.bashrc 中

# 博客项目根目录（必需）
export HUGO_BLOG_DIR=/Users/victor/Desktop/Projects/github/HUGO_blog

# posts 目录相对路径（可选，默认为 content/zh/posts）
# export HUGO_POSTS_DIR=content/zh/posts

# 模板文件相对路径（可选，默认为 archetypes/default.md）
# export HUGO_TEMPLATE_PATH=archetypes/default.md

# 使用说明：
# 1. 将上述配置添加到你的 shell 配置文件中
# 2. 重新加载配置：source ~/.zshrc（或 ~/.bashrc）
# 3. 从任意位置执行发布：
#    python3 ~/.config/opencode/skills/blog-publisher/scripts/publish_blog.py \
#      --md ~/Downloads/my-article.md \
#      --category 技术