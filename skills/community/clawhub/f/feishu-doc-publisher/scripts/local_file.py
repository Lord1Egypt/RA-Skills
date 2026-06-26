import os
import mimetypes

def resolve_path(file_path):
    if os.path.isabs(file_path):
        return file_path
    return os.path.abspath(os.path.join(os.getcwd(), file_path))

def infer_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.png': return 'image/png'
        if ext == '.gif': return 'image/gif'
        if ext == '.webp': return 'image/webp'
        return 'image/jpeg'
    return mime_type

def file_exists(file_path):
    return os.path.exists(resolve_path(file_path))

def read_markdown_content(file_path):
    with open(resolve_path(file_path), 'r', encoding='utf-8') as f:
        return f.read()

def read_binary_file_info(file_path):
    resolved = resolve_path(file_path)
    file_name = os.path.basename(resolved)
    size = os.path.getsize(resolved)
    mime_type = infer_mime_type(resolved)
    
    return {
        'path': resolved,
        'fileName': file_name,
        'mimeType': mime_type,
        'size': size
    }
