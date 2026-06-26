#!/bin/bash

# 阿里云域名帮助文档抓取脚本
# 目标目录
TARGET_DIR="/Users/kevin/doc/aliyun-domain-help"

# 文档列表（从页面导航栏提取）
# 产品概述
DOCS=(
  # 产品概述
  "什么是阿里云域名服务:/zh/dws/product-overview/what-is-domains"
  "图说域名:/zh/dws/product-overview/from-domain-name-to-website-illustration"
  "功能特性:/zh/dws/product-overview/product-function-custom-node-domain-normal"
  "限制条件:/zh/dws/product-overview/limits"
  "基本概念:/zh/dws/product-overview/terms"
  "顶级域名分类解析:/zh/dws/product-overview/top-level-domain-name-suffix-list"
  
  # 快速入门
  "域名注册快速入门:/zh/dws/getting-started/quickly-register-a-new-domain-name"
  "域名交易快速入门:/zh/dws/getting-started/domain-name-trading-quick-start"
  "从域名注册到网站搭建:/zh/dws/getting-started/the-whole-process-of-website-building"
  
  # 操作指南
  "域名实名认证:/zh/dws/user-guide/how-to-complete-domain-name-authentication"
  "域名注册:/zh/dws/user-guide/how-to-register-a-domain-name"
  "域名过户与信息修改:/zh/dws/user-guide/domain-information-modification"
  "域名转移:/zh/dws/user-guide/domain-transfer"
  "域名交易:/zh/dws/user-guide/domain-name-transaction"
  "域名管理:/zh/dws/user-guide/domain-name-management"
  "域名安全:/zh/dws/user-guide/domain-name-security1"
  "轻量网站搭建:/zh/dws/user-guide/ai-static-display-station"
  
  # 安全合规
  "侵权与域名滥用的处理:/zh/dws/security-and-compliance/handling-of-copyright-infringements-and-domain-name-abuse"
  
  # 开发参考
  "集成概览:/zh/dws/developer-reference/call-openapi"
  
  # 服务支持
  "域名功能介绍视频:/zh/dws/support/function-introduction-video"
  
  # 万小智 AI 建站
  "万小智 AI 建站操作指南:/zh/dws/website-backend-management"
  "常见问题:/zh/dws/faq"
)

echo "开始抓取阿里云域名帮助文档..."
echo "目标目录：$TARGET_DIR"
echo ""

# 创建子目录
mkdir -p "$TARGET_DIR/01-产品概述"
mkdir -p "$TARGET_DIR/02-快速入门"
mkdir -p "$TARGET_DIR/03-操作指南"
mkdir -p "$TARGET_DIR/04-安全合规"
mkdir -p "$TARGET_DIR/05-开发参考"
mkdir -p "$TARGET_DIR/06-服务支持"
mkdir -p "$TARGET_DIR/07-万小智 AI 建站"

# 基础 URL
BASE_URL="https://help.aliyun.com"

# 计数器
count=0
total=${#DOCS[@]}

for doc in "${DOCS[@]}"; do
  # 分割名称和路径
  name="${doc%%:*}"
  path="${doc##*:}"
  
  # 构建完整 URL
  url="${BASE_URL}${path}"
  
  # 确定分类目录
  if [[ "$path" == *"/product-overview/"* ]]; then
    category="01-产品概述"
  elif [[ "$path" == *"/getting-started/"* ]]; then
    category="02-快速入门"
  elif [[ "$path" == *"/user-guide/"* ]]; then
    category="03-操作指南"
  elif [[ "$path" == *"/security-and-compliance/"* ]]; then
    category="04-安全合规"
  elif [[ "$path" == *"/developer-reference/"* ]]; then
    category="05-开发参考"
  elif [[ "$path" == *"/support/"* ]]; then
    category="06-服务支持"
  elif [[ "$path" == *"/website-backend-management/"* ]] || [[ "$path" == *"/faq/"* ]]; then
    category="07-万小智 AI 建站"
  else
    category="其他"
  fi
  
  # 生成文件名
  filename=$(echo "$name" | tr ' ' '_').md
  output_file="$TARGET_DIR/$category/$filename"
  
  echo "[$((++count))/$total] 抓取：$name"
  echo "  URL: $url"
  echo "  输出：$output_file"
  
  # 使用 curl 获取页面（这里简化处理，实际需要 browser_use）
  # 由于需要 JavaScript 渲染，我们改用 browser_use
  
done

echo ""
echo "文档列表生成完成！"
echo "总共 ${#DOCS[@]} 个文档"
