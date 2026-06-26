#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""菜谱搜索 - 全网搜索 + AI 生成（无爬虫版）"""
import sys,json

def search_online(kw,n=5):
 """全网搜索菜谱（调用外部搜索服务）"""
 return {
  "type":"search_prompt",
  "keyword":kw,
  "count":n,
  "message":f"🔍 可全网搜索「{kw} 菜谱 做法」，或让我用 AI 生成原创菜谱~"
 }

def generate_recipe_ai(kw):
 """AI 生成菜谱（降级方案）"""
 return {
  "type":"ai_generate_prompt",
  "keyword":kw,
  "message":f"🤖 回复「 更详细的{kw} 菜谱」，我来生成原创菜谱（食材+步骤+小贴士+营养）~"
 }

def search_recipe(kw,n=5):
 """搜索菜谱（全网搜索优先，AI 生成降级）"""
 result={
  "keyword":kw,
  "primary":search_online(kw,n),
  "fallback":generate_recipe_ai(kw),
  "note":""
 }
 return result

if __name__=="__main__":
 if len(sys.argv)<2:
  print("用法: python meal_search.py <关键词> [数量]")
  print("说明: 移除爬虫版，返回搜索提示和 AI 生成建议")
  sys.exit(0)
 kw=sys.argv[1]
 n=int(sys.argv[2])if len(sys.argv)>2 else 5
 print(json.dumps(search_recipe(kw,n),ensure_ascii=False,indent=2))
