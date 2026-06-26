#!/usr/bin/env bash
# SimpleViking Find - 检索工具
# 用法: sv_find "查询关键词" [起始URI] [--vector|--keyword|--hybrid]

source "$(dirname "$0")/lib.sh"

# 解析参数
query=""
start_uri="viking://resources"
search_type="hybrid"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vector)
      search_type="vector"
      shift
      ;;
    --keyword)
      search_type="keyword"
      shift
      ;;
    --hybrid)
      search_type="hybrid"
      shift
      ;;
    -*)
      # 未知选项跳过
      shift
      ;;
    *)
      if [[ -z "$query" ]]; then
        query="$1"
      elif [[ "$1" == viking://* ]]; then
        start_uri="$1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$query" ]]; then
  echo "用法: sv_find \"关键词\" [起始URI] [--vector|--keyword|--hybrid]"
  echo ""
  echo "选项:"
  echo "  --vector   仅语义搜索（需要先构建索引）"
  echo "  --keyword  仅关键词搜索"
  echo "  --hybrid   混合搜索（默认）"
  exit 1
fi

# 执行搜索
case "$search_type" in
  vector)
    sv_semantic_search "$query" "$SV_WORKSPACE" 5
    ;;
  keyword)
    sv_find_smart "$query" "$start_uri"
    ;;
  hybrid)
    sv_hybrid_search "$query" "$SV_WORKSPACE" 5
    ;;
esac
