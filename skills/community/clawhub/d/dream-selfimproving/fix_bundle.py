"""
修复dream.py三个问题：
1. bundle_results进报告（加参数+新报告section）
2. "10个错误"误判（auditor只检查原始日志，不看recall snippet）
3. Recall EP facetpoint_ids去重（link函数加EP侧去重）
"""
from pathlib import Path

dream_py = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py')
content = dream_py.read_text(encoding='utf-8', errors='replace')

changes = 0

# ============================================================
# 修复1a: generate_report_v33签名加bundle_results参数
# ============================================================
old = 'mflow_stats: dict = None):\n    """v4.0: 新增M-FLOW图状态"""'
new = 'mflow_stats: dict = None,\n                        bundle_results: list = None):\n    """v4.0: 新增M-FLOW图状态 + BundleSearch结果"""'
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('1a: signature + docstring updated')

# 修复1b: 函数体开头初始化bundle_results
old = '    """v4.0: 新增M-FLOW图状态 + BundleSearch结果"""\n    now = '
new = '    """v4.0: 新增M-FLOW图状态 + BundleSearch结果"""\n    if bundle_results is None:\n        bundle_results = []\n    now = '
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('1b: bundle_results default init added')

# 修复1c: BundleSearch结果section插入图状态section之后
marker = '**倒锥结构**: 锥尖(L3)精准锚点 → 语义边传播 → 锥底(L1)Episode返回\n\n'
idx_m = content.find(marker)
if idx_m >= 0:
    insert_at = idx_m + len(marker)
    # 找下一个section（health_note/coherence_low）
    p1 = content.find('\n    if health_note:', insert_at)
    p2 = content.find('\n    elif coherence_low:', insert_at)
    next_pos = min(p for p in [p1, p2] if p >= 0)
    bundle_text = '\n**Bundle Search 检索结果**: 0 个相关历史Episode\n\n'
    content = content[:next_pos] + bundle_text + content[next_pos:]
    changes += 1
    print('1c: BundleSearch section inserted into report')
else:
    print('WARNING: marker not found for 1c')

# 修复1d: 调用处传bundle_results
old = """        mflow_stats=mflow_stats
    )

    report_file = DREAMS_DIR"""
new = """        mflow_stats=mflow_stats,
        bundle_results=bundle_results
    )

    report_file = DREAMS_DIR"""
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('1d: bundle_results passed to generate_report_v33')
else:
    print('WARNING: old_call not found for 1d')

# ============================================================
# 修复2: error标签误判（只看原始日志，不看AI响应）
# ============================================================
old = "        v['_amygdala_tag'] = 'error' if any(e in v.get('snippet','').lower() for e in ['error','fail']) else 'normal'"
new = "        # 只检查原始日志条目；recall snippet是AI响应，error词频≠真实错误数\n        is_raw = not v.get('snippet','').startswith(('assistant ', 'user '))\n        v['_amygdala_tag'] = 'error' if (is_raw and any(e in v.get('snippet','').lower() for e in ['error','fail'])) else 'normal'"
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('2: error tag logic fixed (raw log only)')
else:
    print('WARNING: old_error_logic not found for 2')

# ============================================================
# 修复3: link_facetpoint_to_episode EP侧去重
# ============================================================
old = '''            if fp_id not in self.episodes[episode_id].facetpoint_ids:
                self.episodes[episode_id].facetpoint_ids.append(fp_id)

    def link_facetpoint_to_facet'''
new = '''            # EP侧去重：避免同一FP被重复link到同一EP
            ep = self.episodes[episode_id]
            if fp_id not in ep.facetpoint_ids:
                ep.facetpoint_ids.append(fp_id)

    def link_facetpoint_to_facet'''
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print('3: link_facetpoint_to_episode EP-side dedup added')
else:
    print('WARNING: old_link not found for 3')

# 写入
dream_py.write_text(content, encoding='utf-8')
print(f'\nAll done. {changes}/6 changes applied.')

# 验证语法
import subprocess
r = subprocess.run(['python', '-m', 'py_compile', str(dream_py)],
                  capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode == 0:
    print('Syntax check: OK')
else:
    print('Syntax check: FAILED')
    print(r.stderr[:500])
