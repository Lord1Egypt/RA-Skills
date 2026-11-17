#!/bin/bash
# dytext.sh - Videosays 兼容 Skill 脚本
# 通过 npx videosays 调用，自动处理注册/登录/转写

set -e

exec npx videosays "$@"
