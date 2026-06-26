#!/bin/bash
# dytext.sh - 抖音文案提取 Skill 脚本
# 通过 npx dytext-cli 调用，自动处理注册/登录/转写

set -e

exec npx dytext-cli "$@"
