"""
drawio_hooks -- drawiodo 工作流钩子系统
======================================

在 Think -> Confirm -> Iterate -> Version Control 四阶工作流的每个阶段
嵌入 pre/post 两个钩子点，共 8 个 Hook Point。

核心设计原则：
- 强制约束：关键操作由 Python 端自动执行，不依赖 LLM 自觉
- 零依赖：纯 Python 3 标准库，不依赖外部包
- 非阻塞：钩子失败不影响主流程，除非显式 abort
- 可追溯：每次执行记录结果，支持 query
- 零心智负担：内置钩子默认开启，无需手动注册

用法：
    from drawio_hooks import hooks

    # 触发某个钩子点
    result = hooks('pre_think', context={})

    # 查询内置钩子注册情况
    print(hooks.registry())
"""

import json
import os
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable


# ═══════════════════════════════════════════════════════════════
# 枚举定义
# ═══════════════════════════════════════════════════════════════

class HookPoint(str, Enum):
    """8 个 Hook Point，覆盖 4 阶段工作流的 pre/post"""

    PRE_THINK = 'pre_think'
    """思考前：输入校验、上下文补全、前置条件检查"""
    POST_THINK = 'post_think'
    """思考后：分析结果校验、自动建议补充"""

    PRE_CONFIRM = 'pre_confirm'
    """确认前：选项有效性校验、快捷跳转判断"""
    POST_CONFIRM = 'post_confirm'
    """确认后：用户选择解析、执行参数设定"""

    PRE_ITERATE = 'pre_iterate'
    """迭代前：文件存在性检查、自动备份、权限校验"""
    POST_ITERATE = 'post_iterate'
    """迭代后：输出校验、版本管理初始化、自动预览触发、错误报告"""

    PRE_VC = 'pre_vc'
    """版本操作前：版本上限检查、自动清理触发"""
    POST_VC = 'post_vc'
    """版本操作后：状态报告、变更日志写入"""

    @classmethod
    def list_all(cls) -> list[str]:
        return [p.value for p in cls]

    def label(self) -> str:
        """用户友好标签"""
        labels = {
            'pre_think': '思考前',
            'post_think': '思考后',
            'pre_confirm': '确认前',
            'post_confirm': '确认后',
            'pre_iterate': '迭代前',
            'post_iterate': '迭代后',
            'pre_vc': '版本操作前',
            'post_vc': '版本操作后',
        }
        return labels.get(self.value, self.value)


# ═══════════════════════════════════════════════════════════════
# 钩子结果
# ═══════════════════════════════════════════════════════════════

class HookResult:
    """单个钩子的执行结果"""

    def __init__(
        self,
        success: bool = True,
        message: str = '',
        data: dict | None = None,
        abort: bool = False,
    ):
        self.success = success
        self.message = message
        self.data = data or {}
        self.abort = abort  # True 时主流程应停止
        self.name = 'unnamed'
        self.point = ''
        self.timestamp = datetime.now().isoformat(timespec='seconds')

    @property
    def status_icon(self) -> str:
        if self.abort:
            return '[ABORT]'
        return '[OK]' if self.success else '[WARN]'

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'point': self.point,
            'success': self.success,
            'message': self.message,
            'abort': self.abort,
            'timestamp': self.timestamp,
        }

    def __repr__(self) -> str:
        return f'{self.status_icon} [{self.name}] {self.message}'


# ═══════════════════════════════════════════════════════════════
# 注册表
# ═══════════════════════════════════════════════════════════════

_registry: dict[HookPoint, list[dict]] = {}
_history: list[dict] = []


def register(
    hook_point: HookPoint | str,
    name: str | None = None,
    description: str = '',
) -> Callable:
    """注册钩子函数（装饰器模式）

    用法：
        @register('pre_think', name='input_check')
        def my_hook(ctx):
            if not ctx.get('input'):
                return {'success': False, 'message': '输入为空', 'abort': True}
            return {'success': True, 'message': '输入校验通过'}

    参数：
        hook_point : 钩子点名称（HookPoint 枚举或字符串）
        name       : 钩子名称（默认取函数名）
        description: 钩子描述
    """
    point = HookPoint(hook_point) if isinstance(hook_point, str) else hook_point

    def decorator(func: Callable) -> Callable:
        hook_name = name or func.__name__
        if point not in _registry:
            _registry[point] = []
        _registry[point].append({
            'name': hook_name,
            'description': description,
            'func': func,
        })
        return func

    return decorator


