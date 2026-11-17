#!/usr/bin/env python3
"""提取损坏模块的代码信息，从 .pyc 重新构建 .py 文件"""

import sys
import os
import dis
import marshal
import types
import importlib
import importlib.util
import inspect

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

def extract_code_info(code, prefix="", depth=0):
    """递归提取代码对象信息"""
    info = {
        'name': code.co_name,
        'filename': code.co_filename,
        'argcount': code.co_argcount,
        'nlocals': code.co_nlocals,
        'varnames': code.co_varnames,
        'names': code.co_names,
        'consts_raw': code.co_consts,
    }
    
    # 处理常量 - 过滤出字符串常量、数字常量
    strings = []
    numbers = []
    code_objects = []
    for c in code.co_consts:
        if isinstance(c, str):
            strings.append(c)
        elif isinstance(c, (int, float, bool)):
            numbers.append(c)
        elif isinstance(c, type(None)):
            strings.append("None")
        elif isinstance(c, types.CodeType):
            code_objects.append(c)
    
    info['strings'] = strings
    info['numbers'] = numbers
    info['nested_codes'] = [extract_code_info(c, prefix + "  ", depth + 1) for c in code_objects]
    
    # 获取指令列表用于重建
    instructions = []
    for instr in dis.get_instructions(code):
        instructions.append({
            'offset': instr.offset,
            'opname': instr.opname,
            'arg': instr.arg,
            'argrepr': instr.argrepr if hasattr(instr, 'argrepr') else None,
        })
    info['instructions'] = instructions
    
    return info

def extract_module_functions(module_name):
    """从模块中提取所有函数和顶级代码"""
    try:
        # 先尝试清理缓存
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        mod = importlib.import_module(module_name)
        print(f"成功加载模块: {module_name}", file=sys.stderr)
        return mod
    except Exception as e:
        print(f"importlib 加载失败: {e}", file=sys.stderr)
        return None

def dump_marshal(pyc_path):
    """直接通过 marshal 加载 .pyc 文件"""
    with open(pyc_path, 'rb') as f:
        # 跳过 16 字节 .pyc 头部
        header = f.read(16)
        code_obj = marshal.load(f)
    return code_obj

def format_instructions(instructions, indent=""):
    """格式化字节码指令"""
    lines = []
    for instr in instructions:
        argrepr = instr.get('argrepr', '')
        arg = instr.get('arg')
        if argrepr and arg is not None:
            lines.append(f"{indent}  {instr['offset']:4d}: {instr['opname']:25s} {arg:5d} ({argrepr})")
        elif arg is not None:
            lines.append(f"{indent}  {instr['offset']:4d}: {instr['opname']:25s} {arg}")
        else:
            lines.append(f"{indent}  {instr['offset']:4d}: {instr['opname']}")
    return "\n".join(lines)

def reconstruct_function_source(func, info, name=""):
    """根据代码对象信息重建函数源代码"""
    code = func.__code__
    if not name:
        name = code.co_name
    
    # 获取函数的默认参数值和签名
    sig_parts = []
    varnames = code.co_varnames
    
    # 构建参数列表
    argcount = code.co_argcount
    defaults = func.__defaults__
    kwdefaults = func.__kwdefaults__
    
    for i in range(argcount):
        varname = varnames[i] if i < len(varnames) else f"arg{i}"
        sig_parts.append(varname)
    
    if code.co_flags & 0x08:  # CO_VARARGS
        sig_parts.append(f"*{varnames[argcount]}")
    if code.co_flags & 0x04:  # CO_VARKEYWORDS
        idx = argcount + (1 if code.co_flags & 0x08 else 0)
        sig_parts.append(f"**{varnames[idx]}")
    
    sig = ", ".join(sig_parts)
    
    lines = []
    lines.append(f"def {name}({sig}):")
    
    # 提取 docstring
    consts = code.co_consts
    docstring = ""
    if consts and isinstance(consts[0], str):
        docstring = consts[0]
    
    if docstring:
        lines.append(f'    """{docstring}"""')
    
    # 输出字节码注释
    lines.append(f"    # 字节码指令:")
    for instr in dis.get_instructions(code):
        lines.append(f"    #   {instr.opname:25s} {instr.argrepr or ''}")
    
    lines.append(f"    # 局部变量: {list(varnames)}")
    lines.append(f"    # 引用的全局名称: {list(code.co_names)}")
    
    # 输出字符串常量
    str_consts = [repr(c) for c in consts if isinstance(c, str)]
    if str_consts:
        lines.append(f"    # 字符串常量:")
        for s in str_consts[:20]:
            if len(s) < 80:
                lines.append(f"    #   {s}")
    
    lines.append("    pass  # TODO: 从字节码还原\n")
    
    return "\n".join(lines)

