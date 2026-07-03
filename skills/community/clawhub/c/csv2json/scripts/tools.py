from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_csv_info(
    file_path: str
) -> Dict[str, Any]:
    """
    获取 CSV 文件的基本信息，用于辅助转换操作。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    
Returns:
    包含 CSV 文件信息的字典，结构为：
    {
        "success": bool,           # 操作是否成功
        "file_info": Dict[str, Any], # 文件详细信息
        "message": str            # 操作结果消息
    }
    
    文件信息包含以下字段：
    - file_size: 文件大小（字节）
    - row_count: 行数（估算值）
    - column_count: 列数
    - columns: 列名列表
    - sample_data: 示例数据（前几行）
    - file_encoding: 文件编码
    - detected_delimiter: 检测到的分隔符
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或读取失败时
    Exception: 其他未知错误
    
    Args:
        file_path: null
    
    Returns:
        null
    """
    arguments = {
        "file_path": file_path
    }
    
    return call_api("1777419078300675", "get_csv_info", arguments)

def convert_csv_file(
    file_path: str,
    output_file_path: Optional[null] = None,
    delimiter: Optional[str] = ",",
    encoding: Optional[str] = "utf-8",
    skip_rows: Optional[int] = 0.0,
    header: Optional[bool] = True,
    orient: Optional[str] = "records",
    indent: Optional[null] = None
) -> Dict[str, Any]:
    """
    将 CSV 文件转换为 JSON 文件。

Args:
    file_path: CSV 文件路径，必须是有效的文件路径
    output_file_path: 输出 JSON 文件路径（可选，默认为 CSV 文件同目录下同名 .json 文件）
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    encoding: 文件编码，默认为 utf-8，支持 gbk、gb2312 等常见编码
    skip_rows: 跳过的行数，默认为 0，用于跳过文件开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,      # 转换是否成功
        "json_file_path": str, # 生成的 JSON 文件路径
        "message": str       # 操作结果消息
    }
    
Raises:
    FileNotFoundError: 当文件路径不存在时
    ValueError: 当文件格式错误或转换失败时
    Exception: 其他未知错误
    
    Args:
        file_path: null
        output_file_path: null
        delimiter: null
        encoding: null
        skip_rows: null
        header: null
        orient: null
        indent: null
    
    Returns:
        null
    """
    arguments = {
        "file_path": file_path,
        "output_file_path": output_file_path,
        "delimiter": delimiter,
        "encoding": encoding,
        "skip_rows": skip_rows,
        "header": header,
        "orient": orient,
        "indent": indent
    }
    
    return call_api("1777419078300675", "convert_csv_file", arguments)

def convert_csv_string(
    csv_content: str,
    delimiter: Optional[str] = ",",
    skip_rows: Optional[int] = 0.0,
    header: Optional[bool] = True,
    orient: Optional[str] = "records",
    indent: Optional[null] = None
) -> Dict[str, Any]:
    """
    将 CSV 格式的字符串转换为 JSON 格式。

Args:
    csv_content: CSV 格式的字符串内容，必须包含有效的 CSV 数据
    delimiter: CSV 分隔符，默认为逗号(,)，可以是制表符(     )、分号(;)等
    skip_rows: 跳过的行数，默认为 0，用于跳过字符串开头的注释或空行
    header: 是否包含表头，默认为 True，如果为 False 则使用列索引作为键名
    orient: JSON 输出格式，默认为 "records"，可选值：
        - "records": 每行作为一个字典对象的列表
        - "values": 仅包含值的二维数组
        - "index": 包含索引的字典
        - "table": 包含 schema 和数据的完整表格格式
        - "split": 分开存储列名和数据的格式
    indent: JSON 缩进，默认为 None（紧凑格式），可设置为 2 或 4 等值
    
Returns:
    包含转换结果的字典，结构为：
    {
        "success": bool,  # 转换是否成功
        "json": Any,      # 转换后的 JSON 数据
        "message": str    # 操作结果消息
    }
    
Raises:
    ValueError: 当字符串格式错误或转换失败时
    Exception: 其他未知错误
    
    Args:
        csv_content: null
        delimiter: null
        skip_rows: null
        header: null
        orient: null
        indent: null
    
    Returns:
        null
    """
    arguments = {
        "csv_content": csv_content,
        "delimiter": delimiter,
        "skip_rows": skip_rows,
        "header": header,
        "orient": orient,
        "indent": indent
    }
    
    return call_api("1777419078300675", "convert_csv_string", arguments)