def unregister(hook_point: HookPoint | str, name: str) -> bool:
    """注销指定钩子"""
    point = HookPoint(hook_point) if isinstance(hook_point, str) else hook_point
    if point not in _registry:
        return False
    before = len(_registry[point])
    _registry[point] = [h for h in _registry[point] if h['name'] != name]
    return len(_registry[point]) < before


def execute(hook_point: HookPoint | str, context: dict | None = None) -> list[HookResult]:
    """执行指定钩子点的所有注册函数

    参数：
        hook_point: 钩子点名称
        context   : 上下文字典（会被传入每个钩子函数）

    返回值：
        HookResult 列表，按注册顺序排列。如果有 abort=True 的结果，
        后续钩子不会执行。
    """
    point = HookPoint(hook_point) if isinstance(hook_point, str) else hook_point
    ctx = context or {}
    results: list[HookResult] = []

    hooks_at_point = _registry.get(point, [])

    if not hooks_at_point:
        result = HookResult(success=True, message='No hooks registered for this point')
        result.name = '(none)'
        result.point = point.value
        results.append(result)
        _history.append(result.to_dict())
        return results

    for hook in hooks_at_point:
        try:
            ret = hook['func'](ctx)
            if isinstance(ret, dict):
                result = HookResult(**ret)
            elif isinstance(ret, HookResult):
                result = ret
            elif ret is None:
                result = HookResult(success=True, message='ok')
            else:
                result = HookResult(success=True, data={'return': ret})
        except Exception as e:
            result = HookResult(
                success=False,
                message=f'Hook exception: {e}',
                abort=True,
            )
            traceback.print_exc()

        result.name = hook['name']
        result.point = point.value
        results.append(result)
        _history.append(result.to_dict())

        if result.abort:
            break

    return results


def registry() -> dict[str, list[dict]]:
    """返回当前所有注册的钩子（按 HookPoint 分组，不含函数引用）"""
    return {
        p.value: [
            {'name': h['name'], 'description': h['description']}
            for h in hooks
        ]
        for p, hooks in _registry.items()
    }


def history(limit: int = 20) -> list[dict]:
    """返回最近 N 次钩子执行历史"""
    return _history[-limit:]


def clear():
    """清空所有注册（用于测试/重置）"""
    _registry.clear()
    _history.clear()


# ============================================================
# VersionManager 延迟导入
# ============================================================

_VM_CACHE: dict[str, Any] = {}

def _get_vm(output_path: str) -> Any:
    """获取/缓存 VersionManager 实例"""
    if not output_path:
        return None
    base_dir = str(Path(output_path).parent)
    if base_dir not in _VM_CACHE:
        from drawio_version import VersionManager
        _VM_CACHE[base_dir] = VersionManager(base_dir)
    return _VM_CACHE[base_dir]


# ============================================================
# 内置钩子（所有 8 个点默认注册的守护逻辑）
# 关键原则：算法强制约束，不依赖 LLM 自觉
# ============================================================

# ---------- pre_think ----------

@register('pre_think', name='input_validator',
          description='验证用户输入不为空，为空则阻断')
def _pre_think_validate(ctx: dict) -> dict:
    """强制约束：输入为空时直接阻断，不给 LLM 继续执行的机会"""
    user_input = ctx.get('user_input', '')
    if not user_input or not user_input.strip():
        return {
            'success': False,
            'message': 'input_validator: 用户输入为空，阻断流程',
            'abort': True,
        }
    return {'success': True, 'message': f'input_validator: 输入有效（{len(user_input.strip())} chars）'}


@register('pre_think', name='context_enricher',
          description='补全缺失的上下文字段（默认值兜底）')
def _pre_think_enrich(ctx: dict) -> dict:
    if 'workspace' not in ctx:
        ctx['workspace'] = '.'
    if 'timestamp' not in ctx:
        ctx['timestamp'] = datetime.now().isoformat(timespec='seconds')
    return {'success': True, 'message': 'context_enricher: 上下文已补全'}


# ---------- post_think ----------

@register('post_think', name='output_validator',
          description='验证分析输出包含必要字段')
def _post_think_validate(ctx: dict) -> dict:
    output = ctx.get('analysis_output', {})
    required = ['diagram_type', 'complexity']
    missing = [f for f in required if f not in output]
    if missing:
        return {
            'success': False,
            'message': f'output_validator: 缺少必要字段: {", ".join(missing)}',
            'abort': False,  # 不阻塞，只警告
        }
    return {'success': True, 'message': 'output_validator: 分析输出结构完整'}


# ---------- pre_confirm ----------

@register('pre_confirm', name='option_validator',
          description='验证确认选项的完整性，不足则阻断')
