#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Manager Service - 文件管理服务
提供 .openclaw/workspace/projects 目录的文件浏览、查看、删除、创建功能
"""

import os
import json
import shutil
import mimetypes
import zipfile
import io
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from datetime import datetime

app = Flask(__name__)

# 基础路径配置 - 使用用户家目录
HOME_DIR = Path.home()  # macOS: /Users/lengyanhua, Linux: /home/xxx
BASE_DIR = HOME_DIR / '.openclaw/workspace/projects'
NOTES_FILE = BASE_DIR / '.directory_notes.json'
ALLOWED_EXTENSIONS = {'.txt', '.md', '.html', '.py', '.js', '.json', '.yaml', '.yml', '.css', '.xml', '.log', '.sh', '.bash', '.sql', '.java', '.go', '.rs', '.ts', '.jsx', '.tsx', '.htm', '.svg'}


def load_notes():
    """加载目录备注"""
    if NOTES_FILE.exists():
        try:
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_notes(notes):
    """保存目录备注"""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def get_file_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_info(path: Path) -> dict:
    """获取文件信息"""
    try:
        stat = path.stat()
        return {
            'name': path.name,
            'path': str(path.relative_to(BASE_DIR)),
            'type': 'file',
            'size': stat.st_size,
            'size_formatted': get_file_size(stat.st_size),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'extension': path.suffix.lower(),
            'is_text': path.suffix.lower() in ALLOWED_EXTENSIONS
        }
    except Exception as e:
        return {'name': path.name, 'path': str(path), 'type': 'file', 'error': str(e)}


def get_dir_info(path: Path, notes: dict = None) -> dict:
    """获取目录信息"""
    try:
        stat = path.stat()
        items = list(path.iterdir())
        rel_path = str(path.relative_to(BASE_DIR))
        note = notes.get(rel_path, '') if notes else ''
        return {
            'name': path.name,
            'path': rel_path,
            'type': 'directory',
            'items_count': len(items),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'note': note,
            'has_note': len(note) > 0
        }
    except Exception as e:
        return {'name': path.name, 'path': str(path), 'type': 'directory', 'error': str(e)}


def scan_directory(path: Path) -> dict:
    """扫描目录内容"""
    notes = load_notes()
    result = {
        'current': get_dir_info(path, notes),
        'parent': None,
        'directories': [],
        'files': []
    }
    
    # 父目录信息
    if path != BASE_DIR and path.parent != BASE_DIR.parent:
        result['parent'] = {
            'name': '..',
            'path': str(path.parent.relative_to(BASE_DIR)) if path.parent != BASE_DIR else ''
        }
    
    # 扫描子项
    try:
        for item in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                result['directories'].append(get_dir_info(item, notes))
            else:
                result['files'].append(get_file_info(item))
    except PermissionError:
        result['error'] = '无权限访问此目录'
    
    return result


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/files')
def list_files():
    """列出文件"""
    path_param = request.args.get('path', '')
    path = BASE_DIR / path_param if path_param else BASE_DIR
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists():
        return jsonify({'error': '路径不存在'}), 404
    
    return jsonify(scan_directory(path))


@app.route('/api/file/content')
def get_file_content():
    """获取文件内容"""
    path_param = request.args.get('path', '')
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists():
        return jsonify({'error': '文件不存在'}), 404
    
    if path.is_dir():
        return jsonify({'error': '不是文件'}), 400
    
    # 检查文件扩展名
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': '不支持的文件类型', 'preview': False}), 400
    
    try:
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = path.read_text(encoding='gbk')
        
        return jsonify({
            'success': True,
            'path': str(path.relative_to(BASE_DIR)),
            'name': path.name,
            'size': path.stat().st_size,
            'size_formatted': get_file_size(path.stat().st_size),
            'content': content,
            'extension': path.suffix.lower()
        })
    except Exception as e:
        return jsonify({'error': f'读取失败：{str(e)}'}), 500


@app.route('/api/file/download')
def download_file():
    """下载文件"""
    path_param = request.args.get('path', '')
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists() or path.is_dir():
        return jsonify({'error': '文件不存在'}), 404
    
    return send_file(path, as_attachment=False)


@app.route('/api/file/open')
def open_file():
    """在新标签页打开文件"""
    path_param = request.args.get('path', '')
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists() or path.is_dir():
        return jsonify({'error': '文件不存在'}), 404
    
    browser_renderable = {'.html', '.htm', '.svg', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp'}
    if path.suffix.lower() not in browser_renderable:
        return jsonify({'error': '此文件类型不支持在浏览器中直接打开'}), 400
    
    return send_file(path, mimetype=None)


@app.route('/api/delete', methods=['POST'])
def delete_item():
    """删除文件或目录"""
    data = request.get_json()
    path_param = data.get('path', '')
    
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists():
        return jsonify({'error': '路径不存在'}), 404
    
    if path == BASE_DIR:
        return jsonify({'error': '不能删除根目录'}), 403
    
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        
        return jsonify({'success': True, 'message': f'已删除：{path_param}'})
    except Exception as e:
        return jsonify({'error': f'删除失败：{str(e)}'}), 500


@app.route('/api/create/dir', methods=['POST'])
def create_directory():
    """创建目录（支持递归创建父目录）"""
    data = request.get_json()
    path_param = data.get('path', '')
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({'error': '目录名不能为空'}), 400
    
    # 过滤非法字符
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            return jsonify({'error': f'目录名包含非法字符：{char}'}), 400
    
    base_path = BASE_DIR / path_param if path_param else BASE_DIR
    
    # 安全校验
    try:
        base_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    new_path = base_path / name
    
    # 递归创建父目录（如果不存在）
    if not base_path.exists():
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return jsonify({'error': f'创建父目录失败：{str(e)}'}), 500
    
    if new_path.exists():
        return jsonify({'error': '目录已存在'}), 409
    
    try:
        new_path.mkdir(parents=True, exist_ok=True)
        return jsonify({
            'success': True,
            'message': f'已创建目录：{name}',
            'path': str(new_path.relative_to(BASE_DIR))
        })
    except Exception as e:
        return jsonify({'error': f'创建失败：{str(e)}'}), 500


@app.route('/api/create/file', methods=['POST'])
def create_file():
    """创建文件（支持递归创建父目录）"""
    data = request.get_json()
    path_param = data.get('path', '')
    name = data.get('name', '').strip()
    content = data.get('content', '')
    
    if not name:
        return jsonify({'error': '文件名不能为空'}), 400
    
    # 过滤非法字符
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            return jsonify({'error': f'文件名包含非法字符：{char}'}), 400
    
    # 检查扩展名
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': f'不支持的文件类型：{ext}'}), 400
    
    base_path = BASE_DIR / path_param if path_param else BASE_DIR
    
    # 安全校验
    try:
        base_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    new_path = base_path / name
    
    # 递归创建父目录（如果不存在）
    if not base_path.exists():
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return jsonify({'error': f'创建父目录失败：{str(e)}'}), 500
    
    if new_path.exists():
        return jsonify({'error': '文件已存在'}), 409
    
    try:
        new_path.write_text(content, encoding='utf-8')
        return jsonify({
            'success': True,
            'message': f'已创建文件：{name}',
            'path': str(new_path.relative_to(BASE_DIR))
        })
    except Exception as e:
        return jsonify({'error': f'创建失败：{str(e)}'}), 500


@app.route('/api/file/save', methods=['POST'])
def save_file():
    """保存文件"""
    data = request.get_json()
    path_param = data.get('path', '')
    content = data.get('content', '')
    
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if path.is_dir():
        return jsonify({'error': '不能保存为目录'}), 400
    
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': '不支持的文件类型'}), 400
    
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        
        return jsonify({
            'success': True,
            'message': '文件已保存',
            'path': str(path.relative_to(BASE_DIR)),
            'size': len(content.encode('utf-8'))
        })
    except Exception as e:
        return jsonify({'error': f'保存失败：{str(e)}'}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件（支持单文件，不限制文件类型）"""
    if 'file' not in request.files:
        return jsonify({'error': '缺少文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    path_param = request.form.get('path', '')
    base_path = BASE_DIR / path_param if path_param else BASE_DIR
    
    # 安全校验
    try:
        base_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    # 递归创建父目录（如果不存在）
    if not base_path.exists():
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return jsonify({'error': f'创建父目录失败：{str(e)}'}), 500
    
    new_path = base_path / file.filename
    
    # 如果文件已存在，添加序号
    if new_path.exists():
        base_name = new_path.stem
        suffix = new_path.suffix
        parent = new_path.parent
        counter = 1
        while new_path.exists():
            new_name = f"{base_name}_{counter}{suffix}"
            new_path = parent / new_name
            counter += 1
    
    try:
        file.save(str(new_path))
        return jsonify({
            'success': True,
            'message': f'已上传：{file.filename}',
            'path': str(new_path.relative_to(BASE_DIR)),
            'size': new_path.stat().st_size
        })
    except Exception as e:
        return jsonify({'error': f'上传失败：{str(e)}'}), 500


@app.route('/api/upload-folder', methods=['POST'])
def upload_folder():
    """上传文件夹（多个文件，支持目录结构）"""
    import sys
    sys.stdout.flush()
    print(f"[UPLOAD] 收到上传请求", flush=True)
    print(f"[UPLOAD] request.files: {list(request.files.keys())}", flush=True)
    print(f"[UPLOAD] request.form: {dict(request.form)}", flush=True)
    
    if 'files[]' not in request.files:
        print("[UPLOAD] 错误：缺少 files[]")
        return jsonify({'error': '缺少文件', 'debug': list(request.files.keys())}), 400
    
    files = request.files.getlist('files[]')
    print(f"[UPLOAD] 文件数量：{len(files)}", flush=True)
    
    if not files:
        print("[UPLOAD] 错误：文件列表为空")
        return jsonify({'error': '没有文件'}), 400
    
    path_param = request.form.get('path', '')
    base_path = BASE_DIR / path_param if path_param else BASE_DIR
    print(f"[UPLOAD] 目标路径：{base_path}", flush=True)
    
    # 安全校验
    try:
        base_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    # 递归创建父目录（如果不存在）
    if not base_path.exists():
        try:
            base_path.mkdir(parents=True, exist_ok=True)
            print(f"[UPLOAD] 创建目录：{base_path}", flush=True)
        except Exception as e:
            return jsonify({'error': f'创建父目录失败：{str(e)}'}), 500
    
    uploaded = []
    errors = []
    
    for file in files:
        print(f"[UPLOAD] 处理文件：{file.filename} ({file.content_length} bytes)", flush=True)
        
        if file.filename == '':
            continue
        
        # 处理目录结构（webkitdirectory 上传时会包含相对路径）
        file_path = Path(file.filename)
        
        # 安全检查：防止路径遍历攻击
        try:
            safe_path = base_path / file_path
            safe_path.resolve().relative_to(base_path.resolve())
            new_path = safe_path
        except ValueError:
            errors.append(f'{file.filename}: 非法路径')
            continue
        
        # 创建父目录
        try:
            new_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f'{file.filename}: 创建目录失败 - {str(e)}')
            continue
        
        # 如果文件已存在，添加序号
        if new_path.exists():
            base_name = new_path.stem
            suffix = new_path.suffix
            parent = new_path.parent
            counter = 1
            while new_path.exists():
                new_name = f"{base_name}_{counter}{suffix}"
                new_path = parent / new_name
                counter += 1
        
        try:
            file.save(str(new_path))
            uploaded.append(str(new_path.relative_to(BASE_DIR)))
            print(f"[UPLOAD] 已保存：{new_path}", flush=True)
        except Exception as e:
            errors.append(f'{file.filename}: {str(e)}')
            print(f"[UPLOAD] 保存失败：{e}", flush=True)
    
    result = {
        'success': len(errors) == 0,
        'uploaded': uploaded,
        'errors': errors,
        'message': f'已上传 {len(uploaded)} 个文件' + (f' ({len(errors)} 错误)' if errors else '')
    }
    print(f"[UPLOAD] 结果：{result}", flush=True)
    return jsonify(result)


@app.route('/api/notes/get', methods=['GET'])
def get_note():
    """获取目录备注"""
    path_param = request.args.get('path', '')
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    notes = load_notes()
    note = notes.get(path_param, '')
    
    return jsonify({
        'success': True,
        'path': path_param,
        'note': note
    })


@app.route('/api/notes/save', methods=['POST'])
def save_note():
    """保存目录备注"""
    data = request.get_json()
    path_param = data.get('path', '')
    note = data.get('note', '')
    
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    # 安全校验 - 只允许第一级子目录
    if '/' in path_param:
        return jsonify({'error': '只能为第一级子目录添加备注'}), 400
    
    notes = load_notes()
    
    if note.strip():
        notes[path_param] = note.strip()
    else:
        notes.pop(path_param, None)
    
    try:
        save_notes(notes)
        return jsonify({
            'success': True,
            'message': '备注已保存',
            'path': path_param,
            'note': note.strip()
        })
    except Exception as e:
        return jsonify({'error': f'保存失败：{str(e)}'}), 500


@app.route('/api/stats')
def get_stats():
    """获取统计信息"""
    total_files = 0
    total_dirs = 0
    total_size = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        total_dirs += len(dirs)
        for f in files:
            if not f.startswith('.'):
                total_files += 1
                try:
                    total_size += os.path.getsize(os.path.join(root, f))
                except:
                    pass
    
    return jsonify({
        'base_dir': str(BASE_DIR),
        'total_files': total_files,
        'total_dirs': total_dirs,
        'total_size': get_file_size(total_size),
        'total_size_bytes': total_size
    })


@app.route('/api/search')
def search_files():
    """搜索文件（支持正则表达式）"""
    query = request.args.get('q', '')
    use_regex = request.args.get('regex', 'false').lower() == 'true'
    
    if not query:
        return jsonify({'error': '缺少搜索关键词'}), 400
    
    results = {'files': [], 'directories': []}
    notes = load_notes()
    
    # 编译正则表达式（如果启用）
    pattern = None
    if use_regex:
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error as e:
            return jsonify({'error': f'正则表达式无效：{str(e)}'}), 400
    
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for name in files + dirs:
            # 正则匹配或简单包含匹配
            matched = False
            if use_regex and pattern:
                matched = pattern.search(name) is not None
            else:
                matched = query.lower() in name.lower()
            
            if matched:
                full_path = Path(root) / name
                if full_path.is_dir():
                    results['directories'].append(get_dir_info(full_path, notes))
                else:
                    results['files'].append(get_file_info(full_path))
    
    return jsonify(results)


@app.route('/api/move', methods=['POST'])
def move_item():
    """移动文件或目录"""
    data = request.get_json()
    source_path = data.get('source', '')
    dest_path = data.get('dest', '')
    
    if not source_path:
        return jsonify({'error': '缺少源路径'}), 400
    
    if not dest_path:
        return jsonify({'error': '缺少目标路径'}), 400
    
    source = BASE_DIR / source_path
    dest = BASE_DIR / dest_path
    
    # 安全校验 - 源路径
    try:
        source.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法源路径'}), 403
    
    # 安全校验 - 目标路径
    try:
        dest.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法目标路径'}), 403
    
    if not source.exists():
        return jsonify({'error': '源路径不存在'}), 404
    
    if source == BASE_DIR:
        return jsonify({'error': '不能移动根目录'}), 403
    
    # 确保目标目录存在
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # 如果目标已存在，添加序号避免覆盖
    if dest.exists():
        base_name = dest.stem
        suffix = dest.suffix
        parent = dest.parent
        counter = 1
        while dest.exists():
            new_name = f"{base_name}_{counter}{suffix}"
            dest = parent / new_name
            counter += 1
    
    try:
        shutil.move(str(source), str(dest))
        
        return jsonify({
            'success': True,
            'message': f'已移动：{source_path} → {dest.relative_to(BASE_DIR)}',
            'new_path': str(dest.relative_to(BASE_DIR))
        })
    except Exception as e:
        return jsonify({'error': f'移动失败：{str(e)}'}), 500


@app.route('/api/tree')
def get_directory_tree():
    """获取目录树结构（用于移动/下载选择）"""
    path_param = request.args.get('path', '')
    base_path = BASE_DIR / path_param if path_param else BASE_DIR
    
    # 安全校验
    try:
        base_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not base_path.exists():
        return jsonify({'error': '路径不存在'}), 404
    
    def build_tree(path: Path, depth=0, max_depth=5):
        """递归构建目录树"""
        if depth > max_depth:
            return None
        
        result = []
        try:
            for item in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
                if item.name.startswith('.'):
                    continue
                if item.is_dir():
                    node = {
                        'name': item.name,
                        'path': str(item.relative_to(BASE_DIR)),
                        'type': 'directory'
                    }
                    if depth < max_depth:
                        node['children'] = build_tree(item, depth + 1, max_depth)
                    result.append(node)
        except PermissionError:
            pass
        
        return result
    
    tree = build_tree(base_path)
    return jsonify({
        'name': base_path.name if path_param else 'projects',
        'path': path_param or '.',
        'type': 'directory',
        'children': tree
    })


@app.route('/api/download', methods=['GET'])
def download_item():
    """下载文件或目录（目录会打包成 zip）"""
    path_param = request.args.get('path', '')
    
    if not path_param:
        return jsonify({'error': '缺少路径参数'}), 400
    
    path = BASE_DIR / path_param
    
    # 安全校验
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'error': '非法路径'}), 403
    
    if not path.exists():
        return jsonify({'error': '路径不存在'}), 404
    
    try:
        if path.is_dir():
            # 目录：打包成 zip
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(path):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    for file in files:
                        if not file.startswith('.'):
                            file_path = Path(root) / file
                            arcname = str(file_path.relative_to(BASE_DIR))
                            zipf.write(file_path, arcname)
            
            zip_buffer.seek(0)
            from flask import make_response
            response = make_response(zip_buffer.read())
            response.headers['Content-Type'] = 'application/zip'
            response.headers['Content-Disposition'] = f'attachment; filename="{path.name}.zip"'
            return response
        else:
            # 文件：直接下载
            from flask import make_response
            with open(path, 'rb') as f:
                content = f.read()
            response = make_response(content)
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = f'attachment; filename="{path.name}"'
            return response
    except Exception as e:
        return jsonify({'error': f'下载失败：{str(e)}'}), 500


if __name__ == '__main__':
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    
    print(f"📁 File Manager Service")
    print(f"📂 Base Directory: {BASE_DIR}")
    print(f"🌐 Starting server at http://127.0.0.1:8888")
    print(f"✨ Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=8888, debug=False)