def reconstruct_full_source(module, module_name, pyc_path=None):
    """从模块对象重建完整的 .py 源代码"""
    lines = []
    
    # 文件头
    lines.append('"""')
    lines.append(f"自动从 .pyc 重建 - {module_name}")
    lines.append(f"重建时间: 2026-07-14")
    lines.append('"""')
    lines.append("")
    
    # 检查模块的 __all__ 或直接列出所有可调用对象
    all_names = []
    if hasattr(module, '__all__'):
        all_names = module.__all__
    else:
        all_names = [name for name in dir(module) if not name.startswith('_') or name == '__all__']
    
    # 提取所有函数和类
    functions = {}
    classes = {}
    constants = {}
    
    for name in dir(module):
        if name.startswith('_') and name not in ('__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__'):
            continue
        try:
            obj = getattr(module, name)
            if isinstance(obj, types.FunctionType):
                functions[name] = obj
            elif isinstance(obj, type):
                classes[name] = obj
            elif not name.startswith('_'):
                constants[name] = obj
        except Exception:
            pass
    
    # 输出字符串常量  
    lines.append("# ===== 字符串常量 (co_consts) =====")
    lines.append("")
    
    # 输出函数
    if functions:
        lines.append("# ===== 函数 =====")
        lines.append("")
        for fname in sorted(functions.keys()):
            func = functions[fname]
            lines.append(reconstruct_function_source(func, None, fname))
    
    # 输出类
    if classes:
        lines.append("# ===== 类 =====")
        lines.append("")
        for cname in sorted(classes.keys()):
            cls = classes[cname]
            # 查找类的方法
            methods = []
            for mname in dir(cls):
                if not mname.startswith('__'):
                    mobj = getattr(cls, mname)
                    if isinstance(mobj, (types.FunctionType, classmethod, staticmethod)):
                        methods.append((mname, mobj))
            
            # 尝试找基类
            bases = cls.__bases__
            if bases != (object,):
                base_str = "(" + ", ".join(b.__name__ for b in bases if b != object) + ")"
            else:
                base_str = ""
            
            lines.append(f"class {cname}{base_str}:")
            
            doc = cls.__doc__
            if doc:
                lines.append(f'    """{doc}"""')
                lines.append("")
            
            for mname, mobj in methods:
                if isinstance(mobj, classmethod):
                    lines.append("    @classmethod")
                    lines.append(reconstruct_function_source(mobj.__func__, None, mname).replace("def ", "    def "))
                elif isinstance(mobj, staticmethod):
                    lines.append("    @staticmethod")
                    lines.append(reconstruct_function_source(mobj.__func__, None, mname).replace("def ", "    def "))
                else:
                    lines.append(reconstruct_function_source(mobj, None, mname).replace("def ", "    def "))
            
            if not methods:
                lines.append("    pass")
                lines.append("")
    
    # 输出模块级常量
    if constants:
        lines.append("# ===== 模块级常量 =====")
        lines.append("")
        for cname in sorted(constants.keys()):
            cval = constants[cname]
            if isinstance(cval, str):
                lines.append(f'{cname} = {repr(cval)}')
            elif isinstance(cval, (int, float, bool)):
                lines.append(f'{cname} = {cval}')
            elif cval is None:
                lines.append(f'{cname} = None')
    
    return "\n".join(lines)

def reconstruct_via_marshal(pyc_path, module_name):
    """直接通过 marshal 加载并重建"""
    with open(pyc_path, 'rb') as f:
        header = f.read(16)
        code_obj = marshal.load(f)
    
    return walk_code_object(code_obj, module_name)