def _pre_confirm_validate(ctx: dict) -> dict:
    """强制约束：选项不足 2 项时直接阻断"""
    options = ctx.get('confirm_options', [])
    if not options:
        return {
            'success': False,
            'message': 'option_validator: 选项列表为空，阻断流程',
            'abort': True,
        }
    if len(options) < 2:
        return {
            'success': False,
            'message': f'option_validator: 选项不足（{len(options)}），至少 2 项，阻断流程',
            'abort': True,
        }
    return {'success': True, 'message': f'option_validator: 选项完整（{len(options)} items）'}


@register('pre_confirm', name='shortcut_detector',
          description='检测快捷模式，跳过确认时直接清除选项使确认无法进行')
def _pre_confirm_shortcut(ctx: dict) -> dict:
    """
    ！！！！！！强制约束 ！！！！！！
    满足快捷条件时，直接清除 confirm_options 和 skip_confirm 均设。
    清除选项后，option_validator 的 "选项不足" abort 不会触发（因为快捷是白名单）。
    但 LLM 再也无法调用 AskUserQuestion，因为没有选项可以展示。
    """
    output = ctx.get('analysis_output', {})
    diag_type = output.get('diagram_type', '')
    complexity = output.get('complexity', 'medium')

    should_skip = False
    reason = ''

    if diag_type == 'flowchart' and complexity == 'simple':
        should_skip = True
        reason = '简单流程图'
    elif ctx.get('has_json_spec'):
        should_skip = True
        reason = 'JSON spec 模式'
    elif ctx.get('already_confirmed'):
        should_skip = True
        reason = '已确认方案'

    if should_skip:
        ctx['skip_confirm'] = True
        # ========== 强制清除选项 ==========
        # 让 LLM 无法调用 AskUserQuestion，因为没有选项可展示
        ctx['confirm_options'] = []
        # =================================
        return {'success': True, 'message': f'shortcut_detector: {reason}，已清除选项，跳过确认'}
    else:
        ctx['skip_confirm'] = False
        return {'success': True, 'message': 'shortcut_detector: 需要用户确认'}


# ---------- post_confirm ----------

@register('post_confirm', name='choice_parser',
          description='解析用户确认结果，设定执行参数')
def _post_confirm_parse(ctx: dict) -> dict:
    choice = ctx.get('user_choice', {})
    if not choice:
        return {'success': True, 'message': 'choice_parser: 无用户选择，使用默认参数'}
    ctx['execution_params'] = choice
    return {'success': True, 'message': f'choice_parser: 用户选择已解析: {choice}'}


# ---------- pre_iterate (强制备份) ----------

@register('pre_iterate', name='file_checker',
          description='检查/自动创建输出目录')
def _pre_iterate_file_check(ctx: dict) -> dict:
    """强制约束：输出目录不存在时自动创建"""
    output_path = ctx.get('output_path', '')
    if not output_path:
        return {'success': True, 'message': 'file_checker: 首次生成，无需校验'}
    out_dir = os.path.dirname(output_path)
    if not out_dir:
        return {'success': True, 'message': 'file_checker: 使用当前目录'}
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        return {'success': True, 'message': f'file_checker: 自动创建输出目录: {out_dir}'}
    return {'success': True, 'message': f'file_checker: 输出路径可用: {output_path}'}


@register('pre_iterate', name='auto_backup',
          description='【强制】非首次迭代时自动执行版本备份')
def _pre_iterate_auto_backup(ctx: dict) -> dict:
    """
    ！！！！！！强制约束 ！！！！！！
    在迭代更新前，自动执行 VersionManager.save_version() 进行备份。
    不需要 LLM 读取任何 flag，不需要 LLM 调用任何脚本。
    本钩子直接在 Python 端完成备份，LLM 无权跳过。
    """
    output_path = ctx.get('output_path', '')
    is_update = ctx.get('is_update', False)

    if not is_update or not output_path:
        return {'success': True, 'message': 'auto_backup: 首次生成，跳过备份'}

    if not os.path.exists(output_path):
        return {'success': True, 'message': f'auto_backup: 文件不存在（{output_path}），跳过备份'}

    try:
        vm = _get_vm(output_path)
        if vm is None:
            return {'success': False, 'message': 'auto_backup: 无法创建 VersionManager', 'abort': True}

        # ========== Python 端自动执行备份 ==========
        result = vm.save_version(
            output_path,
            description=f'迭代前自动备份（{datetime.now().strftime("%H:%M:%S")}）',
        )
        # ===========================================

        ctx['backup_result'] = result

        # 获取备份后的版本状态
        status = vm.status(output_path)
        ctx['version_count'] = status['total_versions']
        ctx['current_version'] = result['version']
        ctx['version_status'] = status

        return {
            'success': True,
            'message': f'auto_backup: 备份完成 -> {result["version"]}（版本 {status["total_versions"]}/{status["max_versions"]}）',
            'data': {'version': result['version'], 'total': status['total_versions'], 'max': status['max_versions']},
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'auto_backup: 备份失败: {e}',
            'abort': True,  # 备份失败必须阻断，确保不丢数据
        }


