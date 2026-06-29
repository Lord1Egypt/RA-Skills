"""
activity-duration-estimation 分析引擎
CPM关键路径分析 / 多分布蒙特卡洛模拟 / 任务重叠分析 / SVG图表生成
"""

import math
import random
from collections import defaultdict, deque
from typing import Any


# ═══════════════════════════════════════════════════
# 0. 合理性审查
# ═══════════════════════════════════════════════════

class ValidationResult:
    """审查结果"""
    def __init__(self):
        self.passed: bool = True
        self.issues: list[str] = []

    def add(self, msg: str):
        self.passed = False
        self.issues.append(msg)

    def __str__(self):
        if self.passed:
            return '✅ 审查通过'
        return f'❌ {len(self.issues)} 项问题:\n' + '\n'.join(f'  - {s}' for s in self.issues)


def validate_cpm_input(durations: dict, dependencies: dict) -> ValidationResult:
    """CPM输入合理性审查"""
    r = ValidationResult()
    for tid, dur in durations.items():
        if dur < 0:
            r.add(f'任务{tid} 工期为负 ({dur})')
        if dur == 0:
            r.add(f'任务{tid} 工期为0，可能为输入错误')
    for tid, deps in dependencies.items():
        if tid in deps:
            r.add(f'任务{tid} 自引用依赖')
        for d in deps:
            dep_id = d[0] if isinstance(d, (list, tuple)) else d
            if dep_id not in durations:
                r.add(f'任务{tid} 依赖不存在的任务 {dep_id}')
    return r


def validate_cpm_result(result) -> ValidationResult:
    """CPM输出合理性审查"""
    r = ValidationResult()
    if result.has_cycle:
        r.add('任务网络存在循环依赖')
    if result.project_duration <= 0:
        r.add(f'项目总工期异常 ({result.project_duration})')
    for tid, cd in result.task_cpm.items():
        if cd['es'] > cd['ef']:
            r.add(f'任务{tid} ES({cd["es"]}) > EF({cd["ef"]})')
        if cd['ls'] > cd['lf']:
            r.add(f'任务{tid} LS({cd["ls"]}) > LF({cd["lf"]})')
        if cd['tf'] < -1e-6:
            r.add(f'任务{tid} 总时差负值 ({cd["tf"]})')
    return r


def validate_mc_input(phases: list) -> ValidationResult:
    """蒙特卡洛输入合理性审查"""
    r = ValidationResult()
    for name, o, m, p in phases:
        if not (o <= m <= p):
            r.add(f'{name}: O({o}) M({m}) P({p}) 不满足 O≤M≤P')
    return r


def validate_mc_result(results: dict) -> ValidationResult:
    """蒙特卡洛输出合理性审查"""
    r = ValidationResult()
    for dist_name, data in results.items():
        s = data['stats']
        q = data['quantiles']
        if s['min'] > s['max']:
            r.add(f'{dist_name}: min({s["min"]}) > max({s["max"]})')
        if q['p50'] > q['p90']:
            r.add(f'{dist_name}: P50({q["p50"]}) > P90({q["p90"]})')
        if s['stddev'] < 0:
            r.add(f'{dist_name}: 标准差为负 ({s["stddev"]})')
    return r


def validate_overlap_tasks(tasks: list) -> ValidationResult:
    """重叠分析输入合理性审查"""
    r = ValidationResult()
    for t in tasks:
        if t.get('start', 0) > t.get('end', 0):
            r.add(f'{t.get("name","?")}: start({t["start"]}) > end({t["end"]})')
    return r


def validate_all(durations: dict, dependencies: dict,
                 phases: list, tasks: list) -> list[ValidationResult]:
    """全流程合理性审查——在自动编排后执行"""
    results = []
    results.append(validate_cpm_input(durations, dependencies))
    results.append(validate_mc_input(phases))
    results.append(validate_overlap_tasks(tasks))
    return results


# ═══════════════════════════════════════════════════
# 1. CPM关键路径分析
# ═══════════════════════════════════════════════════

