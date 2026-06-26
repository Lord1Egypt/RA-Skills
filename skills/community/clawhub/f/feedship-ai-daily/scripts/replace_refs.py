#!/usr/bin/env python3
"""
feedship-ai-daily 引用替换脚本

用法:
  cat LLM_OUTPUT.md | python3 replace_refs.py > OUTPUT.md

环境变量:
  TODAY_ARTICLES: JSON 对象，键为编号字符串，值为 {"title": ..., "link": ...}
  例如: {"1": {"title": "文章标题", "link": "https://..."}, ...}

替换规则:
  - ${N}         → [标题](链接)
  - ${N,M,P}     → 展开为多个独立链接
  - ${N} (无效)  → [无效引用 #N]（带警告标记）
  - ${N}$        → 同上（兼容旧格式）

注意: LLM 只能输出编号占位符 ${N}，禁止在引用中展开标题或链接。
      标题和链接由本脚本注入，避免 LLM 幻觉。
"""

import sys, json, re, os

def main():
    articles_raw = os.environ.get('TODAY_ARTICLES', '{}')
    try:
        articles = json.loads(articles_raw)
    except json.JSONDecodeError:
        print("ERROR: TODAY_ARTICLES is not valid JSON", file=sys.stderr)
        sys.exit(1)

    if not articles:
        print("WARNING: TODAY_ARTICLES is empty, no replacements will be made", file=sys.stderr)

    text = sys.stdin.read()
    total_replacements = 0
    invalid_refs = []

    def replace_single(idx_str):
        """替换单个编号，返回 [标题](链接) 或 [无效引用 #N]"""
        idx = idx_str.strip()
        item = articles.get(idx)
        if item:
            return f'[{item["title"]}]({item["link"]})'
        else:
            invalid_refs.append(idx)
            return f'[无效引用 #{idx}]'

    def replace_group(m):
        """处理 ${N,M,P} 或 ${N} 格式"""
        inner = m.group(1).strip()
        # 去掉末尾的 $（兼容旧格式）
        inner = inner.rstrip('$')
        # 分割成独立编号
        nums = [n.strip() for n in inner.split(',') if n.strip()]
        parts = [replace_single(n) for n in nums]
        result = ' '.join(parts)
        # 如果是多项合并，增加视觉分隔
        if len(parts) > 1:
            return result
        return result

    # 匹配 ${N,M,P}（逗号分隔多编号）和 ${N}$（带尾$）以及 ${N}
    # 优先匹配逗号分隔的，然后匹配单个编号
    pattern = r'\$\{([^}]+)\}'
    result, count = re.subn(pattern, replace_group, text)
    
    # 报告统计
    invalid_count = len(invalid_refs)
    print(f"[replace_refs] {count} 处引用已替换", file=sys.stderr)
    if invalid_count > 0:
        print(f"[replace_refs] 警告: {invalid_count} 处无效引用 {invalid_refs}", file=sys.stderr)
    
    sys.stdout.write(result)

if __name__ == '__main__':
    main()
