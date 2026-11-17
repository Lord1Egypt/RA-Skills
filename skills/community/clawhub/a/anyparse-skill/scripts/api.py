import os
import sys
import json
import traceback
import argparse
from pathlib import Path
try:
    import requests as rq
except ImportError:
    print(
        "Error: Missing dependency 'requests'. Install with: pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(2)
    

def read_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)
    
    
rootpath = Path(__file__).parent.absolute()
configfile = rootpath.joinpath("config.json")
config = read_json(configfile)
anyparse_api_url = config.get('anyparse_api_url')
anyparse_api_key = config.get('anyparse_api_key')
if os.environ.get('anyparse_api_url'):
    anyparse_api_url = os.environ.get('anyparse_api_url')
if os.environ.get('anyparse_api_key'):
    anyparse_api_key = os.environ.get('anyparse_api_key')

def extract(
    file: str,
    use_doc_cls: bool = False,
    use_doc_rectifier: bool = False,
    use_doc_layout: bool = True,  
):
    """
    Extract content from file
    
    Args:
        file (str): File path, allow file type: [pdf,docx,pptx,jpeg,jpg,png,txt,md,html,xhtml,csv,xls,xlsx,epub,ipynb]
        use_doc_cls (bool, optional): Use document classification. Defaults to False.
        use_doc_rectifier (bool, optional): Use document rectifier, Defaults to False.
        use_doc_layout (bool, optional): Use document layout. Defaults to True.
        
    Returns:
        {
            'code': 2000, # 接口状态码，2000则是成功
            'data': {
                'metadata': { # 文件信息
                    'file_md5': 'f484351567161df1e5e4d9d4b861c594',# 文件md5
                    'file_type': 'jpg', # 文件类型
                    'file_name': 'WechatIMG554.jpg', # 文件名
                    'file_size': '8.10/KB' # 文件大小
                },
               'pages': [ # 页面信息
                   {
                       'id': 1,  # 页码
                        'content': '$10^{9}/L$', # 单个页面的解析内容
                        'layout': [         # 单个页面布局信息
                            {
                                'order_id': 0, # 阅读顺序
                                'label_name': 'text', # 标签名称
                                'box': [0, 0, 196, 80], # layout box:[x1, y1, x2, y2]
                                'task': 'text', # 任务类型
                                'parse_text': '$10^{9}/L$' # 解析内容
                            }
                        ],
                        'elapse_times': 1.9343271255493164 # 单个页面的耗时
                    }
                ],
                'content': '$10^{9}/L$', # 整个文件的解析内容
                'elapse_times': 1.9524128437042236 # 整个文件的耗时
            },
            'msg': 'success' # 接口状态信息
        }
    """
    try:
        if not anyparse_api_url:
            raise Exception("Please set anyparse_api_url in config.json, or set it in environment variable: anyparse_api_url")
        if not anyparse_api_key:
            raise Exception("Please set anyparse_api_key in config.json, or set it in environment variable: anyparse_api_key")
        filepath = Path(file).resolve().absolute()
        if not filepath.exists():
            raise Exception(f"File {filepath} not exists")
        headers = {
            "Authorization": f"Bearer {anyparse_api_key}"
        }

        url = f"{anyparse_api_url}"

        args = {
            "use_doc_cls": use_doc_cls,
            "use_doc_rectifier": use_doc_rectifier,
            "use_doc_layout": use_doc_layout,
        }

        files = {
            'file': open(f"{filepath}",'rb')
        }

        res = rq.post(url, files = files, data = args, headers = headers)
        return res.json()    
    except Exception as e:
        return {
            "code": 5000,
            "msg": traceback.format_exc(),
            "data": {}
        }
    

def main():
    parser = argparse.ArgumentParser(
        description="AnyParse - Extract content from file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from local file and default only use document layout
  python scripts/api.py --file /path/to/image.jpg
  
  # Extract from local file use document orientation classification and layout
  python scripts/api.py --file /path/to/image.jpg --use_doc_cls
  
  # Extract from local file use document rectifier and layout
  python scripts/api.py --file /path/to/image.jpg --use_doc_rectifier
  
  # Extract from local file and not use document layout
  python scripts/api.py --file /path/to/image.jpg --no_doc_layout
        """,
    )

    # Input (one of --file-url or --file required)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", help="Path to local file")

    # Output options
    parser.add_argument(
        "--use_doc_cls", action="store_true", help="use document orientation classification"
    )
    parser.add_argument(
        "--use_doc_rectifier", action="store_true", help="use document rectifier"
    )    
    parser.add_argument(
        "--no_doc_layout", action="store_true", help="not use document layout"
    )

    args = parser.parse_args()    
    res = extract(
        file = args.file,
        use_doc_cls = args.use_doc_cls,
        use_doc_rectifier = args.use_doc_rectifier,
        use_doc_layout = not args.no_doc_layout
    )
    print(json.dumps(res, indent=4, ensure_ascii=False))
    return
    
    
if __name__ == "__main__":
    main()