class CPMResult:
    """CPM分析结果"""
    def __init__(self):
        self.task_cpm: dict[int, dict] = {}    # task_id -> {es, ef, ls, lf, tf, is_critical}
        self.critical_ids: set[int] = set()     # 关键任务ID集合
        self.critical_path: list[int] = []      # 按顺序的关键路径
        self.project_duration: float = 0.0      # 项目总工期
        self.has_cycle: bool = False            # 是否存在循环依赖


def calc_cpm(
    durations: dict[int, float],
    dependencies: dict[int, list[tuple[int, str]] | list[int]]
) -> CPMResult:
    """
    CPM关键路径分析
    输入:
      durations = {任务ID: 工期}
      dependencies = {任务ID: [(前置ID, 关系类型), ...]}
        关系类型: 'FS' / 'SS' / 'FF' / 'SF'
        兼容旧格式: {任务ID: [前置ID, ...]} (默认FS)
    返回: CPMResult 包含所有时差和关键路径信息
    """
    result = CPMResult()
    task_ids = list(durations.keys())
    n = len(task_ids)
    if n == 0:
        return result

    id_to_idx = {tid: i for i, tid in enumerate(task_ids)}

    # 标准化依赖关系格式
    dep_list: dict[int, list[tuple[int, str]]] = {}
    for tid in task_ids:
        if tid not in dependencies:
            dep_list[tid] = []
            continue
        deps = dependencies[tid]
        parsed: list[tuple[int, str]] = []
        for d in deps:
            if isinstance(d, (list, tuple)) and len(d) >= 2:
                pred_id, dep_type = d[0], str(d[1]).upper()
                if dep_type not in ('FS', 'SS', 'FF', 'SF'):
                    dep_type = 'FS'
                parsed.append((pred_id, dep_type))
            elif isinstance(d, (int, float)):
                parsed.append((int(d), 'FS'))
        dep_list[tid] = parsed

    # 构建邻接表（仅用于拓扑排序，基于FS关系）
    adj: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for tid in task_ids:
        for pred_id, _ in dep_list.get(tid, []):
            if pred_id in id_to_idx:
                adj[id_to_idx[pred_id]].append(id_to_idx[tid])
                indegree[id_to_idx[tid]] += 1

    # 拓扑排序
    queue = deque([i for i in range(n) if indegree[i] == 0])
    topo_order: list[int] = []
    indegree_copy = indegree[:]
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            indegree_copy[v] -= 1
            if indegree_copy[v] == 0:
                queue.append(v)

    if len(topo_order) != n:
        result.has_cycle = True
        return result

    # 前向传递 — 支持四种依赖关系
    es = [0.0] * n
    ef = [0.0] * n
    for u in topo_order:
        ef[u] = es[u] + durations[task_ids[u]]
        # FF/SF：前置任务对当前任务的结束时间约束
        for pred_id, dep_type in dep_list.get(task_ids[u], []):
            p_idx = id_to_idx[pred_id]
            if dep_type == 'FF':
                ef[u] = max(ef[u], ef[p_idx])
            elif dep_type == 'SF':
                ef[u] = max(ef[u], es[p_idx])
        # FF/SF调整后，重新计算ES
        es[u] = ef[u] - durations[task_ids[u]]
        # FS/SS：当前任务对后继任务的开始时间约束
        for v_idx in adj[u]:
            for pred_id, dep_type in dep_list.get(task_ids[v_idx], []):
                if pred_id != task_ids[u]:
                    continue
                p_idx = id_to_idx[pred_id]
                if dep_type == 'FS':
                    es[v_idx] = max(es[v_idx], ef[p_idx])
                elif dep_type == 'SS':
                    es[v_idx] = max(es[v_idx], es[p_idx])

    project_duration = max(ef)
    result.project_duration = project_duration

    # 后向传递 — 最晚完成(LF)、最晚开始(LS)
    lf = [project_duration] * n
    ls = [0.0] * n
    for u in reversed(topo_order):
        if adj[u]:
            lf[u] = min(ls[v] for v in adj[u])
        ls[u] = lf[u] - durations[task_ids[u]]

    # 计算总时差、识别关键路径
    tf = [ls[i] - es[i] for i in range(n)]

    for i, tid in enumerate(task_ids):
        is_critical = abs(tf[i]) < 1e-6
        cpm_data = {
            'id': tid,
            'es': es[i], 'ef': ef[i],
            'ls': ls[i], 'lf': lf[i],
            'tf': tf[i],
            'is_critical': is_critical
        }
        result.task_cpm[tid] = cpm_data
        if is_critical:
            result.critical_ids.add(tid)

    # 提取关键路径（按顺序）
    if result.critical_ids:
        start_critical = [tid for tid in task_ids
                          if tid in result.critical_ids
                          and (tid not in dependencies or not dependencies[tid]
                               or not any(d in result.critical_ids for d in dependencies[tid]))]
        if start_critical:
            current = min(start_critical, key=lambda x: result.task_cpm[x]['es'])
            visited = set()
            while current in result.critical_ids and current not in visited:
                visited.add(current)
                result.critical_path.append(current)
                next_tasks = [task_ids[v] for v in adj[id_to_idx[current]]
                              if task_ids[v] in result.critical_ids]
                if next_tasks:
                    current = min(next_tasks, key=lambda x: result.task_cpm[x]['es'])
                else:
                    break

    return result


