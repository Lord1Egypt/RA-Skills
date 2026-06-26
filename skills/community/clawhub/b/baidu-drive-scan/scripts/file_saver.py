import base64
import os
import uuid

def save_base64_image(base64_str: str) -> str:
    try:
        data = base64.b64decode(base64_str)
        tmp_dir = "/tmp"
        os.makedirs(tmp_dir, exist_ok=True)
        filename = f"scan_{uuid.uuid4().hex[:8]}.png"
        path = os.path.join(tmp_dir, filename)
        with open(path, "wb") as f:
            f.write(data)
        return path
    except:
        return ""
    

def image_bytes_to_data_url(image_bytes: bytes, content_type: str = "image/jpeg") -> str:
    """
    将图片二进制转为data URL
    :param image_bytes: 图片二进制
    :param content_type: 图片类型（image/jpeg、image/png等）
    :return: data URL
    """
    b64_str = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{content_type};base64,{b64_str}"