def walk_code_object(code, module_name="", depth=0):
    """遍历代码对象并生成源码"""
    indent = "    " * depth
    lines = []
    
    name = code.co_name
    if name == '<module>':
        lines.append(f'"""Auto-reconstructed from .pyc: {module_name}"""')
        lines.append("")
    
    # 收集所有嵌套的代码对象（函数、类方法）
    nested_funcs = []
    nested_classes = []
    strings = []
    other_consts = []
    
    for c in code.co_consts:
        if isinstance(c, types.CodeType):
            if c.co_name == '<lambda>':
                nested_funcs.append(('lambda', c))
            elif c.co_name and c.co_name[0].isupper():
                nested_classes.append((c.co_name, c))
            else:
                nested_funcs.append((c.co_name, c))
        elif isinstance(c, str):
            strings.append(c)
        else:
            other_consts.append(c)
    
    if name == '<module>':
        # 输出模块级字符串常量
        lines.append("")
        lines.append("# ===== 字符串常量 =====")
        for s in strings:
            if len(s) < 100:
                lines.append(f"# {repr(s)}")
        lines.append("")
        
        # 输出模块级其他常量
        for i, c in enumerate(other_consts[:20]):
            lines.append(f"# const[{i}]: {repr(c)}")
        lines.append("")
        
        # 递归处理所有嵌套函数
        for fname, fcode in nested_funcs:
            lines.extend(walk_code_object(fcode, fname, depth))
        
        return "\n".join(lines)
    
    # 这是一个函数
    lines.append(f"# ---- 函数: {name} ----")
    
    # 提取 docstring
    docstr = ""
    if code.co_consts and isinstance(code.co_consts[0], str):
        docstr = code.co_consts[0]
    
    # 构建签名
    argcount = code.co_argcount
    varnames = code.co_varnames
    posonly = code.co_posonlyargcount if hasattr(code, 'co_posonlyargcount') else 0
    kwonly = code.co_kwonlyargcount if hasattr(code, 'co_kwonlyargcount') else 0
    
    args = list(varnames[:argcount])
    sig = ", ".join(args)
    
    lines.append(f"# 签名: {name}({sig})")
    lines.append(f"# argcount={argcount}, nlocals={code.co_nlocals}")
    lines.append(f"# varnames: {list(varnames)}")
    lines.append(f"# names (globals): {list(code.co_names)}")
    
    if strings:
        lines.append(f"# strings:")
        for s in strings[:15]:
            if len(s) < 120:
                lines.append(f"#   {repr(s)}")
    
    lines.append(f"# bytecode:")
    for instr in dis.get_instructions(code):
        lines.append(f"#   {instr.offset:4d}: {instr.opname:25s} {instr.argrepr or ''}")
    
    # 递归处理嵌套函数（闭包）
    for fname, fcode in [(n, c) for n, c in nested_funcs]:
        lines.extend(walk_code_object(fcode, fname, depth + 1))
    
    # 生成 stub
    lines.append(f"def {name}({sig}):")
    if docstr:
        lines.append(f'    """{docstr}"""')
    if strings:
        lines.append(f"    # TODO: 还原逻辑")
    lines.append(f"    ...")
    lines.append("")
    
    return lines


def main():
    import sys
    
    modules_to_extract = [
        ('project_commands.__init__', os.path.join(BASE, 'project_commands', '__pycache__', '__init__.cpython-313.pyc')),
        ('video_utils', os.path.join(BASE, '__pycache__', 'video_utils.cpython-313.pyc')),
    ]
    
    for module_name, pyc_path in modules_to_extract:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"处理模块: {module_name}", file=sys.stderr)
        print(f"pyc 路径: {pyc_path}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        
        # 尝试方法1: 从模块导入
        mod = extract_module_functions(module_name)
        
        if mod is not None:
            print(f"从 .pyc 成功加载模块 {module_name}", file=sys.stderr)
            source = reconstruct_full_source(mod, module_name)
            
            output_path = pyc_path.replace('.cpython-313.pyc', '.reconstructed.py')
            # Fix path for video_utils
            if 'video_utils' in module_name:
                output_path = os.path.join(BASE, 'video_utils.reconstructed.py')
            elif 'project_commands' in module_name:
                output_path = os.path.join(BASE, 'project_commands', '__init__.reconstructed.py')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(source)
            print(f"已写入: {output_path} ({len(source)} chars)", file=sys.stderr)
        else:
            # 尝试方法2: 直接 marshal
            print(f"模块导入失败，尝试 marshal 直接加载...", file=sys.stderr)
            try:
                result = reconstruct_via_marshal(pyc_path, module_name)
                
                if 'video_utils' in module_name:
                    output_path = os.path.join(BASE, 'video_utils.reconstructed.py')
                elif 'project_commands' in module_name:
                    output_path = os.path.join(BASE, 'project_commands', '__init__.reconstructed.py')
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result if isinstance(result, str) else "\n".join(result))
                print(f"已通过 marshal 重建: {output_path}", file=sys.stderr)
            except Exception as e2:
                print(f"marshal 方法也失败: {e2}", file=sys.stderr)
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    main()