# ═══════════════════════════════════════════════════
# 2. 紧前关系自动规划
# ═══════════════════════════════════════════════════

def infer_dep_type(name_prev: str, name_curr: str) -> str:
    """
    依赖类型推断。

    串行还是并行取决于资源、能力、工期安排等现实约束，
    无法从任务名称可靠推断（刷三遍油漆都叫"油漆"，但不能并行）。
    默认统一返回 FS，用户可手动指定 SS/FF/SF。
    """
    return "FS"


def auto_plan_dependencies(
    phase_count: int,
    phases: list[dict] = None
) -> dict[int, list[int]]:
    """
    自动规划紧前关系。

    输入:
      phase_count: 阶段数
      phases: 可选，阶段列表 [{name, ...}]，用于从名称提取WBS前缀进行分组

    规则:
      - 从 phase name 中提取 WBS 前缀（如 "1.1 痛点调研" → 父组 "1"）
      - 同一父组内的子任务：按 WBS 编码顺序 FS 串联（反映实际工作流）
        → 依赖类型通过 infer_dep_type() 语义推断（FS/SS/FF/SF）
      - 跨父组边界：新组的第一个任务依赖上一组中 M 值最大的任务（FS）
      - 无法提取前缀时回退为全串行
    返回: {阶段索引: [(前置阶段索引, 关系类型), ...]}
    """
    deps: dict[int, list[int]] = {}

    # 尝试从 phases name 中提取 WBS 父组前缀
    groups: dict[str, list[int]] = {}
    has_groups = False
    if phases:
        for idx, p in enumerate(phases, start=1):
            name = p.get("name", "")
            import re
            m = re.match(r'^(\d+)\.', name.strip())
            if m:
                parent = m.group(1)
                groups.setdefault(parent, []).append(idx)
                has_groups = True

    if has_groups and len(groups) > 1:
        # 按组号排序
        sorted_parents = sorted(groups.keys(), key=lambda x: int(x))
        prev_group_constraint = None  # 上一组中 M 值最大的任务ID

        for parent in sorted_parents:
            members = sorted(groups[parent])

            for i, tid in enumerate(members):
                if prev_group_constraint is not None and i == 0:
                    # 跨组边界：本组第一个任务依赖上一组 M 值最大的任务
                    deps[tid] = [(prev_group_constraint, "FS")]
                elif i > 0:
                    # 组内串联：前一个任务 → 当前任务，语义推断类型
                    prev_tid = members[i - 1]
                    dep_type = "FS"
                    if phases and prev_tid <= len(phases) and tid <= len(phases):
                        dep_type = infer_dep_type(
                            phases[prev_tid - 1].get("name", ""),
                            phases[tid - 1].get("name", "")
                        )
                    deps[tid] = [(prev_tid, dep_type)]
                else:
                    # 第一组的第一个任务：无前置
                    deps[tid] = []

            # 找到本组中 M 值最大的任务作为下一组的约束
            if phases and len(phases) >= max(members):
                max_m_tid = max(members, key=lambda x: phases[x - 1].get("m", 0))
            else:
                max_m_tid = members[-1]
            prev_group_constraint = max_m_tid
    else:
        # 无分组信息 → 回退为全串行，语义推断类型
        for i in range(1, phase_count + 1):
            if i > 1:
                dep_type = "FS"
                if phases and i <= len(phases) and (i - 1) <= len(phases):
                    dep_type = infer_dep_type(
                        phases[i - 2].get("name", ""),
                        phases[i - 1].get("name", "")
                    )
                deps[i] = [(i - 1, dep_type)]
            else:
                deps[i] = []

    return deps


