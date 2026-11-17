# 详细参考 - file-browser-tool-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
import os
import subprocess
from datetime import datetime

class DirectoryBrowser:
    """目录浏览器（免费版）"""

    def list_directory(self, path=".", show_hidden=False, long_format=False):
        """列出目录内容"""
        try:
            entries = os.listdir(path)
            if not show_hidden:
                entries = [e for e in entries if not e.startswith('.')]

            if long_format:
                result = []
                for entry in sorted(entries):
                    full_path = os.path.join(path, entry)
                    stat = os.stat(full_path)
                    result.append({
                        'name': entry,
                        'type': 'dir' if os.path.isdir(full_path) else 'file',
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                        'permissions': oct(stat.st_mode)[-3:]
                    })
                return result
            else:
                return sorted(entries)
        except PermissionError:
            return f"无权限访问：{path}"
        except FileNotFoundError:
            return f"目录不存在：{path}"

    def tree(self, path=".", max_depth=3, current_depth=0):
        """树形结构"""
        if current_depth >= max_depth:
            return ""

        result = []
        prefix = "  " * current_depth
        try:
            entries = sorted(os.listdir(path))
            entries = [e for e in entries if not e.startswith('.')]

            for i, entry in enumerate(entries):
                full_path = os.path.join(path, entry)
                is_last = (i == len(entries) - 1)

                connector = "└── " if is_last else "├── "
                if os.path.isdir(full_path):
                    result.append(f"{prefix}{connector}{entry}/")
                    subtree = self.tree(full_path, max_depth, current_depth + 1)
                    if subtree:
                        result.append(subtree)
                else:
                    result.append(f"{prefix}{connector}{entry}")
        except PermissionError:
            result.append(f"{prefix}[无权限]")
        return "\n".join(result)

    def get_file_info(self, filepath):
        """获取文件信息"""
        try:
            stat = os.stat(filepath)
            return {
                'name': os.path.basename(filepath),
                'path': os.path.abspath(filepath),
                'type': 'directory' if os.path.isdir(filepath) else 'file',
                'size': stat.st_size,
                'size_human': self._human_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'accessed': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                'permissions': oct(stat.st_mode)[-3:]
            }
        except FileNotFoundError:
            return f"文件不存在：{filepath}"

    def _human_size(self, size):
        """人类可读的大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

browser = DirectoryBrowser()

print("=== 当前目录 ===")
files = browser.list_directory(".", long_format=True)
for f in files[:5]:
    print(f"  {f['name']:20} {f['type']:5} {f['size_human']:>10}")

print("\n=== 目录树 ===")
print(browser.tree(".", max_depth=2))

print("\n=== 文件信息 ===")
info = browser.get_file_info("README.md")
print(info)
```

## 代码示例 (python)

```python
import fnmatch

class FileSearcher:
    """文件搜索器（免费版）"""

    def find_by_name(self, root_dir, pattern, max_results=100):
        """按文件名搜索"""
        results = []
        try:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]

                for filename in filenames:
                    if fnmatch.fnmatch(filename, pattern):
                        full_path = os.path.join(dirpath, filename)
                        results.append(full_path)
                        if len(results) >= max_results:
                            return results
        except PermissionError:
            pass
        return results

    def find_by_extension(self, root_dir, extension, max_results=100):
        """按扩展名搜索"""
        if not extension.startswith('.'):
            extension = '.' + extension
        return self.find_by_name(root_dir, f"*{extension}", max_results)

    def search_in_files(self, root_dir, pattern, file_pattern="*", max_results=50):
        """在文件内容中搜索"""
        import re
        results = []

        try:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]

                for filename in filenames:
                    if not fnmatch.fnmatch(filename, file_pattern):
                        continue

                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if re.search(pattern, line):
                                    results.append({
                                        'file': filepath,
                                        'line': line_num,
                                        'content': line.rstrip()[:200]
                                    })
                                    if len(results) >= max_results:
                                        return results
                    except:
                        continue
        except PermissionError:
            pass

        return results

    def find_large_files(self, root_dir, min_size_mb=10, max_results=20):
        """查找大文件"""
        min_size = min_size_mb * 1024 * 1024
        results = []

        try:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        size = os.path.getsize(filepath)
                        if size >= min_size:
                            results.append({
                                'file': filepath,
                                'size': size,
                                'size_mb': size / (1024 * 1024)
                            })
                    except:
                        continue
        except PermissionError:
            pass

        results.sort(key=lambda x: x['size'], reverse=True)
        return results[:max_results]

searcher = FileSearcher()

print("=== 查找 .py 文件 ===")
py_files = searcher.find_by_extension(".", "py", max_results=10)
for f in py_files[:5]:
    print(f"  {f}")

print("\n=== 搜索 TODO ===")
results = searcher.search_in_files(".", "TODO", "*.py", max_results=5)
for r in results[:3]:
    print(f"  {r['file']}:{r['line']} - {r['content'][:80]}")
```

## 代码示例 (python)

```python
import shutil

class FileOperations:
    """文件操作（免费版）"""

    def copy(self, src, dst):
        """复制文件/目录"""
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return {"success": True, "message": f"已复制 {src} → {dst}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def move(self, src, dst):
        """移动文件/目录"""
        try:
            shutil.move(src, dst)
            return {"success": True, "message": f"已移动 {src} → {dst}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, path):
        """删除文件/目录"""
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return {"success": True, "message": f"已删除 {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def rename(self, src, dst):
        """重命名"""
        try:
            os.rename(src, dst)
            return {"success": True, "message": f"已重命名 {src} → {dst}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def mkdir(self, path, parents=True):
        """创建目录"""
        try:
            if parents:
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
            return {"success": True, "message": f"已创建目录 {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def touch(self, filepath):
        """创建空文件"""
        try:
            with open(filepath, 'a'):
                os.utime(filepath, None)
            return {"success": True, "message": f"已创建 {filepath}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

ops = FileOperations()

print(ops.mkdir("./test_dir"))

print(ops.touch("./test_dir/test.txt"))

print(ops.copy("./test_dir/test.txt", "./test_dir/test_copy.txt"))

print(ops.rename("./test_dir/test_copy.txt", "./test_dir/renamed.txt"))
```

