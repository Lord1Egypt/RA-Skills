import ctypes
import datetime
import struct
import os
import base64
import sys
import io

# 修复 Windows 控制台中文乱码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100

WINDOWS_TICKS = int(1/10**-7)
WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS

search_results = []
everything_dll = None

def get_time(filetime):
    winticks = struct.unpack('<Q', filetime)[0]
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    try:
        return datetime.datetime.fromtimestamp(microsecs)
    except:
        return None

def initialize_everything():
    global everything_dll
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, "libs", "Everything64.dll"),
        os.path.join(script_dir, "libs", "Everything32.dll"),
        os.path.join(script_dir, "Everything64.dll"),
        os.path.join(script_dir, "Everything32.dll"),
        r"C:\Program Files\Everything\Everything64.dll",
        r"C:\Program Files\Everything\Everything32.dll",
        r"C:\EverythingSDK\DLL\Everything64.dll",
        r"C:\EverythingSDK\DLL\Everything32.dll"
    ]
    
    for dll_path in possible_paths:
        if os.path.exists(dll_path):
            try:
                everything_dll = ctypes.WinDLL(dll_path)
                everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
                everything_dll.Everything_GetResultDateCreated.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
                everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
                everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
                everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p
                return True
            except:
                continue
    return False

def search_files(query):
    global search_results, everything_dll
    
    if everything_dll is None:
        if not initialize_everything():
            return {
                "status": "error",
                "message": "未找到 Everything SDK，请：\n1. 确保 Everything 软件已安装且正在运行\n2. 将 Everything SDK (Everything32.dll 或 Everything64.dll) 放置在技能目录的 libs 文件夹中或技能根目录下"
            }
    
    search_results = []
    
    request_flags = (
        EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME |
        EVERYTHING_REQUEST_SIZE |
        EVERYTHING_REQUEST_DATE_CREATED |
        EVERYTHING_REQUEST_DATE_MODIFIED
    )
    
    everything_dll.Everything_SetSearchW(query)
    everything_dll.Everything_SetRequestFlags(request_flags)
    everything_dll.Everything_SetMax(10)
    everything_dll.Everything_QueryW(1)
    
    num_results = everything_dll.Everything_GetNumResults()
    
    if num_results == 0:
        return {
            "status": "success",
            "message": "未找到匹配的文件。"
        }
    
    filename = ctypes.create_unicode_buffer(260)
    date_created_filetime = ctypes.c_ulonglong(1)
    date_modified_filetime = ctypes.c_ulonglong(1)
    file_size = ctypes.c_ulonglong(1)
    
    for i in range(num_results):
        everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
        everything_dll.Everything_GetResultDateCreated(i, date_created_filetime)
        everything_dll.Everything_GetResultDateModified(i, date_modified_filetime)
        everything_dll.Everything_GetResultSize(i, file_size)
        
        full_path = ctypes.wstring_at(filename)
        file_name = os.path.basename(full_path)
        
        created_time = get_time(date_created_filetime)
        modified_time = get_time(date_modified_filetime)
        
        search_results.append({
            "index": i + 1,
            "path": full_path,
            "filename": file_name,
            "size": file_size.value,
            "date_created": created_time.strftime('%Y-%m-%d %H:%M:%S') if created_time else "未知",
            "date_modified": modified_time.strftime('%Y-%m-%d %H:%M:%S') if modified_time else "未知"
        })
    
    result_message = f"找到 {len(search_results)} 个文件（前10个）：\n\n"
    for result in search_results:
        result_message += f"{result['index']}. {result['filename']}\n   {result['path']}\n\n"
    
    result_message += "使用 `文件 [序号]` 查看文件详情，或 `发送 [序号]` 发送文件。"
    
    return {
        "status": "success",
        "message": result_message
    }

def get_file_info(index):
    global search_results
    
    if not search_results:
        return {
            "status": "error",
            "message": "请先搜索文件。使用 `搜索 [关键词]` 开始搜索。"
        }
    
    if index < 1 or index > len(search_results):
        return {
            "status": "error",
            "message": f"无效的序号，请使用 1 到 {len(search_results)} 之间的数字。"
        }
    
    file_info = search_results[index - 1]
    
    size_str = ""
    if file_info['size'] < 1024:
        size_str = f"{file_info['size']} 字节"
    elif file_info['size'] < 1024 * 1024:
        size_str = f"{file_info['size'] / 1024:.2f} KB"
    elif file_info['size'] < 1024 * 1024 * 1024:
        size_str = f"{file_info['size'] / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{file_info['size'] / (1024 * 1024 * 1024):.2f} GB"
    
    message = f"文件详情：\n\n"
    message += f"文件名：{file_info['filename']}\n"
    message += f"路径：{file_info['path']}\n"
    message += f"大小：{size_str}\n"
    message += f"创建日期：{file_info['date_created']}\n"
    message += f"修改日期：{file_info['date_modified']}\n"
    
    return {
        "status": "success",
        "message": message
    }

def send_file(index):
    global search_results
    
    if not search_results:
        return {
            "status": "error",
            "message": "请先搜索文件。使用 `搜索 [关键词]` 开始搜索。"
        }
    
    if index < 1 or index > len(search_results):
        return {
            "status": "error",
            "message": f"无效的序号，请使用 1 到 {len(search_results)} 之间的数字。"
        }
    
    file_info = search_results[index - 1]
    file_path = file_info['path']
    
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": f"文件不存在：{file_path}"
        }
    
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        file_size = os.path.getsize(file_path)
        
        if file_size > 10 * 1024 * 1024:
            return {
                "status": "error",
                "message": f"文件过大（{file_size / (1024 * 1024):.2f} MB），超过 10 MB 限制。"
            }
        
        return {
            "status": "success",
            "message": f"正在发送文件：{file_info['filename']}",
            "file": {
                "path": file_path,
                "name": file_info['filename'],
                "content": base64.b64encode(file_content).decode('utf-8')
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"发送文件时出错：{str(e)}"
        }

def handle(request):
    message = request.get("message", "").strip()
    
    if message.startswith("搜索 "):
        query = message[3:].strip()
        if not query:
            return {
                "status": "error",
                "message": "请提供搜索关键词，例如：`搜索 report.pdf`"
            }
        return search_files(query)
    
    elif message.startswith("文件 "):
        try:
            index = int(message[3:].strip())
            return get_file_info(index)
        except ValueError:
            return {
                "status": "error",
                "message": "请提供有效的序号，例如：`文件 1`"
            }
    
    elif message.startswith("发送 "):
        try:
            index = int(message[3:].strip())
            return send_file(index)
        except ValueError:
            return {
                "status": "error",
                "message": "请提供有效的序号，例如：`发送 1`"
            }
    
    else:
        return {
            "status": "error",
            "message": "请使用以下命令：\n- `搜索 [关键词]` - 搜索文件\n- `文件 [序号]` - 查看文件详情\n- `发送 [序号]` - 发送文件"
        }

if __name__ == "__main__":
    test_request = {"message": "搜索 openclaw"}
    print(handle(test_request))