def parse_dependency_string(dep_str: str) -> list[tuple[int, int, str]]:
    """
    解析紧前关系字符串
    格式: "1→2(FS), 2→3(SS), 3→4(FF)"
    返回: [(前驱ID, 后继ID, 关系类型)]
    """
    relations = []
    parts = [p.strip() for p in dep_str.replace('，', ',').split(',')]
    for part in parts:
        if '→' not in part:
            continue
        arrow_idx = part.index('→')
        left = part[:arrow_idx].strip()
        right = part[arrow_idx + 1:].strip()
        dep_type = 'FS'  # 默认
        if '(' in right and ')' in right:
            paren_start = right.index('(')
            dep_type = right[paren_start + 1:right.index(')')].strip().upper()
            right = right[:paren_start].strip()
        try:
            pred_id = int(left)
            succ_id = int(right)
            if dep_type in ('FS', 'SS', 'FF', 'SF'):
                relations.append((pred_id, succ_id, dep_type))
        except ValueError:
            continue
    return relations


# ═══════════════════════════════════════════════════
# 3. 多分布蒙特卡洛模拟
# ═══════════════════════════════════════════════════

def _pert_beta_random(o: float, m: float, p: float) -> float:
    """PERT-Beta分布随机数"""
    alpha = 1 + 4 * (m - o) / (p - o) if p > o else 1
    beta = 1 + 4 * (p - m) / (p - o) if p > o else 1
    u1 = random.random()
    u2 = random.random()
    gamma_a = -math.log(1 - u1 ** (1 / alpha)) if alpha > 0 else 0
    gamma_b = -math.log(1 - u2 ** (1 / beta)) if beta > 0 else 0
    total = gamma_a + gamma_b
    if total > 0:
        beta_val = gamma_a / total
    else:
        beta_val = 0.5
    return o + beta_val * (p - o)


def _triangular_random(o: float, m: float, p: float) -> float:
    """三角分布随机数"""
    a, b, c = o, m, p
    if c == a:
        return a
    fc = (b - a) / (c - a)
    r = random.random()
    if r < fc:
        return a + math.sqrt(r * (b - a) * (c - a))
    else:
        return c - math.sqrt((1 - r) * (c - a) * (c - b))


def _poisson_random(mean_val: float) -> float:
    """泊松近似随机数"""
    return max(0, mean_val + (random.random() - 0.5) * mean_val * 0.2)