# ---------- post_iterate (强制初始化版本管理 + 输出校验 + 预览触发) ----------

@register('post_iterate', name='output_validator',
          description='验证生成文件 + 自动初始化版本管理')
def _post_iterate_validate(ctx: dict) -> dict:
    """
    ！！！！！！强制约束 ！！！！！！
    生成完成后，自动执行 VersionManager.init() 注册版本管理。
    不需要 LLM 读取任何 flag，不需要 LLM 调用任何脚本。
    本钩子直接在 Python 端完成版本管理初始化，LLM 无权限跳过。
    """
    output_path = ctx.get('output_path', '')
    if not output_path:
        return {'success': False, 'message': 'output_validator: 输出路径为空', 'abort': False}
    if not os.path.exists(output_path):
        return {
            'success': False,
            'message': f'output_validator: 文件不存在: {output_path}',
            'abort': True,
        }

    # 校验文件大小
    file_size = os.path.getsize(output_path)
    if file_size < 200:
        return {
            'success': False,
            'message': f'output_validator: 文件过小（{file_size} bytes），可能内容不完整',
            'abort': False,
        }

    ctx['generated_file_size'] = file_size

    # ========== Python 端自动初始化版本管理 ==========
    try:
        vm = _get_vm(output_path)
        if vm is not None:
            current = vm.current_version(output_path)
            if current is None:
                init_result = vm.init(output_path, description='初始版本')
                ctx['init_result'] = init_result
                status = vm.status(output_path)
                ctx['version_count'] = status['total_versions']
                ctx['current_version'] = init_result['version']
                msg = f'output_validator: 文件有效（{file_size / 1024:.1f} KB），版本管理已自动初始化 -> {init_result["version"]}'
            else:
                msg = f'output_validator: 文件有效（{file_size / 1024:.1f} KB），版本管理已存在（{current["version"]}）'
        else:
            msg = f'output_validator: 文件有效（{file_size / 1024:.1f} KB），版本管理初始化跳过'
    except Exception as e:
        msg = f'output_validator: 文件有效（{file_size / 1024:.1f} KB），版本管理初始化异常: {e}'
    # ===========================================

    return {
        'success': True,
        'message': msg,
        'data': {'file_size': file_size},
    }


@register('post_iterate', name='preview_trigger',
          description='【强制】生成后自动打开 draw.io 预览')
def _post_iterate_preview(ctx: dict) -> dict:
    """
    ！！！！！！强制约束 ！！！！！！
    生成完成后，直接调用 draw.io 可执行文件打开预览。
    不需要 LLM 读取任何 flag，不需要 LLM 执行任何操作。
    本钩子直接在 Python 端打开预览，LLM 无权跳过。
    """
    output_path = ctx.get('output_path', '')
    if not output_path or not os.path.exists(output_path):
        return {'success': True, 'message': 'preview_trigger: 无输出文件，跳过预览'}

    drawio_exe = r'C:\Program Files\draw.io\draw.io.exe'
    if not os.path.exists(drawio_exe):
        return {
            'success': False,
            'message': f'preview_trigger: draw.io 未安装（预期路径: {drawio_exe}），跳过预览',
            'abort': False,
        }

    try:
        import subprocess
        subprocess.Popen([drawio_exe, output_path], shell=False)
        return {'success': True, 'message': f'preview_trigger: 已打开 draw.io 预览: {output_path}'}
    except Exception as e:
        return {
            'success': False,
            'message': f'preview_trigger: 打开预览失败: {e}',
            'abort': False,
        }


# ---------- pre_vc (强制版本上限控制) ----------

@register('pre_vc', name='limit_checker',
          description='【强制】检查版本数上限，超限时自动清理最旧版本')
def _pre_vc_limit_check(ctx: dict) -> dict:
    """
    ！！！！！！强制约束 ！！！！！！
    版本数超限时，直接删除最旧版本。
    不需要 LLM 读取任何 flag，不需要 LLM 执行任何清理操作。
    本钩子直接在 Python 端完成清理，LLM 无权跳过。
    """
    output_path = ctx.get('output_path', '')
    if not output_path:
        return {'success': True, 'message': 'limit_checker: 无输出路径'}

    version_count = ctx.get('version_count', 0)
    max_versions = ctx.get('max_versions', 5)

    if version_count < max_versions:
        return {
            'success': True,
            'message': f'limit_checker: 版本数正常（{version_count}/{max_versions}），无需清理',
        }

    # ========== Python 端自动清理最旧版本 ==========
    try:
        vm = _get_vm(output_path)
        if vm is not None and version_count >= max_versions:
            changelog = vm.list_versions(output_path)
            while len(changelog) >= max_versions:
                oldest = changelog.pop(0)
                old_dir = Path(vm.versions_dir) / Path(output_path).stem / oldest['version']
                if old_dir.exists():
                    import shutil
                    shutil.rmtree(old_dir)
                    msg_part = f'已删除最旧版本 {oldest["version"]}（{oldest["timestamp"][:10]}）'
                else:
                    msg_part = f'版本 {oldest["version"]} 目录不存在，跳过'
            ctx['pruned'] = True
            msg = f'limit_checker: 版本数达上限（{version_count}/{max_versions}），{msg_part}'
        else:
            msg = f'limit_checker: 版本数正常（{version_count}/{max_versions}）'
    except Exception as e:
        msg = f'limit_checker: 检查完成（{version_count}/{max_versions}），清理异常: {e}'
    # ===========================================

    return {'success': True, 'message': msg}


# ---------- post_vc ----------

@register('post_vc', name='status_reporter',
          description='报告版本操作结果')
def _post_vc_report(ctx: dict) -> dict:
    vc_result = ctx.get('vc_result', {})
    if not vc_result:
        return {'success': True, 'message': 'status_reporter: 无版本操作'}
    version = vc_result.get('version', '?')
    desc = vc_result.get('description', '未知操作')
    return {
        'success': True,
        'message': f'status_reporter: v{version} - {desc}',
        'data': vc_result,
    }


# ============================================================
# 便捷入口
# ============================================================

def hooks(hook_point: str, context: dict | None = None) -> list[HookResult]:
    """一键触发钩子

    这是最常用的入口函数。等效于 execute()。

    用法：
        result = hooks('pre_think', {'user_input': 'draw a flowchart'})
        for r in result:
            print(r)
    """
    return execute(hook_point, context)


def validate_workflow(context: dict) -> list[dict]:
    """遍历所有 8 个 Hook Point 执行一次（用于初始化/自检）

    返回值：按 HookPoint 分组的执行结果列表
    """
    all_results = []
    for point in HookPoint:
        results = execute(point, context)
        for r in results:
            all_results.append(r.to_dict())
    return all_results


# ============================================================
# CLI
# ============================================================

def main():
    """CLI 入口：查看钩子状态"""
    import sys

    if len(sys.argv) < 2:
        print('drawio_hooks CLI')
        print()
        print('Usage:')
        print('  python drawio_hooks.py list       - List all registered hooks')
        print('  python drawio_hooks.py check      - Self-check (traverse all points)')
        print('  python drawio_hooks.py history    - View execution history')
        return

    cmd = sys.argv[1]

    if cmd == 'list':
        reg = registry()
        print(f'{"=" * 60}')
        print(f'drawio_hooks registry (total {sum(len(v) for v in reg.values())} hooks)')
        print(f'{"=" * 60}')
        for point, hooks_list in reg.items():
            label = HookPoint(point).label() if point in HookPoint._value2member_map_ else point
            print(f'\n[{label}] ({len(hooks_list)} hooks)')
            for h in hooks_list:
                print(f'  - {h["name"]}: {h["description"]}')

    elif cmd == 'check':
        print('All hook points self-check...')
        results = validate_workflow({'user_input': 'draw a flowchart'})
        print(f'\n{"=" * 60}')
        print(f'Check complete: {len(results)} results')
        print(f'{"=" * 60}')
        current_point = ''
        for r in results:
            if r['point'] != current_point:
                current_point = r['point']
                label = HookPoint(current_point).label()
                print(f'\n--- {label} ({current_point}) ---')
            icon = '[OK]' if r['success'] else ('[ABORT]' if r['abort'] else '[WARN]')
            print(f'  {icon} {r["name"]}: {r["message"]}')

    elif cmd == 'history':
        hist = history(50)
        if not hist:
            print('No execution history')
            return
        print(f'Recent {len(hist)} executions:')
        for h in hist:
            print(f'  {h["timestamp"]} | {h["point"]:15s} | {h["name"]:20s} | {h["message"]}')

    else:
        print(f'Unknown command: {cmd}')


if __name__ == '__main__':
    main()