def monte_carlo_multi(
    phases: list[tuple[str, float, float, float]],
    iterations: int = 2000,
    distributions: list[str] = None,
    dependencies: dict = None,
    task_count: int = 0,
) -> dict:
    """
    多分布蒙特卡洛模拟

    phases: [(名称, 乐观, 最可能, 悲观), ...]
    iterations: 模拟次数
    distributions: ['pert', 'triangular', 'poisson'] 默认全部
    dependencies: 紧前关系 {任务ID: [(前驱ID, 类型)]}（1-based），
                  传入后每次模拟走 CPM 计算真实工期而非简单求和
    task_count: 任务总数（与 dependencies 对应，传了 dependencies 时必须）
    返回: {分布名: {quantiles, stats, samples}}
    """
    if distributions is None:
        distributions = ['pert', 'triangular', 'poisson']

    if dependencies and not task_count:
        task_count = len(phases)

    dist_funcs = {
        'pert': lambda o, m, p: _pert_beta_random(o, m, p),
        'triangular': lambda o, m, p: _triangular_random(o, m, p),
        'poisson': lambda o, m, p: _poisson_random(m),
    }

    results = {}
    for dist in distributions:
        if dist not in dist_funcs:
            continue
        func = dist_funcs[dist]
        samples = []
        for _ in range(iterations):
            # 为每个任务生成随机工期
            random_durs = {i+1: func(o, m, p) for i, (_, o, m, p) in enumerate(phases)}

            if dependencies and task_count > 0:
                # 走 CPM 计算真实工期（考虑并行）
                cpm_result = calc_cpm(random_durs, dependencies)
                total = cpm_result.project_duration
            else:
                # 无依赖时简单求和（等价于全串行）
                total = sum(random_durs.values())

            samples.append(total)

        samples.sort()
        mean = sum(samples) / iterations
        variance = sum((s - mean) ** 2 for s in samples) / iterations

        results[dist] = {
            'samples': samples[:1000],  # 仅保留1000个用于图表（降采样）
            'stats': {
                'min': samples[0],
                'max': samples[-1],
                'mean': mean,
                'stddev': math.sqrt(variance),
                'median': samples[iterations // 2],
            },
            'quantiles': {
                'p5': samples[int(iterations * 0.05)],
                'p10': samples[int(iterations * 0.10)],
                'p25': samples[int(iterations * 0.25)],
                'p50': samples[int(iterations * 0.50)],
                'p75': samples[int(iterations * 0.75)],
                'p90': samples[int(iterations * 0.90)],
                'p95': samples[int(iterations * 0.95)],
            },
            'histogram': _calc_histogram(samples, 25),
        }

    return results


def _calc_histogram(samples: list[float], bins: int) -> dict:
    """计算直方图数据"""
    min_val = min(samples)
    max_val = max(samples)
    bin_width = (max_val - min_val) / bins if max_val > min_val else 1
    edges = [min_val + i * bin_width for i in range(bins + 1)]
    counts = [0] * bins
    for s in samples:
        idx = min(int((s - min_val) / bin_width), bins - 1) if bin_width > 0 else 0
        counts[idx] += 1

    total = len(samples)
    return {
        'edges': edges,
        'counts': counts,
        'freq': [c / total for c in counts],
        'cumulative': [],
    }


# ═══════════════════════════════════════════════════
# 4. 任务重叠分析
# ═══════════════════════════════════════════════════

def calc_overlap(
    tasks: list[dict]
) -> dict:
    """
    任务重叠分析
    tasks: [{name, start, end}, ...]  start/end 为时间戳
    返回: 最大重叠数区间 + 最长重叠时长区间
    """
    if not tasks:
        return {'max_count': {'count': 0, 'tasks': [], 'start': 0, 'end': 0, 'duration': 0},
                'max_duration': {'count': 0, 'tasks': [], 'start': 0, 'end': 0, 'duration': 0}}

    events: list[tuple[float, int, int]] = []  # (时间, 增量, 任务索引)
    for i, t in enumerate(tasks):
        events.append((t['start'], 1, i))
        events.append((t['end'], -1, i))
    events.sort(key=lambda x: x[0])

    current_count = 0
    current_tasks: set[int] = set()
    prev_time: float | None = None
    segments: list[dict] = []

    for time, delta, task_idx in events:
        if prev_time is not None and time > prev_time and current_count >= 2:
            segments.append({
                'start': prev_time,
                'end': time,
                'count': current_count,
                'tasks': list(current_tasks),
            })
        if delta > 0:
            current_tasks.add(task_idx)
        else:
            current_tasks.discard(task_idx)
        current_count += delta
        prev_time = time

    if not segments:
        return {'max_count': {'count': 0, 'tasks': [], 'start': 0, 'end': 0, 'duration': 0}, 'max_duration': {'count': 0, 'tasks': [], 'start': 0, 'end': 0, 'duration': 0}}

    # 合并相邻且任务相同的区间
    merged: list[dict] = [segments[0]]
    for seg in segments[1:]:
        last = merged[-1]
        if last['count'] == seg['count'] and set(last['tasks']) == set(seg['tasks']):
            last['end'] = seg['end']
        else:
            merged.append(seg)

    # 最大重叠数
    max_count_seg = max(merged, key=lambda s: (s['count'], s['end'] - s['start']))
    # 最长持续时间（重叠数>=2）
    duration_segs = [s for s in merged if s['count'] >= 2]
    max_dur_seg = max(duration_segs, key=lambda s: s['end'] - s['start']) if duration_segs else merged[0]

    def _make_result(seg: dict, tasks_all: list) -> dict:
        return {
            'count': seg['count'],
            'start': seg['start'],
            'end': seg['end'],
            'duration': seg['end'] - seg['start'],
            'tasks': [tasks_all[i]['name'] for i in seg['tasks']],
        }

    return {
        'max_count': _make_result(max_count_seg, tasks),
        'max_duration': _make_result(max_dur_seg, tasks),
    }


# ═══════════════════════════════════════════════════
# 5. SVG图表生成
# ═══════════════════════════════════════════════════

def generate_gantt_svg(
    tasks: list[dict],
    cpm_result: CPMResult | None = None,
    width: int = 800,
    height: int = 350,
    unit: str = "天"
) -> str:
    """生成甘特图SVG
    unit: 时间单位标签，如 "天" "周" "h"
    """
    if not tasks:
        return f'<svg width="{width}" height="{height}"><text x="{width//2}" y="{height//2}" text-anchor="middle" fill="#999">暂无任务数据</text></svg>'

    mag = {'top': 50, 'right': 30, 'bottom': 70, 'left': 160}
    chart_w = width - mag['left'] - mag['right']
    chart_h = height - mag['top'] - mag['bottom']

    # 时间范围
    starts = [t['start'] for t in tasks]
    ends = [t['end'] for t in tasks]
    min_time = min(starts)
    max_time = max(ends)
    time_range = max_time - min_time if max_time > min_time else 1

    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b',
              '#f5576c', '#ff9671', '#ffc75f', '#845ec2', '#008f7a']

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<defs><filter id="shadow"><feDropShadow dx="1" dy="1" stdDeviation="1" flood-opacity="0.2"/></filter></defs>')
    svg.append(f'<text x="{width//2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">任务甘特图（单位：{unit}）</text>')

    # 网格线
    steps = max(6, min(int(time_range / 5) + 1, 20))
    for i in range(steps + 1):
        t = min_time + time_range * i / steps
        x = mag['left'] + chart_w * i / steps
        if i > 0 and i < steps:
            svg.append(f'<line x1="{x}" y1="{mag["top"]}" x2="{x}" y2="{mag["top"] + chart_h}" stroke="#eee" stroke-width="0.5" stroke-dasharray="3,3"/>')

    # 坐标轴
    svg.append(f'<line x1="{mag["left"]}" y1="{mag["top"]}" x2="{mag["left"]}" y2="{mag["top"] + chart_h}" stroke="#333" stroke-width="1.5"/>')
    svg.append(f'<line x1="{mag["left"]}" y1="{mag["top"] + chart_h}" x2="{mag["left"] + chart_w}" y2="{mag["top"] + chart_h}" stroke="#333" stroke-width="1.5"/>')

    # Y轴 - 任务名称
    task_h = min(36, chart_h / max(len(tasks), 1))
    for i, t in enumerate(tasks):
        y = mag['top'] + i * task_h + task_h / 2
        name_display = t["name"]
        if len(name_display) > 12:
            name_display = name_display[:11] + "…"
        svg.append(f'<text x="{mag["left"] - 10}" y="{y}" text-anchor="end" font-size="11" fill="#333">{name_display}</text>')

    # X轴刻度
    for i in range(steps + 1):
        t = min_time + time_range * i / steps
        x = mag['left'] + chart_w * i / steps
        svg.append(f'<line x1="{x}" y1="{mag["top"] + chart_h}" x2="{x}" y2="{mag["top"] + chart_h + 5}" stroke="#333"/>')
        svg.append(f'<text x="{x}" y="{mag["top"] + chart_h + 18}" text-anchor="middle" font-size="9" fill="#666">{t:.0f}</text>')

    # Y轴水平网格线
    for i in range(len(tasks)):
        y = mag['top'] + i * task_h + task_h
        svg.append(f'<line x1="{mag["left"]}" y1="{y:.1f}" x2="{mag["left"] + chart_w}" y2="{y:.1f}" stroke="#f0f0f0" stroke-width="0.5"/>')

    # 绘制任务条
    for i, t in enumerate(tasks):
        y = mag['top'] + i * task_h + 6
        sx = mag['left'] + chart_w * (t['start'] - min_time) / time_range
        ex = mag['left'] + chart_w * (t['end'] - min_time) / time_range
        bw = max(3, ex - sx)
        ci = t.get('id', i) % len(colors)

        is_critical = cpm_result and t.get('id', 0) in (cpm_result.critical_ids or set())
        stroke_color = '#c0392b' if is_critical else 'none'
        fill_color = colors[ci]

        svg.append(f'<rect x="{sx:.1f}" y="{y}" width="{bw:.1f}" height="{task_h - 12}" '
                   f'fill="{fill_color}" stroke="{stroke_color}" stroke-width="2" rx="3" ry="3" filter="url(#shadow)"/>')

        if bw > 40:
            dur = t['end'] - t['start']
            dur_str = f"{dur:.0f}{unit}" if unit else f"{dur:.1f}"
            txt_color = "#fff" if is_critical else "#fff"
            svg.append(f'<text x="{sx + bw/2:.1f}" y="{y + (task_h - 12)/2 + 4}" '
                       f'text-anchor="middle" font-size="9" fill="{txt_color}" font-weight="bold">{dur_str}</text>')

    # 关键路径图例
    if cpm_result and cpm_result.critical_ids:
        ly = height - 12
        svg.append(f'<line x1="{mag["left"]}" y1="{ly}" x2="{mag["left"] + 20}" y2="{ly}" stroke="#c0392b" stroke-width="2"/>')
        svg.append(f'<text x="{mag["left"] + 25}" y="{ly + 4}" font-size="11" fill="#c0392b">关键路径</text>')
        svg.append(f'<text x="{mag["left"] + 160}" y="{ly + 4}" font-size="11" fill="#333">总工期: {cpm_result.project_duration:.0f}{unit}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def generate_mc_svg(
    results: dict,
    width: int = 700,
    height: int = 450
) -> str:
    """生成蒙特卡洛多分布对比图SVG"""
    if not results:
        return f'<svg width="{width}" height="{height}"><text x="{width//2}" y="{height//2}" text-anchor="middle" fill="#999">暂无模拟数据</text></svg>'

    margin = {'top': 40, 'right': 150, 'bottom': 60, 'left': 70}
    chart_w = width - margin['left'] - margin['right']
    chart_h = height - margin['top'] - margin['bottom']

    dist_colors = {'pert': '#667eea', 'triangular': '#f093fb', 'poisson': '#4facfe'}
    dist_labels = {'pert': 'PERT-Beta', 'triangular': '三角分布', 'poisson': '泊松近似'}
    dist_markers = {'pert': 'o', 'triangular': 's', 'poisson': '^'}

    # 计算全局范围
    all_samples = []
    for dist_name, data in results.items():
        all_samples.extend(data['samples'])
    if not all_samples:
        return ''
    global_min = min(all_samples)
    global_max = max(all_samples)
    range_val = global_max - global_min if global_max > global_min else 1

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{width}" height="{height}" fill="#fafbff"/>')
    svg.append(f'<text x="{width//2}" y="25" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">蒙特卡洛模拟多分布对比</text>')

    # 坐标轴
    svg.append(f'<line x1="{margin["left"]}" y1="{margin["top"]}" x2="{margin["left"]}" y2="{margin["top"] + chart_h}" stroke="#333" stroke-width="1.5"/>')
    svg.append(f'<line x1="{margin["left"]}" y1="{margin["top"] + chart_h}" x2="{margin["left"] + chart_w}" y2="{margin["top"] + chart_h}" stroke="#333" stroke-width="1.5"/>')

    # X轴
    for i in range(6):
        val = global_min + range_val * i / 5
        x = margin['left'] + chart_w * i / 5
        svg.append(f'<line x1="{x}" y1="{margin["top"] + chart_h}" x2="{x}" y2="{margin["top"] + chart_h + 5}" stroke="#333"/>')
        svg.append(f'<text x="{x}" y="{margin["top"] + chart_h + 18}" text-anchor="middle" font-size="10" fill="#666">{val:.1f}</text>')
    svg.append(f'<text x="{margin["left"] + chart_w//2}" y="{margin["top"] + chart_h + 38}" text-anchor="middle" font-size="11" fill="#333">项目总工期</text>')

    # 绘制各分布的直方图+曲线
    for idx, (dist_name, data) in enumerate(results.items()):
        hist = data.get('histogram', {})
        if not hist or not hist['counts']:
            continue
        counts = hist['counts']
        max_count = max(counts) if max(counts) > 0 else 1
        color = dist_colors.get(dist_name, '#666')
        n = len(counts)

        # 直方图（半透明）
        for i, c in enumerate(counts):
            if c == 0:
                continue
            x = margin['left'] + chart_w * i / n
            bw = chart_w / n - 1
            bh = chart_h * c / max_count
            y = margin['top'] + chart_h - bh
            svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(bw, 1):.1f}" height="{bh:.1f}" fill="{color}" opacity="0.25"/>')

        # 均值分位线
        stats = data.get('stats', {})
        mean_val = stats.get('mean', 0)
        mx = margin['left'] + chart_w * (mean_val - global_min) / range_val
        svg.append(f'<line x1="{mx:.1f}" y1="{margin["top"]}" x2="{mx:.1f}" y2="{margin["top"] + chart_h}" stroke="{color}" stroke-width="1.5" stroke-dasharray="4,3"/>')

        # P50 / P90 标记
        quants = data.get('quantiles', {})
        for qname, qx in [('P50', 'p50'), ('P90', 'p90')]:
            if qx in quants:
                qv = quants[qx]
                qx_pos = margin['left'] + chart_w * (qv - global_min) / range_val
                qy = margin['top'] + chart_h - 8 - idx * 12
                svg.append(f'<circle cx="{qx_pos:.1f}" cy="{qy}" r="3" fill="{color}"/>')
                svg.append(f'<text x="{qx_pos + 6:.1f}" y="{qy + 4}" font-size="9" fill="{color}">{qname}</text>')

    # 图例
    lx = margin['left'] + chart_w + 15
    ly = margin['top'] + 10
    svg.append(f'<rect x="{lx - 5}" y="{ly - 5}" width="135" height="{len(results) * 28 + 30}" fill="white" stroke="#ddd" rx="5"/>')
    svg.append(f'<text x="{lx}" y="{ly + 15}" font-size="12" font-weight="bold" fill="#333">分布统计</text>')
    for idx, (dist_name, data) in enumerate(results.items()):
        y = ly + 35 + idx * 28
        color = dist_colors.get(dist_name, '#666')
        stats = data.get('stats', {})
        svg.append(f'<rect x="{lx}" y="{y - 7}" width="12" height="12" fill="{color}" opacity="0.5"/>')
        label = dist_labels.get(dist_name, dist_name)
        svg.append(f'<text x="{lx + 18}" y="{y + 2}" font-size="10" fill="#333">{label}</text>')
        svg.append(f'<text x="{lx + 18}" y="{y + 16}" font-size="9" fill="#888">均值 {stats.get("mean", 0):.1f} σ={stats.get("stddev", 0):.1f}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


# ═══════════════════════════════════════════════════
# 6. 实际工时计算
# ═══════════════════════════════════════════════════

def calc_real_work_hours(
    start_ts: float, end_ts: float,
    work_hours_per_day: float = 8,
    workdays: set[int] = None
) -> float:
    """
    计算实际工时（排除非工作日）
    start_ts, end_ts: 时间戳（秒）
    work_hours_per_day: 每日工作小时
    workdays: 工作日集合, 默认 1-5 (周一到周五)
    """
    if workdays is None:
        workdays = {1, 2, 3, 4, 5}

    import datetime
    start_dt = datetime.datetime.fromtimestamp(start_ts)
    end_dt = datetime.datetime.fromtimestamp(end_ts)

    if start_dt >= end_dt:
        return 0

    total_hours = 0.0
    current = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    while current <= end_day:
        weekday = (current.weekday() + 1) % 7  # 转为 1=周一
        if weekday in workdays:
            if current == start_dt.replace(hour=0, minute=0, second=0, microsecond=0):
                # 第一天
                day_end = current.replace(hour=23, minute=59, second=59)
                hours = (min(end_dt, day_end) - start_dt).total_seconds() / 3600
                total_hours += max(0, min(hours, work_hours_per_day))
            elif current == end_day:
                # 最后一天
                hours = (end_dt - current).total_seconds() / 3600
                total_hours += max(0, min(hours, work_hours_per_day))
            else:
                total_hours += work_hours_per_day
        current += datetime.timedelta(days=1)

    return total_hours
